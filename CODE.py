import os
import sys

from PyQt5.QtCore import Qt, QSize, QUrl
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtPrintSupport import QPrintPreviewDialog
from PyQt5.QtWidgets import (QDialog, QDialogButtonBox, QVBoxLayout,
                             QLabel, QMainWindow, QStatusBar, QToolBar,
                             QAction, QLineEdit, QFileDialog, QApplication)

import json
import requests
import ibm_watson
from pandas import DataFrame


import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
# uncomment below line if punkt not present
# nltk.download('punkt')
stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

try:
    from nltk.corpus import stopwords
except Exception as e:
    print(e)
    nltk.download('stopwords')

# Stack Apps API key
Auth_key = "rEi)4Xt7RnJf4tqP)pk5nQ(("


# All the 55000 stack overflow tags stored in value_list  to be used by remove_nonsotag function
with open('SO_tags_dict_2.txt', 'r') as f:
    value_list = json.load(f)
f.close()


def watson_nlu(text_test_eta):
    """
    IBM WATSON NLU API
    :param text_test_eta: String of text
    :return: Non stackoverflow tags based on the custom model trained on watson knowledge studio
    """
    from ibm_watson import NaturalLanguageUnderstandingV1
    from ibm_watson.natural_language_understanding_v1 import Features,KeywordsOptions ,SyntaxOptions, SyntaxOptionsTokens,SentimentOptions,EntitiesOptions

    credentials = {"api_key": "wEHseKE5Iqv2PfZwtOP6FVQYOeoJxIa-32Xu5QbNkBRM",
                   "api_url": "https://gateway.watsonplatform.net/natural-language-understanding/api",
                   "model":"9ccb4de2-2bf1-410a-8d51-36f77f9cf907"
                  }


    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2018-11-16',
        iam_apikey=credentials['api_key'],
        url=credentials['api_url']
    )
    response_eta = natural_language_understanding.analyze(
        text=text_test_eta,
        features=Features(entities=EntitiesOptions(limit=1,model=credentials['model']))).get_result()
#     print(response_eta['usage'])
    return response_eta


def badge_reputation(dict_eta):
    """
    Simple function to calculate badge reputation of a user
    :param dict_eta: dictionary of badges the user have earned
    :return: a float value perfectly representing the badge reputation
    """
    if "badge_counts" in dict_eta:
        alpha = 0.3
        beta = 0.5
        gamma = 0.9
        badge_repu = 0
        dict_eta_2 = dict_eta['badge_counts']
        if 'bronze' in dict_eta_2:
            badge_repu+=alpha*dict_eta_2['bronze']
        if 'silver' in dict_eta_2:
            badge_repu+=beta*dict_eta_2['silver']
        if 'gold' in dict_eta_2:
            badge_repu+=gamma*dict_eta_2['gold']
        return badge_repu
    else:
        return 0


def top_answers_fun(q_id_eta):
    """
    Finds most appropriate answers based on user's reputation and answer's score and acceptance
    :param q_id_eta: ID of the question in stackoverflow database
    :return: returns top relevant answers of that question
    """
    # parameters
    delta = 0.5
    epsilon = 0.5
    zeta = 0.5
    url_eta = "https://api.stackexchange.com/2.2/questions/"+q_id_eta+"/answers?key="+Auth_key+"&order=desc&sort=votes&site=stackoverflow&filter=!)Q7ohwN5q2ex6NuB-d**q(*C"
    top_answers = requests.get(url_eta)
    top_answers = top_answers.json()
    df_ans = DataFrame(top_answers['items'])
#     print(df_ans)
    df_ans['badge_reputation'] = df_ans.apply(lambda row:badge_reputation(row.owner) , axis = 1)
    df_ans['repu'] = df_ans.apply(lambda row:row.owner['reputation'],axis=1)
    df_ans['final_function'] = df_ans.apply(lambda row:delta*row.badge_reputation+epsilon*row.repu+zeta*row.score,axis=1)
    df_ans = df_ans.sort_values(by = ["final_function"],ascending = False)
    eta = df_ans.iloc[0]['final_function']
    df_ans['final_function_2'] = df_ans.apply(lambda row:row.final_function+eta*int(row.is_accepted),axis=1)
    del df_ans['owner']
    type_a = list(df_ans['share_link'])
    return type_a


def remove_nonsotag(words_list_eta):
    """
    To remove unnecssary tag from the previous generated tags.
    :param words_list_eta: Take a list of words.
    :return: Returns a list of words with non stackoverflow tags removed
    """
    for i in words_list_eta:
        if i not in value_list:
            words_list_eta.remove(i)
    local_list_eta = set(words_list_eta)
    return local_list_eta


def remove_stopwords(words_list_eta):
    """
    To remove the stopwords like I,am,the from the user query which are of no use.
    :param words_list_eta: Take a list of words
    :return: Returns a list of word with stopwords removed
    """
    stop_words = stopwords.words('english')
    return [word for word in words_list_eta if word not in stop_words]


def watson_assistantv1(query_eta):
    """
    Watson assistant api
    :param query_eta: A string from which stackoverflow tags will be mined by the watson Assistant
    :return: Returns a list of tags with their relevance factor in a dictionary
    """
    credentials_moh = {"api_key": "HTHsjdKJzDGeQlHu_uJijwKbb48__vZbypti5MVchZL7",
                       "api_url": "https://gateway.watsonplatform.net/assistant/api",
                       "workspace_id": "f2d82aa9-b6a3-4657-a6eb-01ff1cfec5a8"}

    assistant2 = ibm_watson.AssistantV1(
        version='2019-02-28',
        url=credentials_moh['api_url'],
        iam_apikey=credentials_moh['api_key']
    )
    response2 = assistant2.message(
        workspace_id=credentials_moh['workspace_id'],
        input = {'text': query_eta}
    ).get_result()

    tags2 = {}
    for i in response2['entities']:
        if i['entity'] == 'Stack_Overflow_Tag':
            if i['confidence'] > 0.8:
                tags2[i['value']] = i['confidence']
    if len(tags2) >= 1:
        return tags2


def most_relevant_tags(query_eta):
    """
    This function calculates most relevant tags from a query using watson assistant and local implementation
    :param query_eta: Takes a string as input
    :return: List of words which are most relevant tags from that query
    """
    assistant_list = set(watson_assistantv1(query_eta))
    local_list = set(remove_nonsotag(remove_stopwords(query_eta.split())))
    final_list_eta = assistant_list.union(local_list)
#     print("local_list is ",local_list,"assistant_list is",assistant_list)
    return final_list_eta


def remove_error_tags(query_eta,final_list_eta):
    """
    Removes error tags by semantic analysis
    :param query_eta: Question asked by the user
    :param final_list_eta: list of tags before removing the error tags
    :return: list of tags after removing the error tags
    """
    response = watson_nlu(query_eta)
    error_tag = []
    for tag in response['entities']:
        try:
            if tag['type']== 'NO_SO_TAG':
                deviated_version = watson_assistantv1(tag['text'])
                print("Removing",deviated_version," from tags as it is not in context")
                for item in deviated_version:
                    error_tag.append(item)
        except Exception as e:
            print(e)
    final_list_changed = set(final_list_eta).difference(error_tag)
    return list(final_list_changed)


def stem_tokens(tokens):
    """
    :param tokens: List of tokens
    :return: A list of stemmed words of the tokens
    """
    return [stemmer.stem(item) for item in tokens]


def normalize(text):
    """
    :param text: String to be normalised
    :return: Normalised string with punctuations removed
    """
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))


vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')


def cosine_sim(text1, text2):
    """
    Function to check how much are 2 strings similar
    :param text1: String 1 will be title of questions returned by api
    :param text2: String 2 will be title of the query by user
    :return: An float value representing how similar are the 2 sentences
    """
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0, 1]


class Answers:
    def __init__(self, query):
        self.query = query
        self.answer_urls = []
        self.cur_ans_idx = -1
        self.generate_answer_links()
        self.default = 'https://www.stackoverflow.com'

    def generate_answer_links(self):
        """
        Returns a list of StackOverflow question URLs.
        :param query: Question entered by the user.
        :return: List
        """
        urls = []
        try:
            final_list = most_relevant_tags(self.query)
            print(final_list)

            final_list = remove_error_tags(self.query, final_list)
            print(final_list)
            api_url_1 = "https://api.stackexchange.com/2.2/similar?key=" + Auth_key + "&order=desc&sort=relevance&tagged=" + ";".join(
                final_list) + "&title="
            api_url_2 = self.query + "&site=stackoverflow"
            api_url = api_url_1 + api_url_2

            top_relevant_questions = requests.get(api_url)
            top_relevant_questions = top_relevant_questions.json()
            df = DataFrame(top_relevant_questions['items'])
        except Exception as e:
            print(e)

        print(" NO of Questions fetch by the STACK APPS API = ",len(df))
        # PHASE 1
        try:
            print("Removing Questions which are closed")
            df = df[df.closed_reason != 'duplicate']
            df = df[df.closed_reason != 'off-topic']
            df = df[df.closed_reason != "unclear what you're asking"]
            df = df[df.closed_reason != "too broad"]
            df = df[df.closed_reason != "primarily opinion-based"]
            print("Removing Questions which are not answered")
            df = df[df.is_answered]
            print("Removing Quesitons with negative scores")
            df = df[df.score>0]
            print("NO of Questions left after PHASE 1 ARE  = ", len(df))
        except Exception as e:
            print(e)

        # PHASE 2
        print("Creating extra features to sort the questions which are returned by the api")
        print("Using Watson for", len(df), "times on the questions after phase 1")
        try:
            df['Tag_Match'] = df.apply(lambda row: len(set(row.tags).intersection(final_list)), axis=1)
            df['Similarity_index'] = df.apply(lambda row: cosine_sim(row.title, self.query), axis=1)
            df['keyword_in_title'] = df.apply(lambda row: most_relevant_tags(row.title), axis=1)
            df['Keywords_Match'] = df.apply(lambda row: len(set(row.keyword_in_title).intersection(final_list)), axis=1)
            alpha = 0.5
            beta = 1.5
            gamma = 1.2
            df['Final_function'] = df.apply(
                lambda row: (alpha * row.Tag_Match) + (beta * row.Similarity_index) + (gamma * row.Keywords_Match), axis=1)
            df = df.sort_values(by=["Final_function"], ascending=False)
        except Exception as e:
            print(e)

        print("NO of Quesitons choosen after PHASE 2 are 5")
        print("All done!")
        print("Now deciding which answers are the best one!!")
        try:
            question_dict = {}
            for i in range(5):
                print(df.iloc[i].title)
                # print(df.iloc[i].link)
                question_dict[df.iloc[i].question_id] = df.iloc[i].title

            for q_id in question_dict:
                print(question_dict[q_id])
                for ans in top_answers_fun(str(q_id)):
                    urls.append(ans)
        except Exception as e:
            print(e)


        self.answer_urls.extend(urls)
        return self.answer_urls

    def get_next(self):
        self.cur_ans_idx += 1
        if self.cur_ans_idx == len(self.answer_urls):
            self.cur_ans_idx = 0
        try:
            return self.answer_urls[self.cur_ans_idx]
        except IndexError:
            return self.default

    def get_prev(self):
        self.cur_ans_idx -= 1
        if self.cur_ans_idx < 0:
            self.cur_ans_idx = 0
        try:
            return self.answer_urls[self.cur_ans_idx]
        except IndexError:
            return self.default


class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        QBtn = QDialogButtonBox.Ok  # No cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title = QLabel("CRIO")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        layout.addWidget(title)

        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join('images', 'ma-icon-128.png')))
        layout.addWidget(logo)

        layout.addWidget(QLabel("Copyright 2019 CRIO"))

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.stackoverflow.com"))

        self.browser.urlChanged.connect(self.update_urlbar)
        self.browser.loadFinished.connect(self.update_title)

        self.setCentralWidget(self.browser)
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        #####################################################
        navtb2 = QToolBar()
        navtb2.setIconSize(QSize(16, 16))
        navtb2.setFixedHeight(50)
        navtb2.setIconSize(QSize(60, 60))

        self.query_bar = QLineEdit(self)
        self.query_bar.setFixedHeight(45)
        f = self.query_bar.font()
        f.setPointSize(20)  # sets the size to 27
        self.query_bar.setFont(f)
        self.query_bar.setPlaceholderText("Powered by IBM Cloud...")
        self.query_bar.returnPressed.connect(self.process_query)
        navtb2.addWidget(self.query_bar)

        self.back_btn = QAction(QIcon(os.path.join('images', 'arrow-180.png')), "Previous Answer", self)
        self.back_btn.setStatusTip("Back to previous page")
        self.back_btn.triggered.connect(self.prev_answer)
        self.back_btn.setDisabled(True)
        navtb2.addAction(self.back_btn)

        self.next_btn = QAction(QIcon(os.path.join('images', 'arrow-000.png')), "Next Answer", self)
        self.next_btn.setStatusTip("Forward to next page")
        self.next_btn.triggered.connect(self.next_answer)
        self.next_btn.setDisabled(True)
        navtb2.addAction(self.next_btn)

        self.addToolBar(navtb2)
        self.addToolBarBreak()
        #####################################################

        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(16, 16))
        self.addToolBar(navtb)

        reload_btn = QAction(QIcon(os.path.join('images', 'arrow-circle-315.png')), "Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)

        home_btn = QAction(QIcon(os.path.join('images', 'home.png')), "Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        self.httpsicon = QLabel()  # Yes, really!
        self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-nossl.png')))
        navtb.addWidget(self.httpsicon)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        stop_btn = QAction(QIcon(os.path.join('images', 'cross-circle.png')), "Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(self.browser.stop)
        navtb.addAction(stop_btn)

        # Uncomment to disable native menubar on Mac
        # self.menuBar().setNativeMenuBar(False)

        file_menu = self.menuBar().addMenu("&File")

        open_file_action = QAction(QIcon(os.path.join('images', 'disk--arrow.png')), "Open file...", self)
        open_file_action.setStatusTip("Open from file")
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        save_file_action = QAction(QIcon(os.path.join('images', 'disk--pencil.png')), "Save Page As...", self)
        save_file_action.setStatusTip("Save current page to file")
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)

        print_action = QAction(QIcon(os.path.join('images', 'printer.png')), "Print...", self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.print_page)
        file_menu.addAction(print_action)

        help_menu = self.menuBar().addMenu("&Help")

        about_action = QAction(QIcon(os.path.join('images', 'question.png')), "About CRIO", self)
        about_action.setStatusTip("Find out more about CRIO")  # Hungry!
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

        navigate_mozarella_action = QAction(QIcon(os.path.join('images', 'lifebuoy.png')), "CRIO Homepage", self)
        navigate_mozarella_action.setStatusTip("Go to CRIO Homepage")
        navigate_mozarella_action.triggered.connect(self.navigate_mozarella)
        help_menu.addAction(navigate_mozarella_action)

        self.show()

        self.setWindowIcon(QIcon(os.path.join('images', 'ma-icon-64.png')))

    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle("%s - CRIO" % title)

    def navigate_mozarella(self):
        self.browser.setUrl(QUrl("https://github.com/fivecube/CRIO"))

    def about(self):
        dlg = AboutDialog()
        dlg.exec_()

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                                  "Hypertext Markup Language (*.htm *.html);;"
                                                  "All files (*.*)")

        if filename:
            with open(filename, 'r') as f:
                html = f.read()

            self.browser.setHtml(html)
            self.urlbar.setText(filename)

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Page As", "",
                                                  "Hypertext Markup Language (*.htm *html);;"
                                                  "All files (*.*)")

        if filename:
            html = self.browser.page().toHtml()
            with open(filename, 'w') as f:
                f.write(html)

    def print_page(self):
        dlg = QPrintPreviewDialog()
        dlg.paintRequested.connect(self.browser.print_)
        dlg.exec_()

    def navigate_home(self):
        self.browser.setUrl(QUrl("http://www.stackoverflow.com"))

    def navigate_to_url(self):  # Does not receive the Url
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.browser.setUrl(q)

    def update_urlbar(self, q):

        if q.scheme() == 'https':
            # Secure padlock icon
            self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-ssl.png')))
        else:
            # Insecure padlock icon
            self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-nossl.png')))

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def process_query(self):
        q = self.query_bar.text().strip()
        if q.startswith('http:') or q.startswith('https:'):
            self.browser.setUrl(QUrl(q))
        else:
            self.answers = Answers(q)
            self.next_btn.setDisabled(False)
            self.back_btn.setDisabled(False)
            self.next_answer()

    def next_answer(self):
        ans = self.answers.get_next()
        self.browser.setUrl(QUrl(ans))

    def prev_answer(self):
        ans = self.answers.get_prev()
        self.browser.setUrl(QUrl(ans))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("CRIO")
    app.setOrganizationName("CRIO")
    app.setOrganizationDomain("https://github.com/fivecube/CRIO")

    window = MainWindow()

    app.exec_()

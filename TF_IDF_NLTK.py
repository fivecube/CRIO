import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
nltk.download('punkt')
stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

try:
    from nltk.corpus import stopwords
except Exception as e:
    print(e)
    nltk.download('stopwords')


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


def remove_stopwords(words_list_eta):
    """
    To remove the stopwords like I,am,the from the user query which are of no use.
    :param words_list_eta: Take a list of words
    :return: Returns a list of word with stopwords removed
    """
    stop_words = stopwords.words('english')
    return [word for word in words_list_eta if word not in stop_words]
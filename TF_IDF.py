import spacy
import warnings
warnings.filterwarnings("ignore")


nlp = spacy.load('en_core_web_sm')
# nlp = spacy.load('en_core_web_md')


def cosine_sim(text1, text2):
    """
    Function to check how much are 2 strings similar
    :param text1: String 1 will be title of questions returned by api
    :param text2: String 2 will be title of the query by user
    :return: An float value representing how similar are the 2 sentences
    """
    doc1 = nlp(text1)
    doc2 = nlp(text2)
    return doc1.similarity(doc2)


# t = "how to find all the keys of a dictionary in python"
# t2 = "ways to find the keys of a dictionary in python"
# t3 = "How to return dictionary keys as a list in Python?"
#
# print(cosine_sim(t, t2))
# print(cosine_sim(t, t3))
# print(cosine_sim(t3, t2))

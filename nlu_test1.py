import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, CategoriesOptions

credentials = {"api_key": "FQIQwKhvfCy1pjNJqOZ6ZH3M8YZI6on5t8Hr0Eyumep2",
               "api_url": "https://gateway.watsonplatform.net/natural-language-understanding/api"}


natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-11-16',
    iam_apikey=credentials['api_key'],
    url=credentials['api_url']
)

# text_test = "Sharukh khan is richest actor"
text_test = "Node -how to run node app.js?"

response = natural_language_understanding.analyze(
    text=text_test,
    features=Features(categories=CategoriesOptions())).get_result()

print(json.dumps(response, indent=2))

from __future__ import print_function
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, ConceptsOptions
from ibm_watson.natural_language_understanding_v1 import Features, CategoriesOptions, SentimentOptions, EntitiesOptions, KeywordsOptions, RelationsOptions, SemanticRolesOptions

# If service instance provides API key authentication
service = NaturalLanguageUnderstandingV1(
    version='2018-03-16',
    #url is optional, and defaults to the URL below. Use the correct URL for your region.
    url='https://gateway-lon.watsonplatform.net/natural-language-understanding/api',
    iam_apikey='DjnYxF9OlNtL4QoNJEqM0i2mBp_fhFXO9_65OVLn7oSw')

# service = NaturalLanguageUnderstandingV1(
#     version='2018-03-16',
#     ## url is optional, and defaults to the URL below. Use the correct URL for your region.
#     # url='https://gateway.watsonplatform.net/natural-language-understanding/api',
#     username='YOUR SERVICE USERNAME',
#     password='YOUR SERVICE PASSWORD')

response = service.analyze(
	text='Node  how to run   app.js?',
	#url='https://t.justdial.com/Jaipur/Heart-Doctors/nct-10080172?fl=undefined&ismap=undefined&searchCase=&stype=category_list',
	#url = 'www.ibm.com',
    features=Features(entities=EntitiesOptions(),
                      keywords=KeywordsOptions(),
					  concepts=ConceptsOptions(limit=3),
					  relations=RelationsOptions(),
					  semantic_roles=SemanticRolesOptions(),
					  sentiment=SentimentOptions(),
					  categories=CategoriesOptions(limit=3)
					  
					  )).get_result()

print(json.dumps(response, indent=2))

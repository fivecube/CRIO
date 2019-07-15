import ibm_watson

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

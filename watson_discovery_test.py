import json
from ibm_watson import DiscoveryV1

credential = {"api_key": "uA8E4SB4iJrtzLqJfI6_yjoJaTL7jmEk9W5l476VXX5v",
               "api_url": "https://gateway.watsonplatform.net/discovery/api"}


discovery = DiscoveryV1(
    version="2019-04-30",
    iam_apikey=credential['api_key'],
    url=credential['api_url']
)

# response = discovery.create_environment(
#     name="my_environment",
#     description="My environment"
# ).get_result()
#
# print(json.dumps(response, indent=2))

environments = discovery.list_environments().get_result()

# print(environments)
print("Environments related to this account are :-")
for i in range(len(environments['environments'])):
    print(i+1, ")", environments['environments'][i]['name'], "with id as -->",environments['environments'][i]['environment_id'])

# print(discovery.get_environment(environments['environments'][1]['environment_id']))

import requests
import json

# headers = {
#     'Content-Type': 'application/json',
# }
#
# json_data = {
#     'action': 'INCREASE_HEALTH_WORRY',
# }
#
# requests.post('http://localhost:8081/performAction', headers=headers, json=json_data)
#
# question = json.loads(requests.get('http://localhost:8081/getQuestion').text)
# print(question)
# options = zip(question['optionLabels'], question['optionActions'])
# print(list(options))

l = json.loads(requests.get('http://localhost:8081/'+'getUnvisitedNodes').text)
print(len(l))



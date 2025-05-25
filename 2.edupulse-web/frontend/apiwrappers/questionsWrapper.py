import requests
from .commons import jwt_required, verify_jwt_token
from .appConfig import appConfig

config = appConfig()
questionsServiceUrl = config.questions_service_url

# l-ocalService = False
# if localService:
#     questionsServiceUrl = "http://localhost:9117/"

import os
questionsServiceUrl = os.environ.get('qsvc',questionsServiceUrl)

headers = {'Content-Type': 'application/json'}

# def get_webservice(url: str, params: dict = None, headers: dict = None) -> requests.Response:
#     try:
#         response = requests.get(url, params=params, headers=headers)
#         response.raise_for_status()  # Raise an exception for HTTP errors
#         return response
#     except requests.exceptions.RequestException as err:
#         print(f"Request Exception: {err}")
#         return None
@jwt_required 
def get_user_questions_metadata(user_id: str,hdrs={},** kwargs) -> requests.Response:
    api="userQuestions/"
    response = requests.get(questionsServiceUrl+api, headers=hdrs, params={"userid": user_id})
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json() 

# def get_topics_metadata(user_id: str=None) -> requests.Response:
#     try:
#         print("get_topics_metadata:",user_id)
#         if user_id:
#             api="usertopicsMetadata/"
#             response = requests.get(questionsServiceUrl+api, headers=headers, params={"userid": user_id})
#             response.raise_for_status()  # Raise an exception for HTTP errors
#             data=response.json()
#             if "_id" in data:
#                 data.pop("_id")

#             #print("apiResponse:",data)
#             return data
#         else:
#             api="topicsMetadata/"
#             response = requests.get(questionsServiceUrl+api, headers=headers)
#             response.raise_for_status()  # Raise an exception for HTTP errors
#             data=response.json()
#             return data
#         #below code might be deleted after testing
#         ret={}
#         for subject in data:
#             #print("Subject:",subject)
#             ret[subject["_id"]]=subject
#             ret[subject["_id"]].pop("_id")
#         return ret
#     except requests.exceptions.RequestException as err:
#         print(f"Request Exception: {err}")
#         return None

@jwt_required 
def save_selected_topics(user_id: str=None,selected_topics: dict=None,hdrs={},** kwargs) -> dict:
    try:
        api=f"usertopicsMetadata/" 
        params = {"userid": user_id}
        response = requests.post(questionsServiceUrl + api, headers=hdrs, params=params, json=selected_topics)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data=response.json()
        #print("apiResponse:",data)
        return response
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")
        return None
    
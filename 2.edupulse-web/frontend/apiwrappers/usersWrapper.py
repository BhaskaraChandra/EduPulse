from pydantic import BaseModel
import requests

questionsServiceUrl = "https://edupulsesvc.onrender.com/"
userssServiceUrl = "https://edupulsesvc.onrender.com/"

localService = False
if localService:
    questionsServiceUrl = "http://localhost:9117/"
    userssServiceUrl = "http://localhost:9117/"

import os
questionsServiceUrl = os.environ.get('qsvc',questionsServiceUrl)
userssServiceUrl = os.environ.get('usvc',userssServiceUrl)

headers = {'Content-Type': 'application/json'}

def authenticate_user(username, password):
    api="users/authenticate"
    response = requests.post(userssServiceUrl+api, headers=headers, json={"userEmail": username, "password": password})
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()
def createTenant(tenantName):
    api="tenants/"
    response = requests.post(userssServiceUrl+api, headers=headers, json={"tenantName": tenantName})
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def getTenants():
    api="tenants/"
    response = requests.get(userssServiceUrl+api, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json() 

class User(BaseModel):
    userEmail: str
    userName: str
    userGrade: str =""
    userLevel: str = ""
    profilePic: str = ""
    userGroup: str = ""
    userType: str
    tenantName: str
    password: str = ""

def createUser(username, email, hashed_password, tenantName, userType):
    userObj = User(userEmail=email, userName=username, password=hashed_password, tenantName=tenantName, userType=userType)
    api="users/"
    print("Dbg: Createuser api about to be called ")
    response = requests.post(userssServiceUrl+api, headers=headers, json=userObj.model_dump())
    response.raise_for_status()  # Raise an exception for HTTP errors
    print("Createuser Response:",response.json())
    return response.json()
    pass

def addTenantAdmin(username, email, hashed_password, tenantName) :
    return createUser(username, email, hashed_password, tenantName,"tenantadmin")
    pass

def getUsersForTenantAdmin(adminUser_id):
    api="users/"
    #api = f"users/{adminUser_id}"
    response = requests.get(userssServiceUrl+api, headers=headers,params={"tenant_admin_email": adminUser_id})
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json() 

    pass
#############################################################################################
# All The Below can be deleted after integrating and testing with the new users service wrapper

def get_user_questions_metadata(user_id: str) -> requests.Response:
    api="userQuestions/"
    response = requests.get(questionsServiceUrl+api, headers=headers, params={"userid": user_id})
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json() 

def get_topics_metadata(user_id: str=None) -> requests.Response:
    try:
        print("get_topics_metadata:",user_id)
        if user_id:
            api="usertopicsMetadata/"
            response = requests.get(questionsServiceUrl+api, headers=headers, params={"userid": user_id})
            response.raise_for_status()  # Raise an exception for HTTP errors
            data=response.json()
            if "_id" in data:
                data.pop("_id")

            #print("apiResponse:",data)
            return data
        else:
            api="topicsMetadata/"
            response = requests.get(questionsServiceUrl+api, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data=response.json()
            return data
        #below code might be deleted after testing
        ret={}
        for subject in data:
            #print("Subject:",subject)
            ret[subject["_id"]]=subject
            ret[subject["_id"]].pop("_id")
        return ret
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")
        return None
def save_selected_topics(user_id: str=None,selected_topics: dict=None) -> dict:
    try:
        api=f"usertopicsMetadata/" #{user_id}"
        #print("submitquicktest:",quickTestConfig)
        params = {"userid": user_id}
        response = requests.post(questionsServiceUrl + api, headers=headers, params=params, json=selected_topics)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data=response.json()
        #print("apiResponse:",data)
        return response
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")
        return None
    
from pydantic import BaseModel
import requests

from .appConfig import appConfig
config = appConfig()

questionsServiceUrl = config.questions_service_url
userssServiceUrl = config.users_service_url

# l-ocalService = False
# if localService:
#     questionsServiceUrl = "http://localhost:9117/"
#     userssServiceUrl = "http://localhost:9117/"

import os
questionsServiceUrl = os.environ.get('qsvc',questionsServiceUrl)
userssServiceUrl = os.environ.get('usvc',userssServiceUrl)

headers = {'Content-Type': 'application/json'}
    
def authenticate_userV2(username, password):
    api="users/authenticateV2"
    #hitTest()
    print("calling authenticate_userv2:",userssServiceUrl+api)
    try:
        response = requests.post(userssServiceUrl+api, headers=headers, json={"userEmail": username, "password": password},timeout=10)
        print("response:",response.json())
        if response.status_code == 200:
            jwt = response.json()
            user = jwt #verify_jwt_token(jwt)
            if user:
                return user,jwt
            else:
                return None,None
        else:
            return None,None
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None,None
    

def authenticate_user(username, password):
    api="users/authenticate"
    print("calling authenticate_userv2:",userssServiceUrl+api)
    response = requests.post(userssServiceUrl+api, headers=headers, json={"userEmail": username, "password": password})
    print("response:",response.json())
    if response.status_code == 200:
        return response.json()
    else:
        return None
    #response.raise_for_status()  # Raise an exception for HTTP errors
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
    userName: str = ""
    userGrade: str =""
    userLevel: str = ""
    profilePic: str = ""
    userGroup: str = ""
    userType: str = ""
    tenantName: str = ""
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

def updateUser(email,  hashed_password = "", profilePic=""):
    userObj = User(userEmail=email, profilePic=profilePic, password=hashed_password)
    api="users/" #PUT request to update the non blank fields of user.
    #print("Dbg: Update User api about to be called ")
    response = requests.put(userssServiceUrl+api, headers=headers, json=userObj.model_dump())
    response.raise_for_status()  # Raise an exception for HTTP errors
    print("Update User Response:",response.json())
    return response.json()

def addTenantAdmin(username, email, hashed_password, tenantName) :
    return createUser(username, email, hashed_password, tenantName,"tenantadmin")
    pass

def getUsersForTenantAdmin(adminUser_id):
    api="users/"
    #api = f"users/{adminUser_id}"
    response = requests.get(userssServiceUrl+api, headers=headers,params={"tenant_admin_email": adminUser_id})
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json() 

def getTenantadminForTenant(tenantName):
    api="get_tenant_admins_for_tenant/"
    response = requests.get(userssServiceUrl+api, headers=headers,params={"tenantName": tenantName})
    response.raise_for_status()  # Raise an exception for HTTP errors
    print("getAdminsfromTenant Response:",response.json())
    return response.json()
#############################################################################################

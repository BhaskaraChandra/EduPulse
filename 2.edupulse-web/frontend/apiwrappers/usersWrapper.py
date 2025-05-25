from pydantic import BaseModel
import requests

from .commons import jwt_required, verify_jwt_token

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
def hitTest(hdrs={},**kwargs):
    api=""
    print("calling hittest:",userssServiceUrl+api)
    response = requests.get(userssServiceUrl+api, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    print("HitTestResponse:",response.json())
    return response.json() 

def authenticate_user(username, password):
    api="users/authenticateV2"
    #hitTest()
    print("calling authenticate_user:",userssServiceUrl+api)
    try:
        response = requests.post(userssServiceUrl+api, headers=headers, json={"userEmail": username, "password": password},timeout=10)
        print("response:",response.json())
        if response.status_code == 200:
            jwt = response.json()
            user = verify_jwt_token(jwt)
            if user:
                return user,jwt
            else:
                return None,None
        else:
            return None,None
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None,None
    response = requests.post(userssServiceUrl+api, headers=headers, json={"userEmail": username, "password": password})
    print("response:",response.json())
    if response.status_code == 200:
        jwt = response.json()
        user = verify_jwt_token(jwt)
        if user:
            return user,jwt
        else:
            return None,None
    else:
        return None,None
    #response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()
@jwt_required 
def createTenant(tenantName, hdrs={}, **kwargs):
    api="tenants/"
    response = requests.post(userssServiceUrl+api, headers=hdrs, json={"tenantName": tenantName})
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

@jwt_required 
def getTenants(hdrs={},**kwargs):
    api="tenants/"
    response = requests.get(userssServiceUrl+api, headers=hdrs)
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

@jwt_required 
def createUser(username, email, hashed_password, tenantName, userGroup, userType,hdrs={}, **kwargs):
    userObj = User(userEmail=email, userName=username, password=hashed_password, 
                   tenantName=tenantName, userGroup=userGroup, userType=userType)
    api="users/"
    print("Dbg: Createuser api about to be called ")
    response = requests.post(userssServiceUrl+api, headers=hdrs, json=userObj.model_dump())
    response.raise_for_status()  # Raise an exception for HTTP errors
    print("Createuser Response:",response.json())
    return response.json()
    pass

@jwt_required 
def updateUser(email,  hashed_password = "", profilePic="", hdrs={},**kwargs):
    userObj = User(userEmail=email, profilePic=profilePic, password=hashed_password)
    api="users/" #PUT request to update the non blank fields of user.
    #print("Dbg: Update User api about to be called ")
    response = requests.put(userssServiceUrl+api, headers=hdrs, json=userObj.model_dump())
    response.raise_for_status()  # Raise an exception for HTTP errors
    print("Update User Response:",response.json())
    return response.json()

@jwt_required 
def addTenantAdmin(username, email, hashed_password, tenantName, hdrs={}, **kwargs) :
    return createUser(username, email, hashed_password, tenantName,"NA-TenantAdmin","tenantadmin")
    pass

@jwt_required 
def getUsersForTenantAdmin(adminUser_id,hdrs={}, **kwargs):
    api="users/"
    #api = f"users/{adminUser_id}"
    response = requests.get(userssServiceUrl+api, headers=hdrs,params={"tenant_admin_email": adminUser_id})
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json() 

@jwt_required 
def getTenantadminForTenant(tenantName, hdrs={}, **kwargs):
    api="get_tenant_admins_for_tenant/"
    response = requests.get(userssServiceUrl+api, headers=hdrs,params={"tenantName": tenantName})
    response.raise_for_status()  # Raise an exception for HTTP errors
    print("getAdminsfromTenant Response:",response.json())
    return response.json()
#############################################################################################
#UserGroups related wrappers
#############################################################################################
@jwt_required 
def createUserGroup(userGroupName, tenantName, hdrs={}, **kwargs):
    api="createGroupForTenant/"
    response = requests.post(userssServiceUrl+api, headers=hdrs, params={"userGroupName": userGroupName, "tenantName": tenantName})
    response.raise_for_status()  # Raise an exception for HTTP errors
    print(api,response.json())
    return response.json()

@jwt_required 
#def getUserGroupsForTenant(tenantName,hdrs={}, **kwargs):
def getUserGroupsForTenant(tenantName,hdrs={}, **kwargs):
    api="getGroupsForTenant/"
    response = requests.get(userssServiceUrl+api, headers=hdrs,params={"tenantName": tenantName})
    response.raise_for_status()  # Raise an exception for HTTP errors
    print(api,response.json())
    return response.json()

@jwt_required 
def getUsersInGroup(userGroupName, tenantName, hdrs={}, **kwargs):
    api="getUsersInGroup/"
    response = requests.get(userssServiceUrl+api, headers=hdrs, params={"userGroupName": userGroupName, "tenantName": tenantName})
    response.raise_for_status()  # Raise an exception for HTTP errors
    print(api,response.json())
    return response.json()

@jwt_required 
def addUserToGroup(userEmail, userGroupName, tenantName, hdrs={}, **kwargs):
    api="addUserToGroup/"
    response = requests.post(userssServiceUrl+api, headers=hdrs, params={"userEmail": userEmail, "userGroupName": userGroupName, "tenantName": tenantName})
    response.raise_for_status()  # Raise an exception for HTTP errors
    print(api,response.json())
    return response.json()
#testing the API
# def testAPI():
#     print("Testing API with MockData")
#     createUserGroup("testgroup2","dummyytenant")
#     getUserGroupsForTenant("dummyytenant")
#     addUserToGroup("testuser@gmail.com","testgroup2","dummyytenant")
#     getUsersInGroup("testgroup2","dummyytenant")

#testAPI()
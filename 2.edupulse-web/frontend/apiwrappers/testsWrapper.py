#from pyparsing.core import List
from http.client import HTTPException
from typing import List
from fastapi.responses import JSONResponse
import requests
from .commons import jwt_required, verify_jwt_token

from .appConfig import appConfig

config = appConfig()
testsServiceUrl = config.tests_service_url
metricsServiceUrl = config.metrics_service_url

# l-ocalService = False
# if localService:
#     testsServiceUrl = "http://localhost:9117/"
#     metricsServiceUrl = "http://localhost:9117/"
import os
testsServiceUrl = os.environ.get('tsvc',testsServiceUrl)
metricsServiceUrl = os.environ.get('msvc',metricsServiceUrl)
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

@jwt_required 
def generateQuickTest(quickTestConfig: dict=None,hdrs={},** kwargs) -> dict:
    try:
        api="quicktest/"
        #print(quickTestConfig)
        response = requests.post(testsServiceUrl+api, headers=hdrs,json=quickTestConfig)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data=response.json()
        #print("apiResponse:",data)
        return response
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")
        return JSONResponse(content={"error": f"Request Exception: {err}"}, status_code=400)
        #return HTTPException(status_code=400, detail="No questions found for the given criteria")
        return None
    
@jwt_required 
def getActiveQuickTest(user_id: str=None,hdrs={},** kwargs) -> requests.Response:
    try:
        api="quicktest/"
        response = requests.get(testsServiceUrl + api, headers=hdrs, params={"useremail": user_id})
        #print("DBG:testsWrapper: response: getQuickTest:",response.json())
        response.raise_for_status()  # Raise an exception for HTTP errors
        data=response.json()
        return response
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")
        return None    
    
@jwt_required 
def getTestSummary(ids: List,hdrs={},** kwargs) -> requests.Response:
    try:
        #print("getTestSummary:",ids)
        api="questionsSummary/"
        response = requests.get(testsServiceUrl + api, headers=hdrs, params={"ids": ids})
        response.raise_for_status()  # Raise an exception for HTTP errors
        data=response.json()
        return response
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")
        return None    
    
@jwt_required 
def submitTest(quickTestConfig: dict=None,hdrs={},** kwargs) -> dict:
    try:
        api="submitquicktest/"
        #print("submitquicktest:",quickTestConfig)
        response = requests.post(testsServiceUrl+api, headers=hdrs,json=quickTestConfig)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data=response.json()
        #print("apiResponse:",data)
        return response
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")
        return None

@jwt_required 
def getTestsHistory(user_id: str, page: int = 1, page_size: int = 10,hdrs={},** kwargs) -> requests.Response:
    try:
        api="tests-history/"
        response = requests.get(testsServiceUrl + api, headers=hdrs, params={"useremail": user_id})
        response.raise_for_status()  # Raise an exception for HTTP errors
        data=response.json()
        return response
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")
        return None    
@jwt_required 
def getUserMetrics(user_id: str,hdrs={},** kwargs) -> requests.Response:
    try:
        api="user_metrics/"
        response = requests.get(metricsServiceUrl + api, headers=hdrs, params={"user_email": user_id})
        response.raise_for_status()  # Raise an exception for HTTP errors
        data=response.json()
        return response
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")
        return None    

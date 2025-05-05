#from pyparsing.core import List
from http.client import HTTPException
from typing import List
from fastapi.responses import JSONResponse
import requests

testsServiceUrl = "https://edupulsesvc.onrender.com/"
metricsServiceUrl = "https://edupulsesvc.onrender.com/"

localService = False
if localService:
    testsServiceUrl = "http://localhost:9117/"
    metricsServiceUrl = "http://localhost:9117"
import os
testsServiceUrl = os.environ.get('tsvc',testsServiceUrl)
metricsServiceUrl = os.environ.get('msvc',metricsServiceUrl)
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def generateQuickTest(quickTestConfig: dict=None) -> dict:
    try:
        api="quicktest/"
        #print(quickTestConfig)
        response = requests.post(testsServiceUrl+api, headers=headers,json=quickTestConfig)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data=response.json()
        #print("apiResponse:",data)
        return response
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")
        return JSONResponse(content={"error": f"Request Exception: {err}"}, status_code=400)
        #return HTTPException(status_code=400, detail="No questions found for the given criteria")
        return None
    
def getActiveQuickTest(user_id: str=None) -> requests.Response:
    try:
        api="quicktest/"
        response = requests.get(testsServiceUrl + api, headers=headers, params={"useremail": user_id})
        #print("DBG:testsWrapper: response: getQuickTest:",response.json())
        response.raise_for_status()  # Raise an exception for HTTP errors
        data=response.json()
        return response
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")
        return None    
    
def getTestSummary(ids: List) -> requests.Response:
    try:
        #print("getTestSummary:",ids)
        api="questionsSummary/"
        #api="userQuestions/"
        #response = requests.get(testsServiceUrl + api, headers=headers, params={"useremail": "dhoni@csk.com"})
        response = requests.get(testsServiceUrl + api, headers=headers, params={"ids": ids})
        response.raise_for_status()  # Raise an exception for HTTP errors
        data=response.json()
        return response
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")
        return None    
    
def submitTest(quickTestConfig: dict=None) -> dict:
    try:
        api="submitquicktest/"
        #print("submitquicktest:",quickTestConfig)
        response = requests.post(testsServiceUrl+api, headers=headers,json=quickTestConfig)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data=response.json()
        #print("apiResponse:",data)
        return response
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")
        return None

def getTestsHistory(user_id: str, page: int = 1, page_size: int = 10) -> requests.Response:
    try:
        api="tests-history/"
        response = requests.get(testsServiceUrl + api, headers=headers, params={"useremail": user_id})
        response.raise_for_status()  # Raise an exception for HTTP errors
        data=response.json()
        return response
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")
        return None    
def getUserMetrics(user_id: str) -> requests.Response:
    try:
        api="user_metrics/"
        response = requests.get(metricsServiceUrl + api, headers=headers, params={"user_email": user_id})
        response.raise_for_status()  # Raise an exception for HTTP errors
        data=response.json()
        return response
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")
        return None    

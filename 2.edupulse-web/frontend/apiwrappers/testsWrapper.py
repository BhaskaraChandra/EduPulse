import requests

testsServiceUrl = "https://edupulsesvc.onrender.com/"
testsServiceUrl = "http://localhost:9117/"
#headers = {'Content-Type': 'application/json'}
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def generateQuickTest(quickTestConfig: dict=None) -> dict:
    try:
        api="quicktest/"
        print(quickTestConfig)
        response = requests.post(testsServiceUrl+api, headers=headers,json=quickTestConfig)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data=response.json()
        print("apiResponse:",data)
        return response
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")
        return None
    
def getActiveQuickTest(user_id: str=None) -> requests.Response:
    try:
        api="quicktest/"
        response = requests.get(testsServiceUrl + api, headers=headers, params={"useremail": user_id})
        response.raise_for_status()  # Raise an exception for HTTP errors
        data=response.json()
        return response
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")
        return None    
    
def submitTest(quickTestConfig: dict=None) -> dict:
    try:
        api="submitquicktest/"
        print("submitquicktest:",quickTestConfig)
        response = requests.post(testsServiceUrl+api, headers=headers,json=quickTestConfig)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data=response.json()
        print("apiResponse:",data)
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
        response = requests.get(testsServiceUrl + api, headers=headers, params={"user_email": user_id})
        response.raise_for_status()  # Raise an exception for HTTP errors
        data=response.json()
        return response
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")
        return None    

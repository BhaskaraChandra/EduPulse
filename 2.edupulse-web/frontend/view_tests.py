from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import requests
import json
from django.views.decorators.csrf import csrf_exempt

from frontend.apiwrappers import testsWrapper

@require_http_methods(['POST'])
@csrf_exempt
def generate_test(request):
    json_data = json.loads(request.body)# Get the JSON data from the request
    #print(json_data)
    ret = testsWrapper.generateQuickTest(json_data)
    print("received:",ret)
    #return ret
    # Return a JSON response
    return JsonResponse(ret.json(), safe=False)
    return JsonResponse({'status': 'success', 'message': 'Test generated successfully'})

@require_http_methods(['GET'])
@csrf_exempt
def get_active_quick_test(request, curUser_email):
    #json_data = json.loads(request.body)# Get the JSON data from the request
    #print(curUser_email)
    ret = testsWrapper.getActiveQuickTest(curUser_email)
    #print("DBG:Active Test Received at ViewTests:",ret.json())
    # Return a JSON response
    return JsonResponse(ret.json(), safe=False)
    return JsonResponse({'status': 'success', 'message': 'Test generated successfully'})

def livetest(request):
    print("DBG: rendering the livetest.html")
    return render(request, 'liveTest.html')

@require_http_methods(['POST'])
@csrf_exempt
def testSummary(request):
    qidsList = json.loads(request.body)
    #print(qidsList)
    qsSummary = testsWrapper.getTestSummary(qidsList)
    return JsonResponse(qsSummary.json(), safe=False)
    return render(request, 'testSummary.html')

@require_http_methods(['POST'])
@csrf_exempt
def submit_test(request):
    json_data = json.loads(request.body)# Get the JSON data from the request
    #print(json_data)
    testResult = testsWrapper.submitTest(json_data)
    #print("Rendering the testSummary")
    #return render(request, 'testSummary.html', {'testResult1': testResult.json()})
    #return render(request, 'testSummary.html')
    #print("views.py: received:",ret)
    #return ret
    # Return a JSON response
    return JsonResponse(testResult.json(), safe=False)

def history_view(request):
    user_email = request.session.get("user").get("userEmail")
    tests = testsWrapper.getTestsHistory(user_email)
    #print(f"TestsHistory for user:{user_email}\n",tests.json())
    #request.session["tests_history"] = tests.json()
    #request.session.modified = True  # Ensure session updates
    return render(request, 'history.html',{'tests_history': json.dumps(tests.json(), ensure_ascii=False, indent=4)})

def metrics_view(request):
    user_email = request.session.get("user").get("userEmail")
    metrics = testsWrapper.getUserMetrics(user_email)
    #print(f"Metrics for user:{user_email}\n",metrics.json())
    return render(request, 'scoreboard.html',{'user_metrics': json.dumps(metrics.json(), ensure_ascii=False, indent=4)})

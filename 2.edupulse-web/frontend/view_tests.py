import time
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from fastapi.responses import JSONResponse
import requests
import json
from django.views.decorators.csrf import csrf_exempt

from frontend.apiwrappers import questionsWrapper, testsWrapper

@require_http_methods(['POST'])
@csrf_exempt
def generate_test(request):
    json_data = json.loads(request.body)# Get the JSON data from the request
    #print(json_data)
    try:
        ret = testsWrapper.generateQuickTest(json_data,jwt = request.session["jwt"])
        #print("received:",ret)
        #return ret
        # Return a JSON response
        return JsonResponse(ret.json(), safe=False)
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")
        return JsonResponse({}, safe=False)
        return JSONResponse(content={"error": f"Request Exception: {err}"}, status_code=400)
    return JsonResponse({'status': 'success', 'message': 'Test generated successfully'})

@require_http_methods(['GET'])
@csrf_exempt
def get_active_quick_test(request, curUser_email):
    #json_data = json.loads(request.body)# Get the JSON data from the request
    #print(curUser_email)
    ret = testsWrapper.getActiveQuickTest(curUser_email,jwt = request.session["jwt"])
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
    qsSummary = testsWrapper.getTestSummary(qidsList,jwt = request.session["jwt"])
    return JsonResponse(qsSummary.json(), safe=False)
    return render(request, 'testSummary.html')

@require_http_methods(['POST'])
@csrf_exempt
def submit_test(request):
    json_data = json.loads(request.body)# Get the JSON data from the request
    #print(json_data)
    testResult = testsWrapper.submitTest(json_data,jwt = request.session["jwt"])
    #print("Rendering the testSummary")
    #return render(request, 'testSummary.html', {'testResult1': testResult.json()})
    #return render(request, 'testSummary.html')
    #print("views.py: received:",ret)
    #return ret
    # Return a JSON response
    return JsonResponse(testResult.json(), safe=False)

def history_view(request):
    user_email = request.session.get("user").get("userEmail")
    tests = testsWrapper.getTestsHistory(user_email,jwt = request.session["jwt"])
    #print(f"TestsHistory for user:{user_email}\n",tests.json())
    #request.session["tests_history"] = tests.json()
    #request.session.modified = True  # Ensure session updates
    return render(request, 'history.html',{'tests_history': json.dumps(tests.json(), ensure_ascii=False, indent=4)})

def metrics_view(request):
    user_email = request.session.get("user").get("userEmail")
    metrics = testsWrapper.getUserMetrics(user_email,jwt = request.session["jwt"])
    #print(f"Metrics for user:{user_email}\n",metrics.json())
    return render(request, 'scoreboard.html',{'user_metrics': json.dumps(metrics.json(), ensure_ascii=False, indent=4)})


def tests_view(request):
    return render(request, 'tests.html')


def create_test_view(request):
    start_time = time.time()
    print("Create Test View")
    userObj = request.session.get("user")
    #above method to get topics metadata is no longer being used, as the below method is being used.
    user_questions = questionsWrapper.get_user_questions_metadata(userObj["userEmail"],jwt = request.session["jwt"])
    for subject,subObj in user_questions.items():
        if subject in ("_id", "_metrics"): continue
        #print("subject:",subject,"subObj:", subObj)
        for grade, gradeObj in subObj.items():
            if grade in ("_metrics"): continue
            for topic, topicObj in gradeObj.items():
                if topic in ("_metrics"): continue
                #print("topic:",topic,"topicObj:", topicObj)
                for subtopic, subtopicObj in topicObj.items():
                    if subtopic in ("_metrics"): continue
                    subtopicObj = {"_metrics": subtopicObj["_metrics"]}
                    user_questions[subject][grade][topic][subtopic] = subtopicObj
                    pass
    #print("user_questions:", user_questions)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken by create_test_view: {elapsed_time:.4f} seconds")

    # Log the elapsed time
    #logging.info(f"Time taken by create_test_view: {elapsed_time:.4f} seconds")

    return render(request, "create_test.html", {
        "selected_topics_json": json.dumps(user_questions, ensure_ascii=False, indent=4)
    })

    
def daily_challenge_view(request):
    return render(request, 'daily_challenge.html')

def topics_view(request):
    return render(request, 'topics.html')


#http://localhost:9080/api/topics


def manage_topics_view(request):
    start_time = time.time()
    #print("Manage Topics View")
    userObj = request.session.get("user")
    #print("User Object:", userObj)
    userTopicsMetadata = questionsWrapper.get_user_questions_metadata(userObj["userEmail"],jwt = request.session["jwt"])
    #print("Global Topics:", topicsMetadata)
    #print("User Topics:", userTopicsMetadata)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken by manage_topics_view: {elapsed_time:.4f} seconds")
    return render(request, 'manage_topics.html', {
        "topics_json": json.dumps(userTopicsMetadata), #this is the generic topics json
        "selected_topics_json": json.dumps(userTopicsMetadata)  # this is the user specific topics json
    })

@csrf_exempt
def save_selected_topics(request):
    if request.method == "POST":
        try:
            userObj = request.session.get("user");print("User Object:", userObj)
            data = json.loads(request.body)
            selected_topics = data.get("selected_topics", [])
            #print("Selected Topics:", json.dumps(selected_topics, indent=4))
            questionsWrapper.save_selected_topics(userObj["userEmail"],selected_topics,jwt = request.session["jwt"])
            # NOTE: use the below reference code to send any data to the frontend.
            #request.session["selected_topics"] = structured_data
            #request.session.modified = True  # Ensure session updates
            return JsonResponse({"message": "Topics saved successfully!", "data": selected_topics}, status=200)

        except Exception as e:
            print(" Error:", e)
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)
def dashboards_view(request):
    return render(request, 'dashboards.html')

def my_progress_view(request):
    return render(request, 'my_progress.html')

def compare_view(request):
    return render(request, 'compare.html')

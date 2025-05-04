

import json
import random
import time

from pydantic import BaseModel


#Using sys.path

import sys
import os

from questionsWrapper import get_user_questions_metadata
import testsWrapper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
#from ..frontend.apiwrappers.questionsWrapper import get_user_questions_metadata


class RequestPayload(BaseModel):
    Subject: str = "Math"
    Grade: list = ["11"]
    Topics: list = ["Algebra", "Calculus"]
    Subtopics: list = ["Sets , Relations and Functions","Trigonometry"]
    Level: list = [1,2,3,4,5,6,7,8,9,10]
    nQuestions: int = 10
    userid: str= "dhoni@csk.com"


def composeTestConfig(user_questions):
    userid = user_questions["_id"]
    user_questions.pop("_id");user_questions.pop("_metrics")
    random_subject = random.choice(list(user_questions.keys()))
    subjectObj = user_questions[random_subject]
    subjectObj.pop("_metrics")
    random_grade = random.choice(list(subjectObj.keys()))
    gradeObj = subjectObj[random_grade]
    gradeObj.pop("_metrics")
    random_topic = random.choice(list(gradeObj.keys()))
    topicObj = gradeObj[random_topic]
    topicObj.pop("_metrics")
    random_subTopic = random.choice(list(topicObj.keys()))
    subTopicObj = topicObj[random_subTopic]
    payload = RequestPayload(
        Subject=random_subject,
        Grade=[random_grade],
        Topics=[random_topic],
        Subtopics=[random_subTopic],
        Level=[1,2,3,4,5,6,7,8,9,10],
        nQuestions=10,
        userid=userid
    )
    return payload
    pass

def getTestResponse(testPaper,userid):
    testResponse = {}; # this is the payload for submitting the test after completion.
    testResponse["Qs"] = {}
    testResponse["startTime"] = time.time()
    testResponse["endTime"] = time.time()
    testResponse["userid"] = userid
    testResponse["testduration"] = 0
    testResponse["qCount"] = len(testPaper)
    testResponse["attemptCount"] = 0
    testResponse["reviewCount"] = 0
    for qid, qObj in testPaper.items():
        testResponse["Qs"][qid] = {}
        testResponse["Qs"][qid]["qid"] = qid
        testResponse["Qs"][qid]["Choice"]=random.randint(1, 4)
        testResponse["Qs"][qid]["Review"]=False
        testResponse["Qs"][qid]["TimeToSubmit"]=random.randint(1, 30)
    return testResponse
    pass

def CreateAndSubmitTest(userid):
    print(f"CreateAndSubmitTest:{userid}")
    #await asyncio.sleep(1)
    start_time = time.time()
    user_questions = get_user_questions_metadata(userid)
    testConfig = composeTestConfig(user_questions)
    ret = testsWrapper.generateQuickTest(testConfig.model_dump())
    ret = testsWrapper.getActiveQuickTest(userid)
    ret = json.loads(ret.content)
    testResponse = getTestResponse(ret,userid)
    ret = testsWrapper.submitTest(testResponse)
    end_time = time.time()
    print(f"Time taken by CreateAndSubmitTest:{userid}", end_time - start_time, "seconds")
    pass

# CreateAndSubmitTest("perf_testUser")
# CreateAndSubmitTest("perf_testUser")
# CreateAndSubmitTest("perf_testUser")
# CreateAndSubmitTest("perf_testUser")

import asyncio
import concurrent.futures

def CreateAndSubmitTestWrapper(user_id):
    CreateAndSubmitTest(user_id)

N = 20 #int(input("Enter the number of users: "))
async def main():
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        tasks = []
        for i in range(1, N + 1):
            user_id = f"perf_user{i}"
            task = loop.run_in_executor(pool, CreateAndSubmitTestWrapper, user_id)
            tasks.append(task)
        await asyncio.gather(*tasks)
start_time = time.time()
asyncio.run(main())
end_time = time.time()
totalDuration = end_time - start_time
averageTransactionTime = totalDuration / N
print(f"Time taken by CreateAndSubmitTestWrapper: {totalDuration} seconds")
print(f"Average transaction time: {averageTransactionTime} seconds")

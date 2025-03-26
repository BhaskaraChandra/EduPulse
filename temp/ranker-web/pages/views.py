import base64
import json
import os
from django.shortcuts import render,redirect
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from .utils import Utility
from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_GET

utility = Utility()
# Create your views here.

def home(request):
    return render(request, "pages/home.html", {})
#this pulls only subject and topic names as an array.
def pullJsonArrayFromCache(arrName):
    jsonarr=cache.get(arrName)
    if jsonarr is None:
        #print(f"Loading {arrName} from Cache:")
        with open(f"./data/{arrName}.json") as f:
            data = json.load(f)
            jsonarr = list(data.keys())
            cache.set(arrName, jsonarr, 60 * 60)  # cache for 1 hour
    return jsonarr
def pullJsonObjFromCache(objName):
    jsonObj=cache.get(objName+"Obj")
    if jsonObj is None:
        #print(f"Loading {objName} from Cache:")
        with open(f"./data/{objName}.json") as f:
            jsonObj = json.load(f)
            #jsonObj = list(data.keys())
            cache.set(objName+"Obj", jsonObj, 60 * 60)  # cache for 1 hour
    return jsonObj
def createtest(request):
    #print("CreateTest called:")
    subjects = pullJsonArrayFromCache('subjects')
    topics = pullJsonArrayFromCache('topics')
    return render(request, 'pages/createtest.html', {
        'subjects': subjects,
        'topics': topics,
    })

#to be renamed to GenerateTest
def create_test(request):
    #print("GenerateTest")
    if request.method == 'POST':
        data = json.loads(request.body)
        subjects = data['subjects']
        topics = data['topics']
        numQuestions = int(data['numQuestions'])
        #print(subjects)
        questionIds = utility.createTest(subjects, topics, numQuestions)
        #request.session['questionIds'] = questionIds #this line and next line for hidden param passing
        #return HttpResponseRedirect(reverse('live_test'))
        return JsonResponse({'questionIds': questionIds})
def image_view(request):
    image_path = './data/Questions/1._Question.jpg'
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    return HttpResponse(image_data, content_type='image/jpeg')

def live_test(request):
    #questionIds = request.session.get('questionIds')
    # Process questionIds and render liveTest.html
    #return render(request, 'pages/liveTest.html', {'questionIds': questionIds})

    questionIds = request.GET.get('questionIds')
    questionIds = questionIds.split(',')  # Split the string into a list
    questionDetails = {}
    #pdfs = {}

    for q in questionIds:
        questionDetails[q] = utility.getQuestionDetails(q)
        #pdf_file = utility.getQuestionPdf(q)  # Assume this returns the PDF file
        #pdfs[q] = base64.b64encode(pdf_file).decode('utf-8')

    # Process questionIds and render liveTest.html
    #print(questionDetails)
    #return render(request, 'pages/liveTest.html', {'questionIds': questionIds,'questionDetails': questionDetails})
    return render(request, 'pages/liveTest.html', {'questionIds': questionIds,'questionDetails': questionDetails})

#obsolete/unused function. may need this once the code gets scaled.
@require_GET
def get_question(request):
    question_id = request.GET.get('questionId')
    #print(f"qid:{question_id}")
    return JsonResponse(Utility().getQuestionDetails(question_id))
    '''with open('utils/questions.json') as f:
        questions = json.load(f)
    for question in questions:
        if question['id'] == int(question_id):
            return JsonResponse(question)'''
    #return JsonResponse({'error': 'Question not found'})



'''
def createtestWorkingVersion(request):
    #print("createtest")
    subjects = [
        Subject(name='Math'),
        Subject(name='Science'),
        Subject(name='English'),
        Subject(name='History'),
        Subject(name='Geography'),
    ]
    selected_subjects = request.session.get('selected_subjects', [])
 
    return render(request, "pages/createtest.html", {'subjects': subjects, 'selected_subjects': selected_subjects})

from .models import Subject

def index(request):
    #subjects = Subject.objects.all()
    # Create some subjects
    #print("index")
    subjects = ['Math', 'Science', 'English']
    topics = ['Topic 1', 'Topic 2', 'Topic 3']
    return render(request, 'index.html', {
        'subjects': subjects,
        'topics': topics,
    })
'''
'''
    subjectstemp = [
        Subject(name='Math'),
        Subject(name='Science'),
        Subject(name='English'),
        Subject(name='History'),
        Subject(name='Geography'),
    ]

    selected_subjects = request.session.get('selected_subjects', [])
    return render(request, 'createTest.html', {'subjects': subjects, 'selected_subjects': selected_subjects})
'''
'''
def indexcopydeletethislater(request):
    subjects = ['Math', 'Science', 'English']
    topics = ['Topic 1', 'Topic 2', 'Topic 3']
    return render(request, 'index.html', {
        'subjects': subjects,
        'topics': topics,
    })



def select_subject(request):
    #TODO: need to check if this is needed at all
    #print("select_subject")
    subject_id = request.POST.get('subject_id')
    subject = Subject.objects.get(id=subject_id)
    selected_subjects = request.session.get('selected_subjects', [])
    if subject.name in selected_subjects:
        selected_subjects.remove(subject.name)
    else:
        selected_subjects.append(subject.name)
    request.session['selected_subjects'] = selected_subjects
    return render(request, 'createTest.html', {'subjects': Subject.objects.all(), 'selected_subjects': selected_subjects})
'''
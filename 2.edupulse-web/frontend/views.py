from django.shortcuts import render,redirect
from django.http import JsonResponse
from pymongo import MongoClient
from django.contrib import messages
import bcrypt
from django.contrib.auth.hashers import make_password, check_password
from functools import wraps
from bson import ObjectId
import logging

from frontend.apiwrappers import questionsWrapper, usersWrapper
#from frontend.apiwrappers.questionsWrapper import get_topics_metadata
logger = logging.getLogger(__name__)
from django.views.decorators.csrf import csrf_exempt

import os
import json
#import view_tests

# def mongo_login_required(view_func):
#     """ Custom decorator to check if user is authenticated using session. """
#     @wraps(view_func)
#     def _wrapped_view(request, *args, **kwargs):
#         if "user_id" not in request.session:
#             return redirect("login")  # Redirect to login page if not authenticated
#         return view_func(request, *args, **kwargs)
#     return _wrapped_view


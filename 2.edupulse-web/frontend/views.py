from django.shortcuts import render,redirect
# from django.http import JsonResponse
# from pymongo import MongoClient
# from django.contrib import messages
# import bcrypt
# from django.contrib.auth.hashers import make_password, check_password
# from functools import wraps
# from bson import ObjectId
import logging


logger = logging.getLogger(__name__)
from django.views.decorators.csrf import csrf_exempt

import os
import json

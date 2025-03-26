from django.shortcuts import render,redirect
from django.http import JsonResponse
from pymongo import MongoClient
from django.contrib import messages
import bcrypt
from django.contrib.auth.hashers import make_password, check_password
from functools import wraps
from bson import ObjectId
import logging
logger = logging.getLogger(__name__)
from django.views.decorators.csrf import csrf_exempt

import os
import json
from django.conf import settings
from frontend.apiwrappers.TenantsAdapter import TenantsAdapter


# MongoDB Atlas connection
MONGO_URI = 'mongodb+srv://sai444134:1234567899@cluster0.6nyzm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(MONGO_URI)
db = client["test"]  # Database name
users_collection = db["users"]
tenants_collection = db["tenants"]
topics_collection = db["topics"]
tenants = TenantsAdapter()

#users=UsersAdapter()


def mongo_login_required(view_func):
    """ Custom decorator to check if user is authenticated using session. """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if "user_id" not in request.session:
            return redirect("login")  # Redirect to login page if not authenticated
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Find user in MongoDB
        user = users_collection.find_one({"username": username})

        if user:
            # Get hashed password from MongoDB
            hashed_password = user["password"]  # Stored as a hashed value
            print(user["usertype"])
            # Compare the stored hashed password with the entered plain-text password
            if True or bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                request.session["user_id"] = str(user["_id"])  # Store session
                if(user["usertype"]=="superadmin"):
                    return redirect("dashboard")  # Redirect to the homepage or dashboard
                elif(user["usertype"]=="tenantadmin"):
                    print('tenantadmin')
                    return redirect("tenantdashboard")  # Redirect to the homepage or dashboard
                elif(user["usertype"]=="consumer"):
                    print('consumer')
                    return redirect("user_dashboard")  # Redirect to the homepage or dashboard
                # elif(user["usertype"]=="consumer"):
                #     return redirect("usersdashboard") #Redirect to the usersdashboard
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

def tenantdashboard(request):
    return render(request,"tenantdashboard.html")
def user_dashboard(request):
    print("user_dashboard")
    return render(request, 'usersdashboard.html', {'user': request.user})


def logout_view(request):
    print('cleared')
    request.session.flush()  
    return redirect('login')

@mongo_login_required
def dashboard_view(request):
    if "user_id" not in request.session:
        return JsonResponse({"error": "Unauthorized access"}, status=401)
    return render(request, "dashboard.html")

@mongo_login_required
def SubmitTenantAdmin(request):
    print("SubmitTenantAdminClicked")
    if request.method == 'POST':
        option = request.POST.get("option")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        tenantName = request.POST.get("tenant")
        # Process the form data here
        print("Option:", option);print("Username:", username);print("Email:", email);print("Password:", password)
        if username and email and password:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            try:
                users_collection.insert_one({
                    "username": username,
                    "email": email,
                    "usertype": "tenantadmin",
                    "password": hashed_password,
                    "tenant": tenantName
                })
                tenants_collection.update_one({"tenantName": tenantName},{"$inc": {"adminCount": 1}})

                messages.success(request, "TenantAdmin added successfully!")
                #print("tenantadmin added successfully")
                return redirect("sidebar_option", option="tenant")
            except Exception as e:
                print(f"Error adding Tenant Admin: {e}")
                #messages.error(request, f"Error adding Tenant Admin: {e}")

@mongo_login_required
def SubmitTenant(request):
    print("XXXXXSubmitTenantClicked")
    if request.method == 'POST':
        option = request.POST.get("option")
        tenantName = request.POST.get("tenantName") #this shoiuld be tenantName
        user_id = request.session.get("user_id")  #TODO: actually this userid is not needed here.
        # Process the form data here
        print("Option:", option);print("tenant Name:", tenantName)
        if tenantName:
            try:
                tenants_collection.insert_one({
                    "user_id": user_id,
                    "tenantName": tenantName,
                    "adminCount": 0,
                    "userCount": 0
                })
                messages.success(request, "Tenant added successfully!")
                #print("tenant added successfully")
                return redirect("sidebar_option", option="tenant")
            except Exception as e:
                messages.error(request, f"Error adding Tenant: {e}")
    pass
@mongo_login_required
def dashboard(request):
    print("******dashboard called")
    user_id = request.session.get("user_id")  
    user = users_collection.find_one({"_id": ObjectId(user_id)})  # Get logged-in user details
    tenants_data = list(tenants_collection.find({"user_id": user_id}, {"_id": 0}))  
    #return render(request, "dashboard.html", {"tenant_data": tenants_data})

    if request.method == "POST":
        print("Received POST request")  
        print("POST Data:", request.POST)  

        option = request.POST.get("option")
        print("Option:", option)

        if option == "tenantadmin":
            print("Option is tenantadmin")
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")

            if username and email and password:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                try:
                    users_collection.insert_one({
                        "username": username,
                        "email": email,
                        "usertype": "tenantadmin",
                        "password": hashed_password,
                    }) 
                    # user_adapter.adduser(
                    #     "username"= username,
                    #     "email"= email,
                    #     "usertype"= "tenantadmin",
                    #     "password"= hashed_password,

                    # )
                    
                    print("Superadmin added successfully")
                    messages.success(request, "SuperAdmin added successfully!")
                    return redirect("dashboard")  # Keep this for superadmin
                except Exception as e:
                    print("Error:", e)
                    messages.error(request, f"Error adding SuperAdmin: {e}")

        elif option == "consumer":
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")

            if username and email and password:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                try:
                    users_collection.insert_one({
                        "username": username,
                        "email": email,
                        "usertype": "consumer",
                        "password": hashed_password,
                        "created_by": user_id  
                    })
                    print("Consumer added successfully")
                    # user_topic_col=db["user_topic"]
                    
                    # obj={}
                    # obj["_id"]=email
                    # user_topic_col.insertone(obj)
                    messages.success(request, "Consumer added successfully!")

                    # Redirect based on user type
                    if user and user["usertype"] == "tenantadmin":
                        return redirect("tenantdashboard")  # Redirect to tenant dashboard
                    else:
                        return redirect("dashboard")  # Keep default for superadmin

                except Exception as e:
                    print("Error:", e)
                    messages.error(request, f"Error adding Consumer: {e}")

        elif option == "tenant":  # TODO this is adding a tenant.
            print("THIS CODE SHOULD NEVER EXECUTE")
            messages.error(request, f"Error adding tenant: {e}")

    #print("default return from dashboard")
    tenants_data = list(tenants_collection.find({"user_id": user_id}, {"_id": 0}))  
    return render(request, "dashboard.html", {"tenant_data": tenants_data})



@mongo_login_required
def sidebar(request, option=None):
    user_id = request.session.get("user_id")
    print("Side bar Option Clicked: ", option)  # Debugging

    tenants_data = []
    total_tenants = 0
    total_superadmins = 0

    if option == "users":
        print("Fetching users data...")
        user = users_collection.find_one({"_id": ObjectId(user_id)})  

        if user and user["usertype"] == "tenantadmin": 
            tenants_data = list(users_collection.find({"usertype": "consumer", "created_by": user_id}, {"_id": 0}))
            total_tenants = len(tenants_data)
        else:
            tenants_data = list(users_collection.find({}, {"_id": 0}))

        print("Fetched Users Data:", tenants_data)  
        template = "tenantdashboard.html"
    
    elif option == "tenantDummy": #this is unused and dummy
        tenants_data = []
        template = "dashboard.html"

    elif option == "tenant": #this is the actual Tenant Dashboard
        total_superadmins = 0 #users_collection.count_documents({"usertype": "superadmin"})
        #TODO: we may not need the above anymore for now.
        tenants_data = list(tenants_collection.find({"user_id": user_id}, {"_id": 0}))
        total_tenants = len(tenants_data)
        template = "dashboard.html"

    context = {
        "option": option,
        "tenant_data": tenants_data,
        "total_tenants": total_tenants,
        "total_superadmins": total_superadmins
    }

    return render(request, template, context)

#users dashboard

def tests_view(request):
    return render(request, 'tests.html')


def create_test_view(request):
    json_file_path = os.path.join(settings.BASE_DIR, 'frontend', 'static', 'data.json')  # Adjust path if needed

    try:
        with open(json_file_path, "r", encoding="utf-8") as file:
            selected_topics = json.load(file)  # Load JSON from file

        print("Loaded JSON Data for create_test_view:", json.dumps(selected_topics, indent=4))  # Debugging print

    except Exception as e:
        print("Error loading JSON file:", e)
        selected_topics = {}  # Set empty dict if there's an error

    return render(request, "create_test.html", {
        "selected_topics_json": json.dumps(selected_topics, ensure_ascii=False, indent=4)
    })

    
def daily_challenge_view(request):
    return render(request, 'daily_challenge.html')

def history_view(request):
    return render(request, 'history.html')

def topics_view(request):
    return render(request, 'topics.html')


#http://localhost:9080/api/topics


def manage_topics_view(request):
    #json_file_path = os.path.join(settings.BASE_DIR, 'frontend/static/data.json')
    json_file_path = os.path.join(settings.BASE_DIR, 'frontend', 'static', 'data.json')  # Adjust path if needed

    with open(json_file_path, 'r', encoding='utf-8') as file:
        topics_data = json.load(file)

    # Retrieve previously stored session data if available
    selected_topics = request.session.get("selected_topics", {})

    # Debugging print to check session data in the backend
    print("Session Data (selected_topics):", json.dumps(selected_topics, indent=4))

    return render(request, 'manage_topics.html', {
        "topics_json": json.dumps(topics_data),
        "selected_topics_json": json.dumps(selected_topics)  # Ensure the correct variable name
    })

@csrf_exempt
def save_selected_topics(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            selected_topics = data.get("selected_topics", [])

            if not selected_topics:
                return JsonResponse({"message": "No topics selected"}, status=400)

            structured_data = {}

            for topic in selected_topics:
                keys = topic.split(" - ")  # Ensure correct format
                current_level = structured_data

                for i, key in enumerate(keys):
                    if i == len(keys) - 1:
                        if key not in current_level:
                            current_level[key] = []
                    else:
                        if key not in current_level:
                            current_level[key] = {}
                        elif isinstance(current_level[key], list):
                            current_level[key] = {}

                    current_level = current_level[key]

            # Store structured data in session
            request.session["selected_topics"] = structured_data
            request.session.modified = True  # Ensure session updates

            print("Stored Topics in Session:", json.dumps(structured_data, indent=4))

            return JsonResponse({"message": "Topics saved successfully!", "data": structured_data}, status=200)

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

def settings_view(request):
    return render(request, 'settings.html')

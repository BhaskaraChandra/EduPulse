from django.shortcuts import render,redirect
from django.http import JsonResponse
from pymongo import MongoClient
from django.contrib import messages
import bcrypt
from django.contrib.auth.hashers import make_password, check_password
from functools import wraps
from bson import ObjectId


# MongoDB Atlas connection
MONGO_URI = 'mongodb+srv://sai444134:1234567899@cluster0.6nyzm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(MONGO_URI)
db = client["test"]  # Database name
users_collection = db["users"]
tenants_collection = db["tenants"]


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
def SubmitTenant(request):
    print("SubmitTenantClicked")
    if request.method == 'POST':
        option = request.POST.get("option")
        tenantName = request.POST.get("schoolName")
        user_id = request.session.get("user_id")  #TODO: actually this userid is not needed here.
        # Process the form data here
        #print("Option:", option);print("School Name:", tenantName)
        if tenantName:
            try:
                tenants_collection.insert_one({
                    "user_id": user_id,
                    "schoolName": tenantName
                })
                messages.success(request, "Tenant added successfully!")
                #print("tenant added successfully")
                return redirect("sidebar_option", option="school")
            except Exception as e:
                messages.error(request, f"Error adding school: {e}")
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
                    messages.success(request, "Consumer added successfully!")

                    # Redirect based on user type
                    if user and user["usertype"] == "tenantadmin":
                        return redirect("tenantdashboard")  # Redirect to tenant dashboard
                    else:
                        return redirect("dashboard")  # Keep default for superadmin

                except Exception as e:
                    print("Error:", e)
                    messages.error(request, f"Error adding Consumer: {e}")

        elif option == "school":  # TODO this is adding a tenant.
            print("THIS CODE SHOULD NEVER EXECUTE")
            messages.error(request, f"Error adding tenant: {e}")
            '''
            tenantName = request.POST.get("schoolName")
            if tenantName:
                try:
                    tenants_collection.insert_one({
                        "user_id": user_id,
                        "schoolName": tenantName
                    })
                    messages.success(request, "School added successfully!")
                    print("tenant added successfully")
                    #return render(request, "school", {"tenant_data": tenants_data})
                    return redirect("sidebar", option="school")
                except Exception as e:
                    messages.error(request, f"Error adding school: {e}")'
            '''
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
    
    elif option == "tenant":
        tenants_data = []
        template = "dashboard.html"

    elif option == "school":
        total_superadmins = users_collection.count_documents({"usertype": "superadmin"})
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

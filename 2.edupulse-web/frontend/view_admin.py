from django.contrib import messages
from django.contrib.sessions.models import Session
#from datetime import datetime
from django.utils import timezone

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
#from fastapi.responses import JSONResponse
import requests
import json
from django.views.decorators.csrf import csrf_exempt

from frontend.apiwrappers import usersWrapper

def authenticate_PROXY(username,password):
    user = {}
    if password == "fail":
        return None,None
    user["userName"] = username
    if password == "fail":
        return None,None
    user["userType"] = "consumer"
    if password == "tenantadmin":
        user["userType"] = password
    user["userEmail"] = "proxyuser@proxy.com"
    user["userGroup"] = "CSE-1st Year"
    user["profilePic"] = ""
    user["tenantName"] = "PROXY"
    user["_id"] = user["userEmail"]
    #request.session["user"]=user
    return user,"jswt"

#active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
#nSessions = active_sessions.delete()
print("Flushed the active_sessions")
def login_view(request):
    #active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    nSessions = 10; #active_sessions.count() 
    print("Active Sessions:",nSessions)
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        #password = "temp"
        user,jswt = usersWrapper.authenticate_userV2(username, password)
        #user,jswt = authenticate_PROXY(username, password)
        request.session["jwt"]=jswt

        #print(user)
        if user:
            if True :
                request.session["user_id"] = str(user["_id"])  # Store session
                if(user["userType"]=="superadmin"):
                    tenants_data = usersWrapper.getTenants(jwt = request.session["jwt"])
                    return render(request, "superadmin_dashboard.html", {"tenant_data": tenants_data})
                elif(user["userType"]=="tenantadmin"):
                    print('tenantadmin')
                    request.session["user"]=user
                    return redirect("tenantdashboard")  # Redirect to the homepage or dashboard
                elif(user["userType"]=="consumer"):
                    #print('consumer')
                    user.pop("_id");#user.pop("password");#user.pop("created_by");user.pop("usertype")
                    #print(user)
                    request.session["user"]=user
                    #usersWrapper.updateUser(user["userEmail"],profilePic="UPDATED BASE 64 string")
                    #print("redirecting to user_dashboard.html")
                    return redirect("user_dashboard")  # Redirect to the homepage or dashboard
            else:
                return render(request, "login.html",{'Error': "Invalid username or password"})
        else:
            return render(request, "login.html",{'Error': "Invalid username or password"})

    return render(request, "login.html",{'nActiveUsers': f"Currently Active: {nSessions} users"})

def tenantdashboard(request):
    return render(request,"TenantAdmin/newtenantadmin_dashboard.html", {'user':request.session.get("user")})
def user_dashboard(request):
    return render(request, 'usersdashboard.html', {'user': request.session.get("user")})
# def user_dashboard(request):
#     #print('views.py')
#     return render(request, 'usersdashboard.html', {'user': request.user})


def logout_view(request):
    print('cleared')
    request.session.flush()  
    return redirect('login')


# def dashboard_view(request):
#     if "user_id" not in request.session:
#         return JsonResponse({"error": "Unauthorized access"}, status=401)
#     return render(request, "superadmin_dashboard.html")

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
            hashed_password = "Exception" #bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            try:
                usersWrapper.addTenantAdmin(username, email, hashed_password, tenantName,jwt = request.session["jwt"])  
                messages.success(request, "TenantAdmin added successfully!")
                return redirect("sidebar_option", option="tenant")
            except Exception as e:
                print(f"Error adding Tenant Admin: {e}")
                #messages.error(request, f"Error adding Tenant Admin: {e}")

def SubmitTenant(request):
    print("XXXXXSubmitTenantClicked")
    if request.method == 'POST':
        option = request.POST.get("option")
        tenantName = request.POST.get("tenantName") #this shoiuld be tenantName
        #user_id = request.session.get("user_id")  #TODO: actually this userid is not needed here.
        # Process the form data here
        print("Option:", option);print("tenant Name:", tenantName)
        if tenantName:
            try:
                usersWrapper.createTenant(tenantName,jwt = request.session["jwt"])
                messages.success(request, "Tenant added successfully!")
                #print("tenant added successfully")
                return redirect("sidebar_option", option="tenant")
            except Exception as e:
                messages.error(request, f"Error adding Tenant: {e}")
    pass
def SubmitConsumer(request):
    user_id = request.session.get("user_id")  
    if request.method == "POST":
        print("Received POST request")  
        print("POST Data:", request.POST)  

        option = request.POST.get("option")
        print("Option:", option)
        if option == "consumer":
            #print("DBG: Option is consumer")
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            tenantName = request.POST.get("tenant")
            tenantName = request.session.get("tenantName") #request.POST.get("tenantName")
            #print("DBG: after getting the values")
            if username and email and password:
                print("DBG: username, email, password, tenantName:", username, email, password, tenantName)
                hashed_password = "Exception" #bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                #TODO: commented out the above portion because we are getting exception when deployed on render
                #print("DBG: hashedd_password:", hashed_password)
                try:
                    print("DBG:Before calling createUser")
                    usersWrapper.createUser(username, email, hashed_password, tenantName, "consumer",jwt = request.session["jwt"])
                    print("Consumer added successfully")
                    messages.success(request, "Consumer added successfully!")
                    return redirect("sidebar_option", option="users")
                except Exception as e:
                    print("Error in adding consumer:", e)
                    messages.error(request, f"Error adding Consumer: {e}")

def sidebar(request, option=None):
    user_id = request.session.get("user_id")
    print("Side bar Option Clicked: ", option)  # Debugging

    records = []
    total_tenants = 0
    total_superadmins = 0

    if option == "users":#This is when tenant admin logs in
        print("Fetching users data...")
        users_data = usersWrapper.getUsersForTenantAdmin(user_id,jwt = request.session["jwt"])

        print("Fetched Users Data:", users_data)
        records = users_data  
        template = "tenantadmin_dashboard.html"
    
    # elif option == "tenantDummy": #this is unused and dummy
    #     tenants_data = []
    #     template = "d-ashboard.html"

    elif option == "tenant": #this is the actual SuperAdmin Dashboard to add Tenants
        total_superadmins = 0 #users_collection.count_documents({"usertype": "superadmin"})
        #TODO: we may not need the above anymore for now.
        records = usersWrapper.getTenants(jwt = request.session["jwt"])
        for tenant in records:
            tenant["tenantName"]=tenant["_id"] #stupid workaround to get the tenant name. otherwise _id is not getting displayed in javascript
            print(tenant)
        total_tenants = len(records)
        template = "superadmin_dashboard.html"

    context = {
        "option": option,
        "tenant_data": records,
        "records": records,
        "total_tenants": total_tenants,
        "total_superadmins": total_superadmins
    }

    return render(request, template, context)


def settings_view(request):
    return render(request, 'settings.html')

def tenantGroups(request):
    print("loading TenantGroupsPage")
    #return render(request, 'TenantAdmin/groupUsers.html', {'user': request.session.get("user")})
    return render(request, 'TenantAdmin/tenantGroups.html', {'user': request.session.get("user")})

def Rankcard(request):
    print("loading RankcardPage")
    return render(request, 'TenantAdmin/Rankcard.html', {'user': request.session.get("user")})

def groupUsers(request):
    return render(request, 'TenantAdmin/groupUsers.html', {'user': request.session.get("user")})

def getTenantadminForTenant(request):
    try:
        tenantName = request.session.get("tenantName")
        if not tenantName:
            # Try to get tenantName from POST data
            if request.method == "POST":
                import json
                data = json.loads(request.body.decode("utf-8"))
                tenantName = data.get("tenantName")
        if not tenantName:
            print("Error: tenantName not found in session or POST data")
            return JsonResponse({"error": "Tenant name not found"}, status=400)
        adminsData = usersWrapper.getTenantadminForTenant(tenantName,jwt = request.session["jwt"])
        print("getAdminDetails Response:", adminsData)
        return JsonResponse(adminsData, safe=False)
    except Exception as e:
        print(f"Error in getTenantadminForTenant: {e}")
        return JsonResponse({"error": str(e)}, status=500)

#Sample POST request
@require_http_methods(['POST'])
@csrf_exempt
def SamplePOSTAPI(request):
    input = json.loads(request.body)
    retJson = "{}"
    return JsonResponse(retJson, safe=False)

#Sample POST request
@require_http_methods(['POST'])
def getGroupsForTenant(request):
    print("DBG: ********getGroupsForTenant called")
    try:
        data = json.loads(request.body)
        tenantName = data.get("tenantName")
        if not tenantName:
            # Try to get tenantName from POST data
            if request.method == "POST":
                #import json
                data = json.loads(request.body.decode("utf-8"))
                tenantName = data.get("tenantName")
        if not tenantName:
            print("Error: tenantName not found in session or POST data")
            return JsonResponse({"error": "Tenant name not found"}, status=400)
        groupData = usersWrapper.getUserGroupsForTenant(tenantName,jwt = request.session["jwt"])
        print("getAdminDetails Response:", groupData)
        return JsonResponse(groupData, safe=False)
    except Exception as e:
        print(f"Error in getTenantadminForTenant: {e}")
        return JsonResponse({"error": str(e)}, status=500)
    pass
@require_http_methods(['POST'])
def usersForTheTenant(request):
    try:
        data = json.loads(request.body)
        tenantName = data.get("tenantName")
        groupName = data.get("groupName")
        
        print("tenantName:", tenantName, "groupName:", groupName)
        if not tenantName or not groupName:
            print("Missing parameters")
            return JsonResponse({"error": "Missing parameters"}, status=400)

        try:
            userData = usersWrapper.getUsersInGroup(groupName, tenantName,jwt = request.session["jwt"])
            print("userData from API:", userData)
        except requests.exceptions.RequestException as e:
            print("API request failed:", str(e))
            return JsonResponse({"error": f"API request failed: {str(e)}"}, status=500)
        except Exception as e:
            print("Error calling getUsersInGroup:", str(e))
            return JsonResponse({"error": f"Error getting users: {str(e)}"}, status=500)

        # Defensive: handle None or unexpected types
        if not userData:
            print("No user data returned from API")
            return JsonResponse([], safe=False)

        # Handle different response formats
        user_list = []
        if isinstance(userData, dict):
            if "users" in userData:
                user_list = userData["users"]
            elif "error" in userData:
                print("API returned error:", userData["error"])
                return JsonResponse({"error": userData["error"]}, status=400)
            else:
                user_list = [userData]  # Single user object
        elif isinstance(userData, list):
            user_list = userData
        else:
            print("Unexpected userData type:", type(userData))
            return JsonResponse([], safe=False)

        # Map users to consistent format
        mapped_users = []
        for user in user_list:
            try:
                if isinstance(user, dict):
                    mapped_users.append({
                        "id": user.get("id") or user.get("_id") or "N/A",
                        "username": user.get("username") or user.get("userName") or "N/A",
                        "email": user.get("email") or user.get("userEmail") or "N/A",
                        "groupname": user.get("groupname") or user.get("userGroup") or user.get("groupName") or groupName
                    })
                elif isinstance(user, str):
                    mapped_users.append({
                        "id": "N/A",
                        "username": "N/A",
                        "email": user,
                        "groupname": groupName
                    })
                else:
                    print(f"Skipping invalid user data: {user}")
                    continue
            except Exception as e:
                print(f"Error mapping user {user}: {str(e)}")
                continue

        print("mapped_users:", mapped_users)
        return JsonResponse(mapped_users, safe=False)
    except json.JSONDecodeError as e:
        print("JSON decode error:", str(e))
        return JsonResponse({"error": "Invalid JSON in request"}, status=400)
    except Exception as e:
        print("Exception in usersForTheTenant:", str(e))
        return JsonResponse({"error": str(e)}, status=500)

# groupcreation
# Add this at the top of views_admin.py
test_groups = []  # Global variable to store test data

@require_http_methods(['POST'])
@csrf_exempt  # Remove this in production once CSRF is properly handled
def addGroupToTenant(request):
    try:
        # Parse JSON data from request body
        data = json.loads(request.body)
        groupName = data.get('groupName')
        tenantName = data.get('tenantName')

        print("Received:", groupName, tenantName)

        if not all([groupName, tenantName]):
            return JsonResponse({"error": "All fields are required!"}, status=400)
        groupData = usersWrapper.createUserGroup(groupName, tenantName,jwt = request.session["jwt"])
        # Add to test_groups                       
        #print("getAdminDetails Response:", groupData)
        return JsonResponse(groupData, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
test_users = []  # Global variable to store test data

@require_http_methods(['POST'])
@csrf_exempt  # Remove this in production once CSRF is properly handled
def addUsersToGroup(request):
    try:
        # Parse JSON data from request body
        data = json.loads(request.body)
        userName = data.get('userName')
        email = data.get('email')
        # password = data.get('password')
        groupName = data.get('groupName')
        tenantName = data.get('tenantName')

        print("Received:", email , groupName )

        if not all([ email, groupName, tenantName ]):
             return JsonResponse({"error": "All fields are required!"}, status=400)
        usersWrapper.createUser(userName,email, "",tenantName,groupName,"consumer",jwt = request.session["jwt"])
        usersWrapper.addUserToGroup( email, groupName,  tenantName,jwt = request.session["jwt"])
        # Add to test_groups                       
        print("User added to group successfully", email)
        return JsonResponse({"status": "success"})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@require_http_methods(['POST'])
@csrf_exempt  # Remove this in production once CSRF is properly handled
def updateUser(request):
    input = json.loads(request.body)
    print("input:", input)
    user = input.get('user')
    email = user.get('userEmail')
    profilePic = user.get('profilePic')
    usersWrapper.updateUser(email, profilePic = profilePic,jwt = request.session["jwt"])
    retJson = "{}"
    return JsonResponse(retJson, safe=False)
    pass

def aiassistant(request):
    return render(request, 'ai_assistant.html')
    

#Sample POST request
@require_http_methods(['POST'])
@csrf_exempt
def getGroupwiseRanks(request):
    input = json.loads(request.body)
    tenantName = input.get('tenantName')
    userGroups = input.get('userGroups')

    retJson = usersWrapper.getGroupwiseRanks(tenantName,userGroups,jwt = request.session["jwt"])
    return JsonResponse(retJson, safe=False)
    
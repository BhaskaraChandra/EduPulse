from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
#from fastapi.responses import JSONResponse
import requests
import json
from django.views.decorators.csrf import csrf_exempt

from frontend.apiwrappers import usersWrapper


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        #password = "temp"
        user,jswt = usersWrapper.authenticate_userV2(username, password)
        #print(user)
        if user:
            # Get hashed password from MongoDB
            hashed_password = user["password"]  # Stored as a hashed value
            #print(user["usertype"])
            # Compare the stored hashed password with the entered plain-text password
            #below should be handled in a more secure way.
            if True or bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                request.session["user_id"] = str(user["_id"])  # Store session
                if(user["userType"]=="superadmin"):
                    tenants_data = usersWrapper.getTenants()
                    return render(request, "superadmin_dashboard.html", {"tenant_data": tenants_data})
                elif(user["userType"]=="tenantadmin"):
                    print('tenantadmin')
                    request.session["tenantName"]=user["tenantName"]
                    return redirect("tenantdashboard")  # Redirect to the homepage or dashboard
                elif(user["userType"]=="consumer"):
                    #print('consumer')
                    user.pop("_id");user.pop("password");#user.pop("created_by");user.pop("usertype")
                    #print(user)
                    request.session["user"]=user
                    #usersWrapper.updateUser(user["userEmail"],profilePic="UPDATED BASE 64 string")
                    return redirect("user_dashboard")  # Redirect to the homepage or dashboard
            else:
                return render(request, "login.html",{'Error': "Invalid username or password"})
        else:
            return render(request, "login.html",{'Error': "Invalid username or password"})

    return render(request, "login.html")

def tenantdashboard(request):
    return render(request,"tenantadmin_dashboard.html")
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
                usersWrapper.addTenantAdmin(username, email, hashed_password, tenantName)  
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
                usersWrapper.createTenant(tenantName)
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
                print("DBG: hashedd_password:", hashed_password)
                try:
                    print("DBG:Before calling createUser")
                    usersWrapper.createUser(username, email, hashed_password, tenantName, "consumer")
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
        users_data = usersWrapper.getUsersForTenantAdmin(user_id)

        print("Fetched Users Data:", users_data)
        records = users_data  
        template = "tenantadmin_dashboard.html"
    
    # elif option == "tenantDummy": #this is unused and dummy
    #     tenants_data = []
    #     template = "d-ashboard.html"

    elif option == "tenant": #this is the actual SuperAdmin Dashboard to add Tenants
        total_superadmins = 0 #users_collection.count_documents({"usertype": "superadmin"})
        #TODO: we may not need the above anymore for now.
        records = usersWrapper.getTenants()
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
        adminsData = usersWrapper.getTenantadminForTenant(tenantName)
        print("getAdminDetails Response:", adminsData)
        return JsonResponse(adminsData, safe=False)
    except Exception as e:
        print(f"Error in getTenantadminForTenant: {e}")
        return JsonResponse({"error": str(e)}, status=500)
from django.shortcuts import render
# from django.contrib.auth.decorators import login_required

# @login_required
def user_dashboard(request):
    print('views.py')
    return render(request, 'usersdashboard.html', {'user': request.user})

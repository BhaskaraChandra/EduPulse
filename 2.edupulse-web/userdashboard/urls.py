
from django.urls import path
from .views import user_dashboard

# urlpatterns = [
#     path("", login_view, name="login"),
#     path("logout/", logout_view, name="logout"),
#     path("dashboard/", dashboard, name="dashboard"),
#     path("sidebar/", sidebar, name="sidebar"),
#     path("<str:option>/", sidebar, name="sidebar_option"),
# ]
urlpatterns = [
    path('usersdashboard/', user_dashboard, name='user_dashboard'),
]


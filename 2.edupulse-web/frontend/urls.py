from django.urls import path
from .views import sidebar, login_view, logout_view, dashboard,tenantdashboard,user_dashboard

# urlpatterns = [
#     path("", login_view, name="login"),
#     path("logout/", logout_view, name="logout"),
#     path("dashboard/", dashboard, name="dashboard"),
#     path("sidebar/", sidebar, name="sidebar"),
#     path("<str:option>/", sidebar, name="sidebar_option"),
# ]
urlpatterns = [
    path("", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
    path("tenantdashboard/", tenantdashboard, name="tenantdashboard"),
    path("sidebar/<str:option>/", sidebar, name="sidebar_option"),
    path('usersdashboard/', user_dashboard, name='user_dashboard'),
]


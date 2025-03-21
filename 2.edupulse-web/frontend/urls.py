from django.urls import path

from .views import (SubmitTenant, sidebar, login_view, logout_view, dashboard,tenantdashboard,user_dashboard, tests_view, create_test_view, daily_challenge_view,
history_view, topics_view, manage_topics_view,dashboards_view, my_progress_view, compare_view, settings_view,SubmitTenantAdmin)

# from .views import SubmitTenant, SubmitTenantAdmin, sidebar, login_view, logout_view, dashboard,tenantdashboard,user_dashboard
# >>>>>>> 58cdca6496046725c5892ee01285312875b23908

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
    path("SubmitTenant/", SubmitTenant, name="SubmitTenant"),
    path("SubmitTenantAdmin/", SubmitTenantAdmin, name="SubmitTenantAdmin"),
    path('usersdashboard/', user_dashboard, name='user_dashboard'),
    path('tests/', tests_view, name='tests'),
    path('create_test/', create_test_view, name='create_test'),
    path('daily_challenge/', daily_challenge_view, name='daily_challenge'),
    path('history/', history_view, name='history'),
    path('topics/', topics_view, name='topics'),
    path('manage_topics/', manage_topics_view, name='manage_topics'),
    path('dashboards/', dashboards_view, name='dashboards'),
    path('my_progress/', my_progress_view, name='my_progress'),
    path('compare/', compare_view, name='compare'),
    path('settings/', settings_view, name='settings'),
    
    
    
    
]


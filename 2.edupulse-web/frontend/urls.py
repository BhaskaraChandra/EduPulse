from django.urls import path

from frontend.view_admin import Rankcard, SubmitConsumer, SubmitTenant, SubmitTenantAdmin, addGroupToTenant, addUsersToGroup, aiassistant, getGroupsForTenant, getGroupwiseRanks, getTenantadminForTenant, groupUsers, login_view, logout_view, settings_view, sidebar, tenantGroups, tenantdashboard, updateUser, user_dashboard, usersForTheTenant
from frontend.view_tests import compare_view, create_test_view, daily_challenge_view, dashboards_view, generate_test, get_active_quick_test, livetest, manage_topics_view, metrics_view, my_progress_view, save_selected_topics, submit_test, testSummary,history_view, tests_view, topics_view


urlpatterns = [
    #Admin paths
    path("", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("tenantdashboard/", tenantdashboard, name="tenantdashboard"),
    path('usersdashboard/', user_dashboard, name='user_dashboard'),
    path("sidebar/<str:option>/", sidebar, name="sidebar_option"),
    path("SubmitTenant/", SubmitTenant, name="SubmitTenant"),
    path("SubmitTenantAdmin/", SubmitTenantAdmin, name="SubmitTenantAdmin"),
    path("SubmitConsumer/", SubmitConsumer, name="SubmitConsumer"),
    #path("dashboard/", dashboard, name="dashboard"),
    path('tenantGroups/', tenantGroups, name='tenantGroups'),
    path('groupUsers/', groupUsers, name='groupUsers'),
    path('Rankcard/', Rankcard, name='Rankcard'),
    #path('usersdashboard/', user_dashboard, name='user_dashboard'),
    path('getTenantadminForTenant/', getTenantadminForTenant, name='getTenantadminForTenant'),
    path('getGroupsForTenant/', getGroupsForTenant, name="getGroupsForTenant"),
    path('usersForTheTenant/', usersForTheTenant, name="usersForTheTenant"),
    path('addGroupToTenant/', addGroupToTenant, name="addGroupToTenant"),
    path('addUsersToGroup/', addUsersToGroup, name="addUsersToGroup"),
    path('updateUser/', updateUser, name='updateUser'),

    #enduser paths
    path('settings/', settings_view, name='settings'),
    path('getTenantadminForTenant/', getTenantadminForTenant, name='getTenantadminForTenant'),
    
    path('tests/', tests_view, name='tests'),
    path('create_test/', create_test_view, name='create_test'),
    path('daily_challenge/', daily_challenge_view, name='daily_challenge'),
    path('topics/', topics_view, name='topics'),
    path('manage_topics/', manage_topics_view, name='manage_topics'),
    path('dashboards/', dashboards_view, name='dashboards'),
    path('my_progress/', my_progress_view, name='my_progress'),
    path('compare/', compare_view, name='compare'),
    
    path('api/topics/', save_selected_topics, name='save_selected_topics'),
    #tests related

    path('generate_test/', generate_test, name='generate_test'),
    path('get_active_quick_test/', get_active_quick_test, name='get_active_quick_test'),
    path('get_active_quick_test/<str:curUser_email>/', get_active_quick_test, name='get_active_quick_test'),
    path('livetest/', livetest, name='livetest'),
    path('submit_test/', submit_test, name='submit_test'),
    path('testSummary/', testSummary, name='testSummary'),
    path('history/', history_view, name='history'),
    path('metrics/', metrics_view, name='metrics'),

    path('getGroupwiseRanks/', getGroupwiseRanks, name='getGroupwiseRanks'),
    path('aiassistant/', aiassistant, name='aiassistant'),


]


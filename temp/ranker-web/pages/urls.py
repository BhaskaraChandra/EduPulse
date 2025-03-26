from django.urls import path
from pages import views

urlpatterns = [
    path("", views.home, name="home"),
    path("createtest", views.createtest, name="createtest"),
    #path('select_subject/', views.select_subject, name='select_subject'),
    path('create_test/', views.create_test, name='create_test'),
    path('live_test/', views.live_test, name='live_test'),
    path('get_question/', views.get_question, name='get_question'),
    path('image/', views.image_view, name='image_view'),

]
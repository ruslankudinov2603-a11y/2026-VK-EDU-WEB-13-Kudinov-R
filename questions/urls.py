from django.urls import path
from . import views

urlpatterns = [
    path('ask/', views.ask, name='ask'),
    path('question/<int:question_id>/', views.question, name='question'),
]
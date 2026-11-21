from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('hot/',  views.hot, name='hot'),
    path('tag/<str:tag_name>/', views.tag, name='tag'),
    path('answer/<int:answer_id>/correct/',views.mark_correct,name='mark_correct'),
    path('logout/', views.logout, name='logout'),
    path('ask/', views.ask, name='ask'),
    path('question/<int:question_id>/', views.question, name='question'),
    path('question/<int:question_id>/like/', views.question_like, name='question_like'),
    path('answer/<int:answer_id>/like/', views.answer_like, name='answer_like'),
]
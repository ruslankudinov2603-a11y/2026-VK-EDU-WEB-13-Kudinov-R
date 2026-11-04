from django.shortcuts import render
from django.core.paginator import Paginator

# Create your views here.

def index(request):
    questions = []

    for i in range(1,30):
        questions.append({
            'title': 'Вопрос №' + str(i),
            'id': i,
            'text': 'Текст вопроса №' + str(i)
        })
    paginator = Paginator(questions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/index.html', {
        'questions': page_obj,
        'page_obj': page_obj,
    })

def login(request):
    return render(request, 'core/login.html')

def signup(request):
    return render(request, 'core/signup.html')

def profile(request):
    return render(request, 'core/profile.html')

def hot(request):
    questions = []

    for i in range(1, 11):
        questions.append({
            'title': 'Популярный вопрос №' + str(i),
            'id': i,
            'text': 'Текст популярного вопроса №' + str(i),
        })

    paginator = Paginator(questions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/hot.html', {
        'questions': page_obj,
        'page_obj': page_obj,
    })

def tag(request, tag_name):
    questions = []

    for i in range(1, 11):
        questions.append({
            'title': 'Вопрос №' + str(i) + ' по тегу ' + tag_name,
            'id': i,
            'text': 'Текст вопроса по тегу ' + tag_name,
        })

    paginator = Paginator(questions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/tag.html', {
        'questions': page_obj,
        'page_obj': page_obj,
        'tag_name': tag_name,
    })
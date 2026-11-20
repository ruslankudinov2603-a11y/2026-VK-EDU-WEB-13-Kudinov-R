from django.shortcuts import render, get_object_or_404
from questions.models import Question, Tag
from .pagination import paginate


def index(request):
    questions = Question.objects.newest().select_related('author').prefetch_related('tags')
    page_obj = paginate(questions, request)
    return render(request, 'core/index.html', {'questions': page_obj, 'page_obj': page_obj})


def login(request):
    return render(request, 'core/login.html')


def signup(request):
    return render(request, 'core/signup.html')


def profile(request):
    return render(request, 'core/profile.html')


def hot(request):
    questions = Question.objects.popular().select_related('author').prefetch_related('tags')
    page_obj = paginate(questions, request)
    return render(request, 'core/hot.html', {'questions': page_obj, 'page_obj': page_obj})


def tag(request, tag_name):
    tag = get_object_or_404(Tag, slug=tag_name)
    questions = tag.questions.with_counts().select_related('author').prefetch_related('tags')
    questions = questions.order_by('-created_at')
    page_obj = paginate(questions, request)
    return render(request, 'core/tag.html', {
        'questions': page_obj,
        'page_obj': page_obj,
        'tag_name': tag.name,
    })

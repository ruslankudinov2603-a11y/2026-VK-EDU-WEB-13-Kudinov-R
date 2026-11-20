from django.contrib import admin
from .models import Tag, Question, Answer, QuestionLike, AnswerLike


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    autocomplete_fields = ['author']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'text', 'author__username')
    list_filter = ('created_at', 'tags')
    filter_horizontal = ('tags',)
    inlines = [AnswerInline]
    autocomplete_fields = ['author']
    list_select_related = ('author',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'author', 'created_at')
    search_fields = ('text', 'author__username', 'question__title')
    list_filter = ('created_at',)
    autocomplete_fields = ['author', 'question']
    list_select_related = ('author', 'question')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


@admin.register(QuestionLike)
class QuestionLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'question')
    search_fields = ('user__username', 'question__title')
    autocomplete_fields = ['user', 'question']
    list_select_related = ('user', 'question')


@admin.register(AnswerLike)
class AnswerLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'answer')
    search_fields = ('user__username', 'answer__text')
    autocomplete_fields = ['user', 'answer']
    list_select_related = ('user', 'answer')

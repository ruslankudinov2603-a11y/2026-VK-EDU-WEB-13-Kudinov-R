from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count



class QuestionManager(models.Manager):

    def with_counts(self):
        return self.get_queryset().annotate(
            likes_count=Count('likes', distinct=True),
            answers_count=Count('answers', distinct=True),
        )

    def newest(self):
        return self.with_counts().order_by('-created_at')

    def popular(self):
        return self.with_counts().order_by('-likes_count', '-created_at')


class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='URL'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Заголовок'
    )
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='Автор'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='questions',
        blank=True,
        verbose_name='Теги'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    objects = QuestionManager()

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Вопрос'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        ordering = ['created_at']

    def __str__(self):
        return f'Ответ на вопрос: {self.question.title}'


class QuestionLike(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='question_likes',
        verbose_name='Пользователь'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='Вопрос'
    )

    class Meta:
        verbose_name = 'Лайк вопроса'
        verbose_name_plural = 'Лайки вопросов'
        unique_together = ('user', 'question')

    def __str__(self):
        return f'{self.user} — {self.question}'


class AnswerLike(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='answer_likes',
        verbose_name='Пользователь'
    )
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='Ответ'
    )

    class Meta:
        verbose_name = 'Лайк ответа'
        verbose_name_plural = 'Лайки ответов'
        unique_together = ('user', 'answer')

    def __str__(self):
        return f'{self.user} — {self.answer}'

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from core.models import Profile
from questions.models import Question, Answer


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Email'
    )

    first_name = forms.CharField(
        max_length=150,
        required=True,
        label='Имя'
    )

    last_name = forms.CharField(
        max_length=150,
        required=True,
        label='Фамилия'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar',)

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')

        if avatar:
            if avatar.size > 2 * 1024 * 1024:
                raise forms.ValidationError(
                    'Размер изображения не должен превышать 2 МБ.'
                )

            content_type = getattr(avatar.file, 'content_type', None)

            if content_type not in ['image/jpeg', 'image/png']:
                raise forms.ValidationError(
                    'Разрешены только изображения JPG и PNG.'
                )

        return avatar


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'text', 'tags')


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text',)
from django import forms

from . import models


class SkillForm(forms.ModelForm):
    class Meta:
        model = models.Skill
        fields = ('name', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'input',
            })


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        exclude = ['password', 'groups', 'user_permissions', 'is_superuser', 'is_staff', 'last_login']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'input',
            })


class MessageForm(forms.ModelForm):
    class Meta:
        model = models.Message
        fields = ['fullname', 'email', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'input'
            })



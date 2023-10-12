from django import forms

from . import models


class ProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        exclude = ['owner', 'tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'input',
            })

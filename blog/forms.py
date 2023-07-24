from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea(attrs={'col': 40, 'row': 20}))

# For a list of all form fields available, you can visit
# https://docs.djangoproject.com/en/3.0/ref/forms/fields/.


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = {'name', 'email', 'body'}
        labels = {'name': 'Enter name', 'email': 'Enter email'}
        widgets = {'body': forms.Textarea(attrs={'col': 50, 'row': 20})}


class SearchForm(forms.Form):
    query = forms.CharField()


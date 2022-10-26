from django import forms


class EmailPostForm(forms.Form):
    your_name = forms.CharField(max_length=25)
    your_email = forms.EmailField()
    question = forms.CharField(required=False, widget=forms.Textarea)
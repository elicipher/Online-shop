from django import forms


class UploadObjectForm(forms.Form):
    img = forms.FileField()
    
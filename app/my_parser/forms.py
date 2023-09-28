from django import forms

class LinkForm(forms.Form):
    name = form.TextField(help_text = "Введите ссылку")

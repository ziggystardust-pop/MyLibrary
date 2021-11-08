
from django import forms


class SearchForm(forms.Form):
    keyword = forms.CharField(label="关键词", max_length=60,
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入关键词'}))

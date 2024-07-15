from django import forms
from .models import Resource, Domain

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'description', 'category', 'file', 'domain']
        
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    category = forms.ChoiceField(choices=Resource.CATEGORY_CHOICES)
    file = forms.FileField()
    domain = forms.ModelChoiceField(queryset=Domain.objects.all())
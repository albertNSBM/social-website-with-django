from django import forms
from .models import Image
from django.core.files.base import ContentFile
import requests
from django.utils.text import slugify


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model=Image
        fields=['title','slug','description','image','user','user_likes']
         
        
    
            
            
            
from django import forms
from .models import Image
from django.core.files.base import ContentFile
import requests
from django.utils.text import slugify


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model=Image
        fields=['title','url','description']
        widgets={
            'url':forms.HiddenInput
        }
        
        def clean_url(self):
            url=self.clean_data['url']
            valid_extensions =['jpg','jpeg','png']
            extention=url.rsplit('.',1)[1].lower()
            if extention not in valid_extensions:
                raise forms.ValidationError('the given URL does not exist' \
                                            'match valid image extention ')
            return url 
        def save(self,
                 force_insert=False,
                 force_update=False,
                 commit=True):
            image=super().save(commit=False)
            image_url=self.clean_data['url']
            name=slugify(image.title)
            extention=image_url.rsplit('.',1)[1].lower()
            image_name=f'{name} . {extention}'
            
            response=requests.get(image_url)
            image.image.save(image_name,ContentFile(response.content),save=False)
            
            if commit:
                image.save()
            return image
            
            
            
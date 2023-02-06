from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from .models import Image
from django.http import JsonResponse,HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from actions.utils import create_action

# Create your views here.
@login_required
def image_create(request):
    form=ImageCreateForm(request.POST)
    if form.is_valid():
        form.save()
        create_action(request.user,'bookmarked image',form)
    return render(request,'images/image/create.html',{'form':form})
    
def image_detail(request,id,slug):
    image=get_object_or_404(Image,id=id,slug=slug)
    return render(request,
                        'images/image/detail.html',
                        {'image':image,'section':'images'})
          
@login_required
@require_POST
def image_like(request):
    image_id=request.POST.get('id')
    action=request.POST.get('action')
    if image_id and action:
        try:
            image=Image.objects.get(id=image_id)
            if action == 'like':
                image.user_likes.add(request.user)
                create_action(request.user,'likes',image)
                
            else:
                image.user_likes.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Image.DoesNotExist:
                pass
    return JsonResponse({'status': 'error'})

@login_required
def image_list(request):
    images=Image.objects.all()
    paginator=Paginator(images,4)
    page=request.GET.get('page')
    images_only=request.GET.get('images_only')
    try:
        images=paginator.page(page)
    except PageNotAnInteger:
        paginator.page(1)
    except EmptyPage:
        if images_only:
    
            return HttpResponse('')
        images=paginator.page(paginator.num_pages)
    if images_only:
        return render(request,
                      'images/image/list_image.html',{'section':'images','images':images})
    
    return render(request,'images/image/list.html',{'images':images,'section':'images'})
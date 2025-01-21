import os
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.decorators.http import require_POST

def index(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        upload_path = os.path.join(settings.MEDIA_ROOT, 'uploads', image.name)
        
        # 确保上传目录存在
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        
        # 如果文件已存在，先删除它（覆盖）
        if os.path.exists(upload_path):
            os.remove(upload_path)
            
        # 保存新文件
        with open(upload_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
                
        return HttpResponseRedirect(reverse('index'))
    
    # 获取所有已上传的图片
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    if os.path.exists(upload_dir):
        images = [f for f in os.listdir(upload_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        images = [{'name': image, 'url': f'/media/uploads/{image}'} for image in images]
    else:
        images = []
    
    return render(request, 'upload/index.html', {'images': images})

@require_POST
def delete_image(request, filename):
    # 构建文件路径
    file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', filename)
    
    # 检查文件是否存在
    if os.path.exists(file_path):
        # 删除文件
        os.remove(file_path)
        return HttpResponse('success')
    return HttpResponse('file not found', status=404)
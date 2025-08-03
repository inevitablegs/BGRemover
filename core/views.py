import os
from django.shortcuts import render, redirect
from .forms import UploadImageForm
from rembg import remove
from PIL import Image
from django.core.files.storage import default_storage

from django.shortcuts import render
from .forms import UploadImageForm
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect
from django.urls import reverse

def upload_image(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = request.FILES['image']
            path = default_storage.save(f'uploads/{image.name}', image)
            return HttpResponseRedirect(f"{reverse('result')}?image={path}")
    else:
        form = UploadImageForm()
    return render(request, 'core/upload.html', {'form': form})


def result(request):
    image_path = request.GET.get('image')
    input_path = os.path.join('media', image_path)
    output_path = input_path.replace('uploads', 'output')

    with open(input_path, 'rb') as i:
        output = remove(i.read())

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'wb') as o:
        o.write(output)

    return render(request, 'core/result.html', {
        'original': '/' + image_path,
        'processed': '/' + output_path.replace('media/', '')
    })

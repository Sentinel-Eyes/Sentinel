import os.path
import pandas as pd
from deepface import DeepFace
from django.http import JsonResponse
from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'home.html')


def webcam(request):
    return render(request, 'webcam.html')


def facial_recognition(request):
    if request.method == 'POST':
        image_data = request.POST.get('image_data')

        # Perform face recognition using DeepFace
        # You can customize this part according to your recognition needs
        # results = DeepFace.verify("static/images/kuu_c_shyn/shyn6.jpg", image_data)
        if os.path.exists("representations_vgg_face.pkl"):
            os.remove("representations_vgg_face.pkl")

        find_results = DeepFace.find(img_path=image_data, db_path="static/images/")

        response_data = []

        for result in find_results:
            identity_path = result['identity'][0]

            results = DeepFace.verify(img1_path=image_data, img2_path=identity_path)

            results_verified = bool(results['verified'])
            response_data.append({
                'identity_path': str(identity_path),
                'results_verified': results_verified
            })

        return JsonResponse(response_data, safe=False)

    return JsonResponse({'error': 'Invalid request'}, status=400)

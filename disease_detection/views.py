from .predict import predict_disease
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.utils.translation import get_language


def detect(request):

    if request.method == "POST":

        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        image_path = fs.path(filename)
        request.session['image'] = filename   # 🔥 ADD HERE

        # 🤖 prediction
        result, confidence = predict_disease(image_path)

        # 🌐 language
        lang = get_language()[:2]

        # 🌦 SMART WARNING
        if "blight" in result.lower():
            warning = "High humidity increases this disease risk" if lang == "en" else "अधिक नमी से यह रोग बढ़ सकता है"
        else:
            warning = ""

        # 🔥 simple solution mapping (NO disease_data file needed)
        if result == "Potato Early Blight":
            solution = "Use fungicide spray" if lang == "en" else "फफूंदनाशक स्प्रे करें"

        elif result == "Potato Late Blight":
            solution = "Apply fungicide immediately" if lang == "en" else "तुरंत फफूंदनाशक डालें"

        elif result == "Potato Healthy":
            solution = "No treatment required" if lang == "en" else "कोई उपचार आवश्यक नहीं है"

        else:
            solution = "Upload clearer image" if lang == "en" else "कृपया स्पष्ट तस्वीर अपलोड करें"

        # 📦 store
        request.session['disease'] = result
        request.session['solution'] = solution

        return render(request, 'result.html', {
            "result": result,
            "confidence": confidence,
            "solution": solution,
            "warning": warning
        })

    return render(request, 'upload.html')
from django.shortcuts import render, redirect
from .models import Report
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from django.utils.translation import get_language
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path

disease_data = {

    # 🌿 Healthy Leaf
    "Potato Healthy": {
        "en": {
            "description": "The plant is completely healthy with no visible disease.",
            "symptoms": "Fresh green leaves, no spots or discoloration.",
            "causes": "Proper care, watering, and nutrition.",
            "solution": "No treatment required.",
            "prevention": "Continue regular care and monitoring.",
            "soil": "Balanced soil with good nutrients."
        },
        "hi": {
            "description": "पौधा पूरी तरह स्वस्थ है और किसी रोग से प्रभावित नहीं है।",
            "symptoms": "हरे और ताज़ा पत्ते, कोई धब्बे नहीं।",
            "causes": "उचित देखभाल और पोषण।",
            "solution": "कोई उपचार आवश्यक नहीं है।",
            "prevention": "नियमित देखभाल बनाए रखें।",
            "soil": "संतुलित और उपजाऊ मिट्टी।"
        }
    },

    # 🥔 Potato Early Blight
    "Potato Early Blight": {
        "en": {
            "description": "A fungal disease causing dark spots on leaves.",
            "symptoms": "Brown circular spots with concentric rings.",
            "causes": "Alternaria solani fungus.",
            "solution": "Use fungicides.",
            "prevention": "Crop rotation.",
            "soil": "Well-drained soil."
        },
        "hi": {
            "description": "पत्तियों पर गहरे धब्बे बनाने वाली फंगल बीमारी।",
            "symptoms": "गोल भूरे धब्बे।",
            "causes": "Alternaria solani फंगस।",
            "solution": "फफूंदनाशक का उपयोग करें।",
            "prevention": "फसल चक्र अपनाएं।",
            "soil": "अच्छी जल निकासी वाली मिट्टी।"
        }
    },

    # 🥔 Potato Late Blight
    "Potato Late Blight": {
        "en": {
            "description": "Severe fungal disease affecting potatoes.",
            "symptoms": "Dark lesions and rotting leaves.",
            "causes": "Phytophthora infestans.",
            "solution": "Apply fungicides immediately.",
            "prevention": "Avoid wet conditions.",
            "soil": "Dry and aerated soil."
        },
        "hi": {
            "description": "आलू की गंभीर फंगल बीमारी।",
            "symptoms": "पत्तियों का सड़ना और काले धब्बे।",
            "causes": "Phytophthora infestans।",
            "solution": "तुरंत फफूंदनाशक डालें।",
            "prevention": "अधिक नमी से बचें।",
            "soil": "सूखी और हवादार मिट्टी।"
        }
    },

    # 🍅 Tomato Early Blight
    "Tomato Early Blight": {
        "en": {
            "description": "Common fungal disease in tomato plants.",
            "symptoms": "Dark spots with concentric rings.",
            "causes": "Alternaria solani fungus.",
            "solution": "Apply fungicides regularly.",
            "prevention": "Crop rotation and spacing.",
            "soil": "Well-drained soil."
        },
        "hi": {
            "description": "टमाटर में पाई जाने वाली सामान्य फंगल बीमारी।",
            "symptoms": "गोल धब्बे जिनमें छल्ले होते हैं।",
            "causes": "Alternaria solani फंगस।",
            "solution": "नियमित फफूंदनाशक का उपयोग करें।",
            "prevention": "फसल चक्र अपनाएं।",
            "soil": "अच्छी जल निकासी वाली मिट्टी।"
        }
    },

    # 🍅 Tomato Late Blight
    "Tomato Late Blight": {
        "en": {
            "description": "Serious disease causing rapid decay.",
            "symptoms": "Dark wet patches on leaves.",
            "causes": "Phytophthora infestans.",
            "solution": "Use fungicide immediately.",
            "prevention": "Avoid excess moisture.",
            "soil": "Dry soil."
        },
        "hi": {
            "description": "गंभीर बीमारी जो तेजी से फैलती है।",
            "symptoms": "पत्तियों पर काले गीले धब्बे।",
            "causes": "Phytophthora infestans।",
            "solution": "तुरंत फफूंदनाशक का उपयोग करें।",
            "prevention": "अधिक नमी से बचें।",
            "soil": "सूखी मिट्टी।"
        }
    },

    # 🌿 Leaf Mold
    "Leaf Mold": {
        "en": {
            "description": "Fungal disease affecting leaves.",
            "symptoms": "Yellow spots and mold growth.",
            "causes": "High humidity.",
            "solution": "Improve airflow.",
            "prevention": "Avoid overcrowding.",
            "soil": "Well-drained soil."
        },
        "hi": {
            "description": "पत्तियों को प्रभावित करने वाली फंगल बीमारी।",
            "symptoms": "पीले धब्बे और फफूंदी।",
            "causes": "अधिक नमी।",
            "solution": "वेंटिलेशन सुधारें।",
            "prevention": "भीड़ से बचें।",
            "soil": "अच्छी जल निकासी वाली मिट्टी।"
        }
    },

    # 🌿 Powdery Mildew
    "Powdery Mildew": {
        "en": {
            "description": "White powder-like fungus on leaves.",
            "symptoms": "White powder coating.",
            "causes": "Dry weather fungus.",
            "solution": "Apply sulfur fungicide.",
            "prevention": "Maintain spacing.",
            "soil": "Balanced soil."
        },
        "hi": {
            "description": "पत्तियों पर सफेद पाउडर जैसी फफूंदी।",
            "symptoms": "सफेद परत।",
            "causes": "सूखे मौसम की फंगस।",
            "solution": "सल्फर स्प्रे करें।",
            "prevention": "दूरी बनाए रखें।",
            "soil": "संतुलित मिट्टी।"
        }
    },

    # 🌿 Leaf Spot
    "Leaf Spot": {
        "en": {
            "description": "Disease causing spots on leaves.",
            "symptoms": "Brown or black spots.",
            "causes": "Bacterial or fungal infection.",
            "solution": "Remove infected leaves.",
            "prevention": "Avoid wet leaves.",
            "soil": "Balanced nutrients."
        },
        "hi": {
            "description": "पत्तियों पर धब्बे बनने वाली बीमारी।",
            "symptoms": "भूरे या काले धब्बे।",
            "causes": "बैक्टीरिया या फंगस।",
            "solution": "संक्रमित पत्तियां हटाएं।",
            "prevention": "पत्तियों को गीला न रखें।",
            "soil": "संतुलित पोषक तत्व।"
        }
    },

    # 🌾 Rust
    "Rust": {
        "en": {
            "description": "Fungal disease causing rust-colored spots.",
            "symptoms": "Orange or brown powder spots.",
            "causes": "Fungal spores.",
            "solution": "Apply fungicides.",
            "prevention": "Improve air circulation.",
            "soil": "Healthy soil."
        },
        "hi": {
            "description": "जंग जैसे धब्बे बनने वाली फंगल बीमारी।",
            "symptoms": "नारंगी या भूरे धब्बे।",
            "causes": "फंगल स्पोर्स।",
            "solution": "फफूंदनाशक का उपयोग करें।",
            "prevention": "हवा का प्रवाह बनाए रखें।",
            "soil": "स्वस्थ मिट्टी।"
        }
    },

    # 🦠 Bacterial Blight
    "Bacterial Blight": {
        "en": {
            "description": "Bacterial infection damaging crops.",
            "symptoms": "Water-soaked lesions.",
            "causes": "Bacteria.",
            "solution": "Use resistant seeds.",
            "prevention": "Avoid overwatering.",
            "soil": "Clean soil."
        },
        "hi": {
            "description": "बैक्टीरिया से होने वाली बीमारी।",
            "symptoms": "गीले धब्बे।",
            "causes": "बैक्टीरिया।",
            "solution": "प्रतिरोधी बीज उपयोग करें।",
            "prevention": "अधिक पानी से बचें।",
            "soil": "साफ मिट्टी।"
        }
    }

}

@login_required
def generate_report(request):

    if request.method == "POST":

        disease_raw = request.POST.get("disease")

        disease = request.POST.get("disease")
        filename = request.session.get('image')   # 🔥 ADD HERE
        lang = get_language()[:2]
        

        data = disease_data.get(disease, {}).get(lang) \
            or disease_data.get(disease, {}).get("en", {})

        print("DISEASE:", disease)
        print("DATA:", data)

        report = Report.objects.create(
            user=request.user,
            disease=disease,
            description=data.get("description"),
            symptoms=data.get("symptoms"),
            causes=data.get("causes"),
            solution=data.get("solution"),
            prevention=data.get("prevention"),
            soil=data.get("soil"),
            language=lang,
            image=filename
        )

        return render(request, "reports.html", {"single_report": report})

    return redirect('dashboard')
    
def view_reports(request):

    reports = Report.objects.filter(user=request.user).order_by('-created_at')

    return render(request, "reports.html", {
        "reports": reports
    })

from django.utils.translation import get_language
import os
from django.conf import settings

def download_report(request, report_id):

    report = Report.objects.get(id=report_id)

    # 🌐 Detect language
    lang = report.language  # 'en' or 'hi'

    # 🗣️ Labels based on language
    if lang == "hi":
        labels = {
            "title": "🌾 किसान एआई रोग रिपोर्ट",
            "report_id": "रिपोर्ट आईडी",
            "date": "तारीख",
            "field": "फ़ील्ड",
            "details": "विवरण",
            "disease": "रोग",
            "description": "विवरण",
            "symptoms": "लक्षण",
            "causes": "कारण",
            "treatment": "उपचार",
            "prevention": "रोकथाम",
            "soil": "मिट्टी देखभाल",
            "disclaimer_title": "⚠ चेतावनी",
            "disclaimer_text": "यह रिपोर्ट एआई आधारित प्रणाली द्वारा बनाई गई है। कृपया कृषि विशेषज्ञ से सलाह लें।",
            "footer": "© 2026 किसान एआई सिस्टम | स्मार्ट खेती समाधान 🌱",
        }
    else:
        labels = {
            "title": "🌾 Farmers AI Disease Report",
            "report_id": "Report ID",
            "date": "Date",
            "field": "Field",
            "details": "Details",
            "disease": "Disease",
            "description": "Description",
            "symptoms": "Symptoms",
            "causes": "Causes",
            "treatment": "Treatment",
            "prevention": "Prevention",
            "soil": "Soil Care",
            "disclaimer_title": "⚠ Disclaimer",
            "disclaimer_text": "This report is generated using AI-based crop disease detection. Consult an agriculture expert for confirmation.",
            "footer": "© 2026 Farmers AI System | Smart Farming Solution 🌱",
        }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="report_{report.id}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)

    font_path = os.path.abspath(os.path.join(settings.BASE_DIR, "fonts", "Noto.ttf"))

    print("FONT PATH:", font_path)  # debug

    if not os.path.exists(font_path):
        raise Exception(f"Font file not found at {font_path}")

    pdfmetrics.registerFont(TTFont('HindiFont', font_path))

    styles = getSampleStyleSheet()
    if lang == "hi":
        font_name = "HindiFont"
    else:
        font_name = "Helvetica"

    styles['Normal'].fontName = 'HindiFont'
    styles['Title'].fontName = 'HindiFont'
    styles['Heading3'].fontName = 'HindiFont'
    styles['Italic'].fontName = 'HindiFont'

    # 🎨 Styles
    title_style = ParagraphStyle(
        'title',
        parent=styles['Title'],
        fontName=font_name, 
        textColor=colors.darkgreen,
        spaceAfter=20
    )

    section_style = ParagraphStyle(
        'section',
        parent=styles['Heading3'],
        fontName=font_name, 
        textColor=colors.green,
        spaceAfter=10
    )

    normal = styles['Normal']

    elements = []

    # 🌾 TITLE
    elements.append(Paragraph(labels["title"], title_style))

    # 📄 META INFO
    elements.append(Paragraph(f"<b>{labels['report_id']}:</b> {report.id}", normal))
    elements.append(Paragraph(f"<b>{labels['date']}:</b> {report.created_at.strftime('%d %B %Y, %I:%M %p')}", normal))
    elements.append(Spacer(1, 20))

    # 🖼 IMAGE (optional)
    if report.image:
        image_path = os.path.join(settings.MEDIA_ROOT, report.image.name)
        if os.path.exists(image_path):
            elements.append(Image(image_path, width=200, height=150))
            elements.append(Spacer(1, 15))

    # 📊 TABLE
    data = [
        [labels["field"], labels["details"]],
        [labels["disease"], report.disease],
        [labels["description"], report.description or "N/A"],
        [labels["symptoms"], report.symptoms or "N/A"],
        [labels["causes"], report.causes or "N/A"],
        [labels["treatment"], report.solution or "N/A"],
        [labels["prevention"], report.prevention or "N/A"],
        [labels["soil"], report.soil or "N/A"],
    ]

    table = Table(data, colWidths=[120, 350])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.green),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,1), (0,-1), colors.lightgrey),
        ('FONTNAME', (0,0), (-1,-1), font_name),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 30))

    # ⚠ DISCLAIMER
    elements.append(Paragraph(labels["disclaimer_title"], section_style))
    elements.append(Paragraph(labels["disclaimer_text"], normal))

    elements.append(Spacer(1, 40))

    # 📞 FOOTER
    elements.append(Paragraph(labels["footer"], styles['Italic']))

    doc.build(elements)

    return response
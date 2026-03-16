import pdfplumber
import re
from paddleocr import PaddleOCR
from pdf2image import convert_from_path
from PIL import Image
import os

ocr = PaddleOCR(use_angle_cls=True, lang="en")
#                rotation            english

def extract_text_with_ocr_image(image_path):

    result = ocr.ocr(image_path)
#.   extracted text

    text = ""

    for line in result[0]:
        text += line[1][0] + "\n"

    return text


def extract_text_with_ocr_pdf(pdf_path):

    images = convert_from_path(pdf_path)
#.      converting to image
    text = ""

    for img in images:
        result = ocr.ocr(img)
#       full text from each image

        for line in result[0]:
            text += line[1][0] + "\n"
#       converting ext text into line wise
    return text


def extract_data_from_pdf(file_path):

    text = ""

    extension = os.path.splitext(file_path)[1].lower()

    # -------------------------
    # CASE 1: PDF FILE
    # -------------------------
    if extension == ".pdf":

        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        # if page_text is not empty
                        text += page_text
        except:
            #else
            text = ""

        # If PDF has no text → use OCR
        if not text.strip():
            print("Using OCR for scanned PDF...")
            text = extract_text_with_ocr_pdf(file_path)

    # -------------------------
    # CASE 2: IMAGE FILE
    # -------------------------
    elif extension in [".jpg", ".jpeg", ".png"]:

        print("Using OCR for image...")
        text = extract_text_with_ocr_image(file_path)

    else:
        raise Exception("Unsupported file type")

    print("Extracted Text:\n", text)

    patient = re.search(r"Patient Name:\s*(.*)", text)
    diagnosis = re.search(r"Diagnosis:\s*(.*)", text)
    procedure = re.search(r"Procedure:\s*(.*)", text)
    drug = re.search(r"Medication:\s*(.*)", text)
    bill = re.search(r"Total Bill:\s*\D*(\d+)", text)


    data = {
        "patient_name": patient.group(1) if patient else None,
        "diagnosis": diagnosis.group(1) if diagnosis else None,
        "procedure": procedure.group(1) if procedure else None,
        "medication": drug.group(1) if drug else None,
        "total_bill": bill.group(1) if bill else None
        # group(1) bcs group(0) = full text (including the patient_name)
        #              group(1) = after text (captured text)
    }

    return data

# def extract_data_from_pdf(file_path):

#     text = ""

#     with pdfplumber.open(file_path) as pdf:
#         for page in pdf.pages:
#             text += page.extract_text()

#     patient = re.search(r"Patient Name:\s*(.*)", text)
#     diagnosis = re.search(r"Diagnosis:\s*(.*)", text)
#     procedure = re.search(r"Procedure:\s*(.*)", text)
#     medication = re.search(r"Medication:\s*(.*)", text)
#     bill = re.search(r"Total Bill:\s*\D*(\d+)", text)

#     data = {
#         "patient_name": patient.group(1) if patient else None,
#         "diagnosis": diagnosis.group(1) if diagnosis else None,
#         "procedure": procedure.group(1) if procedure else None,
#         "medication": medication.group(1) if medication else None,
#         "total_bill": bill.group(1) if bill else None
#     }

#     return data

import spacy

nlp = spacy.load("en_core_web_sm")

# simple keyword dictionaries
disease_keywords = [
    "pneumonia","diabetes","hypertension","asthma","bronchitis",
    "infection","stroke","heart failure","anemia","arthritis"
]

procedure_keywords = [
    "x-ray","ct scan","mri","blood test","ecg","ultrasound",
    "colonoscopy","endoscopy","biopsy","surgery"
]

medication_keywords = [
    "antibiotic","insulin","paracetamol","ibuprofen",
    "aspirin","metformin"
]

def extract_entities(text):

    text = text.lower()

    doc = nlp(text)

    disease = None
    procedure = None
    medication = None

    for token in doc:

        if not disease:
            for d in disease_keywords:
                if d in text:
                    disease = d

        if not procedure:
            for p in procedure_keywords:
                if p in text:
                    procedure = p

        if not medication:
            for m in medication_keywords:
                if m in text:
                    medication = m

    return {
        "disease": disease,
        "procedure": procedure,
        "medication": medication
    }
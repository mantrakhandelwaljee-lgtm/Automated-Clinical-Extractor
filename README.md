# 🏥 AI-Powered Clinical Data Normalization Engine

An AI system that converts **unstructured medical documents (PDFs, scans, reports)** into **structured healthcare data using FHIR standards**.

This project automatically extracts **diagnosis, procedures, medications, and billing information** from clinical documents and maps them to **standardized medical coding systems (ICD & CPT)**.

---

# 🚀 Problem Statement

Hospitals generate massive amounts of **unstructured clinical data**:

- discharge summaries
- diagnostic reports
- lab reports
- billing documents

However, insurance claims require **structured standardized codes** such as:

- **ICD-10** → diagnosis codes
- **CPT** → procedure codes

This mismatch creates major inefficiencies in **Revenue Cycle Management (RCM)**.

Our system solves this by automatically converting unstructured medical documents into **FHIR-compliant structured data**.

---

# 🧠 Solution Overview

### Pipeline:

Medical Document (PDF / Image)

↓

OCR (PaddleOCR)

↓

Text Extraction

↓

Medical Entity Recognition

↓

AI Code Mapping (ICD & CPT)

↓

FHIR Resource Generation

↓

Insurance Claim Bundle


---

# ⚙️ Features

✅ Supports **PDF and image documents**  
✅ Handles **scanned documents using OCR**  
✅ Extracts key clinical fields:

- Patient Name
- Diagnosis
- Procedure
- Medication
- Total Bill

✅ AI-based **medical entity detection**  
✅ Semantic **ICD-10 code mapping**  
✅ Semantic **CPT procedure mapping**  
✅ Generates **FHIR-compliant healthcare resources**  
✅ Creates structured **insurance claim bundles**

---

# 🧩 Technologies Used

### Backend

- Python
- FastAPI
- Uvicorn

### AI / NLP

- spaCy
- scispaCy
- Sentence Transformers

### OCR

- PaddleOCR
- pdf2image
- pdfplumber

### Data Processing

- pandas
- scikit-learn

### Healthcare Standards

- FHIR (`fhir.resources`)

---

# 📂 Project Structure

```

project/
│
├── main.py                # FastAPI server
├── parser.py              # OCR + text extraction
│
├── entity_extractor.py    # Rule-based entity detection
├── clinical_extractor.py  # Clinical NLP extractor
├── medical_ai_extractor.py # AI medical NER
│
├── icd_ai_mapper.py       # AI-based ICD mapping
├── cpt_ai_mapper.py       # AI-based CPT mapping
│
├── icd10_codes.csv        # ICD dataset
├── cpt_codes.csv          # CPT dataset
│
├── templates/
│   └── index.html         # Upload UI
│
├── static/
│
└── requirements.txt

🧪 Example Input

Example discharge summary:

Patient Name: Anita Verma
Diagnosis: Pneumonia
Procedure: Chest CT Scan
Medication: Amoxicillin
Total Bill: ₹7200

📊 Example Output

Extracted Summary:

Patient: Anita Verma
Diagnosis: Pneumonia
ICD Code: J18
Procedure: Chest CT Scan
CPT Code: 71250
Medication: Amoxicillin
Total Bill: 7200 INR

Generated FHIR Bundle:
{
  "resourceType": "Bundle",
  "entry": [
    {
      "resource": {
        "resourceType": "Patient"
      }
    },
    {
      "resource": {
        "resourceType": "Condition"
      }
    },
    {
      "resource": {
        "resourceType": "Procedure"
      }
    }
  ]
}

```
## 🛠 Installation
### 1️⃣ Clone the repository:

 - git clone https://github.com/yourusername/project-name.git
 - cd project-name

### 2️⃣ Create virtual environment:

```
python3.11 -m venv nlp_env
source nlp_env/bin/activate
```
### 3️⃣ Install dependencies:

```
pip install -r requirements.txt
```

### 4️⃣ Install spaCy models:
```
python -m spacy download en_core_web_sm
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_core_sci_sm-0.5.4.tar.gz
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_ner_bc5cdr_md-0.5.4.tar.gz
```

### 5️⃣ Install Poppler (required for OCR):
```
brew install poppler
```

## ▶️ Running the Application

### Start the server:
```
uvicorn main:app --reload
```

### Open in browser:
```
http://127.0.0.1:8000
```

## 📈 Future Improvements

- Add multi-language medical OCR

- Integrate LLM-based clinical summarization

- Improve negation detection ("no pneumonia")

- Add FHIR server integration

- Build hospital dashboard UI

## 👨‍💻 Author

### Developed by Mantra Khandelwal

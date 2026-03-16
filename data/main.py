# # # # from fastapi import FastAPI, UploadFile, File
# # # # import json
# # # # import shutil

# # # # from parser import extract_data_from_pdf
# # # # from entity_extractor import extract_medical_entities

# # # # from icd_ai_mapper import map_icd_code_ai
# # # # from cpt_ai_mapper import map_cpt_code_ai

# # # # from clinical_extractor import extract_entities


# # # # from fhir.resources.patient import Patient
# # # # from fhir.resources.condition import Condition
# # # # from fhir.resources.procedure import Procedure
# # # # from fhir.resources.medicationrequest import MedicationRequest
# # # # from fhir.resources.observation import Observation
# # # # from fhir.resources.bundle import Bundle



# # # # app = FastAPI()


# # # # @app.post("/upload")
# # # # async def upload_pdf(file: UploadFile = File(...)):

# # # #     # -------------------------
# # # #     # Save uploaded file
# # # #     # -------------------------
# # # #     file_location = f"temp_{file.filename}"

# # # #     with open(file_location, "wb") as buffer:
# # # #         shutil.copyfileobj(file.file, buffer)

# # # #     # -------------------------
# # # #     # Extract structured data
# # # #     # -------------------------
# # # #     data = extract_data_from_pdf(file_location)
# # # #     entities = extract_entities(text)

# # # #     diagnosis_text = entities["disease"]
# # # #     procedure_text = entities["procedure"]
# # # #     medication_text = entities["medication"]

# # # #     text = data.get("raw_text", "")

# # # #     # -------------------------
# # # #     # NLP entity extraction
# # # #     # -------------------------
# # # #     entities = extract_medical_entities(text)

# # # #     diagnosis_text = entities["diagnosis"][0] if entities["diagnosis"] else data["diagnosis"]
# # # #     procedure_text = entities["procedure"][0] if entities["procedure"] else data["procedure"]

# # # #     diagnosis_code = map_icd_code_ai(diagnosis_text)
# # # #     procedure_code = map_cpt_code_ai(procedure_text)

# # # #     procedure_code = str(procedure_code)
# # # #     diagnosis_code = str(diagnosis_code)

# # # #     # -------------------------
# # # #     # Patient
# # # #     # -------------------------

# # # #     procedure_text = (procedure_text or "").strip()
# # # #     diagnosis_text = (diagnosis_text or "").strip()

# # # #     if not procedure_text:
# # # #         procedure_text = "Unknown Procedure"

# # # #     if not diagnosis_text:
# # # #         diagnosis_text = "Unknown Diagnosis"

# # # #     patient_resource = Patient(
# # # #         id="1",
# # # #         name=[{"text": data["patient_name"]}]
# # # #     )

# # # #     # -------------------------
# # # #     # Condition (Diagnosis)
# # # #     # -------------------------
# # # #     condition_resource = Condition(
# # # #         clinicalStatus={
# # # #             "coding": [{
# # # #                 "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
# # # #                 "code": "active"
# # # #             }]
# # # #         },
# # # #         subject={"reference": "Patient/1"},
# # # #         code={
# # # #             "coding": [{
# # # #                 "system": "http://hl7.org/fhir/sid/icd-10",
# # # #                 "code": diagnosis_code,
# # # #                 "display": diagnosis_text
# # # #             }]
# # # #         }
# # # #     )

# # # #     # -------------------------
# # # #     # Procedure
# # # #     # -------------------------
# # # #     procedure_resource = Procedure(
# # # #         status="completed",
# # # #         subject={"reference": "Patient/1"},
# # # #         code={
# # # #             "coding": [{
# # # #                 "system": "http://www.ama-assn.org/go/cpt",
# # # #                 "code": procedure_code,
# # # #                 "display": procedure_text
# # # #             }]
# # # #         }
# # # #     )

# # # #     # -------------------------
# # # #     # MedicationRequest
# # # #     # -------------------------
# # # #     medication_resource = MedicationRequest(
# # # #         status="active",
# # # #         intent="order",
# # # #         subject={"reference": "Patient/1"},
# # # #         medication={
# # # #             "concept": {
# # # #                 "text": data["medication"]
# # # #             }
# # # #         }
# # # #     )

# # # #     # -------------------------
# # # #     # Bill (Observation)
# # # #     # -------------------------
# # # #     bill_value = int(data["total_bill"]) if data.get("total_bill") else 0

# # # #     bill_resource = Observation(
# # # #         status="final",
# # # #         subject={"reference": "Patient/1"},
# # # #         code={"text": "Total Hospital Bill"},
# # # #         valueQuantity={
# # # #             "value": bill_value,
# # # #             "unit": "INR"
# # # #         }
# # # #     )

# # # #     # -------------------------
# # # #     # FHIR Bundle
# # # #     # -------------------------
# # # #     bundle = Bundle(
# # # #         type="collection",
# # # #         entry=[
# # # #             {"resource": patient_resource},
# # # #             {"resource": condition_resource},
# # # #             {"resource": procedure_resource},
# # # #             {"resource": medication_resource},
# # # #             {"resource": bill_resource}
# # # #         ]
# # # #     )

# # # #     return json.loads(bundle.json())

# # # from fastapi import FastAPI, UploadFile, File
# # # import json
# # # import shutil

# # # from parser import extract_data_from_pdf
# # # from entity_extractor import extract_medical_entities
# # # from clinical_extractor import extract_entities

# # # from icd_ai_mapper import map_icd_code_ai
# # # from cpt_ai_mapper import map_cpt_code_ai

# # # from fhir.resources.patient import Patient
# # # from fhir.resources.condition import Condition
# # # from fhir.resources.procedure import Procedure
# # # from fhir.resources.medicationrequest import MedicationRequest
# # # from fhir.resources.observation import Observation
# # # from fhir.resources.bundle import Bundle
# # # from fhir.resources.claim import Claim


# # # app = FastAPI()


# # # @app.post("/upload")
# # # async def upload_pdf(file: UploadFile = File(...)):

# # #     # -------------------------
# # #     # Save uploaded PDF
# # #     # -------------------------
# # #     file_location = f"temp_{file.filename}"

# # #     with open(file_location, "wb") as buffer:
# # #         shutil.copyfileobj(file.file, buffer)

# # #     # -------------------------
# # #     # Extract data from PDF
# # #     # -------------------------
# # #     data = extract_data_from_pdf(file_location)
# # #     text = data.get("raw_text", "")

# # #     # -------------------------
# # #     # Clinical NLP extraction
# # #     # -------------------------
# # #     clinical_entities = extract_entities(text)

# # #     diagnosis_text = clinical_entities["disease"]
# # #     procedure_text = clinical_entities["procedure"]
# # #     medication_text = clinical_entities["medication"]

# # #     # -------------------------
# # #     # Additional NLP extraction
# # #     # -------------------------
# # #     entities = extract_medical_entities(text)

# # #     if entities["diagnosis"]:
# # #         diagnosis_text = entities["diagnosis"][0]

# # #     if entities["procedure"]:
# # #         procedure_text = entities["procedure"][0]

# # #     # -------------------------
# # #     # Safety fallback values
# # #     # -------------------------
# # #     diagnosis_text = (diagnosis_text or "").strip()
# # #     procedure_text = (procedure_text or "").strip()
# # #     medication_text = (medication_text or "").strip()

# # #     if not diagnosis_text:
# # #         diagnosis_text = data.get("diagnosis", "Unknown Diagnosis")

# # #     if not procedure_text:
# # #         procedure_text = data.get("procedure", "Unknown Procedure")

# # #     if not medication_text:
# # #         medication_text = data.get("medication", "Unknown Medication")

# # #     # -------------------------
# # #     # AI Code Mapping
# # #     # -------------------------
# # #     diagnosis_code = str(map_icd_code_ai(diagnosis_text))
# # #     procedure_code = str(map_cpt_code_ai(procedure_text))

# # #     # -------------------------
# # #     # Patient Resource
# # #     # -------------------------
# # #     patient_resource = Patient(
# # #         id="1",
# # #         name=[{"text": data.get("patient_name", "Unknown Patient")}]
# # #     )

# # #     # -------------------------
# # #     # Condition (Diagnosis)
# # #     # -------------------------
# # #     condition_resource = Condition(
# # #         clinicalStatus={
# # #             "coding": [{
# # #                 "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
# # #                 "code": "active"
# # #             }]
# # #         },
# # #         subject={"reference": "Patient/1"},
# # #         code={
# # #             "coding": [{
# # #                 "system": "http://hl7.org/fhir/sid/icd-10",
# # #                 "code": diagnosis_code,
# # #                 "display": diagnosis_text
# # #             }]
# # #         }
# # #     )

# # #     # -------------------------
# # #     # Procedure
# # #     # -------------------------
# # #     procedure_resource = Procedure(
# # #         status="completed",
# # #         subject={"reference": "Patient/1"},
# # #         code={
# # #             "coding": [{
# # #                 "system": "http://www.ama-assn.org/go/cpt",
# # #                 "code": procedure_code,
# # #                 "display": procedure_text
# # #             }]
# # #         }
# # #     )

# # #     # -------------------------
# # #     # Medication Request
# # #     # -------------------------
# # #     medication_resource = MedicationRequest(
# # #         status="active",
# # #         intent="order",
# # #         subject={"reference": "Patient/1"},
# # #         medication={
# # #             "concept": {
# # #                 "text": medication_text
# # #             }
# # #         }
# # #     )

# # #     # -------------------------
# # #     # Hospital Bill (Observation)
# # #     # -------------------------
# # #     bill_value = int(data["total_bill"]) if data.get("total_bill") else 0

# # #     bill_resource = Observation(
# # #         status="final",
# # #         subject={"reference": "Patient/1"},
# # #         code={"text": "Total Hospital Bill"},
# # #         valueQuantity={
# # #             "value": bill_value,
# # #             "unit": "INR"
# # #         }
# # #     )

# # #     # -------------------------
# # #     # Claim Resource (NEW)
# # #     # -------------------------
# # #     from datetime import datetime

# # #     claim_resource = Claim(
# # #     status="active",
# # #     use="claim",
# # #     created=datetime.today().strftime("%Y-%m-%d"),
# # #     type={"text": "medical"},
# # #     patient={"reference": "Patient/1"},

# # #     diagnosis=[{
# # #         "sequence": 1,
# # #         "diagnosisCodeableConcept": {
# # #             "coding": [{
# # #                 "system": "http://hl7.org/fhir/sid/icd-10",
# # #                 "code": diagnosis_code
# # #             }]
# # #         }
# # #     }],

# # #     procedure=[{
# # #         "sequence": 1,
# # #         "procedureCodeableConcept": {
# # #             "coding": [{
# # #                 "system": "http://www.ama-assn.org/go/cpt",
# # #                 "code": procedure_code
# # #             }]
# # #         }
# # #     }]
# # # )

# # #     # -------------------------
# # #     # FHIR Bundle
# # #     # -------------------------
# # #     bundle = Bundle(
# # #         type="collection",
# # #         entry=[
# # #             {"resource": patient_resource},
# # #             {"resource": condition_resource},
# # #             {"resource": procedure_resource},
# # #             {"resource": medication_resource},
# # #             {"resource": bill_resource},
# # #             {"resource": claim_resource}
# # #         ]
# # #     )

# # #     return {
# # #     "summary": {
# # #         "patient": data.get("patient_name"),
# # #         "diagnosis_text": diagnosis_text,
# # #         "diagnosis_code": diagnosis_code,
# # #         "procedure_text": procedure_text,
# # #         "procedure_code": procedure_code,
# # #         "medication": medication_text,
# # #         "bill": bill_value
# # #     },
# # #     "fhir_bundle": json.loads(bundle.json())
# # # }

# # from fastapi import FastAPI, UploadFile, File, Request
# # from fastapi.responses import HTMLResponse
# # from fastapi.templating import Jinja2Templates
# # from fastapi.staticfiles import StaticFiles

# # import json
# # import shutil
# # from datetime import datetime

# # from parser import extract_data_from_pdf
# # from entity_extractor import extract_medical_entities
# # from clinical_extractor import extract_entities

# # from icd_ai_mapper import map_icd_code_ai
# # from cpt_ai_mapper import map_cpt_code_ai

# # from fhir.resources.patient import Patient
# # from fhir.resources.condition import Condition
# # from fhir.resources.procedure import Procedure
# # from fhir.resources.medicationrequest import MedicationRequest
# # from fhir.resources.observation import Observation
# # from fhir.resources.bundle import Bundle
# # from fhir.resources.claim import Claim


# # app = FastAPI()

# # templates = Jinja2Templates(directory="templates")
# # app.mount("/static", StaticFiles(directory="static"), name="static")


# # # -------------------------
# # # Web UI
# # # -------------------------
# # @app.get("/", response_class=HTMLResponse)
# # async def home(request: Request):
# #     return templates.TemplateResponse("index.html", {"request": request})


# # # -------------------------
# # # Upload Endpoint
# # # -------------------------
# # @app.post("/upload")
# # async def upload_pdf(file: UploadFile = File(...)):

# #     # Save uploaded file
# #     file_location = f"temp_{file.filename}"

# #     with open(file_location, "wb") as buffer:
# #         shutil.copyfileobj(file.file, buffer)

# #     # Extract PDF data
# #     data = extract_data_from_pdf(file_location)
# #     text = data.get("raw_text", "")

# #     # -------------------------
# #     # NLP entity extraction
# #     # -------------------------
# #     clinical_entities = extract_entities(text)
# #     entities = extract_medical_entities(text)

# #     diagnosis_text = clinical_entities["disease"]
# #     procedure_text = clinical_entities["procedure"]
# #     medication_text = clinical_entities["medication"]

# #     if entities["diagnosis"]:
# #         diagnosis_text = entities["diagnosis"][0]

# #     if entities["procedure"]:
# #         procedure_text = entities["procedure"][0]

# #     diagnosis_text = (diagnosis_text or "").strip()
# #     procedure_text = (procedure_text or "").strip()
# #     medication_text = (medication_text or "").strip()

# #     if not diagnosis_text:
# #         diagnosis_text = data.get("diagnosis", "Unknown Diagnosis")

# #     if not procedure_text:
# #         procedure_text = data.get("procedure", "Unknown Procedure")

# #     if not medication_text:
# #         medication_text = data.get("medication", "Unknown Medication")

# #     # -------------------------
# #     # AI code mapping
# #     # -------------------------
# #     diagnosis_code = str(map_icd_code_ai(diagnosis_text))
# #     procedure_code = str(map_cpt_code_ai(procedure_text))

# #     # -------------------------
# #     # Patient Resource
# #     # -------------------------
# #     patient_resource = Patient(
# #         id="1",
# #         name=[{"text": data.get("patient_name", "Unknown Patient")}]
# #     )

# #     # -------------------------
# #     # Condition
# #     # -------------------------
# #     condition_resource = Condition(
# #         clinicalStatus={
# #             "coding": [{
# #                 "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
# #                 "code": "active"
# #             }]
# #         },
# #         subject={"reference": "Patient/1"},
# #         code={
# #             "coding": [{
# #                 "system": "http://hl7.org/fhir/sid/icd-10",
# #                 "code": diagnosis_code,
# #                 "display": diagnosis_text
# #             }]
# #         }
# #     )

# #     # -------------------------
# #     # Procedure
# #     # -------------------------
# #     procedure_resource = Procedure(
# #         status="completed",
# #         subject={"reference": "Patient/1"},
# #         code={
# #             "coding": [{
# #                 "system": "http://www.ama-assn.org/go/cpt",
# #                 "code": procedure_code,
# #                 "display": procedure_text
# #             }]
# #         }
# #     )

# #     # -------------------------
# #     # Medication
# #     # -------------------------
# #     medication_resource = MedicationRequest(
# #         status="active",
# #         intent="order",
# #         subject={"reference": "Patient/1"},
# #         medication={
# #             "concept": {
# #                 "text": medication_text
# #             }
# #         }
# #     )

# #     # -------------------------
# #     # Bill Observation
# #     # -------------------------
# #     bill_value = int(data["total_bill"]) if data.get("total_bill") else 0

# #     bill_resource = Observation(
# #         status="final",
# #         subject={"reference": "Patient/1"},
# #         code={"text": "Total Hospital Bill"},
# #         valueQuantity={
# #             "value": bill_value,
# #             "unit": "INR"
# #         }
# #     )

# #     # -------------------------
# #     # Claim Resource
# #     # -------------------------
# #     claim_resource = Claim(
# #         status="active",
# #         use="claim",
# #         created=datetime.today().strftime("%Y-%m-%d"),
# #         type={"text": "medical"},
# #         patient={"reference": "Patient/1"},

# #         diagnosis=[{
# #             "sequence": 1,
# #             "diagnosisCodeableConcept": {
# #                 "coding": [{
# #                     "system": "http://hl7.org/fhir/sid/icd-10",
# #                     "code": diagnosis_code
# #                 }]
# #             }
# #         }],

# #         procedure=[{
# #             "sequence": 1,
# #             "procedureCodeableConcept": {
# #                 "coding": [{
# #                     "system": "http://www.ama-assn.org/go/cpt",
# #                     "code": procedure_code
# #                 }]
# #             }
# #         }]
# #     )

# #     # -------------------------
# #     # FHIR Bundle
# #     # -------------------------
# #     bundle = Bundle(
# #         type="collection",
# #         entry=[
# #             {"resource": patient_resource},
# #             {"resource": condition_resource},
# #             {"resource": procedure_resource},
# #             {"resource": medication_resource},
# #             {"resource": bill_resource},
# #             {"resource": claim_resource}
# #         ]
# #     )

# #     # -------------------------
# #     # Return summary + FHIR
# #     # -------------------------
# #     return {
# #         "summary": {
# #             "patient": data.get("patient_name"),
# #             "diagnosis": diagnosis_text,
# #             "icd_code": diagnosis_code,
# #             "procedure": procedure_text,
# #             "cpt_code": procedure_code,
# #             "medication": medication_text,
# #             "bill": bill_value
# #         },
# #         "fhir_bundle": json.loads(bundle.json())
# #     }

# from fastapi import FastAPI, UploadFile, File, Request
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles

# import json
# import shutil
# from datetime import datetime

# from parser import extract_data_from_pdf
# from entity_extractor import extract_medical_entities
# from clinical_extractor import extract_entities
# from medical_ai_extractor import extract_medical_ai   # NEW AI extractor

# from icd_ai_mapper import map_icd_code_ai
# from cpt_ai_mapper import map_cpt_code_ai

# from fhir.resources.patient import Patient
# from fhir.resources.condition import Condition
# from fhir.resources.procedure import Procedure
# from fhir.resources.medicationrequest import MedicationRequest
# from fhir.resources.observation import Observation
# from fhir.resources.bundle import Bundle
# from fhir.resources.claim import Claim


# app = FastAPI()

# templates = Jinja2Templates(directory="templates")
# app.mount("/static", StaticFiles(directory="static"), name="static")


# # -------------------------
# # Web UI
# # -------------------------
# @app.get("/", response_class=HTMLResponse)
# async def home(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})


# # -------------------------
# # Upload Endpoint
# # -------------------------
# @app.post("/upload")
# async def upload_pdf(file: UploadFile = File(...)):

#     # Save uploaded file
#     file_location = f"temp_{file.filename}"

#     with open(file_location, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     # Extract PDF data
#     data = extract_data_from_pdf(file_location)
#     text = data.get("raw_text", "")

#     # -------------------------
#     # AI medical entity extraction
#     # -------------------------
#     ai_entities = extract_medical_ai(text)

#     # -------------------------
#     # Existing NLP extractors
#     # -------------------------
#     clinical_entities = extract_entities(text)
#     entities = extract_medical_entities(text)

#     diagnosis_text = clinical_entities["disease"]
#     procedure_text = clinical_entities["procedure"]
#     medication_text = clinical_entities["medication"]

#     # AI override if detected
#     if ai_entities["diseases"]:
#         diagnosis_text = ai_entities["diseases"][0]

#     if ai_entities["drugs"]:
#         medication_text = ai_entities["drugs"][0]

#     if entities["diagnosis"]:
#         diagnosis_text = entities["diagnosis"][0]

#     if entities["procedure"]:
#         procedure_text = entities["procedure"][0]

#     # Clean values
#     diagnosis_text = (diagnosis_text or "").strip()
#     procedure_text = (procedure_text or "").strip()
#     medication_text = (medication_text or "").strip()

#     if not diagnosis_text:
#         diagnosis_text = data.get("diagnosis", "Unknown Diagnosis")

#     if not procedure_text:
#         procedure_text = data.get("procedure", "Unknown Procedure")

#     if not medication_text:
#         medication_text = data.get("medication", "Unknown Medication")

#     # -------------------------
#     # AI code mapping
#     # -------------------------
#     diagnosis_code = str(map_icd_code_ai(diagnosis_text))
#     procedure_code = str(map_cpt_code_ai(procedure_text))

#     # -------------------------
#     # Patient Resource
#     # -------------------------
#     patient_resource = Patient(
#         id="1",
#         name=[{"text": data.get("patient_name", "Unknown Patient")}]
#     )

#     # -------------------------
#     # Condition
#     # -------------------------
#     condition_resource = Condition(
#         clinicalStatus={
#             "coding": [{
#                 "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
#                 "code": "active"
#             }]
#         },
#         subject={"reference": "Patient/1"},
#         code={
#             "coding": [{
#                 "system": "http://hl7.org/fhir/sid/icd-10",
#                 "code": diagnosis_code,
#                 "display": diagnosis_text
#             }]
#         }
#     )

#     # -------------------------
#     # Procedure
#     # -------------------------
#     procedure_resource = Procedure(
#         status="completed",
#         subject={"reference": "Patient/1"},
#         code={
#             "coding": [{
#                 "system": "http://www.ama-assn.org/go/cpt",
#                 "code": procedure_code,
#                 "display": procedure_text
#             }]
#         }
#     )

#     # -------------------------
#     # Medication
#     # -------------------------
#     medication_resource = MedicationRequest(
#         status="active",
#         intent="order",
#         subject={"reference": "Patient/1"},
#         medication={
#             "concept": {
#                 "text": medication_text
#             }
#         }
#     )

#     # -------------------------
#     # Bill Observation
#     # -------------------------
#     bill_value = int(data["total_bill"]) if data.get("total_bill") else 0

#     bill_resource = Observation(
#         status="final",
#         subject={"reference": "Patient/1"},
#         code={"text": "Total Hospital Bill"},
#         valueQuantity={
#             "value": bill_value,
#             "unit": "INR"
#         }
#     )

#     # -------------------------
#     # Claim Resource
#     # -------------------------
#     claim_resource = Claim(
#         status="active",
#         use="claim",
#         created=datetime.today().strftime("%Y-%m-%d"),
#         type={"text": "medical"},
#         patient={"reference": "Patient/1"},

#         diagnosis=[{
#             "sequence": 1,
#             "diagnosisCodeableConcept": {
#                 "coding": [{
#                     "system": "http://hl7.org/fhir/sid/icd-10",
#                     "code": diagnosis_code
#                 }]
#             }
#         }],

#         procedure=[{
#             "sequence": 1,
#             "procedureCodeableConcept": {
#                 "coding": [{
#                     "system": "http://www.ama-assn.org/go/cpt",
#                     "code": procedure_code
#                 }]
#             }
#         }]
#     )

#     # -------------------------
#     # FHIR Bundle
#     # -------------------------
#     bundle = Bundle(
#         type="collection",
#         entry=[
#             {"resource": patient_resource},
#             {"resource": condition_resource},
#             {"resource": procedure_resource},
#             {"resource": medication_resource},
#             {"resource": bill_resource},
#             {"resource": claim_resource}
#         ]
#     )

#     return {
#         "summary": {
#             "patient": data.get("patient_name"),
#             "diagnosis": diagnosis_text,
#             "icd_code": diagnosis_code,
#             "procedure": procedure_text,
#             "cpt_code": procedure_code,
#             "medication": medication_text,
#             "bill": bill_value
#         },
#         "fhir_bundle": json.loads(bundle.json())
#     }

from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import json
import shutil
from datetime import datetime

from parser import extract_data_from_pdf
from entity_extractor import extract_medical_entities
from clinical_extractor import extract_entities
from medical_ai_extractor import extract_medical_ai

from icd_ai_mapper import map_icd_code_ai
from cpt_ai_mapper import map_cpt_code_ai

from fhir.resources.patient import Patient
from fhir.resources.condition import Condition
from fhir.resources.procedure import Procedure
from fhir.resources.medicationrequest import MedicationRequest
from fhir.resources.observation import Observation
from fhir.resources.bundle import Bundle
from fhir.resources.claim import Claim


app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    file_location = f"temp_{file.filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    data = extract_data_from_pdf(file_location)
    text = data.get("raw_text", "")

    ai_entities = extract_medical_ai(text)
    clinical_entities = extract_entities(text)
    entities = extract_medical_entities(text)

    diagnosis_text = clinical_entities["disease"]
    procedure_text = clinical_entities["procedure"]
    medication_text = clinical_entities["medication"]

    if ai_entities["diseases"]:
        diagnosis_text = ai_entities["diseases"][0]

    if ai_entities["drugs"]:
        medication_text = ai_entities["drugs"][0]

    if entities["diagnosis"]:
        diagnosis_text = entities["diagnosis"][0]

    if entities["procedure"]:
        procedure_text = entities["procedure"][0]

    diagnosis_text = (diagnosis_text or "").strip()
    procedure_text = (procedure_text or "").strip()
    medication_text = (medication_text or "").strip()

    if not diagnosis_text:
        diagnosis_text = data.get("diagnosis", "Unknown Diagnosis")

    if not procedure_text:
        procedure_text = data.get("procedure", "Unknown Procedure")

    if not medication_text:
        medication_text = data.get("medication", "Unknown Medication")

    diagnosis_code = str(map_icd_code_ai(diagnosis_text))
    procedure_code = str(map_cpt_code_ai(procedure_text))

    patient_resource = Patient(
        id="1",
        name=[{"text": data.get("patient_name", "Unknown Patient")}]
    )

    condition_resource = Condition(
        clinicalStatus={
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                "code": "active"
            }]
        },
        subject={"reference": "Patient/1"},
        code={
            "coding": [{
                "system": "http://hl7.org/fhir/sid/icd-10",
                "code": diagnosis_code,
                "display": diagnosis_text
            }]
        }
    )

    procedure_resource = Procedure(
        status="completed",
        subject={"reference": "Patient/1"},
        code={
            "coding": [{
                "system": "http://www.ama-assn.org/go/cpt",
                "code": procedure_code,
                "display": procedure_text
            }]
        }
    )

    medication_resource = MedicationRequest(
        status="active",
        intent="order",
        subject={"reference": "Patient/1"},
        medication={
            "concept": {
                "text": medication_text
            }
        }
    )

    bill_value = int(data["total_bill"]) if data.get("total_bill") else 0

    bill_resource = Observation(
        status="final",
        subject={"reference": "Patient/1"},
        code={"text": "Total Hospital Bill"},
        valueQuantity={
            "value": bill_value,
            "unit": "INR"
        }
    )

    claim_resource = Claim(
        status="active",
        use="claim",
        created=datetime.today().strftime("%Y-%m-%d"),
        type={"text": "medical"},
        patient={"reference": "Patient/1"},
        diagnosis=[{
            "sequence": 1,
            "diagnosisCodeableConcept": {
                "coding": [{
                    "system": "http://hl7.org/fhir/sid/icd-10",
                    "code": diagnosis_code
                }]
            }
        }],
        procedure=[{
            "sequence": 1,
            "procedureCodeableConcept": {
                "coding": [{
                    "system": "http://www.ama-assn.org/go/cpt",
                    "code": procedure_code
                }]
            }
        }]
    )

    bundle = Bundle(
        type="collection",
        entry=[
            {"resource": patient_resource},
            {"resource": condition_resource},
            {"resource": procedure_resource},
            {"resource": medication_resource},
            {"resource": bill_resource},
            {"resource": claim_resource}
        ]
    )

    bundle_json = json.dumps(json.loads(bundle.json()), indent=4)

    html_content = f"""
    <html>
    <head>
    <title>Medical Analysis Result</title>

    <style>

    body {{
        font-family: Arial;
        background: linear-gradient(135deg,#1e3c72,#2a5298);
        margin:0;
        padding:40px;
    }}

    .container {{
        max-width:900px;
        margin:auto;
    }}

    .card {{
        background:white;
        padding:25px;
        border-radius:10px;
        margin-bottom:25px;
        box-shadow:0 10px 25px rgba(0,0,0,0.2);
    }}

    h2 {{
        color:#1e3c72;
        margin-bottom:15px;
    }}

    .item {{
        margin:8px 0;
        font-size:16px;
    }}

    .label {{
        font-weight:bold;
        color:#2a5298;
    }}

    pre {{
        background:#f4f6fa;
        padding:20px;
        border-radius:8px;
        overflow-x:auto;
        font-size:13px;
    }}

    </style>

    </head>

    <body>

    <div class="container">

        <div class="card">

        <h2>Extracted Medical Summary</h2>

        <div class="item"><span class="label">Patient:</span> {data.get("patient_name")}</div>
        <div class="item"><span class="label">Diagnosis:</span> {diagnosis_text}</div>
        <div class="item"><span class="label">ICD Code:</span> {diagnosis_code}</div>
        <div class="item"><span class="label">Procedure:</span> {procedure_text}</div>
        <div class="item"><span class="label">CPT Code:</span> {procedure_code}</div>
        <div class="item"><span class="label">Medication:</span> {medication_text}</div>
        <div class="item"><span class="label">Total Bill:</span> {bill_value} INR</div>

        </div>

        <div class="card">

        <h2>FHIR Bundle JSON</h2>

        <pre>{bundle_json}</pre>

        </div>

    </div>

    </body>
    </html>
    """

    return HTMLResponse(content=html_content)
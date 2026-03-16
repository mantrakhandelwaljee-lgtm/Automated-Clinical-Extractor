import spacy

nlp = spacy.load("en_ner_bc5cdr_md")

def extract_medical_ai(text):

    doc = nlp(text)

    diseases = []
    drugs = []

    for ent in doc.ents:
        if ent.label_ == "DISEASE":
            diseases.append(ent.text)

        if ent.label_ == "CHEMICAL":
            drugs.append(ent.text)

    return {
        "diseases": list(set(diseases)),
        "drugs": list(set(drugs))
    }
import requests
import ollama
import json
import os
from src.services.ai.ollama_service import run_ollama

def find_PN_and_Adress_with_ai(text):
    return run_ollama("extract_pn_and_country", text)
    # prompt ="""
    # You are an assistant that extracts product information.

    # Task:
    # - Extract all Part Numbers (PN) and their corresponding Country of Origin from the text.
    # - Each Part Number must be linked to its Country of Origin if available.
    # - If a Part Number does not have a Country of Origin, set it to "Not found".
    # - Never make up or guess values.
    # - Always return the result in strict JSON format.

    # Output format:
    # {
    # "Parts": [
    #     {
    #     "PartNumber": "...",
    #     "CountryOfOrigin": "..."
    #     },
    #     {
    #     "PartNumber": "...",
    #     "CountryOfOrigin": "..."
    #     }
    # ]
    # }

    # Text:
    # """ + text

    # result = ollama.generate(model= os.getenv("OLLAMA_MODEL"), prompt=prompt)
    # response =  result['response']
    # return response[response.index("{"):]

def find_adress(pdf_page):
    adress = ""

    box = (40, 115.46, 385, 122.68)

    recorte = pdf_page.crop(box)

    for word in recorte.extract_words():
        adress += (word["text"]+" ")

    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": adress,
        "format": "json",
        "addressdetails": 1,
        "limit": 1
    }
    headers = {
        "User-Agent": "PDFExtractor/1.0"
    }

    resp = requests.get(url, params=params, headers=headers)
    data = resp.json()

    if data:
        return {
            "adress_formatado": data[0]["display_name"],
            "latitude": data[0]["lat"],
            "longitude": data[0]["lon"],
            "detalhes": data[0]["address"]
        }
    return None



def find_pn(pdf_page):
    box = (91, 233, 323, 515)
    recorte = pdf_page.crop(box)

    PN = []
    row = []

    for word in recorte.extract_words():
        if word["text"] == "-":
            try:
                if "PN:" in row[-1]:
                    PN.append(row[-1][3:])
                else:
                    PN.append(row[0])
            except:
                pass
            row = []
            continue

        row.append(word["text"])


    output = {
        "Parts": [
            {
                "PartNumber": pn,
                "CountryOfOrigin": "Not found"
            } for pn in PN
        ]
    }

    return json.dumps(output, indent=4)

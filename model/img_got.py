from PIL import Image
import pytesseract
import re
from model.uploaddata import UploadData

class IMAGERECEIVED:
    def __init__(self, image_path):
        self.image_path = image_path

    def extract_text(self):
        img = Image.open(self.image_path)
        text = pytesseract.image_to_string(img)
        return text

    def extract_structured_data(self):
        text = self.extract_text()
        text = text.replace("\n", " ")  # remove line breaks globally

        data = {}

        print("RAW OCR TEXT:", text)

        # Type
        if "Installation" in text:
            data["Type"] = "Installation"

        # ID
        id_match = re.search(r"\d{2}-\d{10,12}", text)
        if id_match:
            data["id"] = id_match.group()

        # Date
        date_match = re.search(
            r"\d{1,2}\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+.*?(AM|PM)",
            text,
            re.IGNORECASE
        )
        if date_match:
            data["date"] = date_match.group()

        # DSLID
        dsl_match = re.search(r'DSLID\s*(\d+)', text)
        if dsl_match:
            data["DSLID"] = dsl_match.group(1)

        # Tariff Plan
        tariff_match = re.search(r'Tariff Plan\s*(\d+\s*\w+\s*\d+\w+)', text)
        if tariff_match:
            data["Tariff plan"] = tariff_match.group(1)

        # TEL
        tel_match = re.search(r'TEL_[^\s]+', text)
        if tel_match:
            data["TEL"] = tel_match.group()
            
        # Address
        address_match = re.search(r'(No\s.*?)(?=\s+Status:)', text, re.IGNORECASE)

        if address_match:
            address = address_match.group(1)
            address = " ".join(address.split())  # clean extra spaces
            data["Address"] = address

        
        return data

        

        


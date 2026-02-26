from flask import Flask, render_template, request
from model.img_got import IMAGERECEIVED
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def upload_data():
    if request.method == 'POST':
        cilent_name = request.form.get("clientName")
        files = request.files.getlist('imageInput')
        if not files:
            return "No files selected"

        combined_data = {}   # 🔥 ONE dictionary for all images

        for file in files:
            if file.filename == "":
                continue

            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)

            print("Saved:", file_path)

            ocr = IMAGERECEIVED(file_path)
            data = ocr.extract_structured_data()

            if data:
                combined_data.update(data) 

        print("MERGED DATA:", combined_data)
        combined_data['Name'] = cilent_name

        # Save only once
        if combined_data:
            from model.uploaddata import UploadData
            uploader = UploadData()
            uploader.save(combined_data)

        return "Images processed and merged successfully!"

    return render_template('index.html')


if __name__ == '__main__':
    app.run()
from flask import Flask, jsonify, request, redirect, url_for, abort
import os

app = Flask(__name__)
@app.route('/api/v1/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    print(uploaded_file.filename)
    print(uploaded_file)
    if uploaded_file.filename != '':
        try:
            filepath = os.path.join(os.getcwd(), 'files' ,uploaded_file.filename)
            uploaded_file.save(filepath)
            resp = jsonify(f"File uploaded to {filepath}")
            resp.status_code = 200
            return resp
        except Exception as e:
            print(f"Failed to save file {uploaded_file.filename}: {e}")
            return abort(400)
    else:
        return abort(400)
app.run()
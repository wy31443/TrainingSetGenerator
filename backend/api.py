from flask import Flask, jsonify, request, redirect, send_file, abort
import os
from process_video import process_video
import json

app = Flask(__name__)
# Upload video to files folder
@app.route('/api/v1/upload', methods=['POST', 'GET'])
def uploadHandler():
    if request.method == 'POST':
        uploaded_file = request.files['file']
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
    elif request.method == 'GET':
        files = os.listdir(os.path.join(os.getcwd(), 'files'))
        resp = jsonify(files)
        resp.status_code = 200
        return resp

# Process File by name or get processed files
@app.route('/api/v1/process', methods=['POST', 'GET'])
def processHandler():
    try:
        print(request.args)
        if request.method == 'POST':
            filename = request.args.get('filename')
            if filename != None:
                # Process file by name
                filepath = os.path.abspath(os.path.join(os.getcwd(), 'files', filename))
                if process_video(filepath):
                    resp = jsonify(f"Successfully processed file {filename}")
                    resp.status_code = 200
                    return resp
                else:
                    resp = jsonify(f"Failed processing file {filename}")
                    resp.status_code = 500
                    return resp
            else:
                resp = jsonify(f"Failed getting filename")
                resp.status_code = 400
                return resp
        elif request.method == 'GET':
            # Get files in specific processed file folder
            filename = request.args.get('filename')
            if filename != None:
                path = os.path.join(os.getcwd(), 'processed', filename)
                print(path)
                files = os.listdir(path)
                resp = jsonify(files)
                resp.status_code = 200
                return resp
            else: # Get all processed file folders
                path = os.path.join(os.getcwd(), 'processed')
                print(path)
                files = os.listdir(path)
                resp = jsonify(files)
                resp.status_code = 200
                return resp
                
    except Exception as e:
        resp = jsonify(e)
        resp.status_code = 400
        return resp

# Process File by name or get processed files
@app.route('/api/v1/file', methods=['GET'])
def filesHandler():
    try:
        folder = request.args.get('folder')
        frame = request.args.get('frame')
        filepath = os.path.join(os.getcwd(), 'processed', folder, frame)
        return send_file(filepath)
    except Exception as e:
        resp = jsonify(e)
        resp.status_code = 400
        return resp

# Process File by name or get processed files
@app.route('/api/v1/labels', methods=['POST', 'GET'])
def labelsHandler():
    try:
        labelfile = os.path.join(os.getcwd(), 'labels.json')
        # return labels as json
        if request.method == 'GET':
            with open(labelfile, 'r') as f:
                data = json.load(f)
                resp = jsonify(data)
                resp.status_code = 200
                return resp
        # update labels
        elif request.method == 'POST':
            data = request.get_json(silent=True)
            print(data)
            with open(labelfile, 'w+') as f:
                json.dump(data, f)
                resp = jsonify(f"Successfully saved labels to {labelfile}")
                resp.status_code = 200
                return resp
    except Exception as e:
        resp = jsonify(e)
        resp.status_code = 400
        return resp
app.run()
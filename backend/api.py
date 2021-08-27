from flask import Flask, jsonify, request, redirect, send_file, abort
import os
from process_video import process_video
import json
import random


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

# Save labeled data and move target file into training set folder
@app.route('/api/v1/label', methods=['POST'])
def labelHandler():
    try:
        folder = request.args.get('folder')
        frame = request.args.get('frame')
        data = request.get_json(silent=True)
        image_file = os.path.join(os.getcwd(), folder, frame)
        print(f'data = {data}')
        print(f'file = {image_file}')
        labelfile = os.path.join(os.getcwd(), 'labeled', 'images', '{folder}-{frame}')
        with open(labelfile, 'w+') as f:
            json.dump(data, f)
            # Move target file to training set folder
            target = os.path.join(os.getcwd(), 'labeled', 'labels', '{folder}-{frame}')
            os.rename(image_file, target)
            resp = jsonify(f"Successfully saved labels to {labelfile}")
            resp.status_code = 200
            return resp
    except Exception as e:
        resp = jsonify(e)
        resp.status_code = 400
        return resp

# Get random image from image set
@app.route('/api/v1/get_next', methods=['GET'])
def nextHandler():
    folder = random.choice(list(training_files.keys()))
    frame = random.choice(training_files[folder])
    data = {'folder': folder, 'frame': frame}
    resp = jsonify(data)
    return resp #redirect(f"/api/v1/file?folder={folder}&frame={frame}")

def init(basepath):
    videospath = os.path.join(basepath, 'files')
    if not os.path.exists(videospath):
        os.makedirs(videospath)
    
    imagespath = os.path.join(basepath, 'processed')
    if not os.path.exists(imagespath):
        os.makedirs(imagespath)

    labeledpath = os.path.join(basepath, 'labeled', 'images')
    if not os.path.exists(labeledpath):
        os.makedirs(labeledpath)

    labeledpath = os.path.join(basepath, 'labeled', 'labels')
    if not os.path.exists(labeledpath):
        os.makedirs(labeledpath)

def get_list_of_files() -> dict:
    base_folder = os.path.join(os.getcwd(), 'processed')
    folders = os.listdir(base_folder)
    all_files = dict()
    # Iterate over all the entries
    for folder in folders:
        frames = []
        subfolder = os.path.join(base_folder, folder)
        if os.path.isdir(subfolder):
            images = os.listdir(os.path.join(base_folder, folder))
            for image in images:
                frames.append(image)
            all_files[folder] = frames
                
    return all_files

path = os.getcwd()
init(path)
training_files = get_list_of_files()
app.run()
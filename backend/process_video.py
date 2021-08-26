import cv2 as cv
from threading import Thread
import os

# Get blurry score
def get_blurry_score(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    return cv.Laplacian(gray, cv.CV_64F).var()
    
# Get the frames of each time period
def get_the_best_frame(foldername, idx, frames):
    best_frame = max([(get_blurry_score(frame), frame) for frame in frames])    
    cv.putText(best_frame[1], f'blurry score = {best_frame[0]}', (50,50), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    processed_filepath = os.path.join(os.getcwd(), 'processed', foldername)
    if not os.path.exists(processed_filepath):
        os.makedirs(processed_filepath)
    cv.imwrite(os.path.join(processed_filepath, f'{idx}.jpg'), best_frame[1])   

def process_video(filepath):
    try:
        foldername = os.path.basename(filepath)
        vidcap = cv.VideoCapture(filepath)
        framerate = vidcap.get(cv.CAP_PROP_FPS)
        number_of_limit = 10 #framerate
        print(f'Framerate = {framerate}')
        frames = []
        success,image = vidcap.read()
        count = 0
        while success:
            success,image = vidcap.read()
            if len(frames) != number_of_limit:
                frames.append(image)
            else:
                t = Thread(target=get_the_best_frame, args=(foldername, count, frames))
                t.start()
                frames = []
                count += 1
            success,image = vidcap.read()
        print(f'Found {count} samples with fps = {framerate}')
        return True
    except Exception as e:
        print(f'Error: {e}')
        return False
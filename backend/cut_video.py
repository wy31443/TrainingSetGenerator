import cv2 as cv
from threading import Thread

vidcap = cv.VideoCapture('test.mp4')
framerate = vidcap.get(cv.CAP_PROP_FPS)
number_of_limit = 10 #framerate
print(f'Framerate = {framerate}')

# Get blurry score
def get_blurry_score(image):
    gray = cv.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv.Laplacian(gray, cv2.CV_64F).var()
    
# Get the frames of each time period
def get_the_best_frame(idx, frames):
    best_frame = max([(get_blurry_score(frame), frame) for frame in frames])    
    cv.putText(best_frame[1], f'blurry score = {best_frame[0]}', (50,50), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    cv.imwrite("./frames/frame%d.jpg" % idx, best_frame[1]) 

frames = []
success,image = vidcap.read()
count = 0
while success:
    success,image = vidcap.read()
    if len(frames) != number_of_limit:
        frames.append(image)
    else:
        t = Thread(target=get_the_best_frame, args=(count, frames))
        t.start()
        frames = []
        count += 1
    success,image = vidcap.read()
print(f'Found {count} samples with fps = {framerate}')
import cv2
import numpy as np
from moviepy.editor import *

def stickbug(fname):

    clip = VideoFileClip(fname)
    if( clip.duration > 3 ): clip = clip.subclip(0,3)    
    last_frame = clip.get_frame(3)

    # Loads stickbug sound effects from 00:00 to 00:07
    stickbug_sound = AudioFileClip("assets/stickbugged.mp3").subclip(0,7)


    # Finding straight lines on the video
    gray = cv2.cvtColor(last_frame,cv2.COLOR_BGR2GRAY)

    kernel_size = 5
    blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size),0)

    # Processing canny edge detector
    low_threshold = 50
    high_threshold = 150
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 50  # minimum number of pixels making up a line
    max_line_gap = 20  # maximum gap in pixels between connectable line segments

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)


    # Selecting 10 from the lines (if found)
    lines = np.array(lines)
    if (len(lines) > 10):
        idx = np.random.choice(len(lines),10)
        stickbug_lines = lines[idx]
    # If not found 10 lines
    else:
        stickbug_lines = lines
        while (len(stickbug_lines) < 10):
            stickbug_lines = np.append(stickbug_lines, lines[0:10-len(stickbug_lines)], axis=0)


    # Drawing lines in last frame image
    sound_times = [0.504008, 0.938069, 1.262665, 1.609274, 1.874986, 2.28869, 2.621245, 2.901819, 3.261684, 4.47786, 5.1]
    line_image = np.copy(last_frame)  # creating a copy to draw lines on
    frames = []
    transition = ImageClip(last_frame).set_start(0).set_duration(sound_times[0])
    frames.append(transition)
    for i in range(10):
        line = stickbug_lines[i]
        time = sound_times[i]
        [x1,y1,x2,y2] = line[0]
        cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),7)
        
        img = ImageClip(np.copy(line_image)).set_start(time).set_duration(sound_times[i+1] - time)
        frames.append(img)


    # Drawing transition frames (lines moving)
    (height, width) = last_frame.shape[:2]
    timesteps = np.linspace(5.1, 7, 30)
    for i in range(29):
        time = timesteps[i]
        moving_lines = np.copy(last_frame)
        for j in range(len(stickbug_lines)):
            line = stickbug_lines[j][0]
            [x1,y1,x2,y2] = line
            
            cv2.line(moving_lines,(x1,y1),(x2,y2),(255,0,0),7)
            # Moving sticks to the center of the image
            if (x1 < width/2):        
                line[0] += width/200
            elif (x1 > width/2):
                line[0] -= width/200
            if (x2 < width/2):        
                line[2] += width/200
            elif (x2 > width/2):
                line[2] -= width/200
            if (y1 < height/2):        
                line[1] += height/200
            elif (y1 > height/2):
                line[1] -= height/200
            if (y2 < height/2):        
                line[3] += height/200
            elif (y2 > height/2):
                line[3] -= height/200          
            
        img = ImageClip(np.copy(moving_lines)).set_start(time).set_duration(timesteps[i+1] - time)
        frames.append(img)

    transition = CompositeVideoClip(frames)
    transition = transition.set_audio(stickbug_sound)

    # Load Get Stickbugged video
    stickbug_clip = VideoFileClip("assets/stickbug.mp4")
    stickbug_music = stickbug_clip.audio

    # concatenating clips
    final = concatenate_videoclips([clip, transition, stickbug_clip], method="compose")

    #final = final.set_audio(stickbug_audio)
    final.write_videofile(f"out-{fname}", fps=20)
    return
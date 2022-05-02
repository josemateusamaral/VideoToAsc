import cv2
import os
import sys
from PIL import Image
import time
import json
import tkinter
from tkinter import filedialog
from functools import partial

def generateAscImage(file,sx,sy):
    chars = """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;: "^`'."""
    image = Image.open(file)
    imageResized = image.resize((sx,sy))
    imageRecolored = imageResized.convert('L')
    pixelsList = imageRecolored.load()
    ascII_ART = ''
    for x in range(1,sy):
        for y in range(1,sx):
            char = int( pixelsList[y,x] / 3.7 )
            ascII_ART += chars[char]
        ascII_ART += '\n'
    return ascII_ART

def generateAscVideo(video,resolutionX,resolutionY):
    framerate = 10
    name = video.split('.')[0]
    tempFolder = name + '_tempFolder'
    os.mkdir(tempFolder)
    vidcap = cv2.VideoCapture(video)
    success,image = vidcap.read()
    cn = 1
    count = 0
    while success:
        cv2.imwrite(f"{tempFolder}/%d.jpg" % count, image)
        success,image = vidcap.read()
        os.system('cls')
        print(f'extracting frames... ',count)  
        count += 1
    frames = os.listdir(tempFolder)
    quantidadeDeFrames = len(frames) // framerate
    framesConverted = []
    for index,i in enumerate(frames):
        if (index + 1) % framerate != 0: continue
        os.system('cls')
        print(f'Converting frames... {index} de {quantidadeDeFrames}')
        asc = generateAscImage(file=f'{tempFolder}/' + i,sx=resolutionX,sy=resolutionY)
        framesConverted.append(asc)
    data = {'framerate':10,'resolutionX':resolutionX,'resolutionY':resolutionY,'frames':framesConverted}
    with open( name + '.ascVideo','w') as videoFile:
        json.dump(data,videoFile)
    for i in os.listdir(tempFolder): os.remove(tempFolder + '/' + i)
    os.rmdir(tempFolder)

def playAscVideo(video):
    with open(video,'r') as videoFile:
        fileData = json.load(videoFile)
        framerate = fileData['framerate']
        frames = fileData['frames']
    while True:
        for frame in frames:
            os.system('cls')
            print(frame)
            print(f'\nVIDEO: {video}\n\nFPS: {framerate}\n\nPRESS [ CRTL + C ] to close') 
            time.sleep(1/framerate)

class UI:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title('VTA')
        self.initialScreen()
        self.window.mainloop()
        self.lastVideo = None

    def initialScreen(self):
        self.zeroWindow()
        tkinter.Button(text='PLAY VIDEO',master=self.window,command=self.play).pack()
        tkinter.Button(text='CREATE VIDEO',master=self.window,command=self.createScreen).pack()
        tkinter.Button(text='EXIT',master=self.window,command=self.window.destroy).pack()

    def createScreen(self):
        self.zeroWindow()
        tkinter.Label(text='resolution\n\ninsert 360 480 to get the resolution 360x480').pack()
        entrada = tkinter.Entry()
        entrada.pack()
        tkinter.Button(text='create',command=partial(self.create,entrada)).pack()
        tkinter.Button(text='back',command=self.initialScreen).pack()

    def zeroWindow(self):
        for i in self.window.winfo_children():
            i.destroy()
        
    def create(self,entrada):
        entry = entrada.get()
        resolution = entry.split(' ')
        filename = filedialog.askopenfilename()
        self.lastVideo = filename
        generateAscVideo(filename,int(resolution[0]),int(resolution[1]))
        self.zeroWindow()
        name = filename.split('.')[0] + '.ascVideo'
        tkinter.Label(text='video create succesfully').pack()
        tkinter.Button(text='ok',command=self.initialScreen).pack()
        tkinter.Button(text='play',command=partial(self.play,name)).pack()
      
    def play(self,filename=None):
        if filename == None: filename = filedialog.askopenfilename()
        playAscVideo(filename)
        self.window.destroy() 

if __name__ == '__main__':
    UI()

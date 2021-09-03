# RekordBox Playlist Export into Folder
# get music path file from *.m3u8 playlist export format and bulk copy to destination folder
# at RekordBox app, right click on playlist you want to export -> Export a playlist to a file -> for music apps (*.m3u8)
# run this script with Administrator level command prompt, so it can have access for copy paste to user dir

import fnmatch
import os
from os import error
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from shutil import copyfile

root = Tk()
root.title('M3U8 Export Tool')
root.geometry("250x150")

global default_path
default_path = os.environ['USERPROFILE'] + "\\Music\\"
fileName = ''
folderName = ''

def browseFiles():
    global fileName
    global folderName
    fileName = filedialog.askopenfilename(initialdir = default_path,
                                          title = "Select M3U8 File",
                                          filetypes = (("M3U8 files","*.m3u8*"),("All files","*.*")))
    varInput.set(fileName)
    tail = os.path.split(fileName)[-1]
    fileTailName = str(tail).split(".")[0]
    varOutput.set(default_path+fileTailName)
    folderName = default_path+fileTailName

def browseFolder():
    global folderName
    folderName = filedialog.askdirectory(initialdir = default_path)
    varOutput.set('Output Folder: ' + folderName)

def copy(fileName, folderName):
    if fileName == '' or folderName == '':
        messagebox.showerror(title='No Input', message='Input somethings!')
    elif str(fileName).split(".")[-1] != 'm3u8':
        messagebox.showerror(title='Wrong File Input', message='Input M3U8 files only!')
    else:
        window = Toplevel()
        window.title('Log')
        h = Scrollbar(window, orient= 'horizontal')
        h.pack(side= BOTTOM, fill= X)
        v = Scrollbar(window)
        v.pack(side= RIGHT, fill=Y)
        t = Text(window, width = 100, height = 50, wrap = NONE, xscrollcommand = h.set, yscrollcommand = v.set)
        
        if not os.path.exists(folderName):
            os.mkdir(folderName)
        
        lines = []
        with open(fileName, encoding='utf-8') as f:
            lines = f.readlines()
        count = 0
        for line in lines:
            if fnmatch.fnmatch(line, '*:\\*.*') and line.find('#EXTINF') == -1:
                count += 1
                line = line.replace("\n","")
                tail = os.path.split(line)[-1]
                print('File Exist? ' + str(os.path.exists(line)))
                try:
                    copyfile(line, folderName+'\\'+tail)
                    print(f'{count} copying: {tail}')
                    t.insert(END, '[' + str(count) + '] Copied: '+ tail + ' to ' + folderName + '\n')
                except error:
                    t.insert(END, str(error) + ' ' + line + ' Path exist: ' + str(os.path.exists(line)) + '\n')
                t.pack(side=TOP, fill=X)
                h.config(command=t.xview)
                v.config(command=t.yview)

varInput = StringVar()
varInput.set('Open Files')
inputLabel = Label(root, textvariable = varInput).pack()

input = Button(root, text='Load .M3U8 File', command=browseFiles).pack()

varOutput = StringVar()
varOutput.set('Output Folder: ...')
outputLabel = Label(root, textvariable = varOutput).pack()

output = Button(root, text='Browse Output Folder', command=browseFolder).pack()

Label(root).pack()

copyBtn = Button(root, text='Copy!', command=lambda: copy(fileName, folderName)).pack()


root.mainloop()

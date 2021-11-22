from tkinter import *
import tkinter.messagebox
from tkinter.filedialog import *

fileNames = []
path = []
def selectFile():
    #Function to choose file and record filename
    try:
        fileOpen = askopenfilenames(title="Select file",filetypes=(("All files", ["*.txt","*.log"]),("Text files (.txt)", "*.txt"),("Log files (.log)", "*.log")))
        if fileOpen:
            for i in fileOpen:
                path.append("/".join(i.split("/")[:-1]))
                fileNames.append(i.split("/")[-1])
    except Exception as e:
        print(e)


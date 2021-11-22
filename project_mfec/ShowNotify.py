from ExportResult import toExcel
from SelectFile import fileNames,path
from search import sWarnPort, warnPort

from tkinter import *
import tkinter.messagebox
from tkinter.filedialog import *
import socket
from tkinter import ttk
from tkinter.ttk import Notebook


def exportEx():
    # Function for save result to Excel
    ask = tkinter.messagebox.askquestion("Confirm to export to Excel","Do you want to export to Excel ?")
    if ask == "yes":
        #send to export result
        mboxGui()
        tkinter.messagebox.showinfo("Save Success!","Save file as: " + siteName)
        toExcel(siteName)


def mboxGui():
    try:
        global siteName
        fileSave = asksaveasfilename(title="Select save file as",filetypes=[("Excel Workbook (.xlsx)","*.xlsx")],defaultextension=".xlsx")
        if fileSave:
            siteName = fileSave
    except Exception as e:
        print(e)
    

        


from tkinter.filedialog import SaveAs
import pandas as pd
import xlsxwriter
import openpyxl
from search import hostnames
from SelectFile import fileNames
from tkinter import *
import tkinter.messagebox

dfs = {}

def dataframe():
    # Function for convert file to dataframe
    try:
        
        for i in range(1):
            for fileName in fileNames:
                #Read file convert to dataframe
                df = pd.read_csv("conv_file/sort_file" + "/" + "sort" + fileName,sep='\t\t',header=1,engine='python')
                a = hostnames.get(fileName)
                dfs.setdefault(a,df)
                
    except Exception as e:
        print(e)

def toExcel(siteName):
    try:
        dataframe()
        
        # Workbook name
        writer = pd.ExcelWriter(siteName, engine = 'xlsxwriter')
        
        # Convert the dataframe to an XlsxWriter Excel object.
        for sheetName in dfs.keys():
            dfs[sheetName].to_excel(writer, sheet_name = sheetName, startrow = 1,index = False)
            # Get the xlsxwriter objects from the dataframe writer object.    
            worksheet = writer.sheets[sheetName]
            worksheet.write("A1","Hostname:")
            worksheet.write("B1",sheetName)
            # Apply the autofilter based on the dimensions of the dataframe.
            worksheet.autofilter(1, 0, dfs[sheetName].shape[0], dfs[sheetName].shape[1]-1)
            
        writer.save()

        return
    except Exception as e:
        print(e)

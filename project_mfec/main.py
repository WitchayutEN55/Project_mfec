from SelectFile import fileNames, selectFile, path
from search import *
from ShowNotify import *
from ExportResult import *
from search import sWarnPort, warnPort,catOrNex
from tkinter import *
import tkinter.messagebox
from tkinter.filedialog import *
import socket
from tkinter import ttk
from tkinter.ttk import Notebook


def aboutProgram():
    tkinter.messagebox.showinfo("About", "Made By: Witchayut Panyawai")  # message box


def exitProgram():
    confirm = tkinter.messagebox.askquestion("YES", "Do you want to close program ?")
    if confirm == "yes":
        root.destroy()

def on_click():
    nwLabel.after(1000, nwLabel.destroy())
    nwlabel()

def pre_click():
    exportEx()

def nwlabel():
    global nwLabel
    if nwConnection() == True:
        #label
        nwLabel = Label(toper_frame,text="Network Connection: " + "Connected",fg="green",font=20,bg="azure")
        nwLabel.grid(row=0,column=0,sticky="w",rowspan=2)
        
    else:
        #label
        nwLabel = Label(toper_frame,text="")
        nwLabel = Label(toper_frame,text="Network Connection: " + "Not Connected",fg="red",font=20,bg="azure")
        nwLabel.grid(row=0,column=0,sticky="w")
    
def nwConnection():
    try:
        socket.create_connection(('Google.com',80))
        return True
    except OSError:
        return False

def mainWindow():
    global root
    #widget
    root = Tk()
    root.title("Anomaly device detection tools for a computer network")
    #window size
    root.geometry("750x650") #990*770
    root.maxsize(width=750,height=650) #900*770
    root.configure(bg='azure')
    
    #menu
    mainMenu = Menu()
    root.config(menu=mainMenu)

    #sub main menu
    menuitem = Menu(mainMenu, tearoff=0)
    menuitem.add_command(label="About",command=aboutProgram)
    menuitem.add_separator()
    menuitem.add_command(label="Exit",command=exitProgram)

    #main menu
    mainMenu.add_cascade(label="Help",menu=menuitem)

    

    #frame
    global toper_frame
    toper_frame = Frame(root,padx=10,pady=10,bg='azure')
    toper_frame.grid(row=0 ,column=0 ,sticky="nw")
    top_frame = Frame(root,padx=10,pady=10,bg='azure')
    top_frame.grid(row=1 ,column=0 ,sticky="n")
    text_frame = Frame(root,padx=10,pady=10,bg='azure')
    text_frame.grid(row=2 ,column=0 ,sticky="e")
    radio_frame = Frame(root,padx=10,pady=10,bg='azure')
    radio_frame.grid(row=3 ,columnspan=2 ,sticky="s")
    low_frame = Frame(root,padx=10,pady=10,bg='azure')
    low_frame.grid(row=4 ,column=0 ,sticky="n")

    nwlabel()

    #progressbar
    global p
    p = ttk.Progressbar(top_frame,orient=HORIZONTAL,length=400,mode='determinate')
    p.grid(row=1 ,columnspan=2 ,sticky="s")
    

    #label
    outLabel = Label(text_frame,text="Warning: Suspicion Port Output:",font=6,fg="black",bg='azure')
    outLabel.grid(row=0,column=0,sticky='w')
    #label
    pLabel = Label(top_frame,text="Progress status",font=8,fg="Green",bg='azure')
    pLabel.grid(row=0,column=0,sticky='e')

    #label
    fileLabel = Label(low_frame,text="Warnning: Please select type of file .txt or log file",font=6,fg="Red",bg='azure')
    fileLabel.grid(row=2,column=2,sticky='s')
        
    #text
    global text_label
    text_label = Text(text_frame,bg="light gray",font=16, width=77,height=19)
    text_label.grid(row=1,column=0, rowspan=6,columnspan=2, padx=8, pady=4)
    

    #scrollbar
    scrollbar = Scrollbar(text_frame,command=text_label.yview)
    text_label['yscroll'] = scrollbar.set
    scrollbar.grid(row=1,column=2,rowspan=6,sticky='ns')
    text_label.delete("1.0", END)
    text_label.configure(state='disabled')

    #button
    global btn_search,btn_pre, btn_re
    btn_search = Button(radio_frame ,text="Run",fg="white",bg="gray", width=8,height=1,font=1,bd=5, padx=1, pady=1,command=selectSwitch)
    btn_search.grid(row=1,column=0,columnspan=2,padx=30)
    btn_renw = Button(toper_frame ,text="Checking Network",fg="white",bg="gray", width=14,height=1,bd=5, padx=1, pady=1,command=on_click)
    btn_renw.grid(row=0,column=3,sticky='w')
    btn_pre = Button(radio_frame ,text="Export",fg="white",bg="gray", width=8,height=1,font=1,bd=5, padx=1, pady=1,command=pre_click,state='disabled')
    btn_pre.grid(row=1,column=3,columnspan=2,padx=30)
    btn_re = Button(radio_frame ,text="Restart",fg="white",bg="gray", width=8,height=1,font=1,bd=5, padx=1, pady=1,command=rePro,state='disabled')
    btn_re.grid(row=1,column=5,columnspan=2,padx=30)

    return root
    

def rePro():
    fileNames.clear()
    path.clear()
    hostnames.clear()
    warnPort.clear()
    sWarnPort.clear()
    dfs.clear()
    catOrNex.clear()
    root.destroy()
    main()

def myprogress():
    p.stop()
    p['value'] = 100


def warnning(): 
    # Function for warnning after sort file

    try:
        tkinter.messagebox.showwarning("Warning!", "Warning suspicious port!")
        text_label.tag_config('beforewarn', foreground="blue")
        text_label.tag_config('afterwarn', foreground="red")
        for file,ports in warnPort.items():
            text_label.configure(state='normal')
            mss = "File: " + file + " Before filter cisco device!\n" 
            text_label.insert(INSERT,mss,'beforewarn')
            
            for port in ports:
                mss2 = "This port " + port + " is suspicious.\n"
                text_label.insert(INSERT,mss2,'beforewarn')
            text_label.insert(INSERT,"-"*40+"\n")
        
        for file,ports in sWarnPort.items():
            if len(sWarnPort) == 0:
                mss3 = "File: " + file  + " don't have any port that look suspicious\n"
                text_label.insert(INSERT,mss3,'afterwarn')
                text_label.insert(INSERT,"*"*40+"\n")
            else:
                mss4 = "File: " + file + " After filter cisco device!!\n"
                text_label.insert(INSERT,mss4,'afterwarn')
                for port in ports:
                    mss5 = "This port " + port + " is suspicious.\n"
                    text_label.insert(INSERT,mss5,'afterwarn')
                text_label.insert(INSERT,"*"*40+"\n")

        msspre = "Show switch type of file\n"
        text_label.insert(INSERT,msspre)
        text_label.insert(INSERT,"+"*40+"\n")
        for file,tf in catOrNex.items():
            msstf = "File: " + file + " is " + tf + "\n"
            text_label.insert(INSERT,msstf)
        text_label.insert(INSERT,"+"*40+"\n")

        text_label.configure(state='disabled')
    except Exception as e:
        print(e)


def selectSwitch():

    try:
        selectFile()
        if len(fileNames) == 0:
            pass
        elif len(fileNames) > 0:
            btn_search.configure(state='disabled')
            p.start()
            searchAll()
            warnning()
            myprogress()
            btn_pre.configure(state='normal')
            btn_re.configure(state='normal')
            return

    except Exception as e:
        print(e)


def main():
    try:
        mainWindow()
        root.mainloop()

        
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
    

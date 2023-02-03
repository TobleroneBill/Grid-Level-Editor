# has a box for given file path (defaults to current directory), which can be edited
# Button for export Grid as txt, could try a json but will see if that's easier to parse
# Current Message Label, to display what this part of the app is doing
import os
import tkinter
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox


position = [0,0]
lastDir = ""

def SelectFolder(last,buttonUpdate):
    path = filedialog.askdirectory(title="Select a folder")
    if path != "":
        buttonUpdate.delete(0, "end")
    buttonUpdate.insert(0,path)
    buttonUpdate.update()
    global lastDir
    lastDir = path

def UpdatePosition(root):
    position[0] = root.winfo_x()
    position[1] = root.winfo_y()

def ExportToDir(exportGrid,directory,filename):
    global lastDir
    lastDir = directory
    print(directory)
    #try:
    path = directory + f"\{filename}.txt"

    print(path)
    file = open(path,"w")

    for x in exportGrid:
        for y in x:
            file.write(str(y))
        file.write("\n")

    file.close()
    #except:
    #    messagebox.showerror("Error", 'Error occurred while writing to given directory')
    #    return





def main(exportGrid):
    root = tkinter.Tk()
    root.title("Export Level")
    root.pack_propagate(0)
    actionString = "Please select a directory"
    root.geometry(f"+{position[0]}+{position[1]}")

    directory = str(os.getcwd())
    mainframe = ttk.Frame(root,padding="3 3 12 12")
    mainframe.grid(column=0,row=0,sticky="n,w,e,s")
    root.columnconfigure(0,weight=1)
    root.rowconfigure(0,weight=1)


    l_Action = ttk.Label(mainframe,width=len(actionString),text=actionString)
    l_Action.grid(column=2,row=1,sticky="w,e")

    direntry = ttk.Entry(mainframe,width=75,textvariable=directory)
    direntry.grid(column=2,row=2,sticky="w,e")
    # insert last used directory
    if lastDir == "":
        direntry.insert(0,directory)
    else:
        direntry.insert(0,lastDir)

    # ______Name Entry_______
    name = ""

    # Name
    l_name = ttk.Label(mainframe,width=len("Input Name"),text ="Input Name")
    l_name.grid(column=3,row=1,sticky="w,e")
    # Input
    e_name = ttk.Entry(mainframe,width=20,textvariable=name)
    e_name.grid(column=3,row=2,sticky="w,e",padx=5)

    # get directory
    b_filedialog = tkinter.Button(mainframe,text="Select Folder",command=lambda: SelectFolder(lastDir,direntry))
    b_filedialog.grid(column=1,row=2,sticky="w,e" ,padx=5)

    # cancel/quit
    b_cancel = tkinter.Button(mainframe,text="Cancel",command=lambda: root.destroy())
    b_cancel.grid(column=2,row=3,sticky="w,e",pady=3)

    # export
    b_export = tkinter.Button(mainframe,text="export",command=lambda: ExportToDir(exportGrid,direntry.get(),e_name.get()))
    b_export.grid(column=2,row=4,sticky="w,e",pady=3)

    # save window position
    getRootPos = lambda rootPos : UpdatePosition(root)
    root.bind('<Configure>',getRootPos)

    root.mainloop()
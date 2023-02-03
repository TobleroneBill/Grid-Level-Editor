# file location of old grid text file
# read the contents of each line
# make a 256 long array
# for each line of the file, the every index in the 256 array will = the lines

# Game should update automatically, so shouldn't be too difficult
# just need TKINTER stuff which honestly sucks alot

from tkinter import filedialog
from tkinter import messagebox

def main(oldgrid):
    newGrid = oldgrid
    path = filedialog.askopenfilename(title="Select a File", filetypes=[("Text Files", ".txt")])

    if path:
        try:
            LevelGrid = open(path, 'r')
            Grid = []
            Col = []

            for item in LevelGrid.read():
                if item == "\n":
                    Grid.append(Col)  # add column to level data
                    Col = []  # reset Column
                    continue
                Col.append(int(item))
            LevelGrid.close()
            newGrid = Grid
        except:
            messagebox.showerror("Incorrect File Format",'Text File wasnt correctly Formatted')
    else:
        print("Cancelled")

    for item in newGrid:
        if item != [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
            print(item)



    return newGrid

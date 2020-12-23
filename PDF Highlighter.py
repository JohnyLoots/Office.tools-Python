from tkinter import *
from tkinter import filedialog 
from tkinter import messagebox
import sys
import os 
import fitz
import time
from datetime import datetime


#           Functions
#===============================

def Help_box(): 
    help_options = "How it works:\n\nEnter the name you would like to highlight in the entrybox then press start and select the PDF you would like to be handled.\n\n" + "1.File will be saved in the same directory as script.\n" + "2.File will be named according to date and time.\n" + "3.If the console prints out at the end: for inst in text_instances TypeError: NoneType object is not iterable.\nIt means you didn't enter a name\n" + "4.Works with PyMuPDF and Tkinter.\n"
    messagebox.showinfo(title="Instructions", message=help_options)

global filename
def browseFiles(): 
    username = os.environ.get('USERNAME')
    global filename 
    filename = filedialog.askopenfilename(initialdir = f"C:/Users/{username}/Documents", 
                                          title = "Select a File", 
                                          filetypes = (("PDF Files", 
                                                        "*.pdf*"), 
                                                       ("all files", 
                                                        "*.*"))) 

    return filename

def get_text(file):
    doc = fitz.open(file)
    for pages in doc:
       page_content = pages.getText("text")
       print(page_content)

def Submit():  
    global text
    text = textentry.get()
    Start()
    return text

def SaveFile():
    global saveas
    current_dt_float = datetime.now()
    current_dt = current_dt_float.strftime("%Y-%B-%d %H.%M.%S %p")
    pdf_extension = ".pdf"
    saveas = str(f"./{current_dt}{pdf_extension}")
    return saveas

def Start():
    if text == "":
        messagebox.showerror(title="Error", message="No name was entered.")
    else:
        try:
            filename
        except NameError:
            messagebox.showerror(title="Error", message="No file was selected.")
        else:
            filetypes = filename.split(".")
            file_extension = "." + filetypes[-1]
            if file_extension != ".pdf":
                messagebox.showerror(title="Error", message="File is not a pdf.")
            else:
                get_text(filename)
                doc = fitz.open(filename)
                inst_counter = 0
                for pi in range(doc.pageCount):
                     
                     page = doc[pi]
                     text_instances = page.searchFor(text)   
                    
                     for inst in text_instances:  
                         inst_counter += 1
                         highlight = page.addHighlightAnnot(inst)

                SaveFile()
                doc.save(saveas)
                messagebox.showinfo(title="PDF Converter", message="PDF Highligted")
                print(f"The text was found {inst_counter} times.")

def Exit(): 
    sys.exit()
    window.close() 

                #GUI
#==================================

window = Tk()
window.title('PDF Highlighter') 
window.geometry('310x450')
window.config(background = "#D1F8FF") 


#test = filename
menubar = Menu(window)
filemenu = Menu(menubar, tearoff=0,)
filemenu.add_command(label="Open", command=browseFiles)
filemenu.add_command(label="Help", command=Help_box)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=Exit)
menubar.add_cascade(label="File", menu=filemenu)

label_Frame1 = LabelFrame(window, height = 100, width = 309, bg = "#D1F8FF")
label_heading = Label(label_Frame1, text = "PDF Highlighter",font= 'Arial 17 bold' , height = 0, fg = "#000000", bg = "#D1F8FF")
label_Frame2 = LabelFrame(window, height = 30, width = 309, bg = "#D1F8FF")

Label_FILE = Label(label_Frame2, text = f"File being handled:",font= 'Verdena 7 ' , height = 0, fg = "#000000", bg = "#D1F8FF")


label_Frame4 = LabelFrame(window, height = 70, width = 309, bg = "#D1F8FF")
button_select_file = Button(label_Frame4, text = "Select file",width = 10, height = 2, command = browseFiles)
button_submit = Button(label_Frame4, text = "Start",width = 10, height = 2,command = Submit)
button_exit = Button(label_Frame4,  text = "Quit",width = 10, height = 2, command = Exit)

label_Frame3 = LabelFrame(window, height = 50, width = 309, bg = "#D1F8FF")
textentry = Entry(label_Frame3, width = 45,)
subheading = Label(label_Frame3, text = "Please enter the name or word you would like to highlight ?",font= 'Arial 7', height = 0, fg = "#000000", bg = "#D1F8FF")

canvasforimg = Canvas(label_Frame1, width = 78, height = 78, bg = "#D1F8FF")
img = PhotoImage(file="./img/ico.png")
img_scale = img.subsample(2,2)
canvasforimg.create_image(0,0,anchor=NW, image=img_scale)

canvasforimg.place(x=15,y=5)#20
label_Frame1.place(x=1,y=0)
label_heading.place(x=105,y=30)
label_Frame2.place(x=1,y=220)

Label_FILE.place(x=10,y=4)
label_Frame3.place(x=1,y=100)
textentry.place(x=15,y=20)
subheading.place(x=15,y=1)
label_Frame4.place(x=1,y=150)
button_submit.place(x=15,y=11.5)
button_select_file.place(x=113,y=11.5)
button_exit.place(x=210,y=11.5)

window.config(menu=menubar,)
window.geometry("310x250") 
window.mainloop()

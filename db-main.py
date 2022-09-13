import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk   # To get tabs (called Notebooks in Tkinter), you need to use a part of the Tkinter library called ttk. This adds a few more widgets to the library, things like Tabs, ComboBoxes, Progress Bars and Treeviews.

from PIL import ImageTk, Image  # PIL is short for Python Image Library
import pymysql

import os  # os library deals with Operating System stuff
import shutil  # a shell utility. We'll need it to move an image file to the correct folder.

import db_config
    

def on_tab_selected(event): # The function makes use of two Boolean flags. If blank_textboxes_tab_two is False and is image_selected True, then we reload the database.
    global blank_textboxes_tab_two
    global image_selected

    selected_tab = event.widget.select()
    tab_text = event.widget.tab(selected_tab, "text")

    if tab_text == "All Records":

        if (blank_textboxes_tab_two is False) and (image_selected is True):
            load_database_results()

    if tab_text == "Add New Record":
        blank_textboxes_tab_two = True
        image_selected = False

def load_database_results():

    try:
        global rows
        global num_of_rows

        con = pymysql.connect(host=db_config.DB_SERVER, user=db_config.DB_USER, password=db_config.DB_PASS, database=db_config.DB) 
        
        sql = "SELECT * FROM tbl_employees"

        cursor = con.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        num_of_rows = cursor.rowcount
        cursor.close()

        con.close() #close the connection

        has_loaded_successfully = True

    except pymysql.InternalError as e:
        has_loaded_successfully = database_error (e)
    except pymysql.OperationalError as e:
        has_loaded_successfully = database_error (e)
    except pymysql.ProgrammingError as e:
        has_loaded_successfully = database_error (e)
    except pymysql.DatabaseError as e:
        has_loaded_successfully = database_error (e)
    except pymysql.IntegrityError as e:
        has_loaded_successfully = database_error (e)
    except pymysql.NotSupportedError as e:
        has_loaded_successfully = database_error (e)

    return has_loaded_successfully



def database_error(err):
    messageabox.showinfo("Error", err)
    return (False)

def image_path(file_path):
    open_image = Image.open(file_path)
    image = ImageTk.PhotoImage(open_image)
    return image

def load_photo_tab_one(file_path):
    image = image_path(file_path)
    imgLabelTabOne.configure(image=image) # The configure method is used to reconfigure an image. Remember: it has the default image in it, when the program loads. 
                                          # We need to erase this and configure a new one, which will be stored inside of the variable called image. It resets the label.
    imgLabelTabOne.image = image  # This line takes care of placing the image inside of the label.


# ==========SETTING UP THE ROOT WINDOW =================================

form = tk.Tk() # Creating an instance of Tk initializes this interpreter and creates the root window. If you don't explicitly initialize it, one will be implicitly created when you create your first widget.

form.title("Database Form")

form.geometry("500x280")

tab_parent = ttk.Notebook(form)

# ===============================================================

def scroll_forward():

    global row_counter
    global num_of_rows

    if row_counter >= (num_of_rows -1):
        messagebox.showinfo("Database Error", "End of database")

    else:
        row_counter = row_counter + 1
        
        scroll_load_data()

def scroll_back():
    global row_counter

    if row_counter == 0:
        messagebox.showinfo("Database Error", "Start of database")

    else:
        row_counter = row_counter - 1
        scroll_load_data()
        
def scroll_load_data():
        fName.set(rows[row_counter] [1])
        fam.set(rows[row_counter][2])
        job.set(rows[row_counter][3])

        try:
            ph_path = db_config.PHOTO_DIRECTORY + rows[row_counter][4]
            load_photo_tab_one(ph_path)

        except FileNotFoundError:
            load_photo_tab_one(db_config.PHOTO_DIRECTORY + "default.png")

def load_photo_tab_two(file_path):
    image = image_path(file_path)
    imgLabelTabTwo.configure(image=image)
    imgLabelTabTwo.image = image



def select_image():  # adding function to the image button.
    global image_selected
    global image_file_name
    global file_new_home
    global file_to_copy

    path_to_image = filedialog.askopenfilename(initialdir="/",
        title="Open File",
        filetypes=(("PNGs", "*.png"), ("GIFs", "*.gif"), ("All Files", "*.*")))
    try:
        if path_to_image:
            image_file_name = os.path.basename(path_to_image)
            file_new_home = db_config.PHOTO_DIRECTORY + image_file_name
            file_to_copy = path_to_image
            image_selected = True
            load_photo_tab_two(file_to_copy)
    except IOError as err:
        image_selected = False
        messagebox.showinfo("File Error", err)

# ===========SETTING UP TAB TWO =====================

def add_new_record():   # ASSURING THAT WE START WITH 3 BLANK TEXT FIELDS.
    global blank_textboxes_tab_two
    global file_new_home
    global file_to_copy
    blank_textbox_count = 0

    if fNameTabTwo.get() == "":
        blank_textbox_count = blank_textbox_count + 1
    if famTabTwo.get() == "":
        blank_textbox_count = blank_textbox_count + 1
    if jobTabTwo.get() == "":
        blank_textbox_count = blank_textbox_count + 1
    if blank_textbox_count > 0:
        blank_textboxes_tab_two = True
        messagebox.showinfo("Database Error", "Blank Text boxes")
    elif blank_textbox_count == 0:
        blank_textboxes_tab_two = False

        if image_selected:
            try:
                shutil.copy(file_to_copy, file_new_home)
            except shutil.SameFileError:
                pass
            insert_into_database(fNameTabTwo.get(), famTabTwo.get(), jobTabTwo.get(), image_file_name)      # calls a function, passing 4 variables.
        else:
            messagebox.showinfo("File Error", "Please select an image")

def insert_into_database(first_field, family_field, job_field, photo_field):     # function to insert a new file into our database. 
    try:
        con = pymysql.connect(host=db_config.DB_SERVER, # connects to our database.
                                  user=db_config.DB_USER,
                                  password=db_config.DB_PASS,
                                database=db_config.DB)
        sql = "INSERT INTO tbl_employees (First_Name, Family_Name, Job_Title, Photo) VALUES (%s, %s, %s, %s)"
        vals = (first_field, family_field, job_field, photo_field)
        cursor = con.cursor()    #  A cursor is an object which helps to execute the query and fetch the records from the database. The cursor plays a very important role in executing the query.
        cursor.execute(sql, vals)  #  This method executes the given database operation (query or command). The parameters found in the tuple or dictionary params are bound to the variables in the operation.
        con.commit()  #  The commit() method is used to confirm the changes made by the user to the database. Whenever any change is made to the database using update or any other statements, it is necessary to commit the changes.
        cursor.close()
        con.close()
        messagebox.showinfo("Database", "Record Added to Database")
    except pymysql.ProgrammingError as e:
        database_error(e)

    except pymysql.DataError as e:
        database_error(e)

    except pymysql.IntegrityError as e:
        database_error(e)

    except pymysql.NotSupportedError as e:
        database_error(e)

    except pymysql.OperationalError as e:
        database_error(e)

    except pymysql.InternalError as e:
        database_error(e)

def search_records():
    con = pymysql.connect(host=db_config.DB_SERVER, # connects to our database.
                        user=db_config.DB_USER,
                        password=db_config.DB_PASS,
                        database=db_config.DB)
    sql_query = "SELECT * FROM tbl_Employees WHERE Job_Title=%s AND Family_Name=%s"
    vals = (options_var.get(), search_text_var.get())
    cursor = con.cursor()
    cursor.execute(sql_query, vals)
    my_rows = cursor.fetchall()
    total_rows = cursor.rowcount
    cursor.close()
    con.close()
    print(my_rows)
    print("TOTAL ROWS: ", total_rows)








# ====GLOBAL VARIABLES=================

file_name = "default.png"
path = db_config.PHOTO_DIRECTORY + file_name
rows = None
num_of_rows = None
row_counter = 0
image_selected = False
image_file_name = None
file_to_copy = None
file_new_home = None
blank_textboxes_tab_two = True

# ========== The Notebook 'widget' is a method that allows you to select pages of contents by clicking on tabs: ==============  # https://www.pythontutorial.net/tkinter/tkinter-notebook/
#To set up a tab for your notebook, you create Form objects with the name of a Notebook between round brackets. 

tab1 = ttk.Frame(tab_parent)
tab2 = ttk.Frame(tab_parent)
tab3 = ttk.Frame(tab_parent)

# Between double quotes and double pointy brackets, we have NotebookTabChanged. This is something called an event. 
# After a comma, we have a function that's going to deal with this event: on_tab_selected. (on_tab_selected is just a function name, and we could have called it something else.)

tab_parent.bind("<<NotebookTabChanged>>", on_tab_selected)


# THIS SETS THE TAB OBJECTS TO THE PARENT OBJECT.

tab_parent.add(tab1, text="All Records")
tab_parent.add(tab2, text="Add New Record")
tab_parent.add(tab3, text="Search")

# ====== SET UP STRING VARS ====================

fName = tk.StringVar()
fam = tk.StringVar()
job = tk.StringVar()

fNameTabTwo = tk.StringVar()
famTabTwo = tk.StringVar()
jobTabTwo = tk.StringVar()





# === WIDGETS FOR TAB ONE
firstLabelTabOne = tk.Label(tab1, text="First Name:")
familyLabelTabOne = tk.Label(tab1, text="Family Name:")
jobLabelTabOne = tk.Label(tab1, text="Address:")

firstEntryTabOne = tk.Entry(tab1, textvariable=fName)
familyEntryTabOne = tk.Entry(tab1, textvariable=fam)
jobEntryTabOne = tk.Entry(tab1, textvariable=job)

# ============ REMOVED THESE TWO LINES AND SIMPLIFIED OUR CODE ========================
#openImageTabOne = Image.open(path)  # This uses the Image library. This has a method called open. In between round brackets, you need the path and filename of your image.
#imgTabOne = ImageTk.PhotoImage(openImageTabOne) #turns the image type into an object.
# ====================================================================================

imgTabOne = image_path(path)
imgLabelTabOne = tk.Label(tab1, image=imgTabOne)

imgLabelTabOne = tk.Label(tab1, image=imgTabOne) # assigning a variable to the label (creates the label)

buttonForward = tk.Button(tab1, text="Forward", command=scroll_forward)
buttonBack = tk.Button(tab1, text="Back", command=scroll_back)

# === ADD WIDGETS TO GRID ON TAB ONE
firstLabelTabOne.grid(row=0, column=0, padx=15, pady=15)
firstEntryTabOne.grid(row=0, column=1, padx=15, pady=15)

familyLabelTabOne.grid(row=1, column=0, padx=15, pady=15)
familyEntryTabOne.grid(row=1, column=1, padx=15, pady=15)

jobLabelTabOne.grid(row=2, column=0, padx=15, pady=15)
jobEntryTabOne.grid(row=2, column=1, padx=15, pady=15)

imgLabelTabOne.grid(row=0, column=2, rowspan=3, padx=15, pady=15)

buttonBack.grid(row=3, column=0, padx=15, pady=15)
buttonForward.grid(row=3, column=2, padx=15, pady=15)

# === WIDGETS FOR TAB TWO
firstLabelTabTwo = tk.Label(tab2, text="First Name:")
familyLabelTabTwo = tk.Label(tab2, text="Family Name:")
jobLabelTabTwo = tk.Label(tab2, text="Address:")

firstEntryTabTwo = tk.Entry(tab2, textvariable=fNameTabTwo)
familyEntryTabTwo = tk.Entry(tab2, textvariable=famTabTwo)
jobEntryTabTwo = tk.Entry(tab2, textvariable=jobTabTwo)

openImageTabTwo = Image.open(path)
imgTabTwo = ImageTk.PhotoImage(openImageTabTwo)
imgLabelTabTwo = tk.Label(tab2, image=imgTabTwo)

buttonCommit = tk.Button(tab2, text="Add Record to Database", command=add_new_record)
buttonAddImage = tk.Button(tab2, text="Add Image", command=select_image)

# === ADD WIDGETS TO GRID ON TAB TWO
firstLabelTabTwo.grid(row=0, column=0, padx=15, pady=15)
firstEntryTabTwo.grid(row=0, column=1, padx=15, pady=15)
imgLabelTabTwo.grid(row=0, column=2, rowspan=3, padx=15, pady=15)

familyLabelTabTwo.grid(row=1, column=0, padx=15, pady=15)
familyEntryTabTwo.grid(row=1, column=1, padx=15, pady=15)

jobLabelTabTwo.grid(row=2, column=0, padx=15, pady=15)
jobEntryTabTwo.grid(row=2, column=1, padx=15, pady=15)

buttonCommit.grid(row=4, column=1, padx=15, pady=15)
buttonAddImage.grid(row=4, column=2, padx=15, pady=15)

# ====SETTING UP WIDGETS FOR TAB 3, AND ADDING THEM TO THE GRID ============================

search_text_var = tk.StringVar()
search_family = tk.Entry(tab3, textvariable=search_text_var)

contents = {'Graphic Artist', 'IT Manager', 'Programmer', 'Systems Analyst', 'Support'}

options_var = tk.StringVar()
options_var.set("Select Job Title")

dropdown = tk.OptionMenu(tab3, options_var, *contents)
buttonSearch = tk.Button(tab3, text="Search", command=search_records)

search_family.grid(row=0, column=0, padx=15, pady=15)
dropdown.grid(row=0, column=1, padx=15, pady=15)
buttonSearch.grid(row=0, column=2, padx=15, pady=15)


success = load_database_results()

if success:

    fName.set(rows[0][1])
    fam.set(rows[0][2])
    job.set(rows[0][3])
    photo_path = db_config.PHOTO_DIRECTORY + rows[0][4]
    load_photo_tab_one(photo_path)


#Finally, you need to pack the tab parent and its tabs:

tab_parent.pack(expand=1, fill='both')


form.mainloop()


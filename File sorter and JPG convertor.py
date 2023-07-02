import time
import os
import shutil
import customtkinter as ctk
import tkinter
import re
from datetime import datetime
from PIL import Image

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

root = ctk.CTk()
root.geometry('900x500')
root.title("File sorter and JPG convertor")
root.resizable(False,False)

# selects the function for the chosen mode in option_menu
def select_mode():
    mode = option_menu.get()
    try:
        if mode == 'Date' or mode == 'Name':
            date_or_Name_sorter(src.get(), dst.get())
        elif mode == 'Date & JPG' or mode == 'Name & JPG':
            date_or_name_sorter_jpg(src.get(), dst.get(), int(jpg_quality.get()))
        elif mode == 'JPG':
            convert_to_jpg(src.get(), dst.get(), int(jpg_quality.get()))
    except Exception as e:
        # generates error message
        now = datetime.now()
        x = str(e)
        if x == "invalid literal for int() with base 10: ''":
            x = 'invalid quality input for jpg'
        status_textbox.configure(state="normal")
        status_textbox.insert("0.0",f'[{str(now.strftime("%Y/%m/%d, %H:%M:%S"))}] an error has occurred: {x}\n')
        status_textbox.configure(state="disabled")
        print(x)


def date_or_Name_sorter(source_folder, destination_folder):
    start_time = time.time()
    mode = option_menu.get()

    # Create the destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)
    count = len([name for name in os.listdir(destination_folder) if os.path.isfile(os.path.join(destination_folder, name))])
    sortet_image_count = 0
    # Sort files by modified date
    for root, _, files in os.walk(source_folder):
        # Sortiere die Dateien nach dem Änderungsdatum
        if mode == 'Date':
            sorted_files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(root, x)))
        elif mode == 'Name':
            sorted_files = sorted(files, key=lambda x: int(re.findall(r'\d+', x)[0]))

    # Copy the files to the destination folder and number them
        for i, file in enumerate(sorted_files, start=1):
            source_path = os.path.join(root, file)
            filename, file_extension = os.path.splitext(source_path)
            destination_path = os.path.join(destination_folder, f"{count}{file_extension}")
            count += 1
            sortet_image_count += 1

            # Kopiere die Datei als Original und als PNG
            shutil.copy2(source_path, destination_path)
    # ends counting time
    end_time = time.time()
    # calculates the time taken
    execution_time = end_time - start_time
    # converts the time in min and sec or only sec
    if execution_time >= 60:
        execution_time = execution_time /60
        minutes = int(execution_time)
        seconds = float((execution_time - minutes) * 60)
        process_time = f' in {minutes}min {round(seconds, 1)}s'
    else:
        process_time = f' in {round(execution_time, 2)}s'
    # real time
    now = datetime.now()
    # message after process is done
    status_textbox.configure(state="normal")
    status_textbox.insert("0.0",f'[{str(now.strftime("%Y/%m/%d, %H:%M:%S"))}] Sorting was sucessfully {sortet_image_count} files sorted {process_time}\n')
    status_textbox.configure(state="disabled")


def date_or_name_sorter_jpg(source_folder, destination_folder, quality):
    start_time = time.time()
    mode = option_menu.get()

    # Create the destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)
    count = len([name for name in os.listdir(destination_folder) if os.path.isfile(os.path.join(destination_folder, name))])
    convertet_image_count = 0
    # Sort files by modified date
    for root, _, files in os.walk(source_folder):
        # Sortiere die Dateien nach dem Änderungsdatum
        if mode == 'Date & JPG':
            sorted_files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(root, x)))
        elif mode == 'Name & JPG':
            sorted_files = sorted(files, key=lambda x: int(re.findall(r'\d+', x)[0]))
    # Copy the files to the destination folder and number them
        for i, file in enumerate(sorted_files, start=1):
            source_path = os.path.join(root, file)
            filename, file_extension = os.path.splitext(source_path)
            destination_path = os.path.join(destination_folder, f"{count}.jpg")

            # Kopiere die Datei als Original und als PNG
            img = Image.open(source_path)
            img = img.convert("RGB")  # Umwandlung in den RGB-Modus
            img.save(destination_path, "JPEG", quality=quality)
            
            count += 1
            convertet_image_count += 1

    end_time = time.time()
    # calculates the time taken
    execution_time = end_time - start_time
    # converts the time in min and sec or only sec
    if execution_time >= 60:
        execution_time = execution_time /60
        minutes = int(execution_time)
        seconds = float((execution_time - minutes) * 60)
        process_time = f' in {minutes}min {round(seconds, 1)}s'
    else:
        process_time = f' in {round(execution_time, 2)}s'
    # real time
    now = datetime.now()
    # message after process is done
    status_textbox.configure(state="normal")
    status_textbox.insert("0.0",f'[{str(now.strftime("%Y/%m/%d, %H:%M:%S"))}] Converting was sucessfully {convertet_image_count} files convertet {process_time}\n')
    status_textbox.configure(state="disabled")


def convert_to_jpg(input_folder, output_folder, quality):
    start_time = time.time()
    convertet_image_count = 0
    try:
        for filename in os.listdir(input_folder):
            if filename.endswith((".png", ".jpg", ".jpeg")):
                input_path = os.path.join(input_folder, filename)
                output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".jpg")

                img = Image.open(input_path)
                img = img.convert("RGB")  # Umwandlung in den RGB-Modus
                img.save(output_path, "JPEG", quality=quality)
                convertet_image_count += 1

    except Exception as e:
        print(f"Fehler beim Konvertieren der Bilder: {str(e)}")
    
    end_time = time.time()
    # calculates the time taken
    execution_time = end_time - start_time
    # converts the time in min and sec or only sec
    if execution_time >= 60:
        execution_time = execution_time /60
        minutes = int(execution_time)
        seconds = float((execution_time - minutes) * 60)
        process_time = f' in {minutes}min {round(seconds, 1)}s'
    else:
        process_time = f' in {round(execution_time, 2)}s'
    # real time
    now = datetime.now()
    # message after process is done
    status_textbox.configure(state="normal")
    status_textbox.insert("0.0",f'[{str(now.strftime("%Y/%m/%d, %H:%M:%S"))}] Converting was sucessfully {convertet_image_count} files convertet {process_time}\n')
    status_textbox.configure(state="disabled")



frame = ctk.CTkFrame(master=root, fg_color='transparent')
frame.pack(pady=16, padx=24, fill='both', expand=True)

label = ctk.CTkLabel(master=frame,
                               text='File sorter and JPG convertor',
                               font=("sora", 32))
label.place(relx=0.5, rely=0.05, anchor=tkinter.CENTER)
# source entry
src = ctk.CTkEntry(master=frame,
                            placeholder_text='Input folder',
                            font=("sora", 20),
                            width=825,
                            height=32,
                            corner_radius=5)
src.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)
# destination entry
dst = ctk.CTkEntry(master=frame,
                            placeholder_text='Output folder',
                            font=("sora", 20),
                            width=825,
                            height=32,
                            corner_radius=5)
dst.place(relx=0.5, rely=0.35, anchor=tkinter.CENTER)
# entry for quality by jpg
jpg_quality = ctk.CTkEntry(master=frame,
                            placeholder_text='JPG Quality',
                            font=("sora", 20),
                            width=150,
                            height=32,
                            corner_radius=5)
# selects the funktion for option_menu 
def mode(self):
    mode = option_menu.get()
    if 'JPG' in mode:
        show_jpg_quality()
    else:
        hide_jpg_quality()
# hides jpg_quality
def hide_jpg_quality():
    jpg_quality.place_forget()
# shows jpg_quality
def show_jpg_quality():
    jpg_quality.place(relx=0.545, rely=0.49, anchor=tkinter.CENTER)
# menu for changing the mode
option_menu = ctk.CTkOptionMenu(master=frame,
                                font=('sora', 20),
                                width=180,
                                height=36,
                                corner_radius=5,
                                values=['Date', 'Name', 'Date & JPG', 'Name & JPG', 'JPG'],
                                command=mode,)
option_menu.place(relx=0.32, rely=0.49, anchor=tkinter.CENTER)
# button to start the procces
button = ctk.CTkButton(master=frame,
                                    height=32,
                                    corner_radius=5,
                                    text='Sort',
                                    font=('sora', 20),
                                    command=select_mode,)
button.place(relx=0.1, rely=0.49, anchor=tkinter.CENTER)
# textbox whith exit message
status_textbox = ctk.CTkTextbox(master=frame,
                                        font=('sora', 16),
                                        width=825,
                                        height=180,
                                        bg_color='#242424',
                                        corner_radius=5)
status_textbox.place(relx=0.5, rely=0.78, anchor=tkinter.CENTER)
status_textbox.configure(state="disabled")

root.mainloop()
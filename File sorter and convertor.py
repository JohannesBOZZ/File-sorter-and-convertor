import time
import os
import shutil
import customtkinter as ctk
import tkinter
import re
from datetime import datetime
from PIL import Image
import asyncio

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

root = ctk.CTk()
root.geometry('900x500')
root.title("File sorter and convertor")
root.resizable(False,False)

# selects the function for the chosen mode in option_menu
def select_mode():
    mode = f'{option_menu_sort.get()} {option_menu_convert.get()}'
    os.makedirs(dst.get(), exist_ok=True)

    try:
        if '' not in [width_entry.get(), hight_entry.get() ]:
            scale = (int(width_entry.get()), int(hight_entry.get()))
        else:
            scale = None
            
        if mode == 'Date None' or mode == 'Name None' or mode == 'Date revers None' or mode == 'Name revers None':
            date_or_Name_sorter(src.get(), dst.get())
        elif mode == 'Date JPG' or mode == 'Name JPG' or mode == 'Date revers JPG' or mode == 'Name revers JPG':
            date_or_name_sorter_jpg(src.get(), dst.get(), int(jpg_quality.get()), scale)
        elif mode == 'None JPG':
            convert_to_jpg(src.get(), dst.get(), int(jpg_quality.get()), scale)
        elif mode == 'Date PNG' or mode == 'Name PNG' or mode == 'Date revers PNG' or mode == 'Name revers PNG':
            date_or_Name_sorter_png(src.get(), dst.get(), scale)
        elif mode == 'None PNG':
            convert_to_png(src.get(), dst.get(), scale)
        elif mode == 'Date WEBP' or mode == 'Name WEBP' or mode == 'Date revers WEBP' or mode == 'Name revers WEBP':
            date_or_Name_sorter_webp(src.get(), dst.get(), scale, int(jpg_quality.get()))
        elif mode == 'None WEBP':
            convert_to_webp(src.get(), dst.get(), scale, int(jpg_quality.get()))
        elif mode == 'None None':
            only_copy(src.get(), dst.get(), scale)



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
    mode = f'{option_menu_sort.get()} {option_menu_convert.get()}'

    # Create the destination folder if it doesn't exist
    count = len([name for name in os.listdir(destination_folder) if os.path.isfile(os.path.join(destination_folder, name))])
    sortet_image_count = 0
    # Sort files by modified date
    for root, _, files in os.walk(source_folder):
        # Sortiere die Dateien nach dem Änderungsdatum
        if mode == 'Date None':
            sorted_files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(root, x)))
        elif mode == 'Name None':
            sorted_files = sorted(files, key=natural_sort_key)
        elif mode == 'Date revers None':
            sorted_files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(root, x)), reverse=True)
        elif mode == 'Name revers None':
            sorted_files = sorted(files, key=natural_sort_key, reverse=True)
    # Copy the files to the destination folder and number them
        for i, file in enumerate(sorted_files, start=1):
            source_path = os.path.join(root, file)
            filename, file_extension = os.path.splitext(source_path)
            destination_path = os.path.join(destination_folder, f"{count}{file_extension}")
            count += 1
            sortet_image_count += 1
            progress_bar_def(sortet_image_count)


            # Kopiere die Datei als Original und als PNG
            shutil.copy2(source_path, destination_path)
    # ends counting time
    end_time = time.time()
    consol_message(end_time, start_time, sortet_image_count)
    # calculates the time taken



def date_or_name_sorter_jpg(source_folder, destination_folder, quality, scale):
    start_time = time.time()
    mode = f'{option_menu_sort.get()} {option_menu_convert.get()}'
    wb = chackbox_wb.get()

    # Create the destination folder if it doesn't exist
    count = len([name for name in os.listdir(destination_folder) if os.path.isfile(os.path.join(destination_folder, name))])
    convertet_image_count = 0
    # Sort files by modified date
    for root, _, files in os.walk(source_folder):
        # Sortiere die Dateien nach dem Änderungsdatum
        if mode == 'Date JPG':
            sorted_files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(root, x)))
        elif mode == 'Name JPG':
            sorted_files = sorted(files, key=natural_sort_key)
        elif mode == 'Date revers JPG':
            sorted_files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(root, x)), reverse=True)
        elif mode == 'Name revers JPG':
            sorted_files = sorted(files, key=natural_sort_key, reverse=True)

    # Copy the files to the destination folder and number them
        for i, file in enumerate(sorted_files, start=1):
            source_path = os.path.join(root, file)
            filename, file_extension = os.path.splitext(source_path)
            if file_extension.endswith((".png", ".jpg", ".jpeg", ".webp")):
                destination_path = os.path.join(destination_folder, f"{count}.jpg")

                # Checks whether checkbox wb is selected or not
                if wb:
                    img = Image.open(source_path).convert('L')
                else:
                    img = Image.open(source_path).convert("RGB")
                if scale is not None:
                    img.thumbnail(scale, Image.LANCZOS)
                img.save(destination_path, "JPEG", quality=quality)
            else:    
                destination_path = os.path.join(destination_folder, f"{count}{file_extension}")
                shutil.copy2(source_path, destination_path)

            count += 1
            convertet_image_count += 1
            progress_bar_def(convertet_image_count)
            


    end_time = time.time()
    # calculates the time taken
    consol_message(end_time, start_time, convertet_image_count)


def convert_to_jpg(input_folder, output_folder, quality, scale):
    start_time = time.time()
    convertet_image_count = 0
    wb = chackbox_wb.get()

    try:
        for filename in os.listdir(input_folder):
            if filename.endswith((".png", ".jpg", ".jpeg")):
                input_path = os.path.join(input_folder, filename)
                output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".jpg")
            # Checks whether checkbox wb is selected or not
                img=None
                if wb:
                    img = Image.open(input_path).convert('L')
                else:
                    img = Image.open(input_path).convert("RGB") 
                if scale is not None:
                    img.thumbnail(scale, Image.LANCZOS)                    
                img.save(output_path, "JPEG", quality=quality)
                convertet_image_count += 1
                progress_bar_def(convertet_image_count)


    except Exception as e:
        print(f"Fehler beim Konvertieren der Bilder: {str(e)}")
    
    end_time = time.time()
    # calculates the time taken
    consol_message(end_time, start_time, convertet_image_count)


def date_or_Name_sorter_png(source_folder, destination_folder, scale):
    start_time = time.time()
    mode = f'{option_menu_sort.get()} {option_menu_convert.get()}'
    wb = chackbox_wb.get()

    # Create the destination folder if it doesn't exist
    count = len([name for name in os.listdir(destination_folder) if os.path.isfile(os.path.join(destination_folder, name))])
    convertet_image_count = 0
    # Sort files by modified date
    for root, _, files in os.walk(source_folder):
        # Sortiere die Dateien nach dem Änderungsdatum
        if mode == 'Date PNG':
            sorted_files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(root, x)))
        elif mode == 'Name PNG':
            sorted_files = sorted(files, key=natural_sort_key)
        elif mode == 'Date revers PNG':
            sorted_files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(root, x)), reverse=True)
        elif mode == 'Name revers PNG':
            sorted_files = sorted(files, key=natural_sort_key, reverse=True)

    # Copy the files to the destination folder and number them
        for i, file in enumerate(sorted_files, start=1):
            source_path = os.path.join(root, file)
            filename, file_extension = os.path.splitext(source_path)
            if file_extension.endswith((".png", ".jpg", ".jpeg", ".webp")):
                # Checks whether checkbox wb is selected or not
                if wb:
                    img = Image.open(source_path).convert('L')
                else:
                    img = Image.open(source_path)
                if scale is not None:
                    img.thumbnail(scale, Image.LANCZOS)
                    if wb:
                        img = Image.convert('L')
                png_path = os.path.join(destination_folder, f"{count}.png")
                img.save(png_path, 'PNG')
            else:
                destination_path = os.path.join(destination_folder, f"{count}{file_extension}")
                shutil.copy2(source_path, destination_path)
            count += 1
            convertet_image_count += 1
            progress_bar_def(convertet_image_count)
    # ends counting time
    end_time = time.time()
    # calculates the time taken
    consol_message(end_time, start_time, convertet_image_count)


def convert_to_png(input_folder, output_folder, scale):
    start_time = time.time()
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']  # Unterstützte Bildformate
    wb = chackbox_wb.get()
    convertet_image_count = 0

    for filename in os.listdir(input_folder):
            if filename.endswith((".png", ".jpg", ".jpeg", ".webp")):
                input_path = os.path.join(input_folder, filename)
                output_path = os.path.join(output_folder, f'{filename}.png')
                img=None
                # Versuche, das Bild zu öffnen und in PNG zu konvertieren
                if wb:
                    img = Image.open(input_path).convert('L')
                else:
                    img = Image.open(input_path)
                if scale is not None:
                    img.thumbnail(scale, Image.LANCZOS)
                img.save(output_path, 'PNG')
                convertet_image_count += 1
                progress_bar_def(convertet_image_count)

    end_time = time.time()
    # calculates the time taken
    consol_message(end_time, start_time, convertet_image_count)


def date_or_Name_sorter_webp(source_folder, destination_folder, scale, quality):
    start_time = time.time()
    mode = f'{option_menu_sort.get()} {option_menu_convert.get()}'
    wb = chackbox_wb.get()

    # Create the destination folder if it doesn't exist
    count = len([name for name in os.listdir(destination_folder) if os.path.isfile(os.path.join(destination_folder, name))])
    convertet_image_count = 0
    # Sort files by modified date
    for root, _, files in os.walk(source_folder):
        # Sortiere die Dateien nach dem Änderungsdatum
        if mode == 'Date PNG':
            sorted_files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(root, x)))
        elif mode == 'Name PNG':
            sorted_files = sorted(files, key=natural_sort_key)
        elif mode == 'Date revers PNG':
            sorted_files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(root, x)), reverse=True)
        elif mode == 'Name revers PNG':
            sorted_files = sorted(files, key=natural_sort_key, reverse=True)

    # Copy the files to the destination folder and number them
        for i, file in enumerate(sorted_files, start=1):
            source_path = os.path.join(root, file)
            filename, file_extension = os.path.splitext(source_path)
            if file_extension.endswith((".png", ".jpg", ".jpeg", ".webp")):
                # Checks whether checkbox wb is selected or not
                if wb:
                    img = Image.open(source_path).convert('L')
                else:
                    img = Image.open(source_path)
                if scale is not None:
                    img.thumbnail(scale, Image.LANCZOS)
                    if wb:
                        img = Image.convert('L')
                file_path = os.path.join(destination_folder, f"{count}.webp")
                img.save(file_path, 'WEBP', optimize = True, quality = quality)
            else:
                destination_path = os.path.join(destination_folder, f"{count}{file_extension}")
                shutil.copy2(source_path, destination_path)
            count += 1
            convertet_image_count += 1
            progress_bar_def(convertet_image_count)
    # ends counting time
    end_time = time.time()
    # calculates the time taken
    consol_message(end_time, start_time, convertet_image_count)


def convert_to_webp(input_folder, output_folder, scale, quality):
    start_time = time.time()
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']  # Unterstützte Bildformate
    wb = chackbox_wb.get()
    convertet_image_count = 0

    for filename in os.listdir(input_folder):
            if filename.endswith((".png", ".jpg", ".jpeg", ".webp")):
                input_path = os.path.join(input_folder, filename)
                filename, fileExtension = os.path.splitext(filename)
                output_path = os.path.join(output_folder, f'{filename}.webp')
                img=None
                # Versuche, das Bild zu öffnen und in PNG zu konvertieren
                if wb:
                    img = Image.open(input_path).convert('L')
                else:
                    img = Image.open(input_path)
                if scale is not None:
                    img.thumbnail(scale, Image.LANCZOS)
                img.save(output_path, 'WEBP', optimize = True, quality = quality)
                convertet_image_count += 1
                progress_bar_def(convertet_image_count)

    end_time = time.time()
    # calculates the time taken
    consol_message(end_time, start_time, convertet_image_count)


def only_copy(source_folder, destination_folder):
    start_time = time.time()
    copy_count = 0
    count = 0
    # Sort files by modified date
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            source_path = os.path.join(root, file)
            destination_path = os.path.join(destination_folder, os.path.relpath(source_path, source_folder))
            destination_path = r'\\?\{}'.format(os.path.abspath(destination_path))
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            shutil.copy2(source_path, destination_path)
            count += 1
            copy_count += 1
            progress_bar_def(copy_count)


            # Kopiere die Datei als Original und als PNG
    # ends counting time
    end_time = time.time()
    consol_message(end_time, start_time, copy_count)

def natural_sort_key(s):
    # A helper function to provide a natural sorting key for filenames.
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r'(\d+)', s)]


# selects the mode for option_menu 
def mode(self):
    mode = f'{option_menu_sort.get()} {option_menu_convert.get()}'
    # shows jpg_quality and chackbox_wb
    if 'JPG' in mode or 'WEBP' in mode and 'PNG' not in mode:
        jpg_quality.place(relx=0.64, rely=0.49, anchor=tkinter.CENTER)
        chackbox_wb.place(relx=0.86, rely=0.49, anchor=tkinter.CENTER)
    # shows chackbox_wb and hidersjpg_quality
    elif 'PNG' in mode:
        chackbox_wb.place(relx=0.65, rely=0.49, anchor=tkinter.CENTER)
        jpg_quality.place_forget()
    # hides jpg_quality and chackbox_wb
    elif option_menu_convert.get() == 'None':
        chackbox_wb.place_forget()
        jpg_quality.place_forget()
    
    if 'None' in option_menu_convert.get():
        width_entry.place_forget()
        hight_entry.place_forget()
        src.configure(width=820)
        dst.configure(width=820)
    else:
        width_entry.place(relx=0.98, rely=0.2, anchor=tkinter.E)
        hight_entry.place(relx=0.98, rely=0.35, anchor=tkinter.E)
        src.configure(width=700)
        dst.configure(width=700)


def consol_message(end_time, start_time, convertet_image_count):
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
    status_textbox.insert("0.0",f'[{str(now.strftime("%Y/%m/%d, %H:%M:%S"))}] Procces was sucessfully, {convertet_image_count} files{process_time}\n')
    status_textbox.configure(state="disabled")
global Value
Value = 0

def progress_bar_def(value):
    end = 0
    qualle = src.get()
    for root, dirs, files in os.walk(qualle):
        end += len(files)
    Value = value / end
    # Nach 1 Sekunde erneut aufrufen
    progress_bar_text.configure(text=f'{round(Value * 100)}% | {value} of {end}')
    progress_bar_text.update()
    progress_bar.set(Value)
    progress_bar.update()



frame = ctk.CTkFrame(master=root, fg_color='transparent')
frame.pack(pady=16, padx=24, fill='both', expand=True)

label = ctk.CTkLabel(master=frame,
                               text='File sorter and convertor',
                               font=("sora", 32))
label.place(relx=0.5, rely=0.05, anchor=tkinter.CENTER)
# source entry
src = ctk.CTkEntry(master=frame,
                            placeholder_text='Input folder',
                            font=("sora", 20),
                            width=700,
                            height=32,
                            corner_radius=5)
src.place(relx=0.02, rely=0.2, anchor=tkinter.W)
# destination entry
dst = ctk.CTkEntry(master=frame,
                            placeholder_text='Output folder',
                            font=("sora", 20),
                            width=700,
                            height=32,
                            corner_radius=5)
dst.place(relx=0.02, rely=0.35, anchor=tkinter.W)
# width entry
width_entry = ctk.CTkEntry(master=frame,
                            placeholder_text='width',
                            font=("sora", 20),
                            width=100,
                            height=32,
                            corner_radius=5)
width_entry.place(relx=0.98, rely=0.2, anchor=tkinter.E)
# hight entry
hight_entry = ctk.CTkEntry(master=frame,
                            placeholder_text='hight',
                            font=("sora", 20),
                            width=100,
                            height=32,
                            corner_radius=5)
hight_entry.place(relx=0.98, rely=0.35, anchor=tkinter.E)
# entry for quality by jpg
jpg_quality = ctk.CTkEntry(master=frame,
                            placeholder_text='JPG Quality',
                            font=("sora", 20),
                            width=150,
                            height=32,
                            corner_radius=5)

# menu for changing the sort mode
option_menu_sort = ctk.CTkOptionMenu(master=frame,
                                font=('sora', 20),
                                width=180,
                                height=36,
                                corner_radius=5,
                                values=['Date', 'Name', 'Date revers', 'Name revers', 'None'],
                                command=mode,)
option_menu_sort.place(relx=0.263, rely=0.49, anchor=tkinter.CENTER)
# menu for changing the convert mode
option_menu_convert = ctk.CTkOptionMenu(master=frame,
                                font=('sora', 20),
                                width=100,
                                height=36,
                                corner_radius=5,
                                values=['PNG', 'JPG','WEBP' , 'None'],
                                command=mode,)
option_menu_convert.place(relx=0.452, rely=0.49, anchor=tkinter.CENTER)
# if you wont AI generated images
chackbox_wb = ctk.CTkCheckBox(master=frame, 
                                font=('sora', 20),
                                text='White & Black',
                                height=32,
                                corner_radius=5)
chackbox_wb.place(relx=0.65, rely=0.49, anchor=tkinter.CENTER)

# button to start the procces
button = ctk.CTkButton(master=frame,
                                    height=32,
                                    corner_radius=5,
                                    width=100,
                                    text='Sort',
                                    font=('sora', 20),
                                    command=select_mode,)
button.place(relx=0.076, rely=0.49, anchor=tkinter.CENTER)
# textbox whith exit message
status_textbox = ctk.CTkTextbox(master=frame,
                                        font=('sora', 16),
                                        width=825,
                                        height=170,
                                        bg_color='#242424',
                                        corner_radius=5)
status_textbox.place(relx=0.5, rely=0.76, anchor=tkinter.CENTER)
status_textbox.configure(state="disabled")

progress_bar = ctk.CTkProgressBar(master=frame,
                                width=700,
                                mode='determinate',)
progress_bar.place(relx=0.4275, rely=0.99, anchor=tkinter.CENTER)
progress_bar.set(0)

progress_bar_text = ctk.CTkLabel(master=frame,
                                text='0%',
                                bg_color='transparent')
progress_bar_text.place(relx=0.855, rely=0.99, anchor=tkinter.W)

root.mainloop()
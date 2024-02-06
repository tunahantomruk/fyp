import tkinter as tk
from importlib.machinery import SourceFileLoader
from tkinter import messagebox
from PIL import Image, ImageTk
import os

#exception hatasına bak

def run_exercise(file_path):
    try:
        exercise_module = SourceFileLoader("exercise", file_path).load_module()
        exercise_module.run()
    except Exception as e:
        pass
        #tk.messagebox.showerror("Error", f"Error running exercise: {e}")

def show_exercise_info(exercise_number):
    info_window = tk.Toplevel(exercise_menu)
    info_window.title(f"Exercise {exercise_number} Info")
    info_window.geometry("600x600")

    info_text = f"This is the information for Exercise {exercise_number}."

    info_text_widget = tk.Label(info_window, text=info_text, wraplength=500)
    info_text_widget.pack(pady=20)

    image_folder = "expics"
    image_path = os.path.join(image_folder, f"expic{exercise_number}.png")

    try:
        image = Image.open(image_path)
        image = image.resize((500, 500), Image.ANTIALIAS)
        tk_image = ImageTk.PhotoImage(image)

        image_widget = tk.Label(info_window, image=tk_image)
        image_widget.image = tk_image
        image_widget.pack(pady=20)
    except Exception as e:
        tk.messagebox.showerror("Error", f"Error loading image: {e}")

    start_button = tk.Button(info_window, text="Start Exercise", command=lambda num=exercise_number: run_exercise(f"exercise{num}.py"))
    start_button.pack(pady=10)

    back_to_menu_button = tk.Button(info_window, text="Back to Exercise Menu", command=info_window.destroy)
    back_to_menu_button.pack(pady=10)

def go_to_exercise_menu():
    main_menu.iconify()
    exercise_menu.deiconify()

def go_to_main_menu():
    exercise_menu.iconify()
    main_menu.deiconify()

def show_about():
    about_text = "Neck Exercise App Done by Meriç Tunahan Tomruk"

    about_window = tk.Toplevel(main_menu)
    about_window.title("About")
    about_window.geometry("400x400")

    about_text_widget = tk.Text(about_window, wrap=tk.WORD, height=10, width=60)
    about_text_widget.insert(tk.END, about_text)
    about_text_widget.config(state=tk.DISABLED)
    about_text_widget.pack(padx=20, pady=20)

    # Add a "Back" button to close the about window and return to the main menu
    back_button = tk.Button(about_window, text="Back to Main Menu", command=about_window.destroy)
    back_button.pack(pady=10)

main_menu = tk.Tk()
main_menu.title("Main Menu")
main_menu.geometry("800x600")

# Set the background image for the main menu window
background_image_path_main_menu = os.path.join("windowsPics", "main2.png")
image_main_menu = Image.open(background_image_path_main_menu)
image_main_menu = image_main_menu.resize((800, 600), Image.ANTIALIAS)
tk_image_main_menu = ImageTk.PhotoImage(image_main_menu)

background_label_main_menu = tk.Label(main_menu, image=tk_image_main_menu)
background_label_main_menu.image = tk_image_main_menu
background_label_main_menu.place(relwidth=1, relheight=1)

button_style = {'padx': 20, 'pady': 20, 'font': ('Helvetica', 14)}

button_style2 = {'padx': 20, 'pady': 20, 'font': ('Helvetica', 10)}

about_button = tk.Button(main_menu, text="About", command=show_about, **button_style, bg="#FFD700", fg="black")
about_button.pack(pady=20)

exercise_menu_button = tk.Button(main_menu, text="Exercise Menu", command=go_to_exercise_menu, **button_style, bg="#4CAF50", fg="white")
exercise_menu_button.pack(pady=20)

quit_button = tk.Button(main_menu, text="Quit", command=main_menu.quit, **button_style, bg="#FF0000", fg="white")
quit_button.pack(pady=20)

exercise_menu = tk.Toplevel(main_menu)
exercise_menu.title("Exercise Menu")
exercise_menu.geometry("750x500")

# Set the background image for the exercise menu window
background_image_path_exercise_menu = os.path.join("windowsPics", "illust.png")
image_exercise_menu = Image.open(background_image_path_exercise_menu)
image_exercise_menu = image_exercise_menu.resize((750, 500), Image.ANTIALIAS)
tk_image_exercise_menu = ImageTk.PhotoImage(image_exercise_menu)

background_label_exercise_menu = tk.Label(exercise_menu, image=tk_image_exercise_menu)
background_label_exercise_menu.image = tk_image_exercise_menu
background_label_exercise_menu.place(relwidth=1, relheight=1)

def create_exercise_window(exercise_number):
    exercise_window = tk.Toplevel(exercise_menu)
    exercise_window.title(f"Exercise {exercise_number}")
    exercise_window.geometry("600x500")

    start_button = tk.Button(exercise_window, text="Start Exercise", command=lambda num=exercise_number: run_exercise(f"exercise{num}Final.py"),**button_style, bg="#4CAF50", fg="white")
    start_button.pack(pady=20)

    info_button = tk.Button(exercise_window, text="Exercise Information", command=lambda num=exercise_number: show_exercise_info(num), **button_style, bg="#FFD700", fg="white")
    info_button.pack(pady=20)

    back_to_menu_button = tk.Button(exercise_window, text="Back to Exercise Menu", command=exercise_window.destroy,**button_style, bg="#FF0000", fg="white")
    back_to_menu_button.pack(pady=20)

for exercise_number in range(1, 9):
    row = (exercise_number - 1) // 4
    col = (exercise_number - 1) % 4

    exercise_button = tk.Button(exercise_menu, text=f"Exercise {exercise_number}", command=lambda num=exercise_number: create_exercise_window(num), **button_style, bg="#007CBA", fg="white")
    exercise_button.grid(row=row, column=col, padx=20, pady=20)

total_rows = (8 - 1) // 4 + 1

back_to_menu_button = tk.Button(exercise_menu, text="Back to Main Menu", command=go_to_main_menu, **button_style, bg="red", fg="black")
back_to_menu_button.grid(row=total_rows, column=0, columnspan=4, pady=20)

exercise_menu.withdraw()
main_menu.mainloop()

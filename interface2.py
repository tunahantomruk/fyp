import tkinter as tk
from importlib.machinery import SourceFileLoader
from tkinter import messagebox

# Function to run an exercise file
def run_exercise(file_path):
    try:
        exercise_module = SourceFileLoader("exercise", file_path).load_module()
        exercise_module.run()
    except Exception as e:
        tk.messagebox.showerror("Error", f"Error running exercise: {e}")

def show_exercise_info(exercise_number):
    info_text = f"This is the information for Exercise {exercise_number}.\nEdit this text later."

    info_window = tk.Toplevel(exercise_menu)
    info_window.title(f"Exercise {exercise_number} Info")
    info_window.geometry("400x400")

    info_text_widget = tk.Text(info_window, wrap=tk.WORD, height=10, width=60)
    info_text_widget.insert(tk.END, info_text)
    info_text_widget.config(state=tk.DISABLED)
    info_text_widget.pack(padx=20, pady=20)

    back_button = tk.Button(info_window, text="Back to Exercise Menu", command=info_window.destroy)
    back_button.pack(pady=10)

# Function to show about information
def show_about():
    about_text = "Neck Exercise App Done by Meriç Tunahan Tomruk"

    # Create a new window for the about text
    about_window = tk.Toplevel(main_menu)
    about_window.title("About")
    about_window.geometry("400x400")

    # Add a Text widget to display the about text
    about_text_widget = tk.Text(about_window, wrap=tk.WORD, height=10, width=60)
    about_text_widget.insert(tk.END, about_text)
    about_text_widget.config(state=tk.DISABLED)  # Make the Text widget read-only
    about_text_widget.pack(padx=20, pady=20)

    # Add a "Back" button to close the about window and return to the main menu
    back_button = tk.Button(about_window, text="Back to Main Menu", command=about_window.destroy)
    back_button.pack(pady=10)

def show_exercise_menu():
    exercise_menu.deiconify()

def create_exercise_window(exercise_number):
    exercise_window = tk.Toplevel(exercise_menu)
    exercise_window.title(f"Exercise {exercise_number}")
    exercise_window.geometry("400x300")

    start_button = tk.Button(exercise_window, text="Start Exercise", command=lambda: run_exercise(f"exercise{exercise_number}.py"))
    start_button.pack(pady=20)

    info_button = tk.Button(exercise_window, text="Exercise Information", command=lambda: show_exercise_info(exercise_number))
    info_button.pack(pady=20)

    back_to_menu_button = tk.Button(exercise_window, text="Back to Exercise Menu", command=exercise_window.destroy)
    back_to_menu_button.pack(pady=20)

# Create the main window (main menu)
main_menu = tk.Tk()
main_menu.title("Main Menu")
main_menu.geometry("800x600")

# Customize button appearance
button_style = {'padx': 20, 'pady': 20, 'font': ('Helvetica', 14)}

# Function to go to exercise menu
def go_to_exercise_menu():
    main_menu.iconify()
    exercise_menu.deiconify()

# Create buttons for the main menu
about_button = tk.Button(main_menu, text="About", command=show_about, **button_style, bg="#FFD700", fg="black")
about_button.pack(pady=20)

exercise_menu_button = tk.Button(main_menu, text="Exercise Menu", command=go_to_exercise_menu, **button_style, bg="#4CAF50", fg="white")
exercise_menu_button.pack(pady=20)

quit_button = tk.Button(main_menu, text="Quit", command=main_menu.quit, **button_style, bg="#FF0000", fg="white")
quit_button.pack(pady=20)

# Create Exercise Menu
exercise_menu = tk.Toplevel(main_menu)
exercise_menu.title("Exercise Menu")
exercise_menu.geometry("750x500")

# Function to go back to main menu
def go_to_main_menu():
    exercise_menu.iconify()
    main_menu.deiconify()

# Create buttons for exercises in the exercise menu (arranged in four columns)
for exercise_number in range(1, 9):
    row = (exercise_number - 1) // 4
    col = (exercise_number - 1) % 4

    exercise_button = tk.Button(exercise_menu, text=f"Exercise {exercise_number}", command=lambda num=exercise_number: create_exercise_window(num), **button_style, bg="#007CBA", fg="white")
    exercise_button.grid(row=row, column=col, padx=20, pady=20)

# Calculate the total number of rows needed for the exercise buttons
total_rows = (8 - 1) // 4 + 1

# Create back to menu button in the exercise menu
back_to_menu_button = tk.Button(exercise_menu, text="Back to Main Menu", command=go_to_main_menu, **button_style, bg="#FFD700", fg="black")
back_to_menu_button.grid(row=total_rows, column=0, columnspan=4, pady=20)

# Hide the exercise menu initially
exercise_menu.withdraw()

# Start the main loop for the main menu
main_menu.mainloop()

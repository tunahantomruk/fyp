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

def run_left_right():
    run_exercise("exercise5.py")  

def run_neck_stretch():
    run_exercise("exercise6.py")  

def run_head_tilt():
    run_exercise("exercise7.py")

def run_head_circle():
    run_exercise("exercise8.py")



def show_about():
    about_text = "This is the about section.\nEdit this text later."

    # Create a new window for the about text
    about_window = tk.Toplevel(window)
    about_window.title("About")
    about_window.geometry("800x800")

    # Add a Text widget to display the about text
    about_text_widget = tk.Text(about_window, wrap=tk.WORD, height=10, width=60)
    about_text_widget.insert(tk.END, about_text)
    about_text_widget.config(state=tk.DISABLED)  # Make the Text widget read-only
    about_text_widget.pack(padx=20, pady=20)

    # Add a "Back" button to close the about window and return to the main menu
    back_button = tk.Button(about_window, text="Back to Main Menu", command=about_window.destroy)
    back_button.pack(pady=10)

# Create the main window
window = tk.Tk()
window.title("Exercise Menu")
window.geometry("800x800")

# Customize button appearance
button_style = {'padx': 20, 'pady': 20, 'font': ('Helvetica', 14)}

# Create buttons for exercises in the main window
left_right_button = tk.Button(window, text="Left-Right (ex. 5)", command=run_left_right, **button_style, bg="#4CAF50", fg="white")
left_right_button.pack(pady=20)

neck_stretch_button = tk.Button(window, text="Neck Stretch (ex. 6)", command=run_neck_stretch, **button_style, bg="#007CBA", fg="white")
neck_stretch_button.pack(pady=20)

head_tilt_button = tk.Button(window, text="Head Tilt (ex. 7)", command=run_head_tilt, **button_style, bg="#008CCA", fg="white")
head_tilt_button.pack(pady=20)

head_circle_button = tk.Button(window, text="Head Circle (ex. 8)", command=run_head_circle, **button_style, bg="#008CBA", fg="white")
head_circle_button.pack(pady=20)

# Create an "About" button in the main window
about_button = tk.Button(window, text="About", command=show_about, **button_style, bg="#FFD700", fg="black")
about_button.pack(pady=20)

# Start the main loop
window.mainloop()

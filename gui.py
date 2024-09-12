import tkinter as tk
import subprocess

def run_script():
    # Update the path to the actual path of your Python script
    subprocess.run(['python3', './match_teachers_students.py'])  # Use the correct path here

app = tk.Tk()
app.title("Run Script")
button = tk.Button(app, text="Run Script", command=run_script)
button.pack(pady=20, padx=20)
app.mainloop()

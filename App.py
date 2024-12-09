import tkinter as tk
import mysql.connector
from tkinter import messagebox
from tkinter import ttk
from dotenv import load_dotenv
import os

load_dotenv()

# Connection to MySQL database
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host = os.getenv("DB_HOST"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            database = os.getenv("DB_NAME")
        )
        return connection
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error connecting to database: {err}")
        return None

# Function to authenticate user login
def authenticate_user():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Login Error", "Both fields are required.")
        return

    connection = connect_to_database()
    if not connection:
        return

    cursor = connection.cursor()
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    connection.close()

    if result:
        messagebox.showinfo("Login Success", "Welcome to the Fitness System!")
        login_window.destroy()
        show_main_system()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Function to register a new user
def register_user():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Registration Error", "Both fields are required.")
        return

    connection = connect_to_database()
    if not connection:
        return

    cursor = connection.cursor()
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    try:
        cursor.execute(query, (username, password))
        connection.commit()
        messagebox.showinfo("Registration Success", "User registered successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Registration Error", f"Error: {err}")
    finally:
        connection.close()

# Function to display the main fitness system
def show_main_system():
    # Functionality of the fitness system
    def calculate_bmi(weight, height):
        return round(weight / (height ** 2), 2)

    def generate_fitness_plan():
        try:
            age = int(age_entry.get())
            weight = float(weight_entry.get())
            height = float(height_entry.get()) / 100
            goal = goal_combobox.get()

            if age <= 0 or weight <= 0 or height <= 0:
                raise ValueError("Age, weight, and height must be positive numbers.")

            if goal not in ["Weight Loss", "Muscle Gain", "Maintain Fitness"]:
                raise ValueError("Please select a valid fitness goal.")

            bmi = calculate_bmi(weight, height)
            bmi_category = ""
            if bmi < 18.5:
                bmi_category = "Underweight"
            elif 18.5 <= bmi < 24.9:
                bmi_category = "Normal weight"
            elif 25 <= bmi < 29.9:
                bmi_category = "Overweight"
            else:
                bmi_category = "Obesity"

            plan = []
            if goal == "Weight Loss":
                plan = ["30 mins Cardio", "15 mins Strength Training", "Low-calorie Diet"]
            elif goal == "Muscle Gain":
                plan = ["45 mins Weight Training", "20 mins Cardio", "High-protein Diet"]
            elif goal == "Maintain Fitness":
                plan = ["30 mins Mixed Cardio and Strength", "Balanced Diet"]

            if age > 50:
                plan.append("Include Low-impact Exercises")
            if weight > 80:
                plan.append("Focus on Portion Control")

            plan.insert(0, f"Your BMI: {bmi} ({bmi_category})")
            result_text.set("\n".join(plan))
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def reset_form():
        age_entry.delete(0, tk.END)
        weight_entry.delete(0, tk.END)
        height_entry.delete(0, tk.END)
        goal_combobox.set("")
        result_text.set("")

    def save_plan():
        plan = result_text.get()
        if not plan:
            messagebox.showerror("Save Error", "No plan to save!")
            return
        with open("fitness_plan.txt", "w") as file:
            file.write(plan)
        messagebox.showinfo("Save Success", "Fitness plan saved successfully!")

    # Main system window
    root = tk.Tk()
    root.title("AI-Driven Fitness System")
    root.geometry("450x600")

    # UI elements
    title_label = tk.Label(root, text="Personalized Fitness Plan", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=10)

    age_label = tk.Label(root, text="Enter Age:")
    age_label.pack()
    age_entry = tk.Entry(root)
    age_entry.pack(pady=5)

    weight_label = tk.Label(root, text="Enter Weight (kg):")
    weight_label.pack()
    weight_entry = tk.Entry(root)
    weight_entry.pack(pady=5)

    height_label = tk.Label(root, text="Enter Height (cm):")
    height_label.pack()
    height_entry = tk.Entry(root)
    height_entry.pack(pady=5)

    goal_label = tk.Label(root, text="Select Fitness Goal:")
    goal_label.pack()
    goal_combobox = ttk.Combobox(root, values=["Weight Loss", "Muscle Gain", "Maintain Fitness"])
    goal_combobox.pack(pady=5)

    generate_button = tk.Button(root, text="Generate Plan", command=generate_fitness_plan, bg="green", fg="white")
    generate_button.pack(pady=10)

    result_label = tk.Label(root, text="Your Fitness Plan:", font=("Helvetica", 12))
    result_label.pack(pady=10)
    result_text = tk.StringVar()
    result_display = tk.Label(root, textvariable=result_text, font=("Helvetica", 10), justify="left", wraplength=400)
    result_display.pack(pady=5)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    reset_button = tk.Button(button_frame, text="Reset", command=reset_form, bg="orange", fg="white")
    reset_button.grid(row=0, column=0, padx=10)

    save_button = tk.Button(button_frame, text="Save Plan", command=save_plan, bg="blue", fg="white")
    save_button.grid(row=0, column=1, padx=10)

    root.mainloop()

# Login/Register window
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("300x200")

username_label = tk.Label(login_window, text="Username:")
username_label.pack()
username_entry = tk.Entry(login_window)
username_entry.pack(pady=5)

password_label = tk.Label(login_window, text="Password:")
password_label.pack()
password_entry = tk.Entry(login_window, show="*")
password_entry.pack(pady=5)

login_button = tk.Button(login_window, text="Login", command=authenticate_user, bg="green", fg="white")
login_button.pack(pady=5)

register_button = tk.Button(login_window, text="Register", command=register_user, bg="blue", fg="white")
register_button.pack(pady=5)

login_window.mainloop()
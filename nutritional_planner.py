# Final Group Project - Nutritional Planning/Tracking App
# Authors: Fahed Alkhiami, Andrew Rabadi, Arianna Tarki
# Date Due: 08/06/2024
# 
# Description: This program will open a window that will prompt the user to enter their personal information, including
# weight, height, exercise level, dietary restriction/preferences, and name. If user already exists, then they can select
# their preexisting profile. Using the given information, the program will determine whether user should gain, lose, or
# maintain their current body weight. Will display graphical representation of BMI placement, produce a suggested menu
# of healthy foods, and generate a QR code for the user to save information to their phone for easier access. 

#--------------------------------------- Imports ---------------------------------------

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import qrcode
import os
import sqlite3
import requests
import random
import datetime

#--------------------------------------- Functions ---------------------------------------

# Function to calculate BMI
def calculate_bmi(weight, height):

    height_meters = (height[0] * 12 + height[1]) * 0.0254                   # Convert height to meters
    return weight * 0.453592 / (height_meters ** 2)                         # Return calculated BMI using BMI formula

# Function to generate a nutritional plan based on BMI and goals
def get_nutritional_plan(bmi, goals, activity_level, dietary_preferences, allergies):

    plan = ""
    if bmi < 18.5:                                                  # Depending on BMI, assign specific plan
        plan = "Gain weight plan"                                   # If too low, suggest gaining weight
    elif 18.5 <= bmi < 24.9:                                        # If at expected level then maintain weight
        plan = "Maintain weight plan"                               # Otherwise suggest to lose weight
    else:
        plan = "Lose weight plan"
    
    plan += f"\nActivity Level: {activity_level}"                   # Add activity level
    plan += f"\nDietary Preferences: {dietary_preferences}"         # Add any preferences
    plan += f"\nAllergies: {allergies}"                             # Add any allergies
    return plan                                                     # Return nutritional plan (string)

# Function to generate a QR code
def generate_qr_code(data):
    
    qr = qrcode.make(data)                   # Take in data (nutritional plan) and convert to QR
    qr_path = "qr_code.png"                  # Set path to QR code image
    qr.save(qr_path)                         # Save the data to the path
    return qr_path                           # Return QR code path to image => data

# Function to create a table of food options
def create_food_options_table():

    categories = {

        "Breakfast": [
            "Whole grain cereal", "Egg whites", "Fruit juice", "Greek yogurt", "Oatmeal", "Avocado toast", "Smoothie with greens", 
            "Whole grain pancakes", "Almond butter on toast", "Chia seeds pudding", "Mixed berries", "Scrambled eggs with veggies", 
            "Protein shake", "Nut and seed granola", "Quinoa porridge", "Fruit salad", "Cottage cheese", "Breakfast burrito", 
            "Sweet potato hash", "Protein-rich smoothie"
        ],

        "Lunch": [
            "Grilled chicken salad", "Quinoa and black beans", "Turkey and avocado wrap", "Chicken and vegetable stir-fry", 
            "Salmon with quinoa", "Lean beef with veggies", "Chickpea and spinach stew", "Grilled tofu and vegetables", 
            "Greek salad with chicken", "Whole grain pasta with marinara", "Vegetable and lentil soup", "Chicken and sweet potato salad", 
            "Tofu and veggie kebabs", "Turkey chili", "Stuffed bell peppers", "Chicken and quinoa bowl", "Vegetable curry", 
            "Grilled shrimp with brown rice", "Salmon and spinach salad", "Chicken and avocado salad"
        ],

        "Dinner": [
            "Grilled salmon with vegetables", "Chicken breast with steamed broccoli", "Turkey meatballs with zucchini noodles", 
            "Stuffed bell peppers with quinoa", "Baked cod with asparagus", "Vegetable stir-fry with tofu", "Beef and vegetable kebabs", 
            "Lentil soup with spinach", "Chicken curry with brown rice", "Grilled chicken with sweet potato mash", 
            "Vegetarian chili", "Grilled shrimp with mixed vegetables", "Baked chicken thighs with Brussels sprouts", 
            "Spaghetti squash with marinara sauce", "Stuffed mushrooms with spinach", "Salmon and kale salad", 
            "Chicken and vegetable soup", "Baked tofu with broccoli", "Beef stew with carrots", "Grilled portobello mushrooms"
        ],

        "Snacks": [
            "Almonds and walnuts", "Greek yogurt with honey", "Apple slices with almond butter", "Carrot sticks with hummus", 
            "Mixed berries", "Protein bar", "Edamame", "Celery with peanut butter", "Cottage cheese with pineapple", 
            "Homemade trail mix", "Protein shake", "Vegetable sticks with guacamole", "Apple with cheese slices", 
            "Rice cakes with avocado", "Chia pudding", "Pumpkin seeds", "Baked sweet potato fries", "Smoothie with protein powder", 
            "Hard-boiled eggs", "Low-fat cheese sticks"
        ]
    }

    fig, ax = plt.subplots(figsize=(12, 10))            # Initialize figure size dimensions

    positions = {                                       # Place each category of food in designated spots
        "Breakfast": (0.05, 0.55, 0.4, 0.4),
        "Lunch": (0.55, 0.55, 0.4, 0.4),
        "Dinner": (0.05, 0.05, 0.4, 0.4),
        "Snacks": (0.55, 0.05, 0.4, 0.4)
    }

    colors = {                                          # Set color of each menu
        "Breakfast": '#e9153f',
        "Lunch": '#32cd32',
        "Dinner": '#30b3f5',
        "Snacks": '#d1b300'
    }

    # Function to draw a menu including labels and names of food items
    def draw_section(ax, position, title, items, color):       

        x, y, width, height = position
        ax.add_patch(patches.Rectangle((x, y), width, height, color=color, ec='black', lw=1))
        ax.text(x + width / 2, y + height - 0.03, title, ha='center', va='top', fontsize=14, fontweight='bold')
        for i, item in enumerate(items):
            ax.text(x + 0.02, y + height - 0.06 - 0.015 * i, f"• {item}", ha='left', va='top', fontsize=9, wrap=True)

    for category, items in categories.items():
        draw_section(ax, positions[category], category, items, colors[category])    # Draw each menu for each category

    ax.axis('off')

    plt.suptitle('Meal Plan Options', fontsize=18, fontweight='bold', y=0.95)       # Set title

    food_table_path = 'food_options_table.png'                                      # Set name to image
    plt.savefig(food_table_path)                                                    # Save configuration to image name
    plt.close()                                                                     # Close
    
    return food_table_path                                                          # Return path

# Function to return a random selection of meals in each category
def get_food_menu():

    categories = {

        "Breakfast": [
            "Whole grain cereal", "Egg whites", "Fruit juice", "Greek yogurt", "Oatmeal", "Avocado toast", "Smoothie with greens", 
            "Whole grain pancakes", "Almond butter on toast", "Chia seeds pudding", "Mixed berries", "Scrambled eggs with veggies", 
            "Protein shake", "Nut and seed granola", "Quinoa porridge", "Fruit salad", "Cottage cheese", "Breakfast burrito", 
            "Sweet potato hash", "Protein-rich smoothie"
        ],

        "Lunch": [
            "Grilled chicken salad", "Quinoa and black beans", "Turkey and avocado wrap", "Chicken and vegetable stir-fry", 
            "Salmon with quinoa", "Lean beef with veggies", "Chickpea and spinach stew", "Grilled tofu and vegetables", 
            "Greek salad with chicken", "Whole grain pasta with marinara", "Vegetable and lentil soup", "Chicken and sweet potato salad", 
            "Tofu and veggie kebabs", "Turkey chili", "Stuffed bell peppers", "Chicken and quinoa bowl", "Vegetable curry", 
            "Grilled shrimp with brown rice", "Salmon and spinach salad", "Chicken and avocado salad"
        ],

        "Dinner": [
            "Grilled salmon with vegetables", "Chicken breast with steamed broccoli", "Turkey meatballs with zucchini noodles", 
            "Stuffed bell peppers with quinoa", "Baked cod with asparagus", "Vegetable stir-fry with tofu", "Beef and vegetable kebabs", 
            "Lentil soup with spinach", "Chicken curry with brown rice", "Grilled chicken with sweet potato mash", 
            "Vegetarian chili", "Grilled shrimp with mixed vegetables", "Baked chicken thighs with Brussels sprouts", 
            "Spaghetti squash with marinara sauce", "Stuffed mushrooms with spinach", "Salmon and kale salad", 
            "Chicken and vegetable soup", "Baked tofu with broccoli", "Beef stew with carrots", "Grilled portobello mushrooms"
        ],

        "Snacks": [
            "Almonds and walnuts", "Greek yogurt with honey", "Apple slices with almond butter", "Carrot sticks with hummus", 
            "Mixed berries", "Protein bar", "Edamame", "Celery with peanut butter", "Cottage cheese with pineapple", 
            "Homemade trail mix", "Protein shake", "Vegetable sticks with guacamole", "Apple with cheese slices", 
            "Rice cakes with avocado", "Chia pudding", "Pumpkin seeds", "Baked sweet potato fries", "Smoothie with protein powder", 
            "Hard-boiled eggs", "Low-fat cheese sticks"
        ]
    }
    
    menu = "\nSuggested Healthy Menu:\n"
    for key, value in categories.items():

        menu += "{}: {}\n".format(key, random.choice(value)) 
    
    return menu

# Function to replicate and pinpoint BMI on a chart
def replicate_and_pinpoint_bmi_on_chart(weight, height):

    height_meters = (height[0] * 12 + height[1]) * 0.0254                           # Convert height to meters
    
    plt.figure(figsize=(10, 5))
    
    height_range = np.linspace(4.6, 6.9, 100)                                       # Set physical range of heights on x-y plot
    weight_range = np.linspace(100, 250, 100)                                       # Set physical range of weights
    
    height_range_meters = height_range * 0.3048                                     # Set numerical range of heights (meters)
    weight_range_kg = weight_range * 0.453592                                       # Set numerical range of weights (kg)
    
    height_grid, weight_grid = np.meshgrid(height_range_meters, weight_range_kg)    # Create grid using ranges
    bmi_grid = weight_grid / (height_grid ** 2)                                     # Set BMI category divisions
    
    levels = [10, 15, 20, 25, 30, 40]                                               # BMI levels
    colors = ['aqua', 'limegreen', 'yellow', 'orange', 'red']                       # Colors of BMI categories
    
    plt.contourf(height_grid * 3.28084, weight_grid * 2.20462, bmi_grid, levels=levels, colors=colors, alpha=0.8)              # Create graph
    plt.colorbar(label='BMI')
    
    plt.plot(height[0] + height[1] / 12, weight, 'k+', markersize=12, label=f'Your BMI: {calculate_bmi(weight, height):.2f}')  # User's BMI on graph
    
    plt.title('BMI Chart')
    plt.xlabel('Height (ft)')
    plt.ylabel('Weight (lbs)')
    
    plt.legend(loc='upper right')       # Legend in upper right of window
    
    chart_path = 'bmi_chart.png'
    plt.savefig(chart_path)
    plt.close()
    
    return chart_path                   # Return chart path

# Function to fetch real-time nutritional information from an external API
def fetch_nutritional_info():

    try:
        response = requests.get('https://api.nal.usda.gov/fdc/v1/foods/list?api_key=pU0wN58tdNGVf0DE4ZwFIGbrHlPkRn7zO1d3O7Jo')  # Included actual API key
        if response.status_code == 200:
            data = response.json()
            # Process and return the data as needed
            return data[:5]  # Just an example, returning the first 5 items ADJUST TO SHOW MACROS FOR FOOD
        else:
            return "Failed to fetch data"
        
    except Exception as e:
        return f"Error: {e}"

# Function to get daily health and nutrition tips
def get_daily_tip():

    tips = [                                                            # List of tips
        "Drink plenty of water throughout the day.",
        "Include a variety of fruits and vegetables in your diet.",
        "Avoid processed foods and opt for whole foods.",
        "Exercise regularly to maintain a healthy weight.",
        "Get enough sleep to support overall health.",
        "Limit sugary drinks and snacks.",
        "Choose lean proteins such as chicken, fish, and beans.",
        "Include healthy fats like nuts, seeds, and avocados in your diet."
    ]
    return random.choice(tips)                  # Return a random tip from list

# Function to create the Tkinter user interface
def create_tkinter_window():

    # Function to display QR code using QR code path
    def display_qr_code(qr_code_path):  
        qr_code_window = tk.Toplevel(window)
        qr_code_window.title("QR Code")
        
        qr_code_img = tk.PhotoImage(file=qr_code_path)
        qr_code_label = tk.Label(qr_code_window, image=qr_code_img)
        qr_code_label.image = qr_code_img
        qr_code_label.pack(pady=10)

    # Function to display BMI chart with graph
    def display_bmi_chart(chart_path):
        bmi_chart_window = tk.Toplevel(window)
        bmi_chart_window.title("BMI Chart")
        
        chart_img = tk.PhotoImage(file=chart_path)
        chart_label = tk.Label(bmi_chart_window, image=chart_img)
        chart_label.image = chart_img
        chart_label.pack(pady=10)

    # Function to display suggested menu and food options
    def display_food_options(food_table_path):
        food_options_window = tk.Toplevel(window)
        food_options_window.title("Food Options")
        
        food_table_img = tk.PhotoImage(file=food_table_path)
        food_table_label = tk.Label(food_options_window, image=food_table_img)
        food_table_label.image = food_table_img
        food_table_label.pack(pady=10)

    # Function to clear form
    def clear_form():
        weight_entry.delete(0, tk.END)
        height_ft_entry.delete(0, tk.END)
        height_in_entry.delete(0, tk.END)
        goals_entry.delete(0, tk.END)
        activity_level_combobox.set('')
        dietary_preferences_combobox.set('')
        allergies_combobox.set('')

    # Function to save generated nutrition info to a text file locally
    def save_data_to_file(data):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(data)
            messagebox.showinfo("Saved", f"Data saved to {file_path}")

    # Function for loading data from locally saved files
    def load_data_from_file():
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                data = file.read()
                weight, height_ft, height_in, goals, activity_level, dietary_preferences, allergies = data.split(',')
                weight_entry.insert(0, weight)
                height_ft_entry.insert(0, height_ft)
                height_in_entry.insert(0, height_in)
                goals_entry.insert(0, goals)
                activity_level_combobox.set(activity_level)
                dietary_preferences_combobox.set(dietary_preferences)
                allergies_combobox.set(allergies)
            messagebox.showinfo("Loaded", f"Data loaded from {file_path}")

    # Function for showing help messages to guide user
    def show_help():
        help_text = (
            "1. Enter your weight in pounds.\n"
            "2. Enter your height in feet and inches.\n"
            "3. Enter your personal goals.\n"
            "4. Select your activity level (e.g., Sedentary, Moderate, Active).\n"
            "5. Select your dietary preferences (e.g., Vegetarian, Vegan, Keto).\n"
            "6. Select any allergies (e.g., Nuts, Chicken, Gluten).\n"
            "7. Click 'Submit' or press 'Enter' to generate your plan.\n"
            "8. Use 'Save' to save your data, 'Load' to load saved data, and 'Clear' to clear the form.\n"
            "9. View the QR code, BMI chart, and food options generated for you."
        )
        messagebox.showinfo("Help", help_text)

    # Function for creating a profile using the user's input
    def create_profile():
        profile_name = profile_entry.get()
        if profile_name:
            conn = sqlite3.connect('nutritional_planner.db')
            c = conn.cursor()
            c.execute("INSERT INTO profiles (name) VALUES (?)", (profile_name,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Profile Created", f"Profile '{profile_name}' created successfully!")
            profile_entry.delete(0, tk.END)
            load_profiles()
    
    # Function for retrieving profile names from database to display
    def load_profiles():
        conn = sqlite3.connect('nutritional_planner.db')
        c = conn.cursor()
        c.execute("SELECT name FROM profiles")
        profiles = c.fetchall()
        conn.close()
        profile_listbox.delete(0, tk.END)
        for profile in profiles:
            profile_listbox.insert(tk.END, profile[0])

    # Function for retrieving data on a preexisting user from database
    def select_profile(event):
        try:
            selected_profile = profile_listbox.get(profile_listbox.curselection())
            conn = sqlite3.connect('nutritional_planner.db')
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE profile_name=?", (selected_profile,))
            user_data = c.fetchone()
            conn.close()
            if user_data:
                weight_entry.delete(0, tk.END)
                height_ft_entry.delete(0, tk.END)
                height_in_entry.delete(0, tk.END)
                goals_entry.delete(0, tk.END)
                activity_level_combobox.set(user_data[7])
                dietary_preferences_combobox.set(user_data[8])
                allergies_combobox.set(user_data[9])
                weight_entry.insert(0, user_data[1])
                height_ft_entry.insert(0, user_data[2])
                height_in_entry.insert(0, user_data[3])
                goals_entry.insert(0, user_data[4])
        except:
            messagebox.showwarning("Profile Selection", "Please select a valid profile.")

    # Function to process input from user and generate all output data (graph, menu, and qr code)
    def on_submit(event=None):
        try:
            weight = float(weight_entry.get())
            height = (int(height_ft_entry.get()), int(height_in_entry.get()))
            goals = goals_entry.get()
            activity_level = activity_level_combobox.get()
            dietary_preferences = dietary_preferences_combobox.get()
            allergies = allergies_combobox.get()
            
            bmi = calculate_bmi(weight, height)
            nutritional_plan = get_nutritional_plan(bmi, goals, activity_level, dietary_preferences, allergies) + get_food_menu() + get_daily_tip()         # Added food menu and daily tip to nutritional plan

            qr_code_path = generate_qr_code(nutritional_plan)
            chart_path = replicate_and_pinpoint_bmi_on_chart(weight, height)
            food_table_path = create_food_options_table()
            
            selected_profile = profile_listbox.get(profile_listbox.curselection())
            save_user_data(weight, height[0], height[1], goals, bmi, nutritional_plan, activity_level, dietary_preferences, allergies, selected_profile)
            
            messagebox.showinfo("Nutritional Plan", f"Your BMI: {bmi:.2f}\nPlan: {nutritional_plan}")

            display_qr_code(qr_code_path)
            display_bmi_chart(chart_path)
            display_food_options(food_table_path)
            
            data_to_save = f"{weight},{height[0]},{height[1]},{goals},{activity_level},{dietary_preferences},{allergies}"
            save_data_to_file(data_to_save)
        
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for weight and height.")
        except:
            messagebox.showwarning("Profile Selection", "Please select a valid profile.")

    # Graphical creation of the form and initial window
    window = tk.Tk()
    window.title("Nutritional Planner")
    window.geometry('600x800')

    frame = tk.Frame(window, padx=20, pady=20)
    frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(frame, text="Weight (lbs)").pack(pady=(10, 5))
    weight_entry = tk.Entry(frame)
    weight_entry.pack(pady=(0, 10))
    
    tk.Label(frame, text="Height (ft and in)").pack(pady=(10, 5))
    
    height_frame = tk.Frame(frame)
    height_frame.pack(pady=(0, 10))
    
    tk.Label(height_frame, text="Feet").grid(row=0, column=0, padx=5)
    height_ft_entry = tk.Entry(height_frame, width=5)
    height_ft_entry.grid(row=0, column=1, padx=5)
    
    tk.Label(height_frame, text="Inches").grid(row=0, column=2, padx=5)
    height_in_entry = tk.Entry(height_frame, width=5)
    height_in_entry.grid(row=0, column=3, padx=5)
    
    tk.Label(frame, text="Personal Goals").pack(pady=(10, 5))
    goals_entry = tk.Entry(frame)
    goals_entry.pack(pady=(0, 10))
    
    tk.Label(frame, text="Activity Level").pack(pady=(10, 5))
    activity_level_combobox = ttk.Combobox(frame, values=["Sedentary", "Moderate", "Active"])
    activity_level_combobox.pack(pady=(0, 10))

    tk.Label(frame, text="Dietary Preferences").pack(pady=(10, 5))
    dietary_preferences_combobox = ttk.Combobox(frame, values=["None", "Vegetarian", "Vegan", "Keto", "Meat"])
    dietary_preferences_combobox.pack(pady=(0, 10))

    tk.Label(frame, text="Allergies").pack(pady=(10, 5))
    allergies_combobox = ttk.Combobox(frame, values=["None", "Nuts", "Chicken", "Gluten"])
    allergies_combobox.pack(pady=(0, 10))

    tk.Label(frame, text="Profile Name").pack(pady=(10, 5))
    profile_entry = tk.Entry(frame)
    profile_entry.pack(pady=(0, 10))
    tk.Button(frame, text="Create Profile", command=create_profile).pack(pady=(0, 10))

    tk.Label(frame, text="Select Profile").pack(pady=(10, 5))
    profile_listbox = tk.Listbox(frame)
    profile_listbox.pack(pady=(0, 10))
    profile_listbox.bind('<<ListboxSelect>>', select_profile)
    load_profiles()
    
    # Function for producing a graph showing the progress of a user over time as their weight/BMI changes
    def track_progress():
        selected_profile = profile_listbox.get(profile_listbox.curselection())
        conn = sqlite3.connect('nutritional_planner.db')
        c = conn.cursor()
        c.execute("SELECT timestamp, bmi FROM users WHERE profile_name=?", (selected_profile,))
        data = c.fetchall()
        conn.close()

        dates = [datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S') for row in data]
        bmis = [row[1] for row in data]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, bmis, marker='o')
        plt.title('BMI Progress Over Time')
        plt.xlabel('Date')
        plt.ylabel('BMI')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    
    # Button creation
    submit_button = tk.Button(frame, text="Submit", command=on_submit)
    submit_button.pack(pady=10)
    
    clear_button = tk.Button(frame, text="Clear", command=clear_form)
    clear_button.pack(pady=10)
    
    save_button = tk.Button(frame, text="Save", command=lambda: save_data_to_file(f"{weight_entry.get()},{height_ft_entry.get()},{height_in_entry.get()},{goals_entry.get()},{activity_level_combobox.get()},{dietary_preferences_combobox.get()},{allergies_combobox.get()}"))
    save_button.pack(pady=10)
    
    load_button = tk.Button(frame, text="Load", command=load_data_from_file)
    load_button.pack(pady=10)
    
    help_button = tk.Button(frame, text="Help", command=show_help)
    help_button.pack(pady=10)

    track_button = tk.Button(frame, text="Track Progress", command=track_progress)
    track_button.pack(pady=10)

    daily_tip = get_daily_tip()
    tk.Label(frame, text=f"Daily Tip: {daily_tip}", wraplength=400, justify='center', font=('Arial', 12, 'italic')).pack(pady=(20, 10))

    window.bind('<Return>', on_submit)  # Bind the Enter key to the on_submit function
    
    window.mainloop()

# Initialize the database
def create_db():
    conn = sqlite3.connect('nutritional_planner.db')
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS users''')  # Drop existing table to recreate it with correct columns
    c.execute('''CREATE TABLE users
                 (id INTEGER PRIMARY KEY, weight REAL, height_ft INTEGER, height_in INTEGER, goals TEXT, bmi REAL, plan TEXT, activity_level TEXT, dietary_preferences TEXT, allergies TEXT, profile_name TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS profiles (id INTEGER PRIMARY KEY, name TEXT)''')
    conn.commit()
    conn.close()

# Function to save user data to local database
def save_user_data(weight, height_ft, height_in, goals, bmi, plan, activity_level, dietary_preferences, allergies, profile_name):
    conn = sqlite3.connect('nutritional_planner.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (weight, height_ft, height_in, goals, bmi, plan, activity_level, dietary_preferences, allergies, profile_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (weight, height_ft, height_in, goals, bmi, plan, activity_level, dietary_preferences, allergies, profile_name))
    conn.commit()
    conn.close()

# Call create_db() once to initialize the database
create_db()

# Main function to start the Tkinter application
def main():
    create_tkinter_window()

if __name__ == "__main__":
    main()


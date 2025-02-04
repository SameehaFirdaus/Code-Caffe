import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pyttsx3
import speech_recognition as sr

# Initialize text-to-speech engine
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to user's voice input
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("I am listening. Please speak now.")
        try:
            audio = recognizer.listen(source, timeout=10)
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
        except sr.RequestError:
            speak("There seems to be an issue with the speech recognition service.")
        except sr.WaitTimeoutError:
            speak("You didn't say anything. Please try again.")
    return None

# Function to calculate the total price
def calculate_price():
    if not coffee_var.get() or not size_var.get():
        messagebox.showwarning("Input Error", "Please select both coffee type and size.")
        speak("Please select both coffee type and size.")
        return

    total_price = 0
    if coffee_var.get() == "Espresso":
        total_price += 50
    elif coffee_var.get() == "Latte":
        total_price += 60
    elif coffee_var.get() == "Cappuccino":
        total_price += 70

    if size_var.get() == "Small":
        total_price += 10
    elif size_var.get() == "Medium":
        total_price += 20
    elif size_var.get() == "Large":
        total_price += 30

    if add_ons_var.get() == "Yes":
        total_price += 20  # Extra charge for add-ons

    result_text = f"Your total is Rs. {total_price}"
    messagebox.showinfo("Total Price", result_text)
    speak(result_text)

# Function to reset selections
def reset_selections():
    coffee_var.set("")
    size_var.set("")
    add_ons_var.set("No")
    speak("Selections have been reset.")

# Voice assistant to take input for coffee selection
def voice_assistant():
    # Ask for coffee type
    while True:
        speak("What type of coffee would you like? Espresso, Latte, or Cappuccino?")
        coffee_choice = listen()
        if coffee_choice:
            for option in coffee_options:
                if option.lower() in coffee_choice:
                    coffee_var.set(option)
                    speak(f"You selected {option}.")
                    break
            else:
                speak("Invalid choice. Please try again.")
                continue
            break

    # Ask for coffee size
    while True:
        speak("What size would you like? Small, Medium, or Large?")
        size_choice = listen()
        if size_choice:
            for option in size_options:
                if option.lower() in size_choice:
                    size_var.set(option)
                    speak(f"You selected {option} size.")
                    break
            else:
                speak("Invalid choice. Please try again.")
                continue
            break

    # Ask for add-ons
    while True:
        speak("Do you want to add extra toppings like whipped cream? Say Yes or No.")
        addons_choice = listen()
        if addons_choice:
            if "yes" in addons_choice:
                add_ons_var.set("Yes")
                speak("Extra toppings added.")
            elif "no" in addons_choice:
                add_ons_var.set("No")
                speak("No extra toppings added.")
            else:
                speak("Invalid choice. Please say Yes or No.")
                continue
            break

    speak("Your selections have been updated. Please confirm and calculate the total price.")

# Main window setup
root = tk.Tk()
root.title("Code Caffe - Coffee Vending Machine")
root.geometry("800x600")
root.attributes('-fullscreen', True)  # Start in full-screen mode

# Background image setup
try:
    # Load the .jpg image using PIL
    bg_image_pil = Image.open(r"C:\\Users\\syedi\\Downloads\\coffee.jpg")
    bg_photo = ImageTk.PhotoImage(bg_image_pil)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)  # Cover the entire window
except Exception as e:
    messagebox.showerror("Image Error", f"Error loading background image: {e}")
    root.configure(bg="#000000")

# Coffee type selection
coffee_var = tk.StringVar()
coffee_label = tk.Label(root, text="Select Coffee Type", font=("Arial", 24), fg="white", bg="#000000")
coffee_label.pack(pady=10)

coffee_options = ["Espresso", "Latte", "Cappuccino"]
coffee_var.set("")  # Default value
coffee_dropdown = tk.OptionMenu(root, coffee_var, *coffee_options)
coffee_dropdown.pack()

# Coffee size selection
size_var = tk.StringVar()
size_label = tk.Label(root, text="Select Coffee Size", font=("Arial", 24), fg="white", bg="#000000")
size_label.pack(pady=10)

size_options = ["Small", "Medium", "Large"]
size_var.set("")  # Default value
size_dropdown = tk.OptionMenu(root, size_var, *size_options)
size_dropdown.pack()

# Add-ons selection
add_ons_var = tk.StringVar(value="No")
add_ons_label = tk.Label(root, text="Add Extra (e.g., Whipped Cream)?", font=("Arial", 24), fg="white", bg="#000000")
add_ons_label.pack(pady=10)

add_ons_radio_no = tk.Radiobutton(root, text="No", variable=add_ons_var, value="No", font=("Arial", 20), fg="black", bg="#000000")
add_ons_radio_no.pack()
add_ons_radio_yes = tk.Radiobutton(root, text="Yes", variable=add_ons_var, value="Yes", font=("Arial", 20), fg="black", bg="#000000")
add_ons_radio_yes.pack()

# Calculate button
calculate_button = tk.Button(root, text="Calculate Total Price", command=calculate_price, font=("Arial", 20), fg="black", bg="orange")
calculate_button.pack(pady=20)

# Reset button
reset_button = tk.Button(root, text="Reset", command=reset_selections, font=("Arial", 20), fg="black", bg="red")
reset_button.pack()

# Voice assistant button
voice_assistant_button = tk.Button(root, text="Voice Assistant", command=voice_assistant, font=("Arial", 20), fg="black", bg="blue")
voice_assistant_button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()

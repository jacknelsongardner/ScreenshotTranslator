import tkinter as tk
import keyboard

def show_popup():
    print("made popup")
    popup = tk.Toplevel(root)
    popup.overrideredirect(True)  # Remove window decorations
    popup.attributes('-topmost', True)  # Keep the window on top
    popup.geometry("200x100")
    
    # Remove the title bar
    root.overrideredirect(True)

    # Bind the key press event to the function that closes the popup
    #popup.bind("<KeyPress>", lambda event: popup.destroy())

# Main Tkinter window
root = tk.Tk()
root.title("Main Window")

# Button to show the popup
popup_button = tk.Button(root, text="Show Popup", command=show_popup)
popup_button.pack(pady=20)

root.mainloop()






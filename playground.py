import tkinter as tk

def set_transparency(window, alpha):
    window.attributes("-alpha", alpha)

def main():
    root = tk.Tk()
    root.title("Translucent Window")

    # Set initial transparency (0.5 for semi-transparency)
    set_transparency(root, 0.5)

    # Create a label inside the window
    label = tk.Label(root, text="Translucent Window")
    label.pack(padx=20, pady=20)

    # Create a slider to control transparency
    transparency_slider = tk.Scale(root, from_=0.1, to=1.0, resolution=0.1, orient=tk.HORIZONTAL,
                                   label="Transparency", command=lambda value: set_transparency(root, float(value)))
    transparency_slider.set(0.5)  # Set initial value
    transparency_slider.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
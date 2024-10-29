import tkinter as tk

root = tk.Tk()
root.title("AirHub")

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Configure the main window's size
root.geometry(f"{screen_width // 2}x{screen_height // 2}")

# Create the left frame
left_frame = tk.Frame(root, bg='lightblue')
left_frame.grid(
    row=0, column=0, 
    sticky='nsew',
    rowspan=screen_height
)  # Use grid to place the left frame

# Create the right frame
right_frame = tk.Frame(root, bg='lightgreen')
right_frame.grid(row=0, column=1, sticky='nsew')  # Use grid to place the left frame

# Make the column frames expand to fill the window
root.grid_columnconfigure(0, weight=1)  # Allow left frame to take 1 parts
root.grid_columnconfigure(1, weight=7)  # Allow right frame to take 7 parts

right_frame.grid_rowconfigure(0, weight=1)
right_frame.grid_rowconfigure(1, weight=1)
right_frame.grid_rowconfigure(2, weight=1)


# Make the row frames expand to fill the winodow
left_frame.grid_rowconfigure(0, weight=1) 
left_frame.grid_rowconfigure(1, weight=1)
left_frame.grid_rowconfigure(2, weight=1)
left_frame.grid_rowconfigure(3, weight=2,pad=screen_height)

# Add labels to the left column (Column 0) with different rows
tk.Label(left_frame, text="Row 1", bg='lightblue').grid(row=0, column=0, sticky='nsew')
tk.Label(left_frame, text="Row 2", bg='lightblue').grid(row=1, column=0, sticky='nsew')
tk.Label(left_frame, text="Row 3", bg='lightblue').grid(row=2, column=0, sticky='nsew')
tk.Label(left_frame, text="Air", bg='lightblue').grid(row=3, column=0, sticky='nsew')

# Add some content to the frames (optional)
tk.Label(right_frame, text="Social Media Post 1", bg='lightgreen').grid(row=0, column=0, sticky='nsew')  # Center the label with grid
tk.Label(right_frame, text="Social Media Post 2", bg='lightgreen').grid(row=1, column=0, sticky='nsew')  # Center the label with grid
tk.Label(right_frame, text="Social Media Post 3", bg='lightgreen').grid(row=2, column=0, sticky='nsew')  # Center the label with grid



root.mainloop()
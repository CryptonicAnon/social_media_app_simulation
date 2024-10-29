import tkinter as tk

# Initialize the main window
root = tk.Tk()
root.title("AirHub")

# Get the devices screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Fit the main windows size
root.geometry(f"{screen_width // 2}x{screen_height // 2}")

# Left frame
left_frame = tk.Frame(root, bg='lightgrey', width=200)
left_frame.grid(
    row=0, column=0, 
    sticky='ns')

# Create a Canvas in the right frame for scrolling
right_canvas = tk.Canvas(root, bg='white')
right_canvas.grid(row=0, column=1, sticky='nsew')  # Place the canvas with grid

# Add a scrollbar for the right frame
scrollbar = tk.Scrollbar(root, orient="vertical", command=right_canvas.yview)
scrollbar.grid(row=0, column=2, sticky="ns")

# Configure canvas to work with the scrollbar
right_canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas for the scrollable content
right_frame = tk.Frame(right_canvas, bg='white')
right_canvas.create_window((0, 0), window=right_frame, anchor="nw")

# Add content to the right frame (scrollable area)
for i in range(20):
    tk.Label(right_frame, text=f"     Social Media Post {i+1}", bg='white').grid(row=i, column=0, sticky='nsew', pady=30)

# Configure resizing of rows and columns
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=0) 
root.grid_columnconfigure(1, weight=1)

# Configure the right frame scroll region based on its content
def update_scrollregion(event):
    right_canvas.configure(scrollregion=right_canvas.bbox("all"))

# Bind mouse scroll events to the canvas
def on_mouse_wheel(event):
    scroll_speed = 1
    if event.num == 4 or event.delta > 0:
        right_canvas.yview_scroll(int(-scroll_speed), "units")
    elif event.num == 5 or event.delta < 0:
        right_canvas.yview_scroll(int(scroll_speed), "units")

# Windows and macOS
right_canvas.bind_all("<MouseWheel>", on_mouse_wheel)
# Linux
right_canvas.bind_all("<Button-4>", on_mouse_wheel)
right_canvas.bind_all("<Button-5>", on_mouse_wheel)

# Update scroll region whenever the content changes
right_frame.bind("<Configure>", update_scrollregion)

# Left frame content
tk.Label(left_frame, text=" ", bg='lightgrey').grid(row=0, column=0, sticky='nsew')
tk.Label(left_frame, text="Feed", bg='lightgrey').grid(row=1, column=0, sticky='nsew', pady=5)
tk.Label(left_frame, text="Messages", bg='lightgrey').grid(row=2, column=0, sticky='nsew', pady=5)
tk.Label(left_frame, text="    Notifications    ", bg='lightgrey').grid(row=3, column=0, sticky='nsew', pady=5)
tk.Label(left_frame, text="Profile", bg='lightgrey').grid(row=4, column=0, sticky='nsew', pady=5)
tk.Label(left_frame, text=" ", bg='lightgrey').grid(row=5, column=0, sticky='nsew')

# Make the row frames expand to fill the window
left_frame.grid_rowconfigure(5, weight=1)  # Allow last row to expand in the left frame

root.mainloop()

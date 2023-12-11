import tkinter as tk
from datetime import datetime
import math

# Function to update the clock every 1 second
def update_clock():
    current_time = datetime.now().time()
    hour = current_time.hour
    minute = current_time.minute
    second = current_time.second
    
    # Calculate the angles for hour, minute, and second hands
    hour_angle = (hour % 12) * 30 + minute * 0.5
    minute_angle = minute * 6 + second * 0.1
    second_angle = second * 6
    
    # Update the clock hands
    canvas.delete("all")
    draw_clock_face()
    draw_clock_hand(hour_angle, 80, 6, "black")
    draw_clock_hand(minute_angle, 120, 4, "black")
    draw_clock_hand(second_angle, 140, 2, "red")
    
    # Schedule the next update after 1 second
    root.after(1000, update_clock)

# Function to draw the clock face
def draw_clock_face():
    canvas.create_oval(10, 10, 240, 240, width=2)
    for i in range(12):
        angle = math.radians(30 * i - 90)
        x = 125 + math.cos(angle) * 100
        y = 125 + math.sin(angle) * 100
        canvas.create_text(x, y, text=str(i + 1), font=("Arial", 12))

# Function to draw a clock hand
def draw_clock_hand(angle, length, width, color):
    angle = math.radians(angle - 90)
    x = 125 + math.cos(angle) * length
    y = 125 + math.sin(angle) * length
    canvas.create_line(125, 125, x, y, width=width, fill=color)

# Create the main window
root = tk.Tk()
root.title("Analog Clock")

# Create the canvas for drawing the clock
canvas = tk.Canvas(root, width=250, height=250)
canvas.pack()

# Start the clock
update_clock()

# Run the application
root.mainloop()

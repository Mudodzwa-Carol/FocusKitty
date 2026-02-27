import tkinter as tk
from tkinter import messagebox
import threading
import time
import random
from PIL import Image, ImageTk
import winsound

# CONFIGURATION SETTINGS 
# controls how often kitty checks attention and how long the user has to respond
CHECK_MIN = 30
CHECK_MAX = 60
EXPECTANT_TIMEOUT = 8

# UI Colours
BG_COLOR = "#D7B2F8"
BUTTON_COLOR = "#B57EDC"
BUTTON_TEXT = "white"

# MAIN WINDOW SETUP
root = tk.Tk()
root.title("Focus Kitty 🐱")
root.geometry("650x430")
root.configure(bg=BG_COLOR)
root.attributes("-alpha",0.95)       # Slight transparency
root.resizable(False, False)         # Disable resizing

#TITLE LABEL
title_label = tk.Label(
    root,
    text="FocusKitty\nYour Lock-In Buddy 🐱",
    font=("Helvetica", 20, "bold"),
    bg=BG_COLOR,
    fg="#4B2E83",
    justify="center"
)
title_label.pack(pady=10)

# LOAD IMAGES
def load_img(name):
    return ImageTk.PhotoImage(Image.open(name).resize((220, 220)))        # Resize kitty images to 220x220

kitty_happy = load_img("kitty_happy.jpeg")
kitty_expectant = load_img("kitty_expectant.jpeg")
kitty_eating = load_img("kitty_eating.jpeg")
kitty_crying = load_img("kitty_crying.jpeg")

# STATE VARIABLES
# These track session progress
session_running = False
time_left = 0
expectant_active = False

# POMODORO TIMER
left_frame = tk.Frame(root, bg=BG_COLOR)
left_frame.pack(side="left", padx=25, pady=25)

tk.Label(
    left_frame,
    text="Pomodoro Timer",
    font=("Helvetica", 16, "bold"),
    bg=BG_COLOR
).pack(pady=8)

# Entry where user types minutes for focus session
time_entry = tk.Entry(left_frame, font=("Helvetica", 14), justify="center")
time_entry.insert(0, "25")        # Default to 25 minutes
time_entry.pack(pady=5)

tk.Label(
    left_frame,
    text="Minutes",
    bg=BG_COLOR
).pack()

# Countdown display
timer_label = tk.Label(
    left_frame,
    text="00:00",
    font=("Helvetica", 34, "bold"),
    bg=BG_COLOR
)
timer_label.pack(pady=15)

# BUTTON STYLING FUNCTION
# Keeps button design consistent
def styled_button(parent, text, command):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=BUTTON_COLOR,
        fg=BUTTON_TEXT,
        activebackground="#A66BCF",
        relief="flat",
        padx=20,
        pady=8,
        font=("Helvetica", 12, "bold")
    )

# TIMER LOGIC
def update_timer():
    """
    Handles countdown logic.
    Runs in background thread.
    """
    global time_left, session_running

    while session_running and time_left > 0:
        mins, secs = divmod(time_left, 60)
        timer_label.config(text=f"{mins:02d}:{secs:02d}")
        time.sleep(1)
        time_left -= 1

# When timer finishes successfully
    if time_left == 0 and session_running:
        session_running = False
        messagebox.showinfo("Session Complete", "Great job! 🎉")
        set_kitty("happy")


def start_session():
    """
    Starts focus session.
    Launches timer + attention cycle threads.
    """
    global session_running, time_left

    if not session_running:
        try:
            minutes = int(time_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number.")
            return

        time_left = minutes * 60
        session_running = True
        set_kitty("happy")

        threading.Thread(target=update_timer, daemon=True).start()
        threading.Thread(target=attention_cycle, daemon=True).start()


def stop_session():
    """
    Stops session manually.
    """
    global session_running
    session_running = False
    set_kitty("happy")


def fail_session():
    """
    Called when user ignores kitty.
    Fully ends session.
    """
    global session_running, expectant_active

    session_running = False
    expectant_active = False

    for i in range(3):
        winsound.Beep(1200, 400)

    set_kitty("crying")
    messagebox.showwarning("Focus Broken 😿", "You ignored Kitty. Session failed!")
   
# BUTTONS
button_frame = tk.Frame(left_frame, bg=BG_COLOR)
button_frame.pack(pady=10)

start_btn = styled_button(button_frame, "Start", start_session)
stop_btn = styled_button(button_frame, "Stop", stop_session)

start_btn.pack(side="left", padx=5)
stop_btn.pack(side="left", padx=5)

# KITTY UI
right_frame = tk.Frame(root, bg=BG_COLOR)
right_frame.pack(side="right", padx=25)

kitty_label = tk.Label(right_frame, image=kitty_happy, bg=BG_COLOR)
kitty_label.pack()

status_label = tk.Label(
    right_frame,
    text="Kitty is happy 😊",
    font=("Helvetica", 12),
    bg=BG_COLOR
)
status_label.pack(pady=5)

feed_btn = styled_button(right_frame, "Feed Kitty 🍟", lambda: feed_kitty())


def show_feed_button(show):
    """Shows or hides feed button."""
    if show:
        feed_btn.pack(pady=10)
    else:
        feed_btn.pack_forget()


def set_kitty(state):
    """
    Updates kitty image + status text
    based on current emotional state.
    """
    if state == "happy":
        kitty_label.config(image=kitty_happy)
        status_label.config(text="Kitty is happy 😊")
        show_feed_button(False)

    elif state == "expectant":
        kitty_label.config(image=kitty_expectant)
        status_label.config(text="Feed me to prove you're focused 👀")
        show_feed_button(True)

    elif state == "eating":
        kitty_label.config(image=kitty_eating)
        status_label.config(text="Yum! 🍟")
        show_feed_button(False)

    elif state == "crying":
        kitty_label.config(image=kitty_crying)
        status_label.config(text="You ignored me 😿")
        show_feed_button(False)


def feed_kitty():
    """
    Called when user clicks Feed.
    Saves session if within time.
    """
    global expectant_active

    if expectant_active and session_running:
        expectant_active = False
        set_kitty("eating")

        def back_to_happy():
            time.sleep(3)
            if session_running:
                set_kitty("happy")

        threading.Thread(target=back_to_happy, daemon=True).start()

# ATTENTION CHECK LOGIC
def attention_cycle():
    """
    Randomly checks if user is still focused.
    If user does not respond in time -> fail session.
    """
    global expectant_active

    while session_running:
        wait_time = random.randint(CHECK_MIN, CHECK_MAX)
        time.sleep(wait_time)

        if not session_running:
            break

        expectant_active = True
        set_kitty("expectant")

        waited = 0
        while waited < EXPECTANT_TIMEOUT and expectant_active and session_running:
            time.sleep(1)
            waited += 1

        # If user ignored kitty → FAIL
        if expectant_active and session_running:
            fail_session()
            break


# START APPLICATION LOOP
root.mainloop()
🐱 FocusKitty – Your Lock-In Study Buddy

FocusKitty is a fun, interactive Pomodoro timer built with Python and Tkinter.

Instead of just counting down time, FocusKitty checks if you're actually focused. If you ignore Kitty when she asks for attention… your session fails 😿 and a buzz goes off.

This project was built to make productivity more interactive and always visible on the screen you’re working on.

Features

⏳ Custom Pomodoro timer
🎲 Random focus checks (every 30–60 seconds)
🍟 Feed Kitty interaction system
😿 Session fails if you ignore attention checks
🔊 Sound alert on failure
🎨 Soft pastel UI design
🧵 Multithreading for smooth timer + background checks

🧠 How It Works

Start a focus session.
The timer begins counting down.
At random intervals, Kitty becomes “expectant”.
You have 8 seconds to click “Feed Kitty”.
If you respond → session continues.
If you ignore → session fails.

It adds a light accountability system to your study time.

🛠️ Tech Stack

Python
Tkinter (GUI)
Pillow (image handling)
Threading
Winsound (Windows alert sound)

📦 Installation
1️⃣ Clone the repository
git clone https://github.com/Mudodzwa-Carol/focuskitty.git
cd focuskitty
2️⃣ Install dependencies
pip install -r requirements.txt
3️⃣ Add Required Images

Place these images in the same folder as the Python file:

kitty_happy.jpeg
kitty_expectant.jpeg
kitty_eating.jpeg
kitty_crying.jpeg

4️⃣ Run the app
python focuskitty.py

⚠️ Note
winsound only works on Windows.

For macOS/Linux, you may need to replace the beep sound logic.

🎯 Why I Built This

I love using the Pomodoro method, but I didn’t like:

Using a separate device
Switching tabs
Having productivity tools hidden in the background

I wanted something visually present. Something that would call me out if I wasn’t focused. So I built it.


This is a great beginner-friendly project to study.

Feel free to improve it, or build your own version 🐱
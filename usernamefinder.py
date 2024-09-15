import time
import random
import threading
from pynput import keyboard
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Controller as MouseController
import pygetwindow as gw

# --- Global Control ---
running = True

class RobloxBot:
    def __init__(self, window):
        self.window = window
        self.keyboard = KeyboardController()
        self.mouse = MouseController()
        self.current_key = None

    def perform_action(self):
        try:
            self.window.activate()
            time.sleep(0.1)  # Ensure window activation

            # Center mouse in window
            self.center_mouse()

            # Random movement
            new_key = random.choice(['w', 'a', 's', 'd'])
            if self.current_key:
                self.keyboard.release(self.current_key)
            self.keyboard.press(new_key)
            self.current_key = new_key

            # Random looking around
            if random.random() < 0.3:  # 30% chance to look around
                self.mouse_look()

            # Random jumping
            if random.random() < 0.2:  # Increased to 20% chance to jump
                self.keyboard.press(Key.space)
                time.sleep(0.1)
                self.keyboard.release(Key.space)

            time.sleep(random.uniform(0.5, 1.5))  # Hold direction for a random duration

        except Exception as e:
            print(f"Error in bot for window {self.window.title}: {e}")

    def center_mouse(self):
        center_x = self.window.left + self.window.width // 2
        center_y = self.window.top + self.window.height // 2
        self.mouse.position = (center_x, center_y)

    def mouse_look(self):
        x_move = random.randint(-50, 50)
        y_move = random.randint(-30, 30)
        current_x, current_y = self.mouse.position
        new_x = max(self.window.left, min(current_x + x_move, self.window.left + self.window.width - 1))
        new_y = max(self.window.top, min(current_y + y_move, self.window.top + self.window.height - 1))
        self.mouse.position = (new_x, new_y)

def get_game_windows(game_name="Roblox"):
    game_windows = []
    all_windows = gw.getWindowsWithTitle(game_name)
    
    for window in all_windows:
        if "Roblox" in window.title and not ("Account" in window.title or "Manager" in window.title):
            game_windows.append(window)
    
    return game_windows

def bot_thread(bot):
    global running
    while running:
        bot.perform_action()

def on_press(key):
    global running
    if key == keyboard.Key.esc:
        print("Escape key pressed. Stopping bots...")
        running = False
        return False  # Stop the listener

def main():
    global running
    game_windows = get_game_windows()
    if not game_windows:
        print("No Roblox windows found. Exiting...")
        return

    bots = [RobloxBot(window) for window in game_windows]
    threads = []

    for bot in bots:
        thread = threading.Thread(target=bot_thread, args=(bot,))
        thread.daemon = True
        threads.append(thread)
        thread.start()

    print(f"Running {len(bots)} bots. Press 'Esc' to stop.")

    # Set up the keyboard listener
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print("All bots stopped. Exiting...")

if __name__ == "__main__":
    main()
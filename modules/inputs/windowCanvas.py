from queue import Queue
import tkinter as tk
import threading
import tkinter as tk
import random

import modules.settings.settingsConfig as settingsConfig
import main

class FacialExpressionApp:
    def __init__(self, master):
        self.master = master
        self.master.geometry("800x600")
        self.Expresions = ['(0_-)','(--_--)','(-_0)']
        # Calculate center position for the window
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        width,height = 300, 100
        x = int((screen_width - width) // 1.9)
        y = (screen_height - height) // 20
        self.master.geometry(f"{width}x{height}+{x}+{y}")
        
        # Create a canvas
        self.canvas = tk.Canvas(self.master, width=900, height=600, bg="black")
        self.canvas.pack()
        self.master.overrideredirect(True)

        # Initial facial expression
        font_size = self.canvas.winfo_reqheight() // 3  # Font size is half the height of the canvas
        self.face_id = self.canvas.create_text(150, 50, text='(0_0)',fill = "white" ,font=("Arial", int(font_size/4),))
        
        # Schedule the update_expression function every 5 seconds
        self.master.after(3000, self.update_expression)
        self.canvas.bind("<Button-1>", self.handle_click)

    def update_Back_expression(self):
        expression = '(0_0)'
        self.canvas.itemconfig(self.face_id, text=expression)
        self.master.after(5000, self.update_expression)
    def update_expression(self):
        # Change facial expression
        current_expression = self.canvas.itemcget(self.face_id, "text")
        new_expression = self.Expresions[random.randint(0,len(self.Expresions)-1)] if current_expression == "(0_0)" else "(0_0)"
        self.canvas.itemconfig(self.face_id, text=new_expression)
        self.master.after(500, self.update_Back_expression)

    def handle_click(self, event):
        main.listeningSound()
        self.master.withdraw()
        x = settingsConfig.showSettingsOptions()
        self.master.deiconify()
        main.thinkingSound()

class ListDisplayerPanel:
    def __init__(self, window, array, Title,result_queue):
        self.window = window
        self.result_queue = result_queue
        self.Title = Title
        self.array = array
        self.Item = None

        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.x_position = (self.screen_width - 800) // 2
        self.y_position = (self.screen_height - 600) // 2
        self.window.geometry(f"800x600+{self.x_position}+{self.y_position}")
        self.window.overrideredirect(True)

        self.item_frame = None
        if self.item_frame:
            self.item_frame.destroy()

        self.item_frame = tk.Frame(window)
        self.item_frame.place(relx=0.5, rely=0.5, anchor="center")

        topCount = 0
        for item in array:
            if topCount <10:
                button = tk.Button(self.item_frame, text=f"{array.index(item) + 1}. {item}", command=lambda item=item: self.selecteItem(item) )
                button.pack(pady=5)
                topCount +=1
            else:
                break

        self.entry = tk.Entry(window, width=50)
        self.entry.pack(pady=10, padx=20)



    def submit_pressed(self):
        self.window.destroy()
        self.result_queue.put(self.Item)

    def selecteItem(self,item):
        self.Item = item
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, "Selected: " + self.Item)
        
        
    def invokeListDisplayerPanel(self):
        title_label = tk.Label(self.window, text= self.Title, font=("Helvetica", 16))
        title_label.place(relx=0.5, rely=0.1, anchor="center")
        submit_button = tk.Button(self.window, text="Select", width=10, height=2, bg="white", command=self.submit_pressed)
        submit_button.pack(side=tk.LEFT, pady=10)
    
        self.window.wait_window(self.window)

class vKey:
    def __init__(self, window, result_queue):
        self.window = window
        self.result_queue = result_queue
        self.window_width = 800
        self.window_height = 600

        self.Item = None
        self.KeyDone = False

        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        x = (self.screen_width - self.window_width) // 2
        y = (self.screen_height - self.window_height) // 2
        window.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        window.overrideredirect(True)

        self.entry = tk.Entry(self.window, width=50)
        self.entry.pack(side=tk.TOP, pady=0.1, padx=20)

    def submit_pressed(self):
        self.KeyDone = True
        self.Item = self.entry.get()
        self.window.destroy()
        self.result_queue.put(self.Item)

    def on_key_press(self, key):
        self.entry.insert(tk.END, key)

    def delete_last_char(self):
        current_value = self.entry.get()
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, current_value[:-1])

    def invokeKeyboard(self):
        keyboard_layout = [
            '1234567890',
            '.!@#$%^&*()',
            "'\"_-\/?=+:",
            'qwertyuiop',
            'asdfghjkl',
            'zxcvbnm',
            'QWERTYUIOP',
            'ASDFGHJKL',
            'ZXCVBNM'
        ]

        submit_button = tk.Button(self.window, text="Submit", width=10, height=2, bg="white", command=self.submit_pressed)
        submit_button.pack(pady=10)
        space_button = tk.Button(self.window, text="Space", command=lambda: self.on_key_press(" "))
        back_space = tk.Button(self.window, text="<=", command=self.delete_last_char)

        space_button.pack(side=tk.LEFT, padx=1)
        back_space.pack(side=tk.RIGHT, padx=1)

        for row in keyboard_layout:
            button_frame = tk.Frame(self.window)
            button_frame.pack()

            # Calculate the width of each button based on the number of keys in the row
            button_width = 50 // len(row)

            for key in row:
                key_button = tk.Button(button_frame, text=key, width=button_width, height=2, command=lambda k=key: self.on_key_press(k))
                key_button.pack(side=tk.LEFT)

        # Create a modal dialog
        self.window.wait_window(self.window)

def windowCanvas(subject, array = [""], Title = "List"):
    result_queue = Queue()

    def run_window():
        window = tk.Tk()

        if subject == "list":
            listDisplay = ListDisplayerPanel(window, array, Title,result_queue)
            listDisplay.invokeListDisplayerPanel()
        elif subject == "key":
            keyboard = vKey(window, result_queue)
            keyboard.invokeKeyboard()
        
    thread = threading.Thread(target=run_window)
    thread.start()
    thread.join()

    result = result_queue.get()
    return result


def showFace():
    root = tk.Tk()
    app = FacialExpressionApp(root)
    root.mainloop()

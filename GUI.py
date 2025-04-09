import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont
import math
import os
#from write_to_txt import write_values_to_txt
#from email_notification_ver2 import send_email
START_FLAG = 0
# Constants
PINK = "#FF5BAE"
RED = "#e7305b"
GREEN = "#9bdeac"
CYAN_GRE = "#4CCD99"
GRE_BLU = "#41C9E2"
YELLOW = "#f7f5dd"
FONT_COURIER = "Courier"
SAMPLE_VALUE = str(int(1))
DILU_FAC_VALUE = str(int(1))
DILU_RATI_VALUE = str(int(2))

global total_timer_seconds
total_timer_seconds = 0

# ---------------------------- CLASS FOR POPUP WINDOW ------------------------------------------- # 

class PopupWindow:
    def __init__(self, title, label_text, confirm_command, min_value, max_value):
        self.title = title
        self.label_text = label_text
        self.confirm_command = confirm_command
        self.min_value = min_value
        self.max_value = max_value
        self.value = None
        self.window = None

    def button_click(self, value):
        self.entry_var.set(self.entry_var.get() + value)

    def enter_popup(self):
        self.value = self.entry_var.get()
        if self.value.strip() == "":
            tk.messagebox.showerror("No Value Entered", "Please enter a value.")
            return
        if not self.value.isdigit():
            messagebox.showerror("Invalid Input", "Only integers are allowed.")
            return
        if self.validate_input(self.value):
            self.confirm_command()
            self.window.destroy()
            window.deiconify()
            update_start_button_state()  # when enter clicked, check if all parameters changed

    def validate_input(self, value):
        try:
            numeric_value = float(value)
            if self.min_value <= numeric_value <= self.max_value:
                return True
            else:
                raise ValueError
        except ValueError:
            tk.messagebox.showerror("Invalid Input", f"Please enter a valid value between {self.min_value} and {self.max_value}")
            return False
        
    def backspace_delete(self):
        self.entry_var.set(self.entry_var.get()[:-1])

    def cancel_popup(self):
        self.window.destroy()
        window.deiconify()

    def show_root_window(self):
        self.window.destroy()
        window.deiconify()

    def open_popup(self):
        window.withdraw()
        self.window = tk.Toplevel(window)
        self.window.title(self.title)
        self.window.config(padx=50, pady=50, bg=YELLOW)

        label = tk.Label(self.window, text=self.label_text, fg="black", bg=YELLOW,
                                  font=(FONT_COURIER, 20, "bold"))
        label.grid(column=0, row=0)

        self.entry_var = tk.StringVar()
        entry = tk.Entry(self.window, justify="center", font=bold_font, width=5, textvariable=self.entry_var)
        entry.grid(column=1, row=0)

        popup_digit_frame = tk.Frame(self.window, bg=YELLOW)
        popup_digit_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        for i in range(1, 10):
            button_text = str(i)
            if i <= 3:
                row_index = 2
            elif 3 < i <= 6:
                row_index = 1
            else:
                row_index = 0
            col_index = (i - 1) % 3
            button = tk.Button(popup_digit_frame, text=button_text,
                               command=lambda val=button_text: self.button_click(val),
                               font=(FONT_COURIER, 15, "bold"))
            button.grid(row=row_index, column=col_index, padx=5, pady=5)
        
        samplecnt_zero_button = tk.Button(popup_digit_frame, text="0",
                                          command=lambda val="0": self.button_click(val),
                                          font=(FONT_COURIER, 15, "bold"))
        samplecnt_zero_button.grid(row=3, column=0, padx=5, pady=5)
        
        samplecnt_dot_button = tk.Button(popup_digit_frame, text=".",
                                         command=lambda val=".": self.button_click(val),
                                         font=(FONT_COURIER, 15, "bold"))
        samplecnt_dot_button.grid(row=3, column=1, padx=5, pady=5)

        sample_action_frame = tk.Frame(self.window, bg=YELLOW)
        sample_action_frame.grid(row=1, column=3, columnspan=2, padx=10, pady=10)

        enter_button = tk.Button(sample_action_frame, text="✅ Enter", command=self.enter_popup,
                                 font=(FONT_COURIER, 15, "bold"), width=10, bg=GREEN)
        enter_button.grid(row=1, column=0, pady=5)

        backspace_button = tk.Button(sample_action_frame, text="🔙 Delete", command=self.backspace_delete,
                                     font=(FONT_COURIER, 15, "bold"), width=10, bg=PINK)
        backspace_button.grid(row=2, column=0, pady=5)

        cancel_button = tk.Button(sample_action_frame, text="❌ Esc", command=self.cancel_popup,
                                  font=(FONT_COURIER, 15, "bold"), width=10)
        cancel_button.grid(row=3, column=0, pady=5)

        self.window.protocol("WM_DELETE_WINDOW", self.show_root_window)
        self.window.mainloop()

# ------------------------------ CLASS INSTANTIATION ----------------------------------------------------------------- # 

# Popup window for sample count
samplecnt_popup = PopupWindow("Sample Count", "Sample Count", lambda: set_samplecnt_value(samplecnt_popup.value), 1, 12)

# Popup window for dilution Step
dilu_fac_popup = PopupWindow("Dilution Step", "Dilution Step", lambda: set_dilu_fac_value(dilu_fac_popup.value), 1, 7)

# Popup window for dilution ratio
dilu_rati_popup = PopupWindow("Dilution Ratio", "Dilution Ratio", lambda: set_dilu_rati_value(dilu_rati_popup.value), 1, 10)

def open_popup_samplecnt():
    samplecnt_popup.open_popup()

def open_popup_dilu_fac():
    dilu_fac_popup.open_popup()

def open_popup_dilu_rati():
    dilu_rati_popup.open_popup()

# Function to set sample count value
def set_samplecnt_value(value):
    global SAMPLE_VALUE
    SAMPLE_VALUE = str(int(value))
    #print("Updated Sample count = " + str(SAMPLE_VALUE)) # print updated global const
    samplecnt_entry.delete(0, tk.END)  # Clear the entry
    samplecnt_entry.insert(0, SAMPLE_VALUE)
    update_estimated_time()

# Function to set dilution Step value
def set_dilu_fac_value(value):
    global DILU_FAC_VALUE
    DILU_FAC_VALUE = str(int(value))
    #print("Updated dilution Step = " + str(DILU_FAC_VALUE)) # print updated global const
    dilu_fac_entry.delete(0, tk.END)  # Clear the entry
    dilu_fac_entry.insert(0, DILU_FAC_VALUE)  # Insert the dilution value
    update_estimated_time()

# Function to set dilution ratio value
def set_dilu_rati_value(value):
    global DILU_RATI_VALUE
    DILU_RATI_VALUE = str(int(value))
    #print("Updated Dilution Ratio = " + str(DILU_RATI_VALUE)) # print updated global const
    dilu_rati_entry.delete(0, tk.END)  # Clear the entry
    dilu_rati_entry.insert(0, DILU_RATI_VALUE)  # Insert the dilution value
        
# Function to check if all required values are set
def check_values_complete():
    return all((SAMPLE_VALUE, DILU_FAC_VALUE, DILU_RATI_VALUE))

def update_start_button_state():
    if check_values_complete():
        start_button.config(state="normal")
        print("✅Success: all input parameters set")
    else:
        start_button.config(state="disabled")
        
# -------------------------------- EMAIL MSG --------------------------------------------------- # 
def abort_all_button():
    #email_info_docks()
    window.after_cancel(timer)
    minutes = total_timer_seconds // 60
    seconds = total_timer_seconds % 60
    formatted_time = f"{minutes:02d}:{seconds:02d}"
    abort_button.config(state="disable")

# def email_info_docks():
#     count_min = str(canvas.itemcget(canvas_timer_value, "text").split(":")[0])
#     count_sec = str(canvas.itemcget(canvas_timer_value, "text").split(":")[1])
#     # Ensure count_min is represented as a single digit if it's between 0 and 9
#     if int(count_min) < 10:
#         count_min = str(int(count_min) % 10)  # Get the remainder when divided by 10
#     if int(count_sec) < 10:
#         count_sec = str(int(count_sec) % 10)
#     send_email("PaulCHeninus@gmail.com", "🚩Status~", count_min, count_sec, SAMPLE_VALUE, DILU_FAC_VALUE, DILU_RATI_VALUE)
#     print(f"Sampled count value: {count_min}:{count_sec}")
    


# -------------------------------- TIMER MECHANISM --------------------------------------------- # 
# Reset to re-enable Start Button
def enable_start_button():
    start_button.config(state="normal")
    window.after_cancel(timer)
    canvas.itemconfig(canvas_timer_value, text="00:00")
    global START_FLAG
    START_FLAG = 1  # Reset the start flag
    
    # start the timer
def start_timer():
    start_button.config(state="disabled")  # Disable Start button during break
    abort_button.config(state="normal")
    global total_timer_seconds
    count_down(total_timer_seconds)
    global START_FLAG
    START_FLAG = 1  # Reset the start flag
    #write_to_txt()   # click start and write to txt
 
# -------------------------------- TIMING ESTIMATION -------------------------------------------- #    
def update_estimated_time():
    try:
        sample_count = int(samplecnt_entry.get())
        dilution_factor = int(dilu_fac_entry.get())
        global total_timer_seconds
        total_timer_seconds = sample_count * dilution_factor * 156
        minutes = total_timer_seconds // 60
        seconds = total_timer_seconds % 60
        formatted_time = f"{minutes:02d}:{seconds:02d}"
        canvas.itemconfig(canvas_timer_value, text=formatted_time)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid integer values.")
    
    
# -------------------------------- COUNT_UP MECHANISM -------------------------------------------- # 
def count_down(time_remaining):
    if time_remaining >= 0:
        minutes = time_remaining // 60
        seconds = time_remaining % 60
        formatted_time = f"{minutes:02d}:{seconds:02d}"
        canvas.itemconfig(canvas_timer_value, text=formatted_time)
        global timer
        timer = window.after(1000, count_down, time_remaining - 1)
    else:
        start_button.config(state="normal")  # Re-enable start button when timer ends

    
# -------------------------------- main window action ---------------------------------------- # 
def clear_titer_parameter():
    samplecnt_entry.delete(0, tk.END)  # Clear all the entry
    dilu_fac_entry.delete(0, tk.END)
    dilu_rati_entry.delete(0,tk.END)
    start_button.config(state="disabled")
    global SAMPLE_VALUE, DILU_FAC_VALUE, DILU_RATI_VALUE
    SAMPLE_VALUE = DILU_FAC_VALUE = DILU_RATI_VALUE = None
    print("Clear Main Entry Values")
    
# -------------------------------- Subfunction another code ---------------------------------------- # 
# def write_to_txt():
#     try:
#         # Call the write_to_txt.py script and pass the variables as arguments
#         write_values_to_txt(SAMPLE_VALUE, DILU_FAC_VALUE, DILU_RATI_VALUE)
#         print("Values written to file successfully.")
#         # Check if the file exists after creation
#         if os.path.exists("values.txt"):
#             print("File exists.")
#         else:
#             print("File does not exist.")
#     except Exception as e:
#         print("Error:", e)


# ------------------------------------ UI SETUP ------------------------------------------------- #
# main window
window = tk.Tk()
window.title("Automatic Titer")
window.config(padx=100, pady=50, bg=YELLOW)
# custom font 
bold_font = tkFont.Font(weight="bold", size=20)    # it has to follow behind windw = tk.Tk()
# main window frames
title_label_frame = tk.Frame(window, bg=YELLOW)
title_label_frame.grid(column=0, row=0, columnspan=3)
main_entries_frame = tk.Frame(window, bg=YELLOW)
main_entries_frame.grid(column=0, row=1, columnspan=3)
# labels - main title & sample count & dilution ratio
title_label = tk.Label(title_label_frame, text="Automatic Titer Tool", fg="green", bg=YELLOW, font=(FONT_COURIER, 30, "bold"))
title_label.grid(column=0, row=0, columnspan=3)
pad_title_label = tk.Label(main_entries_frame, text="", fg="black", bg=YELLOW, font=(FONT_COURIER, 10))
pad_title_label.grid(column=0, row=0)
samplecnt_label = tk.Label(main_entries_frame, text="Sample Count", fg="black", bg=YELLOW, font=(FONT_COURIER, 20, "bold"))
samplecnt_label.grid(column=0, row=1)                                                                    # sample count label
pad_sam_dilu_label = tk.Label(main_entries_frame, text="", fg="black", bg=YELLOW, font=(FONT_COURIER, 10))
pad_sam_dilu_label.grid(column=0, row=2)
dilu_fac_label = tk.Label(main_entries_frame, text="Dilution Step", fg="black", bg=YELLOW, font=(FONT_COURIER, 20, "bold"))
dilu_fac_label.grid(column=0, row=3)
pad_fac_rati_label = tk.Label(main_entries_frame, text="", fg="black", bg=YELLOW, font=(FONT_COURIER, 10))
pad_fac_rati_label.grid(column=0, row=4)
dilu_rati_label = tk.Label(main_entries_frame, text="Dilution Ratio", fg="black", bg=YELLOW, font=(FONT_COURIER, 20, "bold"))
dilu_rati_label.grid(column=0, row=5)

#  📥 entry box
samplecnt_entry = tk.Entry(main_entries_frame, justify="center", font=bold_font, width=15)
samplecnt_entry.grid(column=1, row=1)
samplecnt_entry.insert(0, SAMPLE_VALUE)                                                 # default entry box value 
dilu_fac_entry  = tk.Entry(main_entries_frame, justify="center", font=bold_font, width=15)
dilu_fac_entry.grid(column=1, row=3)
dilu_fac_entry.insert(0,DILU_FAC_VALUE)
dilu_rati_entry = tk.Entry(main_entries_frame, justify="center", font=bold_font, width=15)
dilu_rati_entry.grid(column=1, row=5)
dilu_rati_entry.insert(0, DILU_RATI_VALUE)
set_samplecnt_button = tk.Button(main_entries_frame, text="Set", fg="black", bg=CYAN_GRE, font=(FONT_COURIER, 15, "bold"), command=open_popup_samplecnt)
set_samplecnt_button.grid(column=3, row=1)
set_dilu_fac_button = tk.Button(main_entries_frame, text="Set", fg="black", bg=GRE_BLU, font=(FONT_COURIER, 15, "bold"), command=open_popup_dilu_fac)
set_dilu_fac_button.grid(column=3, row=3)
set_dilu_rati_button = tk.Button(main_entries_frame, text="Set", fg="black", bg=PINK, font=(FONT_COURIER, 15, "bold"), command=open_popup_dilu_rati)
set_dilu_rati_button.grid(column=3, row=5)
# canvas image
canvas_frame = tk.Frame(window, bg=YELLOW)
canvas_frame.grid(row=1, column=3, columnspan=3, padx=50, pady=50)
canvas = tk.Canvas(canvas_frame, width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = tk.PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image= tomato_img)  # specify the x,y value using half of the canvas width height 200, 224 divide by 2
canvas_timer_value = canvas.create_text(103,130, text="00:00", fill="white", font=(FONT_COURIER, 35, "bold"))
canvas.grid(column=4, row=5)
# create main window frame for action buttons
main_action_frame = tk.Frame(window, bg=YELLOW)
main_action_frame.grid(column=0, row=2, columnspan=3)
# buttons
start_button = tk.Button(main_action_frame, text="Start", font=("Courier", 20, "bold"), highlightthickness=1, command=start_timer, bg= GREEN)
reset_button = tk.Button(main_action_frame, text="Reset", font=("Courier", 20, "bold"), highlightthickness=0, command=enable_start_button)
clear_button = tk.Button(main_action_frame, text="Clear", font=("Courier", 20, "bold"), highlightthickness=0, command=clear_titer_parameter)
abort_button = tk.Button(main_action_frame, text="Abort", font=("Courier", 20, "bold"), highlightthickness=0, command=abort_all_button, bg= RED)
start_button.grid(column=0, row=0, pady=5)
reset_button.grid(column=0, row=1, pady=5)
clear_button.grid(column=0, row=2, pady=5)
abort_button.grid(column=1, row=0, padx=10, pady=5)

# working code, but it needs input constraint so the user only enter valid values

import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont
import math
import os
#from write_to_txt import write_values_to_txt
#from email_notification_ver2 import send_email
START_FLAG = 0
# Constants
PINK = "#FF5BAE"
RED = "#e7305b"
GREEN = "#9bdeac"
CYAN_GRE = "#4CCD99"
GRE_BLU = "#41C9E2"
YELLOW = "#f7f5dd"
FONT_COURIER = "Courier"
SAMPLE_VALUE = str(int(1))
DILU_FAC_VALUE = str(int(1))
DILU_RATI_VALUE = str(int(2))


# ---------------------------- CLASS FOR POPUP WINDOW ------------------------------------------- # 

class PopupWindow:
    def __init__(self, title, label_text, confirm_command, min_value, max_value):
        self.title = title
        self.label_text = label_text
        self.confirm_command = confirm_command
        self.min_value = min_value
        self.max_value = max_value
        self.value = None
        self.window = None

    def button_click(self, value):
        self.entry_var.set(self.entry_var.get() + value)

    def enter_popup(self):
        self.value = self.entry_var.get()
        if self.value.strip() == "":
            tk.messagebox.showerror("No Value Entered", "Please enter a value.")
            return
        if not self.value.isdigit():
            messagebox.showerror("Invalid Input", "Only integers are allowed.")
            return
        if self.validate_input(self.value):
            self.confirm_command()
            self.window.destroy()
            window.deiconify()
            update_start_button_state()  # when enter clicked, check if all parameters changed

    def validate_input(self, value):
        try:
            numeric_value = float(value)
            if self.min_value <= numeric_value <= self.max_value:
                return True
            else:
                raise ValueError
        except ValueError:
            tk.messagebox.showerror("Invalid Input", f"Please enter a valid value between {self.min_value} and {self.max_value}")
            return False
        
    def backspace_delete(self):
        self.entry_var.set(self.entry_var.get()[:-1])

    def cancel_popup(self):
        self.window.destroy()
        window.deiconify()

    def show_root_window(self):
        self.window.destroy()
        window.deiconify()

    def open_popup(self):
        window.withdraw()
        self.window = tk.Toplevel(window)
        self.window.title(self.title)
        self.window.config(padx=50, pady=50, bg=YELLOW)

        label = tk.Label(self.window, text=self.label_text, fg="black", bg=YELLOW,
                                  font=(FONT_COURIER, 20, "bold"))
        label.grid(column=0, row=0)

        self.entry_var = tk.StringVar()
        entry = tk.Entry(self.window, justify="center", font=bold_font, width=5, textvariable=self.entry_var)
        entry.grid(column=1, row=0)

        popup_digit_frame = tk.Frame(self.window, bg=YELLOW)
        popup_digit_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        for i in range(1, 10):
            button_text = str(i)
            if i <= 3:
                row_index = 2
            elif 3 < i <= 6:
                row_index = 1
            else:
                row_index = 0
            col_index = (i - 1) % 3
            button = tk.Button(popup_digit_frame, text=button_text,
                               command=lambda val=button_text: self.button_click(val),
                               font=(FONT_COURIER, 15, "bold"))
            button.grid(row=row_index, column=col_index, padx=5, pady=5)
        
        samplecnt_zero_button = tk.Button(popup_digit_frame, text="0",
                                          command=lambda val="0": self.button_click(val),
                                          font=(FONT_COURIER, 15, "bold"))
        samplecnt_zero_button.grid(row=3, column=0, padx=5, pady=5)
        
        samplecnt_dot_button = tk.Button(popup_digit_frame, text=".",
                                         command=lambda val=".": self.button_click(val),
                                         font=(FONT_COURIER, 15, "bold"))
        samplecnt_dot_button.grid(row=3, column=1, padx=5, pady=5)

        sample_action_frame = tk.Frame(self.window, bg=YELLOW)
        sample_action_frame.grid(row=1, column=3, columnspan=2, padx=10, pady=10)

        enter_button = tk.Button(sample_action_frame, text="✅ Enter", command=self.enter_popup,
                                 font=(FONT_COURIER, 15, "bold"), width=10, bg=GREEN)
        enter_button.grid(row=1, column=0, pady=5)

        backspace_button = tk.Button(sample_action_frame, text="🔙 Delete", command=self.backspace_delete,
                                     font=(FONT_COURIER, 15, "bold"), width=10, bg=PINK)
        backspace_button.grid(row=2, column=0, pady=5)

        cancel_button = tk.Button(sample_action_frame, text="❌ Esc", command=self.cancel_popup,
                                  font=(FONT_COURIER, 15, "bold"), width=10)
        cancel_button.grid(row=3, column=0, pady=5)

        self.window.protocol("WM_DELETE_WINDOW", self.show_root_window)
        self.window.mainloop()

# ------------------------------ CLASS INSTANTIATION ----------------------------------------------------------------- # 

# Popup window for sample count
samplecnt_popup = PopupWindow("Sample Count", "Sample Count", lambda: set_samplecnt_value(samplecnt_popup.value), 1, 12)

# Popup window for dilution Step
dilu_fac_popup = PopupWindow("Dilution Step", "Dilution Step", lambda: set_dilu_fac_value(dilu_fac_popup.value), 1, 7)

# Popup window for dilution ratio
dilu_rati_popup = PopupWindow("Dilution Ratio", "Dilution Ratio", lambda: set_dilu_rati_value(dilu_rati_popup.value), 1, 10)

def open_popup_samplecnt():
    samplecnt_popup.open_popup()

def open_popup_dilu_fac():
    dilu_fac_popup.open_popup()

def open_popup_dilu_rati():
    dilu_rati_popup.open_popup()

# Function to set sample count value
def set_samplecnt_value(value):
    global SAMPLE_VALUE
    SAMPLE_VALUE = str(int(value))
    #print("Updated Sample count = " + str(SAMPLE_VALUE)) # print updated global const
    samplecnt_entry.delete(0, tk.END)  # Clear the entry
    samplecnt_entry.insert(0, SAMPLE_VALUE)

# Function to set dilution Step value
def set_dilu_fac_value(value):
    global DILU_FAC_VALUE
    DILU_FAC_VALUE = str(int(value))
    #print("Updated dilution Step = " + str(DILU_FAC_VALUE)) # print updated global const
    dilu_fac_entry.delete(0, tk.END)  # Clear the entry
    dilu_fac_entry.insert(0, DILU_FAC_VALUE)  # Insert the dilution value

# Function to set dilution ratio value
def set_dilu_rati_value(value):
    global DILU_RATI_VALUE
    DILU_RATI_VALUE = str(int(value))
    #print("Updated Dilution Ratio = " + str(DILU_RATI_VALUE)) # print updated global const
    dilu_rati_entry.delete(0, tk.END)  # Clear the entry
    dilu_rati_entry.insert(0, DILU_RATI_VALUE)  # Insert the dilution value
        
# Function to check if all required values are set
def check_values_complete():
    return all((SAMPLE_VALUE, DILU_FAC_VALUE, DILU_RATI_VALUE))

def update_start_button_state():
    if check_values_complete():
        start_button.config(state="normal")
        print("✅Success: all input parameters set")
    else:
        start_button.config(state="disabled")
        
# -------------------------------- EMAIL MSG --------------------------------------------------- # 
def abort_all_button():
    #email_info_docks()
    window.after_cancel(timer)
    canvas.itemconfig(canvas_timer_value, text="00:00")
    abort_button.config(state="disable")

# def email_info_docks():
#     count_min = str(canvas.itemcget(canvas_timer_value, "text").split(":")[0])
#     count_sec = str(canvas.itemcget(canvas_timer_value, "text").split(":")[1])
#     # Ensure count_min is represented as a single digit if it's between 0 and 9
#     if int(count_min) < 10:
#         count_min = str(int(count_min) % 10)  # Get the remainder when divided by 10
#     if int(count_sec) < 10:
#         count_sec = str(int(count_sec) % 10)
#     send_email("PaulCHeninus@gmail.com", "🚩Status~", count_min, count_sec, SAMPLE_VALUE, DILU_FAC_VALUE, DILU_RATI_VALUE)
#     print(f"Sampled count value: {count_min}:{count_sec}")
    


# -------------------------------- TIMER MECHANISM --------------------------------------------- # 
# Reset to re-enable Start Button
def enable_start_button():
    start_button.config(state="normal")
    window.after_cancel(timer)
    canvas.itemconfig(canvas_timer_value, text="00:00")
    global START_FLAG
    START_FLAG = 1  # Reset the start flag
    
    # start the timer
def start_timer():
    start_button.config(state="disabled")  # Disable Start button during break
    abort_button.config(state="normal")
    count_up(0)
    global START_FLAG
    START_FLAG = 1  # Reset the start flag
    #write_to_txt()   # click start and write to txt
    
# -------------------------------- COUNT_UP MECHANISM -------------------------------------------- # 
def count_up(count):
    count_min = math.floor(count/60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    if count_min < 10:
        count_min = f"0{count_min}"
    canvas.itemconfig(canvas_timer_value, text=f"{count_min}:{count_sec}")
    #print(count)
    global timer
    timer = window.after(1000, count_up, count+1)
    
# -------------------------------- main window action ---------------------------------------- # 
def clear_titer_parameter():
    samplecnt_entry.delete(0, tk.END)  # Clear all the entry
    dilu_fac_entry.delete(0, tk.END)
    dilu_rati_entry.delete(0,tk.END)
    start_button.config(state="disabled")
    global SAMPLE_VALUE, DILU_FAC_VALUE, DILU_RATI_VALUE
    SAMPLE_VALUE = DILU_FAC_VALUE = DILU_RATI_VALUE = None
    print("Clear Main Entry Values")
    
# -------------------------------- Subfunction another code ---------------------------------------- # 
# def write_to_txt():
#     try:
#         # Call the write_to_txt.py script and pass the variables as arguments
#         write_values_to_txt(SAMPLE_VALUE, DILU_FAC_VALUE, DILU_RATI_VALUE)
#         print("Values written to file successfully.")
#         # Check if the file exists after creation
#         if os.path.exists("values.txt"):
#             print("File exists.")
#         else:
#             print("File does not exist.")
#     except Exception as e:
#         print("Error:", e)


# ------------------------------------ UI SETUP ------------------------------------------------- #
# main window
window = tk.Tk()
window.title("Automatic Titer")
window.config(padx=100, pady=50, bg=YELLOW)
# custom font 
bold_font = tkFont.Font(weight="bold", size=20)    # it has to follow behind windw = tk.Tk()
# main window frames
title_label_frame = tk.Frame(window, bg=YELLOW)
title_label_frame.grid(column=0, row=0, columnspan=3)
main_entries_frame = tk.Frame(window, bg=YELLOW)
main_entries_frame.grid(column=0, row=1, columnspan=3)
# labels - main title & sample count & dilution ratio
title_label = tk.Label(title_label_frame, text="Automatic Titer Tool", fg="green", bg=YELLOW, font=(FONT_COURIER, 30, "bold"))
title_label.grid(column=0, row=0, columnspan=3)
pad_title_label = tk.Label(main_entries_frame, text="", fg="black", bg=YELLOW, font=(FONT_COURIER, 10))
pad_title_label.grid(column=0, row=0)
samplecnt_label = tk.Label(main_entries_frame, text="Sample Count", fg="black", bg=YELLOW, font=(FONT_COURIER, 20, "bold"))
samplecnt_label.grid(column=0, row=1)                                                                    # sample count label
pad_sam_dilu_label = tk.Label(main_entries_frame, text="", fg="black", bg=YELLOW, font=(FONT_COURIER, 10))
pad_sam_dilu_label.grid(column=0, row=2)
dilu_fac_label = tk.Label(main_entries_frame, text="Dilution Step", fg="black", bg=YELLOW, font=(FONT_COURIER, 20, "bold"))
dilu_fac_label.grid(column=0, row=3)
pad_fac_rati_label = tk.Label(main_entries_frame, text="", fg="black", bg=YELLOW, font=(FONT_COURIER, 10))
pad_fac_rati_label.grid(column=0, row=4)
dilu_rati_label = tk.Label(main_entries_frame, text="Dilution Ratio", fg="black", bg=YELLOW, font=(FONT_COURIER, 20, "bold"))
dilu_rati_label.grid(column=0, row=5)

#  📥 entry box
samplecnt_entry = tk.Entry(main_entries_frame, justify="center", font=bold_font, width=15)
samplecnt_entry.grid(column=1, row=1)
samplecnt_entry.insert(0, SAMPLE_VALUE)                                                 # default entry box value 
dilu_fac_entry  = tk.Entry(main_entries_frame, justify="center", font=bold_font, width=15)
dilu_fac_entry.grid(column=1, row=3)
dilu_fac_entry.insert(0,DILU_FAC_VALUE)
dilu_rati_entry = tk.Entry(main_entries_frame, justify="center", font=bold_font, width=15)
dilu_rati_entry.grid(column=1, row=5)
dilu_rati_entry.insert(0, DILU_RATI_VALUE)
set_samplecnt_button = tk.Button(main_entries_frame, text="Set", fg="black", bg=CYAN_GRE, font=(FONT_COURIER, 15, "bold"), command=open_popup_samplecnt)
set_samplecnt_button.grid(column=3, row=1)
set_dilu_fac_button = tk.Button(main_entries_frame, text="Set", fg="black", bg=GRE_BLU, font=(FONT_COURIER, 15, "bold"), command=open_popup_dilu_fac)
set_dilu_fac_button.grid(column=3, row=3)
set_dilu_rati_button = tk.Button(main_entries_frame, text="Set", fg="black", bg=PINK, font=(FONT_COURIER, 15, "bold"), command=open_popup_dilu_rati)
set_dilu_rati_button.grid(column=3, row=5)
# canvas image
canvas_frame = tk.Frame(window, bg=YELLOW)
canvas_frame.grid(row=1, column=3, columnspan=3, padx=50, pady=50)
canvas = tk.Canvas(canvas_frame, width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = tk.PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image= tomato_img)  # specify the x,y value using half of the canvas width height 200, 224 divide by 2
canvas_timer_value = canvas.create_text(103,130, text="00:00", fill="white", font=(FONT_COURIER, 35, "bold"))
canvas.grid(column=4, row=5)
# create main window frame for action buttons
main_action_frame = tk.Frame(window, bg=YELLOW)
main_action_frame.grid(column=0, row=2, columnspan=3)
# buttons
start_button = tk.Button(main_action_frame, text="Start", font=("Courier", 20, "bold"), highlightthickness=1, command=start_timer, bg= GREEN)
reset_button = tk.Button(main_action_frame, text="Reset", font=("Courier", 20, "bold"), highlightthickness=0, command=enable_start_button)
clear_button = tk.Button(main_action_frame, text="Clear", font=("Courier", 20, "bold"), highlightthickness=0, command=clear_titer_parameter)
abort_button = tk.Button(main_action_frame, text="Abort", font=("Courier", 20, "bold"), highlightthickness=0, command=abort_all_button, bg= RED)
start_button.grid(column=0, row=0, pady=5)
reset_button.grid(column=0, row=1, pady=5)
clear_button.grid(column=0, row=2, pady=5)
abort_button.grid(column=1, row=0, padx=10, pady=5)

window.mainloop()
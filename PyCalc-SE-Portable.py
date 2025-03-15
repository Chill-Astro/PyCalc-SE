import customtkinter as ctk
import math
import os
class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PyCalc - SE - Portable")
        self.root.geometry("300x425")
        root.resizable(False, False)
        
        self.result_var = ctk.StringVar()
        self.result_var.set("0")
        
        self.create_widgets()
        self.setup_keymaps()
    
    def create_widgets(self):
        # Result display
        result_frame = ctk.CTkFrame(self.root)
        result_frame.pack(fill="x", padx=10, pady=10)
        
        result_label = ctk.CTkLabel(result_frame, textvariable=self.result_var, font=("Arial", 36), anchor="e")
        result_label.pack(fill="x", pady=10)
        
        # Buttons
        buttons_frame = ctk.CTkFrame(self.root)
        buttons_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        buttons = [
            ('C','x²', '±', '⌫'),  
            ('x!', '³√x', '√x', '÷'),  
            ('7', '8', '9', '×'),      
            ('4', '5', '6', '-'),      
            ('1', '2', '3', '+'),      
            ('xⁿ', '0', '.', '=')      
        ]
        
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                button = ctk.CTkButton(buttons_frame, text=text, width=60, height=45, command=lambda t=text: self.on_button_click(t))  # Larger buttons
                button.grid(row=i, column=j, padx=5, pady=5)
    
    def on_button_click(self, text):
        current_text = self.result_var.get()
        
        if text == 'C':
            self.result_var.set("0")  # Clear all
        elif text == '⌫':  # Backspace
            self.on_backspace()
        elif text == '±':  # Toggle sign
            try:
                if current_text != "0" and current_text != "Error":
                    if current_text[0] == '-':
                        self.result_var.set(current_text[1:])  # Remove negative sign
                    else:
                        self.result_var.set('-' + current_text)  # Add negative sign
            except:
                self.result_var.set("Error")
        elif text == '√x':  # Square root
            try:
                result = str(math.sqrt(float(current_text)))
                self.result_var.set(result)
            except:
                self.result_var.set("Error")
        elif text == '³√x':  # Cube root
            try:
                result = str(round(float(current_text) ** (1/3), 8))
                self.result_var.set(result)
            except:
                self.result_var.set("Error")
        elif text == 'x²':  # Square
            try:
                result = str(float(current_text) ** 2)
                self.result_var.set(result)
            except:
                self.result_var.set("Error")
        elif text == 'xⁿ':  # Power functionality
            self.result_var.set(current_text + '^')  # Use '^' for power
        elif text == '=':
            try:
                # Replace '^' with '**' for evaluation
                expression = current_text.replace('^', '**').replace('×', '*').replace('÷', '/')
                result = str(eval(expression))
                self.result_var.set(result)
            except:
                self.result_var.set("Error")
        else:
            if current_text == "0" or current_text == "Error":
                self.result_var.set(text)
            else:
                self.result_var.set(current_text + text)
    
    def setup_keymaps(self):
        # Map keys to calculator functions
        self.root.bind('<Key>', self.on_key_press)
    
    def on_key_press(self, event):
        key = event.char
        if key in '0123456789':
            self.on_button_click(key)
        elif key == '+':
            self.on_button_click('+')
        elif key == '-':
            self.on_button_click('-')
        elif key == '*':
            self.on_button_click('×')
        elif key == '/':
            self.on_button_click('÷')
        elif key == '.':
            self.on_button_click('.')
        elif key == '=' or key == '\r':  # Enter key
            self.on_button_click('=')
        elif key == '\x08':  # Backspace key
            self.on_backspace()
        elif key == '^':  # Power key
            self.on_button_click('xⁿ')
        elif key == 'c':  # Clear key
            self.on_button_click('C')
        elif key == '_' or key == '-':  # Toggle sign key
            self.on_button_click('±')

    def on_backspace(self):
        current_text = self.result_var.get()
        if current_text != "0" and current_text != "Error":
            new_text = current_text[:-1] if len(current_text) > 1 else "0"
            self.result_var.set(new_text)

if __name__ == "__main__":
    root = ctk.CTk()
    app = CalculatorApp(root)
    root.mainloop()
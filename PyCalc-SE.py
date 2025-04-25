#!/usr/bin/env python3
import customtkinter as ctk
import math
import os
CURRENT_VERSION = "1.2" # Linux Release + Improved Linux & MacOS Support
class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PyCalc - Simple Edition")
        self.root.geometry("320x480")
        self.root.resizable(False, False)
        self.expression_history = ""
        self.current_input = "0"
        self.full_expression = ""
        self.result_pending = False

        self._currentNumber = 0.0
        self._previousNumber = 0.0
        self._currentOperator = ""
        self._isNewNumberInput = True
        self._hasDecimal = False

        # --- StringVars for Display ---
        self.history_var = ctk.StringVar()
        self.result_var = ctk.StringVar()
        self.history_var.set("")
        self.result_var.set("0")

        # --- Configure Root Grid ---
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1) # Display Frame (less weight)
        self.root.grid_rowconfigure(1, weight=5) # Buttons Frame (more weight)

        self.create_widgets()
        self.setup_keymaps()

    def create_widgets(self):
        display_frame = ctk.CTkFrame(self.root, corner_radius=7, fg_color="#2b2b2b", border_width=0, border_color="#505050")
        display_frame.grid(row=0, column=0, sticky="nsew", padx=6.2, pady=6.2)
        display_frame.grid_columnconfigure(0, weight=1)
        display_frame.grid_rowconfigure(0, weight=1) # History row
        display_frame.grid_rowconfigure(1, weight=2) # Result row (more weight)

        # History Display (Top Line)
        self.history_label = ctk.CTkLabel(
            display_frame,
            textvariable=self.history_var,
            font=("", 14),
            anchor="se",
            text_color="gray"
        )
        self.history_label.grid(row=0, column=0, sticky="sew", padx=10, pady=(6, 0))

        # Result Display (Bottom Line)
        self.result_label = ctk.CTkLabel(
            display_frame,
            textvariable=self.result_var,
            font=("", 38, "bold"),
            anchor="se"
        )
        self.result_label.grid(row=1, column=0, sticky="sew", padx=10, pady=(0, 10))

        # --- Buttons Frame ---
        buttons_frame = ctk.CTkFrame(self.root, corner_radius=0)
        buttons_frame.grid(row=1, column=0, sticky="nsew", padx=1, pady=1)

        # Configure button grid weights for equal spacing
        for i in range(6): # Rows
            buttons_frame.grid_rowconfigure(i, weight=1)
        for j in range(4): # Columns
            buttons_frame.grid_columnconfigure(j, weight=1)

        # Button layout with xʸ restored
        buttons = [
            ('xʸ','CE', 'C', '⌫'),
            ('x²', 'x³', '√x','÷'),
            ('7', '8', '9', '×'),
            ('4', '5', '6','-'),
            ('1', '2', '3','+'),
            ('+/-', '0', '.', '=')
        ]
        # Define button colors
        num_fg_color = "#ffffff"
        num_bg_color = "#505050"
        num_hover_color = "#6a6a6a"

        op_fg_color = "#ffffff"
        op_bg_color = "#3b3b3b"
        op_hover_color = "#5a5a5a"

        eq_fg_color = "#ffffff"
        eq_bg_color = "#77b6ea"
        eq_hover_color = "#8bc4f0"

        button_padx = 2
        button_pady = 2

        for i, row in enumerate(buttons):
            for j, text in enumerate(row):                    
                fg_color=num_fg_color
                bg_color=num_bg_color
                hover_color=num_hover_color
                font_size = 16

                if text in ['÷', '×', '-', '+', 'xʸ']:
                    bg_color=op_bg_color
                    hover_color=op_hover_color
                    font_size = 20
                elif text in ['CE', 'C', '⌫', 'x²', 'x³', '√x', '+/-']:
                    bg_color=op_bg_color
                    hover_color=op_hover_color
                    if text == '⌫': font_size = 16
                elif text == '=':
                    bg_color=eq_bg_color
                    fg_color=eq_fg_color
                    hover_color=eq_hover_color
                    font_size = 22
                elif text in ['1','2','3','4','5','6','7','8','9','0','.']:
                    bg_color=op_bg_color

                button = ctk.CTkButton(
                    buttons_frame,
                    text=text,
                    font=("", font_size),
                    command=lambda t=text: self.on_button_click(t),
                    fg_color=bg_color,
                    hover_color=hover_color,
                    text_color=fg_color,
                    corner_radius=5
                )
                button.grid(row=i, column=j, padx=button_padx, pady=button_pady, sticky="nsew")

    def setup_keymaps(self):
        """Sets up keyboard bindings."""
        self.root.bind('<Key>', self.handle_key_press)
        self.root.bind('<Return>', lambda event: self.on_button_click('='))
        self.root.bind('<BackSpace>', lambda event: self.on_button_click('⌫'))
        self.root.bind('<KP_Enter>', lambda event: self.on_button_click('='))
        self.root.bind('<KP_Decimal>', lambda event: self.on_button_click('.'))
        self.root.bind('<KP_Add>', lambda event: self.on_button_click('+'))
        self.root.bind('<KP_Subtract>', lambda event: self.on_button_click('-'))
        self.root.bind('<KP_Multiply>', lambda event: self.on_button_click('×'))
        self.root.bind('<KP_Divide>', lambda event: self.on_button_click('÷'))
        self.root.bind('<Delete>', lambda event: self.on_button_click('CE'))
        for i in range(10):
            self.root.bind(f'<KP_{i}>', lambda event, num=str(i): self.on_button_click(num))

    def handle_key_press(self, event):
        """Handles keyboard input."""
        key = event.char
        keysym = event.keysym

        # Skip if already handled by specific bindings
        if keysym in ['Return', 'BackSpace', 'KP_Enter', 'Delete'] or keysym.startswith('KP_'):
            return

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
        elif key == '^': 
            self.on_button_click('xʸ')
        elif key.lower() == 'c':
            if not (event.state & 0x0004): # Not Ctrl+C
                self.on_button_click('C')
        elif key == '=': 
            self.on_button_click('=')

    def update_display(self):
        """Updates the display with current values."""
        if isinstance(self._currentNumber, float):
            # Check if the float is actually an integer
            if self._currentNumber.is_integer() and not self._hasDecimal:
                display_value = str(int(self._currentNumber))
            else:
                display_value = str(self._currentNumber)
        else:
            display_value = str(self._currentNumber)
        
        self.result_var.set(display_value)
        self.history_var.set(self.expression_history)

    def clear_all(self):
        """Resets the calculator state."""
        self.current_input = "0"
        self.expression_history = ""
        self.full_expression = ""
        self.result_pending = False
        self._currentNumber = 0.0
        self._previousNumber = 0.0
        self._currentOperator = ""
        self._isNewNumberInput = True
        self._hasDecimal = False
        self.update_display()

    def clear_entry(self):
        """Clears the current input."""
        self.current_input = "0"
        self._currentNumber = 0.0
        self._isNewNumberInput = True
        self._hasDecimal = False
        self.update_display()

    def backspace(self):
        """Handles backspace action."""
        if self.result_pending:
            return
        
        current_str = str(self._currentNumber)
        if '.' in current_str:
            parts = current_str.split('.')
            if len(parts[0]) > 1:
                new_str = parts[0][:-1] + ('.' + parts[1] if parts[1] else '')
            else:
                new_str = '0' + ('.' + parts[1] if parts[1] else '')
            try:
                self._currentNumber = float(new_str)
                self._hasDecimal = '.' in new_str
            except ValueError:
                self._currentNumber = 0.0
                self._hasDecimal = False
        else:
            if len(current_str) > 1:
                self._currentNumber = int(current_str[:-1])
            else:
                self._currentNumber = 0.0
            self._hasDecimal = False
        
        self._isNewNumberInput = False
        self.update_display()

    def input_digit(self, digit):
        if self.result_pending:
            self._currentNumber = int(digit)
            self.expression_history = ""
            self.full_expression = ""
            self.result_pending = False
            self._isNewNumberInput = False
            self._hasDecimal = False
        elif self._isNewNumberInput or self._currentNumber == 0:
            if self._hasDecimal:
                self._currentNumber = float(f"0.{digit}")
            else:
                self._currentNumber = int(digit)
            self._isNewNumberInput = False
        else:
            current_str = str(self._currentNumber)
            if self._hasDecimal:
                if '.' in current_str:
                    self._currentNumber = float(current_str + digit)
                else:
                    self._currentNumber = float(current_str + '.' + digit)
            else:
                self._currentNumber = float(current_str + digit) if '.' in current_str else int(current_str + digit)
        self.update_display()

    def input_decimal(self):
        """Handles decimal point input."""
        if self.result_pending:
            self._currentNumber = 0.0
            self.expression_history = ""
            self.full_expression = ""
            self.result_pending = False
            self._isNewNumberInput = False
            self._hasDecimal = True
        
        if not self._hasDecimal:
            self._hasDecimal = True
            current_str = str(self._currentNumber)
            if '.' not in current_str:
                self._currentNumber = float(current_str + '.')
            self._isNewNumberInput = False
            self.update_display()

    def input_operator(self, op):
        """Handles binary operators."""
        if not self._currentNumber and op != '-':
            return

        if not self._isNewNumberInput:
            if self._currentOperator:
                self.calculate_intermediate_result()
            else:
                self._previousNumber = self._currentNumber

        visual_op = op.replace('**', '^').replace('*', '×').replace('/', '÷')
        self.expression_history = f"{self._previousNumber} {visual_op} "
        self._currentOperator = op
        self._isNewNumberInput = True
        self._hasDecimal = False
        self.update_display()

    def calculate_intermediate_result(self):
        if self._currentOperator:
            try:
                if self._currentOperator == '+':
                    result = self._previousNumber + self._currentNumber
                elif self._currentOperator == '-':
                    result = self._previousNumber - self._currentNumber
                elif self._currentOperator == '*':
                    result = self._previousNumber * self._currentNumber
                elif self._currentOperator == '/':
                    if self._currentNumber == 0:
                        self._currentNumber = "Error"
                        self.expression_history = ""
                        self._previousNumber = 0
                        self._currentOperator = ""
                        self._isNewNumberInput = True
                        self.result_pending = False
                        self._hasDecimal = False
                        self.update_display()
                        return
                    result = self._previousNumber / self._currentNumber
                
                if isinstance(result, float) and result.is_integer() and not self._hasDecimal:
                    self._currentNumber = int(result)
                else:
                    self._currentNumber = result
                
                self._previousNumber = self._currentNumber
                self._isNewNumberInput = True
                self._hasDecimal = False
                self.update_display()
            except Exception:
                self.handle_calculation_error()

    def calculate_result(self):
        """Handles the equals operation."""
        if self.result_pending or not self._currentOperator:
            return

        second_number = self._currentNumber
        try:
            if self._currentOperator == '+':
                result = self._previousNumber + second_number
            elif self._currentOperator == '-':
                result = self._previousNumber - second_number
            elif self._currentOperator == '*':
                result = self._previousNumber * second_number
            elif self._currentOperator == '/':
                if second_number == 0:
                    self._currentNumber = "Error"
                    self.expression_history = ""
                    self._previousNumber = 0
                    self._currentOperator = ""
                    self._isNewNumberInput = True
                    self.result_pending = False
                    self._hasDecimal = False
                    self.update_display()
                    return
                result = self._previousNumber / second_number
            elif self._currentOperator == '**':
                result = self._previousNumber ** second_number

            if isinstance(result, float) and result.is_integer() and not self._hasDecimal:
                self._currentNumber = int(result)
            else:
                self._currentNumber = result

            self.expression_history = f"{self._previousNumber} {self.get_visual_operator(self._currentOperator)} {second_number} ="
            self.result_pending = True
            self._isNewNumberInput = True
            self._currentOperator = ""
            self._previousNumber = self._currentNumber
            self._hasDecimal = False
            self.update_display()

        except Exception:
            self.handle_calculation_error()

    def handle_calculation_error(self):
        """Handles any calculation errors uniformly."""
        self._currentNumber = "Error"
        self.expression_history = ""
        self._previousNumber = 0
        self._currentOperator = ""
        self._isNewNumberInput = True
        self.result_pending = False
        self._hasDecimal = False
        self.update_display()

    def get_visual_operator(self, op):
        return op.replace('**', '^').replace('*', '×').replace('/', '÷')

    def toggle_sign(self):
        """Toggles the sign of the current number."""
        self._currentNumber = -self._currentNumber
        self.update_display()

    def calculate_square_root(self):
        """Calculates square root with double precision."""
        try:
            num = float(self._currentNumber)
            if num < 0:
                self._currentNumber = "Error"
                self.expression_history = f"√({num})"
            else:
                result = math.sqrt(num)
                if result.is_integer() and not self._hasDecimal:
                    self._currentNumber = int(result)
                else:
                    self._currentNumber = result
                self.expression_history = f"√({num})"
            self.update_display()
        except (ValueError, TypeError):
            self.handle_calculation_error()

    def calculate_cube(self):
        """Calculates cube of the current number."""
        try:
            num = float(self._currentNumber)
            result = num ** 3
            if result.is_integer() and not self._hasDecimal:
                self._currentNumber = int(result)
            else:
                self._currentNumber = result
            self.expression_history = f"cube({num})"
            self.update_display()
        except (ValueError, TypeError):
            self.handle_calculation_error()

    def calculate_square(self):
        """Calculates square of the current number."""
        try:
            num = float(self._currentNumber)
            result = num ** 2
            if result.is_integer() and not self._hasDecimal:
                self._currentNumber = int(result)
            else:
                self._currentNumber = result
            self.expression_history = f"sqr({num})"
            self.update_display()
        except (ValueError, TypeError):
            self.handle_calculation_error()

    def on_button_click(self, text):
        """Main button click handler."""
        if text in '0123456789':
            self.input_digit(text)
        elif text == '.':
            self.input_decimal()
        elif text in '+-×÷':
            op_map = {'+': '+', '-': '-', '×': '*', '÷': '/'}
            self.input_operator(op_map[text])
        elif text == '+/-':
            self.toggle_sign()
        elif text == 'x²':
            self.calculate_square()
        elif text == 'x³':
            self.calculate_cube()
        elif text == '√x':
            self.calculate_square_root()
        elif text == 'xʸ':
            self.input_operator('**')
        elif text == '=':
            self.calculate_result()
        elif text == 'C':
            self.clear_all()
        elif text == 'CE':
            self.clear_entry()
        elif text == '⌫':
            self.backspace()

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    app = CalculatorApp(root)
    icon_path = os.path.join(".", "Pycalc-SE.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
    root.mainloop()
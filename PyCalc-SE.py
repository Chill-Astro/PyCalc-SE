#!/usr/bin/env python3
import sys
import math
import os.path
import requests
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel, QSizePolicy
)
from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QIcon, QFontDatabase, QFont

UPDATE_VERSION_URL = "https://gist.githubusercontent.com/Chill-Astro/45fc2e5cce1c4e7c01b4f75a76121930/raw/7f865f4e71d559934be49b1d556db283434c6ec2/PyC_SE_V.txt"  # Gist URL

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.CURRENT_VERSION = "1.5" # Light Theme Support + Fixes
        self.setWindowTitle("PyCalc - Simple Edition")            
        self.setMinimumSize(340, 500)
        icon_path = os.path.join(".", "Pycalc-SE.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        # Load custom font Inter.ttf
        font_id = QFontDatabase.addApplicationFont("Inter.ttf")
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if font_families:
            custom_font = QFont(font_families[0], 14)
            QApplication.instance().setFont(custom_font)
            self.setFont(custom_font)
        # Restore window geometry
        self.settings = QSettings("ChillAstro", "PyCalc-SE")
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        self.initUI()
        self.apply_theme()
        self.reset()
        self.check_for_updates()
        # --- Theme polling for runtime changes ---
        from PySide6.QtCore import QTimer
        self._last_theme = self._detect_os_theme()
        self._theme_timer = QTimer(self)
        self._theme_timer.timeout.connect(self._check_theme_change)
        self._theme_timer.start(100)  # check every 0.1 seconds for more instant theme change

    def closeEvent(self, event):
        # Save window geometry
        self.settings.setValue("geometry", self.saveGeometry())
        super().closeEvent(event)

    def _detect_os_theme(self):
        # Returns 'dark' or 'light'
        try:
            if sys.platform == 'win32':
                import winreg
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize") as key:
                    value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                    return 'dark' if value == 0 else 'light'
            elif sys.platform == 'darwin':
                import subprocess
                result = subprocess.run([
                    'defaults', 'read', '-g', 'AppleInterfaceStyle'
                ], capture_output=True, text=True)
                return 'dark' if 'Dark' in result.stdout else 'light'
            elif sys.platform.startswith('linux'):
                # Try darkman if available
                import shutil
                if shutil.which('darkman'):
                    import subprocess
                    result = subprocess.run(['darkman', 'get'], capture_output=True, text=True)
                    return 'dark' if 'dark' in result.stdout.lower() else 'light'
                # Try GTK_THEME or XDG_CURRENT_DESKTOP heuristics
                gtk_theme = os.environ.get('GTK_THEME', '').lower()
                if 'dark' in gtk_theme:
                    return 'dark'
                # Try KDE color scheme
                kde_scheme = os.environ.get('KDE_COLOR_SCHEME', '').lower()
                if 'dark' in kde_scheme:
                    return 'dark'
                # Try XDG_CURRENT_DESKTOP for GNOME/KDE
                desktop = os.environ.get('XDG_CURRENT_DESKTOP', '').lower()
                if 'gnome' in desktop or 'kde' in desktop:
                    # Try to read gsettings (GNOME)
                    try:
                        import subprocess
                        result = subprocess.run([
                            'gsettings', 'get', 'org.gnome.desktop.interface', 'color-scheme'
                        ], capture_output=True, text=True)
                        if 'dark' in result.stdout.lower():
                            return 'dark'
                    except Exception:
                        pass
                # Default to dark
                return 'dark'
        except Exception:
            return 'dark'
        return 'dark'

    def _check_theme_change(self):
        current_theme = self._detect_os_theme()
        if current_theme != self._last_theme:
            self._last_theme = current_theme
            self.refresh_theme()

    def apply_theme(self):
        is_dark = self._detect_os_theme() == 'dark'
        if is_dark:
            self.setStyleSheet(self.dark_stylesheet())
            self._current_theme = 'dark'
        else:
            self.setStyleSheet(self.light_stylesheet())
            self._current_theme = 'light'
        self.update_label_styles()

    def refresh_theme(self):
        self.apply_theme()

    def update_label_styles(self):
        # Remove inline color styles so stylesheet takes effect
        self.display.setStyleSheet("font-size: 30px; font-weight: bold; padding-right: 0.5px;")
        self.history.setStyleSheet("font-size: 12px; padding-top: 20px;")

    def dark_stylesheet(self):
        return """
            QWidget { background: #23272e; }
            QLabel { color: #e6e6e6; }
            QLabel#display { color: #e6e6e6; }
            QLabel#history { color: #888; }
            QPushButton {
                background: #31343b; color: #e6e6e6; border: none; border-radius: 5px;
                font-size: 15px; padding: 8px;
            }
            QPushButton:pressed { background: #3a3d44; }
            QPushButton[op="true"] { background: #3b4252; color: #e6e6e6; }
            QPushButton[op="true"]:pressed { background: #434c5e; }
            QPushButton[fn="true"] { background: #2e3440; color: #bfc7d5; }
            QPushButton[fn="true"]:pressed { background: #3b4252; }
            QPushButton[eq="true"] { background: #5e81ac; color: #fff; }
            QPushButton[eq="true"]:pressed { background: #4c669f; }
        """

    def light_stylesheet(self):
        return """
            QWidget { background: #f5f6fa; }
            QLabel { color: #23272e; }
            QLabel#display { color: #23272e; }
            QLabel#history { color: #888; }
            QPushButton {
                background: #e6e9f0; color: #23272e; border: none; border-radius: 5px;
                font-size: 15px; padding: 8px;
            }
            QPushButton:pressed { background: #d1d5e0; }
            QPushButton[op="true"] { background: #dbeafe; color: #23272e; }
            QPushButton[op="true"]:pressed { background: #bcd0ee; }
            QPushButton[fn="true"] { background: #e0e7ef; color: #4b5563; }
            QPushButton[fn="true"]:pressed { background: #cfd8e3; }
            QPushButton[eq="true"] { background: #2563eb; color: #fff; }
            QPushButton[eq="true"]:pressed { background: #1d4ed8; }
        """

    def initUI(self):
        vbox = QVBoxLayout(self)
        vbox.setSpacing(10)
        vbox.setContentsMargins(8, 8, 8, 8)

        self.history = QLabel("")
        self.history.setObjectName("history")
        self.history.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.history.setStyleSheet("font-size: 12px; padding-top: 20px;")
        font_id = QFontDatabase.addApplicationFont("Inter.ttf")
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if font_families:
            self.history.setFont(QFont(font_families[0], 12))
        vbox.addWidget(self.history)

        self.display = QLabel("0")
        self.display.setObjectName("display")
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.display.setMinimumHeight(75)
        self.display.setStyleSheet("font-size: 30px; font-weight: bold; padding-right: 0.5px;")
        if font_families:
            self.display.setFont(QFont(font_families[0], 28, QFont.Bold))
        vbox.addWidget(self.display)

        grid = QGridLayout()
        grid.setSpacing(6)
        vbox.addLayout(grid)
        
        buttons = [
            [('xʸ', 'fn'), ('CE', 'fn'), ('C', 'fn'), ('⌫', 'fn')],
            [('x²', 'fn'), ('∛x', 'fn'), ('√x', 'fn'), ('÷', 'op')],
            [('7', ''), ('8', ''), ('9', ''), ('×', 'op')],
            [('4', ''), ('5', ''), ('6', ''), ('-', 'op')],
            [('1', ''), ('2', ''), ('3', ''), ('+', 'op')],
            [('+/-', 'fn'), ('0', ''), ('.', ''), ('=', 'eq')],
        ]

        self.button_map = {}
        for i, row in enumerate(buttons):
            for j, (text, role) in enumerate(row):
                btn = QPushButton(text)
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                if font_families:
                    btn.setFont(QFont(font_families[0], 16))
                if role == 'op':
                    btn.setProperty('op', True)
                elif role == 'eq':
                    btn.setProperty('eq', True)
                elif role == 'fn':
                    btn.setProperty('fn', True)
                btn.clicked.connect(lambda _, t=text: self.on_button(t))
                grid.addWidget(btn, i, j)
                self.button_map[text] = btn

    def reset(self):
        self.expression_history = ""
        self.current_input = "0"
        self.full_expression = ""
        self.result_pending = False
        self._currentNumber = 0.0
        self._previousNumber = 0.0
        self._currentOperator = ""
        self._isNewNumberInput = True
        self._hasDecimal = False
        self.update_display()

    def update_display(self):
        if isinstance(self._currentNumber, float):
            if self._currentNumber.is_integer() and not self._hasDecimal:
                display_value = str(int(self._currentNumber))
            else:
                display_value = str(self._currentNumber)
        else:
            display_value = str(self._currentNumber)
        self.display.setText(display_value)
        self.history.setText(self.expression_history)

    def clear_entry(self):
        self.current_input = "0"
        self._currentNumber = 0.0
        self._isNewNumberInput = True
        self._hasDecimal = False
        self.update_display()

    def backspace(self):
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
        try:
            self._currentNumber = -float(self._currentNumber)
            self.update_display()
        except Exception:
            self.handle_calculation_error()

    def calculate_square_root(self):
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

    def calculate_cube_root(self):
        try:
            num = float(self._currentNumber)
            # Cube root, handle negative numbers as real roots
            if num < 0:
                result = -(-num) ** (1/3)
            else:
                result = num ** (1/3)
            if isinstance(result, float) and result.is_integer() and not self._hasDecimal:
                self._currentNumber = int(result)
            else:
                self._currentNumber = result
            self.expression_history = f"∛({num})"
            self.update_display()
        except Exception:
            self.handle_calculation_error()

    def calculate_square(self):
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

    def on_button(self, text):
        if text in '0123456789':
            self.input_digit(text)
        elif text == '.':
            self.input_decimal()
        elif text in '+-×÷':
            # If '-' is pressed and we're starting a new number (after operator or at start), treat as negative sign
            if text == '-' and self._isNewNumberInput:
                if self._currentNumber == 0 and (not self._currentOperator or self.expression_history.endswith(('+', '-', '×', '÷', '^', '**'))):
                    self._currentNumber = 0.0
                    self._isNewNumberInput = False
                    self._hasDecimal = False
                    self.toggle_sign()
                    return
            op_map = {'+': '+', '-': '-', '×': '*', '÷': '/'}
            self.input_operator(op_map[text])
        elif text == '+/-':
            self.toggle_sign()
        elif text == 'x²':
            self.calculate_square()
        elif text == '∛x':
            self.calculate_cube_root()
        elif text == '√x':
            self.calculate_square_root()
        elif text == 'xʸ':
            self.input_operator('**')
        elif text == '=':
            self.calculate_result()
        elif text == 'C':
            self.reset()
        elif text == 'CE':
            self.clear_entry()
        elif text == '⌫':
            self.backspace()

    def keyPressEvent(self, event):
        key = event.key()
        text = event.text()
        # Numeric keys
        if text in '0123456789':
            self.on_button(text)
        # Operators
        elif text == '+':
            self.on_button('+')
        elif text == '-':
            self.on_button('-')
        elif text == '*':
            self.on_button('×')
        elif text == '/':
            self.on_button('÷')
        elif text == '.':
            self.on_button('.')
        elif text == '^':
            self.on_button('xʸ')
        elif text.lower() == 'c':
            self.on_button('C')
        elif text == '=' or key == Qt.Key_Enter or key == Qt.Key_Return:
            self.on_button('=')
        elif key == Qt.Key_Backspace:
            self.on_button('⌫')
        elif key == Qt.Key_Delete:
            self.on_button('CE')
        else:
            super().keyPressEvent(event)

    def check_for_updates(self):
        from PySide6.QtCore import QThread, Signal

        class UpdateCheckThread(QThread):
            update_message = Signal(str)

            def __init__(self, parent=None):
                super().__init__(parent)
                self.parent = parent

            def run(self):
                try:
                    response = requests.get(UPDATE_VERSION_URL, timeout=5)
                    response.raise_for_status()
                    latest_version = response.text.strip()
                    if latest_version > self.parent.CURRENT_VERSION:
                        msg = f"🎉 PyCalc-SE v{latest_version} is OUT NOW!"
                    elif latest_version == self.parent.CURRENT_VERSION:
                        msg = "🎉 PyCalc-SE is up to date!"
                    elif latest_version < self.parent.CURRENT_VERSION:
                        msg = "⚠️ This is a Dev. Build of PyCalc-SE!"
                    else:
                        msg = "🎉 PyCalc-SE is up to date!"
                except Exception:
                    msg = "⚠️ Error : Check your Internet Connection."
                self.update_message.emit(msg)

        self.update_thread = UpdateCheckThread(self)
        self.update_thread.update_message.connect(self.show_update_message)
        self.update_thread.start()

    def show_update_message(self, msg):
        from PySide6.QtCore import QTimer
        def clear_message():
            if self.history.text() == msg:
                self.history.setText("")
                self.history.update()
        self.history.setText(msg)
        self.history.setStyleSheet("font-size: 12px; padding-top: 20px;")
        QTimer.singleShot(4000, clear_message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec())
import tkinter as tk
from tkinter import ttk, messagebox, font
import threading
from googletrans import Translator, LANGUAGES

class AdvancedTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Translator")
        self.translator = Translator()
        
        # Theme Configuration
        self.dark_bg = "#1e1e1e"
        self.darker_bg = "#121212"
        self.light_text = "#ffffff"
        self.accent_color = "#4fc3f7"
        self.widget_bg = "#252525"
        self.text_bg = "#2d2d2d"
        self.success_green = "#2e7d32"
        self.error_red = "#c62828"
        
        # Configure root window
        self.root.configure(bg=self.darker_bg)
        self.root.geometry("800x700")
        self.root.minsize(700, 600)
        self.root.resizable(True, True)
        
        # Custom fonts
        self.load_fonts()
        
        # Create style
        self.create_styles()
        
        # Build UI
        self.create_widgets()
        
        # Loading animation
        self.loading = False
        self.loading_frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.current_frame = 0
        
        # Translation history
        self.history = []
        
        # Center window
        self.center_window()

        # Keyboard Shortcuts
        self.root.bind('<Control-t>', lambda event: self.start_translation())
        self.root.bind('<Control-c>', lambda event: self.clear_text())

    def load_fonts(self):
        self.title_font = font.Font(family="Montserrat", size=20, weight="bold")
        self.label_font = font.Font(family="Segoe UI", size=12)
        self.button_font = font.Font(family="Segoe UI", size=12, weight="bold")
        self.text_font = font.Font(family="Consolas", size=12)
        self.status_font = font.Font(family="Segoe UI", size=10)

    def create_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # General styling
        style.configure('.', background=self.darker_bg, foreground=self.light_text)
        style.configure('TLabel', font=self.label_font)
        style.configure('TButton', font=self.button_font, borderwidth=1)
        
        # Custom button styles
        style.map('Submit.TButton',
                 background=[('active', self.success_green), ('!active', '#388e3c')],
                 foreground=[('active', self.light_text), ('!active', self.light_text)])
        
        style.map('Clear.TButton',
                 background=[('active', self.error_red), ('!active', '#d32f2f')],
                 foreground=[('active', self.light_text), ('!active', self.light_text)])
        
        # Entry styling
        style.configure('TCombobox', fieldbackground=self.widget_bg, background=self.widget_bg,
                       foreground=self.light_text, selectbackground=self.accent_color)
        
        # Frame styling
        style.configure('Card.TFrame', background=self.dark_bg, relief=tk.RAISED, borderwidth=2)
        
        # Custom scrollbar
        style.configure("Vertical.TScrollbar", gripcount=0, background=self.widget_bg, 
                      troughcolor=self.darker_bg, arrowcolor=self.accent_color)

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')

    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.title_label = ttk.Label(header_frame, text="ULTIMATE TRANSLATOR", font=self.title_font,
                                   foreground=self.accent_color)
        self.title_label.pack()
        
        # Language selection card
        lang_card = ttk.Frame(main_frame, style='Card.TFrame')
        lang_card.pack(fill=tk.X, pady=10)
        
        # Language selection frame
        lang_frame = ttk.Frame(lang_card)
        lang_frame.pack(padx=15, pady=15, fill=tk.X)
        
        # Source Language
        self.source_lang_label = ttk.Label(lang_frame, text="Source Language:")
        self.source_lang_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        
        self.source_lang = ttk.Combobox(lang_frame, values=["Auto"] + list(LANGUAGES.values()), state="readonly")
        self.source_lang.grid(row=0, column=1, padx=10, pady=5, sticky=tk.EW)
        
        # Target Language
        self.target_lang_label = ttk.Label(lang_frame, text="Target Language:")
        self.target_lang_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        
        self.target_lang = ttk.Combobox(lang_frame, values=list(LANGUAGES.values()), state="readonly")
        self.target_lang.grid(row=1, column=1, padx=10, pady=5, sticky=tk.EW)
        
        # Text input card
        input_card = ttk.Frame(main_frame, style='Card.TFrame')
        input_card.pack(fill=tk.BOTH, expand=True)
        
        # Input text with scrollbar
        input_frame = ttk.Frame(input_card)
        input_frame.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)
        
        self.text_input_label = ttk.Label(input_frame, text="Text to Translate:")
        self.text_input_label.pack(anchor=tk.W)
        
        self.text_input = tk.Text(input_frame, height=10, bg=self.text_bg, fg=self.light_text,
                                insertbackground=self.light_text, font=self.text_font,
                                relief=tk.FLAT, borderwidth=0, padx=10, pady=10)
        self.text_input.pack(fill=tk.BOTH, expand=True)
        
        input_scroll = ttk.Scrollbar(input_frame, command=self.text_input.yview)
        input_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_input.config(yscrollcommand=input_scroll.set)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.submit_button = ttk.Button(button_frame, text="Translate", style='Submit.TButton',
                                      command=self.start_translation)
        self.submit_button.pack(side=tk.LEFT, padx=5, ipady=5, expand=True)
        
        self.clear_button = ttk.Button(button_frame, text="Clear", style='Clear.TButton',
                                     command=self.clear_text)
        self.clear_button.pack(side=tk.RIGHT, padx=5, ipady=5, expand=True)
        
        # Loading label
        self.loading_label = ttk.Label(button_frame, text="", font=self.status_font)
        self.loading_label.pack(pady=5)
        
        # Output card
        output_card = ttk.Frame(main_frame, style='Card.TFrame')
        output_card.pack(fill=tk.BOTH, expand=True)
        
        # Output text with scrollbar
        output_frame = ttk.Frame(output_card)
        output_frame.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)
        
        self.output_label = ttk.Label(output_frame, text="Translation:")
        self.output_label.pack(anchor=tk.W)
        
        self.output_text = tk.Text(output_frame, height=10, bg=self.text_bg, fg=self.light_text,
                                 insertbackground=self.light_text, font=self.text_font,
                                 relief=tk.FLAT, borderwidth=0, padx=10, pady=10, state=tk.DISABLED)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        output_scroll = ttk.Scrollbar(output_frame, command=self.output_text.yview)
        output_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.config(yscrollcommand=output_scroll.set)
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W,
                                   font=self.status_font, foreground=self.accent_color)
        self.status_bar.pack(fill=tk.X, padx=5, pady=(0,5))
        
        # Configure grid weights
        lang_frame.columnconfigure(1, weight=1)

    def start_translation(self):
        if not self.validate_input():
            return
            
        self.loading = True
        self.update_loading_animation()
        self.toggle_buttons_state(False)
        self.status_bar.config(text="Translating... please wait", foreground=self.accent_color)
        
        # Run translation in separate thread
        translation_thread = threading.Thread(target=self.perform_translation, daemon=True)
        translation_thread.start()

    def perform_translation(self):
        try:
            source = self.source_lang.get()
            target = self.target_lang.get()
            text = self.text_input.get("1.0", tk.END).strip()
            
            # Detect language if source is set to "Auto"
            if source == "Auto":
                source_lang_code = 'auto'
            else:
                source_lang_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(source)]
                
            target_lang_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(target)]
            
            translation = self.translator.translate(text, src=source_lang_code, dest=target_lang_code)
            
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, translation.text)
            self.output_text.config(state=tk.DISABLED)
            
            self.status_bar.config(text=f"Successfully translated from {source} to {target}", foreground=self.success_green)
            
            # Save to history
            self.history.append((text, translation.text, source, target))
            
        except Exception as e:
            self.status_bar.config(text=f"Error: {str(e)}", foreground=self.error_red)
            messagebox.showerror("Translation Error", f"An error occurred:\n{str(e)}", parent=self.root)
        finally:
            self.loading = False
            self.toggle_buttons_state(True)
            self.loading_label.config(text="")

    def update_loading_animation(self):
        if self.loading:
            frame = self.loading_frames[self.current_frame % len(self.loading_frames)]
            self.loading_label.config(text=f"{frame} Translating")
            self.current_frame += 1
            self.root.after(100, self.update_loading_animation)

    def validate_input(self):
        if not self.text_input.get("1.0", tk.END).strip():
            self.status_bar.config(text="Error: Please enter text to translate", foreground=self.error_red)
            return False
            
        if not self.source_lang.get() or not self.target_lang.get():
            self.status_bar.config(text="Error: Please select both languages", foreground=self.error_red)
            return False
            
        return True

    def clear_text(self):
        self.text_input.delete("1.0", tk.END)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.source_lang.set('Auto')
        self.target_lang.set('')
        self.status_bar.config(text="Cleared all fields", foreground=self.accent_color)

    def toggle_buttons_state(self, enabled):
        state = tk.NORMAL if enabled else tk.DISABLED
        self.submit_button.config(state=state)
        self.clear_button.config(state=state)

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedTranslatorApp(root)
    root.mainloop()

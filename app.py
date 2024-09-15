import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import time
import os
from functools import lru_cache
import platform
import psutil
try:
    import GPUtil
except ImportError:
    GPUtil = None

class EnhancedDictionaryCreator:
    def __init__(self, master):
        self.master = master
        self.master.title("Enhanced Dictionary Creator")
        self.master.geometry("500x450")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        self.main_frame = ctk.CTkFrame(self.master)
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # System info
        self.system_info_label = ctk.CTkLabel(self.main_frame, text=self.get_system_info(), justify=tk.LEFT)
        self.system_info_label.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="w")
        
        # Mode selection
        self.mode_var = ctk.StringVar(value="Number")
        self.mode_label = ctk.CTkLabel(self.main_frame, text="Mode:")
        self.mode_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.mode_menu = ctk.CTkOptionMenu(self.main_frame, values=["Number", "Alphabet"], 
                                           variable=self.mode_var, command=self.update_labels)
        self.mode_menu.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        # From entry
        self.from_label = ctk.CTkLabel(self.main_frame, text="From (number):")
        self.from_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.start_entry = ctk.CTkEntry(self.main_frame)
        self.start_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        # To entry
        self.to_label = ctk.CTkLabel(self.main_frame, text="To (number):")
        self.to_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.end_entry = ctk.CTkEntry(self.main_frame)
        self.end_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        
        # Output directory
        self.dir_label = ctk.CTkLabel(self.main_frame, text="Output Directory:")
        self.dir_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.dir_entry = ctk.CTkEntry(self.main_frame)
        self.dir_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        self.dir_button = ctk.CTkButton(self.main_frame, text="Browse", command=self.browse_directory)
        self.dir_button.grid(row=4, column=2, padx=5, pady=5)
        
        # Generate button
        self.generate_button = ctk.CTkButton(self.main_frame, text="Generate Dictionary", 
                                             command=self.generate_dictionary)
        self.generate_button.grid(row=5, column=0, columnspan=3, padx=5, pady=20, sticky="ew")
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.main_frame)
        self.progress_bar.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        self.progress_bar.set(0)
        
        # Status label
        self.status_label = ctk.CTkLabel(self.main_frame, text="")
        self.status_label.grid(row=7, column=0, columnspan=3, padx=5, pady=5)
        
        # Configure grid
        self.main_frame.grid_columnconfigure(1, weight=1)
        
    def get_system_info(self):
        cpu_info = f"CPU: {platform.processor()}"
        gpu_info = "GPU: Not detected"
        if GPUtil:
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu_info = f"GPU: {gpus[0].name}"
            except:
                pass
        return f"{cpu_info}\n{gpu_info}"
        
    def update_labels(self, _):
        if self.mode_var.get() == "Alphabet":
            self.from_label.configure(text="From (e.g., a, aa, no):")
            self.to_label.configure(text="To (e.g., z, zz, nzzzzz):")
        else:
            self.from_label.configure(text="From (number):")
            self.to_label.configure(text="To (number):")
            
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)
            
    def generate_dictionary(self):
        start = self.start_entry.get().lower()
        end = self.end_entry.get().lower()
        output_dir = self.dir_entry.get()
        is_alphabet = self.mode_var.get() == "Alphabet"
        
        if not output_dir:
            messagebox.showerror("Error", "Please select an output directory")
            return
        
        if is_alphabet:
            if not (start.isalpha() and end.isalpha()):
                messagebox.showerror("Error", "Please enter valid alphabetic characters")
                return
            if len(start) > len(end) or (len(start) == len(end) and start > end):
                messagebox.showerror("Error", "Start sequence must come before or be the same as end sequence")
                return
        else:
            try:
                start_num = int(start)
                end_num = int(end)
                if start_num > end_num:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers, with start <= end")
                return
        
        filename = os.path.join(output_dir, f"{start}-{end}.txt")
        
        self.generate_button.configure(state="disabled")
        self.progress_bar.set(0)
        self.status_label.configure(text="Generating...")
        
        thread = threading.Thread(target=self.generate, args=(start, end, is_alphabet, filename))
        thread.start()
        
    def generate(self, start, end, is_alphabet, filename):
        chunk_size = 100000
        total_items = 0
        
        with open(filename, 'w') as f:
            if is_alphabet:
                for chunk in self.generate_alphabet_sequence(start, end):
                    f.write(chunk + '\n')
                    total_items += 1
                    if total_items % chunk_size == 0:
                        self.update_progress(total_items, None)
            else:
                total_items = int(end) - int(start) + 1
                for num in range(int(start), int(end) + 1):
                    f.write(str(num) + '\n')
                    if (num - int(start) + 1) % chunk_size == 0:
                        progress = (num - int(start) + 1) / total_items
                        self.update_progress(num - int(start) + 1, progress)
        
        self.master.after(0, self.generation_complete, filename, total_items)
        
    def update_progress(self, items, progress):
        self.master.after(0, self._update_progress, items, progress)
        
    def _update_progress(self, items, progress):
        if progress is not None:
            self.progress_bar.set(progress)
            self.status_label.configure(text=f"Progress: {progress:.1%}")
        else:
            self.status_label.configure(text=f"Generated: {items}")
        
    def generation_complete(self, filename, total_items):
        self.generate_button.configure(state="normal")
        self.progress_bar.set(1)
        self.status_label.configure(text="Generation complete!")
        messagebox.showinfo("Success", f"Dictionary created: {filename}\nTotal items: {total_items}")
        
    @staticmethod
    @lru_cache(maxsize=None)
    def generate_alphabet_sequence(start, end):
        def increment(s):
            chars = list(s)
            for i in range(len(chars) - 1, -1, -1):
                if chars[i] < 'z':
                    chars[i] = chr(ord(chars[i]) + 1)
                    return ''.join(chars)
                chars[i] = 'a'
            return 'a' * (len(s) + 1)

        sequence = []
        current = start
        while len(current) <= len(end):
            sequence.append(current)
            if current == end:
                break
            current = increment(current)
        return sequence

if __name__ == "__main__":
    root = ctk.CTk()
    app = EnhancedDictionaryCreator(root)
    root.mainloop()
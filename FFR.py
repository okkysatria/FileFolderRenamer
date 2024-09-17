import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

undo_stack = []
redo_stack = []
selected_directory = None
scan_mode = "Files"
sort_by = "Name"

def list_items(directory, filter_text="", sort_by="Name"):
    try:
        if scan_mode == "Files":
            items = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        else:
            items = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
        if filter_text:
            items = [f for f in items if filter_text.lower() in f.lower()]
        
        if sort_by == "Name":
            items.sort(key=lambda x: x.lower())
        elif sort_by == "Date Modified":
            items.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)))
        
        return items
    except Exception as e:
        messagebox.showerror("Error", f"Failed to list items: {e}")
        return []

def rename_items(directory, old_names, new_names):
    try:
        for old_name, new_name in zip(old_names, new_names):
            old_path = os.path.join(directory, old_name)
            new_path = os.path.join(directory, new_name)
            if os.path.exists(old_path):
                os.rename(old_path, new_path)
                undo_stack.append((new_name, old_name))
            else:
                messagebox.showwarning("Item Not Found", f"Item not found: {old_name}")
        update_item_list(directory)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to rename items: {e}")

def batch_rename_items():
    old_names = items_listbox.get(0, tk.END)
    new_names_str = new_names_text.get("1.0", tk.END).strip().split('\n')
    
    if len(old_names) != len(new_names_str):
        messagebox.showwarning("Mismatch", "The number of new names does not match the number of items.")
        return

    new_names = [name.strip() for name in new_names_str]
    if not all(new_names):
        messagebox.showwarning("Invalid Input", "New names cannot be empty.")
        return

    try:
        redo_stack.clear()
        rename_items(selected_directory, old_names, new_names)
        messagebox.showinfo("Rename", "Items renamed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to rename items: {e}")
    finally:
        new_names_text.delete("1.0", tk.END)

def undo():
    if not undo_stack:
        messagebox.showinfo("Undo", "Nothing to undo.")
        return
    
    try:
        while undo_stack:
            new_name, old_name = undo_stack.pop()
            old_path = os.path.join(selected_directory, new_name)
            new_path = os.path.join(selected_directory, old_name)
            if os.path.exists(old_path):
                os.rename(old_path, new_path)
                redo_stack.append((old_name, new_name))
            else:
                messagebox.showwarning("Item Not Found", f"Item not found: {new_name}")
        update_item_list(selected_directory)
        messagebox.showinfo("Undo", "Undo operation completed.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to undo rename: {e}")

def redo():
    if not redo_stack:
        messagebox.showinfo("Redo", "Nothing to redo.")
        return
    
    try:
        while redo_stack:
            old_name, new_name = redo_stack.pop()
            old_path = os.path.join(selected_directory, old_name)
            new_path = os.path.join(selected_directory, new_name)
            if os.path.exists(old_path):
                os.rename(old_path, new_path)
                undo_stack.append((new_name, old_name))
            else:
                messagebox.showwarning("Item Not Found", f"Item not found: {old_name}")
        update_item_list(selected_directory)
        messagebox.showinfo("Redo", "Redo operation completed.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to redo rename: {e}")

def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        directory_label.config(text=f'Selected Directory: {directory}')
        start_scan_thread(directory)
        rename_button.config(state=tk.NORMAL)
        copy_button.config(state=tk.NORMAL)
        save_button.config(state=tk.NORMAL)
        filter_button.config(state=tk.NORMAL)
        global selected_directory
        selected_directory = directory
        return directory
    else:
        return None

def start_scan_thread(directory, filter_text=""):
    scan_thread = threading.Thread(target=update_item_list, args=(directory, filter_text))
    scan_thread.start()
    show_loading_indicator(scan_thread)

def update_item_list(directory, filter_text=""):
    items = list_items(directory, filter_text, sort_by)
    items_listbox.delete(0, tk.END)
    for item in items:
        items_listbox.insert(tk.END, item)
    item_count_label.config(text=f"Total items: {len(items)}")

def show_loading_indicator(thread):
    loading_popup = tk.Toplevel(root)
    loading_popup.title("Loading")
    loading_popup.geometry("200x100")
    loading_popup.configure(bg='#2E2E2E')
    loading_label = tk.Label(loading_popup, text="Scanning, please wait...", bg='#2E2E2E', fg='white')
    loading_label.pack(expand=True)

    def check_thread():
        if thread.is_alive():
            root.after(100, check_thread)
        else:
            loading_popup.destroy()

    check_thread()

def copy_to_clipboard():
    items = items_listbox.get(0, tk.END)
    items_str = "\n".join(items)
    try:
        root.clipboard_clear()
        root.clipboard_append(items_str)
        messagebox.showinfo("Copy", "List copied to clipboard!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to copy list to clipboard: {e}")

def save_to_note():
    items = items_listbox.get(0, tk.END)
    items_str = "\n".join(items)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(items_str)
            messagebox.showinfo("Save", "List saved to note!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save list to note: {e}")

def filter_items():
    filter_text = filter_entry.get().strip()
    start_scan_thread(selected_directory, filter_text)

def set_scan_mode():
    global scan_mode
    scan_mode = scan_mode_var.get()
    if selected_directory:
        start_scan_thread(selected_directory)

def set_sort_by(event):
    global sort_by
    sort_by = sort_by_var.get()
    if selected_directory:
        start_scan_thread(selected_directory)

root = tk.Tk()
root.title("File and Folder Renamer")
root.geometry("800x600")
root.configure(bg='#2E2E2E')

main_frame = tk.Frame(root, padx=10, pady=10, bg='#2E2E2E')
main_frame.pack(fill=tk.BOTH, expand=True)

dir_frame = tk.LabelFrame(main_frame, text="Directory", padx=10, pady=10, bg='#2E2E2E', fg='white')
dir_frame.pack(fill=tk.X, pady=(0, 10))

directory_label = tk.Label(dir_frame, text="No directory selected", bg='#2E2E2E', fg='white')
directory_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

select_directory_button = tk.Button(dir_frame, text="Select Directory", command=select_directory, bg='#4A4A4A', fg='white')
select_directory_button.pack(side=tk.RIGHT)

scan_mode_frame = tk.LabelFrame(main_frame, text="Scan Mode", padx=10, pady=10, bg='#2E2E2E', fg='white')
scan_mode_frame.pack(fill=tk.X, pady=(0, 10))

scan_mode_var = tk.StringVar(value="Files")
files_radio = tk.Radiobutton(scan_mode_frame, text="Files", variable=scan_mode_var, value="Files", command=set_scan_mode, bg='#2E2E2E', fg='white', selectcolor='#2E2E2E')
files_radio.pack(side=tk.LEFT)
folders_radio = tk.Radiobutton(scan_mode_frame, text="Folders", variable=scan_mode_var, value="Folders", command=set_scan_mode, bg='#2E2E2E', fg='white', selectcolor='#2E2E2E')
folders_radio.pack(side=tk.LEFT)

sorting_frame = tk.LabelFrame(main_frame, text="Sort By", padx=10, pady=10, bg='#2E2E2E', fg='white')
sorting_frame.pack(fill=tk.X, pady=(0, 10))

sort_by_var = tk.StringVar(value="Name")
sort_by_combobox = ttk.Combobox(sorting_frame, textvariable=sort_by_var, values=["Name", "Date Modified"], state="readonly")
sort_by_combobox.pack(fill=tk.X)
sort_by_combobox.bind("<<ComboboxSelected>>", set_sort_by)

items_frame = tk.LabelFrame(main_frame, text="Items", padx=10, pady=10, bg='#2E2E2E', fg='white')
items_frame.pack(fill=tk.BOTH, expand=True)

items_listbox = tk.Listbox(items_frame, selectmode=tk.MULTIPLE, bg='#4A4A4A', fg='white')
items_listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

scrollbar = tk.Scrollbar(items_frame, orient=tk.VERTICAL)
scrollbar.config(command=items_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
items_listbox.config(yscrollcommand=scrollbar.set)

item_count_label = tk.Label(items_frame, text="Total items: 0", bg='#2E2E2E', fg='white')
item_count_label.pack(fill=tk.X)

new_names_frame = tk.LabelFrame(main_frame, text="New Names", padx=10, pady=10, bg='#2E2E2E', fg='white')
new_names_frame.pack(fill=tk.X, pady=(0, 10))

new_names_text = tk.Text(new_names_frame, height=10, bg='#4A4A4A', fg='white')
new_names_text.pack(fill=tk.X)

control_buttons_frame = tk.Frame(main_frame, padx=10, pady=10, bg='#2E2E2E')
control_buttons_frame.pack(fill=tk.X, pady=(0, 10))

rename_button = tk.Button(control_buttons_frame, text="Batch Rename", command=batch_rename_items, bg='#4A4A4A', fg='white')
rename_button.pack(side=tk.LEFT)
rename_button.config(state=tk.DISABLED)

copy_button = tk.Button(control_buttons_frame, text="Copy to Clipboard", command=copy_to_clipboard, bg='#4A4A4A', fg='white')
copy_button.pack(side=tk.LEFT)
copy_button.config(state=tk.DISABLED)

save_button = tk.Button(control_buttons_frame, text="Save to Note", command=save_to_note, bg='#4A4A4A', fg='white')
save_button.pack(side=tk.LEFT)
save_button.config(state=tk.DISABLED)

filter_label = tk.Label(control_buttons_frame, text="Filter:", bg='#2E2E2E', fg='white')
filter_label.pack(side=tk.LEFT)

filter_entry = tk.Entry(control_buttons_frame, bg='#4A4A4A', fg='white')
filter_entry.pack(side=tk.LEFT, padx=(5, 5))

filter_button = tk.Button(control_buttons_frame, text="Apply Filter", command=filter_items, bg='#4A4A4A', fg='white')
filter_button.pack(side=tk.LEFT)
filter_button.config(state=tk.DISABLED)

undo_button = tk.Button(control_buttons_frame, text="Undo", command=undo, bg='#4A4A4A', fg='white')
undo_button.pack(side=tk.RIGHT)

redo_button = tk.Button(control_buttons_frame, text="Redo", command=redo, bg='#4A4A4A', fg='white')
redo_button.pack(side=tk.RIGHT, padx=(5, 0))

root.mainloop()

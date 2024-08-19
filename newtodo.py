import tkinter as tk
from tkinter import ttk, messagebox
import jsonpickle
import os

# Define the ToDoApp class
class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do App")
        self.root.geometry("900x600")
        self.root.config(bg="#1a1a1a")
        
        self.profiles = ["Work", "School", "Custom"]
        self.current_profile = tk.StringVar(value=self.profiles[0])
        self.todo_data = self.load_data()
        self.current_todo_index = None
        
        self.sidebar_expanded = True
        self.setup_ui()

    def setup_ui(self):
        self.create_sidebar()
        self.create_todo_frame()
        self.create_profile_menu()
        self.load_todos()

    def create_sidebar(self):
        self.sidebar = tk.Frame(self.root, bg="#333", width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        toggle_btn = tk.Button(self.sidebar, text="☰", command=self.toggle_sidebar, bg="#444", fg="white", font=("Helvetica", 16))
        toggle_btn.pack(pady=10, padx=20, fill=tk.X)

        add_todo_btn = tk.Button(self.sidebar, text="Add To-Do", command=self.add_todo, bg="#4CAF50", fg="white", font=("Helvetica", 14))
        add_todo_btn.pack(pady=10, padx=20, fill=tk.X)

        del_todo_btn = tk.Button(self.sidebar, text="Delete Selected", command=self.delete_todo, bg="#ff4c4c", fg="white", font=("Helvetica", 14))
        del_todo_btn.pack(pady=10, padx=20, fill=tk.X)

        self.todo_listbox = tk.Listbox(self.sidebar, selectmode=tk.SINGLE, bg="#333", fg="#f5f5f5", font=("Helvetica", 12))
        self.todo_listbox.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        self.todo_listbox.bind('<<ListboxSelect>>', self.display_todo_content)

    def toggle_sidebar(self):
        if self.sidebar_expanded:
            self.sidebar.pack_forget()
            self.sidebar = tk.Frame(self.root, bg="#333", width=50)
            self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
            toggle_btn = tk.Button(self.sidebar, text="☰", command=self.toggle_sidebar, bg="#444", fg="white", font=("Helvetica", 16))
            toggle_btn.pack(pady=10, padx=20, fill=tk.X)
            self.sidebar_expanded = False
        else:
            self.sidebar.pack_forget()
            self.create_sidebar()
            self.sidebar_expanded = True

    def create_todo_frame(self):
        self.todo_frame = tk.Frame(self.root, bg="#1a1a1a")
        self.todo_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.todo_title_label = tk.Label(self.todo_frame, text="", font=("Helvetica", 18), bg="#1a1a1a", fg="#f5f5f5")
        self.todo_title_label.pack(pady=10)

        self.todo_content_text = tk.Text(self.todo_frame, bg="#333", fg="#f5f5f5", wrap=tk.WORD, font=("Helvetica", 14))
        self.todo_content_text.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        save_changes_btn = tk.Button(self.todo_frame, text="Save Changes", command=self.save_changes, bg="#4CAF50", fg="white", font=("Helvetica", 14))
        save_changes_btn.pack(pady=10)

        delete_todo_btn = tk.Button(self.todo_frame, text="Delete To-Do", command=self.delete_selected_todo, bg="#ff4c4c", fg="white", font=("Helvetica", 14))
        delete_todo_btn.pack(pady=10)

    def create_profile_menu(self):
        profile_menu = tk.Menu(self.root, tearoff=0)
        profile_menu.add_command(label="Add Profile", command=self.add_profile)

        for profile in self.profiles:
            profile_menu.add_radiobutton(label=profile, variable=self.current_profile, command=self.switch_profile)
        
        menubar = tk.Menu(self.root)
        menubar.add_cascade(label="Profiles", menu=profile_menu)
        self.root.config(menu=menubar)

    def add_todo(self):
        new_todo_window = tk.Toplevel(self.root)
        new_todo_window.title("Add To-Do")
        new_todo_window.config(bg="#1a1a1a")

        tk.Label(new_todo_window, text="Title:", font=("Helvetica", 14), bg="#1a1a1a", fg="#f5f5f5").pack(pady=10)
        title_entry = tk.Entry(new_todo_window, font=("Helvetica", 14), bg="#333", fg="#f5f5f5")
        title_entry.pack(pady=10)

        tk.Label(new_todo_window, text="Content:", font=("Helvetica", 14), bg="#1a1a1a", fg="#f5f5f5").pack(pady=10)
        content_text = tk.Text(new_todo_window, height=10, font=("Helvetica", 14), bg="#333", fg="#f5f5f5")
        content_text.pack(pady=10)

        def save_todo():
            title = title_entry.get()
            content = content_text.get("1.0", tk.END).strip()
            if title and content:
                self.todo_data[self.current_profile.get()].append({"title": title, "content": content})
                self.save_data()
                self.load_todos()
                new_todo_window.destroy()
            else:
                messagebox.showwarning("Input Error", "Both title and content are required.")

        tk.Button(new_todo_window, text="Save", command=save_todo, bg="#4CAF50", fg="white", font=("Helvetica", 14)).pack(pady=10)

    def delete_todo(self):
        selected_index = self.todo_listbox.curselection()
        if selected_index:
            del self.todo_data[self.current_profile.get()][selected_index[0]]
            self.save_data()
            self.load_todos()

    def delete_selected_todo(self):
        if self.current_todo_index is not None:
            del self.todo_data[self.current_profile.get()][self.current_todo_index]
            self.save_data()
            self.load_todos()
            self.todo_title_label.config(text="")
            self.todo_content_text.delete("1.0", tk.END)
            self.current_todo_index = None
            messagebox.showinfo("Success", "To-Do deleted successfully.")

    def display_todo_content(self, event):
        selected_index = self.todo_listbox.curselection()
        if selected_index:
            self.current_todo_index = selected_index[0]
            selected_todo = self.todo_data[self.current_profile.get()][self.current_todo_index]
            self.todo_title_label.config(text=selected_todo["title"])
            self.todo_content_text.delete("1.0", tk.END)
            self.todo_content_text.insert(tk.END, selected_todo["content"])

    def save_changes(self):
        if self.current_todo_index is not None:
            title = self.todo_title_label.cget("text")
            content = self.todo_content_text.get("1.0", tk.END).strip()
            if title and content:
                self.todo_data[self.current_profile.get()][self.current_todo_index] = {"title": title, "content": content}
                self.save_data()
                self.load_todos()
                messagebox.showinfo("Success", "Changes saved successfully.")
            else:
                messagebox.showwarning("Input Error", "Both title and content are required.")
    
    def switch_profile(self):
        self.load_todos()

    def add_profile(self):
        new_profile_window = tk.Toplevel(self.root)
        new_profile_window.title("Add Profile")
        new_profile_window.config(bg="#1a1a1a")

        tk.Label(new_profile_window, text="Profile Name:", font=("Helvetica", 14), bg="#1a1a1a", fg="#f5f5f5").pack(pady=10)
        profile_name_entry = tk.Entry(new_profile_window, font=("Helvetica", 14), bg="#333", fg="#f5f5f5")
        profile_name_entry.pack(pady=10)

        def save_profile():
            profile_name = profile_name_entry.get().strip()
            if profile_name and profile_name not in self.profiles:
                self.profiles.append(profile_name)
                self.todo_data[profile_name] = []
                self.current_profile.set(profile_name)
                self.save_data()
                self.create_profile_menu()
                self.load_todos()
                new_profile_window.destroy()
            else:
                messagebox.showwarning("Input Error", "Profile name is required and must be unique.")

        tk.Button(new_profile_window, text="Save", command=save_profile, bg="#4CAF50", fg="white", font=("Helvetica", 14)).pack(pady=10)

    def load_data(self):
        if os.path.exists("todos.json"):
            with open("todos.json", "r") as file:
                return jsonpickle.decode(file.read())
        return {profile: [] for profile in self.profiles}

    def save_data(self):
        with open("todos.json", "w") as file:
            file.write(jsonpickle.encode(self.todo_data))

    def load_todos(self):
        self.todo_listbox.delete(0, tk.END)
        for todo in self.todo_data.get(self.current_profile.get(), []):
            self.todo_listbox.insert(tk.END, todo["title"])

def add_checkbox(self):
    checkbox_state = tk.BooleanVar(value=False)
    checkbox = tk.Checkbutton(self.todo_frame, variable=checkbox_state, bg="#1a1a1a", activebackground="#1a1a1a", selectcolor="#1a1a1a")
    checkbox.pack(pady=10)

    def toggle_checkbox():
        if checkbox_state.get():
            checkbox_state.set(False)
        else:
            checkbox_state.set(True)

    checkbox.config(command=toggle_checkbox)

# Main application start
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()

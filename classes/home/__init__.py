from customtkinter import *
from lib.file import save_file
from lib.utilitys import check_task_id


class FrameTask(CTkFrame):
    def __init__(self, master, finished, id, name, home_class, app_class):
        super().__init__(master, height=40, corner_radius=0, fg_color="#646464")
        self.pack(fill="x", pady=2, padx=(0, 0))
        self.rowconfigure((0, 2), weight=1)
        self.grid_propagate(False)

    # ---------------------- UI COMPONENTS ----------------------
        CTkLabel(self, text=("Sim" if finished else "Não"), text_color="white",
                font=("Arial", 20)).grid(row=1, column=0, padx=(10, 10))
        CTkLabel(self, text=name, text_color="white",
                font=("Arial", 20)).grid(row=1, column=1, padx=(10, 30))
        CTkButton(self, text="Remover", height=30,
                fg_color="#be0101", hover_color="#eb0404",
                corner_radius=0,
                command=lambda: self.remove_task(id, home_class, app_class)).pack(side="right", anchor="center")
        
    # ------------------ CONDITIONAL STRUCTURE ------------------
        if not finished:
            CTkButton(self, text="Concluido", height=30,
                    fg_color="#31ad00", hover_color="#47cf12",
                    corner_radius=0,
                    command=lambda: self.check_task(id, home_class, app_class)).pack(side="right", anchor="center", padx=5)
        
    # ------------------------ FUNCTIONS ------------------------
    def remove_task(self, id, home_class, app_class):
        for i, t in enumerate(app_class.tasks):
            if t["id"] == id:
                del app_class.tasks[i]
                self.destroy()
                home_class.update_list()
                return
                

    def check_task(self, id, home_class, app_class):
        for i, t in enumerate(app_class.tasks):
            if t["id"] == id:
                t["finished"] = True
                home_class.update_list()
                return




class WinHome(CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0)

    # --------------------- UI COMPONENTS ---------------------
        CTkLabel(self, text="Gerenciador de tarefas", font=("Arial", 50, "bold")).pack(pady=10)

        self.main_frame = CTkFrame(self, width=800, height=500, corner_radius=0)
        self.main_frame.pack()
        self.main_frame.pack_propagate(False)

        self.main_top_bar = CTkFrame(self.main_frame, height=40,
                                    corner_radius=0, fg_color="#202020")
        self.main_top_bar.pack(side="top", fill="x")
        self.main_top_bar.grid_propagate(False)
        self.main_top_bar.rowconfigure((0, 2), weight=1)

        self.main_scroll = CTkScrollableFrame(self.main_frame, corner_radius=0, fg_color="#444444")
        self.main_scroll.pack(fill="both", expand=True)

        self.main_bottom_bar = CTkFrame(self.main_frame, height=40,
                                    corner_radius=0, fg_color="#202020")
        self.main_bottom_bar.pack(side="bottom", fill="x")

        self.label_fin = CTkLabel(self.main_top_bar, text="Fin.", text_color="white",
                font=("Arial", 20, "bold"))
        self.label_fin.grid(row=1, column=0, padx=(10, 10))
        self.label_title = CTkLabel(self.main_top_bar, text="Título", text_color="white",
                font=("Arial", 20, "bold"))
        self.label_title.grid(row=1, column=1, padx=(10, 30))
        
        CTkButton(self.main_bottom_bar, corner_radius=0,
                text="Adcionar tarefa", height=40, command=self.win_task).pack(side="right")
        
        self.update_list()
        
    # ------------------------ FUNCTIONS ------------------------
    def update_list(self):
        for widget in self.main_scroll.winfo_children():
            widget.destroy()

        if not self.master.tasks:
            CTkLabel(self.main_scroll,
                    text="Nenhuma tarefa disponível!",
                    text_color="white", font=("Arial", 20)).pack(pady=20)
        else:
            for t in self.master.tasks:
                FrameTask(self.main_scroll, t["finished"], t["id"], t["name"], self, self.master)
        save_file(self.master.tasks)
                

    def win_task(self):
        win = CTkToplevel(self.master)
        win.geometry("400x300")
        win.resizable(False, False)
        win.title("Adcionar tarefa")
        win.grab_set()

        CTkLabel(win, text="Nome da tarefa", font=("Arial", 30, "bold")).pack(pady=30)

        entry_task_name = CTkEntry(win, width=230, height=50, font=("Arial", 15))
        entry_task_name.pack()
        entry_task_name.bind("<Return>",
                            lambda event: add_task(entry_task_name.get()))
        
        entry_waring = CTkLabel(win, text="", text_color="yellow")
        entry_waring.pack(pady=20)

        CTkButton(win, text="Adcionar",
                command=lambda: add_task(entry_task_name.get())).pack(pady=(20, 0))
        
        win.after(200, lambda: win.iconbitmap(self.master.dir_icons/"img"/"app.ico"))
        
        
        def add_task(text: str):
            text = text.strip().capitalize()

            if len(text) == 0:
                entry_waring.configure(
                    text="Por favor, preencha o campo!",
                    text_color="yellow")
            else:
                task_id = check_task_id(self.master.tasks)
                entry_waring.configure(
                    text=f"Tarefa \"{text}\" adcionado com sucesso!",
                    text_color="#979797")
                entry_task_name.delete(0, "end")
                self.master.tasks.append({"id": task_id,"name": text, "finished": False})
                self.update_list()

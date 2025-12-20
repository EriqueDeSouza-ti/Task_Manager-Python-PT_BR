from customtkinter import *
from lib.file import save_user_info
from lib.utilitys import check_task_id
from classes.userdata import User

class FrameTask(CTkFrame):
    def __init__(self, master, finished, id, name, home_class, user: User):
        super().__init__(master, height=40, corner_radius=0, fg_color="#646464")
        self.pack(fill="x", pady=2, padx=(0, 0))
        self.rowconfigure((0, 2), weight=1)
        self.grid_propagate(False)

        self.user = user

    # ---------------------- UI COMPONENTS ----------------------
        CTkLabel(self, text=("Sim." if finished else "Não."), text_color="white",
                font=("Arial", 20)).grid(row=1, column=0, padx=(10, 10))
        CTkLabel(self, text=name, text_color="white",
                font=("Arial", 20)).grid(row=1, column=1, padx=(10, 30))
        CTkButton(self, text="Remover", height=30,
                fg_color="#be0101", hover_color="#eb0404",
                corner_radius=0,
                command=lambda: self.remove_task(id, home_class)).pack(side="right", anchor="center")
        
    # ------------------ CONDITIONAL STRUCTURE ------------------
        if not finished:
            CTkButton(self, text="Concluido", height=30,
                    fg_color="#31ad00", hover_color="#47cf12",
                    corner_radius=0,
                    command=lambda: self.check_task(id, home_class)).pack(side="right", anchor="center", padx=5)
        
    # ------------------------ FUNCTIONS ------------------------
    def remove_task(self, id, home_class):
        for i, t in enumerate(self.user.tasks):
            if t["id"] == id:
                del self.user.tasks[i]
                self.destroy()
                home_class.update_list()
                return
                

    def check_task(self, id, home_class):
        for i, t in enumerate(self.user.tasks):
            if t["id"] == id:
                t["finished"] = True
                home_class.update_list()
                return




class WinHome(CTkFrame):
    def __init__(self, master, user: User):
        super().__init__(master, corner_radius=0)

        self.user = user

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
        
        self.entry_task_name = CTkEntry(self.main_bottom_bar, width=200,
                                        height=40, corner_radius=0,
                                        placeholder_text="Adcionar tarefa")
        self.entry_task_name.pack(side="left")
        self.entry_task_name.bind("<Return>", lambda event: self.add_task())

        self.button_add_task = CTkButton(self.main_bottom_bar, corner_radius=0,
                text="Adcionar tarefa", height=40, command=self.add_task)
        self.button_add_task.pack(side="right")
        
        self.update_list()
        
    # ------------------------ FUNCTIONS ------------------------
    def update_list(self):
        for widget in self.main_scroll.winfo_children():
            widget.destroy()

        if not self.user.tasks:
            CTkLabel(self.main_scroll,
                    text="Nenhuma tarefa disponível!",
                    text_color="white", font=("Arial", 20)).pack(pady=20)
        else:
            for t in self.user.tasks:
                FrameTask(self.main_scroll, t["finished"], t["id"], t["name"], self, self.user)
        save_user_info(self.user)
                
        
    def add_task(self):
        text = str(self.entry_task_name.get()).capitalize().strip()

        if len(text) > 0:
            task_id = check_task_id(self.user.tasks)

            self.entry_task_name.delete(0, "end")
            self.user.tasks.append({"id": task_id,"name": text, "finished": False})
            self.update_list()

            

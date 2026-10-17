import customtkinter as ctk

class Login(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.text = ctk.CTkLabel(self,text="wow") ; self.text.pack()
        self.text1 = ctk.CTkLabel(self,text="1wow") ; self.text1.pack()

        self.btn = ctk.CTkButton(self,text="destroy",command=lambda event=None: self.destroy()) ; self.btn.pack()
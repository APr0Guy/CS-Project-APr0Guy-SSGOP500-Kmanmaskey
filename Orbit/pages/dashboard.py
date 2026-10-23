import customtkinter as ctk
from PIL import Image #for loading image
import webbrowser
from pages.sidebar_menu import Sidebar

class Dashboard(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)

        self.configure(fg_color = ("#E2EEF0","#242424")) #(light_mode_color, dark_mode_color) depending on system bg color

        self.grid_columnconfigure((0,1,2,3),weight=1,uniform="half") # 4 columns cause why not
        self.grid_rowconfigure((0,1),weight=1,uniform="half") #so main window is half half and all space is consumed by 2 sides

        self.sidebar_make = Sidebar(self) #sidebar for menu
        self.sidebar_make.grid(column=0,row=0,rowspan=2,sticky="nesw")  #consumes 1/4 of whole screen

        self.working_space = ctk.CTkFrame(self) #consumes 3/4 of whole screen
        self.working_space.grid(column=1,columnspan=3,row=0,rowspan=2,sticky="nesw")
import customtkinter as ctk
from PIL import Image #for loading image

class Login(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color = ("#E2EEF0","#242424")) #(light_mode_color, dark_mode_color) depending on system bg color

        self.grid_columnconfigure((0,1),weight=1,uniform="half") #divides screen into 2 column half of entire screen
        self.grid_rowconfigure(0,weight=1)

        #------------------------------------------------ side image banner for login
        self.side_panel_with_logo = ctk.CTkFrame(self) ; self.side_panel_with_logo.grid(column=0,row=0,sticky="nesw")
        self.side_panel_with_logo.grid_columnconfigure(0,weight=1) #only 1 column so all items inside is centered
        self.side_panel_with_logo.grid_rowconfigure(tuple(i for i in range(10)),weight=1) #divides frame into n rows equally

        self.side_panel_with_logo.configure(fg_color = ("#FBE076","#DD7744"))

                                # ------------------------- Image
        logo_path = r"Orbit\assets\logo.png"

        self.loaded_logo = ctk.CTkImage(light_image = Image.open(logo_path),
                                        dark_image = Image.open(logo_path), size=(300,300)) #using same logo for both

        self.label_logo = ctk.CTkLabel(self.side_panel_with_logo, image=self.loaded_logo, text="")
        self.label_logo.grid(row=0,column=0) #loads image row and col 0 makes it apprear on top

                                # --------------------------- Text
        self.test = ctk.CTkLabel(self.side_panel_with_logo, text="ORBIT",
                                              font=("Segoe Script",35,"bold"))
        self.test.grid(row=1,column=0)
        
        self.catphrase = ctk.CTkLabel(self.side_panel_with_logo, text="Plan smart. Stay in orbit.",
                                      font=("MV Boli",25))
        self.catphrase.grid(row=2,column=0)

        self.text_made_by = ctk.CTkLabel(self.side_panel_with_logo,font=("Segoe Script",20),
                text="Project By:\n - APr0Guy [UI]\n - SSGOP500 [Connecting UI and Database]\n - Kmanmaskey [Database]")
        self.text_made_by.grid(row=6,column=0)
        #------------------------------------------------
        #------------------------------------------------ side login
        self.side_panel_login = ctk.CTkFrame(self) ; self.side_panel_login.grid(column=1,row=0,sticky="nesw")
        self.side_panel_login.grid_columnconfigure(tuple(i for i in range(5)),weight=1) #3 equal column
        self.side_panel_login.grid_rowconfigure(tuple(i for i in range(50)),weight=1) #50 equal rows

                                # --------------------------- Input
        self.user_container = ctk.CTkFrame(self.side_panel_login,fg_color="transparent",border_width=1,corner_radius=8,
                border_color=("#FBE076","#DD7744")) #(light_mode_color, dark_mode_color) depending on system bg color
        self.user_container.grid(column=1,row=10,sticky="ew")
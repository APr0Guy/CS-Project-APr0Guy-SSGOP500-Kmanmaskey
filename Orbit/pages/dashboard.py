import customtkinter as ctk
from PIL import Image #for loading image
import webbrowser

class Dashboard(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)

        self.configure(fg_color = ("#E2EEF0","#242424")) #(light_mode_color, dark_mode_color) depending on system bg color

        self.grid_columnconfigure((0,1,2,3),weight=1,uniform="half") # 4 columns cause why not
        self.grid_rowconfigure((0,1),weight=1,uniform="half") #so main window is half half and all space is consumed by 2 sides

        self.side_menu = ctk.CTkFrame(self,fg_color=("#FC5C3D", "#D4AF37")) #consumes 1/4 of whole screen
        self.side_menu.grid(column=0,row=0,rowspan=2,sticky="nesw") 

        self.working_space = ctk.CTkFrame(self) #consumes 3/4 of whole screen
        self.working_space.grid(column=1,columnspan=3,row=0,rowspan=2,sticky="nesw")

        # ----------------------------------- side menu
        self.side_menu.grid_columnconfigure((0),weight=1) #so all is centered
        self.side_menu.grid_rowconfigure(tuple(i for i in range(100)),weight=1)
        self.side_menu.propagate(False)

                                # logo and app name

        self.title_holder = ctk.CTkFrame(self.side_menu,fg_color="transparent",height=100)
        self.title_holder.grid(column=0,row=0,sticky="ew",padx=5)
        self.title_holder.grid_columnconfigure(tuple(i for i in range(50)),weight=1,uniform="half")
        self.title_holder.grid_rowconfigure((0),weight=1) #so all is centered
        self.title_holder.propagate(False) #so it donesnt increase size

        self.icon_path_light = r"Orbit\assets\old_logo.png"
        self.icon_path_dark = r"Orbit\assets\old_logo.png"
        self.icon_loaded_logo = ctk.CTkImage(light_image=Image.open(self.icon_path_light),
                                      dark_image=Image.open(self.icon_path_dark),size=(100,100))
        self.icon_label = ctk.CTkLabel(self.title_holder,text="",image=self.icon_loaded_logo)
        self.icon_label.grid(column=0,row=0,padx=5,columnspan=2,pady=1)

        self.logo_name_title = ctk.CTkLabel(self.title_holder,text="Orbit",font=("Arial",25,"bold"),text_color=("white","black"))
        self.logo_name_title.grid(column=15,row=0,columnspan=5)

        for i in [self.title_holder,self.logo_name_title,self.icon_label]: #makes all items inside frame open website
            i.bind("<Button-1>",lambda event:webbrowser.open("https://github.com/APr0Guy/CS-Project-APr0Guy-SSGOP500-Kmanmaskey"))

                                # dashboard menu
        self.dashboard_frame_side_menu = ctk.CTkFrame(self.side_menu,height=50,fg_color="transparent")
        self.dashboard_frame_side_menu.grid(column=0,row=5,sticky="ew",padx=5)
        self.dashboard_frame_side_menu.grid_columnconfigure(tuple(i for i in range(10)),weight=1,uniform="half")
        self.dashboard_frame_side_menu.grid_rowconfigure((0),weight=1) #so all is centered
        self.dashboard_frame_side_menu.propagate(False) #so it donesnt increase size

        self.house_icon_path_dark = r"Orbit\assets\house_(dark_mode).png"
        self.house_icon_path_light = r"Orbit\assets\house_(light_mode).png"
        self.house_loaded_icon = ctk.CTkImage(light_image=Image.open(self.house_icon_path_light),
                        dark_image=Image.open(self.house_icon_path_dark),size=(30,30))
        self.house_icon_label = ctk.CTkLabel(self.dashboard_frame_side_menu,text="",image=self.house_loaded_icon)
        self.house_icon_label.grid(row=0,column=0,padx=5,pady=5,columnspan=2)

        self.dashboard_side_menu_text_label = ctk.CTkLabel(self.dashboard_frame_side_menu,text="   Dashboard",
                        font = ("Arial",20),justify="center",text_color=("white","black"))
        self.dashboard_side_menu_text_label.grid(row=0,column=0,columnspan=10)

        for i in [self.dashboard_frame_side_menu,self.house_icon_label,self.dashboard_side_menu_text_label]:
            i.bind("<Enter>",lambda event=None:self.change_bg_color_enter_side_menu(self.dashboard_frame_side_menu))
            i.bind("<Leave>",lambda event=None:self.change_bg_color_leave_side_menu(self.dashboard_frame_side_menu))

                                # calendar menu
        self.calendar_frame_side_menu = ctk.CTkFrame(self.side_menu,height=50,fg_color="transparent")
        self.calendar_frame_side_menu.grid(column=0,row=6,sticky="ew",padx=5)
        self.calendar_frame_side_menu.grid_columnconfigure(tuple(i for i in range(10)),weight=1,uniform="half")
        self.calendar_frame_side_menu.grid_rowconfigure((0),weight=1) #so all is centered
        self.calendar_frame_side_menu.propagate(False) #so it donesnt increase size

        self.calendar_icon_path_dark = r"Orbit\assets\calendar_(dark_mode).png"
        self.calendar_icon_path_light = r"Orbit\assets\calendar_(light_mode).png"
        self.calendar_loaded_icon = ctk.CTkImage(light_image=Image.open(self.calendar_icon_path_light),
                        dark_image=Image.open(self.calendar_icon_path_dark),size=(30,30))
        self.calendar_icon_label = ctk.CTkLabel(self.calendar_frame_side_menu,text="",image=self.calendar_loaded_icon)
        self.calendar_icon_label.grid(row=0,column=0,padx=5,pady=5,columnspan=2)

        self.calendar_side_menu_text_label = ctk.CTkLabel(self.calendar_frame_side_menu,text="   Calendar",
                        font = ("Arial",20),justify="center",text_color=("white","black"))
        self.calendar_side_menu_text_label.grid(row=0,column=0,columnspan=10)

        for i in [self.calendar_frame_side_menu,self.calendar_icon_label,self.calendar_side_menu_text_label]:
            i.bind("<Enter>",lambda event=None:self.change_bg_color_enter_side_menu(self.calendar_frame_side_menu))
            i.bind("<Leave>",lambda event=None:self.change_bg_color_leave_side_menu(self.calendar_frame_side_menu))

                                # notes menu
        self.notes_frame_side_menu = ctk.CTkFrame(self.side_menu,height=50,fg_color="transparent")
        self.notes_frame_side_menu.grid(column=0,row=7,sticky="ew",padx=5)
        self.notes_frame_side_menu.grid_columnconfigure(tuple(i for i in range(10)),weight=1,uniform="half")
        self.notes_frame_side_menu.grid_rowconfigure((0),weight=1) #so all is centered
        self.notes_frame_side_menu.propagate(False) #so it donesnt increase size

        self.notes_icon_path_dark = r"Orbit\assets\notes_(dark_mode).png"
        self.notes_icon_path_light = r"Orbit\assets\notes_(light_mode).png"
        self.notes_loaded_icon = ctk.CTkImage(light_image=Image.open(self.notes_icon_path_light),
                        dark_image=Image.open(self.notes_icon_path_dark),size=(40,40))
        self.notes_icon_label = ctk.CTkLabel(self.notes_frame_side_menu,text="",image=self.notes_loaded_icon)
        self.notes_icon_label.grid(row=0,column=0,padx=5,pady=5,columnspan=2)

        self.notes_side_menu_text_label = ctk.CTkLabel(self.notes_frame_side_menu,text="   Notes",
                        font = ("Arial",20),justify="center",text_color=("white","black"))
        self.notes_side_menu_text_label.grid(row=0,column=0,columnspan=10)

        for i in [self.notes_frame_side_menu,self.notes_icon_label,self.notes_side_menu_text_label]:
            i.bind("<Enter>",lambda event=None:self.change_bg_color_enter_side_menu(self.notes_frame_side_menu))
            i.bind("<Leave>",lambda event=None:self.change_bg_color_leave_side_menu(self.notes_frame_side_menu))

                                # weather menu
        self.weather_frame_side_menu = ctk.CTkFrame(self.side_menu,height=50,fg_color="transparent")
        self.weather_frame_side_menu.grid(column=0,row=8,sticky="ew",padx=5)
        self.weather_frame_side_menu.grid_columnconfigure(tuple(i for i in range(10)),weight=1,uniform="half")
        self.weather_frame_side_menu.grid_rowconfigure((0),weight=1) #so all is centered
        self.weather_frame_side_menu.propagate(False) #so it donesnt increase size

        self.weather_icon_path_dark = r"Orbit\assets\weather_(dark_mode).png"
        self.weather_icon_path_light = r"Orbit\assets\weather_(light_mode).png"
        self.weather_loaded_icon = ctk.CTkImage(light_image=Image.open(self.weather_icon_path_light),
                        dark_image=Image.open(self.weather_icon_path_dark),size=(45,45))
        self.weather_icon_label = ctk.CTkLabel(self.weather_frame_side_menu,text="",image=self.weather_loaded_icon)
        self.weather_icon_label.grid(row=0,column=0,padx=5,pady=5,columnspan=2)

        self.weather_side_menu_text_label = ctk.CTkLabel(self.weather_frame_side_menu,text="   Weather",
                        font = ("Arial",20),justify="center",text_color=("white","black"))
        self.weather_side_menu_text_label.grid(row=0,column=0,columnspan=10)

        for i in [self.weather_frame_side_menu,self.weather_icon_label,self.weather_side_menu_text_label]:
            i.bind("<Enter>",lambda event=None:self.change_bg_color_enter_side_menu(self.weather_frame_side_menu))
            i.bind("<Leave>",lambda event=None:self.change_bg_color_leave_side_menu(self.weather_frame_side_menu))

                                # settings menu
        


    #change bg color of that frame when entering
    def change_bg_color_enter_side_menu(self,main_frame):
        main_frame.configure(fg_color=("#FBE076", "#374151"))

    #sets bg to default
    def change_bg_color_leave_side_menu(self,main_frame):
        main_frame.configure(fg_color="transparent")
import customtkinter as ctk
from PIL import Image #for loading image
import webbrowser #for opening url when clicking logo and all

class Login(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.configure(fg_color = ("#E2EEF0","#242424")) #(light_mode_color, dark_mode_color) depending on system bg color

        self.grid_columnconfigure((0,1),weight=1,uniform="half") #divides screen into 2 column half of entire screen
        self.grid_rowconfigure(0,weight=1)

        self.pass_visibility_change = {"Login":False,"Sign Up":False} #for password showing or not
        #------------------------------------------------ side image banner for login
        self.side_panel_with_logo = ctk.CTkFrame(self) ; self.side_panel_with_logo.grid(column=0,row=0,sticky="nesw")
        self.side_panel_with_logo.grid_columnconfigure(0,weight=1) #only 1 column so all items inside is centered
        self.side_panel_with_logo.grid_rowconfigure(tuple(i for i in range(10)),weight=1) #divides frame into n rows equally

        self.side_panel_with_logo.configure(fg_color = ("#FBE076","#D4AF37"))
        self.side_panel_with_logo.bind("<Button-1>", #opens github page when clicking left side
            lambda event:webbrowser.open("https://github.com/APr0Guy/CS-Project-APr0Guy-SSGOP500-Kmanmaskey"))

                                # ------------------------- Image
        logo_path_dark = r"Orbit\assets\logo.png"
        logo_path_light = r"Orbit\assets\old_logo.png"

        self.loaded_logo = ctk.CTkImage(light_image = Image.open(logo_path_light),
                                        dark_image = Image.open(logo_path_dark), size=(300,300)) #using same logo for both

        self.label_logo = ctk.CTkLabel(self.side_panel_with_logo, image=self.loaded_logo, text="")
        self.label_logo.grid(row=0,column=0) #loads image row and col 0 makes it apprear on top

                                # --------------------------- Text
        self.test = ctk.CTkLabel(self.side_panel_with_logo, text="ORBIT", text_color="black",
                                              font=("Segoe Script",35,"bold"))
        self.test.grid(row=1,column=0)
        
        self.catphrase = ctk.CTkLabel(self.side_panel_with_logo, text="Plan smart. Stay in orbit.", text_color="black",
                                      font=("MV Boli",25))
        self.catphrase.grid(row=2,column=0)

        self.text_made_by = ctk.CTkLabel(self.side_panel_with_logo,font=("Courier New",20), text_color="black",
                text="Project By:\n - APr0Guy [UI]\n - SSGOP500 [Connecting UI and Database]\n - Kmanmaskey [Database]")
        self.text_made_by.grid(row=4,column=0)

        self.caution = ctk.CTkLabel(self.side_panel_with_logo, text="Click anywhere on this side to open github page", text_color="black")
        self.caution.grid(row=9,column=0)
        #------------------------------------------------
        #------------------------------------------------ side login
        self.side_panel_login = ctk.CTkFrame(self) ; self.side_panel_login.grid(column=1,row=0,sticky="nesw")
        self.side_panel_login.grid_columnconfigure(tuple(i for i in range(5)),weight=1) #3 equal column
        self.side_panel_login.grid_rowconfigure(tuple(i for i in range(50)),weight=1) #50 equal rows

                                # --------------------------- options - login or sign up
        self.login_or_signup_container = ctk.CTkFrame(self.side_panel_login,fg_color="transparent") 
        self.login_or_signup_container.grid(column=1,row=10,columnspan=3,sticky="ew",padx=10)
        self.login_or_signup_container.grid_columnconfigure((0,1),weight=1,uniform="half")
    
        self.tab_seperator = ctk.CTkFrame(self.login_or_signup_container,height=2,fg_color="#E5E7EB",corner_radius=0)
        self.tab_seperator.grid(row=1, column=0, columnspan=2, sticky="ew")

        self.active_line = ctk.CTkFrame(self.login_or_signup_container,height=3,fg_color=("#FC5C3D", "#D4AF37"),corner_radius=0)
        self.active_line.grid(row=1, column=0, sticky="ew") #(light_mode,dark_mode) for color

                                # --------------------------- Login / signup btn
        self.login_switch_btn = ctk.CTkButton(self.login_or_signup_container,text="Login",height=38,fg_color="transparent",
                text_color=("#FC5C3D", "#D4AF37"),hover_color=("#374151", "#E5E7EB"),corner_radius=8,
                font=("Arial", 14, "bold"), command=lambda: self.change_mode("Login"))
        self.login_switch_btn.grid(row=0, column=0, sticky="ew")

        self.signup_btn = ctk.CTkButton(self.login_or_signup_container,text="Sign Up",height=38,fg_color="transparent",
                text_color=("#FC5C3D", "#D4AF37"),hover_color=("#374151", "#E5E7EB"),corner_radius=8,
                font=("Arial", 14, "bold"), command=lambda: self.change_mode("Sign Up"))
        self.signup_btn.grid(row=0, column=1, sticky="ew")



        # login side
                                # --------------------------- Input - user / email
        self.user_container = ctk.CTkFrame(self.side_panel_login,fg_color="transparent",border_width=2,corner_radius=8,
            height=44,border_color=("#FC5C3D","#D4AF37")) #(light_mode_color, dark_mode_color) depending on system bg color
        self.user_container.grid(column=1,row=15,sticky="ew",columnspan=3)
        self.user_container.grid_rowconfigure(0,weight=1) ; self.user_container.grid_columnconfigure(1,weight=1)
        self.user_container.propagate(False) #so frame wont change size to fit more children widget added into it

        self.user_logo_path_dark = r"Orbit\assets\user_logo_(dark_mode).png"
        self.user_logo_path_light = r"Orbit\assets\user_logo_(light_mode).png"
        self.loaded_user_logo = ctk.CTkImage(light_image=Image.open(self.user_logo_path_light),
                                             dark_image=Image.open(self.user_logo_path_dark),size=(18,18))

        self.user_icon = ctk.CTkLabel(self.user_container,image=self.loaded_user_logo,text="")
        self.user_icon.grid(row=0,column=0,padx=(12, 6))

        self.user_input = ctk.CTkEntry(self.user_container,placeholder_text="Username / Email",fg_color="transparent",
                                       border_width=0,height=28,corner_radius=0,font=("Arial", 13))
        self.user_input.grid(row=0,column=1,padx=(0, 8),sticky="ew",pady=8) 
        #padx = (a,b)  <-a->|object|<-b-> spacing || padx = a  <-a->|object|<-a->

                                # --------------------------- Input - password
        
        self.pass_container = ctk.CTkFrame(self.side_panel_login,fg_color="transparent",border_color=("#FC5C3D","#D4AF37"),
                                           height=44,border_width=2,corner_radius=8)
        self.pass_container.grid(row=17,column=1,sticky="ew",columnspan=3)
        self.pass_container.grid_rowconfigure(0,weight=1) ; self.pass_container.grid_columnconfigure(1,weight=1)
        self.pass_container.propagate(False)

        self.pass_logo_path_light = r"Orbit\assets\padlock_(light_mode).png"
        self.pass_logo_path_dark = r"Orbit\assets\padlock_(dark_mode).png"
        self.loaded_pass_logo = ctk.CTkImage(light_image=Image.open(self.pass_logo_path_light),
                dark_image=Image.open(self.pass_logo_path_dark),size=(18,18))

        self.pass_icon = ctk.CTkLabel(self.pass_container,text="",image=self.loaded_pass_logo)
        self.pass_icon.grid(row=0,column=0,padx=(12,6))

        self.pass_input = ctk.CTkEntry(self.pass_container,placeholder_text="Password",border_width=0,
                                       show="*",fg_color="transparent")
        self.pass_input.grid(row=0,column=1,pady=8,padx=(0,8),sticky="ew")

        self.pass_show_logo_path_darkmode = r"Orbit\assets\hide_pass_(dark_mode).png" 
        self.pass_show_logo_path_lightmode = r"Orbit\assets\hide_pass_(light_mode).png"
        self.loaded_pass_show_logo = ctk.CTkImage(light_image=Image.open(self.pass_show_logo_path_lightmode),
                                                dark_image=Image.open(self.pass_show_logo_path_darkmode),size=(20,20))
        self.show_pass = ctk.CTkButton(self.pass_container,text="",image=self.loaded_pass_show_logo,
                                       width=20,fg_color="transparent",hover_color=("#FC5C3D","#D4AF37"))
        self.show_pass.grid(row=0,column=2,padx=(0,8))

        self.show_pass.bind("<Button-1>",lambda event:self.change_pass_visibility("Login"))
        
                                # --------------------------- login btn / create new account
        self.holder_login_create_container = ctk.CTkFrame(self.side_panel_login,fg_color="transparent")
        self.holder_login_create_container.grid(row=24,column = 1,columnspan=3,sticky="nesw")
        self.holder_login_create_container.grid_columnconfigure(1,weight=1)
        self.holder_login_create_container.grid_rowconfigure((0,1,2),weight=1)


        self.login_btn = ctk.CTkButton(self.holder_login_create_container,text="Login",height=44,
            hover_color=("#374151","#E5E7EB"),text_color=("white","black"),font=("Arial",15),
            fg_color=("#FC5C3D","#D4AF37"))
        self.login_btn.grid(row=0,column = 1,sticky="nesw")

        self.or_label_middle = ctk.CTkLabel(self.holder_login_create_container,text_color="grey",
            text="----------------------------------------  or  ----------------------------------------")
        self.or_label_middle.grid(row=1,column = 1,sticky="ew")

        self.create_new_acc_btn = ctk.CTkButton(self.holder_login_create_container,text="Create new account",height=44,font=("Arial",15),
            hover_color=("#D9816F","#DDC881"),text_color=("white","black"),
            fg_color="#66738D",command=lambda: self.change_mode("Sign Up"))
        self.create_new_acc_btn.grid(row=2,column = 1,sticky="nesw")


        # sign up side
                        # --------------------------- Input - user
        self.user_container_sign_up = ctk.CTkFrame(self.side_panel_login,fg_color="transparent",border_width=2,corner_radius=8,
            height=44,border_color=("#FC5C3D","#D4AF37")) #(light_mode_color, dark_mode_color) depending on system bg color
        self.user_container_sign_up.grid(column=1,row=15,sticky="ew",columnspan=3)
        self.user_container_sign_up.grid_rowconfigure(0,weight=1) ; self.user_container_sign_up.grid_columnconfigure(1,weight=1)
        self.user_container_sign_up.propagate(False) #so frame wont change size to fit more children widget added into it

        self.user_icon_sign_up = ctk.CTkLabel(self.user_container_sign_up,image=self.loaded_user_logo,text="") 
        #image is from up login page side
        self.user_icon_sign_up.grid(row=0,column=0,padx=(12, 6))

        self.user_input_signup = ctk.CTkEntry(self.user_container_sign_up,placeholder_text="Username / Email",fg_color="transparent",
                                       border_width=0,height=28,corner_radius=0,font=("Arial", 13))
        self.user_input_signup.grid(row=0,column=1,padx=(0, 8),sticky="ew",pady=8) 
        
                        # --------------------------- Input - email
        self.email_container = ctk.CTkFrame(self.side_panel_login,fg_color="transparent",border_color=("#FC5C3D","#D4AF37"),
                                           height=44,border_width=2,corner_radius=8)
        self.email_container.grid(row=17,column=1,sticky="ew",columnspan=3)
        self.email_container.grid_rowconfigure(0,weight=1) ; self.email_container.grid_columnconfigure(1,weight=1)
        self.email_container.propagate(False)

        self.email_logo_path_light = r"Orbit\assets\email_(light_mode).png"
        self.email_logo_path_dark = r"Orbit\assets\email_(dark_mode).png"
        self.loaded_email_logo = ctk.CTkImage(light_image=Image.open(self.email_logo_path_light),
                dark_image=Image.open(self.email_logo_path_dark),size=(18,18))

        self.pass_icon = ctk.CTkLabel(self.email_container,text="",image=self.loaded_email_logo)
        self.pass_icon.grid(row=0,column=0,padx=(12,6))

        self.email_input = ctk.CTkEntry(self.email_container,placeholder_text="Email",border_width=0,fg_color="transparent")
        self.email_input.grid(row=0,column=1,pady=8,padx=(0,8),sticky="ew")

        self.send_code = ctk.CTkButton(self.email_container,text="Send Code",width=20,fg_color="transparent",
                    hover_color=("#FC5C3D","#D4AF37"),text_color=("black","white"))
        self.send_code.grid(row=0,column=2,padx=(0,8))

                        # --------------------------- Input - pass and comfirm pass
                                    #           pass
        self.pass_container_sign_up = ctk.CTkFrame(self.side_panel_login,fg_color="transparent",border_color=("#FC5C3D","#D4AF37"),
                                           height=44,border_width=2,corner_radius=8)
        self.pass_container_sign_up.grid(row=19,column=1,sticky="ew",columnspan=3)
        self.pass_container_sign_up.grid_rowconfigure(0,weight=1) ; self.pass_container_sign_up.grid_columnconfigure(1,weight=1)
        self.pass_container_sign_up.propagate(False)

        self.pass_icon_sign_up = ctk.CTkLabel(self.pass_container_sign_up,text="",image=self.loaded_pass_logo)
        #pass logo is up
        self.pass_icon_sign_up.grid(row=0,column=0,padx=(12,6))

        self.pass_input_sign_up = ctk.CTkEntry(self.pass_container_sign_up,placeholder_text="Password",border_width=0,
                                       show="*",fg_color="transparent")
        self.pass_input_sign_up.grid(row=0,column=1,pady=8,padx=(0,8),sticky="ew")

        self.show_pass_sign_up = ctk.CTkButton(self.pass_container_sign_up,text="",image=self.loaded_pass_show_logo,
                                       width=20,fg_color="transparent",hover_color=("#FC5C3D","#D4AF37"))
        #logo is from up
        self.show_pass_sign_up.grid(row=0,column=2,padx=(0,8))
        self.show_pass_sign_up.bind("<Button-1>",lambda event:self.change_pass_visibility("Sign Up"))

                                    #           conf pass
        self.conf_pass_container_sign_up = ctk.CTkFrame(self.side_panel_login,fg_color="transparent",border_color=("#FC5C3D","#D4AF37"),
                                           height=44,border_width=2,corner_radius=8)
        self.conf_pass_container_sign_up.grid(row=21,column=1,sticky="ew",columnspan=3)
        self.conf_pass_container_sign_up.grid_rowconfigure(0,weight=1) ; self.conf_pass_container_sign_up.grid_columnconfigure(1,weight=1)
        self.conf_pass_container_sign_up.propagate(False)

        self.conf_pass_icon_sign_up = ctk.CTkLabel(self.conf_pass_container_sign_up,text="",image=self.loaded_pass_logo)
        #pass logo is up
        self.conf_pass_icon_sign_up.grid(row=0,column=0,padx=(12,6))

        self.conf_pass_input_sign_up = ctk.CTkEntry(self.conf_pass_container_sign_up,placeholder_text="Password",border_width=0,
                                       show="*",fg_color="transparent")
        self.conf_pass_input_sign_up.grid(row=0,column=1,pady=8,padx=(0,8),sticky="ew")

        self.conf_show_pass_sign_up = ctk.CTkButton(self.conf_pass_container_sign_up,text="",image=self.loaded_pass_show_logo,
                                       width=20,fg_color="transparent",hover_color=("#FC5C3D","#D4AF37"))
        #logo is from up
        self.conf_show_pass_sign_up.grid(row=0,column=2,padx=(0,8))
        self.conf_show_pass_sign_up.bind("<Button-1>",lambda event:self.change_pass_visibility("Sign Up"))

                                # --------------------------- create new account / login

        self.holder_login_create_container_sign_up = ctk.CTkFrame(self.side_panel_login,fg_color="transparent")
        self.holder_login_create_container_sign_up.grid(row=28,column = 1,columnspan=3,sticky="nesw")
        self.holder_login_create_container_sign_up.grid_columnconfigure(1,weight=1)
        self.holder_login_create_container_sign_up.grid_rowconfigure((0,1,2),weight=1)


        self.create_new_acc_btn_sign_up = ctk.CTkButton(self.holder_login_create_container_sign_up,text="Create new account",height=44,
                font=("Arial",15),hover_color=("#374151","#E5E7EB"),text_color=("white","black"),fg_color=("#FC5C3D","#D4AF37"),
                command=lambda: self.change_mode("Sign Up"))
        self.create_new_acc_btn_sign_up.grid(row=0,column = 1,sticky="nesw")

        self.or_label_middle_sign_up = ctk.CTkLabel(self.holder_login_create_container_sign_up,text_color="grey",
            text="----------------------------------------  or  ----------------------------------------")
        self.or_label_middle_sign_up.grid(row=1,column = 1,sticky="ew")

        self.login_btn_sign_up = ctk.CTkButton(self.holder_login_create_container_sign_up,text="Login",height=44,font=("Arial",15),
            hover_color=("#D9816F","#DDC881"),text_color=("white","black"),fg_color="#66738D")
        self.login_btn_sign_up.grid(row=2,column = 1,sticky="nesw")


        #------------------------------------------------
        self.change_mode("Login") #cause once sign up containers load they replace login containers

    #------------------------------------------------ all functions to be used
    #function to change mdoe between sign up and login
    def change_mode(self,mode):
        if mode == "Login":
            self.active_line.grid_configure(column=0)

            #re-grids all login containers
            self.user_container.grid(column=1,row=15,sticky="ew",columnspan=3)
            self.pass_container.grid(row=17,column=1,sticky="ew",columnspan=3)
            self.holder_login_create_container.grid(row=24,column = 1,columnspan=3,sticky="nesw")

            #removes all sign up containers
            self.user_container_sign_up.grid_forget()
            self.email_container.grid_forget()
            self.pass_container_sign_up.grid_forget()
            self.conf_pass_container_sign_up.grid_forget()
            self.holder_login_create_container_sign_up.grid_forget()

        else: #sign-up
            self.active_line.grid_configure(column=1)

            #re-grids all login containers
            self.user_container_sign_up.grid(column=1,row=15,sticky="ew",columnspan=3)
            self.email_container.grid(row=17,column=1,sticky="ew",columnspan=3)
            self.pass_container_sign_up.grid(row=19,column=1,sticky="ew",columnspan=3)
            self.conf_pass_container_sign_up.grid(row=21,column=1,sticky="ew",columnspan=3)
            self.holder_login_create_container_sign_up.grid(row=28,column = 1,columnspan=3,sticky="nesw")

            #removes all login containers
            self.user_container.grid_forget()
            self.pass_container.grid_forget()
            self.holder_login_create_container.grid_forget()

    #for changing pass showing and not showing
    def change_pass_visibility(self,mode):
        self.pass_visibility_change[mode] = not(self.pass_visibility_change[mode]) #changes value of that mode

        if self.pass_visibility_change[mode]:
            self.pass_show_logo_path_darkmode = r"Orbit\assets\show_pass_(dark_mode).png" 
            self.pass_show_logo_path_lightmode = r"Orbit\assets\show_pass_(light_mode).png"
            self.loaded_pass_show_logo = ctk.CTkImage(light_image=Image.open(self.pass_show_logo_path_lightmode),
            dark_image=Image.open(self.pass_show_logo_path_darkmode),size=(20,20))

            #changes visibility of that only
            if mode == "Login":
                self.pass_input.configure(show="")  
            else:
                self.pass_input_sign_up.configure(show="") #does both at once show pass in sign up and conf show pass
                self.conf_pass_input_sign_up.configure(show="")
        else:
            self.pass_show_logo_path_darkmode = r"Orbit\assets\hide_pass_(dark_mode).png" 
            self.pass_show_logo_path_lightmode = r"Orbit\assets\hide_pass_(light_mode).png"
            self.loaded_pass_show_logo = ctk.CTkImage(light_image=Image.open(self.pass_show_logo_path_lightmode),
                    dark_image=Image.open(self.pass_show_logo_path_darkmode),size=(20,20))

            #changes visibility of that only
            if mode == "Login":
                self.pass_input.configure(show="*")  
            else:
                self.pass_input_sign_up.configure(show="*") #does both at once show pass in sign up and conf show pass
                self.conf_pass_input_sign_up.configure(show="*")

        if mode == "Login":
            self.show_pass.configure(image=self.loaded_pass_show_logo)  
        else: #does both at once show pass in sign up and conf show pass
            self.show_pass_sign_up.configure(image=self.loaded_pass_show_logo)
            self.conf_show_pass_sign_up.configure(image=self.loaded_pass_show_logo)
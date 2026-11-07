import customtkinter as ctk
from PIL import Image #for loading image
from tkinter import messagebox
from database import db

class Settings(ctk.CTkFrame):
    def __init__(self,parent,user=None,on_logout=None,on_theme_change=None):
        super().__init__(parent)

        self.user = user or {}
        self.user_id = self.user.get("id",0)
        self.on_logout = on_logout
        self.on_theme_change = on_theme_change
        self.current_tab = "Profile"
        self.settings_data = db.get_user_settings(self.user_id)
        self.configure(fg_color=("#E2EEF0","#242424")) #(light_mode_color, dark_mode_color) depending on system bg color
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)

        # ------------------------ settings heading
        self.heading_label = ctk.CTkLabel(self,text="Settings",font=("Arial",25,"bold"),text_color=("#1F2937","#F3F4F6"),anchor="w")
        self.heading_label.grid(row=0,column=0,sticky="w",padx=20,pady=(18,12))

        # ------------------------ settings body
        self.settings_body = ctk.CTkFrame(self,fg_color=("#FFFFFF","#30343B"),corner_radius=14)
        self.settings_body.grid(row=1,column=0,sticky="nesw",padx=20,pady=(0,20))
        self.settings_body.grid_columnconfigure(1,weight=1)
        self.settings_body.grid_rowconfigure(0,weight=1)

        self.settings_menu = ctk.CTkFrame(self.settings_body,fg_color=("#F8FAFC","#282D34"),corner_radius=0,width=165)
        self.settings_menu.grid(row=0,column=0,sticky="nesw")
        self.settings_menu.grid_columnconfigure(0,weight=1)
        self.settings_tab_buttons = {}
        for index,tab_name in enumerate(["Profile","Appearance","Account"]):
            settings_tab_button = ctk.CTkButton(self.settings_menu,text=tab_name,height=40,anchor="w",fg_color=("#FCE7E3","#393E45") if index == 0 else "transparent",
                text_color=("#FC5C3D","#D4AF37") if index == 0 else ("#475569","#CBD5E1"),hover_color=("#FCE7E3","#51472B"),
                command=lambda selected=tab_name:self.change_tab(selected))
            settings_tab_button.grid(row=index,column=0,sticky="ew",padx=9,pady=(15 if index == 0 else 4,3))
            self.settings_tab_buttons[tab_name] = settings_tab_button
        self.logout_btn = ctk.CTkButton(self.settings_menu,text="Log Out",height=38,fg_color="transparent",text_color=("#FC5C3D","#D4AF37"),
            hover_color=("#FCE7E3","#51472B"),command=self.logout)
        self.logout_btn.grid(row=5,column=0,sticky="ew",pady=(20,12))

        self.settings_content = ctk.CTkFrame(self.settings_body,fg_color="transparent")
        self.settings_content.grid(row=0,column=1,sticky="nesw",padx=22,pady=20)
        self.settings_content.grid_columnconfigure(0,weight=1)

        # ------------------------ profile settings
        self.profile_page = ctk.CTkFrame(self.settings_content,fg_color="transparent")
        self.profile_page.grid(row=0,column=0,sticky="nesw")
        self.profile_page.grid_columnconfigure(0,weight=1)
        ctk.CTkLabel(self.profile_page,text="Profile Settings",font=("Arial",19,"bold"),text_color=("#1F2937","#F3F4F6")).grid(row=0,column=0,sticky="w",pady=(0,15))
        ctk.CTkLabel(self.profile_page,text="Display name",font=("Arial",12,"bold")).grid(row=1,column=0,sticky="w",pady=(0,4))
        self.display_name_input = ctk.CTkEntry(self.profile_page,height=38)
        self.display_name_input.insert(0,self.user.get("display_name",self.user.get("username","")))
        self.display_name_input.grid(row=2,column=0,sticky="ew",pady=(0,12))
        ctk.CTkLabel(self.profile_page,text="Email address",font=("Arial",12,"bold")).grid(row=3,column=0,sticky="w",pady=(0,4))
        self.email_input = ctk.CTkEntry(self.profile_page,height=38)
        self.email_input.insert(0,self.user.get("email",""))
        self.email_input.grid(row=4,column=0,sticky="ew",pady=(0,15))
        self.save_profile_btn = ctk.CTkButton(self.profile_page,text="Save Changes",height=40,fg_color=("#FC5C3D","#D4AF37"),
            hover_color=("#D9816F","#DDC881"),text_color=("white","#242424"),command=self.save_profile)
        self.save_profile_btn.grid(row=5,column=0,sticky="w")

        # ------------------------ appearance settings
        self.appearance_page = ctk.CTkFrame(self.settings_content,fg_color="transparent")
        self.appearance_page.grid(row=0,column=0,sticky="nesw")
        self.appearance_page.grid_columnconfigure(0,weight=1)
        ctk.CTkLabel(self.appearance_page,text="Appearance",font=("Arial",19,"bold"),text_color=("#1F2937","#F3F4F6")).grid(row=0,column=0,sticky="w",pady=(0,8))
        ctk.CTkLabel(self.appearance_page,text="Choose how Orbit looks on this device.",font=("Arial",12),text_color=("#64748B","#A1A1AA")).grid(row=1,column=0,sticky="w",pady=(0,20))
        ctk.CTkLabel(self.appearance_page,text="Theme",font=("Arial",13,"bold")).grid(row=2,column=0,sticky="w",pady=(0,8))
        self.theme_options = ctk.CTkSegmentedButton(self.appearance_page,values=["Light","Dark","System"],height=40,
            selected_color=("#FC5C3D","#D4AF37"),selected_hover_color=("#D9816F","#DDC881"),
            unselected_color=("#F1F5F9","#393E45"),unselected_hover_color=("#FCE7E3","#51472B"),
            text_color=("#1F2937","#F3F4F6"),command=self.apply_theme)
        self.theme_options.set(self.settings_data.get("theme","System"))
        self.theme_options.grid(row=3,column=0,sticky="w",pady=(0,15))
        ctk.CTkLabel(self.appearance_page,text="Light mode uses Orbit's soft blue-grey background and coral accents.\nDark mode uses the charcoal background and gold accents.",
            font=("Arial",12),text_color=("#64748B","#A1A1AA"),justify="left").grid(row=4,column=0,sticky="w")

        # ------------------------ account settings
        self.account_page = ctk.CTkFrame(self.settings_content,fg_color="transparent")
        self.account_page.grid(row=0,column=0,sticky="nesw")
        self.account_page.grid_columnconfigure(0,weight=1)
        ctk.CTkLabel(self.account_page,text="Account",font=("Arial",19,"bold"),text_color=("#1F2937","#F3F4F6")).grid(row=0,column=0,sticky="w",pady=(0,15))
        ctk.CTkLabel(self.account_page,text=f"Username: {self.user.get('username','')}",font=("Arial",13),text_color=("#64748B","#A1A1AA")).grid(row=1,column=0,sticky="w",pady=5)
        ctk.CTkLabel(self.account_page,text=f"Account created: {self.user.get('created_at','')[:10]}",font=("Arial",13),text_color=("#64748B","#A1A1AA")).grid(row=2,column=0,sticky="w",pady=5)
        ctk.CTkLabel(self.account_page,text="Change password",font=("Arial",14,"bold")).grid(row=3,column=0,sticky="w",pady=(20,8))
        self.old_password_input = ctk.CTkEntry(self.account_page,placeholder_text="Current password",show="*",height=38)
        self.old_password_input.grid(row=4,column=0,sticky="ew",pady=5)
        self.new_password_input = ctk.CTkEntry(self.account_page,placeholder_text="New password (at least 6 characters)",show="*",height=38)
        self.new_password_input.grid(row=5,column=0,sticky="ew",pady=5)
        self.change_password_btn = ctk.CTkButton(self.account_page,text="Update Password",height=40,fg_color=("#FC5C3D","#D4AF37"),
            hover_color=("#D9816F","#DDC881"),text_color=("white","#242424"),command=self.change_password)
        self.change_password_btn.grid(row=6,column=0,sticky="w",pady=(8,0))

        self.change_tab("Profile")

    #------------------------------------------------ all functions to be used
    #shows the selected settings page and hides the other ones
    def change_tab(self,tab_name):
        self.current_tab = tab_name
        for name,button in self.settings_tab_buttons.items():
            if name == tab_name:
                button.configure(fg_color=("#FCE7E3","#393E45"),text_color=("#FC5C3D","#D4AF37"))
            else:
                button.configure(fg_color="transparent",text_color=("#475569","#CBD5E1"))
        self.profile_page.grid_forget()
        self.appearance_page.grid_forget()
        self.account_page.grid_forget()
        if tab_name == "Profile":
            self.profile_page.grid(row=0,column=0,sticky="nesw")
        elif tab_name == "Appearance":
            self.appearance_page.grid(row=0,column=0,sticky="nesw")
        else:
            self.account_page.grid(row=0,column=0,sticky="nesw")

    #saves the profile information in sqlite
    def save_profile(self):
        display_name = self.display_name_input.get().strip()
        email = self.email_input.get().strip()
        success,message = db.update_user_profile(self.user_id,display_name,email)
        if success:
            self.user["display_name"] = display_name
            self.user["email"] = email
            messagebox.showinfo("Settings",message,parent=self)
        else:
            messagebox.showerror("Settings",message,parent=self)

    #changes the application appearance mode and saves the choice
    def apply_theme(self,theme):
        ctk.set_appearance_mode(theme)
        db.update_user_settings(self.user_id,theme)
        self.settings_data["theme"] = theme
        if self.on_theme_change:
            self.on_theme_change()

    #changes the account password
    def change_password(self):
        old_password = self.old_password_input.get()
        new_password = self.new_password_input.get()
        success,message = db.change_user_password(self.user_id,old_password,new_password)
        if success:
            self.old_password_input.delete(0,"end")
            self.new_password_input.delete(0,"end")
            messagebox.showinfo("Account",message,parent=self)
        else:
            messagebox.showerror("Account",message,parent=self)

    #returns to the login page
    def logout(self):
        if messagebox.askyesno("Log Out","Are you sure you want to log out?",parent=self):
            if self.on_logout:
                self.on_logout()

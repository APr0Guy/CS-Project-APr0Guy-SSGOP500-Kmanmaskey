import customtkinter as ctk
from PIL import Image, ImageSequence, ImageTk #for loading image
import webbrowser
import tkinter as tk
from database import db


class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, user=None):
        super().__init__(parent)
        self.master.state("zoomed") #zooms window ONLY when sidebar opens
        #self.winfo_toplevel().state("zoomed") when you want to maximize Orbit, regardless of which page or frame you're currently inside

        self.user = user or {}
        self.user_id = self.user.get("id",0)
        self.settings_data = db.get_user_settings(self.user_id)
        ctk.set_appearance_mode(self.settings_data.get("theme","System"))
        self.configure(fg_color = ("#E2EEF0","#242424")) #(light_mode_color, dark_mode_color) depending on system bg color
        
        self.grid_columnconfigure((0,1,2,3),weight=1,uniform="half") # 4 columns cause why not
        self.grid_rowconfigure((0,1),weight=1,uniform="half") #so main window is half half and all space is consumed by 2 sides

        # ----------------------------------- side menu
        self.side_menu = ctk.CTkFrame(self, fg_color="transparent")
        self.side_menu.grid(column=0,row=0,rowspan=2,sticky="nesw")  #consumes 1/4 of whole screen

        # ----------------------------------- working side for pages like dashboard, notes etc etc
        self.working_space = ctk.CTkFrame(self,fg_color="transparent")
        self.working_space.grid(column=1,columnspan=3,row=0,rowspan=2,sticky="nesw")

        # ---------- misc items
        #for highlighting selected
        self.toggled = {"Dashboard": False,"Calendar": False,"Notes": False,"Weather": False,"Settings": False}

        #all items
        self.menu_names = ["Dashboard", "Calendar", "Notes", "Weather", "Settings"]

        #for hovering effect
        self.hovered_option = None
        self.option_positions = {}
        self.option_backgrounds = {}
        self.option_icons = {}
        self.option_texts = {}

        # ----------------------------------- animated background
        self.gif_path = r"Orbit\assets\sidebar_menu_orbit.gif"
        self.gif_image = Image.open(self.gif_path)
        self.gif_frames = []

        for frame in ImageSequence.Iterator(self.gif_image):
            self.gif_frames.append(frame.convert("RGBA").copy())

        self.gif_durations = [
            frame.info.get("duration", self.gif_image.info.get("duration", 100))
            for frame in ImageSequence.Iterator(self.gif_image)
        ]

        #same canvas for gif + logo + text + options so no solid widget bg covers the gif
        self.gif_canvas = tk.Canvas(self.side_menu,highlightthickness=0,bd=0,background="#080B12")
        self.gif_canvas.pack(fill="both", expand=True)
        self.gif_canvas.bind("<Destroy>", self.stop_gif_animation, add="+")
        self.gif_animation_after_id = None

        self.gif_background_item = self.gif_canvas.create_image(0, 0, anchor="nw")

        #when the sidebar changes size, move and resize everything again
        self.gif_canvas.bind("<Configure>", self.resize_gif_background)

        #hover + click events for all options
        self.gif_canvas.bind("<Motion>", self.check_hover_option)
        self.gif_canvas.bind("<Leave>", self.clear_hover_option)
        self.gif_canvas.bind("<Button-1>", self.click_sidebar)

        # ----------------------------------- logo and app name

        self.icon_path_light = r"Orbit\assets\logo.png"
        self.icon_path_dark = r"Orbit\assets\logo.png"
        self.logo_image = Image.open(self.icon_path_light).convert("RGBA")
        self.logo_photo = None

        #makes the logo and app name open github when clicked
        self.gif_canvas.bind("<Button-1>", self.click_sidebar)

        # ----------------------------------- menu icons

        #all the icons used in the sidebar
        self.icon_paths_dark = { #cause light mode dark icons look better
            "Dashboard": r"Orbit\assets\house_(light_mode).png",
            "Calendar": r"Orbit\assets\calendar_(light_mode).png",
            "Notes": r"Orbit\assets\notes_(light_mode).png",
            "Weather": r"Orbit\assets\weather_(light_mode).png",
            "Settings": r"Orbit\assets\settings_(light_mode).png"
        }
        self.icon_paths = {
            "Dashboard": r"Orbit\assets\house_(dark_mode).png",
            "Calendar": r"Orbit\assets\calendar_(dark_mode).png",
            "Notes": r"Orbit\assets\notes_(dark_mode).png",
            "Weather": r"Orbit\assets\weather_(dark_mode).png",
            "Settings": r"Orbit\assets\settings_(dark_mode).png"
        }

        self.menu_icon_images = {}

        for name, path in self.icon_paths.items():
            #loads each icon once so it doesnt have to load every time
            self.menu_icon_images[name] = Image.open(path).convert("RGBA")

        #draws the logo and menu items after the canvas gets its size
        self.after(0, self.draw_sidebar_items)

        #starts the gif animation
        self.after(0,lambda: self.animate_gif_background(0))
        #------------------------------------------------
        self.change_mode_side_bar("Dashboard") #cause when user first logs in it shows dashboard

    #------------------------------------------------ all functions to be used
    #makes points for rounded rectangle cause canvas doesnt have corner_radius like ctk
    def rounded_rectangle_points(self, x1, y1, x2, y2, radius):
        radius = min(radius, (x2 - x1) / 2, (y2 - y1) / 2)

        return [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]

    def draw_sidebar_items(self, event=None): #draw all sidebar items
        if not self.winfo_exists():
            return

        width = max(self.gif_canvas.winfo_width(), 1)
        height = max(self.gif_canvas.winfo_height(), 1)

        if ctk.get_appearance_mode() == "Dark":
            for name,path in self.icon_paths_dark.items():
                self.menu_icon_images[name] = Image.open(path).convert("RGBA")
        else:
            for name,path in self.icon_paths.items():
                self.menu_icon_images[name] = Image.open(path).convert("RGBA")

        #removes old text, icons and rectangles but keeps the gif background item
        self.gif_canvas.delete("sidebar_item")

        #keeps the gif as the very back item
        self.gif_canvas.tag_lower(self.gif_background_item)

        # ----------------------------------- logo and app name
        #logo size changes depending on sidebar width
        logo_size = min(75, max(45, int(width * 0.28)))
        resized_logo = self.logo_image.resize((logo_size, logo_size),Image.Resampling.LANCZOS)

        self.logo_photo = ImageTk.PhotoImage(resized_logo)

        #logo is on the left side of the header
        self.gif_canvas.create_image(width * 0.25,55,image=self.logo_photo,tags=("sidebar_item", "github_header"))

        if ctk.get_appearance_mode() == "Dark": #app name / dark mode
            self.gif_canvas.create_text(width * 0.66,55,text="Orbit",fill="#D4AF37",tags=("sidebar_item", "github_header"),
                    font=("Arial", max(18, min(25, int(width * 0.09))), "bold")) # gold text color
        else: #app name / dark mode
            self.gif_canvas.create_text(width * 0.66,55,text="Orbit",fill="#FC5C3D",tags=("sidebar_item", "github_header"),
                    font=("Arial", max(18, min(25, int(width * 0.09))), "bold")) # orange text color

        # ----------------------------------- menu options
        #positions are based on sidebar height so it can fit different screen sizes
        option_height = max(38, min(50, int(height * 0.062)))
        gap = max(3, int(height * 0.006))
        start_y = max(115, int(height * 0.205))

        #if there isnt enough space, reduce the gaps a little
        total_needed = len(self.menu_names) * option_height + (len(self.menu_names) - 1) * gap
        if start_y + total_needed > height:
            gap = 2
            option_height = max(32, int((height - start_y - 10 - 4 * gap) / 5))

        self.option_positions = {}

        for index, name in enumerate(self.menu_names):
            top = start_y + index * (option_height + gap)
            bottom = top + option_height

            self.option_positions[name] = (top, bottom)

            #background rectangle is transparent until hovered or selected
            bg = self.gif_canvas.create_polygon(
                self.rounded_rectangle_points(4, top, width - 4, bottom, 12),
                fill="", outline="", smooth=True, splinesteps=24,
                tags=("sidebar_item", name)
            )
            self.option_backgrounds[name] = bg

            #menu icon
            icon_size = min(30, max(20, int(option_height * 0.58)))
            resized_icon = self.menu_icon_images[name].resize((icon_size, icon_size),Image.Resampling.LANCZOS)

            #keep references so tkinter doesnt remove the images
            photo = ImageTk.PhotoImage(resized_icon)
            self.option_icons[name] = photo

            self.gif_canvas.create_image(width * 0.16,(top + bottom) / 2,image=photo,tags=("sidebar_item", name))

            if ctk.get_appearance_mode() == "Dark": #menu text / Dark mode
                self.gif_canvas.create_text(width * 0.57,(top + bottom) / 2,text=name,fill="#D4AF37", #gold text color
                        font=("Arial", max(15, min(20, int(width * 0.075))),),tags=("sidebar_item", name))
            else: #menu text / Light mode
                self.gif_canvas.create_text(width * 0.57,(top + bottom) / 2,text=name,fill="#FC5C3D", #orange text color
                        font=("Arial", max(15, min(20, int(width * 0.075))),),tags=("sidebar_item", name))


        #puts the backgrounds behind the icons and text
        for name in self.menu_names:
            self.gif_canvas.tag_lower(self.option_backgrounds[name], self.gif_background_item)
            #the line above puts the rectangle behind the gif, so raise it back above the gif
            self.gif_canvas.tag_raise(self.option_backgrounds[name], self.gif_background_item)

        #updates selected/hovered colours after redrawing
        self.update_option_backgrounds()

    def check_hover_option(self, event): #check which option is being hovered
        hovered_name = None

        #checks if the mouse is inside one of the option rows
        for name, (top, bottom) in self.option_positions.items():
            if top <= event.y <= bottom:
                hovered_name = name
                break

        if hovered_name != self.hovered_option:
            self.hovered_option = hovered_name
            self.update_option_backgrounds()

    def clear_hover_option(self, event=None):#sets hover back to nothing when mouse leaves the sidebar
        self.hovered_option = None
        self.update_option_backgrounds()

    # ----------------------------------- change background colours
    def update_option_backgrounds(self):
        if not hasattr(self, "option_backgrounds"):
            return

        for name, bg in self.option_backgrounds.items():
            if self.toggled[name]:
                #clicked option stays grey blue ish
                self.gif_canvas.itemconfigure(bg,fill="#51472B" if ctk.get_appearance_mode() == "Dark" else "#FCE1DA",stipple="")
            elif name == self.hovered_option:
                #hover effect - blueish  background
                self.gif_canvas.itemconfigure(bg,fill="#393E45" if ctk.get_appearance_mode() == "Dark" else "#FFEDE8",stipple="")
            else:
                #normal state - no background so gif can show through
                self.gif_canvas.itemconfigure(bg,fill="",stipple="")

    # ----------------------------------- clicking options
    def click_sidebar(self, event):
        #clicks on the logo/header opens github
        if event.y < 100:
            webbrowser.open("https://github.com/APr0Guy/CS-Project-APr0Guy-SSGOP500-Kmanmaskey")
            return

        #checks which option was clicked
        for name, (top, bottom) in self.option_positions.items():
            if top <= event.y <= bottom:
                self.change_mode_side_bar(name)
                return

    #highlights selected mode
    def change_mode_side_bar(self, name):
        if name not in self.toggled:
            return

        if not self.toggled[name]:
            for key in self.toggled:
                self.toggled[key] = False #makes everything else not selected

            self.toggled[name] = True #only the current item is toggled true
            self.update_option_backgrounds()


            self.working_space.destroy() #removing working space removes all elements of other page already on it

            self.working_space = ctk.CTkFrame(self,fg_color="transparent") #makes working space again
            self.working_space.grid(column=1,columnspan=3,row=0,rowspan=2,sticky="nesw")

            # pages working space
            if name == "Dashboard":
                from pages.dashboard import Dashboard
                dashboard_working_space_make = Dashboard(self.working_space,self.user)
                dashboard_working_space_make.pack(fill="both", expand=True)

            elif name == "Notes":
                from pages.notes import Notes
                notes_working_space_make = Notes(self.working_space,self.user)
                notes_working_space_make.pack(fill="both", expand=True)

            elif name == "Calendar":
                from pages.calendar import Calendar
                calendar_working_space_make = Calendar(self.working_space,self.user)
                calendar_working_space_make.pack(fill="both", expand=True)

            elif name == "Weather":
                from pages.weather import Weather
                weather_working_space_make = Weather(self.working_space)
                weather_working_space_make.pack(fill="both", expand=True)

            elif name == "Settings":
                from pages.settings import Settings
                settings_working_space_make = Settings(self.working_space,self.user,self.logout,self.update_sidebar_theme)
                settings_working_space_make.pack(fill="both", expand=True)

    #updates sidebar icons and text after the appearance mode changes
    def update_sidebar_theme(self):
        self.settings_data = db.get_user_settings(self.user_id)
        self.draw_sidebar_items()
        self.update_option_backgrounds()

    #returns to login when the user logs out
    def logout(self):
        self.destroy()
        from pages.login import Login
        login_page_start = Login(self.master)
        login_page_start.pack(fill="both",expand=True)

    # ----------------------------------- animated background functions
    def resize_gif_background(self, event=None):
        if not self.winfo_exists():
            return

        if hasattr(self, "gif_canvas"):
            self.gif_canvas.coords(self.gif_background_item, 0, 0)
            self.draw_sidebar_items()

    def stop_gif_animation(self, event=None):
        if self.gif_animation_after_id is not None:
            try:
                self.after_cancel(self.gif_animation_after_id)
            except tk.TclError:
                pass
            self.gif_animation_after_id = None

    def animate_gif_background(self, index):
        if not self.winfo_exists() or not self.gif_canvas.winfo_exists():
            return

        width = max(self.gif_canvas.winfo_width(), 1)
        height = max(self.gif_canvas.winfo_height(), 1)

        #resizes the current gif frame to fit the sidebar
        frame = self.gif_frames[index].resize((width, height),Image.Resampling.LANCZOS)

        self.gif_bg_photo = ImageTk.PhotoImage(frame)

        self.gif_canvas.itemconfigure(self.gif_background_item,image=self.gif_bg_photo)

        #makes sure the gif stays behind the logo, text and options
        self.gif_canvas.tag_lower(self.gif_background_item)

        delay = max(self.gif_durations[index], 20)
        next_index = (index + 1) % len(self.gif_frames)

        self.gif_animation_after_id = self.after(delay,lambda: self.animate_gif_background(next_index))
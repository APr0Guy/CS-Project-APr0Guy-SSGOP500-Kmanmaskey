import customtkinter as ctk
from PIL import Image #for loading image
import calendar as calendar_module
from datetime import date, datetime
from tkinter import messagebox
from database import db
from paths import resource_path

class Calendar(ctk.CTkFrame):
    def __init__(self,parent,user=None):
        super().__init__(parent)

        self.user = user or {}
        self.user_id = self.user.get("id",0)
        self.current_date = date.today()
        self.selected_date = date.today()
        self.day_buttons = []
        self.configure(fg_color=("#E2EEF0","#242424")) #(light_mode_color, dark_mode_color) depending on system bg color
        self.grid_columnconfigure(0,weight=2)
        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(1,weight=1)

        # ------------------------ calendar heading
        self.heading_frame = ctk.CTkFrame(self,fg_color="transparent")
        self.heading_frame.grid(row=0,column=0,columnspan=2,sticky="ew",padx=20,pady=(18,12))
        self.heading_frame.grid_columnconfigure(0,weight=1)

        self.heading_label = ctk.CTkLabel(self.heading_frame,text="Calendar",font=("Arial",25,"bold"),text_color=("#1F2937","#F3F4F6"))
        self.heading_label.grid(row=0,column=0,sticky="w")
        self.add_event_btn = ctk.CTkButton(self.heading_frame,text="+ Add Event",height=36,fg_color=("#FC5C3D","#D4AF37"),
            hover_color=("#D9816F","#DDC881"),text_color=("white","#242424"),command=self.open_event_window)
        self.add_event_btn.grid(row=0,column=1,sticky="e")

        # ------------------------ month calendar
        self.month_frame = ctk.CTkFrame(self,fg_color=("#FFFFFF","#30343B"),corner_radius=14)
        self.month_frame.grid(row=1,column=0,sticky="nesw",padx=(20,8),pady=(0,20))
        self.month_frame.grid_columnconfigure(0,weight=1)
        self.month_frame.grid_rowconfigure(2,weight=1)

        self.month_heading_frame = ctk.CTkFrame(self.month_frame,fg_color="transparent")
        self.month_heading_frame.grid(row=0,column=0,sticky="ew",padx=14,pady=12)
        self.month_heading_frame.grid_columnconfigure(1,weight=1)
        self.previous_month_btn = ctk.CTkButton(self.month_heading_frame,text="‹",width=35,height=32,fg_color="transparent",font=("Arial",27,"bold"),
            text_color=("#1F2937","#F3F4F6"),hover_color=("#F1F5F9","#393E45"),command=lambda:self.change_month(-1))
        self.previous_month_btn.grid(row=0,column=0,padx=(0,4))
        self.month_label = ctk.CTkLabel(self.month_heading_frame,text="",font=("Arial",17,"bold"),text_color=("#1F2937","#F3F4F6"))
        self.month_label.grid(row=0,column=1)
        self.next_month_btn = ctk.CTkButton(self.month_heading_frame,text="›",width=35,height=32,fg_color="transparent",font=("Arial",27,"bold"),
            text_color=("#1F2937","#F3F4F6"),hover_color=("#F1F5F9","#393E45"),command=lambda:self.change_month(1))
        self.next_month_btn.grid(row=0,column=2,padx=(0,4))
        self.today_btn = ctk.CTkButton(self.month_heading_frame,text="Today",width=55,height=30,fg_color=("#FC5C3D","#D4AF37"),
            hover_color=("#D9816F","#DDC881"),text_color=("white","#242424"),command=self.go_to_today)
        self.today_btn.grid(row=0,column=3,padx=(8,0))

        self.weekday_frame = ctk.CTkFrame(self.month_frame,fg_color="transparent")
        self.weekday_frame.grid(row=1,column=0,sticky="ew",padx=10)
        self.weekday_frame.grid_columnconfigure((0,1,2,3,4,5,6),weight=1,uniform="days")
        for index,weekday in enumerate(["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]):
            ctk.CTkLabel(self.weekday_frame,text=weekday,font=("Arial",11,"bold"),text_color=("#64748B","#A1A1AA")).grid(row=0,column=index,sticky="ew",pady=8)

        self.days_frame = ctk.CTkFrame(self.month_frame,fg_color="transparent")
        self.days_frame.grid(row=2,column=0,sticky="nesw",padx=10,pady=(0,12))
        self.days_frame.grid_columnconfigure((0,1,2,3,4,5,6),weight=1,uniform="days")
        self.days_frame.grid_rowconfigure((0,1,2,3,4,5),weight=1,uniform="weeks")

        # ------------------------ selected date events
        self.events_panel = ctk.CTkFrame(self,fg_color=("#FFFFFF","#30343B"),corner_radius=14)
        self.events_panel.grid(row=1,column=1,sticky="nesw",padx=(8,20),pady=(0,20))
        self.events_panel.grid_columnconfigure(0,weight=1)
        self.events_panel.grid_rowconfigure(2,weight=1)

        self.selected_date_label = ctk.CTkLabel(self.events_panel,text="Events",font=("Arial",18,"bold"),text_color=("#1F2937","#F3F4F6"))
        self.selected_date_label.grid(row=0,column=0,sticky="w",padx=16,pady=(15,2))
        self.selected_date_subtitle = ctk.CTkLabel(self.events_panel,text="Select a date to view events",font=("Arial",12),text_color=("#64748B","#A1A1AA"))
        self.selected_date_subtitle.grid(row=1,column=0,sticky="w",padx=16,pady=(0,10))
        self.event_list_frame = ctk.CTkScrollableFrame(self.events_panel,fg_color="transparent")
        self.event_list_frame.grid(row=2,column=0,sticky="nesw",padx=10,pady=(0,12))
        self.event_list_frame.grid_columnconfigure(0,weight=1)

        self.draw_calendar()
        self.refresh_selected_events()

    #------------------------------------------------ all functions to be used
    #moves the calendar forward or backward by one month
    def change_month(self,amount):
        month_number = self.current_date.month + amount
        year_number = self.current_date.year
        if month_number < 1:
            month_number = 12
            year_number -= 1
        elif month_number > 12:
            month_number = 1
            year_number += 1
        self.current_date = self.current_date.replace(year=year_number,month=month_number,day=1)
        self.selected_date = self.current_date
        self.draw_calendar()
        self.refresh_selected_events()

    #returns the calendar to today's date
    def go_to_today(self):
        self.current_date = date.today()
        self.selected_date = date.today()
        self.draw_calendar()
        self.refresh_selected_events()

    #draws all days and highlights the selected date
    def draw_calendar(self):
        self.month_label.configure(text=self.current_date.strftime("%B %Y"))
        for widget in self.days_frame.winfo_children():
            widget.destroy()
        month_days = calendar_module.Calendar(firstweekday=6).monthdayscalendar(self.current_date.year,self.current_date.month)
        events = db.get_events(self.user_id,self.current_date.replace(day=1).isoformat(),
            self.current_date.replace(day=calendar_module.monthrange(self.current_date.year,self.current_date.month)[1]).isoformat())
        event_dates = [event["event_date"] for event in events]

        for row_index,week in enumerate(month_days):
            for column_index,day_number in enumerate(week):
                if day_number == 0:
                    ctk.CTkLabel(self.days_frame,text="",fg_color="transparent").grid(row=row_index,column=column_index,sticky="nesw",padx=2,pady=2)
                else:
                    day_date = date(self.current_date.year,self.current_date.month,day_number)
                    is_selected = day_date == self.selected_date
                    has_event = day_date.isoformat() in event_dates
                    if is_selected:
                        button_color = ("#FC5C3D","#D4AF37")
                        text_color = ("white","#242424")
                    elif day_date == date.today():
                        button_color = ("#FCE7E3","#51472B")
                        text_color = ("#FC5C3D","#D4AF37")
                    else:
                        button_color = "transparent"
                        text_color = ("#1F2937","#F3F4F6")
                    day_text = f"{day_number}\n•" if has_event else str(day_number)
                    day_button = ctk.CTkButton(self.days_frame,text=day_text,height=54,corner_radius=9,fg_color=button_color,
                        hover_color=("#FCE7E3","#51472B"),text_color=text_color,font=("Arial",18,"bold"),
                        command=lambda chosen_date=day_date:self.select_date(chosen_date))
                    day_button.grid(row=row_index,column=column_index,sticky="nesw",padx=2,pady=2)

    #updates the selected date and event list
    def select_date(self,chosen_date):
        self.selected_date = chosen_date
        self.draw_calendar()
        self.refresh_selected_events()

    #shows the events saved for the selected date
    def refresh_selected_events(self):
        self.selected_date_label.configure(text=self.selected_date.strftime("%d %B %Y"))
        self.selected_date_subtitle.configure(text=self.selected_date.strftime("%A"))
        for widget in self.event_list_frame.winfo_children():
            widget.destroy()
        events = db.get_events(self.user_id,self.selected_date.isoformat(),self.selected_date.isoformat())
        if not events:
            ctk.CTkLabel(self.event_list_frame,text="Nothing planned for this day.",font=("Arial",12),text_color=("#64748B","#A1A1AA")).grid(row=0,column=0,sticky="w",pady=10)
        for index,event in enumerate(events):
            event_card = ctk.CTkFrame(self.event_list_frame,fg_color=("#F1F5F9","#393E45"),corner_radius=10)
            event_card.grid(row=index,column=0,sticky="ew",pady=5)
            event_card.grid_columnconfigure(0,weight=1)
            ctk.CTkLabel(event_card,text=event["title"],font=("Arial",13,"bold"),text_color=("#1F2937","#F3F4F6"),anchor="w").grid(row=0,column=0,sticky="ew",padx=10,pady=(9,2))
            ctk.CTkLabel(event_card,text=event["event_time"] or "All day",font=("Arial",11),text_color=("#FC5C3D","#D4AF37"),anchor="w").grid(row=1,column=0,sticky="w",padx=10,pady=(0,2))
            if event["description"]:
                ctk.CTkLabel(event_card,text=event["description"],font=("Arial",11),text_color=("#64748B","#A1A1AA"),anchor="w",wraplength=220).grid(row=2,column=0,sticky="w",padx=10,pady=(0,8))
            ctk.CTkButton(event_card,text="Delete",width=55,height=25,fg_color="transparent",text_color=("#FC5C3D","#D4AF37"),
                hover_color=("#FCE7E3","#51472B"),command=lambda event_id=event["id"]:self.remove_event(event_id)).grid(row=0,column=1,rowspan=2,padx=7)

    #opens a small window to add an event to the selected date
    def open_event_window(self):
        self.event_window = ctk.CTkToplevel(self)
        self.event_window.title("Add Event")
        self.event_window.resizable(False,False)
        self.event_window.transient(self.winfo_toplevel())
        self.event_window.grab_set()
        self.event_window.grid_columnconfigure(0,weight=1)
        self.event_window.iconbitmap(resource_path("assets/logo.ico")) #logo

        ctk.CTkLabel(self.event_window,text="Add New Calendar Event",font=("Arial",20,"bold"),text_color=("#1F2937","#F3F4F6")).grid(row=0,column=0,sticky="w",padx=24,pady=(22,14))
        ctk.CTkLabel(self.event_window,text="Event title",font=("Arial",12,"bold")).grid(row=1,column=0,sticky="w",padx=24)
        self.event_title_input = ctk.CTkEntry(self.event_window,placeholder_text="e.g. Physics test",height=38)
        self.event_title_input.grid(row=2,column=0,sticky="ew",padx=24,pady=(4,12))
        ctk.CTkLabel(self.event_window,text="Date (YYYY-MM-DD)",font=("Arial",12,"bold")).grid(row=3,column=0,sticky="w",padx=24)
        self.event_date_input = ctk.CTkEntry(self.event_window,height=38)
        self.event_date_input.insert(0,self.selected_date.isoformat())
        self.event_date_input.grid(row=4,column=0,sticky="ew",padx=24,pady=(4,12))
        ctk.CTkLabel(self.event_window,text="Time (optional)",font=("Arial",12,"bold")).grid(row=5,column=0,sticky="w",padx=24)
        self.event_time_input = ctk.CTkEntry(self.event_window,placeholder_text="e.g. 10:00 AM",height=38)
        self.event_time_input.grid(row=6,column=0,sticky="ew",padx=24,pady=(4,12))
        ctk.CTkLabel(self.event_window,text="Description (optional)",font=("Arial",12,"bold")).grid(row=7,column=0,sticky="w",padx=24)
        self.event_description_input = ctk.CTkEntry(self.event_window,placeholder_text="Add a little detail",height=38)
        self.event_description_input.grid(row=8,column=0,sticky="ew",padx=24,pady=(4,15))
        ctk.CTkButton(self.event_window,text="Save Event",height=40,fg_color=("#FC5C3D","#D4AF37"),text_color=("white","#242424"),
            hover_color=("#D9816F","#DDC881"),command=self.save_event).grid(row=9,column=0,sticky="ew",padx=24,pady=(0,22))

    #validates and saves a new calendar event
    def save_event(self):
        title = self.event_title_input.get().strip()
        event_date = self.event_date_input.get().strip()
        event_time = self.event_time_input.get().strip()
        description = self.event_description_input.get().strip()
        try:
            datetime.strptime(event_date,"%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid date","Enter the date in YYYY-MM-DD format.",parent=self.event_window)
            return
        if not title:
            messagebox.showwarning("Missing title","Enter an event title.",parent=self.event_window)
            return
        db.add_event(self.user_id,title,description,event_date,event_time)
        self.selected_date = datetime.strptime(event_date,"%Y-%m-%d").date()
        self.current_date = self.selected_date.replace(day=1)
        self.event_window.destroy()
        self.draw_calendar()
        self.refresh_selected_events()

    #deletes the selected event
    def remove_event(self,event_id):
        if messagebox.askyesno("Delete event","Delete this event?",parent=self):
            db.delete_event(event_id,self.user_id)
            self.draw_calendar()
            self.refresh_selected_events()

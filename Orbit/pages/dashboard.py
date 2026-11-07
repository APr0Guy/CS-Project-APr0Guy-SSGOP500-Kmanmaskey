import customtkinter as ctk
from PIL import Image #for loading image
from datetime import date, datetime
from database import db

class Dashboard(ctk.CTkFrame):
    def __init__(self,parent,user=None):
        super().__init__(parent)

        self.user = user or {}
        self.user_id = self.user.get("id", 0)
        self.configure(fg_color= ("#E2EEF0", "#242424")) #(light_mode_color, dark_mode_color) depending on system bg color

        self.grid_columnconfigure((0,1),weight=1,uniform="half")
        self.grid_rowconfigure(3,weight=1)

        # all frames used 2 half one for task and event other for welcome quick widget etc
        # ------------------------ welcome area
        self.welcome_frame = ctk.CTkFrame(self,fg_color="transparent")
        self.welcome_frame.grid(row=0,column=0,columnspan=2,sticky="ew",padx=22,pady=(18,8))
        self.welcome_frame.grid_columnconfigure(0,weight=1)

        self.welcome_label = ctk.CTkLabel(self.welcome_frame,text=f"Welcome back, {self.user.get('display_name',self.user.get('username','Student'))}!",
            font=("Arial",26,"bold"),text_color=("#1F2937","#F3F4F6"),anchor="w")
        self.welcome_label.grid(row=0,column=0,sticky="w")
        self.welcome_subtitle = ctk.CTkLabel(self.welcome_frame,text="Plan smart. Stay in orbit.",
            font=("Arial",13),text_color=("#64748B","#A1A1AA"),anchor="w")
        self.welcome_subtitle.grid(row=1,column=0,sticky="w",pady=(3,0))
        self.today_label = ctk.CTkLabel(self.welcome_frame,text=date.today().strftime("%A, %d %B %Y"),
            font=("Arial",13,"bold"),text_color=("#FC5C3D","#D4AF37"))
        self.today_label.grid(row=0,column=1,rowspan=2,padx=(10,0))

        # ------------------------ quick summary cards
        self.pending_card = ctk.CTkFrame(self,fg_color=("#FFFFFF","#30343B"),corner_radius=14)
        self.pending_card.grid(row=1,column=0,sticky="nesw",padx=(22,8),pady=8)
        self.pending_card.grid_columnconfigure(0,weight=1)

        self.pending_title = ctk.CTkLabel(self.pending_card,text="Pending Work",font=("Arial",14,"bold"),text_color=("#64748B","#A1A1AA"))
        self.pending_title.grid(row=0,column=0,sticky="w",padx=16,pady=(13,0))
        self.pending_count = ctk.CTkLabel(self.pending_card,text="0",font=("Arial",30,"bold"),text_color=("#FC5C3D","#D4AF37"))
        self.pending_count.grid(row=1,column=0,sticky="w",padx=16,pady=(2,0))
        self.pending_caption = ctk.CTkLabel(self.pending_card,text="Tasks still to complete",font=("Arial",12),text_color=("#64748B","#A1A1AA"))
        self.pending_caption.grid(row=2,column=0,sticky="w",padx=16,pady=(0,13))

        self.upcoming_card = ctk.CTkFrame(self,fg_color=("#FFFFFF","#30343B"),corner_radius=14)
        self.upcoming_card.grid(row=1,column=1,sticky="nesw",padx=(8,22),pady=8)
        self.upcoming_card.grid_columnconfigure(0,weight=1)

        self.upcoming_title = ctk.CTkLabel(self.upcoming_card,text="Upcoming Events",font=("Arial",14,"bold"),text_color=("#64748B","#A1A1AA"))
        self.upcoming_title.grid(row=0,column=0,sticky="w",padx=16,pady=(13,0))
        self.upcoming_count = ctk.CTkLabel(self.upcoming_card,text="0",font=("Arial",30,"bold"),text_color=("#FC5C3D","#D4AF37"))
        self.upcoming_count.grid(row=1,column=0,sticky="w",padx=16,pady=(2,0))
        self.upcoming_caption = ctk.CTkLabel(self.upcoming_card,text="Events on your calendar",font=("Arial",12),text_color=("#64748B","#A1A1AA"))
        self.upcoming_caption.grid(row=2,column=0,sticky="w",padx=16,pady=(0,13))

        # ------------------------ weather widget spans both dashboard columns
        self.weather_frame = ctk.CTkFrame(self,fg_color="transparent")
        self.weather_frame.grid(row=2,column=0,columnspan=2,sticky="nesw",padx=22,pady=8)
        from pages.weather import Weather
        self.weather_widget = Weather(self.weather_frame,compact=True)
        self.weather_widget.pack(fill="both",expand=True)

        # ------------------------ lower dashboard area
        self.task_and_event_frame = ctk.CTkFrame(self,fg_color="transparent")
        self.task_and_event_frame.grid(row=3,column=0,columnspan=2,sticky="nesw",padx=22,pady=(8,18))
        self.task_and_event_frame.grid_columnconfigure((0,1),weight=1,uniform="half")
        self.task_and_event_frame.grid_rowconfigure(0,weight=1)

        self.task_frame = ctk.CTkFrame(self.task_and_event_frame,fg_color=("#FFFFFF","#30343B"),corner_radius=14)
        self.task_frame.grid(row=0,column=0,sticky="nesw",padx=(0,8))
        self.task_frame.grid_columnconfigure(0,weight=1)
        self.task_frame.grid_rowconfigure(3,weight=1)

        self.task_heading = ctk.CTkLabel(self.task_frame,text="Today's Tasks",font=("Arial",17,"bold"),text_color=("#1F2937","#F3F4F6"))
        self.task_heading.grid(row=0,column=0,sticky="w",padx=16,pady=(14,8))

        self.new_task_container = ctk.CTkFrame(self.task_frame,fg_color="transparent")
        self.new_task_container.grid(row=1,column=0,sticky="ew",padx=12,pady=(0,8))
        self.new_task_container.grid_columnconfigure(0,weight=1)
        self.new_task_input = ctk.CTkEntry(self.new_task_container,placeholder_text="Add a task...",height=36)
        self.new_task_input.grid(row=0,column=0,sticky="ew",padx=(0,6))
        self.new_task_input.bind("<Return>",lambda event:self.add_new_task())
        self.new_task_btn = ctk.CTkButton(self.new_task_container,text="Add",width=65,height=36,fg_color=("#FC5C3D","#D4AF37"),
            hover_color=("#D9816F","#DDC881"),text_color=("white","#242424"),command=self.add_new_task)
        self.new_task_btn.grid(row=0,column=1)

        self.task_list_frame = ctk.CTkScrollableFrame(self.task_frame,fg_color="transparent")
        self.task_list_frame.grid(row=3,column=0,sticky="nesw",padx=10,pady=(0,10))
        self.task_list_frame.grid_columnconfigure(0,weight=1)

        self.event_frame = ctk.CTkFrame(self.task_and_event_frame,fg_color=("#FFFFFF","#30343B"),corner_radius=14)
        self.event_frame.grid(row=0,column=1,sticky="nesw",padx=(8,0))
        self.event_frame.grid_columnconfigure(0,weight=1)
        self.event_frame.grid_rowconfigure(1,weight=1)

        self.event_heading = ctk.CTkLabel(self.event_frame,text="Upcoming Events",font=("Arial",17,"bold"),text_color=("#1F2937","#F3F4F6"))
        self.event_heading.grid(row=0,column=0,sticky="w",padx=16,pady=(14,8))
        self.event_list_frame = ctk.CTkScrollableFrame(self.event_frame,fg_color="transparent")
        self.event_list_frame.grid(row=1,column=0,sticky="nesw",padx=10,pady=(0,10))
        self.event_list_frame.grid_columnconfigure(0,weight=1)

        # ------------------------

        self.refresh_dashboard()

    #------------------------------------------------ all functions to be used
    #updates the cards and lists with the latest database information
    def refresh_dashboard(self):
        if not self.winfo_exists():
            return
        task_counts = db.get_task_counts(self.user_id)
        pending_tasks = db.get_tasks(self.user_id,"Pending")
        all_events = db.get_events(self.user_id,date.today().isoformat(),"9999-12-31")
        self.pending_count.configure(text=str(task_counts["pending"]))
        self.upcoming_count.configure(text=str(len(all_events)))

        for widget in self.task_list_frame.winfo_children():
            widget.destroy()
        todays_tasks = [task for task in pending_tasks if not task["due_date"] or task["due_date"] <= date.today().isoformat()]
        if not todays_tasks:
            ctk.CTkLabel(self.task_list_frame,text="No tasks due today. Add one above!",font=("Arial",12),text_color=("#64748B","#A1A1AA")).grid(row=0,column=0,sticky="w",pady=10)
        for index,task in enumerate(todays_tasks):
            self.task_row = ctk.CTkFrame(self.task_list_frame,fg_color=("#F1F5F9","#393E45"),corner_radius=9)
            self.task_row.grid(row=index,column=0,sticky="ew",pady=4)
            self.task_row.grid_columnconfigure(0,weight=1)
            ctk.CTkLabel(self.task_row,text=task["title"],font=("Arial",13),text_color=("#1F2937","#F3F4F6"),anchor="w").grid(row=0,column=0,sticky="ew",padx=10,pady=9)
            ctk.CTkButton(self.task_row,text="Done",width=55,height=27,fg_color=("#FC5C3D","#D4AF37"),
                text_color=("white","#242424"),hover_color=("#D9816F","#DDC881"),command=lambda task_id=task["id"]:self.complete_task(task_id)).grid(row=0,column=1,padx=5,pady=5)

        for widget in self.event_list_frame.winfo_children():
            widget.destroy()
        if not all_events:
            ctk.CTkLabel(self.event_list_frame,text="No upcoming events. Add one in Calendar.",font=("Arial",12),text_color=("#64748B","#A1A1AA")).grid(row=0,column=0,sticky="w",pady=10)
        for index,event in enumerate(all_events[:6]):
            self.event_row = ctk.CTkFrame(self.event_list_frame,fg_color=("#F1F5F9","#393E45"),corner_radius=9)
            self.event_row.grid(row=index,column=0,sticky="ew",pady=4)
            self.event_row.grid_columnconfigure(0,weight=1)
            ctk.CTkLabel(self.event_row,text=event["title"],font=("Arial",13,"bold"),text_color=("#1F2937","#F3F4F6"),anchor="w").grid(row=0,column=0,sticky="ew",padx=10,pady=(7,0))
            event_date = datetime.strptime(event["event_date"],"%Y-%m-%d").strftime("%d %b %Y")
            event_time = event["event_time"] or "All day"
            ctk.CTkLabel(self.event_row,text=f"{event_date}  •  {event_time}",font=("Arial",11),text_color=("#64748B","#A1A1AA"),anchor="w").grid(row=1,column=0,sticky="w",padx=10,pady=(0,7))

    #adds a task from the quick add field
    def add_new_task(self):
        title = self.new_task_input.get().strip()
        if not title:
            return
        db.add_task(self.user_id,title,due_date=date.today().isoformat())
        self.new_task_input.delete(0,"end")
        self.refresh_dashboard()

    #marks a task as completed
    def complete_task(self,task_id):
        db.update_task_status(task_id,self.user_id,"Completed")
        self.refresh_dashboard()
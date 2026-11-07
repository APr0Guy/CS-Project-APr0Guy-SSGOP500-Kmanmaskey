import customtkinter as ctk
from PIL import Image #for loading image
from tkinter import filedialog, messagebox
from pathlib import Path
import shutil
import webbrowser
from database import db

class Notes(ctk.CTkFrame):
    def __init__(self,parent,user=None):
        super().__init__(parent)

        self.user = user or {}
        self.user_id = self.user.get("id",0)
        self.selected_note_id = None
        self.selected_category = "All Notes"
        self.attachment_path = ""
        self.note_categories = ["All Notes","School","Personal","Projects"]
        self.configure(fg_color=("#E2EEF0","#242424")) #(light_mode_color, dark_mode_color) depending on system bg color
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)

        # ------------------------ notes heading
        self.heading_frame = ctk.CTkFrame(self,fg_color="transparent")
        self.heading_frame.grid(row=0,column=0,sticky="ew",padx=18,pady=(16,10))
        self.heading_frame.grid_columnconfigure(0,weight=1)
        self.heading_label = ctk.CTkLabel(self.heading_frame,text="Notes",font=("Arial",25,"bold"),text_color=("#1F2937","#F3F4F6"))
        self.heading_label.grid(row=0,column=0,sticky="w")
        self.new_note_btn = ctk.CTkButton(self.heading_frame,text="+ New Note",height=36,fg_color=("#FC5C3D","#D4AF37"),
            hover_color=("#D9816F","#DDC881"),text_color=("white","#242424"),command=self.new_note)
        self.new_note_btn.grid(row=0,column=1)

        # ------------------------ three note workspace columns
        self.notes_workspace = ctk.CTkFrame(self,fg_color=("#FFFFFF","#30343B"),corner_radius=14)
        self.notes_workspace.grid(row=1,column=0,sticky="nesw",padx=18,pady=(0,18))
        self.notes_workspace.grid_columnconfigure(0,weight=1,minsize=135)
        self.notes_workspace.grid_columnconfigure(1,weight=2,minsize=180)
        self.notes_workspace.grid_columnconfigure(2,weight=5,minsize=300)
        self.notes_workspace.grid_rowconfigure(0,weight=1)

        # ------------------------ note folders
        self.folder_frame = ctk.CTkFrame(self.notes_workspace,fg_color=("#F8FAFC","#282D34"),corner_radius=0)
        self.folder_frame.grid(row=0,column=0,sticky="nesw")
        self.folder_frame.grid_columnconfigure(0,weight=1)
        ctk.CTkLabel(self.folder_frame,text="Folders",font=("Arial",14,"bold"),text_color=("#1F2937","#F3F4F6")).grid(row=0,column=0,sticky="w",padx=13,pady=(17,12))
        self.folder_buttons = {}
        for index,category in enumerate(self.note_categories):
            folder_btn = ctk.CTkButton(self.folder_frame,text=f"▤  {category}",height=36,anchor="w",fg_color=("#FCE7E3","#393E45") if category == "All Notes" else "transparent",
                text_color=("#FC5C3D","#D4AF37") if category == "All Notes" else ("#475569","#CBD5E1"),hover_color=("#FCE7E3","#51472B"),
                command=lambda selected=category:self.change_category(selected))
            folder_btn.grid(row=index+1,column=0,sticky="ew",padx=8,pady=3)
            self.folder_buttons[category] = folder_btn

        # ------------------------ note list
        self.note_list_frame = ctk.CTkFrame(self.notes_workspace,fg_color="transparent")
        self.note_list_frame.grid(row=0,column=1,sticky="nesw",padx=8,pady=8)
        self.note_list_frame.grid_columnconfigure(0,weight=1)
        self.note_list_frame.grid_rowconfigure(2,weight=1)
        ctk.CTkLabel(self.note_list_frame,text="Your Notes",font=("Arial",14,"bold"),text_color=("#1F2937","#F3F4F6")).grid(row=0,column=0,sticky="w",padx=8,pady=(9,7))
        self.search_input = ctk.CTkEntry(self.note_list_frame,placeholder_text="Search notes...",height=34)
        self.search_input.grid(row=1,column=0,sticky="ew",padx=6,pady=(0,8))
        self.search_input.bind("<KeyRelease>",lambda event:self.refresh_note_list())
        self.note_list_scroll = ctk.CTkScrollableFrame(self.note_list_frame,fg_color="transparent")
        self.note_list_scroll.grid(row=2,column=0,sticky="nesw")
        self.note_list_scroll.grid_columnconfigure(0,weight=1)

        # ------------------------ note editor
        self.editor_frame = ctk.CTkFrame(self.notes_workspace,fg_color="transparent")
        self.editor_frame.grid(row=0,column=2,sticky="nesw",padx=(8,15),pady=10)
        self.editor_frame.grid_columnconfigure(0,weight=1)
        self.editor_frame.grid_rowconfigure(4,weight=1)

        self.editor_heading_frame = ctk.CTkFrame(self.editor_frame,fg_color="transparent")
        self.editor_heading_frame.grid(row=0,column=0,sticky="ew",pady=(0,10))
        self.editor_heading_frame.grid_columnconfigure(0,weight=1)
        ctk.CTkLabel(self.editor_heading_frame,text="Edit Note",font=("Arial",16,"bold"),text_color=("#1F2937","#F3F4F6")).grid(row=0,column=0,sticky="w")
        self.delete_note_btn = ctk.CTkButton(self.editor_heading_frame,text="Delete",width=65,height=29,fg_color="transparent",
            text_color=("#FC5C3D","#D4AF37"),hover_color=("#FCE7E3","#51472B"),command=self.delete_note)
        self.delete_note_btn.grid(row=0,column=1)

        self.note_title_input = ctk.CTkEntry(self.editor_frame,placeholder_text="Note title",height=40,font=("Arial",17,"bold"))
        self.note_title_input.grid(row=1,column=0,sticky="ew",pady=(0,8))
        self.note_category_menu = ctk.CTkOptionMenu(self.editor_frame,values=["School","Personal","Projects"],height=32,
            fg_color=("#FC5C3D","#D4AF37"),button_color=("#D9816F","#DDC881"),button_hover_color=("#D9816F","#DDC881"),
            text_color=("white","#242424"))
        self.note_category_menu.set("Personal")
        self.note_category_menu.grid(row=2,column=0,sticky="w",pady=(0,8))
        self.note_content_input = ctk.CTkTextbox(self.editor_frame,corner_radius=9,wrap="word",font=("Arial",13))
        self.note_content_input.grid(row=4,column=0,sticky="nesw",pady=(0,8))
        self.attachment_frame = ctk.CTkFrame(self.editor_frame,fg_color="transparent")
        self.attachment_frame.grid(row=5,column=0,sticky="ew",pady=(0,8))
        self.attachment_frame.grid_columnconfigure(0,weight=1)
        self.attachment_label = ctk.CTkLabel(self.attachment_frame,text="No attachment",font=("Arial",11),text_color=("#64748B","#A1A1AA"),anchor="w")
        self.attachment_label.grid(row=0,column=0,sticky="w")
        self.attachment_btn = ctk.CTkButton(self.attachment_frame,text="Attach file",width=90,height=29,fg_color="transparent",
            text_color=("#FC5C3D","#D4AF37"),hover_color=("#FCE7E3","#51472B"),command=self.attach_file)
        self.attachment_btn.grid(row=0,column=1,padx=(5,0))
        self.open_attachment_btn = ctk.CTkButton(self.attachment_frame,text="Open",width=55,height=29,fg_color="transparent",
            text_color=("#FC5C3D","#D4AF37"),hover_color=("#FCE7E3","#51472B"),command=self.open_attachment)
        self.open_attachment_btn.grid(row=0,column=2,padx=(5,0))
        self.editor_actions_frame = ctk.CTkFrame(self.editor_frame,fg_color="transparent")
        self.editor_actions_frame.grid(row=6,column=0,sticky="ew")
        self.editor_actions_frame.grid_columnconfigure((0,1),weight=1,uniform="actions")
        self.save_note_btn = ctk.CTkButton(self.editor_actions_frame,text="Save Note",height=40,fg_color=("#FC5C3D","#D4AF37"),
            hover_color=("#D9816F","#DDC881"),text_color=("white","#242424"),command=self.save_note)
        self.save_note_btn.grid(row=0,column=0,sticky="ew",padx=(0,5))
        self.export_note_btn = ctk.CTkButton(self.editor_actions_frame,text="Export .txt",height=40,fg_color=("#F1F5F9","#393E45"),
            hover_color=("#FCE7E3","#51472B"),text_color=("#FC5C3D","#D4AF37"),command=self.export_note)
        self.export_note_btn.grid(row=0,column=1,sticky="ew",padx=(5,0))

        self.refresh_note_list()
        self.new_note()

    #------------------------------------------------ all functions to be used
    #changes the folder currently displayed in the note list
    def change_category(self,category):
        self.selected_category = category
        for name,button in self.folder_buttons.items():
            if name == category:
                button.configure(fg_color=("#FCE7E3","#393E45"),text_color=("#FC5C3D","#D4AF37"))
            else:
                button.configure(fg_color="transparent",text_color=("#475569","#CBD5E1"))
        self.refresh_note_list()

    #refreshes the middle column based on folder and search text
    def refresh_note_list(self):
        for widget in self.note_list_scroll.winfo_children():
            widget.destroy()
        notes = db.get_notes(self.user_id,self.selected_category,self.search_input.get())
        if not notes:
            ctk.CTkLabel(self.note_list_scroll,text="No notes found.",font=("Arial",12),text_color=("#64748B","#A1A1AA")).grid(row=0,column=0,sticky="w",pady=10)
        for index,note in enumerate(notes):
            note_button = ctk.CTkButton(self.note_list_scroll,text=f"{note['title']}\n{note['category']}  •  {note['updated_at'][:10]}",
                height=62,anchor="w",fg_color=("#FCE7E3","#393E45") if note["id"] == self.selected_note_id else "transparent",
                text_color=("#1F2937","#F3F4F6"),hover_color=("#F1F5F9","#51472B"),font=("Arial",12),
                command=lambda selected_note=note:self.load_note(selected_note))
            note_button.grid(row=index,column=0,sticky="ew",pady=3)

    #loads a note into the editor
    def load_note(self,note):
        self.selected_note_id = note["id"]
        self.note_title_input.delete(0,"end")
        self.note_title_input.insert(0,note["title"])
        self.note_category_menu.set(note["category"])
        self.note_content_input.delete("1.0","end")
        self.note_content_input.insert("1.0",note["content"] or "")
        self.attachment_path = note["attachment_path"] or ""
        self.attachment_label.configure(text=Path(self.attachment_path).name if self.attachment_path else "No attachment")
        self.refresh_note_list()

    #clears the editor to start a new note
    def new_note(self):
        self.selected_note_id = None
        self.attachment_path = ""
        self.note_title_input.delete(0,"end")
        self.note_category_menu.set("Personal")
        self.note_content_input.delete("1.0","end")
        self.attachment_label.configure(text="No attachment")
        self.refresh_note_list()

    #saves a new note or updates the currently selected note
    def save_note(self):
        title = self.note_title_input.get().strip() or "Untitled note"
        category = self.note_category_menu.get()
        content = self.note_content_input.get("1.0","end-1c")
        if self.selected_note_id:
            db.update_note(self.selected_note_id,self.user_id,title,category,content,self.attachment_path)
        else:
            self.selected_note_id = db.add_note(self.user_id,title,category,content,self.attachment_path)
        messagebox.showinfo("Notes","Note saved successfully.",parent=self)
        self.refresh_note_list()

    #exports the current note as a normal text file
    def export_note(self):
        title = self.note_title_input.get().strip() or "Untitled note"
        content = self.note_content_input.get("1.0","end-1c")
        file_path = filedialog.asksaveasfilename(title="Export Note",defaultextension=".txt",initialfile=f"{title}.txt",
            filetypes=[("Text files","*.txt")])
        if not file_path:
            return
        with open(file_path,"w",encoding="utf-8") as file:
            file.write(f"{title}\n\n{content}")
        messagebox.showinfo("Notes","Note exported successfully.",parent=self)

    #deletes the currently selected note
    def delete_note(self):
        if not self.selected_note_id:
            messagebox.showwarning("Notes","Select a note to delete.",parent=self)
            return
        if messagebox.askyesno("Delete note","Delete this note permanently?",parent=self):
            db.delete_note(self.selected_note_id,self.user_id)
            self.new_note()

    #attaches an image or imports text from a text file
    def attach_file(self):
        file_path = filedialog.askopenfilename(title="Attach a file",filetypes=[("Images and text files","*.png *.jpg *.jpeg *.gif *.txt"),("All files","*.*")])
        if not file_path:
            return
        source_path = Path(file_path)
        if source_path.suffix.lower() == ".txt":
            try:
                with open(source_path,"r",encoding="utf-8") as file:
                    imported_text = file.read()
                self.note_content_input.insert("end",f"\n\n{imported_text}")
                self.attachment_label.configure(text=f"Imported: {source_path.name}")
            except UnicodeDecodeError:
                messagebox.showerror("File error","This text file could not be read as UTF-8.",parent=self)
            return

        attachment_folder = Path(db.DATABASE_PATH).parent / "attachments"
        attachment_folder.mkdir(parents=True,exist_ok=True)
        destination_path = attachment_folder / f"user_{self.user_id}_{source_path.name}"
        shutil.copy2(source_path,destination_path)
        self.attachment_path = str(Path("attachments") / destination_path.name)
        self.attachment_label.configure(text=destination_path.name)

    #opens the currently attached image or file
    def open_attachment(self):
        if not self.attachment_path:
            messagebox.showinfo("Attachment","This note has no saved attachment.",parent=self)
            return
        attachment_file = Path(db.DATABASE_PATH).parent / self.attachment_path
        if attachment_file.exists():
            webbrowser.open(attachment_file.resolve().as_uri())
        else:
            messagebox.showerror("Attachment","The attachment file could not be found.",parent=self)

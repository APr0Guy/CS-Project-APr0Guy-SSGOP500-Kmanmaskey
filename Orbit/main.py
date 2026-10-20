import ctypes #for changing app logo in taskbar
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Orbit")

import customtkinter as ctk
# SSG connect the db and these files all them are in quotes or comments
root = ctk.CTk()

#ctk.set_appearance_mode("Light")  #testing purposes

needed_width = 1100 #<database>.<width>
needed_height = 700 #<database>.<width>
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width - needed_width) // 2
y = (screen_height - needed_height) // 2

root.geometry(f"{needed_width}x{needed_height}+{x}+{y}") #screen centered with offset x and y amount
root.iconbitmap(r"Orbit\assets\logo.ico") #image
'''
if <databse>.<fullscreen>:
    root.state("zoomed")
'''
'''
if <database>.<resizable> == False:
    root.resizable(False,False)
'''
root.title("Orbit")
root.minsize(1100,700) #so user cant decrese size less that this amount
root.configure(fg_color=("#DBDBDB","#242424")) #(light_mode_color, dark_mode_color) depending on system bg color

from pages.login import Login
login_page_start = Login(root) ; login_page_start.pack(fill="both",expand=True) #so the entire window is being used

root.mainloop()
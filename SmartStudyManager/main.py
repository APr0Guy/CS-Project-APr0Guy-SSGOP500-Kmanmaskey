import customtkinter as ctk
# SSG connect the db and these files all them are in quotes or comments
root = ctk.CTk()

needed_width = 1100 #<database>.<width>
needed_height = 700 #<database>.<width>
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width - needed_width) // 2
y = (screen_height - needed_height) // 2

root.geometry(f"{needed_width}x{needed_height}+{x}+{y}") #screen size centered with offset x and y amount
root.iconbitmap(r"SmartStudyManager\assets\logo.ico") #image
'''
if <databse>.<fullscreen>:
    root.state("zoomed")
'''
'''
if <database>.<resizable> == False:
    root.resizable(False,False)
'''
root.title("")
root.minsize(1100,700) #so user cant decrese size less that this amount
root.mainloop()
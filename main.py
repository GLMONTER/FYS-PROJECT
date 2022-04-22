




window = Tk()
window.geometry("800x480")
style = ThemedStyle(window)
style.set_theme("equilux")


# setting attribute
#window.attributes('-fullscreen', True)
leftFrame = ttk.Frame(window, padding=0)
leftFrame.pack(side=LEFT, expand=True, fill='both')
rightFrame = ttk.Frame(window, padding=0)
rightFrame.pack(side=RIGHT, expand=True, fill='both')

ttk.Button(leftFrame, text="Shutdown", command=Shutdown).grid(column=0, row=4)
button = ttk.Button(leftFrame, text="Stop Recording", command=toggleVideo)
button.grid(column=0, row=3)
ttk.Button(leftFrame, text="Save Recording", command=saveVideo).grid(column=0, row=0)
ttk.Button(leftFrame, text="Preview Camera").grid(column=0, row=1)
currentSpeed = Label(rightFrame, height=1, width=3, bg="black", fg="gray", text="55", font=("Arial, 150"))
currentSpeed.grid(column=3, row=0)
readSpeed = Label(rightFrame, height=1, width=3, bg="black", fg="gray", text="50", font=("Arial, 150"))
readSpeed.grid(column=3, row=1)

window.mainloop()


  


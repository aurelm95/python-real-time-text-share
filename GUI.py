import tkinter as tk
import threading

from client import ShareTXT_Client

class ShareTXT_GUI(ShareTXT_Client):
    def __init__(self, width=80, verbose=False):
        self.width=width
        self.verbose=verbose

        self.root = tk.Tk()
        # https://stackoverflow.com/questions/6548837/how-do-i-get-an-event-callback-when-a-tkinter-entry-widget-is-modified
        self.sv = tk.StringVar()
        self.sv.trace("w", lambda name, index, mode, sv=self.sv: self.on_change_text(text=self.sv.get()))
        self.e = tk.Entry(self.root, textvariable=self.sv, width=self.width)
        self.e.pack()

        self.last_text_was_recieved=False
        
    
    def on_change_text(self,text):
        if self.verbose:
            print("on_change_text(): text:",text,"last_text_was_recieved:",self.last_text_was_recieved,end="\r")
        if self.last_text_was_recieved:
            self.last_text_was_recieved=False
            return
        
        
        self.send_text(text)

    # override
    def on_new_text_recieved(self, text):
        self.last_text_was_recieved=True
        self.e.delete(0, tk.END)
        self.last_text_was_recieved=True
        self.e.insert(tk.END,text)

    def start(self):
        # https://stackoverflow.com/questions/11815947/cannot-kill-python-script-with-ctrl-c
        client_thread=threading.Thread(target=self.start_client)
        client_thread.daemon=True
        client_thread.start()

        print("Running GUI...")
        self.root.mainloop()


if __name__=='__main__':
    sg=ShareTXT_GUI()
    sg.start()

# client2.py
#!/usr/bin/env python
import os
import socket
import ast
search_word=str()
option=str()
pageindex=str()

host = 'localhost'
port = 9001
BUFFER_SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

from tkinter import*

def close_window():
    global search_word
    global e
    global window
    search_word=e.get()
    search_word=search_word.lower()
    window.destroy()
    
def option_upload():
    global option
    option="upload"
    master.destroy()
def option_search():
    global option
    option="search"
    master.destroy()

master=Tk()

Button(master, text='UPLOAD', command=option_upload).grid(row=3, column=0, sticky=W, pady=4)
Button(master, text='SEARCH', command=option_search).grid(row=3, column=1, sticky=W, pady=4)
mainloop()


s.send(option.encode('ascii'))

def upload_to_server():
    global directory
    global master
    global dir_entry
    directory=dir_entry.get()
    f=open(directory,'rb')
    read_variable=f.read(2048)
    s.send(read_variable)
    if not read_variable:
        f.close()
    s.close()
    master.destroy()
    print("Successfully Uploaded..!!")
            
def upload():
    global master
    global dir_entry
    master=Tk()
    Label(master,text="DIRECTORY").grid(row=1)
    dir_entry=Entry(master)
    dir_entry.grid(row=1,column=5)
    Button(master,text="UPLOAD",command=upload_to_server).grid(row=2,column=3,sticky=W,pady=4)
    mainloop()    
def assign_index(k):
    global root
    global pageindex
    pageindex=str(k)
    root.destroy()
def search():
    global window
    window=Tk()
    global e
    e = Entry(window)
    e.grid(row=1,column=1)
    Button(window, text='SEARCH', command=close_window).grid(row=3, column=3, sticky=N, pady=4)
    mainloop()
    m = search_word
    message="G:\\package\\htmlfolder\\"+m+".html"
    s.send(m.encode('ascii'))
    d=s.recv(1024)
    d=d.decode('ascii')
    d=ast.literal_eval(d)
    global root
    root=Tk()
    for num in range(len(d)):
        btn=Button(root,text=d[num],command= lambda k=num:assign_index(k))
        btn.pack(side=LEFT)
    mainloop()
    #pageindex=input('Enter the page index  :')
    s.send(pageindex.encode('ascii'))
    with open('G:\\package\\new.html', 'wb') as f:    
        #print ('file opened')
        while True:
            #print('receiving data...')
            data = s.recv(BUFFER_SIZE)
            #print('data=%s', (data))
            if not data:
                f.close()
                #print ('file close()')
                break
            # write data to a file
            f.write(data)
            os .startfile("G:\\package\\new.html")
        

    #print(' get the file')
    s.close()
    print('connection closed')

from tkinter import*
if(option=="upload"):
   upload()
elif(option=="search"):
   search()

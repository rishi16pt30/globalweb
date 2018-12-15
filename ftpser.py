# server2.py
import socket
from threading import Thread
from socketserver import ThreadingMixIn
from urllib import request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter


TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024

class ClientThread(Thread):

    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print( " New thread started for "+ip+":"+str(port))

    def run(self):
        data = conn.recv(1024)
        search=data.decode("ascii")
        print(search)
        htmls=[]
        related=list(open("G:\\package\\npad\\related.txt","r"))
        related=[related[i][:-1] for i in range(len(related))]
        for i in range(len(related)):
            k=[]
            j=[]
            k=related[i].split(":")
            j=list(k[0].split(","))
            if(search in j):
                #print("in j")
                htmls.append(k[1])
        #print(htmls)
        conn.send(str(htmls).encode('ascii'))
        ind=conn.recv(1024)
        ind=int(ind.decode('ascii'))
        mainpage=htmls[ind]
        filename='G:\\package\\htmlfolder\\'+mainpage+'.html'
        f = open(filename,'rb')
        while True:
            l = f.read(BUFFER_SIZE)
            while (l):
                self.sock.send(l)
                l = f.read(BUFFER_SIZE)
            if not l:
                f.close()
                self.sock.close()
                break


    def upload(self):
        with open("G:\\package\\server\\test2.html",'wb') as f:
            print("sever receiving...")
            data=conn.recv(1024)
            html_content=data.decode('ascii')
            #print(data)
            f.write(data)
            f.close()
            self.sock.close()
        html_folder=open("G:\\package\\server\\test2.html").read()
        soup=BeautifulSoup(html_folder)
        for script in soup(["script","style"]):
            script.extract()
        text_in_html=soup.get_text()
        lines=(line.strip() for line in text_in_html.splitlines())
        chunks=(phrase.strip() for line in lines for phrase in line.split(" "))
        text_in_html='\n'.join(chunk for chunk in chunks if chunk)
        text_model=re.findall(r"[\w']+",text_in_html)
        stop_words=set(stopwords.words('english'))
        filtered_sentence=[w for w in text_model if not w in stop_words]
        max_frequency_list=Counter(filtered_sentence).most_common(10)
        #print(max_frequency_list)
        append_word=[]
        for i in max_frequency_list:
            append_word.append(i[0])
        related_string=append_word[0]
        for i in range(len(append_word)-1):
            related_string=related_string+","+append_word[i+1]
        words_htmls=list(open("G:\\package\\npad\\related.txt","r"))
        available_html=[]
        for i in words_htmls:
            temp=[]
            temp=i.split(":")
            available_html.append(temp[1])
        html_name=append_word[0]
        available_html=[available_html[i][:-1] for i in range(len(available_html))]
        #print(available_html)
        for i in range(len(available_html)):
            if (html_name in available_html):
                html_name=html_name+str(i+1)
            if(html_name not in available_html):
                break
        #print(html_name)
        main_line=related_string+":"+html_name
        with open("G:\\package\\npad\\related.txt","a") as related_file:
            related_file.write(main_line)
            related_file.write("\n")
        related_file.close()
        name="G:\\package\\htmlfolder\\"+html_name+".html"
        file=open(name,"w")
        file.write(html_content)
        file.close()
        

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpsock.listen(5)
    print ("Waiting for incoming connections...")
    (conn, (ip,port)) = tcpsock.accept()
    print ('Got connection from ', (ip,port))
    newthread = ClientThread(ip,port,conn)
    client_option=(conn.recv(1024)).decode('ascii')
    #print(client_option)
    if(client_option=="search"):
        newthread.run()
    elif(client_option=="upload"):
        newthread.upload()
    threads.append(newthread)

for t in threads:
    t.join()

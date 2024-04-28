import socket
import threading
import json
import customtkinter 
from customtkinter  import  * 
from CTkMessagebox import CTkMessagebox
from PIL import Image ,ImageTk ,ImageEnhance,ImageFile

background="#06283D" #
Framebg="#081e69"  #
Framefg="#081e69" #
frame3bg="#1a9ce5"
BB="#272A37" #
colore1="#081e69"
colore2="#5eaec8"
global username


global host
global port
global nom
global prenom
global n 
n=0 
z=0
host=socket.gethostbyname(socket.gethostname() )
port=9091


client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((host,port))

def forgetpass ():
    frame1.pack_forget()
    frame5.pack(pady=40,padx=60,fill='both',expand=True,side=LEFT)
    client.send("motdepaaseobl".encode('utf-8'))
def Reinitialiser():
   y=[nom_entryF.get(),prenom_entryF.get(),username_entryF.get(),new_passwordF_entry.get()]
   newpass=new_passwordF_entry.get()
   y=json.dumps(y)
   client.send(y.encode())
   print(y)
   resu=client.recv(1024).decode('utf-8')
   print(resu)
   if resu!="notexit":
      CTkMessagebox(message=f"le mot de passe a été modifé avec succès.\nAncien mot de passe :{resu}\n Nouveau mot de passe :{newpass}",
                  icon="check", option_1="Yes")
      frame5.pack_forget()
      gotologin()
   else :
      CTkMessagebox(title="Erreur", message="Les informations que vous avez saisies incorrect .veuille réessayer.", icon="cancel")
def changernom ():
    global stop_thread    
    global newnom,win
    stop_thread = True  # Arrêtez le thread
    client.send("changer".encode('utf-8'))
    stop_thread = False
    
def changer():
    global username, nom, win
    newuser = newnom.get()
    h = [newuser, username]
    username = newuser
    c = json.dumps(h)
    client.send(c.encode())
    CTkMessagebox(message="le nom d'utilisateur a été modifié avec succès.",
                  icon="check", option_1="Merci")
    global z
    z = 1
    win.pack_forget() 
    frame4.pack(pady=40,padx=60,fill='both',expand=True)
    EXIT()
       
def his() :
   global stop_thread
   stop_thread = True  # Arrêtez le thread
   client.send("his".encode('utf-8'))
   stop_thread = False
def memebres():
   global stop_thread
   stop_thread = True
   client.send("mbr".encode('utf-8'))
   stop_thread = False
def online ():
   global stop_thread
   stop_thread = True
   client.send("online".encode('utf-8'))
   stop_thread = False
def EXIT():

 global z
 frame4.pack_forget()
 username=username_entry.get()
 client.send(f"****{username} a quitté !****".encode('utf-8'))
 client.close()
 root.destroy()

def gotologin():
    print("Login Clicked")
   
    frame2.pack_forget()
    frame1.pack(pady=40,padx=60,fill='both',expand=True,side=LEFT)
    
    
def gotosignup():
    print("Signup Clicked")
    frame1.pack_forget()
    
    frame2.pack(pady=40,padx=60,fill='both',expand=True,side=LEFT)
   
def hidepass ():
  bthide=CTkButton(frame1, height = 1, width = 12, image=tk_img ,command=showpass ,text="",
                      fg_color=Framebg)
  bthide.place(relx=0.92,rely=0.362)
  password_entry.configure(show='*')

def showpass():
 bthide=CTkButton(frame1, height = 1, width = 12, image=tkh_img ,text="",
                      fg_color=Framebg,command=hidepass)
 bthide.place(relx=0.92,rely=0.362)
 
 password_entry.configure(show='')

def msgeframe():
        client.send("CL1".encode('utf-8')) 
        frame1.pack_forget()
        frame2.pack_forget()
        frame3.pack_forget()
        frame4.pack(pady=40,padx=60,fill='both',expand=True)
        clientactive()
        
def creenewclient():
      client.send("signup".encode('utf-8')) 
      clients=[]
      global username,nom,prenom,username,mot_de_passe
       
      nom=nom_entry.get()
      prenom= prenom_entry.get()
      username = new_username_entry.get()
      mot_de_passe= new_password_entry.get()

      clients=[nom,prenom,username,mot_de_passe]
      global x
      x=json.dumps(clients)
      print(x)
      mesage= client.recv(1024).decode('utf-8')
      if mesage == "CL" :
         client.send(x.encode())
      msgeframe()




def verifylogin():
    global n,nom,prenom,mot_de_passe,username 
    username = username_entry.get()
    password = password_entry.get()
    if n==0:
     client.send("login".encode('utf-8'))
    
    user=[username,password]
    y=json.dumps(user)
    client.send(y.encode('utf-8'))
    data=client.recv(1024).decode('utf-8')
    
    if data=="exist":
     print("exist")
     resu= client.recv(1024)
     print(resu)
     resu=json.loads(resu)
     print("Login successful!")
     username = resu[0][0]
    
     nom=resu[0][1]
     prenom= resu[0][2]
     mot_de_passe= resu[0][3]
     print(username,nom,prenom,mot_de_passe)
     msgeframe()
    
    if data=="notexits":
        n=n+1
        print("notexist")
        print("Identifiant ou mot de passe incorrect .veuille réessayer.")
        CTkMessagebox(title="Erreur", message="Identifiant ou mot de passe incorrect .veuille réessayer.", icon="cancel")




def clientactive():

 print("clientactive")

 global client
 global receive_thread

 receive_thread= threading.Thread(target=receive)
 clireceive()
def receive():
  global stop_thread  
  while not stop_thread: 
    try :
      mesage= client.recv(1024).decode('utf-8')
      print(mesage)

      if mesage == "<--Historique" :
        r=client.recv(1024).decode('utf-8')
        r= json.loads(r)
        #print(r)
        textbox2.configure(state="normal")  # Assurez-vous que le CTkTextbox est en mode édition
        textbox2.delete("1.0", "end")    # Supprime tout le contenu du CTkTextbox
        textbox.configure(state="disabled")  # Remettez le CTkTextbox en mode lecture seule si nécessaire
        for i in r: 
         textbox2.configure(state="normal")
         textbox2.insert("0.0",f"{i[0]}:{i[1]}\n")
         textbox2.configure(state="disabled")
        
        textbox2.configure(state="normal")
        textbox2.insert("0.0",f"Historique\n")
        textbox2.configure(state="disabled")

      elif mesage == "<-- listes des membres en ligne":
         h= client.recv(1024).decode('utf-8')
         print(h)
         h= json.loads(h)
         n=0
         textbox2.configure(state="normal")  
         textbox2.delete("1.0", "end")   # Supprime tout le contenu du CTkTextbox
         textbox2.configure(state="disabled")

         for i in h: 
          n=n+1
          textbox2.configure(state="normal")
          textbox2.insert("0.0",f"{n}:@{i}\n")
          textbox2.configure(state="disabled")
         textbox2.configure(state="normal")
         textbox2.insert("0.0",f"online\n")
         textbox2.configure(state="disabled")

      elif mesage == "listes des membres":
         h= client.recv(1024).decode('utf-8')
         print(h)
         h= json.loads(h)
         n=0
         textbox2.configure(state="normal")  
         textbox2.delete("1.0", "end")   # Supprime tout le contenu du CTkTextbox
         textbox2.configure(state="disabled")

         for i in h: 
          n=n+1
          textbox2.configure(state="normal")
          textbox2.insert("0.0",f"@{i[0]}\n")
          textbox2.configure(state="disabled")
         textbox2.configure(state="normal")
         textbox2.insert("0.0",f"les membres\n")
         textbox2.configure(state="disabled")

      elif  mesage =="changernom":
        global win
        frame4.pack_forget()
        win=CTkFrame(root,bg_color="#1a9ce5",fg_color="#1a9ce5")
        win.pack(pady=40,padx=60,fill='both',expand=True)
        chan_label = CTkLabel(win, text="changer votre nom d'utilisateur", font=("Helvetica", 15))
        chan_label.pack()
        textbox3 = CTkTextbox(master=win, corner_radius=0)
        textbox3.pack(pady=12,fill='both' , padx=8)
        textbox3.insert("0.0",f"Nom d'utilisateur actuel:    {username}\n")
        textbox3.configure(state="disabled")
        global newnom
        newnom = CTkEntry(win, placeholder_text="Nouveau nom d'utilisateur"
            ,text_color="black",placeholder_text_color="#5eaec8",fg_color="white")
        newnom.pack()
        changen= CTkButton(win, text="changer", command=changer,cursor="hand2",fg_color=Framefg,border_width=0,
                                 font=("yu gothic ui Bold", 15 * -1),
        bg_color=Framefg)
        changen.pack()
    
        #win.mainloop()
      else:
         
         textbox.configure(state="normal")
         textbox.insert("0.0",f"{mesage}\n")
         textbox.configure(state="disabled")
    except:
        print("serveur est hors ligne ")
        client.close()
        textbox.configure(state="normal")
        textbox.insert("0.0",f"serveur est hors ligne\n")
        textbox.configure(state="disabled")
        break
    
def write():
   if True :
       y=mesage_entry.get()
       mesage=f"{username}:{y}"
       client.send(mesage.encode('utf-8'))

def clireceive  ():
  global stop_thread #aj
  stop_thread = False#aj
  receive_thread.start()

def send(mesage_entry):
  if mesage_entry.get()!="": 
   write()
  mesage_entry.delete(0, "end")


#*********************************************************************************


# Create the main window
root= customtkinter.CTk()
customtkinter.set_default_color_theme("blue") 
root.config(bg=background)


root.title("C-Chat")

root.geometry("1080x480")

root.iconbitmap("C-Chatr.ico")

# Login Frame(frame1)
frame3=CTkFrame(root,bg_color=Framebg,fg_color="#1a9ce5")
frame4=CTkFrame(root,bg_color=Framebg,fg_color="white")
frame3.pack(pady=40,padx=60,fill='both',expand=True)
img=Image.open("tyt.png")
img=img.resize((420, 415))
backimage=ImageTk.PhotoImage(img)
oo=CTkLabel(frame3,text="",image=backimage).pack(side=LEFT)


frame1 =CTkFrame(frame3,fg_color=Framefg)
frame1.pack(pady=40,padx=60,fill='both',expand=True,side=LEFT)

login_label =CTkLabel(frame1, text="Se connecter", font=("Helvetica", 20))
login_label.pack(pady=12,fill='both' ,padx=10)

username_entry = CTkEntry(master=frame1,placeholder_text="nom d'utilisateur"
      ,text_color="black",placeholder_text_color="#5eaec8",fg_color="white")
username_entry.pack(pady=12,fill='both' , padx=10)

password_entry = CTkEntry(frame1, placeholder_text="mot de passe", show="*"
      ,text_color="black",placeholder_text_color="#5eaec8",fg_color="white")
password_entry.pack(pady=12,fill='both',padx=10)

img=Image.open("show.png")
img = img.resize((20, 20)) 
tk_img=ImageTk.PhotoImage(img)

img2=Image.open("hide.png")
img2 = img2.resize((20, 20)) 
tkh_img=ImageTk.PhotoImage(img2)


btnshow = CTkButton(frame1, height = 1, width = 12, image=tk_img ,command=showpass ,text="",
                     fg_color=Framebg)
btnshow.place(relx=0.92,rely=0.362)

forgot = CTkButton(frame1, height = 1, width = 12 ,command=forgetpass ,text="mot de passe oublié  ?",
                     fg_color=Framebg)
forgot.pack()

login_button = CTkButton(frame1, text="Se connecter", fg_color=frame3bg,hover_color=colore2,command=verifylogin )
login_button.pack(pady=12,fill='both' ,padx=10)



gosignup_button = CTkButton(frame1, text="S'inscrire      ", command=gotosignup,cursor="hand2"
    ,fg_color=Framefg,border_width=0,
    font=("yu gothic ui Bold", 15 * -1),
    height = 0, width = 0.1,
    bg_color=Framebg,
    hover_color=Framebg,
    text_color_disabled= colore1,text_color="white"   )
gosignup_button.pack(pady=12,fill='both' ,padx=10,side=RIGHT)
label =CTkLabel(frame1, text="Pas encore inscrit(e) ?    ", font=("Helvetica", 15))
label.pack(pady=12,fill='both' ,padx=10 ,side=RIGHT)

#Mot de passe oublié(Frame5)******************************
frame5 = CTkFrame(frame3,fg_color=Framefg)

signup_label = CTkLabel(frame5, text="Mot de passe oublié ?", font=("Helvetica", 20))
signup_label.pack(pady=6,fill='both' ,padx=4)

nom_entryF = CTkEntry(frame5, placeholder_text="Nom"
            ,text_color="black",placeholder_text_color="#5eaec8",fg_color="white")
nom_entryF.pack(pady=6,fill='both' ,padx=4)

prenom_entryF = CTkEntry(frame5, placeholder_text="Prénom"
            ,text_color="black",placeholder_text_color="#5eaec8",fg_color="white")
prenom_entryF.pack(pady=6,fill='both' ,padx=4)

username_entryF = CTkEntry(frame5, placeholder_text="nom d'utilisateur"
             ,text_color="black",placeholder_text_color="#5eaec8",fg_color="white")
username_entryF.pack(pady=6,fill='both' ,padx=4)

new_passwordF_entry = CTkEntry(frame5, placeholder_text="Nouveau mot de passe"
              ,text_color="black",placeholder_text_color="#5eaec8",fg_color="white")
new_passwordF_entry.pack(pady=6,fill='both' ,padx=4)

changer_button = CTkButton(frame5, text="Réinitialiser mot de passe ",command =Reinitialiser )
changer_button.pack(pady=6,fill='both' ,padx=6)

gotologingf = CTkButton(frame5, text="EXIT", command=EXIT,cursor="hand2",fg_color=Framefg,border_width=0,
    font=("yu gothic ui Bold", 15 * -1),
    bg_color=Framebg,hover_color=Framebg,text_color_disabled= colore1,text_color="white" )
gotologingf.pack(pady=6,fill='both' ,padx=4)

# Signup Frame(Frame2)*********************************
frame2 = CTkFrame(frame3,fg_color=Framefg)


signup_label = CTkLabel(frame2, text="Création d'un compte", font=("Helvetica", 20))
signup_label.pack(pady=6,fill='both' ,padx=4)

nom_entry = CTkEntry(frame2, placeholder_text="Nom"
            ,text_color="black",placeholder_text_color="#5eaec8",fg_color="white")
nom_entry.pack(pady=6,fill='both' ,padx=4)

prenom_entry = CTkEntry(frame2, placeholder_text="Prénom"
            ,text_color="black",placeholder_text_color="#5eaec8",fg_color="white")
prenom_entry.pack(pady=6,fill='both' ,padx=4)

new_username_entry = CTkEntry(frame2, placeholder_text="nom d'utilisateur"
             ,text_color="black",placeholder_text_color="#5eaec8",fg_color="white")
new_username_entry.pack(pady=6,fill='both' ,padx=4)

new_password_entry = CTkEntry(frame2, placeholder_text="mot de passe"
              ,text_color="black",placeholder_text_color="#5eaec8",fg_color="white")
new_password_entry.pack(pady=6,fill='both' ,padx=4)

signup_button = CTkButton(frame2, text="S'inscrire",command = creenewclient)
signup_button.pack(pady=6,fill='both' ,padx=6)

label2 =CTkLabel(frame2, text="Déjà inscrirt(e) ?", font=("Helvetica", 12))



gotologing = CTkButton(frame2, text="Se connecter ", command=gotologin,cursor="hand2",fg_color=Framefg,border_width=0,
    font=("yu gothic ui Bold", 15 * -1),
    bg_color=Framebg,hover_color=Framebg,text_color_disabled= colore1,text_color="white" )
gosignup_button.pack(pady=6,fill='both' ,padx=4)
gotologing.pack(pady=6,fill='both' ,padx=4,side=RIGHT )
label2.pack(pady=12,fill='both' ,padx=10 ,side=RIGHT)

#fram message(frame 4) ****************

label =CTkLabel(frame4, text="Salon de chat ",text_color=frame3bg, font=("Helvetica", 20))######
label.pack()

textbox2 = CTkTextbox(master=frame4, width=100, corner_radius=0)
textbox2.pack(pady=12,fill='both' , padx=10,side=LEFT)
textbox2.configure(state="disabled")
global textbox
textbox = CTkTextbox(master=frame4, width=200, corner_radius=0)
textbox.pack(pady=12,fill='both' , padx=8)
textbox.configure(state="disabled")

mesage_entry = CTkEntry(master=frame4,placeholder_text="Message")
mesage_entry.pack(pady=12,fill='both' , padx=10)


send_button = CTkButton(frame4, text="Envoyer",command=lambda: send(mesage_entry))
send_button.pack(pady=12,fill='both' ,padx=10)

HIS = CTkButton(frame4, text="Historique" ,command=his)
HIS.pack(pady=12 ,padx=10 ,side=LEFT)

onl = CTkButton(frame4, text="en ligne" ,command=online)
onl.pack(pady=12 ,padx=10 ,side=LEFT)
chang = CTkButton(frame4, text="changer nom d'utilisateur" ,command=changernom)
chang.pack(pady=12 ,padx=10 ,side=LEFT)

list = CTkButton(frame4, text="les membres" ,command=memebres)
list.pack(pady=12 ,padx=10 ,side=LEFT)

Exit= CTkButton(frame4, text="Exit", command=EXIT,cursor="hand2",fg_color=Framefg,border_width=0,
font=("yu gothic ui Bold", 15 * -1),
bg_color=Framefg)
Exit.pack(pady=12,fill='both' ,padx=10)

root.mainloop()



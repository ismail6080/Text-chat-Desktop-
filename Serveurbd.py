import socket
import threading
import sqlite3

import json

host=socket.gethostbyname(socket.gethostname() )
print(host)
port=9091
cmp=0
n=0
t=0
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()
clients=[]
usernames=[]
noms=[]
motdepasss=[]
prenoms=[]
mesages=[]

db= sqlite3.connect("database.db")
print("Connexion réussie à SQLite ")


server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

#************fonction de SQLite3********************
def creatable():
 vdb = db.cursor()
 sql="""create table if not exists client (
     username text PRIMARY KEY not NULL,
     nom text not NULL,
     prenom text not NULL,
     mot_de_pass text not NULL
)"""

 vdb.execute(sql)
 db.commit()
 vdb = db.cursor()
 print("Table1 SQLite est créée")
 sql="""create table if not exists msg (
     username text not NULL,
     message text not NULL,
     distinateur text
)"""
 vdb.execute(sql)
 print("Table messages SQLite est créée")
 db.commit()
creatable()

def insert(x):
    vdb = db.cursor()
    sql = "insert into client(nom,prenom,username,mot_de_pass) values (?, ?, ?, ?)"
    vdb.execute(sql, x)
    print("Enregistrement inséré avec succès")
    db.commit()
    # db.close()
def insertMSG(db, y):
    vdb = db.cursor()
    sql_insert = "insert into msg(username, message,distinateur) values (?, ?, ?)"
    sql_update = "update msg set message = ? where username = ?"

    
    vdb.execute(sql_insert, y)
  

    print("message inserted/updated successfully")
    db.commit()

def aficherhis(user):
    with sqlite3.connect("database.db") as db_thread:
        vdb = db_thread.cursor()
        sql = "SELECT * FROM msg where username = ? or distinateur= ? or distinateur =? "
        vdb.execute(sql, (user,user,"ALL"))
        resu = vdb.fetchall()
        return resu
def allcolumn():
 with sqlite3.connect("database.db") as db_thread:
  vdb = db_thread.cursor()
  sql="SELECT username FROM client"
  vdb.execute(sql)
  res=vdb.fetchall()
  return res

  

"""def Delet(username):
  with sqlite3.connect("database.db") as db:
   vdb = db.cursor()
   sql="DELETE FROM client WHERE username = ? "
   vdb.execute(sql,username)
   print("Enregistrement supprimé avec succès")
   db.close()"""

def changenom(h):
 with sqlite3.connect("database.db") as db:
  vdb = db.cursor()
  sql="UPDATE client SET username = ? WHERE username = ? "
  vdb.execute(sql, (h[0], h[1]))
  
  print("le nom d'utilisateur a été modifé avec succès")
  db.commit()
  vdb = db.cursor()
  sql="UPDATE msg SET username = ? WHERE username = ? "
  vdb.execute(sql, (h[0], h[1]))
  db.commit()
  db.close()

def changemotdepasse(h):
    
    with sqlite3.connect("database.db") as db:
        vdb = db.cursor()
        sql = "SELECT mot_de_pass FROM client WHERE nom = ? AND prenom =? AND username = ?"
        vdb.execute(sql, (h[0], h[1], h[2]))
        resu = vdb.fetchall()
        sql = "UPDATE client SET mot_de_pass = ? WHERE nom = ? AND prenom =? AND username = ? "
        vdb.execute(sql, (h[3], h[0], h[1], h[2]))
        print("le mot de pass a été modifié avec succès")
      
        db.commit()
        return resu
 
def verifyclient (y):
  vdb = db.cursor()
  sql='select * from client where username = ? and mot_de_pass = ?'
  vdb.execute(sql,y)
  resu=vdb.fetchall()
  
  
  
  return resu


"""def aficher():
 with sqlite3.connect("database.db") as db:
  vdb = db.cursor()
  n=0
  sql="SELECT * FROM client"
  vdb.execute(sql)
  rsu=vdb.fetchall()
  for i in rsu:
   n=n+1
   print(f"client{n}: {i[n][0]}\t  le nom :{i[n][1]} le prenom : {i[n][2]} \n")
  db.close()"""
 


global client
#************brodcast**********
def broadcast(mesage):
  print("broadcastfonction")
  for client in clients:
     client.send(f"{mesage}".encode('utf-8'))

def broadcastprv(user,mesage,dis):
  print("broadcastprv")
  if dis in usernames:
   ind1=usernames.index(dis)
   ind2=usernames.index(user)
  
   for client in clients:
    if client ==clients[ind1] or client ==clients[ind2] :
     client.send(f"{user}:{mesage}".encode('utf-8'))
  else :
    print("elseee")
    for client in clients:
      
      client.send(f"***{dis} n'est pas en ligne !*** ".encode('utf-8'))
#**********handle ******************
def handle(client):
 while True: 
  try :
   mesage=client.recv(1024).decode('utf-8')
   if mesage=="EXIT":
     broadcast(f"****{x[0]} a quitté le salon !****\n".encode('utf-8'))
     index = clients.index(client)

     clients.remove(client)
     nom = usernames[index]
     nom=noms[index]
     prenom=prenoms[index]
     usernames.remove(nom)
     noms.remove(nom)
     prenoms.remove(prenom)
     db.close()
   
   elif mesage=="his":
     r=aficherhis(username)


     r=json.dumps(r)
     client.send("<--Historique".encode('utf-8'))
    
     client.send(r.encode('utf-8'))
     
   elif  mesage=="online" :
       r=json.dumps(usernames)
       print(r)
       client.send("<-- listes des membres en ligne".encode('utf-8'))
       client.send(r.encode())
   elif  mesage=="mbr" :
       
       rsu=allcolumn()
    
       r=json.dumps(rsu)
       #print(r)
       client.send("listes des membres".encode('utf-8'))
       client.send(r.encode())
   
   elif mesage=="changer":
     client.send("changernom".encode('utf-8'))
     h=client.recv(1024).decode('utf-8')
     h = json.loads(h)
     changenom(h)
   
    
   else:
      y=mesage.split(":")
     
      t=y[1].split("@")

      t.append("ALL")
      if t[1]!="ALL":
        print("append t[1]")
        y.append(t[1])
        y=[y[0],t[0],y[2]]
      else :
        print("append ALL")
        y.append("ALL")
      
      #print(y)
      
      with sqlite3.connect("database.db") as dbt:
       
       insertMSG(dbt, y)
      
      if  t[1]!="ALL":
       broadcastprv(y[0],y[1],y[2])
      else:

       broadcast(mesage)
      mesages.append(mesage)
      #n = len(mesages)
      #for i in range(n):
       #print(f"{i}:{mesages[i]}")
    
  except :
    index = clients.index(client)

    clients.remove(client)
    user = usernames[index]
    nom=noms[index]
    prenom=prenoms[index]
    usernames.remove(user)
    noms.remove(nom)
    prenoms.remove(prenom)
    receive()
    break 
  
def receive():
    while True:
      cmp=0
      global client
      client, address = server.accept()
      global username,motdepass,nom,prenom
      print(f"Connecté avec {str(address)}")
     
      data=client.recv(1024).decode('utf-8')
#********-----------------*********************
      if data=="motdepaaseobl":
         t=0
         while t==0 :
          h=client.recv(1024).decode('utf-8')
          h = json.loads(h)
          res=changemotdepasse(h)
       
          print(res)
          
          if res:
            cmp=1
            t=1
            print("exit")
            client.send(f"{res[0]}".encode('utf-8'))

          else :
            print("notexit")
            client.send("notexit".encode('utf-8'))
          

      if cmp == 1:
        data=client.recv(1024).decode('utf-8')

      if data=="login":
        t=0
        while t==0 :
         print("login")
         y= client.recv(1024).decode('utf-8')
         print(y)
         y= json.loads(y)
         username=y[0]
         motdepass=y[1]
         y=verifyclient (y)  
         resu=y
         print(y)

         if resu:
          print("exist")
          t=1
          client.send("exist".encode('utf-8'))
          print("RESU LOIGIN")
          resu=json.dumps(resu)
          client.send(resu.encode('utf-8'))

          username=y[0][0]
          nom = y[0][1]
          prenom=y[0][2]
          motdepass=y[0][3]

          clients.append(client)
          noms.append(nom)
          prenoms.append(prenom)
          usernames.append(username)
          motdepasss.append(motdepass)
          print(noms,prenoms,usernames,motdepasss)
          index=len(usernames)-1
          index=usernames.index(username)
      
          print(index)
         else:
          resu=json.dumps(resu)
          client.send("notexits".encode('utf-8'))
          print("notexits")
          
      
#**********----------------*********************
      if data=="signup":

          client.send("CL".encode('utf-8'))
          global x
          print("signup")
          x = client.recv(1024)
          x = json.loads(x)
          username=x[2]
          insert(x)
          noms.append(x[0])
          prenoms.append(x[1])
          usernames.append(x[2])
          motdepasss.append(x[3])
          clients.append(client)
          index=len(usernames)-1





      data=client.recv(1024).decode('utf-8')
      
      if data=="CL1":

         """ print("Le nom est :", x[0])
         print(f"le prenom est : {x[1]} ")
         print("Le nom d'utilisateur est :", x[2])"""
         n = len(usernames)
         for i in range(n):
               print(f"Client {i}:  {usernames[i]} le nom : {noms[i]} le prenom : {prenoms[i]}\n")
         #aficher()
         broadcast(f"****{noms[index]} {prenoms[index]} ({username})a rejoint ****\n")
         client.send("****Connecté au serveur***** :\n ".encode('utf-8'))

         thread = threading.Thread(target=handle, args=(client,))
         thread.start()

            
     
    
print("Attente de connexion ...")

receive()


 
     
  













 
     
  










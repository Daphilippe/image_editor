# -*- coding: utf-8 -*-

"""

auteur: PHAM Duy Anh Philippe

date: 30/03/2017

projet, version 7



problème: annuler et répéter

non traité pour les carrées



probleme: interface graphique

décocher puis recocher bouton carrée après utilisation d'une fonction pour le réutiliser

origine: programme actu() (essentiel pour les autres fonctions afin d'actualiser)

solution: partiellement trouvé

couleur carrée dessin non actualiser en temps réel

solution: trouvé mais plus d'inconvéniant, autre solution: actualiser manuellement

"""

from PIL import Image as img

from PIL import ImageTk

import tkinter as TK

import tkinter.filedialog,tkinter.messagebox,tkinter.simpledialog

import numpy as np

import matplotlib.pyplot as plt 





global sauv,chemin,limage,zd_f,n,coul,apercoul

#==============================================================================

# Fonctions

#============================================================================== 

#Général

def demandechemin():

    global chemin

    filename=tkinter.filedialog.askopenfilename(title="Chemin d'accès",filetypes=[('gif','.gif'),('jpg','.jpg'),('tout','.*')])    

    print(filename)

    chemin=filename

    

def converimg(chemin):

    global limage

    uneimage=img.open(chemin)#Ouverture d'une image qui doit être dans le même répertoire que le fichier .py

    uneimage=uneimage.convert('L') #Convertir en N&B

    tabImage=np.array(uneimage)#Transformer l'image en tableau

    limage=tabImage.tolist()#Transformer le tableau en liste    

    

def converlimg(limage):

    tabimage=np.asarray(limage)#Transformer la liste en tableau

    uneimage=img.fromarray(tabimage) #Transformer le tableau en image

    uneimage=uneimage.convert('L') #Convertir en N&B

    return uneimage

    

def zd():

    global limage,zd_f

    zd_h=len(limage)

    zd_l=len(limage[0])

    zd_f=TK.Canvas(fen,height=zd_h,width=zd_l,bg="white",bd=0, highlightthickness=0) 

    zd_f.bind('<Motion>',mouvement)

    zd_f.pack(side="top",padx=0,pady=0)



def actu():

    global limage,zd_f

    zd_f.destroy()

    zd()

    A=converlimg(limage)

    photo=ImageTk.PhotoImage(A)#ne fonctionne pas erreur inconnue

    zd_f.create_image(0,0,anchor="nw",image=photo)

    fen.mainloop()

    #print "actualisé"

    

def copier(limage):

    lbrute=[] #si lbrute=limage, même attribution dans la ram et cause des problemes origine: utilisation de global

    for l in limage:

        lbrute.append([])

    for l in range(len(limage)):

        k=lbrute[l]

        for c in range(len(limage[0])):

            k.append(limage[l][c])

    return lbrute

#==============================================================================  

    #Gestion fichier

    

def ouvrir():

    global chemin,limage,sauv

    demandechemin() #ouvre une image, désactiver pour test

    fermer()

    converimg(chemin)

    sauv=[limage]    

    zd()

    A=converlimg(limage)

    photo=ImageTk.PhotoImage(A)

    zd_f.create_image(0,0,anchor="nw",image=photo)

    hisgram()

    fen.mainloop()

    #print "ouvert" 



def nouveau(): 

    global zd_f,chemin,limage,sauv,n

    if tkinter.messagebox.askokcancel("Fichier","Nouveau projet ?"):

        fermer()

        zd_h=tkinter.simpledialog.askinteger("Nouveau projet", "Largeur ?") 

        zd_l=tkinter.simpledialog.askinteger("Nouveau projet", "Longueur ?") 

        zd_f=TK.Canvas(fen,height=abs(zd_h),width=abs(zd_l),bg="white",bd=0, highlightthickness=0)

        limage=[]

        for i in range(abs(zd_h)):

            limage.append([])

        for k in limage:    

            for j in range(abs(zd_l)):

                k.append(255)

        sauv=[]

        sauv.append(limage)

        chemin="initiale.gif" #désactiver pour test image

        actu()

    

def ecraser():

    global chemin,limage

    uneimage=converlimg(limage)

    uneimage.save(chemin) #Enregistrer l'image

    #print "écrasé"

    

def enregistrer():#liste de valeur image

    global limage,chemin

    uneimage=converlimg(limage)

    chemin=tkinter.filedialog.asksaveasfilename(title="Chemin d'accès",filetypes=[('gif','.gif'),('jpg','.jpg'),('tout','.*')]) 

    try:

        uneimage.save(chemin) #Enregistrer l'image

    except KeyError:

        uneimage.save(chemin+'.gif')#si l'utilisateur oublie de rentrer l'extension

    #print "enregistré"

    

def fermer():

    global sauv,limage

    zd_f.destroy()

    sauv=[]    

    limage=[]

         

def quitter():

    message="Voulez vous quitter ?"

    if tkinter.messagebox.askokcancel("Quitter",message):

        exit()    

#==============================================================================

    #perfectionner 

    

def sauvauto():#n'est mis en place que pour des actions irréversibles

    global sauv,limage,n

    lbrute=copier(limage)

    sauv.append(lbrute)

    n=n+1

    try:

        while len(sauv)>n:

            del sauv[-2]

    except IndexError:#si l'utilisateur annule répète annule et rerépète: comportement étrange

        #print "Erreur index sauvauto",len(sauv)

        n=1

        sauv=[lbrute]

    

def annuler():

    global sauv,limage,n

    try:

        n=n-1

        limage=sauv[n]

    except IndexError:#boucle les annulations: moins de contrainte utilisateur

        limage=sauv[0]

        n=1

    actu()

        

def repeter():

    global sauv,limage,n

    limage=sauv[-1]

    n=len(sauv)

    actu()

#==============================================================================

    #fonctions sur images

    

def rotationg():

    global limage    

    tabimage=np.asarray(limage)#Transformer la liste en tableau

    tabimage=np.rot90(np.asarray(tabimage))

    lbrute=tabimage.tolist()

    #print "rotation gauche faite"

    limage=lbrute

    actu()



    

def rotationd():

    global limage  

#autre solution moins lourde:

#lbrut=rotationg(limage)

    c_i=len(limage[0])

    lbrut=[]

    for i in range(c_i):

        lbrut.append([])

    for j in limage:

        for k in range(c_i):

            lbrut[k].append(j[k])          

#lbrute=symetriev(lbrut)

    lbrute=[]

    for i in lbrut:

        lbrute.append(i[::-1])

    #print "rotation droite faite"

    limage=lbrute

    actu()

    

def symetriev():

    global limage  

    lbrute=[]

    for i in limage:

        lbrute.append(i[::-1])

    #print "symétrie verticale faite"

    limage=lbrute

    actu()

    

def symetrieh():

    global limage  

    lbrute=limage[::-1]

    #print "symétrie horizontale faite"

    limage=lbrute

    actu()

     

def lumim():

    global limage

    lbrute=limage

    for i in range(len(lbrute)):

        l=lbrute[i]

        for j in range(len(l)): 

            if l[j]-10<0:

                l[j]=0

            else:

                l[j]=l[j]-10

    #print "luminosité moins faite"

    limage=lbrute

    hisgram()

    sauvauto()

    actu()#permet d'actualiser la zone dessin

     

def lumip():

    global limage

    lbrute=limage

    for i in range(len(lbrute)):

        l=lbrute[i]

        for j in range(len(l)):

            if l[j]+10>255:

                l[j]=255

            else:

             l[j]=l[j]+10

    #print "luminosité plus faite"

    limage=lbrute

    hisgram()

    sauvauto()

    actu()#permet d'actualiser la zone dessin

     

def negatif(): 

    global limage

    lbrute=copier(limage)

    for i in range(len(lbrute)):

        l=lbrute[i]

        for j in range(len(l)):

            l[j]=255-l[j]

    #print "négatif fait"

    limage=lbrute

    hisgram()

    actu()#permet d'actualiser la zone dessin

 

def contraste():

    global limage

    lbrute=copier(limage)

    for i in range(len(lbrute)):

        l=lbrute[i]

        for j in range(len(l)):#contraste 100%

            if l[j]<128:

                l[j]=0

            else:

                l[j]=255

    #print "contraste fait"

    limage=lbrute

    hisgram()

    sauvauto()

    actu()#permet d'actualiser la zone dessin

    

def coup(coupage,limage):

    lbrute=copier(limage)

    lpixels=[]

    for i in limage:

           for j in i:

            lpixels.append(j)

    lpixels=sorted(lpixels)#ordonne la liste

    #Calcule des tranches

    effectif=len(lbrute)*len(lbrute[0])

    palier=[]

    for i in range(1,coupage):

        d=(float(i)/coupage)

        palier.append(int(float(effectif)*d))

    #couleur effectif correspondant

    liste=[]

    liste.append(0)

    for i in palier:

        liste.append(lpixels[i])

    liste.append(255)

    #attribution des couleurs par tranche suivant caractéristique effectif

    for k in range(len(liste)):

        for i in range(len(lbrute)):

            l=lbrute[i]

            for j in range(0,len(l)-1):

                if liste[k]<l[j]<liste[k+1]:#attribution n couleurs pour n-1 segment

                    if k+1<=int(len(liste)/2):

                        l[j]=liste[k]

                    else:

                        l[j]=liste[k+1]



    return lbrute

    

def seuillage():

    global limage

    coupage=tkinter.simpledialog.askinteger("Sensibilité: 0 à 255", "Valeur conseillée 3 à 15: ")

    lbrute=coup(abs(coupage),limage)

    #print "seuillage fait"

    limage=lbrute

    hisgram()

    sauvauto()

    actu()#permet d'actualiser la zone dessin



def contour():

    global limage

    lbrute=limage

    coupage=tkinter.simpledialog.askinteger("Sensibilité: 0 à 255", "Valeur recommandée 3: ")

    lbrute=coup(abs(coupage),limage)

    #mise en place du contour   

    for i in range(1,len(lbrute)-1):

        l=lbrute[i]

        for j in range(1,len(l)-1):

            if (l[j]!=l[j-1] and l[j]!=l[j+1]) or (lbrute[i-1][j]!=lbrute[i][j] and lbrute[i+1][j]!=lbrute[i][j]):

                l[j]=255

            else:

                l[j]=0   

    #print "contour fait"

    limage=lbrute

    sauvauto()

    actu()#permet d'actualiser la zone dessin

            

#==============================================================================

    #fonctions graphiques

           

def hisgram():

    global limage

    var=varhis.get()

    if var==1:

        lpixels=[]

        for i in limage:

            for j in i:

                lpixels.append(j) 

        plt.hist(lpixels, range= (0,255),  bins = 255, histtype = 'step')

        plt.ylabel("Nombre de pixels")

        plt.xlabel("Nuance de gris")

        plt.title("Histogramme")

        plt.grid(True)

        plt.show()

        

def mouvement(event): 

    etiquette.configure(text="x="+str(event.x)+" et y="+str(event.y))    

x1=""

y1=""

x2=""

y2=""



def couleur():

    global coul

    coul=tkinter.simpledialog.askinteger("Niveau de gris 0 à 255", "Valeur couleur:")

    while coul<0 or coul>255:    

        coul=tkinter.simpledialog.askinteger("Erreur valeur couleur", "entre 0 et 255:")

    coulap()



def coulap():

    global coul,apercoul

    lcouleur=[]

    for i in range(20):

        lcouleur.append([])

        for j in range(20):

            lcouleur[i].append(coul)

    apercoul.destroy()

    imgcouleur=converlimg(lcouleur)

    imgcouleur=ImageTk.PhotoImage(imgcouleur)

    apercoul=Tk.Canvas(outil_f,height=20,width=20,bg="white")    

    apercoul.create_image(0,0,anchor='nw',image=imgcouleur)

    apercoul.pack(side="top",padx=0,pady=0)

    fen.mainloop()

        

def carre(event):

    global limage,zd_f,coul

    lbrute=copier(limage)

    var=varcr.get()

    if var==1:

        for i in range(0,11):

            zd_f.create_rectangle(event.x,event.y,event.x+i,event.y+i)

        for x in range(event.x,event.x+11,1):

            for i in range(0,11):

                if event.y+i<len(lbrute) and x<len(lbrute[0]):

                    lbrute[event.y+i][x]=coul

        for y in range(event.y,event.y+11,1):

            for i in range(0,11):

                if y<len(lbrute) and event.x+i<len(lbrute[0]):

                    lbrute[y][event.x+i]=coul

    sauvauto()

    limage=lbrute

    fen.mainloop()

    

def gcarre():

    global zd_f

    zd_f.bind( "<Button-1>" ,carre)

    

#==============================================================================

# Fenetre

#==============================================================================

        #éléments

fen=TK.Tk("Programme","Prog")

titre_f=fen.title("Programme")

taille_f=fen.geometry("1000x900")

        #zone dessin

zd_h=100

zd_l=200

zd_f=TK.Canvas(fen,height=zd_h,width=zd_l,bg="white",bd=0, highlightthickness=0)

        #sous-fenetres et boutons

menu_f=TK.Frame(fen)

menu_f.pack(side="top",padx=0,pady=10)



mainmenu = TK.Menu(fen)  ## Barre de menu 

menuFichier = TK.Menu(mainmenu, tearoff=0)  ## Menu fils menuExample 

menuFichier.add_command(label="Nouveau", command=nouveau)  ## Ajout d'une option au menu fils menuFile 

menuFichier.add_command(label="Ouvrir", command=ouvrir)

menuFichier.add_command(label="Ecraser", command=ecraser)  

menuFichier.add_command(label="Enregistrer Sous", command=enregistrer)

menuFichier.add_command(label="Fermer projet", command=fermer) 

menuFichier.add_command(label="Quitter", command=quitter) 

mainmenu.add_cascade(label = "Fichier", menu=menuFichier)  



menuannuler = TK.Menu(mainmenu, tearoff=0)

mainmenu.add_command(label="Annuler",command=annuler)

menurepeter = TK.Menu(mainmenu, tearoff=0)

mainmenu.add_command(label="Repeter",command=repeter)

menurepeter = TK.Menu(mainmenu, tearoff=0)

mainmenu.add_command(label="Actualiser",command=actu)

fen.config(menu = mainmenu)

#==============================================================================

    #Interface fonctions   

rot_m=TK.Frame(menu_f)

rot_m.pack(side="left",padx=1,pady=0)

TK.Label(rot_m, text="Rotation").pack(side="top")

rotg=TK.Button(rot_m,text="gauche",height=1,width=5,command=rotationg)

rotg.pack(side="left",padx=0,pady=0)

rotd=TK.Button(rot_m,text="droite",height=1,width=5,command=rotationd)

rotd.pack(side="left",padx=0,pady=0)

        

sym_m=TK.Frame(menu_f)

sym_m.pack(side="left",padx=1,pady=0)

TK.Label(sym_m, text="Symétrie").pack(side="top") 

symv=TK.Button(sym_m,text="verticale",height=1,width=10,command=symetriev)

symv.pack(side="top",padx=0,pady=0)

symh=TK.Button(sym_m,text="horizontale",height=1,width=10,command=symetrieh)

symh.pack(side="top",padx=0,pady=0)



lum_m=TK.Frame(menu_f)

lum_m.pack(side="left",padx=1,pady=0)

TK.Label(lum_m, text="Luminosité").pack(side="top")       

lumm=TK.Button(lum_m,text="moins",height=1,width=5,command=lumim)

lumm.pack(side="left",padx=0,pady=0)

lump=TK.Button(lum_m,text="plus",height=1,width=5,command=lumip)  

lump.pack(side="left",padx=0,pady=0)      

#==============================================================================

    #Interface filtrage

ens_m=TK.Frame(menu_f)

ens_m.pack(side="left",padx=1,pady=0)

TK.Label(ens_m, text="Filtres").pack(side="top")



ens_s=TK.Frame(ens_m)

ens_s.pack(side="top",padx=1,pady=0)

neg=TK.Button(ens_s,text="négatif",height=1,width=8,command=negatif)

neg.pack(side="left",padx=1,pady=0)

const=TK.Button(ens_s,text="contraste",height=1,width=8,command=contraste)

const.pack(side="left",padx=1,pady=0)



ens_t=TK.Frame(ens_m)

ens_t.pack(side="top",padx=1,pady=0)

an=TK.Button(ens_t,text="contour",height=1,width=8,command=contour)

an.pack(side="left",padx=1,pady=0)

rep=TK.Button(ens_t,text="seuillage",height=1,width=8,command=seuillage)

rep.pack(side="left",padx=1,pady=0)



#==============================================================================

    #Boite à outils

outil_f=TK.Frame(fen)

outil_f.pack(side="left",padx=1,pady=0)

TK.Label(outil_f, text="Boite à outils").pack(side="top")



varhis=TK.IntVar()

his=TK.Checkbutton(outil_f,text="Graphe",variable=varhis,height=1,width=7,command=hisgram)

his.pack(side="top",padx=0,pady=1)

his.deselect()



varcr=TK.IntVar()

car=TK.Checkbutton(outil_f,text="Carrée",variable=varcr,height=1,width=7,command=gcarre)

car.pack(side="top",padx=0,pady=1)

car.deselect()



col=TK.Button(outil_f,text="Couleur",height=1,width=8,command=couleur)

col.pack(side="top",padx=1,pady=0)



apercoul=TK.Canvas(outil_f,height=20,width=20,bg="black")

apercoul.pack(side="top",padx=1,pady=0)



#affiche les coordonées du curseur sur Zd_f 

etiquette=TK.Label(fen) 

etiquette.pack() 

zd_f.bind('<Motion>',mouvement)

zd_f.pack(side="top",padx=0,pady=0)



#==============================================================================

    #Initialisation des variables globales

chemin="initiale.gif" #désactiver pour test image

limage=[]

for i in range(zd_h):

    limage.append([])

for k in limage:    

    for j in range(zd_l):

        k.append(255)

sauv=[limage]

n=1

coul=0

#==============================================================================

#programme maitre

#==============================================================================

fen.mainloop()
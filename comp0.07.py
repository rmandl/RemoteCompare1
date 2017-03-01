#!/usr/bin/python

# Verzweichnisvergleich 0.05
# comp0.04
# laedt ./dirlist.txt und stellt Struktur im Baum dar
# Klick links oben laesst einen Ordner waehlen
# behoben: C:/ ist moeglich
# comp0.05
# 05-2016: Knoepfe sollen Darstellung und (aus)lesen initiieren
# Progressbar funktioniert so nicht
# comp0.052 mit self.root.after(500,machweiter) funktioniert wenigstens die Schrift


import Tkinter as tk
import ttk
import os
import unicodedata
import tkFileDialog as tkf
import platform
import hashlib


'''
logfile = open("verzverg.log","w")

def reporterror(asd):
    print "Fehler REPORTERROR"
    print asd
    print asd.filename
    print "oje"
'''

       

class App:

    # Dictionary mit icons fuer Ordner, Dateien und Zwillinge
    im = {}
    verz={}
    lliste=[]
    rliste=[]
    rootdir=''


    def __init__(self):
        self.root = tk.Tk()
        self.root.wm_title('VerzeichnisVergleich')
        #self.root.geometry("700x450")

        #self.tree = ttk.Treeview(columns=[0,1,2,3],height=12)        
        self.tree = ttk.Treeview(columns=[0,1,2,3])        
        self.tree.heading(column = '#0',text='Linker Ordner',command=self.lkopf)
        self.tree.heading(column = '#1',text='Eigenschaften')
        self.tree.heading(column = '#2',text='Rechter Ordner',command=self.rkopf)
        self.tree.heading(column = '#3',text='md5 Checksumme')        
        self.tree.column('#0',stretch=True, minwidth=250)
        self.tree.column('#1',stretch=True)
        self.tree.column('#2',stretch=True)
        self.tree.column('#2',stretch=True)
   
# icons erzeugen
        def OrdnerIcon(color1,color2):
            horz1_line = "{" + " ".join([color1]*5) +" "+  " ".join(['#BBBBBB']*11) + "}"
            horz2_line = "{" + " ".join([color1]*8) +" "+ " ".join([color2]*8) + "}"
            horz3_line = "{" + " ".join(['#BBBBBB']*11) +" "+  " ".join([color2]*5) + "}"
            photo = tk.PhotoImage(width=16, height=12)
            photo.put(" ".join([horz1_line]*3)+" "+ " ".join([horz2_line]*6)+" "+ " ".join([horz3_line]*3))
            return photo

        def DateiIcon(color):
            horz1_line = "{" + " ".join(['#BBBBBB']*10) + "}"
            horz2_line = "{" + " ".join([color]*8) +" "+ " ".join(['#BBBBBB']*2)+"}"
            photo = tk.PhotoImage(width=10, height=14)
            photo.put(" ".join([horz2_line]*10) +" "+ " ".join([horz1_line]*2))
            return photo
        
        def ZwillIcon(color1,color2):
            horz1_line = "{" + " ".join(['#BBBBBB']*18) + "}"
            horz2_line = "{" + " ".join([color1]*7) +" "+ " ".join(['#BBBBBB']*2) +" "+ " ".join([color2]*7) +" "+ " ".join(['#BBBBBB']*2)+"}"
            photo = tk.PhotoImage(width=18, height=14)
            photo.put(" ".join([horz2_line]*10) +" "+ " ".join([horz1_line]*2))
            return photo

        ge='#FFFF66'
        bl='#1111EE'
        rt='#EE1111'
        og='#FFCC11'
        vi='#EE66FF'
        tq='#11EEEE'
        ordnerfarbe=[[ge,ge],[bl,bl],[rt,rt],[bl,rt],[bl,og],[og,rt]]
        dateifarbe=[ge,bl,rt,vi,tq]
        zwillingfarbe=[[ge,ge],[bl,bl],[rt,rt],[bl,og],[og,rt]]
        self.im['ordner']=[]
        for [farbe1,farbe2] in ordnerfarbe:
            self.im['ordner'].append(OrdnerIcon(farbe1,farbe2))
            firstitem = self.tree.insert('', 'end', text=farbe1+farbe2,image=self.im['ordner'][-1])
        self.im['datei']=[]    
        for farbe in dateifarbe:
            self.im['datei'].append(DateiIcon(farbe))
            firstitem = self.tree.insert('', 'end', text=farbe,image=self.im['datei'][-1])
        self.im['zwilling']=[]    
        for [farbe1,farbe2] in zwillingfarbe:
            self.im['zwilling'].append(ZwillIcon(farbe1,farbe2))
            firstitem = self.tree.insert('', 'end', text=farbe1+farbe2,image=self.im['zwilling'][-1])

        # icon im Betriebssystemfenster (statt "Tk")
        ic = OrdnerIcon('#FFFF66','#FFFF66')
        self.root.tk.call('wm', 'iconphoto',self.root._w, ic)

        self.tree.pack()
        self.button = tk.Button(self.root,text="liesDatei",image=self.im['ordner'][1],command=self.liesDatei)        
        self.button.pack(anchor='sw')
        #self.button.configure(state='disable')
        self.button.configure(state='active')
        self.progresslabel = tk.Label(self.root,text="")
        #self.progresslabel = tk.Label(self.root,height=50,text="progress")
        self.progresslabel.pack()

        self.root.mainloop()



    def liesDatei(self):
        # Datei einlesen
        self.liste=[]
        listfile = open("dirlisting.txt","r")
        params = listfile.readline().rstrip().split('\t')
        if params[0]=="# MR-WalkList":
            system=params[1].split('system: ')[1]
            host=params[2].split('host: ')[1]
            rootdir=params[3].split('rootdir: ')[1]
        self.tree.heading(column = '#0',text=rootdir)    
        for line in listfile:
            if (not('\t' in line)):
                print(line)
            else:
                aux=line.rstrip().split('\t')
                if len(aux)==3:
                    aux.append('')
                self.liste.append(aux)
        listfile.close()
        self.fuelleBaum()


    def fuelleBaum(self,liste):
        # Baum leeren
        for item in self.tree.get_children():
           self.tree.delete(item)
        self.verz = {}   
            
        # Erstes Verzeichnis ist root
        # verz['rootverzeichnis'] muss existieren, damit itemA was wird... (siehe unten) 
        self.verz[liste[0][0]]=''
        # Baum befuellen
        for [pfad,datei,groesse,md5] in liste:
            if (datei==''):
                # kein Dateiname -> es ist ein Ordner
                parent=os.path.dirname(pfad)                
                if parent=='':
                    # '' -> win: C:/ linux: /
                    parent=liste[0][0]
                basename = os.path.basename(pfad) 
                if basename == '':
                    basename = pfad                    
                try:    
                    self.verz[pfad] = self.tree.insert(self.verz[parent],'end',text=basename,image=self.im['ordner'][0])
                except:
                    print("parent"+parent)
                    print("pfad"+pfad)
            else:
                itemA = self.tree.insert(self.verz[pfad], 'end', text=datei,image=self.im['datei'][0])
                self.tree.set(itemA, column = "#1", value = groesse)

        self.tree.bind("<Double-1>", self.OnClick)
        self.tree.bind("<ButtonPress>", self.maus)
        self.tree.bind("<Configure>", self.winsize)
# naechste Zeile geht nicht... (tag_configure) 
        self.tree.tag_configure('rttk', background="red")
        print(self.lliste)

    def liesOrdner(self):
        # lies ein Verzeichnis ein

        rootdir = self.rootdir
        
        if rootdir == '':
            return
        # name of root, '/' or 'C:/' will result in '' so this workaround:
        rootbase = os.path.basename(rootdir)
        if rootbase == '':
            rootbase = rootdir
 
        liste=[]
        md5=False
#        for w in os.walk(rootdir,onerror=reporterror):
# wie mit Fehlern in walk umgehen?
        for w in os.walk(rootdir):
            curdir = os.path.normpath(w[0])
            curdir = os.path.relpath(curdir,rootdir)
            curdir = os.path.join(rootbase,curdir)
            curdir = os.path.normpath(curdir)
            curdir = curdir.replace('\\','/')
            liste.append([curdir,'',str(0),''])
            for datei in w[2]:
                size=os.path.getsize(os.path.join((w[0]),(datei)))
                if md5:
                    a=open(os.path.join((w[0]),(datei)),'rb')
                    md5 = hashlib.md5(a.read()).hexdigest()
                    a.close()
                else:
                    md5=''        
                liste.append([curdir,datei,str(size),md5])
                
        self.progresslabel.config(text='')
        self.rootdir = rootdir
        self.lliste = liste
        #return [rootdir,liste]
        self.root.after(0,self.rufBaum)
                        
    def lkopf(self):
        self.rootdir = tkf.askdirectory()
        self.progresslabel.config(text='Bitte warten... Verzeichnisse werden gesucht')
        self.root.after(80,self.liesOrdner)
        
        #[rootdir,self.lliste] = self.liesOrdner(self.lliste)

    def rufBaum(self):
        if self.rootdir: 
            self.tree.heading(column = '#0',text=self.rootdir)
            self.fuelleBaum(self.lliste)


    def rkopf(self):
        [rootdir,self.rliste] = self.liesOrdner(self.rliste)
        if rootdir:
            self.tree.heading(column = '#2',text=rootdir)
            self.fuelleBaum(self.rliste)
    

    def maus(self,was):
        print(was)

    def winsize(self,was):
        #self.progresslabel.config(text=self.root.winfo_height())
        self.tree.pack() 
        self.tree.config(height=(self.root.winfo_height()/20)-3)
        self.progresslabel.config(text=str(ttk.Style().lookup("Treeview", "rowheight")))
        #self.tree.geometry

        

    def OnClick(self, event):
        item2 = self.tree.selection()[0]
        print("you clicked on"+self.tree.item(item2,"text"))
        self.tree.item(item2,image=self.im['zwilling'][0])
        print(self.tree.item(item2))


if __name__ == "__main__":
    app=App()





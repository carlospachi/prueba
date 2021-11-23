from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter.font import Font
import sys
import datos_monedas 

lista=datos_monedas.lista_mercados()
lista_demercados=[]
for i in lista:
	lista_demercados.append([i.moneda])

print(lista_demercados)	




def mensaje_resumen(mercado):
	#print(type(mercado))
	lista=datos_monedas.lista_mercados()
	for i in lista:
		if i.moneda==mercado:
			eda=str(i.moneda)
			tual=str(round(float(i.precio_actual),4))
			enta=str(round(float(i.inversion_venta),4))
			ompra=str(round(float(i.presupuesto_compra),4))
			nta=str(round(float(i.presupuesto_venta),4))
		
	mensaje_mercado.set(" El mercado es {}, esta a {} y tienes  {} invertido".format(eda, tual,enta))
	mensaje_usuario.set(" Tienes {} presupueto para comprar y {} para vender".format(ompra,nta))

#activar=False


def lanzar(mercado):
	mercado=menu_mercado.get()	
	valor=messagebox.askquestion("Datos", "Desea comenzar las operaciones?, \n Compruebe el mercado escogido")
	if valor=="yes":
		for i in (lista_demercados):
			#print(i)
			if i==[mercado]: 				
				activar=True

		if activar==False:
			messagebox.showinfo("Error", "El mercado introducido no esta en la lista.")


def previsualizar(mercado):
	mercado=menu_mercado.get()
	valor=messagebox.askquestion("Datos", "Desea ver la situacion actual?, \n Compruebe el mercado escogido.")
	if valor=="yes":
		for i in (lista_demercados):
			if i==[mercado]: 
				mensaje_resumen(mercado)
				activar=True

		if activar==False:
			messagebox.showinfo("Error", "El mercado introducido no esta en la lista.")


def cancelar(mercado):
	activar=False
	mercado=menu_mercado.get()
	print(mercado)
	valor=messagebox.askquestion("Datos", "Desea parar el mercado actual?, \n Compruebe el mercado escogido")
	if valor=="yes":
		for i in (lista_demercados):
			if i==[mercado]:				
				activar=True

		if activar==False:
			messagebox.showinfo("Error", "El mercado introducido no esta en la lista.")


def salir():
	valor=messagebox.askquestion("Salir", "¿Desea realmente salir de la aplicacion?. ")
	if valor=="yes":
		sys.exit()	



raiz=Tk()

raiz.title("BNBEUR")

raiz.iconbitmap("iconoBNBEUR.ico")

fuente_grande = Font(family="Arial", size=20)
fuente_chica=Font(family="Arial", size=12)

mensaje_mercado=StringVar()
mensaje_mercado.set("hola otra vez")

mensaje_usuario=StringVar()
mensaje_usuario.set("hola mensaje 3")

mensaje_operaciones=StringVar()
mensaje_operaciones.set("Sin operaciones a la vista")


mi_ventana=Frame(raiz)
mi_ventana.pack()


espacio_elecion=Frame(mi_ventana,relief="groove", bd=2)
espacio_elecion.pack( anchor="center")
espacio_menu=Frame(espacio_elecion,relief="groove", bd=2, width=15)
espacio_menu.grid(row=0, column=0)
espacio_botones=Frame(espacio_elecion,relief="groove", bd=2)
espacio_botones.grid(row=0, column=1)

menu_mercado=ttk.Combobox(espacio_menu, values=lista_demercados, font=fuente_grande,width=7, state="readonly")
menu_mercado.grid(row=1,column=1,padx=10, pady=10)
mercado=menu_mercado.get()


lanzar_boton=Button(espacio_botones, text=" LANZAR ",fg="red",width=40,font=fuente_grande, command=lambda:lanzar(mercado))
lanzar_boton.grid(row=0, columnspan=2,padx=10, pady=10)
ver_boton=Button(espacio_botones, text=" DATOS ", width=20,font=fuente_chica, command=lambda:previsualizar(mercado))
ver_boton.grid(row=1, column=0,padx=10, pady=10)
cancelar_boton=Button(espacio_botones,text=" CANCELAR ",font=fuente_chica, width=20, command=lambda:cancelar(mercado))
cancelar_boton.grid(row=1, column=1,padx=10, pady=10)


espacio_comentario=Frame(espacio_elecion,relief="groove", bd=2,  height=20)
espacio_comentario.grid(row=1, columnspan=2)
#espacio_comentario.geometry(600*400)
comentario_mercado=Entry(espacio_comentario,relief="groove",bd=2,font=fuente_grande,width=60, textvariable=mensaje_mercado )
comentario_mercado.config(state="readonly",font=fuente_grande)
comentario_mercado.pack()
comentario_usuario=Entry(espacio_comentario,relief="groove",bd=2,font=fuente_grande,width=60, textvariable=mensaje_usuario )
comentario_usuario.config(state="readonly",font=fuente_grande)
comentario_usuario.pack()

espacio_pestanas=ttk.Notebook(mi_ventana)

pestana_1=ttk.Frame(espacio_pestanas)
espacio_pestanas.add(pestana_1, text="mercado1")

#pestana_2=ttk.Frame(espacio_pestanas)
#espacio_pestanas.add(pestana_2, text="mercado2")

espacio_pestanas.pack()

texto_mercado1=Text(pestana_1 , font=fuente_chica,width=150, height=20)
texto_mercado1.grid(row=0, column=0)
scroll_mercado1=Scrollbar(pestana_1, command=texto_mercado1.yview)
scroll_mercado1.grid(row=0, column=1, sticky="nesw")
texto_mercado1.config(yscrollcommand=scroll_mercado1)
texto_mercado1.insert(INSERT, mensaje_operaciones.get())


boton_salir=Button(mi_ventana, text=" SALIR ",font=fuente_chica,fg="red", command=lambda:salir())
boton_salir.pack(anchor="s", side="bottom", padx=10, pady=10 )


raiz.mainloop()





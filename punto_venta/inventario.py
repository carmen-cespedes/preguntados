from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from colores import *
from fuentes import *
import sqlite3

class Inventario(tk.Frame):
    db_name = "index.db"
    
    def __init__(self, padre):
        super().__init__(padre)
        self.pack()
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.widgets()
        
    def widgets(self):
        frame1 = tk.Frame(self, bg= color_principal)
        frame1.pack()
        #contiene el titulo
        frame1.place(x= 0, y= 0, width=1100, height=100)
        
        titulo = tk.Label(self, text="INVENTARIOS",font= font_inventario,fg=blanco, bg= color_principal, anchor="center")
        titulo.pack()
        titulo.place(x=5, y=0, width=1090, height=90)
        
        frame2 = tk.Frame(self, bg= negro )
        frame2.place(x=0, y=100, width=1100, height=550)
        
        lblframe = LabelFrame(frame2, text="Productos", bg= gris, font= font_venta)
        lblframe.place(x=20, y=30, width=400, height= 500)
        
        lblnombre = Label(lblframe,text="Nombre: ", font=font_inventario, bg=gris )
        lblnombre.place(x=10, y=20)
        self.nombre = ttk.Entry(lblframe, font= font_inventario)
        self.nombre.place(x=140, y=20, width=240, height=40)
        
        lblproveedor = Label(lblframe, text="Proveedor: ", font=font_inventario, bg=gris)
        lblproveedor.place(x=10, y=80)
        self.proveedor = ttk.Entry(lblframe, font= font_inventario)
        self.proveedor.place(x=140, y=80, width=240, height=40)
        
        lblprecio = Label(lblframe, text="Precio: ", font=font_inventario, bg=gris)
        lblprecio.place(x=10, y=140)
        self.precio = ttk.Entry(lblframe,font= font_inventario)
        self.precio.place(x=140, y=140, width=240, height=40)
        
        lblcosto = Label(lblframe, text="Costo: ", font=font_inventario, bg=gris)
        lblcosto.place(x=10, y=200)
        self.costo = ttk.Entry(lblframe,font= font_inventario)
        self.costo.place(x=140, y=200, width=240, height=40)
        
        lblstock = Label(lblframe, text="Stock: ", font=font_inventario, bg=gris)
        lblstock.place(x=10, y=260)
        self.stock = ttk.Entry(lblframe,font= font_inventario) 
        self.stock.place(x=140, y=260, width=240, height=40)
        
        boton_agregar = tk.Button(lblframe, text= "Ingresar", font=font_inventario, bg=gris, command=self.registrar)
        boton_agregar.place(x=80, y=340, width=240, height=40)
        
        boton_editar = tk.Button(lblframe, text= "Editar", font=font_inventario, bg=gris, command=self.editar_producto)
        boton_editar.place(x=80, y=400, width=240, height=40)
        
        
        
        #tabla
        treFrame = Frame(frame2, bg= blanco)
        treFrame.place(x=450, y=50, width=620, height=450)
        
        scrol_y = ttk.Scrollbar(treFrame)
        scrol_y.pack(side=RIGHT, fill=Y)
        
        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)
        
        self.tre = ttk.Treeview(treFrame, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set, height=40 ,columns=("ID", "PRODUCTO", "PROVEEDOR", "PRECIO", "COSTO", "STOCK"), show="headings")
        self.tre.pack(expand=True, fill=BOTH)
        
        scrol_y.config(command=self.tre.yview)
        scrol_x.config(command=self.tre.xview)
        
        self.tre.heading("ID", text="Id")
        self.tre.heading("PRODUCTO", text="Producto")
        self.tre.heading("PROVEEDOR", text="Proveedor")
        self.tre.heading("PRECIO", text="Precio")
        self.tre.heading("COSTO", text="Costo")
        self.tre.heading("STOCK", text="Stock")
        
        self.tre.column("ID", width=70, anchor="center")
        self.tre.column("PRODUCTO", width=150, anchor="center")
        self.tre.column("PROVEEDOR", width=100, anchor="center")
        self.tre.column("PRECIO", width=100, anchor="center")
        self.tre.column("COSTO", width=100, anchor="center")
        self.tre.column("STOCK", width=70, anchor="center")
        
        self.mostrar()
        
        btn_actualizar = Button(frame2, text="Actualizar", font=font_button)
        btn_actualizar.place(x=440, y=480, width=260, height=50)
        
    def eje_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(consulta, parametros)
            conn.commit()
        return result
    
    def validacion(self, nombre, prov, precio, costo, stock):
        if not nombre and prov and precio and costo and stock:
            return False
        try:
            float(precio)
            float(costo)
            int(stock)
        except ValueError:
            return False
        return True
    
    def mostrar(self):
        consulta = "SELECT * FROM inventario ORDER BY id DESC"
        result = self.eje_consulta(consulta)
        for elem in result:
            try:
                precio_peso = "$ {:,.0f}".format(float(elem[3])) if elem[3] else ""
                costo_peso = "$ {:,.0f}".format(float(elem[3])) if elem[4] else ""
            except ValueError:
                precio_peso = elem[3]
                costo_peso = elem[4]
            self.tre.insert("", 0, text=elem[0], values=(elem[0], elem[1], elem[2], precio_peso, costo_peso, elem[5]))
            
    def actualizar_inventario(self):
        for item in self.tre.get_children():
            self.tre.delete(item)
            
        self.mostrar()
        
        messagebox.showinfo("Actualizacion", "El inventario ha sido actualizado correctamente")
        
    def registrar(self):
        result = self.tre.get_children()
        for i in result:
            self.tre.delete(i)
        nombre = self.nombre.get()
        prov = self.proveedor.get()
        precio = self.precio.get()
        costo = self.costo.get()
        stock = self.stock.get()
        if self.validacion(nombre, prov, precio, costo ,stock):
            try:
                consulta = "INSERT INTO inventario VALUES(?,?,?,?,?,?)"
                parametros = (None, nombre, prov, precio, costo, stock)
                self.eje_consulta(consulta, parametros)
                self.mostrar()
                self.nombre.delete(0, END)        
                self.proveedor.delete(0, END)
                self.precio.delete(0, END)
                self.costo.delete(0, END)
                self.stock.delete(0, END)
            except Exception as e:
                messagebox.showwarning(title="Error", message=f"Error al registrar el producto: {e}")
        
        else:
            messagebox.showwarning(title="Error", message="Rellene todos los campos correctamente")
            self.mostrar()
        
    def editar_producto(self):
        seleccion = self.tre.selection()
        if not seleccion:
            messagebox.showwarning("Editar producto", "Seleccione un producto para editar")
            return
        
        item_id = self.tre.item(seleccion)["text"]
        item_values = self.tre.item(seleccion)["values"]
        
        ventana_editar = Toplevel(self)
        ventana_editar.title("Editar producto")
        ventana_editar.geometry("400x400")
        ventana_editar.config(bg=gris)
        ventana_editar.grab_set()
        
        lbl_nombre = Label(ventana_editar, text="Nombre:", font=font_inventario, bg=gris)
        lbl_nombre.grid(row=0, column=0, padx=10, pady=10)
        entry_nombre = Entry(ventana_editar, font=font_inventario)
        entry_nombre.grid(row=0, column=1, padx=10, pady=10)
        entry_nombre.insert(0, item_values[1])
        
        lbl_proveedor = Label(ventana_editar, text="Proveedor:", font=font_inventario, bg=gris)
        lbl_proveedor.grid(row=1, column=0, padx=10, pady=10)
        entry_proveedor = Entry(ventana_editar, font=font_inventario)
        entry_proveedor.grid(row=1, column=1, padx=10, pady=10)
        entry_proveedor.insert(0, item_values[2].split()[0].replace(",", ""))
        
        lbl_precio = Label(ventana_editar, text="Precio:", font=font_inventario, bg=gris)
        lbl_precio.grid(row=2, column=0, padx=10, pady=10)
        entry_precio = Entry(ventana_editar, font=font_inventario)
        entry_precio.grid(row=2, column=1, padx=10, pady=10)
        entry_precio.insert(0, item_values[3].split()[0].replace(",", ""))
        
        
        lbl_costo = Label(ventana_editar, text="Costo:", font=font_inventario, bg=gris)
        lbl_costo.grid(row=3, column=0, padx=10, pady=10)
        entry_costo = Entry(ventana_editar, font=font_inventario)
        entry_costo.grid(row=3, column=1, padx=10, pady=10)
        entry_costo.insert(0, item_values[4].split()[0].replace(",", ""))
        
        lbl_stock = Label(ventana_editar, text="Stock:", font=font_inventario, bg=gris)
        lbl_stock.grid(row=4, column=0, padx=10, pady=10)
        entry_stock = Entry(ventana_editar, font=font_inventario)
        entry_stock.grid(row=4, column=1, padx=10, pady=10)
        entry_stock.insert(0, item_values[5])
        
        def guardar_cambios():
            nombre = entry_nombre.get()
            proveedor = entry_proveedor.get()
            precio = entry_precio.get()
            costo = entry_costo.get()
            stock = entry_stock.get()
            
            if not (nombre and proveedor and precio and costo and stock):
                messagebox.showwarning("Guardar cambios", "Rellene todos los campos.")
                return 
            try:
                precio = precio.replace(",", "").strip()
                costo = costo.replace(",", "").strip()
                precio = float(precio.replace(",", "").strip())
                costo = float(costo.replace(",", "").strip())
                stock = int(stock)
            except ValueError:
                messagebox.showwarning("Guardar cambios", "Ingrese valores numericos validos para precios y costos")
                return
            
            consulta = "UPDATE inventario SET nombre=?, proveedor=?, precio=?, costo=?, stock=? WHERE id=?"
            parametros = (nombre, proveedor, precio, costo, stock, item_id)
            self.eje_consulta(consulta, parametros)
            
            self.actualizar_inventario()
            
            ventana_editar.destroy()
            
        btn_guardar = Button(ventana_editar, text="Guardar cambios", font=font_inventario, command=guardar_cambios)
        btn_guardar.place(x=80, y=250, width=240, height=40)
        
        ventana_editar.grab_set()
        
    
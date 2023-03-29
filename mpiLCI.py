from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
import subprocess
import re
import paramiko

# FUNCIONES
def compilar(source):
    stdin, stdout, stderr = ssh.exec_command('mpiLCIFunctions -s ' + source)
    output = stdout.read().decode().strip()

    ventana_resultado('Resultado de Compilación', '700x130', output)


def ejecutar(build, numproc):
    stdin, stdout, stderr = ssh.exec_command(
        'mpiLCIFunctions -b ' + build + ' -np ' + str(numproc))
    output = stdout.read().decode().strip()

    ventana_resultado('Resultado de Ejecución', '675x500', output)


def eliminar(dir, archivo, orden):
    stdin, stdout, stderr = ssh.exec_command(
        'mpiLCIFunctions ' + orden + ' ' + archivo)
    output = stdout.read().decode().strip()

    if len(output) == 0:
        stdin, stdout, stderr = ssh.exec_command("rm " + dir + archivo)
        output = 'El archivo '+archivo + ' fue eliminado con éxito'

    ventana_resultado('Resultado de Eliminación', '325x80', output)


def cargar_archivo(dir, archivo, ruta_absoluta, orden):

    if archivo == '':
        output = 'No se ha seleccionado ningún archivo'
    else:
        if orden == '-chs':
            if not re.search(r"\.(c|cpp)$", archivo):
                output = 'El archivo sebe de tener la extension .c/.cpp'
        else:
            if not re.search(r"\.txt$", archivo):
                output = 'El archivo sebe de tener la extension .txt'

        if output == '':
            # Construyendo el comando de scp
            comando_scp = "scp {} {}@{}:{}".format(
                ruta_absoluta, user, host, dir)
            # Ejecutando el comando de scp en una terminal
            subprocess.run(comando_scp, shell=True, input=password,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output = 'El archivo ' + archivo + 'Se cargo en el servidor con éxito'

    ventana_resultado('Resultado de Carga', '325x80', output)


def connect_ssh(h, u, p):
    global host, user, password, ssh

    host = h
    user = u
    password = p

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Conectar al servidor utilizando las credenciales necesarias
        ssh.connect(host, username=user, password=password)
        # Si la conexión es exitosa se muestra el menu principal
        crear_menu_principal()

    except Exception as e:
        print(e)
        print("Error de conexión")


def volver(frame):
    frame.destroy()
    crear_menu_principal()


def volver_eliminar():
    menu_eliminar.pack_forget()
    ventana.geometry("300x190")
    menu_select_dir.pack()


def volver_cargar():
    menu_cargar.pack_forget()
    menu_select_cargar.pack()


def salir():
    ssh.close()
    ventana.destroy()


def ventana_resultado(titulo, dimensiones, output):
    # crear ventana para mostrar resultado
    resultado_window = tk.Toplevel()
    resultado_window.title(titulo)
    resultado_window.geometry(dimensiones)
    # crear widget Text y agregar resultado
    resultado_text = tk.Text(
        resultado_window, wrap="word", font=("Console", 12))
    resultado_text.insert("1.0", output)
    resultado_text.pack(fill="both", expand=True)


def crear_menu_compilar():
    global menu_compilar, archivo_seleccionado

    centrar_ventana(500, 175)
    ventana.title("Menu Compilar")

    menu_principal.destroy()
    menu_compilar = ttk.Frame(ventana)

    mostrar_directorio('$HOME/MPI/sourceMPI/', menu_compilar)

    archivo_seleccionado = Entry(menu_compilar, width=30)
    archivo_seleccionado.pack(pady=5)

    botón_compilar = Button(menu_compilar, text="Compilar",
                            command=lambda: compilar(archivo_seleccionado.get()))
    botón_compilar.pack(side=LEFT, padx=25)

    botón_regresar = Button(menu_compilar, text="Regresar",
                            command=lambda: volver(menu_compilar))
    botón_regresar.pack(side=LEFT)

    menu_compilar.pack()


def crear_menu_ejecutar():
    global menu_ejecutar, archivo_seleccionado

    ventana.title("Menu Ejecutar")
    centrar_ventana(500, 175)

    menu_principal.destroy()
    menu_ejecutar = ttk.Frame(ventana)

    mostrar_directorio('$HOME/MPI/buildMPI/', menu_ejecutar)

    archivo_seleccionado = Entry(menu_ejecutar, width=30)
    archivo_seleccionado.pack(pady=5)

    slider_valor = IntVar()
    slider = Scale(menu_ejecutar, from_=1, to=128,
                   variable=slider_valor, orient=HORIZONTAL, length=300)
    slider.set(2)
    slider.pack(pady=5)

    botón_ejecutar = Button(menu_ejecutar, text="Ejecutar",
                            command=lambda: ejecutar(archivo_seleccionado.get(), slider_valor.get()))
    botón_ejecutar.pack(side=LEFT, padx=25)

    botón_regresar = Button(menu_ejecutar, text="Regresar",
                            command=lambda: volver(menu_ejecutar))
    botón_regresar.pack(side=LEFT)

    menu_ejecutar.pack()


def crear_menu_select_eliminar():
    global menu_select_dir

    # Creamos el frame del menu principal
    centrar_ventana(300, 190)
    ventana.title("Seleccionar Directorio")

    menu_principal.destroy()
    menu_select_dir = ttk.Frame(ventana)

    # Creamos los elementos del menu principal
    Label(menu_select_dir, text="Seleccione un directorio:").pack(pady=10)
    Button(menu_select_dir, text="sourceMPI",
           command=lambda: crear_menu_eliminar('$HOME/MPI/sourceMPI/', '-chs')).pack()
    Button(menu_select_dir, text="buildMPI",
           command=lambda: crear_menu_eliminar('$HOME/MPI/buildMPI/', '-chb')).pack()
    Button(menu_select_dir, text="outputMPI",
           command=lambda: crear_menu_eliminar('$HOME/MPI/outputMPI/', '-cho')).pack()
    Button(menu_select_dir, text="machinefileMPI",
           command=lambda: crear_menu_eliminar('$HOME/MPI/machinefileMPI/', '-chm')).pack()
    Button(menu_select_dir, text="Regresar",
           command=lambda: volver(menu_select_dir)).pack(pady=10)

    # Mostramos el menu principal
    menu_select_dir.pack()


def crear_menu_eliminar(dir, orden):
    global menu_eliminar, archivo_seleccionado

    centrar_ventana(500, 190)
    ventana.title("Menu Eliminar - Directorio " + dir)

    menu_select_dir.pack_forget()
    menu_eliminar = ttk.Frame(ventana)

    mostrar_directorio(dir, menu_eliminar)

    archivo_seleccionado = Entry(menu_eliminar, width=30)
    archivo_seleccionado.pack(pady=5)

    botón_eliminar = Button(menu_eliminar, text="Eliminar",
                            command=lambda: eliminar(dir, archivo_seleccionado.get(), orden))
    botón_eliminar.pack(side=LEFT, padx=25)

    botón_regresar = Button(
        menu_eliminar, text="Regresar", command=volver_eliminar)
    botón_regresar.pack(side=LEFT)

    menu_eliminar.pack()


def crear_menu_select_cargar():
    global menu_select_cargar

    centrar_ventana(300, 150)
    ventana.title("Seleccionar Directorio")

    menu_principal.destroy()
    menu_select_cargar = ttk.Frame(ventana)

    Label(menu_select_cargar, text="Seleccione un directorio:").pack(pady=10)
    Button(menu_select_cargar, text="sourceMPI",
           command=lambda: crear_menu_cargar('$HOME/MPI/sourceMPI/', '-chs')).pack()
    Button(menu_select_cargar, text="machinefileMPI",
           command=lambda: crear_menu_cargar('$HOME/MPI/machinefileMPI/', '-chm')).pack()
    Button(menu_select_cargar, text="Regresar",
           command=lambda: volver(menu_select_cargar)).pack(pady=10)

    menu_select_cargar.pack()


def crear_menu_cargar(dir, orden):
    global menu_cargar, archivo_seleccionado

    centrar_ventana(300, 150)
    ventana.title("Cargar en " + dir)

    menu_select_cargar.pack_forget()
    menu_cargar = ttk.Frame(ventana)

    def abrir_archivo():
        global archivo_seleccionado, ruta_absoluta
        archivo = filedialog.askopenfilename()
        archivo_seleccionado.set(archivo.split("/")[-1])
        ruta_absoluta = archivo

    archivo_seleccionado = StringVar()
    archivo_seleccionado.set("Ningún archivo seleccionado")

    Label(menu_cargar, textvariable=archivo_seleccionado).pack(pady=10)
    Button(menu_cargar, text="Abrir",
           command=abrir_archivo).pack()
    Button(menu_cargar, text="Cargar",
           command=lambda: cargar_archivo(dir, archivo_seleccionado.get(), ruta_absoluta, orden)).pack()
    Button(menu_cargar, text="Regresar", command=volver_cargar).pack(pady=10)

    menu_cargar.pack()


def mostrar_directorio(directorio, frame):

    def seleccionar_archivo(event):
        widget = event.widget
        selección = widget.curselection()
        archivo_seleccionado.delete(0, END)
        archivo_seleccionado.insert(END, widget.get(selección))

    stdin, stdout, stderr = ssh.exec_command('ls ' + directorio)
    archivos = stdout.read().splitlines()

    # Crear un Frame contenedor para el listbox y el scrollbar
    frame = Frame(frame)
    frame.pack(side=LEFT, fill=Y)

    # Crear el listbox y el scrollbar dentro del Frame
    lista_archivos = Listbox(frame, font=("Helvetica", 10), width=35)
    scrollbar = Scrollbar(frame, orient=VERTICAL)
    lista_archivos.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=lista_archivos.yview)

    # Empaquetar el listbox y el scrollbar dentro del Frame
    lista_archivos.pack(side=LEFT, fill=Y)
    scrollbar.pack(side=LEFT, fill=Y)

    # Insertar los archivos en el listbox
    if len(archivos) == 0:
        archivos = ['<Directorio Vació>']
        for archivo in archivos:
            lista_archivos.insert(END, archivo)
    else:
        for archivo in archivos:
            lista_archivos.insert(END, archivo.decode())
        # Asociar evento de selección de archivo a la función seleccionar_archivo()
        lista_archivos.bind('<ButtonRelease-1>', seleccionar_archivo)


def crear_menu_principal():
    global menu_principal

    # Creamos el frame del menu principal
    centrar_ventana(300, 190)
    ventana.title("Menu mpiLCI")

    menu_conexion.destroy()
    menu_principal = ttk.Frame(ventana)

    # Creamos los elementos del menu principal
    Label(menu_principal, text="Seleccione una opción:").pack(pady=10)
    Button(menu_principal, text="Compilar",
           command=crear_menu_compilar).pack()
    Button(menu_principal, text="Ejecutar",
           command=crear_menu_ejecutar).pack()
    Button(menu_principal, text="Cargar",
           command=crear_menu_select_cargar).pack()
    Button(menu_principal, text="Eliminar",
           command=crear_menu_select_eliminar).pack()
    Button(menu_principal, text="Salir", command=salir).pack(pady=10)

    # Mostramos el menu principal
    menu_principal.pack()


def crear_menu_connect():
    global menu_conexion

    centrar_ventana(250, 100)
    ventana.title("Sesión")
    menu_conexion = ttk.Frame(ventana)
    menu_conexion.pack()

    label_host = ttk.Label(menu_conexion, text="Host:")
    entry_host = ttk.Entry(menu_conexion)
    label_user = ttk.Label(menu_conexion, text="Username:")
    entry_user = ttk.Entry(menu_conexion)
    label_pass = ttk.Label(menu_conexion, text="Password:")
    entry_pass = ttk.Entry(menu_conexion, show="*")
    button_exec = ttk.Button(
        menu_conexion, text="Conectar", command=lambda: connect_ssh(entry_host.get(), entry_user.get(), entry_pass.get()))
    text_output = Text(menu_conexion)

    # Posicionar los widgets
    label_host.grid(row=0, column=0, sticky="W")
    entry_host.grid(row=0, column=0, sticky="W", padx=80)
    label_user.grid(row=1, column=0, sticky="W")
    entry_user.grid(row=1, column=0, sticky="W", padx=80)
    label_pass.grid(row=2, column=0, sticky="W")
    entry_pass.grid(row=2, column=0, sticky="W", padx=80)
    button_exec.grid(row=3, column=0, sticky="W", padx=100)


def centrar_ventana(ancho_ventana, alto_ventana):
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    # ancho_ventana = ventana.winfo_width()
    # altura_ventana = ventana.winfo_height()
    pos_x = (ancho_pantalla // 2) - (ancho_ventana // 2)
    pos_y = (alto_pantalla // 2) - (alto_ventana // 2)
    ventana.geometry('{}x{}+{}+{}'.format(ancho_ventana,
                                          alto_ventana, pos_x, pos_y))


ventana = Tk()
ventana.resizable(0, 0)

crear_menu_connect()

ventana.mainloop()

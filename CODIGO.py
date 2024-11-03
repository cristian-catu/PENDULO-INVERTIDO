#UNIVERSIDAD DEL VALLE DE GUATEMALA
#CRISTIAN ANIBAL CATU RIERA 20295
#TRABAJO DE GRADUACIÓN - PLATAFORMAS DE APRENDIZAJE: PÉNDULO INVERTIDO

import serial
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial.tools.list_ports
from tkinter import messagebox
import re

# Inicializa las listas para almacenar los datos
angulo2_data = []
v_angular2_data = []
distance_data = []
v_lineal_data = []
puerto_conectado = False

# Pestaña 1: Configura la figura de Matplotlib con subplots en una cuadrícula 2x2
fig, axs = plt.subplots(2, 2, figsize=(7, 5))
axs[0, 0].set_ylim(-180, 180)
axs[0, 0].set_title('Ángulo')
axs[0, 0].set_ylabel('grados')
line1, = axs[0, 0].plot([], [], color='red')
axs[0, 0].grid(True)

axs[0, 1].set_ylim(-200, 200)
axs[0, 1].set_title('Velocidad Angular')
axs[0, 1].set_ylabel('grad/s')
line2, = axs[0, 1].plot([], [], color='orange')
axs[0, 1].grid(True)

axs[1, 0].set_ylim(-800, 800)
axs[1, 0].set_title('Distancia')
axs[1, 0].set_ylabel('mm')
line3, = axs[1, 0].plot([], [], color='blue')
axs[1, 0].grid(True)

axs[1, 1].set_ylim(-300, 300)
axs[1, 1].set_title('Velocidad Lineal')
axs[1, 1].set_ylabel('mm/s')
line4, = axs[1, 1].plot([], [], color='green')
fig.subplots_adjust(hspace=0.3,wspace=0.5)
axs[1, 1].grid(True)

# Pestaña 2: Configura la figura de Matplotlib con solo la gráfica del ángulo
fig2, ax2 = plt.subplots(figsize=(6, 5))
ax2.set_ylim(-20, 20)
ax2.set_title('Ángulo')
ax2.set_ylabel('grados')
line5, = ax2.plot([], [], color='red')
ax2.grid(True)

# Pestaña 3: Configura la figura de Matplotlib con subplots en una cuadrícula 2x2
fig3, axs3 = plt.subplots(2, 2, figsize=(7, 5))
axs3[0, 0].set_ylim(-30, 30)
axs3[0, 0].set_title('Ángulo')
axs3[0, 0].set_ylabel('grados')
line9, = axs3[0, 0].plot([], [], color='red')
axs3[0, 0].grid(True)

axs3[0, 1].set_ylim(-200, 200)
axs3[0, 1].set_title('Velocidad Angular')
axs3[0, 1].set_ylabel('grad/s')
line10, = axs3[0, 1].plot([], [], color='orange')
axs3[0, 1].grid(True)

axs3[1, 0].set_ylim(-800, 800)
axs3[1, 0].set_title('Distancia')
axs3[1, 0].set_ylabel('mm')
line11, = axs3[1, 0].plot([], [], color='blue')
axs3[1, 0].grid(True)

axs3[1, 1].set_ylim(-700, 700)
axs3[1, 1].set_title('Velocidad Lineal')
axs3[1, 1].set_ylabel('mm/s')
line12, = axs3[1, 1].plot([], [], color='green')
axs3[1, 1].grid(True)

fig3.subplots_adjust(hspace=0.3)


def obtener_puertos_com():
    return [port.device for port in serial.tools.list_ports.comports()]


def update(frame):
    global puerto_conectado
    if puerto_conectado:  # Verifica si el puerto está conectado y abierto
        try:
            line = ser.readline().decode('utf-8').strip()
            # El resto de tu código para procesar los datos
        except Exception as e:
            label_estado_conexion.config(text=f"Error leyendo datos: {str(e)}")
            return line1, line2, line3, line4
    else:
        return line1, line2, line3, line4
    try:
        data = json.loads(line)
        angulo2_data.append(float(data['d1']))
        v_angular2_data.append(data['d2'])
        distance_data.append(data['d3'])
        v_lineal_data.append(data['d4'])
        angulo_medido = data['d5']  # Asume que 'd5' es enviado como parte del JSON

        label_angulo_medido.config(text=f"Angulo medido: {angulo_medido}°")  # Actualiza el label con el valor recibido

        if len(angulo2_data) > 100:
            angulo2_data.pop(0)
            v_angular2_data.pop(0)
            distance_data.pop(0)
            v_lineal_data.pop(0)

        line1.set_data(range(len(angulo2_data)), angulo2_data)
        line2.set_data(range(len(v_angular2_data)), v_angular2_data)
        line3.set_data(range(len(distance_data)), distance_data)
        line4.set_data(range(len(v_lineal_data)), v_lineal_data)

        for ax in axs.flat:
            ax.set_xlim(max(0, len(angulo2_data) - 100), len(angulo2_data))
    except json.JSONDecodeError:
        pass
    return line1, line2, line3, line4

def update_tab2(frame):
    global puerto_conectado
    if puerto_conectado:  # Verifica si el puerto está conectado y abierto
        try:
            line = ser.readline().decode('utf-8').strip()
            # El resto de tu código para procesar los datos
        except Exception as e:
            label_estado_conexion.config(text=f"Error leyendo datos: {str(e)}")
            return line5,
    else:
        return line5,
    try:
        data = json.loads(line)
        angulo2_data.append(float(data['d1']))
        angulo_medido2 = data['d5'] 

        label_angulo_medido2.config(text=f"Angulo medido: {angulo_medido2}°")
        if len(angulo2_data) > 100:
            angulo2_data.pop(0)

        line5.set_data(range(len(angulo2_data)), angulo2_data)
        ax2.set_xlim(max(0, len(angulo2_data) - 100), len(angulo2_data))
    except json.JSONDecodeError:
        pass
    return line5,

def update_tab3(frame):
    global puerto_conectado
    if puerto_conectado:  # Verifica si el puerto está conectado y abierto
        try:
            line = ser.readline().decode('utf-8').strip()
            # El resto de tu código para procesar los datos
        except Exception as e:
            label_estado_conexion.config(text=f"Error leyendo datos: {str(e)}")
            return line9, line10, line11, line12
    else:
        return line9, line10, line11, line12
    try:
        data = json.loads(line)
        angulo2_data.append(float(data['d1']))
        v_angular2_data.append(data['d2'])
        distance_data.append(data['d3'])
        v_lineal_data.append(data['d4'])
        angulo_medido3 = data['d5'] 

        label_angulo_medido3.config(text=f"Angulo medido: {angulo_medido3}°")

        if len(angulo2_data) > 100:
            angulo2_data.pop(0)
            v_angular2_data.pop(0)
            distance_data.pop(0)
            v_lineal_data.pop(0)

        line9.set_data(range(len(angulo2_data)), angulo2_data)
        line10.set_data(range(len(v_angular2_data)), v_angular2_data)
        line11.set_data(range(len(distance_data)), distance_data)
        line12.set_data(range(len(v_lineal_data)), v_lineal_data)

        for ax3 in axs3.flat:
            ax3.set_xlim(max(0, len(angulo2_data) - 100), len(angulo2_data))
    except json.JSONDecodeError:
        pass
    return line9, line10, line11, line12


# Configura la GUI de Tkinter
root = tk.Tk()

root.title("Interfaz de control para péndulo invertido")
root.geometry("1500x800+10+10")  # Ajusta el tamaño según tus necesidades


# Crea el contenedor de pestañas
notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))


# Valores iniciales de las variables
initial_values = {
    'amperaje': '800',
    'microstep': '16',
    'velocidad_maxima': '32000',
    'aceleracion': '150000',
    't_muestreo': '1',
    'offset': '283'
}

# Función para enviar los datos de los Entry en la pestaña 1
def send_config():

    initial_values['t_muestreo'] = entry_t_muestreo.get()
    initial_values['offset'] = entry_offset.get()

    config_data = {
        'amperaje': entry_amperaje.get(),
        'microstep': entry_microstep.get(),
        'velocidad_maxima': entry_velocidad_maxima.get(),
        'aceleracion': entry_aceleracion.get(),
        't_muestreo': entry_t_muestreo.get(),
        'offset': entry_offset.get()
    }
    try:
        ser.write((json.dumps(config_data) + '\n').encode('utf-8'))
    except:
        pass

    # Restaurar el color de fondo a blanco en los Entry después de enviar
    entry_amperaje.config(bg="white")
    entry_microstep.config(bg="white")
    entry_velocidad_maxima.config(bg="white")
    entry_aceleracion.config(bg="white")
    entry_t_muestreo.config(bg="white")
    entry_offset.config(bg="white")



# Pestaña 1 - Contendrá las gráficas originales y los Entry para configuración
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text='Configuración')

# Crear el frame izquierdo para el Label "Angulo medido", el nuevo Entry, y las gráficas
left_frame1 = ttk.Frame(tab1)
left_frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Crear un frame superior dentro del frame izquierdo para contener el label, el entry y el botón
top_frame = ttk.Frame(left_frame1)
top_frame.pack(fill=tk.X, padx=10, pady=5, anchor='nw')

# Función para mostrar el cuadro de ayuda
def mostrar_ayuda():
    mensaje_ayuda = (
        "Bienvenido a la interfaz de control serial.\n\n"
        "1. Selecciona un puerto COM disponible y presiona 'Conectar'.\n"
        "2. Configura las variables de estado como Amperaje, Velocidad, etc.\n"
        "3. Usa el campo de 'Velocidad Motor' para ajustar la velocidad del motor en rangos de -32000 a 32000.\n"
        "4. Observa las gráficas en tiempo real para monitorear el ángulo, velocidad angular, distancia y velocidad lineal.\n"
        "5. En caso de necesitar resetear la distancia, presiona 'Reiniciar Distancia'.\n"
        "6. Cambia la dirección del péndulo usando el botón de dirección.\n\n"
        "IMPORTANTE: Calibra el péndulo con Offset (°) y establece la dirección antes de iniciar cualquier control\n\n"
        "Si necesitas más asistencia, contacta al soporte (+502) 3273-6867"
    )
    messagebox.showinfo("Ayuda - Interfaz de Control", mensaje_ayuda)

# Crear el botón de ayuda en la esquina superior derecha de la pestaña 1
btn_ayuda = tk.Button(tab1, text="Ayuda", command=mostrar_ayuda)
btn_ayuda.pack(side=tk.TOP, anchor='ne', padx=10, pady=10)

# Crear el frame superior dentro del frame izquierdo para contener el desplegable y el botón de conectar
top_frame_com = ttk.Frame(left_frame1)
top_frame_com.pack(fill=tk.X, padx=10, pady=5, anchor='nw')

# Crear la lista desplegable para los puertos COM disponibles
label_puerto_com = tk.Label(top_frame_com, text="Puerto COM:", font=("Arial", 12))
label_puerto_com.pack(side=tk.LEFT, padx=10)

puertos_disponibles = obtener_puertos_com()
selected_com = tk.StringVar()
com_dropdown = ttk.Combobox(top_frame_com, textvariable=selected_com, values=puertos_disponibles, state='readonly')
com_dropdown.pack(side=tk.LEFT, padx=10)

def conectar_puerto():
    puerto_seleccionado = com_dropdown.get()  # Obtiene el puerto seleccionado de la lista desplegable
    global ser, puerto_conectado
    if puerto_seleccionado:
        try:
            ser = serial.Serial(puerto_seleccionado, 115200)  # Intenta conectar al puerto seleccionado
            puerto_conectado = True  # Establece la bandera en True cuando hay una conexión exitosa
            label_estado_conexion.config(text=f"Conectado a {puerto_seleccionado}")
        except Exception as e:  # Captura cualquier otra excepción
            label_estado_conexion.config(text=f"Error inesperado: {str(e)}")
            puerto_conectado = False


# Botón para conectar al puerto seleccionado
btn_conectar = tk.Button(top_frame_com, text="Conectar", command=conectar_puerto)
btn_conectar.pack(side=tk.LEFT, padx=10)

# Etiqueta para mostrar el estado de la conexión
label_estado_conexion = tk.Label(top_frame_com, text="No conectado", font=("Arial", 12))
label_estado_conexion.pack(side=tk.LEFT, padx=10)




# Crear el label "Angulo medido"
label_angulo_medido = tk.Label(top_frame, text="Angulo medido: --", font=("Arial", 12))
label_angulo_medido.pack(side=tk.LEFT, padx=80)

# Añadir espacio antes del conjunto de "Velocidad Motor"
tk.Frame(top_frame, width=20).pack(side=tk.LEFT)  # Añade un pequeño espacio ajustable

# Crear el label "Velocidad Motor"
label_velocidad_motor = tk.Label(top_frame, text="Velocidad Motor (steps/s):", font=("Arial", 12))
label_velocidad_motor.pack(side=tk.LEFT, padx=10)

def validar_numeros(entry_value):
    # Expresión regular que permite números negativos y decimales en cualquier orden
    regex = re.compile(r'^-?\d*\.?\d*$')
    
    # Verificar si el valor ingresado coincide con el patrón
    return bool(regex.match(entry_value))

validacion = tab1.register(validar_numeros)

# Crear un Entry para "Motor"
entry_motor = tk.Entry(top_frame, width=10, validate="key", validatecommand=(validacion, '%P'))
entry_motor.pack(side=tk.LEFT, padx=10)

# Función para enviar los datos del motor
def enviar_motor(event):
    valor_motor = entry_motor.get()  # Obtener el valor del Entry
    data = {'motor': valor_motor}
    try:
        ser.write((json.dumps(data) + '\n').encode('utf-8'))
    except:
        pass    
    entry_motor.delete(0, tk.END)

# Vincular la tecla "Enter" al Entry
entry_motor.bind('<Return>', enviar_motor)


# Agregar una línea divisora
separator0 = ttk.Separator(left_frame1, orient='horizontal')
separator0.pack(fill=tk.X, pady=10)

# Agregar el título "Variables de Estado" debajo del top frame
tk.Label(left_frame1, text="Variables de Estado", font=("Arial", 14)).pack(pady=10)

# Colocar las gráficas debajo del título "Variables de Estado"
canvas1 = FigureCanvasTkAgg(fig, master=left_frame1)
canvas1.get_tk_widget().pack(fill=tk.NONE, expand=False)

# Crear el frame derecho para los Entry y el botón en la pestaña 1
right_frame1 = ttk.Frame(tab1)
right_frame1.pack(side=tk.RIGHT, fill=tk.NONE, expand=False, padx=10, pady=0)

# Agregar el título "Configuración" en la parte superior del right_frame1
tk.Label(right_frame1, text="Configuración", font=("Arial", 14)).pack(pady=0)

# Crear un frame para las entradas
entry_frame = ttk.Frame(right_frame1)
entry_frame.pack(expand=True, pady=(0, 0))  # Reducir el espacio para que el botón esté más cerca

# Crear los frames para cada columna dentro de entry_frame
frame_col1 = ttk.Frame(entry_frame)
frame_col1.pack(side=tk.LEFT, padx=5, pady=0)

frame_col2 = ttk.Frame(entry_frame)
frame_col2.pack(side=tk.RIGHT, padx=5, pady=0)





# Crear los Entry y Labels para la primera columna
tk.Label(frame_col1, text="Amperaje (mA)").pack(padx=5, pady=5)
entry_amperaje = tk.Entry(frame_col1, validate="key", validatecommand=(validacion, '%P'))
entry_amperaje.pack(padx=5, pady=5)
entry_amperaje.insert(0, initial_values['amperaje'])

tk.Label(frame_col1, text="Velocidad Máxima (steps/s)").pack(padx=5, pady=5)
entry_velocidad_maxima = tk.Entry(frame_col1, validate="key", validatecommand=(validacion, '%P'))
entry_velocidad_maxima.pack(padx=5, pady=5)
entry_velocidad_maxima.insert(0, initial_values['velocidad_maxima'])

tk.Label(frame_col1, text="T Muestreo (ms)").pack(padx=5, pady=5)
entry_t_muestreo = tk.Entry(frame_col1, validate="key", validatecommand=(validacion, '%P'))
entry_t_muestreo.pack(padx=5, pady=0)
entry_t_muestreo.insert(0, initial_values['t_muestreo'])

# Crear los Entry y Labels para la segunda columna
tk.Label(frame_col2, text="Microstep (2,4,8,16,32)").pack(padx=5, pady=5)
entry_microstep = tk.Entry(frame_col2, validate="key", validatecommand=(validacion, '%P'))
entry_microstep.pack(padx=5, pady=5)
entry_microstep.insert(0, initial_values['microstep'])

tk.Label(frame_col2, text="Aceleración (steps/s2)").pack(padx=5, pady=5)
entry_aceleracion = tk.Entry(frame_col2, validate="key", validatecommand=(validacion, '%P'))
entry_aceleracion.pack(padx=5, pady=5)
entry_aceleracion.insert(0, initial_values['aceleracion'])

tk.Label(frame_col2, text="Offset (°)").pack(padx=5, pady=5)
entry_offset = tk.Entry(frame_col2, validate="key", validatecommand=(validacion, '%P'))
entry_offset.pack(padx=5, pady=0)
entry_offset.insert(0, initial_values['offset'])


# Crear el botón Modificar
btn_modificar = tk.Button(right_frame1, text="Modificar", command= send_config)
btn_modificar.pack(pady=10)  # Reducir el espacio para que esté más pegado a los Entry

# Agregar una línea divisora
separator = ttk.Separator(right_frame1, orient='horizontal')
separator.pack(fill=tk.X, pady=10)

# Agregar el título "Reiniciar Distancia" y un botón "Reiniciar" debajo del separador
reiniciar_frame = ttk.Frame(right_frame1)
reiniciar_frame.pack(pady=10, fill=tk.X)

# Función para enviar el comando de reinicio
def enviar_reiniciar():
    data = {'reiniciar': 1}
    try:
        ser.write((json.dumps(data) + '\n').encode('utf-8'))
    except:
        pass

tk.Label(reiniciar_frame, text="Reiniciar Distancia", font=("Arial", 14)).pack(pady=5)
btn_reiniciar = tk.Button(reiniciar_frame, text="Reiniciar", command=enviar_reiniciar)
btn_reiniciar.pack()




# Añadir otra línea divisora debajo del botón "Reiniciar"
separator2 = ttk.Separator(right_frame1, orient='horizontal')
separator2.pack(fill=tk.X, pady=10)

# Agregar el título "Dirección"
tk.Label(right_frame1, text="Dirección péndulo", font=("Arial", 14)).pack(pady=5)

# Variable para el estado del péndulo, inicializado en "Abajo"
estado_pendulo = tk.StringVar(value="Abajo")

# Función para cambiar la dirección del péndulo y enviar el JSON correspondiente
def cambiar_direccion():
    if estado_pendulo.get() == "Arriba":
        estado_pendulo.set("Abajo")
        btn_direccion.config(text="Abajo", bg="#FF6666")
        btn_direccion_tab2.config(text="Abajo", bg="#FF6666")
        btn_direccion_tab3.config(text="Abajo", bg="#FF6666")
        enviar_direccion(0)
    else:
        estado_pendulo.set("Arriba")
        btn_direccion.config(text="Arriba", bg="lightgreen")
        btn_direccion_tab2.config(text="Arriba", bg="lightgreen")
        btn_direccion_tab3.config(text="Arriba", bg="lightgreen")
        enviar_direccion(1)

# Crear el botón que cambia de estado y lo envía
btn_direccion = tk.Button(right_frame1, text="Abajo", command=cambiar_direccion, width=20, bg="#FF6666", fg="black")
btn_direccion.pack(pady=10)

# Función para enviar la dirección
def enviar_direccion(direccion):
    data = {'direccion': direccion}
    try:
        ser.write((json.dumps(data) + '\n').encode('utf-8'))
    except:
        pass



# Función que cambia el color de fondo a amarillo cuando el usuario empieza a escribir
def on_entry_change(event):
    event.widget.config(bg="yellow")

# Vincula la función on_entry_change a los eventos de los Entry en la pestaña 1
entry_amperaje.bind("<Key>", on_entry_change)
entry_microstep.bind("<Key>", on_entry_change)
entry_velocidad_maxima.bind("<Key>", on_entry_change)
entry_aceleracion.bind("<Key>", on_entry_change)
entry_t_muestreo.bind("<Key>", on_entry_change)
entry_offset.bind("<Key>", on_entry_change)

# Inicializa la animación para las gráficas en la pestaña 1
ani1 = FuncAnimation(fig, update, interval=15, blit=False, cache_frame_data=False)




# Valores iniciales para las variables PID
pid_initial_values = {  
    'kp': '900',
    'ki': '0.001',
    'kd': '0.001',
    'stepper': '2'
}

# Función para enviar los datos de PID en la pestaña 2
def send_pid_config():
    pid_config = {
        'kp': entry_kp.get(),
        'ki': entry_ki.get(),
        'kd': entry_kd.get()
    }
    try:
        ser.write((json.dumps(pid_config) + '\n').encode('utf-8'))
    except:
        pass

    entry_kp.config(bg="white")
    entry_ki.config(bg="white")
    entry_kd.config(bg="white")

# Función para enviar los datos de HOLA y ADIOS en la pestaña 3
def send_offset_t_muestreo():
# Actualizar el diccionario con los valores actuales de los Entry
    if notebook.index(notebook.select()) == 1:
        initial_values['t_muestreo'] = entry_t_muestreo2.get()
        initial_values['offset'] = entry_offset2.get()
        offset_t_muestreo = {
            't_muestreo': entry_t_muestreo2.get(),
            'offset': entry_offset2.get(),
            'stepper': entry_stepper.get()
        }
        entry_t_muestreo2.config(bg="white")
        entry_offset2.config(bg="white")
        entry_stepper.config(bg="white")

    elif notebook.index(notebook.select()) == 2:
        initial_values['t_muestreo'] = entry_t_muestreo3.get()
        initial_values['offset'] = entry_offset3.get()
        offset_t_muestreo = {
            't_muestreo': entry_t_muestreo3.get(),
            'offset': entry_offset3.get(),
            'punto': entry_punto.get(),
        }
        entry_t_muestreo3.config(bg="white")
        entry_offset3.config(bg="white")
        entry_punto.config(bg="white")
    try:
        ser.write((json.dumps(offset_t_muestreo) + '\n').encode('utf-8'))
    except:
        pass

# Pestaña 2 - Solo gráfica de ángulo y configuración PID
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text='Control PID')

# Crear el frame izquierdo para la gráfica en la pestaña 2
left_frame2 = ttk.Frame(tab2)
left_frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Función para mostrar el cuadro de ayuda en la pestaña 2
def mostrar_ayuda_tab2():
    mensaje_ayuda = (
        "Bienvenido a la interfaz de control PID (Pestaña Control PID).\n\n"
        "1. Ajusta los valores de PID (Kp, Ki, Kd) para controlar el sistema.\n"
        "2. Configura los parámetros adicionales como el tiempo de muestreo y el offset angular.\n"
        "3. Observa la gráfica de ángulo para monitorear el comportamiento del sistema en tiempo real.\n\n"
        "IMPORTANTE: Calibra el péndulo con Offset (°) y establece la dirección antes de iniciar cualquier control\n\n"
        "Los valores funcionales para estabilizar el péndulo son los siguientes\n"
        "Abajo:                     Arriba: \n"
        "   Kp = 900                   Kp = 15000\n"
        "   Ki = 0.001                      Ki = 0\n"
        "   Kd = 0.001                    Kd = 0\n\n"
        "Si necesitas más asistencia, contacta al soporte (+502) 3273-6867"
    )
    messagebox.showinfo("Ayuda - Pestaña Control PID", mensaje_ayuda)

# Crear el botón de ayuda en la esquina superior derecha de la pestaña 2
btn_ayuda_tab2 = tk.Button(tab2, text="Ayuda", command=mostrar_ayuda_tab2)
btn_ayuda_tab2.pack(side=tk.TOP, anchor='ne', padx=10, pady=10)

# Crear el label "Angulo medido"
label_angulo_medido2 = tk.Label(left_frame2, text="Angulo medido: --", font=("Arial", 12))
label_angulo_medido2.pack(padx=5, pady=5)

# Agregar el título "Variables de Estado" debajo del top frame
tk.Label(left_frame2, text="Salida del sistema", font=("Arial", 14)).pack(pady=10)

# Crear el canvas para la gráfica en la pestaña 2
canvas2 = FigureCanvasTkAgg(fig2, master=left_frame2)
canvas2.get_tk_widget().pack(fill=tk.NONE, expand=False)

# Crear el frame derecho para los Entry y el botón en la pestaña 2
right_frame2 = ttk.Frame(tab2)
right_frame2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Agregar el título "PID" en la parte superior del right_frame2
tk.Label(right_frame2, text="PID", font=("Arial", 14)).pack(pady=10)

# Registro de la función de validación para los Entry de la pestaña 2
validacion_tab2 = tab2.register(validar_numeros)

# Crear los Entry para cada parámetro PID en la pestaña 2
tk.Label(right_frame2, text="Kp").pack(padx=5, pady=5)
entry_kp = tk.Entry(right_frame2, validate="key", validatecommand=(validacion_tab2, '%P'))
entry_kp.pack(padx=5, pady=5)
entry_kp.insert(0, pid_initial_values['kp'])

tk.Label(right_frame2, text="Ki").pack(padx=5, pady=5)
entry_ki = tk.Entry(right_frame2, validate="key", validatecommand=(validacion_tab2, '%P'))
entry_ki.pack(padx=5, pady=5)
entry_ki.insert(0, pid_initial_values['ki'])

tk.Label(right_frame2, text="Kd").pack(padx=5, pady=5)
entry_kd = tk.Entry(right_frame2, validate="key", validatecommand=(validacion_tab2, '%P'))
entry_kd.pack(padx=5, pady=5)
entry_kd.insert(0, pid_initial_values['kd'])

# Crear el botón Modificar, centrado debajo de los Entry
btn_modify_pid = tk.Button(right_frame2, text="Modificar", command=send_pid_config)
btn_modify_pid.pack(pady=10)

# Crear un nuevo frame para los Entry de T Muestreo y Offset
extra_frame2 = ttk.Frame(tab2)
extra_frame2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Agregar el título "Configuración Extra" en la parte superior del extra_frame2
tk.Label(extra_frame2, text="Configuración", font=("Arial", 14)).pack(pady=10)

# Crear los Entry para T Muestreo y Offset en la pestaña 2
tk.Label(extra_frame2, text="T Muestreo (ms)").pack(padx=5, pady=5)
entry_t_muestreo2 = tk.Entry(extra_frame2, validate="key", validatecommand=(validacion_tab2, '%P'))
entry_t_muestreo2.pack(padx=5, pady=5)
entry_t_muestreo2.insert(0, initial_values['t_muestreo'])

tk.Label(extra_frame2, text="Offset angular (°)").pack(padx=5, pady=5)
entry_offset2 = tk.Entry(extra_frame2, validate="key", validatecommand=(validacion_tab2, '%P'))
entry_offset2.pack(padx=5, pady=5)
entry_offset2.insert(0, initial_values['offset'])

tk.Label(extra_frame2, text="Tiempo stepper (ms)").pack(padx=5, pady=5)
entry_stepper = tk.Entry(extra_frame2, validate="key", validatecommand=(validacion_tab2, '%P'))
entry_stepper.pack(padx=5, pady=5)
entry_stepper.insert(0, pid_initial_values['stepper'])

# Crear el botón Modificar para T Muestreo y Offset, centrado debajo de los Entry
btn_modify3 = tk.Button(extra_frame2, text="Modificar", command=send_offset_t_muestreo)
btn_modify3.pack(pady=10)

# Añadir otra línea divisora debajo del botón "Reiniciar"
separator8 = ttk.Separator(extra_frame2, orient='horizontal')
separator8.pack(fill=tk.X, pady=5)

tk.Label(extra_frame2, text="Dirección Péndulo", font=("Arial", 14)).pack(pady=5)
btn_direccion_tab2 = tk.Button(extra_frame2, text="Abajo", command=cambiar_direccion, width=20, bg="#FF6666", fg="black")
btn_direccion_tab2.pack(pady=10)



# Añadir otra línea divisora debajo del botón "Reiniciar"
separator3 = ttk.Separator(extra_frame2, orient='horizontal')
separator3.pack(fill=tk.X, pady=5)

# Agregar el título "Dirección"
tk.Label(extra_frame2, text="Apagar/encender", font=("Arial", 14)).pack(pady=5)

# Variable para el estado del péndulo, inicializado en "Abajo"
estado2 = tk.StringVar(value="Apagado")

# Función para cambiar la dirección del péndulo y enviar el JSON correspondiente
def cambiar2():
    if estado2.get() == "Apagado":
        estado2.set("Encendido")
        btn_encender.config(text="Encendido", bg="lightgreen")
        enviar_encender(1)
    else:
        estado2.set("Apagado")
        btn_encender.config(text="Apagado", bg="#FF6666")
        enviar_encender(0)

# Crear el botón que cambia de estado y lo envía
btn_encender = tk.Button(extra_frame2, text="Apagado", command=cambiar2, width=20, bg="#FF6666", fg="black")
btn_encender.pack(pady=10)

# Función para enviar la dirección
def enviar_encender(encendido):
    try:
        data = {'encendido1': encendido}
        ser.write((json.dumps(data) + '\n').encode('utf-8'))
    except Exception:
        pass

def on_entry_change_tab2(event):
    event.widget.config(bg="yellow")

entry_kp.bind("<Key>", on_entry_change_tab2)
entry_ki.bind("<Key>", on_entry_change_tab2)
entry_kd.bind("<Key>", on_entry_change_tab2)
entry_t_muestreo2.bind("<Key>", on_entry_change_tab2)
entry_offset2.bind("<Key>", on_entry_change_tab2)
entry_stepper.bind("<Key>", on_entry_change_tab2)


# Animación para la gráfica en la pestaña 2
ani2 = FuncAnimation(fig2, update_tab2, interval=15, blit=False, cache_frame_data=False)


# Valores iniciales para las variables del vector K
vector_k_initial_values = {
    'k1': '2000',
    'k2': '20',
    'k3': '80',
    'k4': '0.4',
    'punto': '0'
}

# Función para enviar los datos del vector K en la pestaña 3
def send_vector_k_config():
    vector_k_config = {
        'k1': entry_k1.get(),
        'k2': entry_k2.get(),
        'k3': entry_k3.get(),
        'k4': entry_k4.get()
    }
    try:
        ser.write((json.dumps(vector_k_config) + '\n').encode('utf-8'))
    except:
        pass
    
    entry_k1.config(bg="white")
    entry_k2.config(bg="white")
    entry_k3.config(bg="white")
    entry_k4.config(bg="white")

# Pestaña 3 - Gráficas y configuración del vector K
tab3 = ttk.Frame(notebook)
notebook.add(tab3, text='Control Variables de Estado')

# Crear el frame izquierdo para las gráficas en la pestaña 3
left_frame3 = ttk.Frame(tab3)
left_frame3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Función para mostrar el cuadro de ayuda en la pestaña 3
def mostrar_ayuda_tab3():
    mensaje_ayuda = (
        "Bienvenido a la pestaña de Control de Variables de Estado.\n\n"
        "1. Ajusta los parámetros del Vector K (K1, K2, K3, K4) para controlar las variables del sistema.\n"
        "2. Configura el tiempo de muestreo, el offset angular, y la distancia final.\n"
        "3. Observa las gráficas en tiempo real de las variables de estado, incluyendo el ángulo, la velocidad angular, la distancia y la velocidad lineal.\n\n"
        "IMPORTANTE: Calibra el péndulo con Offset (°) y establece la dirección antes de iniciar cualquier control\n\n"
        "Los valores funcionales para estabilizar el péndulo son los siguientes\n"
        "Abajo:                     Arriba: \n"
        "   K1 = 2000                  K1 = 1500\n"
        "   K2 = 20                      K2 = 250\n"
        "   K3 = 80                      K3 = -15\n"
        "   K4 = 0.4                     K4 = -50\n\n"
        "Si necesitas más asistencia, contacta al soporte (+502) 3273-6867"
    )
    messagebox.showinfo("Ayuda - Pestaña Control Variables de Estado", mensaje_ayuda)

# Crear el botón de ayuda en la esquina superior derecha de la pestaña 3
btn_ayuda_tab3 = tk.Button(tab3, text="Ayuda", command=mostrar_ayuda_tab3)
btn_ayuda_tab3.pack(side=tk.TOP, anchor='ne', padx=10, pady=10)

# Crear el label "Angulo medido"
label_angulo_medido3 = tk.Label(left_frame3, text="Angulo medido: --", font=("Arial", 12))
label_angulo_medido3.pack(padx=5, pady=5)

# Agregar el título "Variables de Estado" en la parte superior del left_frame3
tk.Label(left_frame3, text="Variables de Estado", font=("Arial", 14)).pack(pady=10)

# Crear el canvas para las gráficas en la pestaña 3
canvas3 = FigureCanvasTkAgg(fig3, master=left_frame3)
canvas3.get_tk_widget().pack(fill=tk.NONE, expand=False)

# Crear el frame derecho para los Entry y el botón en la pestaña 3
right_frame3 = ttk.Frame(tab3)
right_frame3.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Agregar el título "Vector K" en la parte superior del right_frame3
tk.Label(right_frame3, text="Vector K", font=("Arial", 14)).pack(pady=10)

# Registro de la función de validación para los Entry de la pestaña 3
validacion_tab3 = tab3.register(validar_numeros)

# Crear los Entry para cada parámetro del vector K en la pestaña 3
tk.Label(right_frame3, text="K1").pack(padx=5, pady=5)
entry_k1 = tk.Entry(right_frame3, validate="key", validatecommand=(validacion_tab3, '%P'))
entry_k1.pack(padx=5, pady=5)
entry_k1.insert(0, vector_k_initial_values['k1'])

tk.Label(right_frame3, text="K2").pack(padx=5, pady=5)
entry_k2 = tk.Entry(right_frame3, validate="key", validatecommand=(validacion_tab3, '%P'))
entry_k2.pack(padx=5, pady=5)
entry_k2.insert(0, vector_k_initial_values['k2'])

tk.Label(right_frame3, text="K3").pack(padx=5, pady=5)
entry_k3 = tk.Entry(right_frame3, validate="key", validatecommand=(validacion_tab3, '%P'))
entry_k3.pack(padx=5, pady=5)
entry_k3.insert(0, vector_k_initial_values['k3'])

tk.Label(right_frame3, text="K4").pack(padx=5, pady=5)
entry_k4 = tk.Entry(right_frame3, validate="key", validatecommand=(validacion_tab3, '%P'))
entry_k4.pack(padx=5, pady=5)
entry_k4.insert(0, vector_k_initial_values['k4'])

# Crear el botón Modificar, centrado debajo de los Entry del vector K
btn_modify_vector_k = tk.Button(right_frame3, text="Modificar", command=send_vector_k_config)
btn_modify_vector_k.pack(pady=10)

# Crear un nuevo frame para los Entry
extra_frame = ttk.Frame(tab3)
extra_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Agregar el título "Configuración Extra" en la parte superior del extra_frame
tk.Label(extra_frame, text="Configuración", font=("Arial", 14)).pack(pady=10)

# Crear los Entry para T Muestreo, Offset y Distancia Final en la pestaña 3
tk.Label(extra_frame, text="T Muestreo (ms)").pack(padx=5, pady=5)
entry_t_muestreo3 = tk.Entry(extra_frame, validate="key", validatecommand=(validacion_tab3, '%P'))
entry_t_muestreo3.pack(padx=5, pady=5)
entry_t_muestreo3.insert(0, initial_values['t_muestreo'])

tk.Label(extra_frame, text="Offset angular (°)").pack(padx=5, pady=5)
entry_offset3 = tk.Entry(extra_frame, validate="key", validatecommand=(validacion_tab3, '%P'))
entry_offset3.pack(padx=5, pady=5)
entry_offset3.insert(0, initial_values['offset'])

tk.Label(extra_frame, text="Distancia final (mm)").pack(padx=5, pady=5)
entry_punto = tk.Entry(extra_frame, validate="key", validatecommand=(validacion_tab3, '%P'))
entry_punto.pack(padx=5, pady=5)
entry_punto.insert(0, vector_k_initial_values['punto'])

# Crear el botón Modificar, centrado debajo de los Entry de HOLA y ADIOS
btn_modify2 = tk.Button(extra_frame, text="Modificar", command=send_offset_t_muestreo)
btn_modify2.pack(pady=10)

# Añadir otra línea divisora debajo del botón "Reiniciar"
separator9 = ttk.Separator(extra_frame, orient='horizontal')
separator9.pack(fill=tk.X, pady=5)

tk.Label(extra_frame, text="Dirección Péndulo", font=("Arial", 14)).pack(pady=5)
btn_direccion_tab3 = tk.Button(extra_frame, text="Abajo", command=cambiar_direccion, width=20, bg="#FF6666", fg="black")
btn_direccion_tab3.pack(pady=10)

# Añadir otra línea divisora debajo del botón "Reiniciar"
separator4 = ttk.Separator(extra_frame, orient='horizontal')
separator4.pack(fill=tk.X, pady=5)

# Agregar el título "Dirección"
tk.Label(extra_frame, text="Apagar/encender", font=("Arial", 14)).pack(pady=5)

# Variable para el estado del péndulo, inicializado en "Abajo"
estado3 = tk.StringVar(value="Apagado")

# Función para cambiar la dirección del péndulo y enviar el JSON correspondiente
def cambiar3():
    if estado3.get() == "Apagado":
        estado3.set("Encendido")
        btn_encender2.config(text="Encendido", bg="lightgreen")
        enviar_encender2(1)
    else:
        estado3.set("Apagado")
        btn_encender2.config(text="Apagado", bg="#FF6666")
        enviar_encender2(0)

# Crear el botón que cambia de estado y lo envía
btn_encender2 = tk.Button(extra_frame, text="Apagado", command=cambiar3, width=20, bg="#FF6666", fg="black")
btn_encender2.pack(pady=10)

# Función para enviar la dirección
def enviar_encender2(encendido):

    try:
        data = {'encendido2': encendido}
        ser.write((json.dumps(data) + '\n').encode('utf-8'))
    except Exception:
        pass

def on_entry_change_tab3(event):
    event.widget.config(bg="yellow")

entry_k1.bind("<Key>", on_entry_change_tab3)
entry_k2.bind("<Key>", on_entry_change_tab3)
entry_k3.bind("<Key>", on_entry_change_tab3)
entry_k4.bind("<Key>", on_entry_change_tab3)
entry_t_muestreo3.bind("<Key>", on_entry_change_tab3)
entry_offset3.bind("<Key>", on_entry_change_tab3)
entry_punto.bind("<Key>", on_entry_change_tab3)

# Animación para la gráfica en la pestaña 3
ani3 = FuncAnimation(fig3, update_tab3, interval=15, blit=False, cache_frame_data=False)


def on_tab_change(event):
    selected_tab = event.widget.index("current")
    mode_data = {'modo': selected_tab + 1}
    try:
        ser.write((json.dumps(mode_data) + '\n').encode('utf-8'))
    except Exception:
        pass

    # Pausa las animaciones de todas las pestañas
    ani1.event_source.stop()
    ani2.event_source.stop()
    ani3.event_source.stop()

    estado2.set("Apagado")
    btn_encender.config(text="Apagado", bg="#FF6666")
    enviar_encender(0)

    estado3.set("Apagado")
    btn_encender2.config(text="Apagado", bg="#FF6666")
    enviar_encender2(0)
    # Reanuda la animación de la pestaña seleccionada
    if selected_tab == 0:
        ani1.event_source.start()

        # Actualiza los Entry de la pestaña 3 con los valores actuales de initial_values
        entry_t_muestreo.delete(0, tk.END)
        entry_t_muestreo.insert(0, initial_values['t_muestreo'])

        entry_offset.delete(0, tk.END)
        entry_offset.insert(0, initial_values['offset'])

    elif selected_tab == 1:
        ani2.event_source.start()

        # Actualiza los Entry de la pestaña 3 con los valores actuales de initial_values
        entry_t_muestreo2.delete(0, tk.END)
        entry_t_muestreo2.insert(0, initial_values['t_muestreo'])

        entry_offset2.delete(0, tk.END)
        entry_offset2.insert(0, initial_values['offset'])

    elif selected_tab == 2:
        ani3.event_source.start()
        # Actualiza los Entry de la pestaña 3 con los valores actuales de initial_values
        entry_t_muestreo3.delete(0, tk.END)
        entry_t_muestreo3.insert(0, initial_values['t_muestreo'])

        entry_offset3.delete(0, tk.END)
        entry_offset3.insert(0, initial_values['offset'])

notebook.bind("<<NotebookTabChanged>>", on_tab_change)

plt.tight_layout()
root.mainloop()
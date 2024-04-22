Documentación del Código

Introducción

Este código define una clase AdministradorRedes que permite gestionar información sobre campus y dispositivos de red. La clase proporciona funciones para cargar y guardar datos de un archivo JSON, agregar y modificar campus y dispositivos, y convertir la información a formato de texto.

Descripción del Código

1. Importaciones:
os: Módulo para operaciones del sistema operativo.
json: Módulo para trabajar con datos JSON.
re: Módulo para expresiones regulares.

2. Clases y Funciones:

Campus: Representa un campus con su nombre y descripción.

__init__(self, nombre, descripcion): Inicializa un nuevo campus.

Dispositivo: Representa un dispositivo de red con sus características.

__init__(self, nombre, modelo, capa, interfaces, ips_masks, vlans, servicios): Inicializa un nuevo dispositivo.

AdministradorRedes: Representa un administrador de redes que gestiona campus y dispositivos.

__init__(self, nombre_archivo): Inicializa un nuevo administrador de redes con el nombre del archivo para guardar los datos.

cargar_desde_archivo(self): Carga los datos del archivo JSON especificado.

guardar_en_archivo(self): Guarda los datos en el archivo JSON especificado.

interpretar_json_y_guardar_texto(self, archivo_texto): Interpreta los datos del archivo JSON, los convierte a formato de texto y los guarda en un archivo de texto.

convertir_a_formato_texto(self): Convierte los datos a formato de texto.

menu_principal(self): Muestra el menú principal y permite al usuario seleccionar una opción.

administrar_campus(self): Muestra el menú de administración de campus y permite al usuario seleccionar una opción.

agregar_campus(self): Agrega un nuevo campus.

modificar_campus(self): Modifica la descripción de un campus existente.

borrar_campus(self): Elimina un campus existente.

administrar_dispositivos(self): Muestra el menú de administración de dispositivos y permite al usuario seleccionar una opción.

agregar_dispositivos(self, nombre_campus): Agrega dispositivos a un campus existente.

seleccionar_capa(self): Muestra el menú de selección de capa y permite al usuario seleccionar una opción.

ingresar_ips_masks(self, interfaces): Solicita al usuario ingresar las direcciones IP y máscaras de red para las interfaces de un dispositivo.

ingresar_vlans(self): Solicita al usuario ingresar los nombres y números de VLAN para un dispositivo.

es_direccion_ipv4(direccion): Verifica si una cadena de dirección ip esta bien ingresada.

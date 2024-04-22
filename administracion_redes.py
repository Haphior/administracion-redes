import os
import re

class Campus:
    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion
        self.dispositivos = []

class Dispositivo:
    def __init__(self, nombre, modelo, capa, interfaces, ips, vlans, servicios):
        self.nombre = nombre
        self.modelo = modelo
        self.capa = capa
        self.interfaces = interfaces
        self.ips = ips
        self.vlans = vlans
        self.servicios = servicios

def es_direccion_ipv4(direccion):
    patron_ipv4 = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return re.match(patron_ipv4, direccion) is not None

class AdministradorRedes:
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo
        self.campus = {}
        if os.path.exists(nombre_archivo):
            self.cargar_desde_archivo()

    def cargar_desde_archivo(self):
        with open(self.nombre_archivo, "r") as archivo:
            seccion_actual = None
            detalles_dispositivo = {}
            for linea in archivo:
                linea = linea.strip()
                if linea == "Campus:":
                    seccion_actual = "campus"
                elif linea == "Dispositivos de Red:":
                    seccion_actual = "dispositivos"
                elif seccion_actual == "campus":
                    partes = linea.split(": ", 1)
                    if len(partes) == 2:
                        nombre, descripcion = partes
                        self.campus[nombre.strip()] = Campus(nombre.strip(), descripcion.strip())
                elif seccion_actual == "dispositivos":
                    if linea:
                        if linea.startswith("    "):  # Verifica si la línea es parte de un dispositivo
                            clave, valor = linea.strip().split(": ")
                            clave = clave.strip()
                            valor = valor.strip()
                            if clave == "Interfaces":
                                valor = valor.split(", ")
                            elif clave == "IPs":
                                valor = valor[1:-1].split(", ")
                            elif clave == "VLANs":
                                valor = dict(pair.split(": ") for pair in valor[1:-1].split(", "))
                            detalles_dispositivo[clave] = valor
                        else:
                            nombre_dispositivo = detalles_dispositivo.pop("Nombre", None)
                            if nombre_dispositivo:
                                dispositivo = Dispositivo(nombre_dispositivo, **detalles_dispositivo)
                                self.campus[self.current_campus].dispositivos.append(dispositivo)
                                detalles_dispositivo = {}

    def guardar_en_archivo(self):
        with open(self.nombre_archivo, "w") as archivo:
            archivo.write("Campus:\n")
            for nombre, campus in self.campus.items():
                archivo.write(f"{campus.nombre}: {campus.descripcion}\n")
            archivo.write("\nDispositivos de Red:\n")
            for campus in self.campus.values():
                for dispositivo in campus.dispositivos:
                    archivo.write(f"{dispositivo.nombre}:\n")
                    for clave, valor in dispositivo.__dict__.items():
                        if clave != "nombre":
                            archivo.write(f"    {clave}: {valor}\n")
                    archivo.write("\n")
        print("Información guardada en el archivo con éxito.")
        input("Presione Enter para continuar.")

    def menu_principal(self):
        while True:
            os.system("clear")
            print("¡Bienvenido al Administrador de Redes!")
            print("1. Administrar campus")
            print("2. Administrar dispositivos de red")
            print("3. Guardar información en archivo de texto")
            print("4. Salir")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                self.administrar_campus()
            elif opcion == "2":
                self.administrar_dispositivos()
            elif opcion == "3":
                self.guardar_en_archivo()
            elif opcion == "4":
                print("¡Hasta luego!")
                break
            else:
                input("Opción no válida. Presione Enter para continuar.")

    def administrar_campus(self):
        while True:
            os.system("clear")
            print("Campus:")
            for nombre, campus in self.campus.items():
                print(f"{campus.nombre}: {campus.descripcion}")
            opcion = input("Seleccione una opción:\n1. Agregar campus\n2. Modificar campus\n3. Borrar campus\n4. Volver al menú principal\n")
            if opcion == "1":
                nombre = input("Ingrese el nombre del campus: ")
                descripcion = input("Ingrese una descripción del campus: ")
                self.campus[nombre] = Campus(nombre, descripcion)
                input("Campus agregado. Presione Enter para continuar.")
            elif opcion == "2":
                nombre = input("Ingrese el nombre del campus que desea modificar: ")
                if nombre in self.campus:
                    nueva_descripcion = input("Ingrese la nueva descripción del campus: ")
                    self.campus[nombre].descripcion = nueva_descripcion
                    input("Campus modificado. Presione Enter para continuar.")
                else:
                    input("El campus especificado no existe. Presione Enter para continuar.")
            elif opcion == "3":
                nombre = input("Ingrese el nombre del campus que desea borrar: ")
                if nombre in self.campus:
                    del self.campus[nombre]
                    input("Campus eliminado. Presione Enter para continuar.")
                else:
                    input("El campus especificado no existe. Presione Enter para continuar.")
            elif opcion == "4":
                break
            else:
                input("Opción no válida. Presione Enter para continuar.")

    def administrar_dispositivos(self):
        while True:
            os.system("clear")
            opcion = input("Seleccione una opción:\n1. Agregar dispositivo\n2. Modificar dispositivo\n3. Volver al menú principal\n")
            if opcion == "1":
                self.agregar_dispositivo()
            elif opcion == "2":
                self.modificar_dispositivo()
            elif opcion == "3":
                break
            else:
                input("Opción no válida. Presione Enter para continuar.")

    def agregar_dispositivo(self):
        os.system("clear")
        print("Campus disponibles:")
        for nombre, campus in self.campus.items():
            print(f"{nombre}: {campus.descripcion}")
        
        nombre_campus = input("Ingrese el nombre del campus en el que desea agregar el dispositivo: ")
        if nombre_campus not in self.campus:
            print("El campus especificado no existe.")
            input("Presione Enter para continuar.")
            return

        nombre = input("Ingrese el nombre del dispositivo: ")
        modelo = input("Ingrese el modelo del dispositivo: ")
        print("Seleccione la capa jerárquica a la que pertenece:")
        print("1) Núcleo")
        print("2) Distribución")
        print("3) Acceso")
        capa_opcion = input("Opción: ")
        if capa_opcion == "1":
            capa = "Núcleo"
        elif capa_opcion == "2":
            capa = "Distribución"
        elif capa_opcion == "3":
            capa = "Acceso"
        else:
            capa = "Desconocida"
        interfaces = input("Ingrese las interfaces de red del dispositivo (separadas por coma): ").split(",")
        ips = []
        for interfaz in interfaces:
            ip_valida = False
            while not ip_valida:
                ip = input(f"Ingrese la dirección IP para la interfaz {interfaz}: ")
                if es_direccion_ipv4(ip):
                    ips.append(ip)
                    ip_valida = True
                else:
                    print("La dirección IP ingresada no es válida. Inténtelo nuevamente.")
        vlans = {}
        while True:
            nombre_vlan = input("Ingrese el nombre de la VLAN (o 'fin' para terminar): ")
            if nombre_vlan.lower() == 'fin':
                break
            numero_vlan = input("Ingrese el número de la VLAN: ")
            vlans[nombre_vlan] = numero_vlan
        servicios = input("Ingrese los servicios de red configurados (separados por coma): ").split(",")

        dispositivo = Dispositivo(nombre, modelo, capa, interfaces, ips, vlans, servicios)
        self.campus[nombre_campus].dispositivos.append(dispositivo)
        input("Dispositivo agregado. Presione Enter para continuar.")

    def modificar_dispositivo(self):
        nombre_campus = input("Ingrese el nombre del campus donde se encuentra el dispositivo que desea modificar: ")
        if nombre_campus not in self.campus:
            print("El campus especificado no existe.")
            input("Presione Enter para continuar.")
            return

        nombre_dispositivo = input("Ingrese el nombre del dispositivo que desea modificar: ")
        campus = self.campus[nombre_campus]
        dispositivo = next((d for d in campus.dispositivos if d.nombre == nombre_dispositivo), None)
        if dispositivo:
            dispositivo.modelo = input("Ingrese el nuevo modelo del dispositivo: ")
            print("Seleccione la nueva capa jerárquica a la que pertenece:")
            print("1) Núcleo")
            print("2) Distribución")
            print("3) Acceso")
            capa_opcion = input("Opción: ")
            if capa_opcion == "1":
                dispositivo.capa = "Núcleo"
            elif capa_opcion == "2":
                dispositivo.capa = "Distribución"
            elif capa_opcion == "3":
                dispositivo.capa = "Acceso"
            else:
                dispositivo.capa = "Desconocida"
            dispositivo.interfaces = input("Ingrese las nuevas interfaces de red del dispositivo (separadas por coma): ").split(",")
            dispositivo.ips = []
            for interfaz in dispositivo.interfaces:
                ip_valida = False
                while not ip_valida:
                    ip = input(f"Ingrese la nueva dirección IP para la interfaz {interfaz}: ")
                    if es_direccion_ipv4(ip):
                        dispositivo.ips.append(ip)
                        ip_valida = True
                    else:
                        print("La dirección IP ingresada no es válida. Inténtelo nuevamente.")
            dispositivo.vlans = {}
            while True:
                nombre_vlan = input("Ingrese el nombre de la VLAN (o 'fin' para terminar): ")
                if nombre_vlan.lower() == 'fin':
                    break
                numero_vlan = input("Ingrese el número de la VLAN: ")
                dispositivo.vlans[nombre_vlan] = numero_vlan
            dispositivo.servicios = input("Ingrese los nuevos servicios de red configurados (separados por coma): ").split(",")
            input("Dispositivo modificado. Presione Enter para continuar.")
        else:
            input("El dispositivo especificado no existe. Presione Enter para continuar.")

if __name__ == "__main__":
    nombre_archivo = input("Ingrese el nombre del archivo para cargar o crear la información: ")
    administrador = AdministradorRedes(nombre_archivo)
    administrador.menu_principal()
    
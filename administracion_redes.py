import os
import re

def es_direccion_ipv4(direccion):
    patron_ipv4 = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return re.match(patron_ipv4, direccion) is not None

class AdministradorRedes:
    def __init__(self, nombre_archivo):
        self.campus = {}
        self.dispositivos = {}
        self.dispositivos_por_campus = {}
        self.nombre_archivo = nombre_archivo

        if os.path.exists(nombre_archivo):
            self.cargar_desde_archivo()


    def cargar_desde_archivo(self):
        seccion_actual = None
        with open(self.nombre_archivo, "r") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if linea == "Campus:":
                    seccion_actual = "campus"
                elif linea == "Dispositivos de Red:":
                    seccion_actual = "dispositivos"
                elif seccion_actual == "campus" or seccion_actual == "dispositivos":
                    partes = linea.split(": ")
                    if len(partes) >= 2:
                        nombre, descripcion = partes[0], partes[1]
                        if seccion_actual == "campus":
                            self.campus[nombre] = descripcion
                            self.dispositivos_por_campus[nombre] = []
                        elif seccion_actual == "dispositivos":
                            self.dispositivos[nombre] = descripcion

    def guardar_en_archivo(self):
        with open(self.nombre_archivo, "w") as archivo:
            archivo.write("Campus:\n")
            for nombre, descripcion in self.campus.items():
                archivo.write(f"{nombre}: {descripcion}\n")

            archivo.write("\nDispositivos de Red:\n")
            for nombre, detalles in self.dispositivos.items():
                archivo.write(f"{nombre}:\n")
                archivo.write(f"    Modelo: {detalles['Modelo']}\n")
                archivo.write(f"    Capa: {detalles['Capa']}\n")
                archivo.write("    Interfaces:\n")
                for interfaz, ip in zip(detalles['Interfaces'], detalles['IPs']):
                    archivo.write(f"        {interfaz}: {ip}\n")
                archivo.write("    VLANs:\n")
                for nombre_vlan, numero_vlan in detalles['VLANs'].items():
                    archivo.write(f"        {nombre_vlan}: {numero_vlan}\n")
                archivo.write("    Servicios:\n")
                for servicio in detalles['Servicios']:
                    archivo.write(f"        {servicio}\n")
                archivo.write("\n")
        print("Archivo guardado con éxito.")
        input("Presione Enter para continuar.")
        self.menu_principal()

    def menu_principal(self):
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
            exit()
        else:
            input("Opción no válida. Presione Enter para continuar.")
            self.menu_principal()

    def administrar_campus(self):
        os.system("clear")
        print("Campus:")
        for nombre, descripcion in self.campus.items():
            print(f"{nombre}: {descripcion}")
        opcion = input("Seleccione una opción:\n1. Agregar campus\n2. Modificar campus\n3. Volver al menú principal\n")
        if opcion == "1":
            nombre = input("Ingrese el nombre del campus: ")
            descripcion = input("Ingrese una descripción del campus: ")
            self.campus[nombre] = descripcion
            self.dispositivos_por_campus[nombre] = []
            input("Campus agregado. Presione Enter para continuar.")
            self.administrar_campus()
        elif opcion == "2":
            nombre = input("Ingrese el nombre del campus que desea modificar: ")
            if nombre in self.campus:
                nueva_descripcion = input("Ingrese la nueva descripción del campus: ")
                self.campus[nombre] = nueva_descripcion
                input("Campus modificado. Presione Enter para continuar.")
            else:
                input("El campus especificado no existe. Presione Enter para continuar.")
            self.administrar_campus()
        elif opcion == "3":
            self.menu_principal()
        else:
            input("Opción no válida. Presione Enter para continuar.")
            self.administrar_campus()

    def administrar_dispositivos(self):
        os.system("clear")
        print("Dispositivos de Red:")
        for nombre, detalles in self.dispositivos.items():
            print(f"{nombre}: {detalles}")
        opcion = input("Seleccione una opción:\n1. Agregar dispositivo\n2. Modificar dispositivo\n3. Volver al menú principal\n")
        if opcion == "1":
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
            detalles = {
                "Modelo": modelo,
                "Capa": capa,
                "Interfaces": interfaces,
                "IPs": ips,
                "VLANs": vlans,
                "Servicios": servicios
            }
            self.dispositivos[nombre] = detalles
            input("Dispositivo agregado. Presione Enter para continuar.")
            self.administrar_dispositivos()
    
        elif opcion == "2":
            nombre = input("Ingrese el nombre del dispositivo que desea modificar: ")
            if nombre in self.dispositivos:
                nuevos_detalles = input("Ingrese los nuevos detalles del dispositivo: ")
                self.dispositivos[nombre] = nuevos_detalles
                input("Dispositivo modificado. Presione Enter para continuar.")
            else:
                input("El dispositivo especificado no existe. Presione Enter para continuar.")
            self.administrar_dispositivos()
    
        elif opcion == "3":
            self.menu_principal()
    
        else:
            input("Opción no válida. Presione Enter para continuar.")
            self.administrar_dispositivos()

if __name__ == "__main__":
    nombre_archivo = input("Ingrese el nombre del archivo para cargar o crear la información: ")
    administrador = AdministradorRedes(nombre_archivo)
    administrador.menu_principal()
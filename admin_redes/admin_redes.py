import os
import json
import re
import requests
from github import Github

class Campus:
    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion
        self.dispositivos = []

class Dispositivo:
    def __init__(self, nombre, modelo, capa, interfaces, ips_masks, vlans, servicios):
        self.nombre = nombre
        self.modelo = modelo
        self.capa = capa
        self.interfaces = interfaces
        self.ips_masks = ips_masks
        self.vlans = vlans
        self.servicios = servicios

class AdministradorRedes:
    def __init__(self, nombre_archivo, token):
        self.nombre_archivo = nombre_archivo
        self.github = Github(token)
        self.repo = None
        self.campus = {}
        self.version_local = self.obtener_version_local()  # Obtener la versión local al iniciar
        if os.path.exists(nombre_archivo):
            self.cargar_desde_archivo()
    
    def obtener_version_local(self):
        if os.path.exists("version.txt"):
            with open("version.txt", "r") as file:
                return file.read().strip()
        else:
            return None

    def obtener_version_github(self):
        contenido = self.repo.get_contents("version.txt")
        return contenido.decoded_content.decode().strip()

    def actualizar_desde_github(self):
        # Comprobar si la versión en GitHub es más reciente
        version_github = self.obtener_version_github()
        if version_github != self.version_local:
            print("¡Hay una versión más reciente disponible en GitHub!")
            confirmacion = input("¿Desea actualizar? (s/n): ").lower()
            if confirmacion == "s":
                # Descargar el nuevo código desde GitHub
                contenido = self.repo.get_contents(__file__)
                with open(__file__, "wb") as file:
                    file.write(contenido.decoded_content)
                # Actualizar la versión local
                self.version_local = version_github
                with open("version.txt", "w") as file:
                    file.write(version_github)
                print("¡Actualización exitosa!")
            else:
                print("Actualización cancelada.")
        else:
            print("No hay actualizaciones disponibles.")

    def cargar_desde_archivo(self):
        with open(self.nombre_archivo, "r") as archivo:
            datos = json.load(archivo)
            for nombre, descripcion in datos["campus"].items():
                campus = Campus(nombre, descripcion)
                self.campus[nombre] = campus
                dispositivos_info = datos.get(nombre, [])
                for dispositivo_info in dispositivos_info:
                    dispositivo = Dispositivo(**dispositivo_info)
                    campus.dispositivos.append(dispositivo)

    def guardar_en_archivo(self):
        datos = {"campus": {}, "dispositivos": {}}
        for nombre, campus in self.campus.items():
            datos["campus"][nombre] = campus.descripcion
            datos[nombre] = [dispositivo.__dict__ for dispositivo in campus.dispositivos]
        with open(self.nombre_archivo, "w") as archivo:
            json.dump(datos, archivo, indent=4)

    def guardar_en_archivo_texto(self, archivo_texto):
        self.guardar_en_archivo()  
        texto_formato = self.convertir_a_formato_texto()
        with open(archivo_texto, "w") as archivo:
            archivo.write(texto_formato)
        print(f"Datos convertidos y guardados en el archivo: {archivo_texto}")

    def convertir_a_formato_texto(self):
        texto_formato = ""
        for nombre, campus in self.campus.items():
            texto_formato += f"Campus: {nombre}\nDescripción: {campus.descripcion}\n"
            for dispositivo in campus.dispositivos:
                texto_formato += f"\nDispositivo: {dispositivo.nombre}\nModelo: {dispositivo.modelo}\nCapa: {dispositivo.capa}\n"
                texto_formato += "Interfaces:\n" + "\n".join([f"- {interface}: IP: {dispositivo.ips_masks[interface][0]}, Máscara: {dispositivo.ips_masks[interface][1]}" for interface in dispositivo.interfaces]) + "\n"
                texto_formato += "VLANs:\n" + "\n".join([f"- {vlan}: {numero}" for vlan, numero in dispositivo.vlans.items()]) + "\n"
                texto_formato += f"Servicios: {', '.join(dispositivo.servicios)}\n" + "-" * 30 + "\n"
        return texto_formato

    @staticmethod
    def es_direccion_ipv4(direccion):
        patron_ipv4 = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        return re.match(patron_ipv4, direccion) is not None

    def menu_principal(self):
        # Realizar el chequeo y la actualización al iniciar
        self.actualizar_desde_github()
        
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
                archivo_texto = input("Ingrese el nombre del archivo de texto para guardar los datos: ")
                self.guardar_en_archivo_texto(archivo_texto)
                input("Presione Enter para continuar.")
            elif opcion == "4":
                print("¡Hasta luego!")
                break
            else:
                input("Opción no válida. Presione Enter para continuar.")

    def administrar_campus(self):
        while True:
            os.system("clear")
            print("Campus:")
            for nombre in sorted(self.campus.keys()):
                print(nombre)
            opcion = input("Seleccione una opción:\n1. Agregar campus\n2. Modificar campus\n3. Borrar campus\n4. Volver al menú principal\n")
            if opcion == "1":
                self.agregar_campus()
            elif opcion == "2":
                self.modificar_campus()
            elif opcion == "3":
                self.borrar_campus()
            elif opcion == "4":
                break
            else:
                input("Opción no válida. Presione Enter para continuar.")

    def agregar_campus(self):
        nombre = input("Ingrese el nombre del campus: ")
        descripcion = input("Ingrese una descripción del campus: ")
        self.campus[nombre] = Campus(nombre, descripcion)
        input("Campus agregado. Presione Enter para continuar.")

    def modificar_campus(self):
        nombre = input("Ingrese el nombre del campus que desea modificar: ")
        if nombre in self.campus:
            nueva_descripcion = input("Ingrese la nueva descripción del campus: ")
            self.campus[nombre].descripcion = nueva_descripcion
            input("Campus modificado. Presione Enter para continuar.")
        else:
            input("El campus especificado no existe. Presione Enter para continuar.")

    def borrar_campus(self):
        nombre = input("Ingrese el nombre del campus que desea borrar: ")
        if nombre in self.campus:
            del self.campus[nombre]
            input("Campus eliminado. Presione Enter para continuar.")
        else:
            input("El campus especificado no existe. Presione Enter para continuar.")

    def administrar_dispositivos(self):
        while True:
            os.system("clear")
            print("Campus disponibles:")
            for nombre, campus in self.campus.items():
                print(f"{nombre}: {campus.descripcion}")
            campus_seleccionado = input("Ingrese el nombre del campus en el que desea administrar dispositivos (o 'fin' para salir): ")
            if campus_seleccionado.lower() == "fin":
                break
            elif campus_seleccionado in self.campus:
                while True:
                    os.system("clear")
                    print("Dispositivos en el campus:")
                    for dispositivo in self.campus[campus_seleccionado].dispositivos:
                        print(dispositivo.nombre)
                    opcion_dispositivo = input("Seleccione una opción:\n1. Agregar dispositivo\n2. Modificar dispositivo\n3. Borrar dispositivo\n4. Volver al menú anterior\n")
                    if opcion_dispositivo == "1":
                        self.agregar_dispositivos(campus_seleccionado)
                    elif opcion_dispositivo == "2":
                        nombre_dispositivo = input("Ingrese el nombre del dispositivo que desea modificar: ")
                        self.modificar_dispositivo(campus_seleccionado, nombre_dispositivo)
                    elif opcion_dispositivo == "3":
                        nombre_dispositivo = input("Ingrese el nombre del dispositivo que desea borrar: ")
                        self.borrar_dispositivo(campus_seleccionado, nombre_dispositivo)
                    elif opcion_dispositivo == "4":
                        break
                    else:
                        input("Opción no válida. Presione Enter para continuar.")
            else:
                print("El campus especificado no existe.")

    def agregar_dispositivos(self, nombre_campus):
        os.system("clear")
        dispositivos_nuevos = []
        while True:
            nombre = input("Ingrese el nombre del dispositivo (o 'fin' para salir): ")
            if nombre.lower() == "fin":
                break
            modelo = input("Ingrese el modelo del dispositivo: ")
            capa = self.seleccionar_capa()
            interfaces = input("Ingrese las interfaces de red del dispositivo (separadas por coma): ").split(",")
            ips_masks = self.ingresar_ips_masks(interfaces)
            vlans = self.ingresar_vlans()
            servicios = input("Ingrese los servicios de red configurados (separados por coma): ").split(",")
            dispositivo = Dispositivo(nombre, modelo, capa, interfaces, ips_masks, vlans, servicios)
            dispositivos_nuevos.append(dispositivo)
        self.campus[nombre_campus].dispositivos.extend(dispositivos_nuevos)
        print("Dispositivos agregados.")

    def modificar_dispositivo(self, nombre_campus, nombre_dispositivo):
        if nombre_campus in self.campus:
            campus = self.campus[nombre_campus]
            for dispositivo in campus.dispositivos:
                if dispositivo.nombre == nombre_dispositivo:
                    dispositivo.modelo = input("Ingrese el nuevo modelo del dispositivo: ")
                    dispositivo.capa = self.seleccionar_capa()
                    dispositivo.interfaces = input("Ingrese las interfaces de red del dispositivo (separadas por coma): ").split(",")
                    dispositivo.ips_masks = self.ingresar_ips_masks(dispositivo.interfaces)
                    dispositivo.vlans = self.ingresar_vlans()
                    dispositivo.servicios = input("Ingrese los servicios de red configurados (separados por coma): ").split(",")
                    print("Dispositivo modificado.")
                    return
            print("El dispositivo especificado no existe en el campus.")
        else:
            print("El campus especificado no existe.")

    def borrar_dispositivo(self, nombre_campus, nombre_dispositivo):
        if nombre_campus in self.campus:
            campus = self.campus[nombre_campus]
            for dispositivo in campus.dispositivos:
                if dispositivo.nombre == nombre_dispositivo:
                    campus.dispositivos.remove(dispositivo)
                    print("Dispositivo eliminado.")
                    return
            print("El dispositivo especificado no existe en el campus.")
        else:
            print("El campus especificado no existe.")

    def seleccionar_capa(self):
        print("Seleccione la capa jerárquica a la que pertenece:")
        print("1) Núcleo")
        print("2) Distribución")
        print("3) Acceso")
        capa_opcion = input("Opción: ")
        return {"1": "Núcleo", "2": "Distribución", "3": "Acceso"}.get(capa_opcion, "Desconocida")

    def ingresar_ips_masks(self, interfaces):
        ips_masks = {}
        for interfaz in interfaces:
            while True:
                ip = input(f"Ingrese la dirección IP para la interfaz {interfaz}: ")
                mask = input(f"Ingrese la máscara de red para la interfaz {interfaz}: ")
                if self.es_direccion_ipv4(ip):
                    ips_masks[interfaz] = (ip, mask)
                    break
                else:
                    print("La dirección IP ingresada no es válida. Inténtelo nuevamente.")
        return ips_masks

    def ingresar_vlans(self):
        vlans = {}
        while True:
            nombre_vlan = input("Ingrese el nombre de la VLAN (o 'fin' para terminar): ")
            if nombre_vlan.lower() == 'fin':
                break
            numero_vlan = input("Ingrese el número de la VLAN: ")
            vlans[nombre_vlan] = numero_vlan
        return vlans

if __name__ == "__main__":
    nombre_archivo = input("Ingrese el nombre del archivo para cargar o crear la información: ")
    administrador = AdministradorRedes(nombre_archivo)
    administrador.menu_principal()
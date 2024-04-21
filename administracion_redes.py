import os

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
                archivo.write(f"{nombre}: {detalles}\n")
            archivo.write("\nDispositivos por Campus:\n")
            for nombre_campus, dispositivos_asociados in self.dispositivos_por_campus.items():
                archivo.write(f"{nombre_campus}:\n")
                for dispositivo in dispositivos_asociados:
                    archivo.write(f"- {dispositivo}\n")
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
            capa = input("Ingrese la capa jerárquica a la que pertenece (núcleo, distribución, acceso): ")
            interfaces = input("Ingrese las interfaces de red del dispositivo (separadas por coma): ").split(",")
            ips = input("Ingrese las IPs de las interfaces (separadas por coma): ").split(",")
            vlans = input("Ingrese las VLANs configuradas (separadas por coma): ").split(",")
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
                modelo = input("Ingrese el nuevo modelo del dispositivo: ")
                capa = input("Ingrese la nueva capa jerárquica a la que pertenece (núcleo, distribución, acceso): ")
                interfaces = input("Ingrese las nuevas interfaces de red del dispositivo (separadas por coma): ").split(",")
                ips = input("Ingrese las nuevas IPs de las interfaces (separadas por coma): ").split(",")
                vlans = input("Ingrese las nuevas VLANs configuradas (separadas por coma): ").split(",")
                servicios = input("Ingrese los nuevos servicios de red configurados (separados por coma): ").split(",")
                detalles = {
                    "Modelo": modelo,
                    "Capa": capa,
                    "Interfaces": interfaces,
                    "IPs": ips,
                    "VLANs": vlans,
                    "Servicios": servicios
                }
                self.dispositivos[nombre] = detalles
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

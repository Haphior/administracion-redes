import os

class AdministradorRedes:
    def __init__(self, nombre_archivo):
        self.secciones = {
            "campus": {},
            "dispositivos": {},
            "dispositivos_por_campus": {}
        }
        self.nombre_archivo = nombre_archivo
        if os.path.exists(nombre_archivo):
            self.cargar_desde_archivo()

    def cargar_desde_archivo(self):
        with open(self.nombre_archivo, "r") as archivo:
            seccion_actual = None
            for linea in archivo:
                linea = linea.strip()
                if linea in self.secciones:
                    seccion_actual = linea
                elif seccion_actual:
                    partes = linea.split(": ")
                    if len(partes) >= 2:
                        nombre, descripcion = partes[0], partes[1]
                        if seccion_actual == "dispositivos_por_campus":
                            self.secciones[seccion_actual].setdefault(nombre, []).append(descripcion)
                        else:
                            self.secciones[seccion_actual][nombre] = descripcion

    def guardar_en_archivo(self):
        with open(self.nombre_archivo, "w") as archivo:
            for seccion, contenido in self.secciones.items():
                archivo.write(f"{seccion}:\n")
                if seccion == "dispositivos_por_campus":
                    for nombre, elementos in contenido.items():
                        archivo.write(f"{nombre}:\n")
                        for elemento in elementos:
                            archivo.write(f"- {elemento}\n")
                else:
                    for nombre, descripcion in contenido.items():
                        archivo.write(f"{nombre}: {descripcion}\n")
        print("Archivo guardado con éxito.")

    def mostrar_menu(self, opciones):
        os.system("clear")
        print("¡Bienvenido al Administrador de Redes!")
        for idx, opcion in enumerate(opciones, start=1):
            print(f"{idx}. {opcion}")
        opcion = input("Seleccione una opción: ")
        return opcion

    def administrar_campus(self):
        while True:
            os.system("clear")
            print("Campus:")
            for nombre, descripcion in self.secciones["campus"].items():
                print(f"{nombre}: {descripcion}")
            print("\n1. Agregar campus")
            print("2. Volver al menú principal")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                nombre = input("Ingrese el nombre del campus: ")
                descripcion = input("Ingrese una descripción del campus: ")
                self.secciones["campus"][nombre] = descripcion
                self.secciones["dispositivos_por_campus"][nombre] = []
                input("Campus agregado. Presione Enter para continuar.")
            elif opcion == "2":
                break
            else:
                input("Opción no válida. Presione Enter para continuar.")

    def administrar_dispositivos(self):
        while True:
            os.system("clear")
            print("Dispositivos de Red:")
            for nombre, detalles in self.secciones["dispositivos"].items():
                print(f"{nombre}: {detalles}")
            print("\n1. Agregar dispositivo")
            print("2. Modificar dispositivo")
            print("3. Volver al menú principal")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                nombre = input("Ingrese el nombre del dispositivo: ")
                detalles = input("Ingrese los detalles del dispositivo: ")
                self.secciones["dispositivos"][nombre] = detalles
                input("Dispositivo agregado. Presione Enter para continuar.")
            elif opcion == "2":
                nombre = input("Ingrese el nombre del dispositivo que desea modificar: ")
                if nombre in self.secciones["dispositivos"]:
                    nuevos_detalles = input("Ingrese los nuevos detalles del dispositivo: ")
                    self.secciones["dispositivos"][nombre] = nuevos_detalles
                    input("Dispositivo modificado. Presione Enter para continuar.")
                else:
                    input("El dispositivo especificado no existe. Presione Enter para continuar.")
            elif opcion == "3":
                break
            else:
                input("Opción no válida. Presione Enter para continuar.")

    def ejecutar(self):
        while True:
            opcion = self.mostrar_menu(["Administrar campus", "Administrar dispositivos de red", "Guardar información en archivo de texto", "Salir"])
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

if __name__ == "__main__":
    nombre_archivo = input("Ingrese el nombre del archivo para cargar o crear la información: ")
    administrador = AdministradorRedes(nombre_archivo)
    administrador.ejecutar()

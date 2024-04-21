import os

class AdministradorRedes:
    def __init__(self, nombre_archivo):
        self.areas = {}
        self.zonas = {}
        self.zonas_por_area = {}
        self.dispositivos = {}
        self.dispositivos_por_zona = {}
        self.nombre_archivo = nombre_archivo

        if os.path.exists(nombre_archivo):
            self.cargar_desde_archivo()

    def cargar_desde_archivo(self):
        with open(self.nombre_archivo, "r") as archivo:
            seccion_actual = None
            for linea in archivo:
                linea = linea.strip()
                if linea == "Áreas de Red:":
                    seccion_actual = "areas"
                elif linea == "Zonas:":
                    seccion_actual = "zonas"
                elif linea == "Zonas por Área:":
                    seccion_actual = "zonas_por_area"
                elif linea == "Dispositivos de Red:":
                    seccion_actual = "dispositivos"
                elif linea == "Dispositivos por Zona:":
                    seccion_actual = "dispositivos_por_zona"
                elif seccion_actual == "areas" or seccion_actual == "zonas" or seccion_actual == "dispositivos":
                    partes = linea.split(": ")
                    if len(partes) >= 2:
                        nombre, descripcion = partes[0], partes[1]
                        if seccion_actual == "areas":
                            self.areas[nombre] = descripcion
                        elif seccion_actual == "zonas":
                            self.zonas[nombre] = descripcion
                        elif seccion_actual == "dispositivos":
                            self.dispositivos[nombre] = descripcion


    def menu_principal(self):
        os.system("clear")
        print("¡Bienvenido al Administrador de Redes!")
        print("1. Administrar áreas de red")
        print("2. Administrar zonas")
        print("3. Administrar dispositivos de red")
        print("4. Asociar")
        print("5. Guardar información en archivo de texto")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            self.administrar_areas()
        elif opcion == "2":
            self.administrar_zonas()
        elif opcion == "3":
            self.administrar_dispositivos()
        elif opcion == "4":
            self.asociar()
        elif opcion == "5":
            self.guardar_en_archivo()
        elif opcion == "6":
            print("¡Hasta luego!")
            exit()
        else:
            input("Opción no válida. Presione Enter para continuar.")
            self.menu_principal()


    def administrar_areas(self):
        os.system("clear")
        print("Áreas de Red:")
        for nombre, descripcion in self.areas.items():
            print(f"{nombre}: {descripcion}")
        opcion = input("Seleccione una opción:\n1. Agregar área\n2. Modificar área\n3. Volver al menú principal\n")
        if opcion == "1":
            nombre = input("Ingrese el nombre del área: ")
            descripcion = input("Ingrese una descripción del área: ")
            self.areas[nombre] = descripcion
            self.zonas_por_area[nombre] = []
            input("Área agregada. Presione Enter para continuar.")
            self.administrar_areas()
        elif opcion == "2":
            nombre = input("Ingrese el nombre del área que desea modificar: ")
            if nombre in self.areas:
                nueva_descripcion = input("Ingrese la nueva descripción del área: ")
                self.areas[nombre] = nueva_descripcion
                input("Área modificada. Presione Enter para continuar.")
            else:
                input("El área especificada no existe. Presione Enter para continuar.")
            self.administrar_areas()
        elif opcion == "3":
            self.menu_principal()
        else:
            input("Opción no válida. Presione Enter para continuar.")
            self.administrar_areas()

    def administrar_zonas(self):
        os.system("clear")
        print("Zonas:")
        for nombre, descripcion in self.zonas.items():
            print(f"{nombre}: {descripcion}")
        opcion = input("Seleccione una opción:\n1. Agregar zona\n2. Modificar zona\n3. Volver al menú principal\n")
        if opcion == "1":
            nombre = input("Ingrese el nombre de la zona: ")
            descripcion = input("Ingrese una descripción de la zona: ")
            self.zonas[nombre] = descripcion
            self.dispositivos_por_zona[nombre] = []
            input("Zona agregada. Presione Enter para continuar.")
            self.administrar_zonas()
        elif opcion == "2":
            nombre = input("Ingrese el nombre de la zona que desea modificar: ")
            if nombre in self.zonas:
                nueva_descripcion = input("Ingrese la nueva descripción de la zona: ")
                self.zonas[nombre] = nueva_descripcion
                input("Zona modificada. Presione Enter para continuar.")
            else:
                input("La zona especificada no existe. Presione Enter para continuar.")
            self.administrar_zonas()
        elif opcion == "3":
            self.menu_principal()
        else:
            input("Opción no válida. Presione Enter para continuar.")
            self.administrar_zonas()

    def asociar(self):
        os.system("clear")
        print("Asociar:")
        print("1. Asociar zona a área")
        print("2. Asociar dispositivo a zona")
        print("3. Volver al menú principal")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            self.asociar_zonas_areas()
        elif opcion == "2":
            self.asociar_dispositivo_zona()
        elif opcion == "3":
            self.menu_principal()
        else:
            input("Opción no válida. Presione Enter para continuar.")
            self.asociar()

    def asociar_zonas_areas(self):
        os.system("clear")
        print("Asociar Zonas a Áreas:")
        print("Áreas de Red:")
        for nombre, descripcion in self.areas.items():
            print(f"{nombre}: {descripcion}")
        print("\nZonas:")
        for nombre, descripcion in self.zonas.items():
            print(f"{nombre}: {descripcion}")
        opcion = input("Seleccione una opción:\n1. Asociar zona a área\n2. Volver al menú principal\n")
        if opcion == "1":
            nombre_area = input("Ingrese el nombre del área: ")
            nombre_zona = input("Ingrese el nombre de la zona: ")
            if nombre_area in self.areas and nombre_zona in self.zonas:
                self.zonas_por_area[nombre_area].append(nombre_zona)
                input("Zona asociada al área. Presione Enter para continuar.")
            else:
                input("El área o la zona especificada no existe. Presione Enter para continuar.")
            self.asociar_zonas_areas()
        elif opcion == "2":
            self.menu_principal()
        else:
            input("Opción no válida. Presione Enter para continuar.")
            self.asociar_zonas_areas()

    def asociar_dispositivo_zona(self):
        os.system("clear")
        print("Asociar Dispositivo a Zona:")
        print("Dispositivos de Red:")
        for nombre, detalles in self.dispositivos.items():
            print(f"{nombre}: {detalles}")
        print("\nZonas:")
        for nombre, descripcion in self.zonas.items():
            print(f"{nombre}: {descripcion}")
        opcion = input("Seleccione una opción:\n1. Asociar dispositivo a zona\n2. Volver al menú principal\n")
        if opcion == "1":
            nombre_dispositivo = input("Ingrese el nombre del dispositivo: ")
            nombre_zona = input("Ingrese el nombre de la zona: ")
            if nombre_dispositivo in self.dispositivos and nombre_zona in self.zonas:
                self.dispositivos_por_zona[nombre_zona].append(nombre_dispositivo)
                input("Dispositivo asociado a la zona. Presione Enter para continuar.")
            else:
                input("El dispositivo o la zona especificada no existe. Presione Enter para continuar.")
            self.asociar_dispositivo_zona()
        elif opcion == "2":
            self.menu_principal()
        else:
            input("Opción no válida. Presione Enter para continuar.")
            self.asociar_dispositivo_zona()

    def administrar_dispositivos(self):
        os.system("clear")
        print("Dispositivos de Red:")
        for nombre, detalles in self.dispositivos.items():
            print(f"{nombre}: {detalles}")
        opcion = input("Seleccione una opción:\n1. Agregar dispositivo\n2. Modificar dispositivo\n3. Volver al menú principal\n")
        if opcion == "1":
            nombre = input("Ingrese el nombre del dispositivo: ")
            detalles = input("Ingrese los detalles del dispositivo: ")
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

    def guardar_en_archivo(self):
        with open(self.nombre_archivo, "w") as archivo:
            archivo.write("Áreas de Red:\n")
            for nombre, descripcion in self.areas.items():
                archivo.write(f"{nombre}: {descripcion}\n")
            archivo.write("\nZonas:\n")
            for nombre, descripcion in self.zonas.items():
                archivo.write(f"{nombre}: {descripcion}\n")
            archivo.write("\nZonas por Área:\n")
            for nombre_area, zonas_asociadas in self.zonas_por_area.items():
                archivo.write(f"{nombre_area}:\n")
                for zona in zonas_asociadas:
                    archivo.write(f"- {zona}\n")
            archivo.write("\nDispositivos de Red:\n")
            for nombre, detalles in self.dispositivos.items():
                archivo.write(f"{nombre}: {detalles}\n")
            archivo.write("\nDispositivos por Zona:\n")
            for nombre_zona, dispositivos_asociados in self.dispositivos_por_zona.items():
                archivo.write(f"{nombre_zona}:\n")
                for dispositivo in dispositivos_asociados:
                    archivo.write(f"- {dispositivo}\n")
        print("Archivo guardado con éxito.")

    def ejecutar(self):
        self.nombre_archivo = input("Ingrese el nombre del archivo para guardar o crear la información: ")
        while True:
            self.menu_principal()

if __name__ == "__main__":
    nombre_archivo = input("Ingrese el nombre del archivo para cargar o crear la información: ")
    administrador = AdministradorRedes(nombre_archivo)
    administrador.menu_principal()
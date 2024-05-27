import os
import json
from models import Campus, Dispositivo

class AdministradorRedes:
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo
        self.campus = {}
        if os.path.exists(nombre_archivo):
            self.cargar_desde_archivo()

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
            datos[nombre] = []
            for dispositivo in campus.dispositivos:
                datos[nombre].append(dispositivo.__dict__)

        with open(self.nombre_archivo, "w") as archivo:
            json.dump(datos, archivo, indent=4)

    def convertir_a_formato_texto(self):
        texto_formato = ""
        for nombre, campus in self.campus.items():
            texto_formato += f"Campus: {nombre}\nDescripción: {campus.descripcion}\n"
            for dispositivo in campus.dispositivos:
                texto_formato += f"\nDispositivo: {dispositivo.nombre}\n"
                texto_formato += f"Modelo: {dispositivo.modelo}\n"
                texto_formato += f"Capa: {dispositivo.capa}\n"
                texto_formato += "Interfaces:\n"
                for interface in dispositivo.interfaces:
                    ip, mask = dispositivo.ips_masks.get(interface, ("", ""))
                    texto_formato += f"- {interface}: IP: {ip}, Máscara: {mask}\n"
                texto_formato += "VLANs:\n"
                for vlan, numero in dispositivo.vlans.items():
                    texto_formato += f"- {vlan}: {numero}\n"
                texto_formato += f"Servicios: {', '.join(dispositivo.servicios)}\n"
                texto_formato += "-" * 30 + "\n"
        return texto_formato

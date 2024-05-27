from flask import Flask, request, jsonify
from admin import AdministradorRedes

app = Flask(__name__)

# Inicializa el administrador de redes
nombre_archivo = "redes.json"
admin_redes = AdministradorRedes(nombre_archivo)

@app.route('/campus', methods=['GET'])
def obtener_campus():
    campus = []
    for nombre, campus_obj in admin_redes.campus.items():
        campus.append({"nombre": nombre, "descripcion": campus_obj.descripcion})
    return jsonify(campus)

@app.route('/campus', methods=['POST'])
def agregar_campus():
    datos = request.json
    nombre = datos.get("nombre")
    descripcion = datos.get("descripcion")
    admin_redes.campus[nombre] = Campus(nombre, descripcion)
    admin_redes.guardar_en_archivo()
    return jsonify({"mensaje": "Campus agregado"}), 201

@app.route('/dispositivos', methods=['POST'])
def agregar_dispositivo():
    datos = request.json
    nombre_campus = datos.get("nombre_campus")
    dispositivo_info = datos.get("dispositivo")
    dispositivo = Dispositivo(**dispositivo_info)
    if nombre_campus in admin_redes.campus:
        admin_redes.campus[nombre_campus].dispositivos.append(dispositivo)
        admin_redes.guardar_en_archivo()
        return jsonify({"mensaje": "Dispositivo agregado"}), 201
    else:
        return jsonify({"error": "Campus no encontrado"}), 404

@app.route('/guardar_texto', methods=['POST'])
def guardar_texto():
    archivo_texto = request.json.get("archivo_texto")
    texto_formato = admin_redes.convertir_a_formato_texto()
    with open(archivo_texto, "w") as archivo:
        archivo.write(texto_formato)
    return jsonify({"mensaje": f"Datos convertidos y guardados en el archivo: {archivo_texto}"}), 201

if __name__ == "__main__":
    app.run(debug=True)

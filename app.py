from flask import Flask, request, jsonify, send_from_directory, render_template
from lexer import analizar_lexico
from parser import analizar_sintactico
from turing import maquina_turing
import os
import time as import_time

app = Flask(__name__, static_folder='templates', static_url_path='/templates')

# Ruta para servir archivos estáticos desde templates
@app.route('/templates/<path:path>')
def send_template(path):
    return send_from_directory('templates', path)

# Ruta específica para servir imágenes
@app.route('/templates/imagenes/<path:filename>')
def serve_image(filename):
    return send_from_directory('templates/imagenes', filename)

# Ruta para servir el HTML
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para análisis léxico
@app.route('/analizar-lexico', methods=['POST'])
def lexico():
    try:
        data = request.get_json()
        if not data or 'code' not in data:
            return jsonify({
                'resultado': 'Error: No se proporcionó código para analizar',
                'status': 'error'
            }), 400
        
        code = data['code']
        if not code.strip():
            return jsonify({
                'resultado': 'Error: El código está vacío',
                'status': 'error'
            }), 400

        resultado = analizar_lexico(code)
        status = 'error' if 'Error' in resultado else 'success'
        
        return jsonify({
            'resultado': resultado,
            'status': status,
            'timestamp': import_time.strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        return jsonify({
            'resultado': f'Error en el análisis léxico: {str(e)}',
            'status': 'error'
        }), 500

# Ruta para análisis sintáctico
@app.route('/analizar-sintactico', methods=['POST'])
def sintactico():
    try:
        data = request.get_json()
        if not data or 'code' not in data:
            return jsonify({
                'resultado': 'Error: No se proporcionó código para analizar',
                'status': 'error'
            }), 400
        
        code = data['code']
        if not code.strip():
            return jsonify({
                'resultado': 'Error: El código está vacío',
                'status': 'error'
            }), 400

        resultado = analizar_sintactico(code)
        status = 'error' if 'Error' in resultado else 'success'
        
        return jsonify({
            'resultado': resultado,
            'status': status,
            'timestamp': import_time.strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        return jsonify({
            'resultado': f'Error en el análisis sintáctico: {str(e)}',
            'status': 'error'
        }), 500

# Ruta para ejecutar máquina de Turing
@app.route('/turing', methods=['POST'])
def turing():
    try:
        data = request.get_json()
        print("Datos recibidos:", data)  # Debug log
        
        if not data or 'code' not in data:
            return jsonify({
                'resultado': 'Error: No se proporcionó código para analizar',
                'status': 'error'
            }), 400
        
        code = data['code']
        print("Código a procesar:", code)  # Debug log
        
        if not code.strip():
            return jsonify({
                'resultado': 'Error: El código está vacío',
                'status': 'error'
            }), 400

        resultado = maquina_turing(code)
        print("Resultado de la máquina:", resultado)  # Debug log
        status = 'error' if 'Error' in resultado else 'success'
        
        response_data = {
            'resultado': resultado,
            'status': status,
            'timestamp': import_time.strftime('%Y-%m-%d %H:%M:%S')
        }
        print("Respuesta a enviar:", response_data)  # Debug log
        
        return jsonify(response_data)
    except Exception as e:
        return jsonify({
            'resultado': f'Error en la máquina de Turing: {str(e)}',
            'status': 'error'
        }), 500

if __name__ == '__main__':
    print("\n=== Servidor iniciado ===")
    print("URL del servidor: http://127.0.0.1:5000")
    print("=====================\n")
    app.run(debug=False, host='127.0.0.1', port=5000)
from flask import Flask, request, jsonify, send_from_directory, render_template
from lexer import analizar_lexico
from parser import Parser
from turing import maquina_turing
import os
import time as import_time

app = Flask(__name__)

# Configurar la carpeta de templates y archivos estáticos
app.template_folder = 'templates'
app.static_folder = 'static'
app.static_url_path = '/static'

parser = Parser()  # Crear una instancia del analizador sintáctico

# Ruta para servir el HTML
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para análisis léxico
@app.route('/analizar-lexico', methods=['POST'])
def lexico():
    try:
        data = request.get_json()
        if not data or 'codigo' not in data:
            return jsonify({
                'error': 'No se proporcionó código para analizar',
                'resultados': [],
                'exitoso': False,
                'mensaje': 'Error: No se proporcionó código para analizar',
                'timestamp': import_time.strftime('%d/%m/%Y, %I:%M:%S %p'),
                'linea': 'undefined',
                'posicion': 'undefined',
                'numero': 'undefined',
                'total_tokens': 0,
                'tokens_validos': 0,
                'tokens_error': 0,
                'lineas_analizadas': 'NaN'
            }), 400
        
        codigo = data['codigo']
        if not codigo.strip():
            return jsonify({
                'error': 'El código está vacío',
                'resultados': [],
                'exitoso': False,
                'mensaje': 'Error: El código está vacío',
                'timestamp': import_time.strftime('%d/%m/%Y, %I:%M:%S %p'),
                'linea': 'undefined',
                'posicion': 'undefined',
                'numero': 'undefined',
                'total_tokens': 1,
                'tokens_validos': 0,
                'tokens_error': 1,
                'lineas_analizadas': 'NaN'
            }), 400

        # Analizar el código
        resultado = analizar_lexico(codigo)
        
        return jsonify({
            'error': None,
            'resultados': resultado['tokens'],
            'exitoso': resultado['tokens_error'] == 0,
            'mensaje': 'Análisis léxico completado correctamente',
            'timestamp': import_time.strftime('%d/%m/%Y, %I:%M:%S %p'),
            'linea': resultado['linea'],
            'posicion': resultado['posicion'],
            'numero': resultado['numero'],
            'total_tokens': resultado['total_tokens'],
            'tokens_validos': resultado['tokens_validos'],
            'tokens_error': resultado['tokens_error'],
            'lineas_analizadas': resultado['lineas_analizadas']
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'resultados': [],
            'exitoso': False,
            'mensaje': f'Error en el análisis léxico: {str(e)}',
            'timestamp': import_time.strftime('%d/%m/%Y, %I:%M:%S %p'),
            'linea': 'undefined',
            'posicion': 'undefined',
            'numero': 'undefined',
            'total_tokens': 0,
            'tokens_validos': 0,
            'tokens_error': 0,
            'lineas_analizadas': 'NaN'
        }), 500

# Ruta para análisis sintáctico
@app.route('/analizar-sintactico', methods=['POST'])
def sintactico():
    try:
        data = request.get_json()
        if not data or 'codigo' not in data:
            return jsonify({
                'error': 'No se proporcionó código para analizar',
                'errores': [],
                'exitoso': False,
                'mensaje': 'Error: No se proporcionó código para analizar',
                'lineas_analizadas': 0,
                'lineas_validas': 0,
                'lineas_error': 0,
                'timestamp': import_time.strftime('%Y-%m-%d %H:%M:%S')
            }), 400
        
        codigo = data['codigo']
        if not codigo.strip():
            return jsonify({
                'error': 'El código está vacío',
                'errores': [],
                'exitoso': False,
                'mensaje': 'Error: El código está vacío',
                'lineas_analizadas': 0,
                'lineas_validas': 0,
                'lineas_error': 0,
                'timestamp': import_time.strftime('%Y-%m-%d %H:%M:%S')
            }), 400

        resultado = parser.parse(codigo)
        
        return jsonify({
            'error': None,
            'errores': resultado['errores'],
            'exitoso': resultado['exitoso'],
            'mensaje': resultado['mensaje'],
            'lineas_analizadas': resultado['lineas_analizadas'],
            'lineas_validas': resultado['lineas_validas'],
            'lineas_error': resultado['lineas_error'],
            'timestamp': import_time.strftime('%Y-%m-%d %H:%M:%S')
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'errores': [],
            'exitoso': False,
            'mensaje': f'Error en el análisis sintáctico: {str(e)}',
            'lineas_analizadas': 0,
            'lineas_validas': 0,
            'lineas_error': 0,
            'timestamp': import_time.strftime('%Y-%m-%d %H:%M:%S')
        }), 500

# Ruta para ejecutar máquina de Turing
@app.route('/turing', methods=['POST'])
def turing():
    try:
        data = request.get_json()
        if not data or 'codigo' not in data:
            return jsonify({
                'error': 'No se proporcionó código para analizar',
                'resultado': '',
                'exitoso': False,
                'mensaje': 'Error: No se proporcionó código para analizar'
            }), 400
        
        codigo = data['codigo']
        if not codigo.strip():
            return jsonify({
                'error': 'El código está vacío',
                'resultado': '',
                'exitoso': False,
                'mensaje': 'Error: El código está vacío'
            }), 400

        resultado = maquina_turing(codigo)
        
        # Determinar si fue exitoso basado en el contenido del resultado
        exitoso = "Rechazada" not in resultado and "Error" not in resultado
        mensaje = "Cadena aceptada" if exitoso else "Cadena rechazada"
        
        return jsonify({
            'error': None,
            'resultado': resultado,
            'exitoso': exitoso,
            'mensaje': mensaje
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'resultado': '',
            'exitoso': False,
            'mensaje': f'Error en la máquina de Turing: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
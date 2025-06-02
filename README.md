# IDE RICH

IDE web que incluye un analizador léxico, sintáctico y una máquina de Turing.

## 👨‍🎓 Datos del Estudiante

<img src="static/imagenes/icon.jpg" alt="Datos del Estudiante" width="200" height="250" style="display: block; margin: auto;">

- **Nombre:** Richard De Jesus Espinoza Francisco
- **Materia:** Lenguajes Automatas I
- **Profesor:** Kevin David Molina Gomez
- **Institución:** Tecnologico Nacional De Mexico Campus Minititlán

## 📋 Descripción del Proyecto
Este proyecto implementa tres componentes principales:
1. Un analizador léxico que identifica y clasifica los tokens del código
2. Un analizador sintáctico que verifica la estructura gramatical
3. Una máquina de Turing especializada en detectar patrones en cadenas binarias

## 🛠️ Tecnologías y Lenguajes Utilizados

### Backend (Python)
- **Flask**: Framework web para Python
- **PLY**: Herramienta para análisis léxico y sintáctico
- **Python**: Lenguaje principal del backend

### Frontend
- **HTML5**: Estructura de la interfaz web
- **CSS**: Estilos y diseño responsivo
- **JavaScript**: Interactividad en el frontend

### Estructura del Proyecto
```
IDE_RICH/
├── app.py              # Servidor Flask y rutas principales
├── lexer.py           # Implementación del analizador léxico
├── parser.py          # Implementación del analizador sintáctico
├── turing.py          # Implementación de la máquina de Turing
├── requirements.txt    # Dependencias del proyecto
├── templates/         # Plantillas HTML
│   └── index.html     # Página principal
├── static/           # Archivos estáticos
│   ├── estilo.css     # Estilos CSS
│   ├── logica.js      # Lógica del frontend
│   └── imagenes/      # Imágenes del proyecto
└── README.md         # Documentación
```

## ⚙️ Requisitos e Instalación

### Dependencias
```bash
Flask==3.0.2
Werkzeug==3.0.1
ply==3.11
pytest==8.0.0
python-dotenv==1.0.1
Flask-Cors==4.0.0
gunicorn==21.2.0
Flask-Session==0.6.0
Jinja2>=3.0.0
MarkupSafe>=2.0.0
itsdangerous>=2.0.0
click>=8.0.0
```

### Instalación y Ejecución
1. Clona el repositorio:
```bash
git clone [url-del-repositorio]
cd IDE_RICH
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecuta el servidor:
```bash
python app.py
```

4. Abre tu navegador y visita:
```
http://127.0.0.1:5000
```

## 🔍 Componentes Principales

### 1. Analizador Léxico (`lexer.py`)
- Reconoce los siguientes tipos de tokens:
  - Palabras clave (if, else, while, for, return, def, class, etc.)
  - Símbolos y operadores (+, -, *, /, =, ==, !=, etc.)
  - Números (enteros y decimales)
  - Identificadores (variables y nombres de funciones)
- Características principales:
  - Análisis línea por línea del código
  - Detección de caracteres inválidos (~, @, $, %, #, ¡, ¿)
  - Validación de identificadores (deben comenzar con letra o _)
  - Manejo de operadores compuestos (+=, -=, *=, /=)
- Información detallada de cada token:
  - Número de línea y posición
  - Tipo y valor del token
  - Validez del token
- Estadísticas del análisis:
  - Total de tokens y líneas analizadas
  - Tokens válidos e inválidos
  - Mensajes de error descriptivos
    
#### Visualización del RICH_IDE
<img src="static/imagenes/Icon 1.png" alt="Aplicación WEB" width="1000" height="500" style="display: block; margin: auto;">
<img src="static/imagenes/Icon 2.png" alt="Aplicación WEB 2" width="1000" height="500" style="display: block; margin: auto;">


#### Ejemplo de Análisis Léxico
<img src="static/imagenes/Img_lex.png" alt="Análisis Léxico" width="1000" height="500" style="display: block; margin: auto;">

<img src="static/imagenes/Img_lex_2.png" alt="Análisis Léxico" width="1000" height="500" style="display: block; margin: auto;">

*Ejemplo de análisis léxico mostrando la identificación de tokens y sus propiedades*

### 2. Analizador Sintáctico (`parser.py`)
- Análisis de estructura del código:
  - Validación de asignaciones (formato "identificador = valor")
  - Verificación de punto y coma al final de las instrucciones
  - Control de estructuras no permitidas
- Manejo de errores:
  - Detección de símbolos desbalanceados
  - Validación de puntos y comas faltantes
  - Errores en asignaciones
  - Identificadores inválidos
- Estadísticas y resultados:
  - Total de líneas analizadas
  - Líneas válidas e inválidas
  - Lista detallada de errores

#### Ejemplo de Análisis Sintáctico
<img src="static/imagenes/Img_sin.png" alt="Análisis Sintáctico" width="1000" height="500" style="display: block; margin: auto;">

<img src="static/imagenes/Img_sin_2.png" alt="Análisis Léxico" width="1000" height="500" style="display: block; margin: auto;">

*Ejemplo de análisis sintáctico mostrando la validación de una asignación simple*

### 3. Máquina de Turing (`turing.py`)
- Análisis de cadenas binarias:
  - Validación de entrada (solo 0s y 1s)
  - Verificación de cadena no vacía
  - Comprobación de al menos un 0 y un 1
- Características técnicas:
  - Estados definidos (q0, qf)
  - Transiciones configurables
  - Control de posición del cabezal
  - Cinta de símbolos
- Visualización y resultados:
  - Representación gráfica de la cinta
  - Estado inicial y final
  - Conteo de 0s y 1s
  - Emojis para indicar estados (✅, ❌)

#### Ejemplo de Máquina de Turing
<img src="static/imagenes/Img_tur.png" alt="Máquina de Turing" width="1000" height="500" style="display: block; margin: auto;">

<img src="static/imagenes/Img_tur_2.png" alt="Análisis Léxico" width="1000" height="500" style="display: block; margin: auto;">

*Ejemplo de procesamiento de una cadena binaria mostrando el análisis y resultado*

## 📝 Ejemplos de Uso

### Análisis de Código
```python
# Código Válido
x = 42
variable_nombre = 100
resultado = 5

# Código Inválido
if x = 5          # Error: estructura de control no permitida
variable  = 10;   # Error: punto y coma no necesario
resultado: = 20   # Error: dos puntos no permitidos
= 30              # Error: falta identificador
x = = 40          # Error: operador duplicado
```

### Análisis de Cadenas Binarias
```
Entrada: 1001     ✅ Válida: contiene 0s y 1s
Entrada: 111      ❌ Inválida: falta 0
Entrada: abc      ❌ Inválida: caracteres no permitidos
```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

---

⌨️ con ❤️ por Richard De Jesus 

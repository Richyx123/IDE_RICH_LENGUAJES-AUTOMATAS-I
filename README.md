# IDE RICH

IDE web que incluye un analizador léxico, sintáctico y una máquina de Turing.

## 👨‍🎓 Datos del Estudiante
![Datos del Estudiante](templates/imagenes/icon.jpg)

- **Nombre:** Richard De Jesus Espinoza Francisco
- **Materia:** Lenguajes Automatas I
- **Profesor:** Kevin David Molina Gomez
- **Institución:** Tecnologico Nacional De Mexico Campus Minititlán

- ## Características

- Analizador léxico para tokens
- Analizador sintáctico
- Máquina de Turing para cadenas binarias
- Interfaz web moderna y responsive

## Requisitos

- Python 3.x
- Flask 3.0.2
- Werkzeug 3.0.1
- ply 3.11
- pytest 8.0.0

## Instalación

1. Clona este repositorio:
```bash
git clone [url-del-repositorio]
cd IDE_RICH
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

1. Ejecuta el servidor:
```bash
python app.py
```

2. Abre tu navegador y visita:
```
http://127.0.0.1:5000
```

## Estructura del Proyecto

```
IDE_RICH/
├── app.py              # Servidor Flask y rutas principales
├── lexer.py           # Implementación del analizador léxico
├── parser.py          # Implementación del analizador sintáctico
├── turing.py          # Implementación de la máquina de Turing
├── requirements.txt    # Dependencias del proyecto
├── templates/         # Plantillas y archivos estáticos
│   ├── index.html     # Página principal
│   ├── estilo.css     # Estilos CSS
│   ├── logica.js      # Lógica del frontend
│   └── imagenes/      # Imágenes del proyecto
└── README.md         # Documentación
```

## Funcionalidades

### Analizador Léxico (`lexer.py`)
- Identifica y clasifica tokens en el código
- Reconoce palabras clave, identificadores, números y símbolos
- Muestra resultados detallados del análisis
- Manejo de errores léxicos

### Analizador Sintáctico (`parser.py`)
- Analiza la estructura del código
- Verifica la gramática del lenguaje
- Reporta errores de sintaxis
- Genera árbol de análisis sintáctico

### Máquina de Turing (`turing.py`)
- Procesa cadenas binarias (0s y 1s)
- Muestra el proceso paso a paso
- Validación de entrada
- Visualización del estado de la cinta

## ⚠️ Manejo de Errores

- Validación de entrada en tiempo real
- Mensajes de error descriptivos
- Resaltado de errores en el código
- Manejo de excepciones en el servidor

## 📝 Notas Adicionales

- La aplicación corre en modo no debug por seguridad
- Los archivos estáticos se sirven desde el directorio templates
- Soporte para diferentes tipos de análisis
- Interfaz moderna con diseño responsive

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

---

Realizado con dedicación por Richard De Jesus 

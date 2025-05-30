// Objeto para manejar las operaciones del IDE
const IDE = {
    // Elementos del DOM
    elements: {
        codeInput: document.getElementById('codigo'),
        resultOutput: document.getElementById('resultado'),
        buttons: {
            lexico: document.getElementById('btn-lexico'),
            sintactico: document.getElementById('btn-sintactico'),
            turing: document.getElementById('btn-turing')
        }
    },

    // Configuración del analizador
    config: {
        palabras_clave: new Set([
            'if', 'else', 'while', 'for', 'return', 'def', 'class',
            'import', 'from', 'as', 'try', 'except', 'finally',
            'with', 'is', 'in', 'and', 'or', 'not', 'True', 'False', 'None'
        ]),
        simbolos: new Set([
            '(', ')', '{', '}', '[', ']', ';', '+', '-', '*', '/',
            '=', '<', '>', '!', ':', ',', '.', '+=', '-=', '*=', '/=',
            '==', '!=', '<=', '>=', '&&', '||'
        ]),
        caracteres_invalidos: new Set(['~', '@', '$', '%', '#', '¡', '¿'])
    },

    // Estado del IDE
    state: {
        isAnalyzing: false,
        lastAnalysis: null,
        analysisHistory: []
    },

    // Editor CodeMirror
    editor: null,

    // Inicializar la aplicación
    init() {
        if (!this.elements.codeInput) {
            console.error('No se encontró el elemento del editor');
            return;
        }
        
        this.setupCodeMirror();
        this.bindEvents();
        this.setupAutoSave();
        
        console.log('IDE inicializado correctamente');
    },

    // Configurar CodeMirror
    setupCodeMirror() {
        try {
            this.editor = CodeMirror.fromTextArea(this.elements.codeInput, {
                mode: 'python',
                theme: 'monokai',
                lineNumbers: true,
                matchBrackets: true,
                autoCloseBrackets: true,
                indentUnit: 4,
                tabSize: 4,
                indentWithTabs: false,
                lineWrapping: true,
                gutters: ["CodeMirror-lint-markers"],
                lint: true,
                extraKeys: {
                    "Ctrl-Space": "autocomplete",
                    "Ctrl-/": "toggleComment",
                    "Ctrl-S": () => this.saveToLocalStorage()
                }
            });

            // Validación en tiempo real
            this.editor.on('change', () => {
                this.validateInRealTime();
                this.saveToLocalStorage();
            });

            console.log('Editor CodeMirror configurado correctamente');
        } catch (error) {
            console.error('Error al configurar CodeMirror:', error);
        }
    },

    // Configurar auto-guardado
    setupAutoSave() {
        // Cargar código guardado
        const savedCode = localStorage.getItem('editorCode');
        if (savedCode) {
            this.editor.setValue(savedCode);
        }

        // Auto-guardar cada 30 segundos
        setInterval(() => this.saveToLocalStorage(), 30000);
    },

    // Guardar en localStorage
    saveToLocalStorage() {
        const code = this.editor.getValue();
        localStorage.setItem('editorCode', code);
        this.showTemporaryMessage('Código guardado', 'success');
    },

    // Mostrar mensaje temporal
    showTemporaryMessage(message, type = 'info') {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.textContent = message;
        document.querySelector('.editor-section').appendChild(messageDiv);

        setTimeout(() => messageDiv.remove(), 3000);
    },

    // Validar código en tiempo real
    validateInRealTime() {
        const code = this.editor.getValue();
        
        this.editor.operation(() => {
            // Limpiar marcadores existentes
            this.editor.getAllMarks().forEach(mark => mark.clear());

            // Detectar si es una entrada para la máquina de Turing - versión mejorada
            // Primero verificamos si el código solo contiene 0s, 1s y espacios en blanco
            const isValidTuringFormat = /^[01\s\n\r]*$/.test(code);
            const cleanCode = code.replace(/[\s\n\r]+/g, '');
            const isTuringInput = cleanCode.length > 0 && /^[01]+$/.test(cleanCode);

            if (isValidTuringFormat && isTuringInput) {
                // Si es entrada de la máquina de Turing válida, no aplicar validaciones normales
                return;
            }

            // Solo continuar con la validación normal si no es una entrada de Turing
            const lines = code.split('\n');
            lines.forEach((line, i) => {
                // Validar caracteres inválidos
                for (let j = 0; j < line.length; j++) {
                    if (this.config.caracteres_invalidos.has(line[j])) {
                        this.markError(i, j, j + 1, `Carácter inválido: ${line[j]}`);
                    }
                }

                // Validar palabras clave y símbolos
                const tokens = line.split(/\s+/);
                let pos = 0;
                tokens.forEach(token => {
                    if (token) {
                        if (this.config.palabras_clave.has(token)) {
                            this.markToken(i, line.indexOf(token, pos), token.length, 'keyword');
                        } else if (this.config.simbolos.has(token)) {
                            this.markToken(i, line.indexOf(token, pos), token.length, 'symbol');
                        }
                        pos = line.indexOf(token, pos) + token.length;
                    }
                });

                // Validar estructura básica
                this.validateStructure(line, i);
            });
        });
    },

    // Marcar error en el editor
    markError(line, from, to, message) {
        this.editor.markText(
            {line: line, ch: from},
            {line: line, ch: to},
            {
                className: 'cm-error',
                title: message
            }
        );
    },

    // Marcar token en el editor
    markToken(line, from, length, type) {
        this.editor.markText(
            {line: line, ch: from},
            {line: line, ch: from + length},
            {
                className: `cm-${type}`,
                title: `${type}: ${this.editor.getRange(
                    {line: line, ch: from},
                    {line: line, ch: from + length}
                )}`
            }
        );
    },

    // Validar estructura del código
    validateStructure(line, lineNum) {
        // Validar paréntesis y llaves
        const stack = [];
        const brackets = {'(': ')', '{': '}', '[': ']'};
        
        for (let i = 0; i < line.length; i++) {
            const char = line[i];
            if ('({['.includes(char)) {
                stack.push(char);
            } else if (')}]'.includes(char)) {
                if (stack.length === 0 || brackets[stack.pop()] !== char) {
                    this.markError(lineNum, i, i + 1, "Paréntesis/llave no coincidente");
                }
            }
        }

        if (stack.length > 0) {
            this.markError(lineNum, line.length - 1, line.length, "Paréntesis/llave sin cerrar");
        }

        // Validar estructura de control
        if (line.trim().startsWith('if') && !line.trim().endsWith(':')) {
            this.markError(lineNum, 0, line.length, "Se espera ':' al final de la condición");
        }
    },

    // Vincular eventos
    bindEvents() {
        try {
            // Vincular eventos de los botones
            Object.entries(this.elements.buttons).forEach(([tipo, btn]) => {
                if (btn) {
                    const action = btn.dataset.action;
                    btn.addEventListener('click', () => {
                        console.log(`Ejecutando acción: ${action}`);
                        this.analizar(action);
                    });
                }
            });

            // Agregar atajos de teclado
            document.addEventListener('keydown', (e) => {
                if (e.ctrlKey && e.key === 'Enter') {
                    if (this.state.lastAnalysis) {
                        this.analizar(this.state.lastAnalysis);
                    }
                }
            });

            console.log('Eventos vinculados correctamente');
        } catch (error) {
            console.error('Error al vincular eventos:', error);
        }
    },

    // Mostrar resultados
    mostrarResultado(data) {
        console.log('Mostrando resultado:', data);
        
        // Limpiar resultado anterior
        this.elements.resultOutput.innerHTML = '';
        this.elements.resultOutput.className = 'resultado-container';

        // Agregar timestamp
        const timestampDiv = document.createElement('div');
        timestampDiv.className = 'timestamp';
        timestampDiv.textContent = data.timestamp || 'Análisis realizado: ' + new Date().toLocaleString();
        this.elements.resultOutput.appendChild(timestampDiv);

        // Procesar y formatear el resultado
        const contenidoResultado = document.createElement('div');
        contenidoResultado.className = 'resultado-contenido';
        
        if (data.resultado) {
            const lineas = data.resultado.split('\n');
            lineas.forEach(linea => {
                if (linea.trim()) {
                    const lineaDiv = document.createElement('div');
                    
                    // Determinar si es un mensaje especial
                    if (linea.includes('✓') || linea.includes('Análisis léxico completado correctamente') || linea.includes('Tokens válidos:')) {
                        lineaDiv.className = 'mensaje-especial success';
                    } else if (linea.includes('⚠') || linea.includes('Tokens con error:')) {
                        lineaDiv.className = 'mensaje-especial error';
                    } else {
                        lineaDiv.className = 'resultado-linea';
                    }
                    
                    lineaDiv.textContent = linea;
                    contenidoResultado.appendChild(lineaDiv);
                }
            });
        }

        // Agregar el contenido al resultado
        this.elements.resultOutput.appendChild(contenidoResultado);
        
        // Animar el scroll al resultado
        this.elements.resultOutput.scrollIntoView({ behavior: 'smooth' });
    },

    // Procesar el resumen del análisis
    procesarResumen(resultado) {
        const resumenDiv = document.createElement('div');
        resumenDiv.className = 'analisis-resumen';
        
        const lineas = resultado.split('\n');
        const inicioResumen = lineas.findIndex(l => l.includes('Resumen del análisis'));
        
        if (inicioResumen !== -1) {
            const resumenLineas = lineas.slice(inicioResumen);
            
            resumenLineas.forEach(linea => {
                if (linea.includes(':')) {
                    const [titulo, valor] = linea.split(':').map(s => s.trim());
                    const itemDiv = document.createElement('div');
                    itemDiv.className = 'resumen-item';
                    
                    const tituloSpan = document.createElement('span');
                    tituloSpan.textContent = titulo;
                    
                    const valorSpan = document.createElement('span');
                    valorSpan.className = 'resumen-valor';
                    valorSpan.textContent = valor;
                    
                    // Agregar clases basadas en el tipo de valor
                    if (titulo.toLowerCase().includes('error')) {
                        valorSpan.classList.add('error');
                    } else if (titulo.toLowerCase().includes('válidos')) {
                        valorSpan.classList.add('success');
                    }
                    
                    itemDiv.appendChild(tituloSpan);
                    itemDiv.appendChild(valorSpan);
                    resumenDiv.appendChild(itemDiv);
                }
            });
        }
        
        return resumenDiv;
    },

    // Mostrar error
    mostrarError(error) {
        const errorContainer = document.createElement('div');
        errorContainer.className = 'resultado-linea error';
        errorContainer.textContent = `Error: ${error}`;
        
        this.elements.resultOutput.innerHTML = '';
        this.elements.resultOutput.className = 'error';
        this.elements.resultOutput.appendChild(errorContainer);
    },

    // Mostrar estado de carga
    mostrarCargando() {
        const loadingContainer = document.createElement('div');
        loadingContainer.className = 'loading-container';
        
        const spinner = document.createElement('div');
        spinner.className = 'loading-spinner';
        
        loadingContainer.appendChild(spinner);
        
        this.elements.resultOutput.innerHTML = '';
        this.elements.resultOutput.appendChild(loadingContainer);
    },

    // Realizar análisis
    async analizar(tipo) {
        if (this.state.isAnalyzing) {
            this.showTemporaryMessage('Análisis en proceso, por favor espere...', 'warning');
            return;
        }

        const code = this.editor.getValue().trim();
        console.log('Código original:', code); // Debug log
        
        if (!code) {
            this.mostrarError('Por favor, ingrese código para analizar.');
            return;
        }

        // Validación específica para máquina de Turing
        if (tipo === 'turing') {
            console.log('Iniciando análisis de Turing'); // Debug log
            
            // Verificar si el código solo contiene 0s, 1s y espacios en blanco
            if (!/^[01\s\n\r]*$/.test(code)) {
                console.log('Entrada inválida: contiene caracteres no permitidos'); // Debug log
                this.mostrarError('La entrada para la máquina de Turing solo puede contener 0s y 1s.');
                return;
            }
            
            const cleanCode = code.replace(/[\s\n\r]+/g, '');
            console.log('Código limpio:', cleanCode); // Debug log
            
            if (cleanCode.length === 0 || !cleanCode.match(/^[01]+$/)) {
                console.log('Entrada inválida: vacía o sin 0s y 1s'); // Debug log
                this.mostrarError('La entrada para la máquina de Turing debe contener al menos un 0 o 1.');
                return;
            }
        }

        try {
            this.state.isAnalyzing = true;
            this.state.lastAnalysis = tipo;
            
            // Mostrar estado de carga
            this.mostrarCargando();
            
            console.log('Enviando petición al servidor...'); // Debug log
            const response = await fetch(`/${tipo}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code: tipo === 'turing' ? code.replace(/[\s\n\r]+/g, '') : code })
            });

            console.log('Respuesta recibida, status:', response.status); // Debug log

            if (!response.ok) {
                throw new Error(`Error del servidor: ${response.status}`);
            }

            const data = await response.json();
            console.log('Datos recibidos:', data); // Debug log

            if (data.status === 'error') {
                console.log('Error en el resultado:', data.resultado); // Debug log
                this.mostrarError(data.resultado);
                return;
            }

            this.mostrarResultado(data);

        } catch (error) {
            console.error('Error en el análisis:', error);
            this.mostrarError(`Error al procesar la solicitud: ${error.message}`);
        } finally {
            this.state.isAnalyzing = false;
        }
    }
};

// Inicializar la aplicación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    console.log('Iniciando IDE...');
    IDE.init();
}); 
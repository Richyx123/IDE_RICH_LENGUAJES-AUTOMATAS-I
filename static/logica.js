// Inicialización de CodeMirror
let editor;

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar CodeMirror
    editor = CodeMirror.fromTextArea(document.getElementById('codigo'), {
        mode: 'python',
        theme: 'monokai',
        lineNumbers: true,
        autoCloseBrackets: true,
        matchBrackets: true,
        indentUnit: 4,
        tabSize: 4,
        indentWithTabs: false,
        lineWrapping: true,
        autofocus: true
    });

    // Configurar eventos de botones
    document.getElementById('btn-lexico').addEventListener('click', () => realizarAnalisis('analizar-lexico'));
    document.getElementById('btn-sintactico').addEventListener('click', () => realizarAnalisis('analizar-sintactico'));
    document.getElementById('btn-turing').addEventListener('click', () => realizarAnalisis('turing'));

    // Agregar evento para validación en tiempo real
    editor.on('change', function(cm, change) {
        validarEnTiempoReal(cm);
    });
});

function validarEnTiempoReal(cm) {
    // Limpiar marcadores existentes
    cm.getAllMarks().forEach(mark => mark.clear());

    const codigo = cm.getValue();
    const lineas = codigo.split('\n');

    lineas.forEach((linea, numLinea) => {
        // Si estamos en modo sintáctico
        if (cm.getOption('mode') === 'analizar-sintactico') {
            if (!linea.trim()) return; // Ignorar líneas vacías

            // Remover el punto y coma final si existe
            let lineaSinPuntoComa = linea.trim();
            const tienePuntoComa = lineaSinPuntoComa.endsWith(';');
            if (tienePuntoComa) {
                lineaSinPuntoComa = lineaSinPuntoComa.slice(0, -1).trim();
            }

            // Validar la estructura de asignación
            const partes = lineaSinPuntoComa.split('=');
            
            if (partes.length !== 2) {
                // Marcar toda la línea como error
                cm.markText(
                    {line: numLinea, ch: 0},
                    {line: numLinea, ch: linea.length},
                    {
                        className: 'syntax-error',
                        title: 'Error de sintaxis: La línea debe tener formato "identificador = valor;"'
                    }
                );
                return;
            }

            const [identificador, valor] = partes.map(p => p.trim());
            
            // Validar que el identificador sea válido
            if (!identificador.match(/^[a-zA-Z_][a-zA-Z0-9_]*$/)) {
                cm.markText(
                    {line: numLinea, ch: linea.indexOf(identificador)},
                    {line: numLinea, ch: linea.indexOf(identificador) + identificador.length},
                    {
                        className: 'syntax-error',
                        title: 'Identificador inválido: Debe comenzar con letra o _ y contener solo letras, números y _'
                    }
                );
            }

            // Validar que el valor sea un número o un identificador válido
            if (!valor.match(/^[0-9]+$/) && !valor.match(/^[a-zA-Z_][a-zA-Z0-9_]*$/)) {
                cm.markText(
                    {line: numLinea, ch: linea.indexOf(valor)},
                    {line: numLinea, ch: linea.indexOf(valor) + valor.length},
                    {
                        className: 'syntax-error',
                        title: 'Valor inválido: Debe ser un número o un identificador válido'
                    }
                );
            }

            // Validar que tenga punto y coma al final
            if (!tienePuntoComa) {
                cm.markText(
                    {line: numLinea, ch: linea.length},
                    {line: numLinea, ch: linea.length},
                    {
                        className: 'syntax-error',
                        title: 'Error de sintaxis: Falta punto y coma (;) al final de la línea'
                    }
                );
            }
        }
        // Si estamos en modo Turing
        else if (cm.getOption('mode') === 'turing') {
            let pos = 0;
            while (pos < linea.length) {
                let char = linea[pos];
                if (!/[01\s]/.test(char)) {
                    cm.markText(
                        {line: numLinea, ch: pos},
                        {line: numLinea, ch: pos + 1},
                        {
                            className: 'syntax-error',
                            title: 'Carácter inválido: Solo se permiten 0s y 1s'
                        }
                    );
                }
                pos++;
            }
        }
        // Para el análisis léxico
        else {
            let pos = 0;
            while (pos < linea.length) {
                let char = linea[pos];
                if (/[^a-zA-Z0-9_\s=+\-*\/(){}[\]<>!&|;,."']/.test(char)) {
                    cm.markText(
                        {line: numLinea, ch: pos},
                        {line: numLinea, ch: pos + 1},
                        {
                            className: 'syntax-error',
                            title: 'Carácter inválido'
                        }
                    );
                }
                pos++;
            }
        }
    });
}

// Función para cambiar el modo de validación
function cambiarModoValidacion(modo) {
    editor.setOption('mode', modo);
    validarEnTiempoReal(editor);
}

async function realizarAnalisis(tipo) {
    // Cambiar el modo de validación según el tipo de análisis
    cambiarModoValidacion(tipo);
    
    const codigo = editor.getValue();
    const resultadoContainer = document.querySelector('.resultado-container');
    
    try {
        const response = await fetch(`/${tipo}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ codigo: codigo })
        });

        const data = await response.json();
        
        // Limpiar el contenedor de resultados
        resultadoContainer.innerHTML = '';

        if (data.error) {
            // Mostrar error
            const errorDiv = document.createElement('div');
            errorDiv.className = 'resultado-error';
            errorDiv.textContent = data.error;
            resultadoContainer.appendChild(errorDiv);
            return;
        }

        // Procesar resultados según el tipo de análisis
        if (tipo === 'analizar-lexico') {
            mostrarResultadoLexico(data, resultadoContainer);
        } else if (tipo === 'analizar-sintactico') {
            mostrarResultadoSintactico(data, resultadoContainer);
        } else {
            mostrarResultadoTuring(data, resultadoContainer);
        }

    } catch (error) {
        console.error('Error:', error);
        resultadoContainer.innerHTML = `
            <div class="resultado-error">
                Error al procesar la solicitud: ${error.message}
            </div>
        `;
    }
}

function mostrarResultadoLexico(data, container) {
    // Contenedor principal con borde verde
    const mainContainer = document.createElement('div');
    mainContainer.className = `resultado-principal resultado-container ${data.exitoso ? 'valido' : 'invalido'}`;

    // Mensaje de éxito
    const mensajeExito = document.createElement('div');
    mensajeExito.className = 'resultado-mensaje-exito';
    mensajeExito.innerHTML = `✓ Análisis léxico completado correctamente:`;
    mainContainer.appendChild(mensajeExito);

    // Lista de todos los tokens encontrados
    const tokensHeader = document.createElement('div');
    tokensHeader.className = 'resultado-resumen-header';
    tokensHeader.textContent = 'Tokens encontrados:';
    mainContainer.appendChild(tokensHeader);

    // Contenedor para los tokens
    const tokensContainer = document.createElement('div');
    tokensContainer.className = 'tokens-container';
    
    data.resultados.forEach((token, index) => {
        const tokenDiv = document.createElement('div');
        tokenDiv.className = `resultado-token ${token.valido ? 'token-valido' : 'token-invalido'}`;
        tokenDiv.innerHTML = `
            <strong>Token ${index + 1}:</strong>
            Tipo: ${token.tipo}
            | Valor: ${token.valor}
            | Línea: ${token.linea}
            | Posición: ${token.posicion}
            | Estado: ${token.valido ? '✓ Válido' : '❌ Inválido'}
        `;
        tokensContainer.appendChild(tokenDiv);
    });
    mainContainer.appendChild(tokensContainer);

    // Resumen del análisis
    const resumenHeader = document.createElement('div');
    resumenHeader.className = 'resultado-resumen-header';
    resumenHeader.textContent = 'Resumen del análisis léxico:';
    mainContainer.appendChild(resumenHeader);

    // Total de tokens
    const totalTokens = document.createElement('div');
    totalTokens.className = 'resultado-total';
    totalTokens.textContent = `Total de tokens analizados: ${data.total_tokens}`;
    mainContainer.appendChild(totalTokens);

    // Tokens válidos (en contenedor verde)
    const validosDiv = document.createElement('div');
    validosDiv.className = 'resultado-validos';
    validosDiv.innerHTML = `✓ Tokens válidos: ${data.tokens_validos}`;
    mainContainer.appendChild(validosDiv);

    // Tokens con error (en contenedor rojo)
    const invalidosDiv = document.createElement('div');
    invalidosDiv.className = 'resultado-invalidos';
    invalidosDiv.innerHTML = `⚠ Tokens con error: ${data.tokens_error}`;
    mainContainer.appendChild(invalidosDiv);

    // Número de líneas analizadas
    const lineasDiv = document.createElement('div');
    lineasDiv.className = 'resultado-lineas';
    lineasDiv.textContent = `Número de líneas analizadas: ${data.lineas_analizadas}`;
    mainContainer.appendChild(lineasDiv);

    container.appendChild(mainContainer);
}

function mostrarResultadoSintactico(data, container) {
    // Contenedor principal
    const mainContainer = document.createElement('div');
    mainContainer.className = `sintactico-container ${data.exitoso ? 'valido' : 'invalido'}`;

    // Timestamp
    const timestamp = document.createElement('div');
    timestamp.className = 'resultado-timestamp';
    timestamp.textContent = data.timestamp;
    mainContainer.appendChild(timestamp);

    // Mensaje de estado del análisis
    const mensajeDiv = document.createElement('div');
    mensajeDiv.className = data.exitoso ? 'sintactico-mensaje-exito' : 'sintactico-mensaje-error';
    mensajeDiv.textContent = data.mensaje;
    mainContainer.appendChild(mensajeDiv);

    // Mostrar errores si existen
    if (data.errores && data.errores.length > 0) {
        data.errores.forEach(error => {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'sintactico-error';
            errorDiv.textContent = error;
            mainContainer.appendChild(errorDiv);
        });

        // Mostrar el código con error
        const codigoErrorDiv = document.createElement('div');
        codigoErrorDiv.className = 'codigo-error';
        codigoErrorDiv.textContent = editor.getValue();
        mainContainer.appendChild(codigoErrorDiv);

        // Mensaje de error sintáctico
        const errorSpanDiv = document.createElement('div');
        errorSpanDiv.className = 'error-sintactico';
        errorSpanDiv.innerHTML = '└─ Error sintáctico</span>';
        mainContainer.appendChild(errorSpanDiv);
    }

    // Resumen del análisis
    const resumenHeader = document.createElement('div');
    resumenHeader.className = 'sintactico-resumen-header';
    resumenHeader.textContent = 'Resumen del análisis sintáctico:';
    mainContainer.appendChild(resumenHeader);

    // Total de líneas analizadas
    const totalLineas = document.createElement('div');
    totalLineas.className = 'sintactico-total-lineas';
    totalLineas.textContent = `Total de líneas analizadas: ${data.lineas_analizadas}`;
    mainContainer.appendChild(totalLineas);

    // Líneas válidas
    const lineasValidas = document.createElement('div');
    lineasValidas.className = 'sintactico-lineas-validas';
    lineasValidas.textContent = `Líneas válidas: ${data.lineas_validas}`;
    mainContainer.appendChild(lineasValidas);

    // Líneas con error
    const lineasError = document.createElement('div');
    lineasError.className = 'sintactico-lineas-error';
    lineasError.textContent = `Líneas con error: ${data.lineas_error}`;
    mainContainer.appendChild(lineasError);

    container.appendChild(mainContainer);
}

function mostrarResultadoTuring(data, container) {
    // Crear el contenedor principal
    const resultadoDiv = document.createElement('div');
    resultadoDiv.className = `turing-resultado ${data.exitoso ? 'valido' : 'invalido'}`;

    // Dividir el resultado en líneas y aplicar formato
    const lineas = data.resultado.split('\n');
    lineas.forEach((linea, index) => {
        const lineaDiv = document.createElement('div');
        
        // Aplicar clases según el contenido de la línea
        if (linea.includes('╔') || linea.includes('╚') || linea.includes('║')) {
            lineaDiv.className = 'turing-border';
        } else if (linea.includes('📍')) {
            lineaDiv.className = 'entrada';
        } else if (linea.includes('❌')) {
            lineaDiv.className = 'error';
        } else if (linea.includes('✅')) {
            lineaDiv.className = 'success';
        } else if (linea.includes('═')) {
            lineaDiv.className = 'separator';
        }

        // Mantener los emojis y caracteres especiales
        lineaDiv.textContent = linea;
        resultadoDiv.appendChild(lineaDiv);
    });

    container.appendChild(resultadoDiv);
}

// Función para resaltar líneas específicas
function resaltarLinea(numeroLinea, tipo) {
    const linea = editor.getLineHandle(numeroLinea - 1);
    editor.addLineClass(linea, 'background', tipo === 'valido' ? 'linea-valida' : 'linea-invalida');
    
    // Remover el resaltado después de la animación
    setTimeout(() => {
        editor.removeLineClass(linea, 'background', tipo === 'valido' ? 'linea-valida' : 'linea-invalida');
    }, 2000);
}
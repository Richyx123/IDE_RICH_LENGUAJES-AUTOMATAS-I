def analizar_lexico(code):
    # Conjunto de tokens reconocidos
    palabras_clave = {
        "if", "else", "while", "for", "return", "def", "class",
        "import", "from", "as", "try", "except", "finally",
        "with", "is", "in", "and", "or", "not", "True", "False", "None"
    }
    
    simbolos = {
        "(", ")", "{", "}", "[", "]", ";", "+", "-", "*", "/",
        "=", "<", ">", "!", ":", ",", ".", "+=", "-=", "*=", "/=",
        "==", "!=", "<=", ">=", "&&", "||"
    }
    
    numeros = set("0123456789")
    caracteres_invalidos = {"~", "@", "$", "%", "#", "¡", "¿"}
    tokens = []
    hay_error = False
    numero_linea = 1

    # Dividir el código en líneas para mejor seguimiento
    lineas = code.split('\n')
    
    for linea in lineas:
        if not linea.strip():  # Ignorar líneas vacías
            numero_linea += 1
            continue
            
        palabras = linea.strip().split()
        posicion_en_linea = 1
        
        for palabra in palabras:
            # Verificar caracteres inválidos
            caracteres_invalidos_encontrados = [c for c in palabra if c in caracteres_invalidos]
            if caracteres_invalidos_encontrados:
                tokens.append(f"Error en línea {numero_linea}, posición {posicion_en_linea}: "
                            f"Caracteres inválidos en '{palabra}': {', '.join(caracteres_invalidos_encontrados)}")
                hay_error = True
                posicion_en_linea += len(palabra) + 1
                continue

            # Verificar operadores compuestos
            if palabra in simbolos:
                tokens.append(f"Línea {numero_linea}, posición {posicion_en_linea}: "
                            f"Operador/Símbolo válido: {palabra}")
            # Verificar palabras clave
            elif palabra in palabras_clave:
                tokens.append(f"Línea {numero_linea}, posición {posicion_en_linea}: "
                            f"Palabra clave: {palabra}")
            # Verificar números
            elif palabra.isdigit():
                tokens.append(f"Línea {numero_linea}, posición {posicion_en_linea}: "
                            f"Número: {palabra}")
            # Verificar números decimales
            elif palabra.replace('.', '', 1).isdigit() and palabra.count('.') == 1:
                tokens.append(f"Línea {numero_linea}, posición {posicion_en_linea}: "
                            f"Número decimal: {palabra}")
            # Verificar identificadores
            elif palabra[0].isalpha() or palabra[0] == '_':
                if all(c.isalnum() or c == '_' for c in palabra):
                    tokens.append(f"Línea {numero_linea}, posición {posicion_en_linea}: "
                                f"Identificador válido: {palabra}")
                else:
                    tokens.append(f"Error en línea {numero_linea}, posición {posicion_en_linea}: "
                                f"Identificador inválido '{palabra}' - solo se permiten letras, números y _")
                    hay_error = True
            # Verificar operadores y símbolos compuestos
            else:
                # Intentar descomponer en símbolos válidos
                token_actual = ""
                es_valido = True
                for char in palabra:
                    token_actual += char
                    if token_actual in simbolos:
                        tokens.append(f"Línea {numero_linea}, posición {posicion_en_linea}: "
                                    f"Operador/Símbolo válido: {token_actual}")
                        token_actual = ""
                    elif len(token_actual) > 2:  # Si no se reconoce después de 2 caracteres, es inválido
                        tokens.append(f"Error en línea {numero_linea}, posición {posicion_en_linea}: "
                                    f"Token no reconocido: {token_actual}")
                        hay_error = True
                        es_valido = False
                        break
                
                if token_actual and es_valido:
                    tokens.append(f"Error en línea {numero_linea}, posición {posicion_en_linea}: "
                                f"Token no reconocido: {token_actual}")
                    hay_error = True

            posicion_en_linea += len(palabra) + 1
        
        numero_linea += 1

    if not tokens:
        return "Error: No se encontraron tokens para analizar"
    
    # Agregar resumen del análisis
    total_tokens = len(tokens)
    tokens_error = sum(1 for t in tokens if "Error" in t)
    tokens_validos = total_tokens - tokens_error
    
    resumen = [
        "\nResumen del análisis léxico:",
        f"Total de tokens analizados: {total_tokens}",
        f"Tokens válidos: {tokens_validos}",
        f"Tokens con error: {tokens_error}",
        f"Número de líneas analizadas: {numero_linea - 1}\n"
    ]
    
    if hay_error:
        return "Análisis léxico completado con errores:\n" + "\n".join(tokens + resumen)
    else:
        return "Análisis léxico completado correctamente:\n" + "\n".join(tokens + resumen)
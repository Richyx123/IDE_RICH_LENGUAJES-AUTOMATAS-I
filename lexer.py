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

    # Si el código está vacío
    if not code.strip():
        return {
            'tokens': [],
            'linea': 'undefined',
            'posicion': 'undefined',
            'numero': 'undefined',
            'total_tokens': 1,
            'tokens_validos': 0,
            'tokens_error': 1,
            'lineas_analizadas': 'NaN'
        }

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
                tokens.append({
                    'linea': numero_linea,
                    'posicion': posicion_en_linea,
                    'tipo': 'Error',
                    'valor': f"Caracteres inválidos en '{palabra}': {', '.join(caracteres_invalidos_encontrados)}",
                    'valido': False
                })
                hay_error = True
                posicion_en_linea += len(palabra) + 1
                continue

            # Verificar operadores compuestos
            if palabra in simbolos:
                tokens.append({
                    'linea': numero_linea,
                    'posicion': posicion_en_linea,
                    'tipo': 'Símbolo',
                    'valor': palabra,
                    'valido': True
                })
            # Verificar palabras clave
            elif palabra in palabras_clave:
                tokens.append({
                    'linea': numero_linea,
                    'posicion': posicion_en_linea,
                    'tipo': 'Palabra clave',
                    'valor': palabra,
                    'valido': True
                })
            # Verificar números
            elif palabra.isdigit():
                tokens.append({
                    'linea': numero_linea,
                    'posicion': posicion_en_linea,
                    'tipo': 'Número',
                    'valor': palabra,
                    'valido': True
                })
            # Verificar números decimales
            elif palabra.replace('.', '', 1).isdigit() and palabra.count('.') == 1:
                tokens.append({
                    'linea': numero_linea,
                    'posicion': posicion_en_linea,
                    'tipo': 'Número decimal',
                    'valor': palabra,
                    'valido': True
                })
            # Verificar identificadores
            elif palabra[0].isalpha() or palabra[0] == '_':
                if all(c.isalnum() or c == '_' for c in palabra):
                    tokens.append({
                        'linea': numero_linea,
                        'posicion': posicion_en_linea,
                        'tipo': 'Identificador',
                        'valor': palabra,
                        'valido': True
                    })
                else:
                    tokens.append({
                        'linea': numero_linea,
                        'posicion': posicion_en_linea,
                        'tipo': 'Error',
                        'valor': f"Identificador inválido '{palabra}' - solo se permiten letras, números y _",
                        'valido': False
                    })
                    hay_error = True
            # Verificar operadores y símbolos compuestos
            else:
                # Intentar descomponer en símbolos válidos
                token_actual = ""
                es_valido = True
                for char in palabra:
                    token_actual += char
                    if token_actual in simbolos:
                        tokens.append({
                            'linea': numero_linea,
                            'posicion': posicion_en_linea,
                            'tipo': 'Símbolo',
                            'valor': token_actual,
                            'valido': True
                        })
                        token_actual = ""
                    elif len(token_actual) > 2:  # Si no se reconoce después de 2 caracteres, es inválido
                        tokens.append({
                            'linea': numero_linea,
                            'posicion': posicion_en_linea,
                            'tipo': 'Error',
                            'valor': f"Token no reconocido: {token_actual}",
                            'valido': False
                        })
                        hay_error = True
                        es_valido = False
                        break
                
                if token_actual and es_valido:
                    tokens.append({
                        'linea': numero_linea,
                        'posicion': posicion_en_linea,
                        'tipo': 'Error',
                        'valor': f"Token no reconocido: {token_actual}",
                        'valido': False
                    })
                    hay_error = True

            posicion_en_linea += len(palabra) + 1
        
        numero_linea += 1

    if not tokens:
        return {
            'tokens': [{
                'linea': 1,
                'posicion': 1,
                'tipo': 'Error',
                'valor': 'No se encontraron tokens',
                'valido': False
            }],
            'linea': 1,
            'posicion': 1,
            'numero': None,
            'total_tokens': 1,
            'tokens_validos': 0,
            'tokens_error': 1,
            'lineas_analizadas': 1
        }
    
    # Preparar el resultado
    tokens_validos = sum(1 for t in tokens if t['valido'])
    tokens_error = len(tokens) - tokens_validos
    
    # Devolver el resultado estructurado
    return {
        'tokens': tokens,
        'linea': tokens[0]['linea'],
        'posicion': tokens[0]['posicion'],
        'numero': tokens[0]['valor'] if tokens[0]['tipo'] == 'Número' else None,
        'total_tokens': len(tokens),
        'tokens_validos': tokens_validos,
        'tokens_error': tokens_error,
        'lineas_analizadas': numero_linea - 1
    }
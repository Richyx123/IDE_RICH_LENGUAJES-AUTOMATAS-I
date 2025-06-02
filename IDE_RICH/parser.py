import ply.yacc as yacc
from lexer import analizar_lexico

class Parser:
    def __init__(self):
        self.errores = []
        self.tokens = []
        self.arbol = None
        self.current_token = None
        self.token_index = -1
        self.lineas_validas = 0
        self.lineas_error = 0
        self.total_lineas = 0

    def _validar_lexico(self, codigo):
        """Valida el código léxicamente sin mostrar los resultados"""
        resultado = analizar_lexico(codigo)
        # Verificar si hay errores léxicos sin mostrar el resultado completo
        return not ("Error" in resultado and "completado con errores" in resultado)

    def _generar_subrayado(self, linea, inicio, fin):
        """Genera el mensaje de error sin subrayado"""
        return f'{linea}'

    def _encontrar_error_posicion(self, linea, tipo_error):
        """Encuentra la posición del error basado en el tipo"""
        if tipo_error == 'balance':
            # Buscar el primer símbolo desbalanceado
            pila = []
            pares = {')': '(', '}': '{', ']': '['}
            for i, char in enumerate(linea):
                if char in '({[':
                    pila.append((char, i))
                elif char in ')}]':
                    if not pila or pila[-1][0] != pares[char]:
                        return i, i + 1
                    pila.pop()
            if pila:
                return pila[0][1], pila[0][1] + 1
        
        elif tipo_error == 'dos_puntos':
            # Error por falta de dos puntos al final
            return len(linea), len(linea) + 1
        
        elif tipo_error == 'punto_y_coma':
            # Error por falta de punto y coma al final
            return len(linea), len(linea) + 1
        
        elif tipo_error == 'asignacion':
            # Error en la asignación
            igual_pos = linea.find('=')
            if igual_pos != -1:
                return igual_pos - 1, igual_pos + 2
        
        return 0, len(linea)  # Por defecto, subraya toda la línea

    def parse(self, codigo):
        if not codigo:
            return {
                'exitoso': False,
                'mensaje': 'No hay código para analizar',
                'errores': ['No hay código para analizar'],
                'lineas_analizadas': 0,
                'lineas_validas': 0,
                'lineas_error': 0
            }

        lineas = codigo.strip().split('\n')
        self.total_lineas = len([l for l in lineas if l.strip()])
        self.lineas_validas = 0
        self.lineas_error = 0
        self.errores = []

        for num_linea, linea in enumerate(lineas, 1):
            if not linea.strip():
                continue

            # Verificar si la línea termina con punto y coma
            if not linea.strip().endswith(';'):
                self.errores.append(f'Error en línea {num_linea}: Falta punto y coma al final de la instrucción')
                self.lineas_error += 1
                continue

            # Remover el punto y coma para el análisis
            linea_sin_pc = linea.strip()[:-1].strip()

            # Verificar la estructura de asignación
            partes = linea_sin_pc.split('=')
            if len(partes) != 2:
                self.errores.append(f'Error en línea {num_linea}: La línea debe tener formato "identificador = valor"')
                self.lineas_error += 1
                continue

            identificador, valor = partes[0].strip(), partes[1].strip()

            # Validar el identificador
            if not identificador.isidentifier():
                self.errores.append(f'Error en línea {num_linea}: Identificador inválido "{identificador}"')
                self.lineas_error += 1
                continue

            # Validar el valor (debe ser un número o un identificador)
            if not (valor.isdigit() or valor.isidentifier()):
                self.errores.append(f'Error en línea {num_linea}: Valor inválido "{valor}"')
                self.lineas_error += 1
                continue

            # Si llegamos aquí, la línea es válida
            self.lineas_validas += 1

        # Preparar el resultado
        resultado = {
            'exitoso': len(self.errores) == 0,
            'mensaje': 'Análisis sintáctico completado correctamente' if len(self.errores) == 0 else 'Análisis sintáctico completado con errores',
            'errores': self.errores,
            'lineas_analizadas': self.total_lineas,
            'lineas_validas': self.lineas_validas,
            'lineas_error': self.lineas_error
        }

        return resultado

    def tokenize(self, codigo):
        self.tokens = []
        lineas = codigo.split('\n')
        
        for num_linea, linea in enumerate(lineas, 1):
            palabras = linea.strip().split()
            for palabra in palabras:
                if palabra in ['if', 'else', 'while', 'for', 'def', 'return']:
                    self.tokens.append({
                        'tipo': 'palabra_clave',
                        'valor': palabra,
                        'linea': num_linea
                    })
                elif palabra.isdigit():
                    self.tokens.append({
                        'tipo': 'numero',
                        'valor': palabra,
                        'linea': num_linea
                    })
                elif palabra[0].isalpha() or palabra[0] == '_':
                    self.tokens.append({
                        'tipo': 'identificador',
                        'valor': palabra,
                        'linea': num_linea
                    })
                elif palabra in ['(', ')', '{', '}', '[', ']', ';', '+', '-', '*', '/', '=', '<', '>', '!']:
                    self.tokens.append({
                        'tipo': 'operador',
                        'valor': palabra,
                        'linea': num_linea
                    })
                else:
                    self.errores.append(f"Error en línea {num_linea}: Token no reconocido '{palabra}'")

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None

    def programa(self):
        while self.current_token is not None:
            if self.current_token['tipo'] == 'palabra_clave':
                if self.current_token['valor'] == 'if':
                    self.if_statement()
                elif self.current_token['valor'] == 'while':
                    self.while_statement()
                elif self.current_token['valor'] == 'for':
                    self.for_statement()
                elif self.current_token['valor'] == 'def':
                    self.function_definition()
                else:
                    self.advance()
            else:
                self.advance()

    def if_statement(self):
        if self.current_token['valor'] != 'if':
            self.errores.append(f"Error en línea {self.current_token['linea']}: Se esperaba 'if'")
            return
        
        self.advance()  # Consumir 'if'
        
        # Verificar paréntesis de apertura
        if not self.current_token or self.current_token['valor'] != '(':
            self.errores.append(f"Error en línea {self.current_token['linea']}: Se esperaba '(' después de 'if'")
            return
        
        self.advance()  # Consumir '('
        
        # Verificar condición
        while self.current_token and self.current_token['valor'] != ')':
            self.advance()
        
        if not self.current_token or self.current_token['valor'] != ')':
            self.errores.append(f"Error en línea {self.current_token['linea']}: Se esperaba ')'")
            return
        
        self.advance()  # Consumir ')'

    def while_statement(self):
        if self.current_token['valor'] != 'while':
            self.errores.append(f"Error en línea {self.current_token['linea']}: Se esperaba 'while'")
            return
        
        self.advance()  # Consumir 'while'
        
        # Verificar paréntesis de apertura
        if not self.current_token or self.current_token['valor'] != '(':
            self.errores.append(f"Error en línea {self.current_token['linea']}: Se esperaba '(' después de 'while'")
            return
        
        self.advance()  # Consumir '('
        
        # Verificar condición
        while self.current_token and self.current_token['valor'] != ')':
            self.advance()
        
        if not self.current_token or self.current_token['valor'] != ')':
            self.errores.append(f"Error en línea {self.current_token['linea']}: Se esperaba ')'")
            return
        
        self.advance()  # Consumir ')'

    def for_statement(self):
        if self.current_token['valor'] != 'for':
            self.errores.append(f"Error en línea {self.current_token['linea']}: Se esperaba 'for'")
            return
        
        self.advance()  # Consumir 'for'
        
        # Verificar paréntesis de apertura
        if not self.current_token or self.current_token['valor'] != '(':
            self.errores.append(f"Error en línea {self.current_token['linea']}: Se esperaba '(' después de 'for'")
            return
        
        self.advance()  # Consumir '('
        
        # Verificar condición
        while self.current_token and self.current_token['valor'] != ')':
            self.advance()
        
        if not self.current_token or self.current_token['valor'] != ')':
            self.errores.append(f"Error en línea {self.current_token['linea']}: Se esperaba ')'")
            return
        
        self.advance()  # Consumir ')'

    def function_definition(self):
        if self.current_token['valor'] != 'def':
            self.errores.append(f"Error en línea {self.current_token['linea']}: Se esperaba 'def'")
            return
        
        self.advance()  # Consumir 'def'
        
        # Verificar nombre de función
        if not self.current_token or self.current_token['tipo'] != 'identificador':
            self.errores.append(f"Error en línea {self.current_token['linea']}: Se esperaba un identificador después de 'def'")
            return
        
        self.advance()  # Consumir nombre de función
        
        # Verificar paréntesis de apertura
        if not self.current_token or self.current_token['valor'] != '(':
            self.errores.append(f"Error en línea {self.current_token['linea']}: Se esperaba '(' después del nombre de la función")
            return
        
        self.advance()  # Consumir '('
        
        # Verificar parámetros
        while self.current_token and self.current_token['valor'] != ')':
            self.advance()
        
        if not self.current_token or self.current_token['valor'] != ')':
            self.errores.append(f"Error en línea {self.current_token['linea']}: Se esperaba ')'")
            return
        
        self.advance()  # Consumir ')'

    def _verificar_balance(self, linea):
        pila = []
        pares = {')': '(', '}': '{', ']': '['}
        
        for char in linea:
            if char in '({[':
                pila.append(char)
            elif char in ')}]':
                if not pila or pila.pop() != pares[char]:
                    return False
        
        return len(pila) == 0

    def _es_estructura_control(self, linea):
        palabras_control = ['if', 'for', 'while', 'def', 'class']
        return any(linea.strip().startswith(palabra) for palabra in palabras_control)

    def _requiere_punto_y_coma(self, linea):
        # Lista de palabras clave que no requieren punto y coma
        excepciones = ['if', 'for', 'while', 'def', 'class']
        return not any(linea.strip().startswith(palabra) for palabra in excepciones)

    def _marcar_error(self, mensaje, texto_error):
        """Marca el error en rojo y negrita"""
        return f'{mensaje}\n<span style="color: red; font-weight: bold;">{texto_error}</span>'

    def _formatear_error(self, tipo, mensaje):
        return f'<span style="color: red; font-weight: bold;">{tipo}: {mensaje}</span>'

    def _formatear_exito(self, tipo, mensaje):
        return f'<span style="color: green;">{tipo}: {mensaje}</span>'
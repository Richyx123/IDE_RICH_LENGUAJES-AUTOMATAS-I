import re

def marcar_error(mensaje, texto_error):
    """Marca el error subrayando la parte problemática"""
    return f'{mensaje}\n<span style="text-decoration: underline;">{texto_error}</span>'

def maquina_turing(cadena):
    log = []
    
    # Mostrar estado inicial con formato especial
    log.append("╔══════════════════════════════════════╗")
    log.append("║        MÁQUINA DE TURING             ║")
    log.append("╚══════════════════════════════════════╝")
    log.append(f"\n📍 Entrada recibida: {cadena}")
    
    # Si la cadena está vacía
    if not cadena:
        log.append("❌ Error: Debes ingresar una cadena válida")
        log.append("\n" + "═" * 40)
        log.append("❌ Resultado: Cadena Rechazada")
        log.append("La entrada está vacía")
        log.append("═" * 40)
        return "\n".join(log)
    
    # Verificar que solo contenga 1's y 0's usando expresión regular
    if not re.match('^[01]+$', cadena):
        caracteres_invalidos = [c for c in cadena if c not in ['0', '1']]
        log.append(f"❌ Error: La cadena contiene caracteres inválidos: {caracteres_invalidos}")
        log.append("\n" + "═" * 40)
        log.append("❌ Resultado: Cadena Rechazada")
        log.append("Solo se aceptan 1's y 0's")
        log.append("═" * 40)
        return "\n".join(log)
    
    # Verificar que contenga al menos un 0 y un 1
    if '0' not in cadena or '1' not in cadena:
        log.append("❌ Error: La cadena debe contener al menos un 0 y un 1")
        log.append("\n" + "═" * 40)
        log.append("❌ Resultado: Cadena Rechazada")
        log.append("Debe contener al menos un 0 y un 1")
        log.append("═" * 40)
        return "\n".join(log)
    
    # Si llegamos aquí, la cadena es válida
    log.append("✅ Cadena aceptada: contiene una combinación válida de 0s y 1s")
    log.append(f"   Cantidad de 0s: {cadena.count('0')}")
    log.append(f"   Cantidad de 1s: {cadena.count('1')}")
    
    # Resultado final con formato especial
    log.append("\n" + "═" * 40)
    log.append("✅ Resultado: Cadena Aceptada")
    log.append("La cadena contiene una combinación válida de 0s y 1s")
    log.append("═" * 40)
    
    return "\n".join(log)

class MaquinaTuring:
    def __init__(self):
        self.cinta = []
        self.posicion_cabezal = 0
        self.estado_actual = 'q0'
        self.estados_finales = {'qf'}
        self.errores = []

    def inicializar_cinta(self, entrada):
        """Inicializa la cinta con la entrada proporcionada"""
        if not self._validar_entrada(entrada):
            return marcar_error("Error de entrada", "La entrada solo debe contener 0s y 1s")
        
        self.cinta = list(entrada)
        self.posicion_cabezal = 0
        self.estado_actual = 'q0'
        return "Cinta inicializada correctamente"

    def ejecutar_paso(self):
        """Ejecuta un paso de la máquina de Turing"""
        try:
            if self.estado_actual in self.estados_finales:
                return "La máquina ha terminado"

            if self.posicion_cabezal < 0 or self.posicion_cabezal >= len(self.cinta):
                return marcar_error(
                    "Error de ejecución",
                    "El cabezal está fuera de los límites de la cinta"
                )

            # Obtener el símbolo actual
            simbolo_actual = self.cinta[self.posicion_cabezal]

            # Aplicar la transición según el estado actual y el símbolo
            nuevo_estado, nuevo_simbolo, movimiento = self._obtener_transicion(self.estado_actual, simbolo_actual)

            if nuevo_estado is None:
                return marcar_error(
                    "Error de transición",
                    f"No hay transición definida para el estado {self.estado_actual} y símbolo {simbolo_actual}"
                )

            # Actualizar la cinta y el estado
            self.cinta[self.posicion_cabezal] = nuevo_simbolo
            self.estado_actual = nuevo_estado

            # Mover el cabezal
            if movimiento == 'R':
                self.posicion_cabezal += 1
            elif movimiento == 'L':
                self.posicion_cabezal -= 1

            return f"Paso ejecutado: Estado={self.estado_actual}, Posición={self.posicion_cabezal}"

        except Exception as e:
            return marcar_error("Error de ejecución", str(e))

    def obtener_estado_cinta(self):
        """Devuelve una representación visual de la cinta"""
        try:
            if not self.cinta:
                return marcar_error("Error", "La cinta está vacía")

            resultado = []
            for i, simbolo in enumerate(self.cinta):
                if i == self.posicion_cabezal:
                    resultado.append(f"[{simbolo}]")
                else:
                    resultado.append(simbolo)
            
            return " ".join(resultado)

        except Exception as e:
            return marcar_error("Error al mostrar la cinta", str(e))

    def _validar_entrada(self, entrada):
        """Valida que la entrada solo contenga 0s y 1s"""
        return all(c in '01' for c in entrada)

    def _obtener_transicion(self, estado, simbolo):
        """Define las transiciones de la máquina de Turing"""
        # Ejemplo de tabla de transiciones para una máquina que convierte 0s en 1s
        transiciones = {
            ('q0', '0'): ('q0', '1', 'R'),
            ('q0', '1'): ('q0', '1', 'R'),
            ('q0', ' '): ('qf', ' ', 'N')
        }
        
        return transiciones.get((estado, simbolo), (None, None, None))

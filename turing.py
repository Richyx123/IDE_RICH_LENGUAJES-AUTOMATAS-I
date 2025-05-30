import re

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

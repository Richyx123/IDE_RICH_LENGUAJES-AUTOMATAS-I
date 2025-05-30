def analizar_sintactico(code):
    lineas = code.strip().split('\n')
    errores = []
    hay_error = False

    palabras_clave = ("if", "while", "for", "def", "else", "elif")

    for i, linea in enumerate(lineas, start=1):
        linea = linea.strip()
        if not linea:
            continue  # saltar líneas vacías

        if any(linea.startswith(clave) for clave in palabras_clave):
            if not linea.endswith(":"):
                errores.append(f"Error en línea {i}: Se esperaba ':' al final de '{linea}'")
                hay_error = True
            else:
                errores.append(f"Línea {i}: Estructura de control correcta: '{linea}'")
        elif "=" in linea:
            partes = linea.split("=")
            if len(partes) != 2 or not partes[0].strip().isidentifier():
                errores.append(f"Error en línea {i}: Asignación inválida en '{linea}'")
                hay_error = True
            else:
                errores.append(f"Línea {i}: Asignación correcta: '{linea}'")
        else:
            errores.append(f"Error en línea {i}: Estructura no reconocida: '{linea}'")
            hay_error = True

    if not errores:
        return "Error: No hay código para analizar"

    if hay_error:
        return "Análisis sintáctico completado con errores:\n" + "\n".join(errores)
    else:
        return "Análisis sintáctico completado correctamente:\n" + "\n".join(errores)
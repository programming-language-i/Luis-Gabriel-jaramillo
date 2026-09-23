def suma(valor1, valor2):
    return valor1 + valor2


def resta(valor1, valor2):
    return valor1 - valor2


def multi(valor1, valor2):
    return valor1 * valor2


def divi(valor1, valor2):
    if valor2 != 0:
        return valor1 / valor2
    else:
        return "Operacion no permitida sobre 0"


resultado_suma = suma(2, 5)
resultado_resta = resta(2, 5)
resultado_multi = multi(2, 5)
resultado_divi = divi(2, 5)

print(f"Resultado Suma: {resultado_suma}")
print(f"Resultado Resta: {resultado_resta}")
print(f"Resultado Multiplicacion: {resultado_multi}")
print(f"Resultado Division: {resultado_divi}")
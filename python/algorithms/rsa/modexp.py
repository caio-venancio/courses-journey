def modexp(base, exp, mod):
    resultado = 1

    while exp > 0:
        if exp % 2:
            resultado = (resultado * base) % mod

        base = (base * base) % mod
        exp //= 2

    return resultado


e = 7
d = 23
n = 187

mensagem = 189

c = modexp(mensagem, e, n)
print("Criptografado:", c)

m = modexp(c, d, n)
print("Descriptografado:", m)
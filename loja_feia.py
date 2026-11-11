# CODIGO FEIO DE PROPOSITO (TF 11). Funciona, mas viola quase todas as regras do
# Object Calisthenics. A missao e consertar SEM mudar o que ele imprime.
# Rodar no terminal: python3 loja_feia.py

pedidos = []                  # todos os pedidos da loja: lista solta, global


class Cpf:
    def __init__(self, valor):
        self.valor = valor

    def valido(self):
        return len(self.valor) == 11


class Email:
    def __init__(self, valor):
        self.valor = valor

    def tem_conteudo(self):
        return len(self.valor) > 0

    def tem_arroba(self):
        return "@" in self.valor


class Cep:
    def __init__(self, valor):
        self.valor = valor

    def valido(self):
        return len(self.valor) == 8


class Cliente:
    def __init__(self, nome, cpf, email, rua, cidade, cep, tipo_cliente):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.rua = rua
        self.cidade = cidade
        self.cep = cep
        self.tipo_cliente = tipo_cliente      # "N" normal, "V" vip, "F" funcionario


class Produto:
    def __init__(self, nome, valor_unitario):
        self.nome = nome
        self.valor_unitario = valor_unitario


class Pedido:
    def __init__(self, numero, cliente):
        self.numero = numero                  # numero do pedido
        self.cliente = cliente                # aponta para UM cliente
        self.itens = []                       # cada item e uma lista: [produto, quantidade]
        self.status = "A"                     # A = aberto, P = pago, C = cancelado

    def get_status(self):
        return self.status

    def set_status(self, valor):
        self.status = valor


def valida(email, cpf, cep):
    if email.tem_conteudo():
        if email.tem_arroba():
            if cpf.valido():
                if cep.valido():
                    return "ok"
                else:
                    return "cep invalido"
            else:
                return "cpf invalido"
        else:
            return "email invalido"
    else:
        return "email vazio"


def novo_pedido(numero, cliente):
    resultado = valida(cliente.email, cliente.cpf, cliente.cep)
    if resultado != "ok":
        print("pedido", numero, "recusado:", resultado)
        return None
    else:
        pedido = Pedido(numero, cliente)
        pedidos.append(pedido)
        return pedido


def adicionar_item(pedido, produto, quantidade):
    pedido.itens.append([produto, quantidade])


def total(pedido):
    soma = 0
    for item in pedido.itens:
        soma = soma + item[1] * item[0].valor_unitario
    return soma


def calcular_desconto(tipo_cliente, total_do_pedido):
    if tipo_cliente == "V":
        desconto = total_do_pedido * 0.10
    elif tipo_cliente == "F":
        desconto = total_do_pedido * 0.20
    else:
        desconto = 0
    return desconto


def valor_a_pagar(pedido):
    return total(pedido) - calcular_desconto(pedido.cliente.tipo_cliente, total(pedido))


def pagar(pedido):
    if pedido.get_status() == "A":
        if len(pedido.itens) > 0:
            pedido.set_status("P")
            return True
        else:
            return False
    else:
        return False


def cancelar(pedido):
    if pedido.get_status() == "A":
        pedido.set_status("C")
        return True
    else:
        return False


def status_por_extenso(status):
    if status == "A":
        return "aberto"
    elif status == "P":
        return "pago"
    else:
        return "cancelado"


def relatorio():
    for pedido in pedidos:
        print("Pedido", pedido.numero, "-", pedido.cliente.nome, "-", pedido.cliente.cidade)
        print("  status:", status_por_extenso(pedido.get_status()))
        for item in pedido.itens:
            print("  ", item[1], "x", item[0].nome, "= R$ %.2f" % (item[1] * item[0].valor_unitario))
        if len(pedido.itens) > 0:
            print("  total: R$ %.2f | desconto: R$ %.2f | a pagar: R$ %.2f" % (total(pedido), calcular_desconto(pedido.cliente.tipo_cliente, total(pedido)), valor_a_pagar(pedido)))


def arrecadado():
    soma = 0
    for pedido in pedidos:
        if pedido.get_status() == "P":
            soma = soma + valor_a_pagar(pedido)
    return soma


def quantidade_de_abertos():
    contagem = 0
    for pedido in pedidos:
        if pedido.get_status() == "A":
            contagem = contagem + 1
    return contagem


# --- o roteiro da loja (o TF mantem esta saida identica) -----------------------
caderno = Produto("Caderno", 15.5)
caneta = Produto("Caneta", 2.5)
livro = Produto("Livro", 89.5)
fone = Produto("Fone", 60.0)

ana = Cliente("Ana Souza", Cpf("12345678901"), Email("ana@mail.com"), "Rua das Flores, 10", "Sorocaba", Cep("18010000"), "V")
bruno = Cliente("Bruno Lima", Cpf("123"), Email("bruno@mail.com"), "Av. Central, 200", "Votorantim", Cep("18110000"), "N")
carla = Cliente("Carla Dias", Cpf("98765432100"), Email("carla.mail.com"), "Rua do Sol, 55", "Sorocaba", Cep("18020000"), "F")
diego = Cliente("Diego Rocha", Cpf("11122233344"), Email("diego@mail.com"), "Rua Nova, 7", "Itu", Cep("13300000"), "N")
eva = Cliente("Eva Nunes", Cpf("55566677788"), Email("eva@mail.com"), "Alameda Azul, 1", "Itu", Cep("13300001"), "F")
fabio = Cliente("Fabio Costa", Cpf("99988877766"), Email("fabio@mail.com"), "Rua Velha, 3", "Itu", Cep("123"), "N")
gil = Cliente("Gil Alves", Cpf("44455566677"), Email("gil@mail.com"), "Rua do Meio, 9", "Sorocaba", Cep("18030000"), "N")

pedido_ana_1 = novo_pedido(1, ana)
adicionar_item(pedido_ana_1, caderno, 2)
adicionar_item(pedido_ana_1, caneta, 5)

novo_pedido(2, bruno)

pedido_ana_3 = novo_pedido(3, ana)
adicionar_item(pedido_ana_3, livro, 1)

novo_pedido(4, carla)

pedido_diego = novo_pedido(5, diego)

pedido_eva = novo_pedido(6, eva)
adicionar_item(pedido_eva, fone, 1)

novo_pedido(7, fabio)

pedido_gil = novo_pedido(8, gil)
adicionar_item(pedido_gil, fone, 2)

print("pagar 1:", pagar(pedido_ana_1))
print("pagar 3:", pagar(pedido_ana_3))
print("pagar 5:", pagar(pedido_diego))
print("pagar 6:", pagar(pedido_eva))
print("cancelar 5:", cancelar(pedido_diego))
print("cancelar 1:", cancelar(pedido_ana_1))

relatorio()
print("arrecadado: R$ %.2f" % arrecadado())
print("abertos:", quantidade_de_abertos())
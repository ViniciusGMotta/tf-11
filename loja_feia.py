# CODIGO FEIO DE PROPOSITO (TF 11). Funciona, mas viola quase todas as regras do
# Object Calisthenics. A missao e consertar SEM mudar o que ele imprime.
# Rodar no terminal: python3 loja_feia.py


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


class Dinheiro:
    def __init__(self, valor):
        self.valor = valor

    def somar(self, outro):
        return Dinheiro(self.valor + outro.valor)

    def subtrair(self, outro):
        return Dinheiro(self.valor - outro.valor)

    def multiplicar(self, quantidade):
        return Dinheiro(self.valor * quantidade)

    def percentual(self, taxa):
        return Dinheiro(self.valor * taxa)

    def texto(self):
        return "%.2f" % self.valor


class Status:
    def __init__(self, valor):
        self.valor = valor                    # A = aberto, P = pago, C = cancelado

    def esta_aberto(self):
        return self.valor == "A"

    def esta_pago(self):
        return self.valor == "P"

    def texto(self):
        if self.valor == "A":
            return "aberto"
        elif self.valor == "P":
            return "pago"
        else:
            return "cancelado"


class Perfil:
    def __init__(self, nome, tipo_cliente):
        self.nome = nome
        self.tipo_cliente = tipo_cliente      # "N" normal, "V" vip, "F" funcionario


class Contato:
    def __init__(self, cpf, email):
        self.cpf = cpf
        self.email = email


class Identidade:
    def __init__(self, perfil, contato):
        self.perfil = perfil
        self.contato = contato


class Localidade:
    def __init__(self, cidade, cep):
        self.cidade = cidade
        self.cep = cep


class Endereco:
    def __init__(self, rua, localidade):
        self.rua = rua
        self.localidade = localidade


class Cliente:
    def __init__(self, identidade, endereco):
        self.identidade = identidade
        self.endereco = endereco


class Produto:
    def __init__(self, nome, valor_unitario):
        self.nome = nome
        self.valor_unitario = valor_unitario


class ItensDoPedido:
    def __init__(self):
        self.lista = []                       # cada item e uma lista: [produto, quantidade]

    def adicionar(self, produto, quantidade):
        self.lista.append([produto, quantidade])

    def tem_itens(self):
        return len(self.lista) > 0

    def total(self):
        soma = Dinheiro(0)
        for item in self.lista:
            soma = soma.somar(item[0].valor_unitario.multiplicar(item[1]))
        return soma

    def imprimir(self):
        for item in self.lista:
            print("  ", item[1], "x", item[0].nome, "= R$ %s" % item[0].valor_unitario.multiplicar(item[1]).texto())


class CabecalhoDoPedido:
    def __init__(self, numero, cliente):
        self.numero = numero                  # numero do pedido
        self.cliente = cliente                # aponta para UM cliente


class Andamento:
    def __init__(self, itens, status):
        self.itens = itens
        self.status = status


class Pedido:
    def __init__(self, numero, cliente):
        self.cabecalho = CabecalhoDoPedido(numero, cliente)
        self.andamento = Andamento(ItensDoPedido(), Status("A"))

    def get_status(self):
        return self.andamento.status

    def set_status(self, valor):
        self.andamento.status = valor


class Pedidos:
    def __init__(self):
        self.lista = []

    def adicionar(self, pedido):
        self.lista.append(pedido)

    def arrecadado(self):
        soma = Dinheiro(0)
        for pedido in self.lista:
            if pedido.get_status().esta_pago():
                soma = soma.somar(valor_a_pagar(pedido))
        return soma

    def quantidade_de_abertos(self):
        contagem = 0
        for pedido in self.lista:
            if pedido.get_status().esta_aberto():
                contagem = contagem + 1
        return contagem

    def relatorio(self):
        for pedido in self.lista:
            imprimir_pedido(pedido)


pedidos = Pedidos()           # todos os pedidos da loja


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
    email = cliente.identidade.contato.email
    cpf = cliente.identidade.contato.cpf
    cep = cliente.endereco.localidade.cep
    resultado = valida(email, cpf, cep)
    if resultado != "ok":
        print("pedido", numero, "recusado:", resultado)
        return None
    else:
        pedido = Pedido(numero, cliente)
        pedidos.adicionar(pedido)
        return pedido


def adicionar_item(pedido, produto, quantidade):
    pedido.andamento.itens.adicionar(produto, quantidade)


def total(pedido):
    return pedido.andamento.itens.total()


def calcular_desconto(tipo_cliente, total_do_pedido):
    if tipo_cliente == "V":
        desconto = total_do_pedido.percentual(0.10)
    elif tipo_cliente == "F":
        desconto = total_do_pedido.percentual(0.20)
    else:
        desconto = Dinheiro(0)
    return desconto


def valor_a_pagar(pedido):
    tipo_cliente = pedido.cabecalho.cliente.identidade.perfil.tipo_cliente
    return total(pedido).subtrair(calcular_desconto(tipo_cliente, total(pedido)))


def pagar(pedido):
    if pedido.get_status().esta_aberto():
        if pedido.andamento.itens.tem_itens():
            pedido.set_status(Status("P"))
            return True
        else:
            return False
    else:
        return False


def cancelar(pedido):
    if pedido.get_status().esta_aberto():
        pedido.set_status(Status("C"))
        return True
    else:
        return False


def imprimir_pedido(pedido):
    cliente = pedido.cabecalho.cliente
    nome = cliente.identidade.perfil.nome
    cidade = cliente.endereco.localidade.cidade
    tipo_cliente = cliente.identidade.perfil.tipo_cliente
    print("Pedido", pedido.cabecalho.numero, "-", nome, "-", cidade)
    print("  status:", pedido.get_status().texto())
    pedido.andamento.itens.imprimir()
    if pedido.andamento.itens.tem_itens():
        print("  total: R$ %s | desconto: R$ %s | a pagar: R$ %s" % (total(pedido).texto(), calcular_desconto(tipo_cliente, total(pedido)).texto(), valor_a_pagar(pedido).texto()))


# --- o roteiro da loja (o TF mantem esta saida identica) -----------------------
caderno = Produto("Caderno", Dinheiro(15.5))
caneta = Produto("Caneta", Dinheiro(2.5))
livro = Produto("Livro", Dinheiro(89.5))
fone = Produto("Fone", Dinheiro(60.0))

ana = Cliente(Identidade(Perfil("Ana Souza", "V"), Contato(Cpf("12345678901"), Email("ana@mail.com"))), Endereco("Rua das Flores, 10", Localidade("Sorocaba", Cep("18010000"))))
bruno = Cliente(Identidade(Perfil("Bruno Lima", "N"), Contato(Cpf("123"), Email("bruno@mail.com"))), Endereco("Av. Central, 200", Localidade("Votorantim", Cep("18110000"))))
carla = Cliente(Identidade(Perfil("Carla Dias", "F"), Contato(Cpf("98765432100"), Email("carla.mail.com"))), Endereco("Rua do Sol, 55", Localidade("Sorocaba", Cep("18020000"))))
diego = Cliente(Identidade(Perfil("Diego Rocha", "N"), Contato(Cpf("11122233344"), Email("diego@mail.com"))), Endereco("Rua Nova, 7", Localidade("Itu", Cep("13300000"))))
eva = Cliente(Identidade(Perfil("Eva Nunes", "F"), Contato(Cpf("55566677788"), Email("eva@mail.com"))), Endereco("Alameda Azul, 1", Localidade("Itu", Cep("13300001"))))
fabio = Cliente(Identidade(Perfil("Fabio Costa", "N"), Contato(Cpf("99988877766"), Email("fabio@mail.com"))), Endereco("Rua Velha, 3", Localidade("Itu", Cep("123"))))
gil = Cliente(Identidade(Perfil("Gil Alves", "N"), Contato(Cpf("44455566677"), Email("gil@mail.com"))), Endereco("Rua do Meio, 9", Localidade("Sorocaba", Cep("18030000"))))

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

pedidos.relatorio()
print("arrecadado: R$ %s" % pedidos.arrecadado().texto())
print("abertos:", pedidos.quantidade_de_abertos())
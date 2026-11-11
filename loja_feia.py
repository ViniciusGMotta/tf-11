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

    def nome_texto(self):
        return self.nome

    def desconto_sobre(self, total):
        if self.tipo_cliente == "V":
            desconto = total.percentual(0.10)
        elif self.tipo_cliente == "F":
            desconto = total.percentual(0.20)
        else:
            desconto = Dinheiro(0)
        return desconto


class Contato:
    def __init__(self, cpf, email):
        self.cpf = cpf
        self.email = email

    def validar(self):
        if self.email.tem_conteudo():
            if self.email.tem_arroba():
                if self.cpf.valido():
                    return "ok"
                else:
                    return "cpf invalido"
            else:
                return "email invalido"
        else:
            return "email vazio"


class Identidade:
    def __init__(self, perfil, contato):
        self.perfil = perfil
        self.contato = contato

    def validar(self):
        return self.contato.validar()

    def nome_texto(self):
        return self.perfil.nome_texto()

    def desconto_sobre(self, total):
        return self.perfil.desconto_sobre(total)


class Localidade:
    def __init__(self, cidade, cep):
        self.cidade = cidade
        self.cep = cep

    def validar(self):
        if self.cep.valido():
            return "ok"
        else:
            return "cep invalido"

    def cidade_texto(self):
        return self.cidade


class Endereco:
    def __init__(self, rua, localidade):
        self.rua = rua
        self.localidade = localidade

    def validar(self):
        return self.localidade.validar()

    def cidade_texto(self):
        return self.localidade.cidade_texto()


class Cliente:
    def __init__(self, identidade, endereco):
        self.identidade = identidade
        self.endereco = endereco

    def validar(self):
        resultado = self.identidade.validar()
        if resultado != "ok":
            return resultado
        else:
            return self.endereco.validar()

    def nome_texto(self):
        return self.identidade.nome_texto()

    def cidade_texto(self):
        return self.endereco.cidade_texto()

    def desconto_sobre(self, total):
        return self.identidade.desconto_sobre(total)


class Produto:
    def __init__(self, nome, valor_unitario):
        self.nome = nome
        self.valor_unitario = valor_unitario

    def nome_texto(self):
        return self.nome

    def valor_para(self, quantidade):
        return self.valor_unitario.multiplicar(quantidade)


class Item:
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade

    def subtotal(self):
        return self.produto.valor_para(self.quantidade)

    def imprimir(self):
        subtotal = self.subtotal()
        print("  ", self.quantidade, "x", self.produto.nome_texto(), "= R$ %s" % subtotal.texto())


class ItensDoPedido:
    def __init__(self):
        self.lista = []

    def adicionar(self, item):
        self.lista.append(item)

    def tem_itens(self):
        return len(self.lista) > 0

    def total(self):
        soma = Dinheiro(0)
        for item in self.lista:
            soma = soma.somar(item.subtotal())
        return soma

    def imprimir(self):
        for item in self.lista:
            item.imprimir()


class CabecalhoDoPedido:
    def __init__(self, numero, cliente):
        self.numero = numero                  # numero do pedido
        self.cliente = cliente                # aponta para UM cliente

    def desconto_sobre(self, total):
        return self.cliente.desconto_sobre(total)

    def imprimir(self):
        print("Pedido", self.numero, "-", self.cliente.nome_texto(), "-", self.cliente.cidade_texto())


class Andamento:
    def __init__(self, itens, status):
        self.itens = itens
        self.status = status

    def adicionar_item(self, produto, quantidade):
        self.itens.adicionar(Item(produto, quantidade))

    def tem_itens(self):
        return self.itens.tem_itens()

    def total(self):
        return self.itens.total()

    def esta_aberto(self):
        return self.status.esta_aberto()

    def esta_pago(self):
        return self.status.esta_pago()

    def pagar(self):
        if self.status.esta_aberto():
            if self.itens.tem_itens():
                self.status = Status("P")
                return True
            else:
                return False
        else:
            return False

    def cancelar(self):
        if self.status.esta_aberto():
            self.status = Status("C")
            return True
        else:
            return False

    def imprimir(self):
        print("  status:", self.status.texto())
        self.itens.imprimir()


class Pedido:
    def __init__(self, numero, cliente):
        self.cabecalho = CabecalhoDoPedido(numero, cliente)
        self.andamento = Andamento(ItensDoPedido(), Status("A"))

    def adicionar_item(self, produto, quantidade):
        self.andamento.adicionar_item(produto, quantidade)

    def total(self):
        return self.andamento.total()

    def desconto(self):
        total = self.total()
        return self.cabecalho.desconto_sobre(total)

    def valor_a_pagar(self):
        total = self.total()
        desconto = self.desconto()
        return total.subtrair(desconto)

    def esta_aberto(self):
        return self.andamento.esta_aberto()

    def esta_pago(self):
        return self.andamento.esta_pago()

    def pagar(self):
        return self.andamento.pagar()

    def cancelar(self):
        return self.andamento.cancelar()

    def imprimir(self):
        self.cabecalho.imprimir()
        self.andamento.imprimir()
        self.imprimir_resumo()

    def imprimir_resumo(self):
        if self.andamento.tem_itens():
            total = self.total()
            desconto = self.desconto()
            a_pagar = self.valor_a_pagar()
            print("  total: R$ %s | desconto: R$ %s | a pagar: R$ %s" % (total.texto(), desconto.texto(), a_pagar.texto()))


class Pedidos:
    def __init__(self):
        self.lista = []

    def adicionar(self, pedido):
        self.lista.append(pedido)

    def arrecadado(self):
        soma = Dinheiro(0)
        for pedido in self.lista:
            if pedido.esta_pago():
                soma = soma.somar(pedido.valor_a_pagar())
        return soma

    def quantidade_de_abertos(self):
        contagem = 0
        for pedido in self.lista:
            if pedido.esta_aberto():
                contagem = contagem + 1
        return contagem

    def relatorio(self):
        for pedido in self.lista:
            pedido.imprimir()


pedidos = Pedidos()           # todos os pedidos da loja


def novo_pedido(numero, cliente):
    resultado = cliente.validar()
    if resultado != "ok":
        print("pedido", numero, "recusado:", resultado)
        return None
    else:
        pedido = Pedido(numero, cliente)
        pedidos.adicionar(pedido)
        return pedido


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
pedido_ana_1.adicionar_item(caderno, 2)
pedido_ana_1.adicionar_item(caneta, 5)

novo_pedido(2, bruno)

pedido_ana_3 = novo_pedido(3, ana)
pedido_ana_3.adicionar_item(livro, 1)

novo_pedido(4, carla)

pedido_diego = novo_pedido(5, diego)

pedido_eva = novo_pedido(6, eva)
pedido_eva.adicionar_item(fone, 1)

novo_pedido(7, fabio)

pedido_gil = novo_pedido(8, gil)
pedido_gil.adicionar_item(fone, 2)

print("pagar 1:", pedido_ana_1.pagar())
print("pagar 3:", pedido_ana_3.pagar())
print("pagar 5:", pedido_diego.pagar())
print("pagar 6:", pedido_eva.pagar())
print("cancelar 5:", pedido_diego.cancelar())
print("cancelar 1:", pedido_ana_1.cancelar())

pedidos.relatorio()
total_arrecadado = pedidos.arrecadado()
print("arrecadado: R$ %s" % total_arrecadado.texto())
print("abertos:", pedidos.quantidade_de_abertos())
# TF 11 - A loja feia

Refatoração do `loja_feia.py` seguindo o Object Calisthenics, sem mudar o que o programa imprime. A cada passo rodei o programa e comparei a saída com `saida_original.txt` usando `diff`. Um commit por passo.

## Passos (commits)

| Passo | O que foi feito |
|---|---|
| 0 | Código original e saída de referência |
| 1 | Nomes sem abreviar |
| 2 | Normalização: classe `Cliente` |
| 3 | Normalização: classe `Produto` |
| 4a | Primitivos: `Cpf`, `Email`, `Cep` |
| 4b | Primitivos: `Dinheiro` |
| 4c | Primitivos: `Status` |
| 5 | Coleções de primeira classe: `ItensDoPedido`, `Pedidos` |
| 6 | Entidades pequenas (até 2 variáveis por classe) |
| 7 | Lei de Demeter e diga, não pergunte |
| 8 | Sem `else`: fail first e polimorfismo |

## Normalização

Antes, cada pedido carregava uma cópia de todos os dados do cliente (a Ana aparecia duas vezes com tudo repetido) e o preço do produto era digitado em cada item (o "Fone" tinha `60.0` escrito duas vezes). Agora o cliente é cadastrado uma vez e os pedidos apontam para ele, e o produto é cadastrado uma vez com o seu preço e os itens apontam para ele. Cada dado mora em um lugar só.

## Tipos primitivos

Antes, CPF, e-mail, CEP e status eram `str` soltos, e o dinheiro era um `float` solto, com as regras espalhadas pelo código. Agora cada um virou uma classe com a regra dentro:

- `Cpf`, `Email` e `Cep`: sabem se são válidos
- `Dinheiro`: sabe somar, subtrair, multiplicar e calcular percentual
- `StatusAberto`, `StatusPago` e `StatusCancelado`: no lugar das letras "A", "P" e "C"
- `TipoNormal`, `TipoVip` e `TipoFuncionario`: no lugar das letras "N", "V" e "F", cada um sabe o seu desconto

## Modularização (uma linha por classe)

| Classe | Responsabilidade |
|---|---|
| `Cpf` | Guarda o CPF e diz se tem 11 dígitos |
| `Email` | Guarda o e-mail e diz se tem conteúdo e arroba |
| `Cep` | Guarda o CEP e diz se tem 8 dígitos |
| `Dinheiro` | Valor em reais com as contas (somar, subtrair, multiplicar, percentual) |
| `StatusAberto` | Estado "aberto" do pedido |
| `StatusPago` | Estado "pago" do pedido |
| `StatusCancelado` | Estado "cancelado" do pedido |
| `TipoNormal` | Cliente comum, sem desconto |
| `TipoVip` | Cliente VIP, desconto de 10% |
| `TipoFuncionario` | Funcionário, desconto de 20% |
| `Perfil` | Nome e tipo do cliente |
| `Contato` | CPF e e-mail, e a validação dos dois |
| `Identidade` | Junta o perfil e o contato |
| `Localidade` | Cidade e CEP, e a validação do CEP |
| `Endereco` | Rua e localidade |
| `Cliente` | Junta a identidade e o endereço |
| `Produto` | Nome e valor unitário |
| `Item` | Um produto com a quantidade e o subtotal |
| `ItensDoPedido` | Coleção de itens, soma o total |
| `CabecalhoDoPedido` | Número do pedido e o cliente |
| `Andamento` | Itens e status, e as ações de pagar e cancelar |
| `Pedido` | Junta o cabeçalho e o andamento, calcula desconto e valor a pagar |
| `Pedidos` | Coleção de pedidos, relatório, arrecadado e quantidade de abertos |

## Dívida técnica que sobrou

- `Dinheiro` usa `float`, que pode dar erro de arredondamento. O certo seria guardar em centavos (`int`) ou usar `Decimal`.
- `nome_texto()` e `cidade_texto()` são getters disfarçados, criados só para conseguir imprimir.
- Várias classes (`Identidade`, `Endereco`, `Cliente`) só repassam chamadas para a classe de dentro. Isso é efeito colateral do limite de 2 variáveis.
- A validação devolve textos como `"ok"` e `"cpf invalido"`. Isso ainda é obsessão por primitivos, o ideal seria um tipo de resultado.
- A validação do CPF só confere o tamanho, não calcula os dígitos verificadores.
- A função `novo_pedido` e a variável global `pedidos` continuam soltas no arquivo.
- Está tudo em um arquivo só, daria para separar em módulos.
- Não há testes automatizados, a única rede de segurança foi o `diff` da saída.
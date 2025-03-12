import ply.lex as lex
import json
import sys

class item:
    def __init__(self, cod, name, quant, preco):
        self.cod = cod
        self.name = name
        self.quant = quant
        self.preco = preco

    def __repr__(self): 
        return f"  {self.cod}  | {self.name} |  {self.quant}  |  {self.preco}"

def load_Stock(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            stock_items = data.get("stock", [])

            stock_dict = {item_data["cod"]: item(
                cod=item_data["cod"],
                name=item_data["nome"],
                quant=item_data["quant"],
                preco=item_data["preco"]
            ) for item_data in stock_items}

            return stock_dict
        
    except FileNotFoundError:
        print(f"Error: O ficheiro '{file}' não existe.")

def save_Stock(file, stock_dict):
    try:
        stock_items = [{
            "cod": item_obj.cod,
            "nome": item_obj.name,
            "quant": item_obj.quant,
            "preco": item_obj.preco
        } for item_obj in stock_dict.values()]
        
        data = {"stock": stock_items}
        
        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"Stock armazenado no ficheiro '{file}'")
    except Exception as e:
        print(f"Erro a guardar o stock: {e}")

Moedas = {
    "2e": 2,
    "1e": 1,
    "50c": 0.5,
    "20c": 0.2,
    "10c": 0.1,
    "5c": 0.05
}

Notas = {
    "5e": 5,
    "10e": 10
}

tokens = (
    'LISTAR',
    'DEPOSITAR',
    'MOEDA',
    'NOTA',
    'VALOR',
    'SELECIONAR',
    'PRODUTO',
    'SAIR',
    'REABASTECER',
    'ADICIONAR',
    'QUANTIDADE',
    'NOME',
    'PRECO',
    'VIRGULA',
    'PONTO',
    'skip'
)

def t_LISTAR(t):
    #r'(?i)listar'
    r'LISTAR'
    return t

def t_DEPOSITAR(t):
    #r'(?i)depositar'
    r'DEPOSITAR'
    return t
#(?i)moeda[ \d+\w+\,]+ \d+\w+ \.
def t_MOEDA(t):
    #r'(?i)^moeda'
    r'MOEDA'
    return t
#(?i)nota[\ \d+\w+\,]+ \d+\w+ \.
def t_NOTA(t):
    #r'(?i)^nota'
    r'NOTA'
    return t

def t_VALOR(t):
    r'\d+\w+'
    return t 

def t_SELECIONAR(t):
    #r'(?i)^selecionar'
    r'SELECIONAR'
    return t

def t_PRODUTO(t):
    r'\w\d+'
    return t

def t_SAIR(t):
    #r'(?i)^sair'
    r'SAIR'
    return t

def t_REABASTECER(t):
    #r'(?i)^reabastecer'
    r'REABASTECER'
    return t

def t_QUANTIDADE(t):
    r'(?<![\.\w])\d+(?![\.\w])'
    return t

def t_ADICIONAR(t):
    r'ADICIONAR'
    return t

def t_NOME(t):
    r'[\w\ ]+\d+[mg][l]?'
    return t

def t_PRECO(t):
    r'\d+\.\d{2}'
    return t

def t_VIRGULA(t):
    r'\,'
    return t

def t_PONTO(t):
    r'(?<!\d)\.'
    return t

def t_skip(t):
    r'[ \t\n]+'
    pass

def t_error(t):
    print(f"maq: Caractere inválido: '{t.value[0]}' na posição {t.lexpos}")
    t.lexer.skip(1)  

t_ignore = ' \t\n'


def listar_produtos(stock):
    print("maq: ")
    print(f"{'Código':<8} | {'         Nome':<25} | {'Quantidade':<10} | {'Preço':<6}")
    if stock:
        for cod, item in stock.items():
            print(f"{item.cod:<8} | {item.name:<25} | {item.quant:<10} | {item.preco:<6.2f}")

def atualiza_saldo(deposito, saldo_atual):
    return saldo_atual + deposito

def depositar_dinheiro(lexer):
    deposito = 0 
   
    for token in lexer:
        if token.type == "MOEDA":
            for token in lexer:
                if token.type == "VALOR":
                    moeda = token.value.lower()
                    if moeda in Moedas:
                        deposito += Moedas[moeda]
                    else:
                        print(f"maq: Moeda inválida: {moeda}")
                elif token.type == "PONTO":
                    break
        elif token.type == "NOTA":
            for token in lexer:
                if token.type == "VALOR":
                    nota = token.value.lower()
                    if nota in Notas:
                        deposito += Notas[nota]
                    else:
                        print(f"maq: Nota inválida: {nota}")
                elif token.type == "PONTO":
                    break
            
    return deposito

def selecionar_item(lexer, stock, saldo_atual):
    codigo = None

    for token in lexer:
        if token.type == 'PRODUTO':
            codigo = token.value
            break

    if not codigo:
        print("maq: Produto inválido, selecione um dos produtos disponíveis:")
        listar_produtos(stock)
        return saldo_atual
    
    item = stock.get(codigo)

    if not item:
            print("maq: Produto inválido, selecione um dos produtos disponíveis:")
            listar_produtos(stock)
            return saldo_atual

    print(f"maq: Produto selecionado: {item}")

    preco = item.preco
    if saldo_atual < preco:
        print(f"maq: Saldo insuficiente para comprar {item.name}. Preço: {preco}€. Saldo disponível: {saldo_atual:.2f}€. ")
        return saldo_atual
    
    if item.quant > 0:
        item.quant -= 1
        saldo_atual -= preco
        print(f"maq: {item.name} comprado com sucesso. Novo saldo: {saldo_atual:.2f}€.")
        print(f"maq: Quantidade restante de {item.name}: {item.quant}")
    else:
        print(f"maq: Erro: {item.name} fora de stock.")
    
    return saldo_atual

def reabastecer_maquina(lexer, stock):
    produto = None
    for token in lexer:
        if token.type == 'PRODUTO':
            codigo = token.value
            produto = stock.get(codigo)
            if not produto:
                print(f"maq: Produto {codigo} não encontrado.")
                continue 

        if token.type == "QUANTIDADE":
            if token.type == "QUANTIDADE":
                if produto:  
                    if not token.value.isdigit():
                        print(f"maq: Quantidade inválida: '{token.value}' não é um número inteiro.")
                    else:
                        quantidade = int(token.value)
                        produto.quant += quantidade
                        print(f"maq: Produto {produto.name} reabastecido com sucesso. Nova quantidade: {produto.quant}")
                produto = None

        if token.type == 'PONTO':
            break

def adicionar_maquina(lexer, stock):
    produto = None
    codigo = None
    nome = None
    quantidade = None
    preco = None

    for token in lexer:
        #print(f"Token: {token.type} -> {token.value}")
        if token.type == 'PRODUTO':
            codigo = token.value
            produto = stock.get(codigo)
            if produto:
                print(f"maq: Já existe um produto com o código {codigo}, por favor tente outro.")
                return
        if token.type == "NOME":
            nome = token.value
        if token.type == "QUANTIDADE":
            quantidade = int(token.value)
        if token.type == "PRECO":
            preco = float(token.value)
            break 
    
    if codigo and nome and quantidade and preco and not produto:
        produto = item(codigo, nome, quantidade, preco)
        print("maq: Novo produto adicionado ", produto)
        stock[codigo] = produto
    else:
        print("maq: Falha ao adicionar produto. Verifique os dados e tente novamente.")
        
def main():
    machine_stock_file = r'bd/stock.json'
    stock_data = []
    saldo_atual = 0

    try:
        stock_data = load_Stock(machine_stock_file)
        listar_produtos(stock_data)

        print("maq: Pretende dar reset ao stock da máquina para o default(s|n)?")
        reset = input(">> ").lower()

        if reset == "s":
            for item in stock_data.values():
                item.quant = 10
            listar_produtos(stock_data)

        start_machine = True
        lexer = lex.lex()
        while start_machine:
            print("maq: Selecione um comando(SAIR | LISTAR | SELECIONAR | DEPOSITAR | REABASTECER | ADICIONAR):")
            command = input(">> ")
            lexer.input(command)
            token = lexer.token()

            if token is None:
                print("maq: Comando inválido")
                continue

            if token.type == "SAIR":
                start_machine = False

            if token.type == "LISTAR":
                listar_produtos(stock_data)

            if token.type == "DEPOSITAR":
                print("maq: Aceitam se Notas de 5 ou 10(ex: NOTA 5e, 10e .) e Moedas entre 5c e 2e(ex: MOEDA 1e, 50c .):")
                command = input(">> ")
                lexer.input(command)
                deposito = depositar_dinheiro(lexer)
                saldo_atual = atualiza_saldo(deposito, saldo_atual)
                print(f"maq: Saldo Atual: {saldo_atual:.2f}€")
            
            if token.type == "SELECIONAR":
                saldo_atual = selecionar_item(lexer, stock_data, saldo_atual)

            if token.type == "REABASTECER":
                print("maq: Liste os produtos que pretende reabastecer na máquina e a sua quantidade (ex A10 5, B12 4 .):")
                command = input(">> ")
                lexer.input(command)
                reabastecer_maquina(lexer, stock_data)

            if token.type == "ADICIONAR":
                print("maq: Adicione um novo produto(ex C10 Bolo de Bolacha 250g 5 2.00):")
                print("maq: Atenção é necessário dar o nome do item no formato: Nome tamanho(ml|g)")
                print("maq: Atenção é necessário especificar as 2  casas decimais no preço: 1.00")
                command = input(">> ")
                lexer.input(command)
                adicionar_maquina(lexer, stock_data)

        print("maq: Pretende guardar as mudanças feitas no estado da máquina(s|n)?")
        save = input(">> ").lower()
        if save == "s":
            save_Stock(machine_stock_file, stock_data)
    except Exception as e:
        print(f"{e}")

if __name__ == "__main__":
    main()
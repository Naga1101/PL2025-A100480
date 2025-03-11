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
    'VIRGULA',
    'PONTO',
    'SELECIONAR',
    'PRODUTO',
    'SAIR',
    'REABASTECER',
    'ITEM',
    'QUANTIDADE',
    'skip'
)

def t_LISTAR(t):
    #r'(?i)^listar'
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

def t_VIRGULA(t):
    r'\,'
    return t

def t_PONTO(t):
    r'\.'
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

def t_ITEM(t):
    #r'(?i)^item'
    r'ITEM'
    return t

def t_QUANTIDADE(t):
    r'\d+'
    return t

def t_skip(t):
    r'[ \t\n]+'
    pass

t_ignore = ' \t\n'


def listar_produtos(stock):
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
            moeda = token.value.lower()
            if moeda in Moedas:
                deposito += Moedas[moeda]
            else:
                print(f"Moeda inválida: {moeda}")
        elif token.type == "NOTA":
            nota = token.value.lower()
            if nota in Notas:
                deposito += Notas[nota]
            else:
                print(f"Nota inválida: {nota}")
    
    return deposito

def selecionar_item(lexer, stock, saldo_atual):
    codigo = None

    for token in lexer:
        if token.Type == 'Produto':
            item_code = token.value
            break

    if not codigo:
        print("Produto inválido, selecione um dos produtos disponíveis:")
        listar_produtos(stock)
        return saldo_atual
    
    item = stock.get(codigo)

    if not item:
            print("Produto inválido, selecione um dos produtos disponíveis:")
            listar_produtos(stock)
            return saldo_atual

    print(f"Produto selecionado: {item}")

    preco = item.preco
    if saldo_atual < preco:
        print(f"Saldo insuficiente para comprar {item.name}. Preço: {preco}€. Saldo disponível: {saldo_atual:.2f}€. ")
        return saldo_atual
    
    if item.quant > 0:
        item.quant -= 1
        print(f"{item.name} comprado com sucesso. Novo saldo: {saldo_atual:.2f}€.")
        print(f"Quantidade restante de {item.name}: {item.quant}")
    else:
        print(f"Erro: {item.name} fora de stock.")
    
    return saldo_atual

def main():
    machine_stock_file = r'bd/stock.json'
    stock_data = []
    saldo_atual = 0

    try:
        stock_data = load_Stock(machine_stock_file)
        listar_produtos(stock_data)

        start_machine = True
        lexer = lex.lex()
        while start_machine:
            command = input(">> ")
            lexer.input(command)
            token = lexer.token()

            if token is None:
                print("Comando inválido")
                continue

            if token.type == "SAIR":
                start_machine = False

            if token.type == "LISTAR":
                listar_produtos(stock_data)

            if token.type == "DEPOSITAR":
                print("Aceitam se Notas de 5 ou 10(ex: NOTA 5e, 10e .) e Moedas entre 5c e 2e(ex: MOEDA 1e, 50c .)")
                deposito = depositar_dinheiro(lexer)
                saldo_atual = atualiza_saldo(deposito, saldo_atual)
                print(f"Saldo Atual: {saldo_atual:.2f}€")
            
            if token.type == "SELECIONAR":
                saldo_atual = selecionar_item(lexer, stock_data, saldo_atual)

        save_Stock(machine_stock_file, stock_data)
    except Exception as e:
        print(f"{e}")

if __name__ == "__main__":
    main()
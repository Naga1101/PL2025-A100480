import ply.yacc as yacc
import ply.lex as lex

# Gramática do Lexer

tokens = (
    'LPAREN',
    'NUM',
    'MULT',
    'DIV',
    'PLUS',
    'MINUS',
    'RPAREN'
)

def t_LPAREN(t):
    r'\('
    return t

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_MULT(t):
    r'\*'
    return t

def t_DIV(t):
    r'/'
    return t

def t_PLUS(t):
    r'\+'
    return t

def t_MINUS(t):
    r'\-'
    return t

def t_RPAREN(t):
    r'\)'
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# Gramática do Parser

"""
P1: InitExpr --> ' ' | '(' Var1
P2: Var1 --> num PriExpr | BasicExpr | FimExpr | ' '
P3: PriExpr --> * | / Var2 | InitExpr
P4: Var2 --> num FimExpr | ' ' | BasicExpr | PriExp
P5: BasicExpr --> + | - Var | ' ' | InitExpr
P6: FimExpr --> ) BasicExpr | PriExpr | ' '
"""

# Token a ser processado
next_token = None

def get_token():
    global next_token
    next_token = lexer.token()
    # print(next_token)

# P1: InitExpr --> ' ' | '(' Var1
def r_init_expr():
    # print("r_init_expr")
    global next_token
    if next_token.type == 'LPAREN':
        get_token()
        result = r_var1()
        if next_token == None or next_token.type != 'RPAREN':
            if result == ')':
                raise SyntaxError("Empty Expression")
            else:
                raise SyntaxError("Expected closing parenthesis ')'")
        
        result = r_fim_expr(result)
        return result
    elif next_token.type == 'NUM':
        return r_var1()
    else:
        raise SyntaxError("Unexpected token in InitExpr")
    
# P2: Var1 --> num PriExpr | BasicExpr | Fim
def r_var1():
    # print("r_var1")
    global next_token
    num = next_token.value
    get_token()
    if next_token is None or next_token.type == 'RPAREN':
        return num
    
    if next_token.type in ('DIV', 'MULT'):
        return r_pri_operation(num)
    elif next_token.type in ('PLUS', 'MINUS'):
        return num + r_basic_operation()
    else:
        raise SyntaxError("Number must be followed by a valid operation!")
    

# P3: PriExpr --> * | / Var2 | InitExpr
def r_pri_operation(value):
    # print("r_pri_operation ")
    global next_token
    op = next_token.type
    get_token()  
    if op in ('MULT', 'DIV') and next_token.type == 'NUM':
        return r_var2(op, value)
    else:
        if op == 'MULT':
            result = value * r_init_expr()
        else:
            result = value / r_init_expr()
        return result

# P4: Var2 --> num Fim | BasicExpr | PriExp
def r_var2(op, value):
    # print("r_var2")
    global next_token
    if next_token.type == 'NUM':
        num = next_token.value
        get_token()
        if op == 'MULT':
            value *= num
        elif op == 'DIV':
            value /= num
    else:
        raise SyntaxError("Unexpected token in Var2")
    
    if next_token != None:
        if next_token.type in ('MULT', 'DIV'):
            op = next_token.type
            get_token()  
            return r_var2(op, value)
        elif next_token.type in ('PLUS', 'MINUS'):
            result = r_basic_operation()
            result += value
            return result
        elif next_token.type == 'RPAREN':
            return value
    return value

# P5: BasicExpr --> + | - Var | Fim | InitExpr
def r_basic_operation():
    # print("r_basic_operation")
    global next_token
    if next_token.type in ('PLUS', 'MINUS'):
        op = next_token.type
        get_token()
        if next_token != None and next_token.type in ('NUM', 'LPAREN'):
            if next_token.type == 'LPAREN':
                result = r_init_expr()
            else:
                result = r_var1() 
            if op == 'PLUS':
                return result
            elif op == 'MINUS':
                return -result
            return +result 
        else:
            raise SyntaxError("Expected a number, '(' or end of expression after operator")
    
    return r_pri_operation(0)

# P6: FimExpr --> ) BasicExpr | PriExpr | Fim
def r_fim_expr(value):
    # print("r_fim_expr")
    global next_token
    get_token()
    if next_token != None:
        if next_token.type in ('PLUS', 'MINUS'):
            return value + r_basic_operation()
        elif next_token.type in ('MULT', 'DIV'):
            return r_pri_operation(value)
        else:
            return value
    return value

def parse(expression):
    global next_token
    lexer.input(expression)
    get_token()
    result = r_init_expr()

    if next_token is not None:
        print(f"Remaining token after parsing: {next_token}")
        raise SyntaxError("Unexpected tokens remaining after parsing")
    return result

def main():
    while True:
        print("Digite uma expressão para ser calculada ou exit para desligar o programa:")
        command = input("Expressão = ")
        if command == "exit":
            break
        result = parse(command)
        print(f"Result: {result}")
    
if __name__ == '__main__':
    main()

import ply.lex as lex
    
r"""
comentario -> #[^\n]+
variaveis -> \?\w+
select -> select
where -> where
limit -> LIMIT
lBracket -> \{
rBracket -> \}
skip -> '\ '
uri -> \w+\:\w+
dot -> \.
string -> \"[^"]+\"\@\w+
numeric -> \d+
"""

tokens = (
    'comentario',
    'lBracket',
    'rBracket',
    'variavel',
    'numeric',
    'select',
    'string',
    'where',
    'limit',
    'ignore',
    'uri',
    'dot'
)

t_comentario = r'\#[^\n]+'
t_lBracket = r'\{'
t_rBracket = r'\}'
t_variavel = r'\?\w+'
t_numeric = r'\d+'
t_select = r'select'
t_string = r'\"[^"]+\"\@\w+'
t_where = r'where'
t_limit = r'LIMIT'
t_ignore = r' '
t_uri = r'\w+\:\w+'
t_dot = r'\.'

def t_error(t):
    t.lexer.skip(1)

lexer = lex.lex()

def tokenize(code):
    lexer.input(code)
    
    for token in lexer:
        print(token)

def main():
    text = """
    # DBPedia: obras de Chuck Berry
    
    select ?nome ?desc where {
    ?s a dbo:MusicalArtist.
    ?s foaf:name "Chuck Berry"@en .
    ?w dbo:artist ?s.
    ?w foaf:name ?nome.
    ?w dbo:abstract ?desc
    } LIMIT 1000
    """

    tokenize(text)
    

if __name__ == "__main__":
    main()
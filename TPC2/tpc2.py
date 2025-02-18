import re
"""
^([^;]+);([^;]+);([^;]+);([^;]+);([^;]+);([^;]+);([^;]+)$ -> apanha 7 grupos numa linha
       0     1        2          3          4         5      6
csv: (nome)(desc)(anoCriacao)(periodo)(compositor)(duracao)(_id)
data_parsed:((nome)(desc)(anoCriacao)(periodo)(compositor)(duracao)(_id)), ((nome)(desc)(anoCriacao)(periodo)(compositor)(duracao)(_id)), ...

"""
def parse_csv(path):
    with open(path, "r", encoding="utf-8") as file_to_filter:
        text = file_to_filter.read()

    pattern = r'^([^;]+);"([\s\S]*?)";([^;]+);([^;]+);([^;]+);([^;]+);([^;]+)$'

    data_parsed = re.findall(pattern, text, re.MULTILINE | re.DOTALL)

    return data_parsed

def list_compositores(data_parsed):
    compositores = []

    for row in data_parsed:
        if(row[4] not in compositores):
            compositores.append(row[4]) 

    compositores = sorted(compositores)
    print("Lista ordenada alfabeticamente dos compositores musicais")
    print(compositores)
    print()
    

def dist_obras_por_periodo(data_parsed):
    nr_obras_periodo = {}

    for row in data_parsed:
        if row[3] not in nr_obras_periodo:
            nr_obras_periodo[row[3]] = 1
        else:
            nr_obras_periodo[row[3]] += 1
    print("Distribuição das obras por período: quantas obras catalogadas em cada período:")
    print(nr_obras_periodo)
    print()
    
def dict_periodo_listaAlf(data_parsed):
    obras_periodo_catalg = {}

    for row in data_parsed:
        if row[3] not in obras_periodo_catalg:
            obras_periodo_catalg[row[3]] = [row[0]]
        else:
            obras_periodo_catalg[row[3]].append(row[0])

    for key in obras_periodo_catalg:
        obras_periodo_catalg[key] = sorted(obras_periodo_catalg[key])

    print("Dicionário em que a cada período está a associada uma lista alfabética dos títulos das obras: ")
    print(obras_periodo_catalg)
    print()

def main():
    data_parsed = parse_csv(r"TPC2\obras.csv")
    list_compositores(data_parsed)
    dist_obras_por_periodo(data_parsed)
    dict_periodo_listaAlf(data_parsed)

if __name__ == "__main__":
    main()
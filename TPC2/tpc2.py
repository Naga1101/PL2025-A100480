import re

"""
^([^;]+);([^;]+);([^;]+);([^;]+);([^;]+);([^;]+);([^;]+)$ -> apanha 7 grupos numa linha
       0     1        2          3          4         5      6
csv: (nome)(desc)(anoCriacao)(periodo)(compositor)(duracao)(_id)
fields:((nome)(desc)(anoCriacao)(periodo)(compositor)(duracao)(_id)), ((nome)(desc)(anoCriacao)(periodo)(compositor)(duracao)(_id)), ...

"""

with open(r"obras.csv", "r", encoding="utf-8") as file_to_filter:
    text = file_to_filter.read()

pattern = r'^([^;]+);"([\s\S]*?)";([^;]+);([^;]+);([^;]+);([^;]+);([^;]+)$'

fields = re.findall(pattern, text, re.MULTILINE | re.DOTALL)

compositores = []

for row in fields:
    if(row[4] not in compositores):
        compositores.append(row[4]) 

compositores = sorted(compositores)
print(compositores)

###

nr_obras_periodo = {}

for row in fields:
    if row[3] not in nr_obras_periodo:
        nr_obras_periodo[row[3]] = 1
    else:
        nr_obras_periodo[row[3]] += 1
print(nr_obras_periodo)

###

obras_periodo_catalg = {}

for row in fields:
    if row[3] not in obras_periodo_catalg:
        obras_periodo_catalg[row[3]] = [row[0]]
    else:
        obras_periodo_catalg[row[3]].append(row[0])

for key in obras_periodo_catalg:
    obras_periodo_catalg[key] = sorted(obras_periodo_catalg[key])

print(obras_periodo_catalg)
# PL2025
## Aluno

**Nome:**  Nuno Aguiar

**Número:**  A100480

**Email:** a100480@alunos.uminho.pt

## Objetivo

Construir um programa que simule uma máquina de vending.
A máquina tem stock de produtos armazenado num json com o formato seguinte: 
```
stock = [
    {
        "cod": "A23", 
        "nome": "água 0.5L", 
        "quant": 8, 
        "preco": 0.7
    },
]```
E os comandos implementados foram os seguintes:
- **LISTAR:** Demonstra uma lista com os itens que existem de momento no stock da máquina;
- **DEPOSITAR:** Comando utilizado para inserir dinheiro na máquina, sendo que as opções e depósito são demonstradas no ecrã;
- **SELECIONAR:** Seleciona e compra o item pretendido;
- **REABASTECER:** Incrementa a quantidade dos itens existentes na máquina através de uma lista inserida pelo utilizador;
- **ADICIONAR:** Adiciona um novo item à máquina inserido pelo utilizador;
- **SAIR:** Desliga a máquina dando a opção de guardar o estado atual da mesma no ficheiro json do stock.
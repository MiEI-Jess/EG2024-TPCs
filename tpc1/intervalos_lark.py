from lark import Lark
from lark.tree import pydot__tree_to_png

grammar = '''
// Regras Sintaticas
start: sentido intervalos
sentido: MAIS
       | MENOS
intervalos : intervalo (intervalo)*
intervalo : PE NUMERO VIR NUMERO PD

// Regras Lexicográficas
NUMERO:/-?\d+/
MAIS: "+"
MENOS: "-"
PE:"["
PD:"]"
VIR:","

// Tratamento dos espaços em branco
%import common.WS
%ignore WS
'''

frase = "-[-3,0][1,23][25,64]"

p = Lark(grammar)

tree = p.parse(frase)
print(tree)
print(tree.pretty())
pydot__tree_to_png(tree,'lark_test.png')

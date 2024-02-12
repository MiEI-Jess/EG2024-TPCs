# ------------------------------------------------------------
# TPC1 : Intervalos (definição sintática)
#  + [100,200][3,12]
#  + [-4,-2][1,2][3,5][7,10][12,14][15,19]
#  - [19,15][12,6][-1,-3]
#  - [1000,200][30,12]
# ------------------------------------------------------------

import sys
import ply.yacc as yacc
from intervalos_lex import tokens

# The set of syntatic rules
def p_sequencia(p):
    "sequencia : sentido intervalos"
    p[0] = p[1]
    print(f"Intervalos: {p[0]}")

def p_sentidoA(p):
    "sentido : '+'"
    parser.sentido = True

def p_sentidoD(p):
    "sentido : '-'"
    parser.sentido = False

def p_intervalos_intervalo(p):
    "intervalos : intervalo"
    p[0] = p[1]

def p_intervalos_intervalos(p):
    "intervalos : intervalos intervalo"
    p[0] = p[1] + p[2]

def p_intervalo(p):
    "intervalo : '[' NUM ',' NUM ']'"
    if parser.sentido:
        if parser.anterior:
            if parser.anterior >= p[2]:
                parser.succes = False
        else:
            parser.first = p[2]
        
        if p[2] >= p[4]:
            p[0]= 0
            parser.succes = False
        else:
            p[0] = 1
            parser.anterior = p[4]
    else:
        if parser.anterior:
            if parser.anterior <= p[2]:
                parser.succes = False
        else:
            parser.first = p[2]
        
        if p[2] <= p[4]:
            p[0] = 0
            parser.succes = False
        else:
            p[0] = 1
            parser.anterior = p[4]

    

                
    #nr_intervalos +=1
    #comprimento = abs(p[4] - p[2])
    #comprimentos.append(comprimento)
    #intv_mais_longo = max(intv_mais_longo, comprimento)
    #intv_mais_curto = min(intv_mais_curto, comprimento)



# Syntatic Error handling rule
def p_error(p):
    print('Syntax error: ', p)
    parser.success = False

# Build the parser
parser = yacc.yacc()
parser.anterior = None
parser.sentido = True
parser.first = None
parser.amplitude = 0

# Start parsing the input text
for line in sys.stdin:
    parser.success = True
    parser.flag = True
    parser.last = 0
    parser.parse(line)

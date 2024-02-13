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
from textwrap import dedent # remove indent

# The set of syntatic rules
def p_sequencia(p):
    "sequencia : sentido intervalos"
    if parser.success:
        output = f"""
                Número de intervalos: {parser.count}
                Comprimento de cada intrervalo: {p[2]}
                Intervalo mais longo: {max(p[2])}
                Intervalo mais curto: {min(p[2])}
                Amplitude: {parser.amplitude}"""
        p[0] = dedent(output)
    else:
        p[0] = "Erro no formato, por favor corrige"
    print(p[0])

def p_sentidoA(p):
    "sentido : '+'"
    parser.flag = True

def p_sentidoD(p):
    "sentido : '-'"
    parser.flag = False

def p_intervalos_intervalo(p):
    "intervalos : intervalo"
    p[0] = [p[1]]

def p_intervalos_intervalos(p):
    "intervalos : intervalos intervalo"
    p[1].append(p[2])
    p[0] = p[1]


def p_intervalo(p):
    "intervalo : '[' NUM ',' NUM ']'"
    if parser.last:
        if parser.flag:
            if not (p[2] < p[4] and p[2] > parser.last):
                parser.success = False
        else:
            if not (p[2] > p[4] and p[2] < parser.last):
                parser.success = False
    else:
        parser.first = p[2] 
        
        if parser.flag:
            if not (p[2] < p[4]):
                parser.success = False
        else:
            if not (p[2] > p[4]):
                parser.success = False
    
    parser.last = p[4]
    parser.amplitude = abs(p[4] - parser.first)
    parser.count += 1
    p[0] = abs(p[2] - p[4])


# Syntatic Error handling rule
def p_error(p):
    print('Syntax error: ', p)
    parser.success = False

# Build the parser
parser = yacc.yacc()

# Start parsing the input text
for line in sys.stdin:
    parser.success = True
    parser.flag = True
    parser.last = None
    parser.first = None
    parser.count = 0
    parser.amplitude = 0
    parser.parse(line)

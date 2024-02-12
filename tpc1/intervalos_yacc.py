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
    if parser.success:
        p[0] = f"""
                Número de intervalos: {parser.count}
                Comprimento de cada intrervalo: {p[2]}
                Intervalo mais longo: {max(p[2])}
                Intervalo mais curto: {min(p[2])}
                Amplitude: {parser.amplitude}
                """
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
            if p[2] < p[4] and p[2] > parser.last:
                parser.last = p[4]
                parser.amplitude = abs(p[4] - parser.first)
                parser.count += 1
                p[0] = abs(p[2] - p[4])
            else:
                parser.success = False
        else:
            if p[2] > p[4] and p[2] < parser.last:
                parser.last = p[4]
                parser.amplitude = abs(p[4] - parser.first)
                parser.count += 1
                p[0] = abs(p[2] - p[4])
            else:
                parser.success = False
    else:
        if parser.flag:
            if p[2] < p[4]:
                parser.last = p[4]
                parser.first = p[2]
                parser.amplitude = abs(p[4] - parser.first)
                parser.count += 1
                p[0] = abs(p[2] - p[4])
            else:
                parser.success = False
        else:
            if p[2] > p[4]:
                parser.last = p[4]
                parser.first = p[2]
                parser.amplitude = abs(p[4] - parser.first)
                parser.count += 1
                p[0] = abs(p[2] - p[4])
            else:
                parser.success = False



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

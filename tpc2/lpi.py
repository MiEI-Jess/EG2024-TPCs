from lark import Lark
from lark.tree import pydot__tree_to_png

grammar = """
//Regras Semanticas
start: expressao
expressao: atribuicao 
         | operacao 
         | condicional 
         | ciclo

atribuicao: var "=" [tipo|operacao]
operacao: termo operador termo (operacao)*

condicional: alternativa 
           | casos
alternativa: IF PE condicao PD CE expressao+ CD 
		   | IF PE condicao PD CE expressao+ CD ELSE CE expressao+ CD
casos: "match" PE var PD CE "case" tipo DP expressao* "case" "_" DP expressao* CD

ciclo: enquanto 
     | repete 
     | percorre
enquanto: "while" PE condicao PD CE expressao* CD 
repete: "do" CE expressao* CD "while" PE condicao PD
percorre: "for" var "in" conjunto CE expressao* CD

condicao: int 
        | bool 
        | operacao 
bool: "TRUE" 
    | "FALSE"

int : NUMBER
string: STRING
tuplo: PE tipo [VIR tipo]* PD
array: PRE  PRD 
     | PRE tipo PRD 
     | PRE tipo (VIR tipo)* PRD
lista: PRE PRD 
     | PRE tipo lista PRD
set: CE CD 
   | CE tipo CD 
   | CE tipo VIR set* CD
tipo: int
    | bool 
    | string 
    | tuplo 
    | array 
    | lista 
    | set
var: /[a-zA-Z]\w*/ 

termo: var
     | int
conjunto: array 
        | set 
        | lista
     
operador: "+" 
        | "-" 
        | "*" 
        | "/" 
        | "%" 
        | "==" 
        | "!=" 
        | "<" 
        | ">" 
        | "<=" 
        | ">="
        | "="


//Regras Lexicograficas
DP: ":"
PE: "("
PD: ")"
PRE: "["
PRD: "]"
VIR: ","
CE: "{"
CD: "}"
IF: "if"
ELSE: "else"
CASE: "case"
NUMBER: /\-?\d+/
STRING: /\"\w+\"/

%import common.WS_INLINE
%ignore WS_INLINE
"""

frase = "while(TRUE){x+1}"

p = Lark(grammar)

tree = p.parse(frase)
#print(tree)
print(tree.pretty())
#pydot__tree_to_png(tree,'lark_test.png')
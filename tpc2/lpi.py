from lark import Lark
from lark.tree import pydot__tree_to_png

grammar = """
//Regras Semanticas
start: expressao
expressao: atribuicao 
         | operacao 
         | condicional 
         | ciclo

atribuicao:tipo var "=" [objeto|operacao]
operacao: termo operador termo
        | termo operador (operacao)+ 

condicional: alternativa 
           | casos
alternativa: IF PE condicao PD CE expressao+ CD 
		   | IF PE condicao PD CE expressao+ CD ELSE CE expressao+ CD
casos: "match" PE var PD CE "case" objeto DP expressao* "case" "_" DP expressao* CD

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
string: STR
tuplo: PE objeto [VIR objeto]* PD
array: PRE  PRD 
     | PRE objeto PRD 
     | PRE objeto (VIR objeto)* PRD
lista: PRE PRD 
     | PRE objeto lista PRD
set: CE CD 
   | CE objeto CD 
   | CE objeto VIR set* CD
objeto: int
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
     
operador: PLUS 
        | MINUS 
        | MULT
        | DIV
        | MOD 
        | EQUAL 
        | DIFF 
        | LESS 
        | GREAT 
        | LEQUAL 
        | GEQUAL

tipo: INT
    | BOOL
    | STRING
    | TUPLO 
    | ARRAY 
    | LISTA 
    | SET

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
INT: "int"
BOOL: "bool" 
STRING: "string"
TUPLO: "tuplo" 
ARRAY: "array" 
LISTA: "lista" 
SET: "set"
PLUS: "+" 
MINUS: "-" 
MULT: "*" 
DIV: "/" 
MOD: "%" 
EQUAL: "==" 
DIFF: "!=" 
LESS: "<" 
GREAT: ">" 
LEQUAL:"<=" 
GEQUAL:">="
NUMBER: /\-?\d+/
STR: /\"\w+\"/


%import common.WS_INLINE
%ignore WS_INLINE
"""

frase = "int x = 10 + 23"

p = Lark(grammar)

tree = p.parse(frase)
print(tree)
print(tree.pretty())
pydot__tree_to_png(tree,'lark_test.png')
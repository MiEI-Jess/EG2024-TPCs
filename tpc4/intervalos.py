from lark import Lark
from lark.visitors import Interpreter

grammar1 = '''
// Regras Sintaticas
start: sentido intervalos
sentido: MAIS
       | MENOS
intervalos: intervalo (intervalo)*
intervalo: PE NUM VIR NUM PD

// Regras Lexicográficas
NUM: /-?\d+/
MAIS:"+"
MENOS:"-"
PE:"["
PD:"]"
VIR:","

// Tratamento dos espaços em branco
%import common.WS
%ignore WS
'''

frase0 = "+ [1,2][3,4]" 
frase1 = "- [4,3][2,1]"
frase2 = "+ [10,20][4,3]"
frase3 = "- [3,4][2,1]"
frase4 = "+ [10,20][15,22]"
frase5 = "- [4,2][3,1]"

p = Lark(grammar1) # cria um objeto parser

tree = p.parse(frase2)  # retorna uma tree

print(tree.pretty())

class InterpreterIntervalos(Interpreter):
  def __init__(self):
      self.sinal=True
      self.last = None
      self.error = False

  def start(self, tree):
    self.sinal = self.visit(tree.children[0])
    self.visit(tree.children[1])
    return self.error
    
  
  def sentido(self, tree):
    return tree.children[0] == '+'
  
  def intervalo(self,tree):
    x,y = tree.children[1], tree.children[3]
    
    if not self.error:
      if self.last:
        if self.sinal:
          self.error = (x > y) and (y > self.last)
        else:
          self.error = (x < y) and (y < self.last)
      
      else:
        if self.sinal:
          self.error = x > y
        else:
          self.error = x < y

      self.last = y


data = InterpreterIntervalos().visit(tree)
print(data)
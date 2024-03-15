from lark import Lark,Transformer,Discard
from lark.tree import pydot__tree_to_png

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

tree = p.parse(frase0)  # retorna uma tree

print(tree.pretty())

class TransformerIntervalos(Transformer):
  def __init__(self):
      self.sinal=1
      self.first = None
      self.last = None
      self.valid = True
      self.success = True
      self.error = []
      self.amp_max = None
      self.amps = []

  def start(self,elementos):
    print("start",elementos)
    self.amp_max = abs(self.first - self.last)
    maior = max(self.amps)
    return elementos, self.error, self.amp_max , maior

  def sentido(self,sentido):
    print("sentido",sentido[0].value)
    if sentido[0].value == '-':
      self.sinal=-1
    return Discard

  def intervalos(self,intervalos):
    print("intervalos",intervalos)
    for a,b in intervalos:
      self.amps.append(abs(a-b))
    return intervalos

  def intervalo(self,intervalo):
    print("intervalo",intervalo)
    
    x,y = intervalo

    crescente = self.sinal == 1
    
    #Check intervalo
    self.success = not ((crescente and x >= y) or (not crescente and x <= y))
    
    #Check intervalos anteriores
    if self.success:
      if self.last and crescente:
        self.success = x > self.last
      elif self.last and not crescente:
        self.success = x < self.last
      else:
        self.first = x
      self.last = y
    
    if not self.success:
      self.error.append(intervalo)

    result = intervalo if self.success else Discard
    
    return result

  def NUM (self,numero):
    print("NUM",numero)
    return int(numero)

  def PE(self,pe):
    print("PE",pe)
    return Discard

  def PD(self,pd):
    print("PD",pd)
    return Discard

  def VIR(self,vir):
    print("VIR",vir)
    return Discard

data,erro,amplitude, maior = TransformerIntervalos().transform(tree)
print(f"saida :{data}\nerros :{erro}\namplitude maxima:{amplitude}\nmaior amplitude: {maior}")
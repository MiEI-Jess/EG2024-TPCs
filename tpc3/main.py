from lark import Lark, Transformer, Discard
from lark.tree import pydot__tree_to_png
from statistics import mean
from datetime import date

grammar = """
//Sintaxe
start: turma +
turma: "TURMA" LETRA alunos PON
alunos: aluno (PV alunos)* 
aluno: NOME PE NUMBER (VIR NUMBER)* PD

//Lexicos
LETRA: /[A-Z]/
NOME: /\w+/
NUMBER: /\d+/
PE: "("
PD: ")"
PV: ";"
VIR: ","
PON: "."

%import common.WS
%ignore WS
"""

frase = '''
TURMA A
ana (12, 13, 15, 12, 13, 15, 14);
joao (9,7,3,6,9);
xico (12,16).
TURMA B
ana (12, 13, 15, 12, 13, 15, 14);
joao (9,7,3,6,9,12);
xico (12,16).
'''

p = Lark(grammar)

tree = p.parse(frase)

print(tree.pretty())

class Transformer(Transformer):
    def __init__(self):
        self.num_alunos = 0
        self.current_turma = None
        self.medias = dict()
        self.alunos_notas = dict()
        self.sql_query = """
        INSERT INTO Resultado (nomeAluno, nota, dataInsercao, turma)
        VALUES
        """
        self.markdown = """
# Visualizador de turmas\n
"""

    def start(self,elementos):
        return elementos, self.num_alunos, self.medias, self.alunos_notas, self.sql_query, self.markdown
    
    def turma(self,turma):
        return turma
    
    def alunos(self,alunos):
        return alunos
    
    def aluno(self,aluno):
        alu = aluno[0]
        notas_raw = aluno[1:]
        notas_int = map(int,notas_raw)

        #Aluno counter
        self.num_alunos += 1

        #Media alunos
        media = mean(notas_int)
        aluno_media = self.medias.get(alu, [])
        self.medias[alu] = aluno_media + [media]

        #Alunos por notas
        for n in notas_raw:
            a = self.alunos_notas.get(n,[])
            self.alunos_notas[n] = list(dict.fromkeys(a+[alu])) #remove duplicados

        #SQL Query
        self.sql_query += f"({alu},{notas_raw},{date.today()},{self.current_turma})"

        #Markdown Query
        self.markdown += f"| {alu} | {media} |\n"

        return aluno
    
    def LETRA(self, letra):
        self.current_turma = letra.value
        self.markdown += f"## Turma {self.current_turma}\n### Lista de alunos\n"
        self.markdown += "### Notas\n| Aluno | Media |\n|  --------  |  -------  |\n"
        return letra.value
    
    def NOME(self, nome):
        return nome.value
    
    def NUMBER(self, number):
        return number.value
    
    def PE(self, pe):
        return Discard
    
    def PD(self, pd):
        return Discard
    
    def PV(self, pv):
        return Discard
    
    def VIR(self, vir):
        return Discard
    
    def PON(self, pon):
        return Discard
    
data, num, med, alunot, sql, markd = Transformer().transform(tree)
print(f"saida :{data}")
print(f"Numero de alunos:{num}")
print(f"Medias: {med}")
print(f"Alunos por notas: {alunot}")
print(sql)
print(markd)
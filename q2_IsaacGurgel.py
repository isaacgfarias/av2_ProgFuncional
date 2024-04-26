from q1_IsaacGurgel import *
import threading

##Teste fluxo Cash
teste1 = lambda nome, senha, tipo, valor: True if "transacaoAprovada" in criar_transacao(nome, senha, tipo)(valor) else False
##Teste fluxo Fund Transfer
teste2 = lambda nome, senha, tipo, valor, autorizado, id_do_outro: True if "transacaoAprovada" in criar_transacao(nome, senha,tipo)(valor, autorizado,id_do_outro) else False
##Teste fluxo Credit
teste3 = lambda nome, senha, tipo, valor, autorizado: True if "transacaoAprovada" in criar_transacao(nome, senha, tipo)(valor, autorizado) else False

# Limpando o terminal
os.system('cls' if os.name=='nt' else 'clear')

assert teste1('fulano', '2143','dinheiro', 200)
assert teste2('isaac', '2468','transferência', 500, True, 2)
assert teste3('isaac', '2468','crédito', 500, True)


pbranches = 10000
threads = []
for i in range(pbranches):
    t = threading.Thread(target=verificar_usuario, args=('isaac', '2468'))
    threads.append(t)
    t.start()
for t in threads:
    t.join()
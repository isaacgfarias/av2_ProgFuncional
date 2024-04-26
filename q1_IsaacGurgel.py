import os
import aux_func as aux


detalhes_usuarios = lambda : {
    'isaac': {
        id:1, 
        'saldo_conta': 1000, 
        'senha': '2468', 
        'transacaoAprovada': False
    },
    'fulano': {
        id:2, 
        'saldo_conta': 2500, 
        'senha': '2143', 
        'transacaoAprovada': False
    }
}

usuario_inicial = detalhes_usuarios()
imprimir_texto = lambda texto : print(texto)
verificar_usuario = lambda usuario, senha : usuario in tuple(detalhes_usuarios().keys()) and senha == detalhes_usuarios()[usuario]['senha']
resetar_transacao_usuario = lambda usuario : usuario_inicial[usuario].update({'transacaoAprovada': False})

criar_transacao = lambda usuario, senha, tipo : \
                    (lambda valor : etapas_dinheiro(usuario, valor)) \
                        if verificar_usuario(usuario, senha) and tipo == "dinheiro" \
            else    (lambda valor, aprovado : etapas_credito(usuario, valor, aprovado)) \
                        if verificar_usuario(usuario, senha) and tipo == "crédito" \
            else    (lambda valor, aprovado, idOutro : etapas_transferencia(usuario, valor, aprovado, idOutro)) \
                        if verificar_usuario(usuario, senha) and tipo == "transferência" \
            else    imprimir_texto("Usuário inválido ou senha") or fechar_transacao(usuario, True)

verificar_valor = lambda usuario, valor : True if usuario_inicial[usuario]['saldo_conta'] >= valor else imprimir_texto("Fundos insuficientes") or False
novos_detalhes_conta = lambda usuario : imprimir_texto(f"Novos detalhes da conta: {usuario} saldo da conta: R${usuario_inicial[usuario]['saldo_conta']}")
atualizar_saldo_menos = lambda usuario, valor : usuario_inicial[usuario].update({'saldo_conta': usuario_inicial[usuario]['saldo_conta'] - valor, 'transacaoAprovada': True }) or novos_detalhes_conta(usuario)
atualizar_saldo_mais = lambda usuario, valor : usuario_inicial[usuario].update({'saldo_conta': usuario_inicial[usuario]['saldo_conta'] + valor, 'transacaoAprovada': True }) or novos_detalhes_conta(usuario)
mensagem_transferencia = lambda usuario : "transacaoAprovada" if usuario_inicial[usuario]['transacaoAprovada'] else "Transação não aprovada"

def etapas_dinheiro(usuario, valor):
    imprimir_texto("\nETAPAS POR TRANSAÇ. DINHEIRO:")
    receber_dinheiro(usuario, valor)
    return (mensagem_transferencia(usuario))
    

def etapas_credito(usuario, valor, aprovado):
    imprimir_texto("\nETAPAS DO TRANSAÇ. CRÉDITO:")
    detalhes_conta(usuario)
    solicitar_pagamento(usuario, valor, aprovado)
    fechar_transacao(usuario, False)
    return mensagem_transferencia(usuario)



def etapas_transferencia(usuario, valor, aprovado, idOutro):
    imprimir_texto("\nETAPAS DA TRANSF. BANCÁRIA:")
    fornecer_detalhes_deposito_banco()
    confirmacao_fundos(usuario, valor, aprovado, idOutro)
    fechar_transacao(usuario, False)
    return mensagem_transferencia(usuario)

receber_dinheiro = lambda usuario, valor : imprimir_texto(f"Dinheiro recebido") or atualizar_saldo_menos(usuario, valor) or imprimir_recibo_pagamento(usuario, valor) if verificar_valor(usuario, valor) else fechar_transacao(usuario, True);
imprimir_recibo_pagamento = lambda usuario, valor : imprimir_texto(f"Recibo de pagamento: {usuario} pagou R${valor}") or retornar_recibo_pagamento(usuario);
retornar_recibo_pagamento = lambda usuario : imprimir_texto("Recibo de pagamento retornado") or completar_transacao(usuario);
completar_transacao = lambda usuario : imprimir_texto("Transação concluída") or fechar_transacao(usuario, False); 

detalhes_conta = lambda usuario : imprimir_texto(f"Solicitação de detalhes da conta: {usuario} detalhes da conta: R${usuario_inicial[usuario]['saldo_conta']}")
solicitar_pagamento = lambda usuario, valor, aprovado : imprimir_texto("Pagamento solicitado") or confirmar_pagamento(usuario, valor) if aprovado and verificar_valor(usuario, valor) else cancelar_transacao(usuario); 
confirmar_pagamento = lambda usuario, valor : imprimir_texto("Pagamento confirmado") or atualizar_saldo_mais(usuario, valor);

fornecer_detalhes_deposito_banco = lambda : imprimir_texto("Detalhes do depósito bancário fornecidos");
obter_usuario_por_id = lambda idOutro : [nome for nome, dados in usuario_inicial.items() if dados[id] == idOutro]
transferir_fundo_para_outra_conta = lambda usuario, idOutro, valor : atualizar_saldo_menos(usuario, valor) or atualizar_saldo_mais(obter_usuario_por_id(idOutro)[0], valor) if len(obter_usuario_por_id(idOutro)) > 0 and obter_usuario_por_id(idOutro)[0] != usuario else imprimir_texto("Conta inválida para transferência") or fechar_transacao(usuario, True)
confirmacao_fundos = lambda usuario, valor, aprovado, idOutro : transferir_fundo_para_outra_conta(usuario, idOutro, valor) if aprovado and verificar_valor(usuario, valor) else cancelar_transacao(usuario);

cancelar_transacao = lambda usuario : imprimir_texto("Transação cancelada") or resetar_transacao_usuario(usuario);
fechar_transacao = lambda usuario, controle : imprimir_texto("Transação fechada\n") or resetar_transacao_usuario(usuario) if controle else imprimir_texto("Transação fechada\n")

def interface_interativa():
    usuario = lambda : aux.input_valido(f"Usuarios cadastrados:\n{'\n'.join(n.capitalize() for n in list(detalhes_usuarios().keys()))}\nDigite o nome do usuário: ", list(detalhes_usuarios().keys())).lower()
    senha = lambda : input ( f"pss... as senhas são...\n{ '\n'.join (  [ f'{n}: {detalhes_usuarios()[n]["senha"]}' for n in list ( detalhes_usuarios().keys() ) ] ) }\nDigite a senha do usuário: " )
    tipo = int(aux.input_valido('1 - Dinheiro\n2 - Crédito\n3 - Transferência Bancária\nInsira o tipo da transferência: ', ["1", "2", "3"]))
    valor = lambda : aux.input_apenas_nums("Digite o valor da transação: ")
    if tipo == 1:
        tipo = lambda : "dinheiro"
        criar_transacao(usuario(), senha(), tipo())(valor())
    else :
        aprovado = lambda : aux.input_valido("Confirmar transação? (s/n): ", ["s", "n"]) == "s"
        if tipo == 2:
            tipo = lambda : "crédito"
            criar_transacao(usuario(), senha(), tipo())(valor(), aprovado())
        elif tipo == 3:
            tipo = lambda : "transferência"
            idOutro = lambda : int(input("Digite o ID do outro usuário: "))
            criar_transacao(usuario(), senha(), tipo())(valor(), aprovado(), idOutro())

if __name__=="__main__":
    # Limpando o terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    interface_interativa()


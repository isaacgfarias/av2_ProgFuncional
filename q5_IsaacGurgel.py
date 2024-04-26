##Questão escolhida: 2
## Está sendo feita a criptografia das senhas e a descriptografia das senhas, utilizando a biblioteca Crypto do Python.
## Explicação: se todos os testes passarem, a função retornará a string "Testes foram realizados e passaram com sucesso!"

from q2_IsaacGurgel import *
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad



key = get_random_bytes(16)
iv = get_random_bytes(16)

cipher = AES.new(key, AES.MODE_CBC, iv)
decipher = AES.new(key, AES.MODE_CBC, iv)


lambda_encrypt = lambda password: cipher.encrypt(password)
lambda_decrypt = lambda password: decipher.decrypt(password).decode().strip()

user_dic = lambda : {
    'isaac': {id:1, 'saldo_conta': 5000, 'senha': lambda_encrypt(pad(b'2468', 16)), 'transacaoAprovada': False},
    'fulano': {id:2, 'saldo_conta': 2500, 'senha': lambda_encrypt(pad(b'2143', 16)), 'transacaoAprovada': False}
}

usuarios = user_dic()

senhaIsaac_criptografada = usuarios['isaac']['senha']
senhaFulano_criptografada = usuarios['fulano']['senha']

senhaIsaac_descriptografada = lambda_decrypt(senhaIsaac_criptografada)
senhaFulano_descriptografada = lambda_decrypt(senhaFulano_criptografada)


from flask import Flask
app = Flask('app')

h1 = lambda: "Testes foram realizados e passaram com sucesso!"

@app.route('/')

def hello_world():
    assert teste1('fulano', senhaFulano_descriptografada,'dinheiro', 200)
    assert teste2('isaac', senhaIsaac_descriptografada,'transferência', 500, True, 2)
    assert teste3('isaac', senhaIsaac_descriptografada,'crédito', 500, True)

    return h1()

app.run(host='0.0.0.0', port=5000)
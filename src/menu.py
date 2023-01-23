import os

def initialMenu():
    Kp = 30.0
    Ki = 0.2
    Kd = 400
    print('==========================================================')
    print(f'==== TRABALHO 02 - FUNDAMENTOS DE SISTEMAS EMBARCADOS ====')
    print('==========================================================\n')
    print('VALORES DEFAULT:')
    print('Kp: 30.0')
    print('Ki: 0.2')
    print('Kd: 400\n')
    tipo_de_dados = int(input("DESEJA USAR OS VALORES DEFAULT?\nSIM (1)\nNÃO (2)\n"))
    os.system('clear')
    if tipo_de_dados != 1:
        Kp = float(input("Digite o valor para Kp: "))
        Ki = float(input("Digite o valor para Ki: "))
        Kd = float(input("Digite o valor para Kd: "))
        
    tr_res = float(input("COMO DESEJA OBTER OS VALORES DA TEMPERATURA REFERENCIAL?\nVALOR DEFINIDO PELA UART (1)\nESCOLHER MANUALMENTE (2)\nCURVA REFLOW (3)\n"))

    os.system('clear')
    return Kp, Ki, Kd, tr_res

    

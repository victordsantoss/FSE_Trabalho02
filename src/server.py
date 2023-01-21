# BIBLIOTECAS
import RPi.GPIO as GPIO
import serial
import struct
import time
# MÓDULOS
from gpioConfig import handleGPIOConfig
from crc16 import calcula_CRC
from pid import pid_controle

uart = serial.Serial("/dev/serial0")

# COMANDOS
comandos = {
    "temperatura_interna": b'\x01\x23\xc1\x08\x06\x08\x05',
    "temperatura_referencia": b'\x01\x23\xc2\x08\x06\x08\x05',
    "comandos_dashboard": b'\x01\x23\xc3\x08\x06\x08\x05',
    "atualizar_estado_do_sistema_on": b'\x01\x16\xd3\x08\x06\x08\x05\x01',
    "atualizar_estado_do_sistema_off": b'\x01\x16\xd3\x08\x06\x08\x05\x00',
    "iniciar_aquecimento": b'\x01\x16\xd5\x08\x06\x08\x05\x01',
    "parar_aquecimento": b'\x01\x16\xd5\x08\x06\x08\x05\x00',
    "sinal_de_controle": b'\x01\x16\xd1\x08\x06\x08\x05',
}

dashboard = [
    {
        "funcionalidade": "Ligar Forno",
        "codigo": "0xa1"
    },
    {
        "funcionalidade": "Desligar Forno",
        "codigo": "0xa2"
    },
    {
        "funcionalidade": "Iniciar Aquecimento",
        "codigo": "0xa3"
    },
    {
        "funcionalidade": "Parar Aquecimento",
        "codigo": "0xa4"
    },
]

def handleGetCRC16(comando, tamanho):
    crc_res = calcula_CRC(comando, tamanho).to_bytes(2,'little')
    return crc_res

def handleVerifyCRC16(tamanho_uart, tamanho_crc):
    uart_res = uart.read(tamanho_uart)
    crc_res = handleGetCRC16(uart_res[:-2],tamanho_crc)
    if crc_res == uart_res[-2:]:
        print("UART_RES",uart_res)
        return uart_res
    else:
        handleVerifyCRC16(9, 7)

def handleTemperature(comando_atual):
    crc = handleGetCRC16(comando_atual, 7)
    uart.write(comando_atual + crc)
    temperatura_verificada = handleVerifyCRC16(9, 7)
    temperatura_tratada = struct.unpack("f",temperatura_verificada[3:-2])
    print(temperatura_tratada[0])
    return temperatura_tratada[0]

def handleCommandAction(comando_atual):
    crc = handleGetCRC16(comando_atual, 8)
    uart.write(comando_atual + crc)
    handleVerifyCRC16(9, 7)

def handleUserCommands():
    crc = handleGetCRC16(comandos["comandos_dashboard"], 7)
    uart.write(comandos["comandos_dashboard"] + crc)
    comando_verificado = handleVerifyCRC16(9, 7)
    if str(hex(comando_verificado[3])) == dashboard[0]["codigo"]:
        print("RECEBEU COMANDO DE LIGAR FORNO")
        handleCommandAction(comandos["atualizar_estado_do_sistema_on"])
    if str(hex(comando_verificado[3])) == dashboard[1]["codigo"]:
        print("RECEBEU COMANDO DE DESLIGAR FORNO")
        handleCommandAction(comandos["atualizar_estado_do_sistema_off"])
    if str(hex(comando_verificado[3])) == dashboard[2]["codigo"]:
        print("RECEBEU COMANDO DE INICIAR AQUECIMENTO DO FORNO")
        handleCommandAction(comandos["iniciar_aquecimento"])
    if str(hex(comando_verificado[3])) == dashboard[3]["codigo"]:
        print("RECEBEU COMANDO DE PARAR AQUECIMENTO DO FORNO")
        handleCommandAction(comandos["parar_aquecimento"])

def handleControlSinal(pid_result):
    pid_result = pid_result.to_bytes(4,'little', signed = True)
    aux = comandos["sinal_de_controle"] + pid_result
    crc = handleGetCRC16(aux, len(aux))
    uart.write(aux + crc)
    handleVerifyCRC16(5,3)

def main():
    devices = handleGPIOConfig()
    # TEMPERATURA INTERNA
    temp_interna = handleTemperature(comandos["temperatura_interna"])
    print("temp interna", temp_interna)
    # TEMPERATURA REFERENCIAL
    temp_referencial = handleTemperature(comandos["temperatura_referencia"])
    print("temp referencial", temp_referencial)
    #LEITURA DE COMANDOS DA DASHBOARD
    # while 1:   
    #     handleUserCommands()
    #     time.sleep(1.5)
    
    pid_result = pid_controle(30.0, 0.2, 400, temp_referencial)
    handleControlSinal(int(pid_result))



main()
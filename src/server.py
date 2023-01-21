# BIBLIOTECAS
import RPi.GPIO as GPIO
import serial
import struct
import time
# MÓDULOS
from gpioConfig import handleGPIOConfig
from crc16 import calcula_CRC

uart = serial.Serial("/dev/serial0")

# COMANDOS
comandos = {
    "temperatura_interna": b'\x01\x23\xc1\x08\x06\x08\x05',
    "temperatura_referencia": b'\x01\x23\xc2\x08\x06\x08\x05',
    "comandos_dashboard": b'\x01\x23\xc3\x08\x06\x08\x05',
}

dashboard = [
    {
        "comando": "Ligar Forno",
        "codigo": "0xa1"
    },
    
]



def handleGetCRC16(comando, tamanho):
    crc_res = calcula_CRC(comando, tamanho).to_bytes(2,'little')
    return crc_res

def handleVerifyCRC16(tamanho_uart, tamanho_crc):
    uart_res = uart.read(tamanho_uart)
    crc_res = handleGetCRC16(uart_res[:-2],tamanho_crc)
    if crc_res == uart_res[-2:]:
        return uart_res

def main():
    devices = handleGPIOConfig()
    # TEMPERATURA INTERNA
    crc = handleGetCRC16(comandos["temperatura_interna"], 7)
    uart.write(comandos["temperatura_interna"] + crc)
    temperatura_interna_verificada = handleVerifyCRC16(9, 7)
    temperatura_interna_tratada = struct.unpack("f",temperatura_interna_verificada[3:-2])
    print(temperatura_interna_tratada[0])

    # TEMPERATURA DE REFERENCIA 
    crc = handleGetCRC16(comandos["temperatura_referencia"], 7)
    uart.write(comandos["temperatura_referencia"] + crc)
    temperatura_interna_verificada = handleVerifyCRC16(9, 7)
    temperatura_interna_tratada = struct.unpack("f",temperatura_interna_verificada[3:-2])
    print(temperatura_interna_tratada[0])
    # LER COMANDOS DA DASHBOARD

    print("dasdasdasd", dashboard[0]["codigo"])

    while 1:   
        crc = handleGetCRC16(comandos["comandos_dashboard"], 7)
        uart.write(comandos["comandos_dashboard"] + crc)
        temperatura_interna_verificada = handleVerifyCRC16(9, 7)
        print("mensagem inteira", temperatura_interna_verificada)
        print("mensagem cortada", temperatura_interna_verificada[3])
        print("comando dashboard", dashboard[0]["codigo"])
        print("verificacaao", str(hex(temperatura_interna_verificada[3])) == dashboard[0]["codigo"])

        time.sleep(3.0)

main()
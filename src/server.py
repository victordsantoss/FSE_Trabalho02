import RPi.GPIO as GPIO
import serial

# CONEXÃO COM A UART
uart_connection = serial.Serial("/dev/serial0", baudrate=115200)
print("uart_connection", uart_connection)


def pid_controle(Kp, Ki, Kd, temperatura_referencia, saida_medida):
    sinal_de_controle = 0.0
    T = 1.0;      
    erro_total = 0.0
    erro_anterior = 0.0
    sinal_de_controle_MAX = 100.0
    sinal_de_controle_MIN = -100.0
    erro = temperatura_referencia - saida_medida;
    erro_total += erro;

    if erro_total >= sinal_de_controle_MAX: 
        erro_total = sinal_de_controle_MAX
    
    if erro_total <= sinal_de_controle_MIN:
        erro_total = sinal_de_controle_MIN
    
    delta_error = erro - erro_anterior
    sinal_de_controle = Kp*erro + (Ki*T)*erro_total + (Kd/T)*delta_error;

    if sinal_de_controle >= sinal_de_controle_MAX:
        sinal_de_controle = sinal_de_controle_MAX
    
    if sinal_de_controle <= sinal_de_controle_MIN:
        sinal_de_controle = sinal_de_controle_MIN

    erro_anterior = erro;
    return sinal_de_controle;

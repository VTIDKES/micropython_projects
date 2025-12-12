import network
import time

# Cria instância da interface STA
wlan = network.WLAN(network.STA_IF)

# Ativa a interface
wlan.active(True)

# Conecta à rede Wi-Fi
wlan.connect("ANA_5g", "VI913602")

# Aguarda a conexão ser estabelecida
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('Aguardando conexão...')
    time.sleep(1)

# Verifica se a conexão foi bem sucedida
if wlan.isconnected():
    print("Conectado com sucesso!")
    print('Status:', wlan.status())
    print('IP:', wlan.ifconfig()[0])
else:
    print("Falha na conexão")
    print('Status:', wlan.status())

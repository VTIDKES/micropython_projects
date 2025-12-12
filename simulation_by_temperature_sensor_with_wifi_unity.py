from machine import Pin, PWM, ADC, SoftI2C
import ssd1306
import network
import time
import urequests  # MicroPython HTTP requests

# =========================
# CONFIGURAÇÃO WIFI
# =========================
SSID = "name of wifi"
PASSWORD = "passaword"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# =========================
# CONFIGURAÇÃO DO BUZZER E LEDS
# =========================
LED_VERMELHO = Pin(13 , Pin.OUT)
LED_VERDE = Pin(11, Pin.OUT)
buzzer = PWM(Pin(21))

def som_conexao(duracao=0.2, frequencia=1000):
    buzzer.freq(frequencia)
    buzzer.duty_u16(32768)
    time.sleep(duracao)
    buzzer.duty_u16(0)

# =========================
# CONFIGURAÇÃO DISPLAY OLED
# =========================
i2c = SoftI2C(scl=Pin(15), sda=Pin(14))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

# =========================
# INDICANDO CONEXÃO WIFI
# =========================
display.fill(0)
display.text("Conectando...", 10, 20)
display.show()
LED_VERMELHO.on()
LED_VERDE.off()

print("Conectando ao Wi-Fi...")
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    print(".", end="")
    time.sleep(0.5)

LED_VERMELHO.off()
LED_VERDE.on()
display.fill(0)
display.text("Conectado!", 10, 20)
display.show()
som_conexao()
print("\nConectado!")
print("Configuração de rede:", wlan.ifconfig())

# =========================
# CONFIGURAÇÃO SENSOR DE TEMPERATURA
# =========================
sensor_temp = ADC(28)  # GPIO28
VREF = 3.3

def ler_temperatura():
    valor_adc = sensor_temp.read_u16()
    volts = (valor_adc / 35535) * VREF
    temp_c = (volts - 0.5) * 10  # TMP36
    return temp_c

def mostrar_temperatura_no_display(temp):
    display.fill(0)
    display.text("Temp RN:", 0, 0)
    display.text("{:.1f} C".format(temp), 0, 20)
    display.show()

# =========================
# CONFIGURAÇÃO THINGSPEAK
# =========================
THINGSPEAK_API_KEY = "UDNCLX7JPX0693CI"  # sua Write API Key

def enviar_thingspeak(temp):
    url = "https://api.thingspeak.com/update?api_key={}&field1={}".format(THINGSPEAK_API_KEY, temp)
    try:
        resposta = urequests.get(url)
        resposta.close()
        print("Dado enviado para ThingSpeak:", temp)
        # Som curto indicando envio bem-sucedido
        som_conexao(0.1, 1500)
    except:
        print("Erro ao enviar para ThingSpeak")

# =========================
# LOOP PRINCIPAL
# =========================
while True:
    temp = ler_temperatura()
    mostrar_temperatura_no_display(temp)
    enviar_thingspeak(temp)
    time.sleep(15)  # ThingSpeak permite no máximo 1 atualização a cada 15 segundos






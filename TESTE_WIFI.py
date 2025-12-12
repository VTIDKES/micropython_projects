from machine import I2C, Pin, PWM
import ssd1306
import time

# --- Configuração do Display OLED ---
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
display = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

# --- Configuração dos LEDs ---
LED_VERMELHO = Pin(12, Pin.OUT)   # Pisca durante a música
LED_AZUL = Pin(13, Pin.OUT)       # Jogador 1
LED_VERDE = Pin(11, Pin.OUT)      # Jogador 2

# --- Buzzer com PWM ---
buzzer = PWM(Pin(21))

# --- Botões com pull-up ---
BOTAO_J1 = Pin(5, Pin.IN, Pin.PULL_UP)
BOTAO_J2 = Pin(6, Pin.IN, Pin.PULL_UP)

# --- Frequências das notas (Hz) ---
DO = 262; REb = 277; RE = 294; MIb = 311; MI = 330
FA = 349; SOLb = 370; SOL = 392; LAb = 415; LA = 440
SIb = 466; SI = 494

# --- Variáveis do jogo ---
pontos_j1 = 0
pontos_j2 = 0
fator = 1.5  # Ajuste de tom

# --- Melodia do jogo ---
melodia = [
    (int(SOL*fator),300),(int(SOL*fator),300),(int(SOL*fator),300),
    (int(MIb*fator),500),(int(RE*fator),500),(int(DO*fator),700),
    # ... (restante da melodia como no código original)
]

def atualizar_display():
    display.fill(0)
    display.text("The Good, Bad & Ugly", 0, 0)
    display.text(f"J1: {pontos_j1} pts", 0, 20)
    display.text(f"J2: {pontos_j2} pts", 0, 40)
    display.text("Aperte para jogar!", 0, 55)
    display.show()

def tocar_musica():
    global pontos_j1, pontos_j2
    for freq, dur in melodia:
        if not BOTAO_J1.value():
            pontos_j1 += 1
            return 1
        if not BOTAO_J2.value():
            pontos_j2 += 1
            return 2
        
        buzzer.freq(freq)
        buzzer.duty_u16(30000)
        LED_VERMELHO.toggle()
        time.sleep_ms(dur)
        buzzer.duty_u16(0)
        LED_VERMELHO.off()
        time.sleep_ms(100)
    return 0

def reset_leds():
    LED_VERMELHO.off()
    LED_AZUL.off()
    LED_VERDE.off()

# --- Inicialização ---
display.fill(0)
display.text("Iniciando jogo...", 0, 30)
display.show()
time.sleep(2)

# --- Loop Principal ---
while True:
    reset_leds()
    atualizar_display()
    
    print("\nNova rodada iniciando...")
    vencedor = tocar_musica()

    buzzer.duty_u16(0)
    LED_VERMELHO.off()

    if vencedor == 1:
        print("Jogador 1 venceu!")
        LED_AZUL.on()
    elif vencedor == 2:
        print("Jogador 2 venceu!")
        LED_VERDE.on()
    else:
        print("Ninguém venceu.")

    atualizar_display()
    time.sleep(3)
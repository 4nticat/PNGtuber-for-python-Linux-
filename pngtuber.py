import tkinter as tk
from PIL import Image, ImageTk
import pyaudio
import numpy as np
import random

# --- CONFIGURACIÓN ---
# Imágenes: 1=Normal, 2=Parpadeo
IMG_C_1 = "cerrada.png"
IMG_C_2 = "cerrada_p.png"
IMG_A_1 = "abierta.png"
IMG_A_2 = "abierta_p.png"

UMBRAL = 600  # Sensibilidad del micro
CHUNK = 1024

class PNGTuberPro:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.config(bg='green')
        
        # Cargar las 4 imágenes
        self.imgs = {
            "quieto": ImageTk.PhotoImage(Image.open(IMG_C_1).resize((150, 150))),
            "quieto_p": ImageTk.PhotoImage(Image.open(IMG_C_2).resize((150, 150))),
            "hablar": ImageTk.PhotoImage(Image.open(IMG_A_1).resize((150, 150))),
            "hablar_p": ImageTk.PhotoImage(Image.open(IMG_A_2).resize((150, 150)))
        }
        
        self.label = tk.Label(root, image=self.imgs["quieto"], bg='green')
        self.label.pack()

        # Audio
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=CHUNK)
        
        self.is_blinking = False
        self.check_audio()
        self.blink_logic()

    def blink_logic(self):
        # Alterna el estado de parpadeo aleatoriamente
        self.is_blinking = not self.is_blinking
        duracion = 150 if self.is_blinking else random.randint(2000, 4000)
        self.root.after(duracion, self.blink_logic)

    def check_audio(self):
        try:
            data = np.frombuffer(self.stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
            rms = np.sqrt(np.mean(data**2))
            
            # Lógica de estados
            if rms > UMBRAL:
                estado = "hablar_p" if self.is_blinking else "hablar"
            else:
                estado = "quieto_p" if self.is_blinking else "quieto"
                
            self.label.config(image=self.imgs[estado])
        except:
            pass
        self.root.after(50, self.check_audio)

root = tk.Tk()
# Permitir mover la ventana con el click izquierdo
def start_move(event): root.x, root.y = event.x, event.y
def stop_move(event): root.x = root.y = None
def on_move(event):
    deltax, deltay = event.x - root.x, event.y - root.y
    root.geometry(f"+{root.winfo_x() + deltax}+{root.winfo_y() + deltay}")

root.bind("<Button-1>", start_move)
root.bind("<ButtonRelease-1>", stop_move)
root.bind("<B1-Motion>", on_move)

app = PNGTuberPro(root)
root.mainloop()

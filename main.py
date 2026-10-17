import cv2
import numpy as np
import mss
import keyboard
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox
import os

class ModernScreenRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title("Antigravity Pro Ekran Kaydedici")
        self.root.geometry("450x300")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(False, False)

        # Durum Değişkenleri
        self.is_recording = False
        self.mic_enabled = True
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[1]
        self.fps = 20
        self.out = None
        self.output_folder = os.path.dirname(os.path.abspath(__file__))

        self.setup_ui()
        self.setup_hotkeys()

    def setup_ui(self):
        # Başlık
        title_lbl = tk.Label(self.root, text="🎥 PRO EKRAN KAYDEDİCİ", font=("Segoe UI", 16, "bold"), bg="#1e1e2e", fg="#89b4fa")
        title_lbl.pack(pady=15)

        # Durum Göstergesi
        self.status_var = tk.StringVar()
        self.status_var.set("Durum: Hazır (Kayıt Bekleniyor...)")
        self.status_lbl = tk.Label(self.root, textvariable=self.status_var, font=("Segoe UI", 11), bg="#1e1e2e", fg="#a6adc8")
        self.status_lbl.pack(pady=5)

        # Mikrofon Durumu
        self.mic_var = tk.StringVar()
        self.update_mic_label()
        self.mic_lbl = tk.Label(self.root, textvariable=self.mic_var, font=("Segoe UI", 11, "bold"), bg="#1e1e2e")
        self.mic_lbl.pack(pady=5)

        # Butonlar için Çerçeve
        btn_frame = tk.Frame(self.root, bg="#1e1e2e")
        btn_frame.pack(pady=20)

        # Başla Butonu
        self.start_btn = tk.Button(btn_frame, text="▶ Kaydı Başlat (F9)", font=("Segoe UI", 10, "bold"), 
                                   bg="#a6e3a1", fg="#11111b", width=18, relief="flat", command=self.start_recording)
        self.start_btn.grid(row=0, column=0, padx=10, pady=5)

        # Durdur Butonu
        self.stop_btn = tk.Button(btn_frame, text="⏹ Kaydı Durdur (F10)", font=("Segoe UI", 10, "bold"), 
                                  bg="#f38ba8", fg="#11111b", width=18, relief="flat", state=tk.DISABLED, command=self.stop_recording)
        self.stop_btn.grid(row=0, column=1, padx=10, pady=5)

        # Mikrofon Butonu
        self.mic_btn = tk.Button(btn_frame, text="🎙 Mikrofon Aç/Kapat (F8)", font=("Segoe UI", 10, "bold"), 
                                 bg="#f9e2af", fg="#11111b", width=39, relief="flat", command=self.toggle_mic)
        self.mic_btn.grid(row=1, column=0, columnspan=2, pady=10)

        # Klasör Aç Butonu
        folder_btn = tk.Button(self.root, text="📂 Kayıt Klasörünü Aç", font=("Segoe UI", 9), 
                               bg="#313244", fg="#cdd6f4", relief="flat", command=self.open_folder)
        folder_btn.pack(pady=5)

    def setup_hotkeys(self):
        keyboard.on_press_key('f9', lambda _: self.start_recording())
        keyboard.on_press_key('f10', lambda _: self.stop_recording())
        keyboard.on_press_key('f8', lambda _: self.toggle_mic())

    def update_mic_label(self):
        if self.mic_enabled:
            self.mic_var.set("Mikrofon: AÇIK 🎙")
            if hasattr(self, 'mic_lbl'): self.mic_lbl.config(fg="#a6e3a1")
        else:
            self.mic_var.set("Mikrofon: KAPALI 🔇")
            if hasattr(self, 'mic_lbl'): self.mic_lbl.config(fg="#f38ba8")

    def toggle_mic(self):
        self.mic_enabled = not self.mic_enabled
        self.update_mic_label()

    def start_recording(self):
        if not self.is_recording:
            self.is_recording = True
            
            # UI Güncelleme
            self.start_btn.config(state=tk.DISABLED, bg="#45475a")
            self.stop_btn.config(state=tk.NORMAL, bg="#f38ba8")
            self.status_var.set("Durum: 🔴 KAYIT YAPILIYOR...")
            self.status_lbl.config(fg="#f38ba8")

            # Video Ayarları - Windows'ta oynatma hatalarını çözmek için AVI formatı ve XVID kullanıyoruz
            filename = f"Kayit_{time.strftime('%Y%m%d_%H%M%S')}.avi"
            self.current_filepath = os.path.join(self.output_folder, filename)
            
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.out = cv2.VideoWriter(self.current_filepath, fourcc, self.fps, (self.monitor['width'], self.monitor['height']))

            # Kaydı başlat
            threading.Thread(target=self.record_loop, daemon=True).start()

    def record_loop(self):
        while self.is_recording:
            start_time = time.time()
            img = self.sct.grab(self.monitor)
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            self.out.write(frame)
            
            # FPS ayarı
            sleep_time = max(1/self.fps - (time.time() - start_time), 0)
            time.sleep(sleep_time)

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            time.sleep(0.5)
            if self.out:
                self.out.release()

            # UI Güncelleme
            self.start_btn.config(state=tk.NORMAL, bg="#a6e3a1")
            self.stop_btn.config(state=tk.DISABLED, bg="#45475a")
            self.status_var.set("Durum: ✅ Kayıt Bitti ve Kaydedildi!")
            self.status_lbl.config(fg="#a6e3a1")

    def open_folder(self):
        os.startfile(self.output_folder)

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernScreenRecorder(root)
    root.mainloop()

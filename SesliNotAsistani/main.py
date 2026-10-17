import tkinter as tk
from tkinter import scrolledtext, messagebox
import speech_recognition as sr
import threading
import os
import time

class VoiceToTextApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎙️ Akıllı Ses Asistanı (Sesi Yazıya Çevir)")
        self.root.geometry("550x500")
        self.root.configure(bg="#2E3440")
        self.root.resizable(False, False)

        self.is_listening = False
        self.recognizer = sr.Recognizer()
        self.output_folder = os.path.dirname(os.path.abspath(__file__))

        self.setup_ui()

    def setup_ui(self):
        # Üst Başlık
        title_lbl = tk.Label(self.root, text="🗣️ Sesten Metne Asistanı", font=("Segoe UI", 18, "bold"), bg="#2E3440", fg="#88C0D0")
        title_lbl.pack(pady=15)

        # Durum Çubuğu
        self.status_var = tk.StringVar()
        self.status_var.set("Durum: Başlamak için 'Dinlemeyi Başlat'a basın.")
        self.status_lbl = tk.Label(self.root, textvariable=self.status_var, font=("Segoe UI", 11, "italic"), bg="#2E3440", fg="#D8DEE9")
        self.status_lbl.pack(pady=5)

        # Çıktı Metin Kutusu
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=12, font=("Consolas", 11), bg="#3B4252", fg="#ECEFF4", insertbackground="white")
        self.text_area.pack(pady=10, padx=20)
        self.text_area.insert(tk.INSERT, "Söyledikleriniz burada görünecek...\n\n")

        # Buton Çerçevesi
        btn_frame = tk.Frame(self.root, bg="#2E3440")
        btn_frame.pack(pady=15)

        # Dinle Butonu
        self.listen_btn = tk.Button(btn_frame, text="🎤 Dinlemeyi Başlat", font=("Segoe UI", 11, "bold"), bg="#A3BE8C", fg="#2E3440", width=18, relief="flat", command=self.start_listening)
        self.listen_btn.grid(row=0, column=0, padx=10)

        # Kaydet Butonu
        self.save_btn = tk.Button(btn_frame, text="💾 Metni Kaydet (.txt)", font=("Segoe UI", 11, "bold"), bg="#EBCB8B", fg="#2E3440", width=18, relief="flat", command=self.save_to_file)
        self.save_btn.grid(row=0, column=1, padx=10)

        # Temizle Butonu
        clear_btn = tk.Button(self.root, text="🗑️ Ekranı Temizle", font=("Segoe UI", 10), bg="#BF616A", fg="#ECEFF4", relief="flat", command=self.clear_text)
        clear_btn.pack(pady=5)

    def start_listening(self):
        self.listen_btn.config(state=tk.DISABLED, bg="#4C566A")
        self.status_var.set("Durum: 🔴 Seni Dinliyorum... Konuşabilirsin.")
        self.status_lbl.config(fg="#BF616A")
        
        # Dinleme işlemini ayrı bir thread'de (arka planda) başlat ki arayüz donmasın
        threading.Thread(target=self.listen_and_transcribe, daemon=True).start()

    def listen_and_transcribe(self):
        with sr.Microphone() as source:
            # Ortam gürültüsüne göre mikrofonu ayarla (daha net anlaşılması için)
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                # Kullanıcının sesini dinle (max 10 saniyelik konuşma alıyoruz tek seferde)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=15)
                
                self.status_var.set("Durum: ⏳ Analiz ediliyor, lütfen bekle...")
                self.status_lbl.config(fg="#EBCB8B")

                # Ses verisini Google'ın konuşma motoruna gönder ve Türkçe ('tr-TR') olarak çevir
                text = self.recognizer.recognize_google(audio, language="tr-TR")
                
                # Metin kutusuna ekle
                self.text_area.insert(tk.END, f"- {text}\n")
                self.text_area.see(tk.END) # Otomatik olarak en aşağı kaydır

                self.status_var.set("Durum: ✅ Başarılı! Tekrar konuşmak için Başlat'a basın.")
                self.status_lbl.config(fg="#A3BE8C")

            except sr.WaitTimeoutError:
                self.status_var.set("Durum: ⚠️ Kimseden ses çıkmadı.")
                self.status_lbl.config(fg="#D08770")
            except sr.UnknownValueError:
                self.status_var.set("Durum: ⚠️ Ne dediğini tam anlayamadım, tekrarla.")
                self.status_lbl.config(fg="#D08770")
            except sr.RequestError as e:
                self.status_var.set("Durum: ❌ İnternete bağlanılamadı!")
                self.status_lbl.config(fg="#BF616A")
            except Exception as e:
                self.status_var.set("Durum: ❌ Bir hata oluştu.")
                self.status_lbl.config(fg="#BF616A")
            finally:
                # İşlem bitince butonu tekrar aktif et
                self.listen_btn.config(state=tk.NORMAL, bg="#A3BE8C")

    def save_to_file(self):
        text_content = self.text_area.get("1.0", tk.END).strip()
        if not text_content or text_content == "Söyledikleriniz burada görünecek...":
            messagebox.showwarning("Boş Metin", "Kaydedilecek bir yazı bulunamadı!")
            return

        filename = f"SesliNot_{time.strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = os.path.join(self.output_folder, filename)
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("--- SESLİ ASİSTAN NOTLARI ---\n\n")
                f.write(text_content)
            
            messagebox.showinfo("Başarılı", f"Metin başarıyla şu dosyaya kaydedildi:\n\n{filename}")
            # Kaydedilen klasörü aç
            os.startfile(self.output_folder)
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya kaydedilirken hata oluştu:\n{e}")

    def clear_text(self):
        self.text_area.delete("1.0", tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceToTextApp(root)
    root.mainloop()

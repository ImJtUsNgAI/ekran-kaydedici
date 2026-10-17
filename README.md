# Ekran Kaydedici

Windows için Python ve tkinter ile yazılmış ekran kaydedici. Görüntüyü `mss` ile alıp OpenCV ile videoya yazıyor, kısayol tuşları `keyboard` kütüphanesinden.

- `main.py`: masaüstü uygulaması
- `Ekran kaydedici (tek sayfa).html`: tarayıcıda çalışan sürüm
- `SesliNotAsistani/main.py`: konuşmayı yazıya çeviren küçük not uygulaması

```
pip install opencv-python numpy mss keyboard SpeechRecognition
python main.py
```
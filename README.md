
# 🔊 WAL - WhatsApp Audio Leak

**WAL (WhatsApp Audio Leak)** es una herramienta desarrollada para fines de **peritaje informático forense** y **seguridad ofensiva**. Puede ser utilizada tanto por profesionales en investigaciones judiciales como por equipos de concientización en campañas de ciberseguridad, para demostrar la sensibilidad de la información que se transmite por audio en dispositivos Android.

## 🎯 ¿Para qué sirve?

WAL permite analizar los audios de WhatsApp almacenados en un dispositivo Android, extrayéndolos automáticamente mediante ADB y procesándolos con inteligencia artificial para buscar palabras clave sensibles como contraseñas, datos bancarios, usuarios o cualquier información personal que pueda representar un riesgo si es interceptada por un ciberdelincuente.

## 🔐 Casos de uso

- 🧑‍⚖️ **Peritaje digital:** búsqueda de nombres, contraseñas, claves y patrones en audios relacionados a investigaciones judiciales.
- 🧑‍💻 **Campañas de concientización:** demostración del impacto de fugas de datos por audio ante empresas o usuarios.
- 🕵️‍♂️ **Auditorías de privacidad:** verificación de información crítica filtrada vía mensajes de voz.

---

## 🛠 ¿Cómo funciona?

1. Conectás un celular Android con **Depuración USB** activada.
2. WAL extrae automáticamente los mensajes de voz de WhatsApp.
3. Utiliza **Whisper** (modelo de transcripción de OpenAI) para convertir audio a texto.
4. Analiza las transcripciones en busca de **palabras clave sensibles**.
5. Muestra en pantalla los posibles hallazgos y los guarda en un archivo (`secretleak.txt`).

---

## 📲 ¿Cómo activar la Depuración USB?

1. Abrí **Configuración** en tu celular.
2. Ingresá a **Acerca del teléfono**.
3. Tocá 7 veces sobre **Número de compilación** para activar las opciones de desarrollador.
4. Volvé atrás e ingresá a **Opciones de desarrollador**.
5. Activá la opción **Depuración USB**.

---

## 🧪 Guía de uso

1. Ejecutá `WAL_UI.py` o el `.exe` generado (si estás en Windows).
2. Conectá tu celular Android por USB. La herramienta mostrará “🔌 Esperando conexión ADB...” hasta que lo detecte.
3. Una vez detectado el dispositivo, se desbloquearán las opciones de análisis:

   - **Todos los audios** (opción predeterminada), o
   - Los **últimos X audios** (configurable).

4. Podés agregar **palabras clave adicionales** a los filtros por defecto:
   - Filtros por defecto: `tarjeta de credito`, `contraseña`, `clave`, `usuario`, `tarjeta`, `correo`, `acceso`, `banco`, `password`.

5. Hacé clic en **"Iniciar análisis"**.
6. La herramienta mostrará paso a paso:
   - 🔍 Extracción de audios
   - 🧠 Transcripción con Whisper
   - 🕵️ Búsqueda de palabras clave
   - 📄 Resultados encontrados

7. Al finalizar, se mostrará un resumen de lo detectado y se generará un archivo llamado `secretleak.txt` con los resultados.

---

## 🖼 Capturas de ejemplo

### Menú con filtros por defecto:
![Captura de pantalla 2025-06-08 210400](https://github.com/user-attachments/assets/38a304ef-8340-4899-9d98-9937989d2854)


### Menú con filtros personalizados:
![Captura de pantalla 2025-06-08 210434](https://github.com/user-attachments/assets/3042af3b-2a6f-4b2c-9842-ec921e2c2c45)


---

## 🧠 Autor

**Un Hacker En Capital**  
🎥 YouTube: [Un Hacker En Capital](https://www.youtube.com/@unhackerencapital)  
🎮 Twitch: [UnHackerEnCapital](https://twitch.tv/unhackerencapital)  
📱 TikTok: [@unhackerencapital](https://www.tiktok.com/@unhackerencapital)

---

## ⚠️ Disclaimer

> Esta herramienta se proporciona exclusivamente con fines educativos y de investigación.  
> El autor no se responsabiliza por el uso indebido de este script o su aplicación fuera de entornos controlados.  
> Usala con responsabilidad, ética y respeto por la ley.

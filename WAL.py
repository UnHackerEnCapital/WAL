
import sys
import os
import threading
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,
                             QHBoxLayout, QSpinBox, QTextEdit, QMessageBox, QCheckBox, QLineEdit)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer

class WALApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("W.A.L. - Whatsapp Audio Leak")
        self.setGeometry(200, 200, 700, 680)
        self.setStyleSheet("background-color: black; color: white;")

        self.layout = QVBoxLayout()
        self.banner = QLabel()
        self.banner.setPixmap(QPixmap("logo.png").scaledToWidth(400, Qt.SmoothTransformation))
        self.banner.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.banner)

        self.header = QLabel("Análisis de Audios de WhatsApp")
        self.header.setFont(QFont("Courier", 14, QFont.Bold))
        self.header.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.header)

        self.instrucciones_btn = QPushButton("📱 ¿Cómo activar Depuración USB?")
        self.instrucciones_btn.clicked.connect(self.mostrar_instrucciones)
        self.layout.addWidget(self.instrucciones_btn)

        self.estado_dispositivo = QLabel("🔌 Esperando conexión ADB...")
        self.estado_dispositivo.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.estado_dispositivo)

        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_estado_adb)
        self.toggle = False
        self.timer.start(500)

        self.opciones_layout = QVBoxLayout()
        self.titulo_analisis = QLabel("¿Qué deseas analizar?")
        self.opciones_layout.addWidget(self.titulo_analisis)

        self.checkbox_todos = QCheckBox("Todos los audios")
        self.checkbox_todos.setChecked(True)
        self.checkbox_todos.stateChanged.connect(self.toggle_cantidad)
        self.opciones_layout.addWidget(self.checkbox_todos)

        self.hbox = QHBoxLayout()
        self.label_cantidad = QLabel("Cantidad de últimos audios:")
        self.label_cantidad.setEnabled(False)
        self.hbox.addWidget(self.label_cantidad)

        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setRange(1, 1000)
        self.spin_cantidad.setEnabled(False)
        self.hbox.addWidget(self.spin_cantidad)
        self.opciones_layout.addLayout(self.hbox)

        self.label_filtros = QLabel("Palabras clave adicionales (separadas por coma):")
        self.opciones_layout.addWidget(self.label_filtros)

        self.input_filtros = QLineEdit()
        self.input_filtros.setPlaceholderText("Ej: visa, DNI, código")
        self.opciones_layout.addWidget(self.input_filtros)

        self.layout.addLayout(self.opciones_layout)

        self.analizar_btn = QPushButton("Iniciar análisis")
        self.analizar_btn.clicked.connect(self.iniciar_analisis)
        self.layout.addWidget(self.analizar_btn)

        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setStyleSheet("background-color: #111; color: white;")
        self.resultado.setPlaceholderText("📝 Estado del proceso paso a paso...")
        self.layout.addWidget(self.resultado)

        self.salida = QTextEdit()
        self.salida.setReadOnly(True)
        self.salida.setStyleSheet("background-color: #222; color: white;")
        self.salida.setPlaceholderText("📋 Resultados encontrados...")
        self.layout.addWidget(self.salida)

        self.setLayout(self.layout)

        self.adb_detectado = False
        self.filtros_por_defecto = ["tarjeta de credito", "contraseña", "clave", "usuario", "tarjeta", "correo", "acceso", "banco", "password"]

    def toggle_cantidad(self):
        estado = not self.checkbox_todos.isChecked()
        self.label_cantidad.setEnabled(estado)
        self.spin_cantidad.setEnabled(estado)

    def mostrar_instrucciones(self):
        texto = (
            "1. Ir a Configuración del celular.\n"
            "2. Entrar a 'Acerca del teléfono' y presionar 7 veces sobre 'Número de compilación'.\n"
            "3. Volver atrás y entrar a 'Opciones de desarrollador'.\n"
            "4. Activar 'Depuración USB'.\n"
        )
        QMessageBox.information(self, "Cómo activar la Depuración USB", texto)

    def actualizar_estado_adb(self):
        result = os.popen("adb get-state").read().strip()
        if "device" in result:
            self.estado_dispositivo.setText("✅ Dispositivo ADB detectado.")
            self.timer.stop()
            self.adb_detectado = True
        else:
            self.toggle = not self.toggle
            estado = "🔌 Esperando conexión ADB..." if self.toggle else ""
            self.estado_dispositivo.setText(estado)

    def iniciar_analisis(self):
        if not self.adb_detectado:
            QMessageBox.warning(self, "Dispositivo no conectado", "Conecte un dispositivo Android con Depuración USB activada.")
            return

        self.resultado.clear()
        self.salida.clear()
        threading.Thread(target=self.proceso_analisis, daemon=True).start()

    def proceso_analisis(self):
        self.resultado.append("🔍 Iniciando extracción de audios...")
        os.system("mkdir Audios >nul 2>&1")
        result = os.popen("adb shell find '/storage/emulated/0/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Voice Notes/' -type f -name '*.opus'").read()
        files = sorted([f.strip() for f in result.strip().split("\n") if f.strip()])
        if not self.checkbox_todos.isChecked():
            files = files[-self.spin_cantidad.value():]

        for f in files:
            nombre = os.path.basename(f)
            os.system(f'adb pull "{f}" "Audios/{nombre}" >nul 2>&1')
        self.resultado.append(f"📁 Audios copiados: {len(files)}")

        self.resultado.append("🧠 Analizando con Whisper...")
        os.system("del audioleak.txt >nul 2>&1")
        import whisper
        model = whisper.load_model("base")
        with open("audioleak.txt", "w", encoding="utf-8") as out_file:
            for f in files:
                nombre = os.path.basename(f)
                path_local = f"Audios/{nombre}"
                result = model.transcribe(path_local, language="es")
                out_file.write(result["text"] + "\n")
        self.resultado.append("✅ Transcripción completada.")

        self.resultado.append("🕵️ Buscando secretos sensibles...")
        user_keywords = [x.strip().lower() for x in self.input_filtros.text().split(",") if x.strip()]
        filtros = self.filtros_por_defecto + user_keywords
        encontrados = []
        with open("audioleak.txt", "r", encoding="utf-8") as f:
            for linea in f:
                texto = linea.strip().lower()
                if any(filtro in texto for filtro in filtros):
                    encontrados.append(linea.strip())

        self.resultado.append(f"🔎 Se encontraron {len(encontrados)} posibles secretos.")
        if encontrados:
            with open("secretleak.txt", "w", encoding="utf-8") as out:
                for l in encontrados:
                    out.write(l + "\n")
        self.resultado.append("📄 Guardado en secretleak.txt")

        resumen_filtros = ", ".join(filtros)
        cantidad = "Todos" if self.checkbox_todos.isChecked() else self.spin_cantidad.value()
        self.resultado.append(f"\n📋 Análisis configurado:\n- Audios: {cantidad}\n- Filtros: {resumen_filtros}")

        if encontrados:
            self.salida.append("🔐 Secretos detectados:")
            for linea in encontrados:
                self.salida.append(f" - {linea}")
        else:
            self.salida.append("🛡 No se encontraron secretos sensibles en los audios analizados.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = WALApp()
    ventana.show()
    sys.exit(app.exec_())

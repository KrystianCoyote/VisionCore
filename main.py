import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import numpy as np


class SistemaAnalisisGrafico:
    def __init__(self, root):
        self.root = root
        self.root.title("VisionCore - Engine de Reconocimiento y Procesamiento v1.0")
        self.root.geometry("1150x700")
        self.root.configure(bg="#0f172a")  # Fondo principal oscuro/grafito

        # Estado de persistencia de datos
        self.ruta_imagen = None
        self.imagen_original = None
        self.imagen_procesada = None

        self.construir_entorno_visual()

    def construir_entorno_visual(self):
        """Genera una distribución de tres niveles con estética industrial/cyberpunk."""

        # ==========================================
        # 1. BARRA SUPERIOR DE ACCIONES (TOP BAR)
        # ==========================================
        barra_superior = tk.Frame(self.root, bg="#1e293b", height=70)
        barra_superior.pack(side=tk.TOP, fill=tk.X)
        barra_superior.pack_propagate(False)

        lbl_marca = tk.Label(barra_superior, text="VISION//CORE", font=("Courier New", 14, "bold"), bg="#1e293b",
                             fg="#10b981")
        lbl_marca.pack(side=tk.LEFT, padx=20)

        # Botonera horizontal con estilo plano y moderno
        self.btn_cargar = tk.Button(barra_superior, text="[+] Importar Imagen", font=("Arial", 9, "bold"), bg="#8b5cf6",
                                    fg="white", bd=0, padx=15, pady=8, command=self.cargar_recurso)
        self.btn_cargar.pack(side=tk.LEFT, padx=10)

        self.btn_grises = tk.Button(barra_superior, text="Filtro Grises", font=("Arial", 9), bg="#334155", fg="#cbd5e1",
                                    bd=0, padx=12, pady=8, command=self.aplicar_escala_grises)
        self.btn_grises.pack(side=tk.LEFT, padx=5)

        self.btn_umbral = tk.Button(barra_superior, text="Segmentación Binaria", font=("Arial", 9), bg="#334155",
                                    fg="#cbd5e1", bd=0, padx=12, pady=8, command=self.aplicar_binarizacion)
        self.btn_umbral.pack(side=tk.LEFT, padx=5)

        self.btn_bordes = tk.Button(barra_superior, text="Aislamiento Bordes", font=("Arial", 9), bg="#334155",
                                    fg="#cbd5e1", bd=0, padx=12, pady=8, command=self.aplicar_canny)
        self.btn_bordes.pack(side=tk.LEFT, padx=5)

        self.btn_ia = tk.Button(barra_superior, text="// EJECUTAR RECONOCIMIENTO", font=("Arial", 9, "bold"),
                                bg="#10b981", fg="#0f172a", bd=0, padx=15, pady=8, command=self.clasificar_boceto)
        self.btn_ia.pack(side=tk.RIGHT, padx=20)

        # ==========================================
        # 2. ESPACIO CENTRAL: MONITORES DE VISUALIZACIÓN
        # ==========================================
        contenedor_monitores = tk.Frame(self.root, bg="#0f172a")
        contenedor_monitores.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=15)

        # Monitor Izquierdo (Input)
        frame_input = tk.LabelFrame(contenedor_monitores, text=" MONITOR DE ENTRADA: BUFFER ORIGINAL ",
                                    font=("Arial", 9, "bold"), bg="#111827", fg="#94a3b8", labelanchor="nw")
        frame_input.place(x=30, y=10, width=520, height=440)

        self.view_boceto = tk.Label(frame_input, bg="#1f2937")
        self.view_boceto.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Monitor Derecho (Output)
        frame_output = tk.LabelFrame(contenedor_monitores, text=" MONITOR DE RENDER: MATRIZ PROCESADA ",
                                     font=("Arial", 9, "bold"), bg="#111827", fg="#94a3b8", labelanchor="nw")
        frame_output.place(x=590, y=10, width=520, height=440)

        self.view_render = tk.Label(frame_output, bg="#1f2937")
        self.view_render.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ==========================================
        # 3. CONSOLA INFERIOR DE DIAGNÓSTICO
        # ==========================================
        frame_consola = tk.LabelFrame(self.root, text=" SYSTEM CONSOLE // DIAGNOSTIC LOGS ", font=("Arial", 9, "bold"),
                                      bg="#1e293b", fg="#8b5cf6")
        frame_consola.pack(side=tk.BOTTOM, fill=tk.X, padx=30, pady=20)
        frame_consola.pack_propagate(False)
        frame_consola.config(height=110)

        self.txt_logs = tk.Label(frame_consola,
                                 text="[STATUS] Sistema en espera. Cargue un recurso gráfico para inicializar el pipeline de visión.",
                                 font=("Courier New", 10), bg="#0f172a", fg="#38bdf8", anchor="w", justify=tk.LEFT,
                                 padx=15)
        self.txt_logs.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

    # --- CONTROLADORES DE ARCHIVO ---
    def cargar_recurso(self):
        self.ruta_imagen = filedialog.askopenfilename(filetypes=[("Formatos de Imagen", "*.png *.jpg *.jpeg *.bmp")])
        if self.ruta_imagen:
            self.imagen_original = cv2.imread(self.ruta_imagen)
            self.imagen_procesada = self.imagen_original.copy()

            self.renderizar_en_pantalla(self.imagen_original, self.view_boceto)
            self.view_render.config(image='')
            self.txt_logs.config(
                text="[OK] Imagen importada con éxito al búfer de entrada. Lista para operaciones morfológicas.",
                fg="#34d399")

    def renderizar_en_pantalla(self, img_cv, destino_canvas):
        alto, ancho = img_cv.shape[:2]
        proporcion = min(500 / ancho, 400 / alto)
        w_final = int(ancho * proporcion)
        h_final = int(alto * proporcion)

        img_aux = cv2.resize(img_cv, (w_final, h_final))

        if len(img_aux.shape) == 3:
            img_rgb = cv2.cvtColor(img_aux, cv2.COLOR_BGR2RGB)
        else:
            img_rgb = cv2.cvtColor(img_aux, cv2.COLOR_GRAY2RGB)

        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(image=img_pil)

        destino_canvas.image = img_tk
        destino_canvas.config(image=img_tk)

    # --- PIPELINE DE PROCESAMIENTO DIGITAL ---
    def aplicar_escala_grises(self):
        if self.imagen_original is None:
            messagebox.showwarning("Pipeline Error", "No hay ninguna matriz cargada en memoria.")
            return
        self.imagen_procesada = cv2.cvtColor(self.imagen_original, cv2.COLOR_BGR2GRAY)
        self.renderizar_en_pantalla(self.imagen_procesada, self.view_render)
        self.txt_logs.config(
            text="[PROCESS] Conversión espacial completada: Espacio cromático reducido a un solo canal (Grises).",
            fg="#cbd5e1")

    def aplicar_binarizacion(self):
        if self.imagen_original is None:
            messagebox.showwarning("Pipeline Error", "No hay ninguna matriz cargada en memoria.")
            return
        gris = cv2.cvtColor(self.imagen_original, cv2.COLOR_BGR2GRAY)
        _, self.imagen_procesada = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        self.renderizar_en_pantalla(self.imagen_procesada, self.view_render)
        self.txt_logs.config(
            text="[PROCESS] Umbralización adaptativa ejecutada: Segmentación binaria mediante varianza de Otsu completada.",
            fg="#a78bfa")

    def aplicar_canny(self):
        if self.imagen_original is None:
            messagebox.showwarning("Pipeline Error", "No hay ninguna matriz cargada en memoria.")
            return
        gris = cv2.cvtColor(self.imagen_original, cv2.COLOR_BGR2GRAY)
        suave = cv2.GaussianBlur(gris, (5, 5), 0)
        self.imagen_procesada = cv2.Canny(suave, 60, 160)
        self.renderizar_en_pantalla(self.imagen_procesada, self.view_render)
        self.txt_logs.config(
            text="[PROCESS] Operador multinivel Canny aplicado: Histéresis de contornos estructurados aislada.",
            fg="#f87171")

    # --- HEURÍSTICA DE RECONOCIMIENTO (IA GEOMÉTRICA) ---
    def clasificar_boceto(self):
        if self.imagen_original is None:
            messagebox.showwarning("Pipeline Error", "No hay datos para analizar.")
            return

        gris = cv2.cvtColor(self.imagen_original, cv2.COLOR_BGR2GRAY)
        _, umbral = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        contornos, _ = cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contornos:
            self.txt_logs.config(
                text="[ANALYSIS FAILED] No se encontraron patrones geométricos evaluables en la imagen.", fg="#ef4444")
            return

        c = max(contornos, key=cv2.contourArea)
        perimetro = cv2.arcLength(c, True)

        # Tolerancia del 2% para retener curvas orgánicas y detalles finos
        aproximacion = cv2.approxPolyDP(c, 0.02 * perimetro, True)
        vertices = len(aproximacion)

        x, y, w, h = cv2.boundingRect(c)
        aspecto = float(w) / h

        copia_render = self.imagen_original.copy()
        cv2.drawContours(copia_render, [aproximacion], -1, (139, 92, 246), 3)  # Contorno en morado
        cv2.rectangle(copia_render, (x, y), (x + w, y + h), (16, 185, 129), 2)  # Caja en verde neón

        # --- ÁRBOL DE DECISIONES CON PRIORIDAD Y TOLERANCIA CALIBRADA ---
        if aspecto >= 3.5 or aspecto <= 0.40:
            categoria = "ELEMENTO ELONGADO // ESPADA u OBJETO ALARGADO"
            log_detalles = f"Relación de aspecto extrema detectada ({aspecto:.2f}). Desviación de simetría axial."
        elif vertices == 4 and (0.5 <= aspecto <= 3.0):  # Rango ampliado para plataformas horizontales largas
            categoria = "ESTRUCTURA POLIGONAL // BLOQUE o PLATAFORMA DE JUEGO"
            log_detalles = f"Polígono cerrado de 4 vértices con proporción de plataforma ({aspecto:.2f})."
        elif vertices > 7:
            categoria = "ELEMENTO CIRCULAR // MONEDA / ESCUDO"
            log_detalles = f"Alta densidad esférica aproximada en contorno plano ({vertices} vértices evaluados)."
        else:
            categoria = "ENTIDAD COMPLEJA // PERSONAJE u OBJETO ASIMÉTRICO"
            log_detalles = f"Geometría orgánica asimétrica detectada con {vertices} puntos de control."

        self.renderizar_en_pantalla(copia_render, self.view_render)

        # Salida formateada de forma técnica en consola
        reporte_consola = (
            f"[VERDICTO]: {categoria}\n"
            f"[MÉTRICAS]: Vértices calculados: {vertices} | Aspect Ratio: {aspecto:.2f}\n"
            f"[LÓGICA]: {log_detalles}"
        )
        self.txt_logs.config(text=reporte_consola, fg="#38bdf8")


if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaAnalisisGrafico(root)
    root.mainloop()
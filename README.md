# VisionCore - Engine de Reconocimiento y Procesamiento v1.0

VisionCore es una aplicación de escritorio avanzada para el procesamiento digital de imágenes y reconocimiento de patrones geométricos mediante visión artificial. Diseñada con una estética industrial/cyberpunk, integra herramientas de segmentación y una heurística de inteligencia artificial para clasificar bocetos y objetos en tiempo real.

## ?? Características Principales

- **Procesamiento de Imágenes:**
  - **Filtro Grises:** Reducción del espacio cromático.
  - **Segmentación Binaria:** Umbralización adaptativa utilizando la varianza de Otsu.
  - **Aislamiento de Bordes:** Implementación del operador multinivel Canny con suavizado Gaussiano.
- **IA de Reconocimiento Geométrico:**
  - Clasificación inteligente de objetos (Espadas, Bloques, Monedas, Entidades Complejas).
  - Cálculo de métricas técnicas: Vértices, Relación de Aspecto (Aspect Ratio) y Perímetro.
- **Interfaz Moderna:** GUI construida en Tkinter con un diseño optimizado para monitoreo técnico y diagnóstico.

## ??? Requisitos Técnicos

El proyecto utiliza Python 3.x y las siguientes bibliotecas:

- **OpenCV (`opencv-python`):** Motor principal de visión artificial.
- **Pillow (`PIL`):** Gestión y renderizado de imágenes para la interfaz.
- **NumPy:** Procesamiento de matrices numéricas.
- **Tkinter:** Framework de interfaz gráfica.

## ?? Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/KrystianCoyote/VisionCore.git
   cd VisionCore
   ```

2. Crea y activa un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv .venv
   # En Windows:
   .venv\Scripts\activate
   # En Linux/macOS:
   source .venv/bin/activate
   ```

3. Instala las dependencias:
   ```bash
   pip install opencv-python pillow numpy
   ```

## ??? Uso

Para iniciar la aplicación, ejecuta el archivo principal:

```bash
python main.py
```

1. Haz clic en **[+] Importar Imagen** para cargar un recurso gráfico.
2. Utiliza los botones de **Pipeline de Procesamiento** para aplicar filtros.
3. Ejecuta **// EJECUTAR RECONOCIMIENTO** para que el sistema analice y clasifique el objeto detectado basándose en su geometría.

## ?? Estructura del Proyecto

- `main.py`: Lógica central de la aplicación y la interfaz.
- `.gitignore`: Configuración para excluir archivos temporales y entornos.
- `README.md`: Documentación del proyecto.

---
**Desarrollado por KrystianCoyote**

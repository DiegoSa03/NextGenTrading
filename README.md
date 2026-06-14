# NextGen Trading Simulator 📈✨

Un simulador interactivo de "Paper Trading" (inversiones virtuales) construido con Python (Flask) usando datos reales del mercado de valores a través de Yahoo Finance. Este fue desarrollado como proyecto final para Code in Place (Stanford).

## ✨ Características Principales
- **Datos en Tiempo Real:** Utiliza la librería `yfinance` para descargar precios actuales de las acciones.
- **Interfaz Premium (Glassmorphism):** Diseño moderno, modo oscuro elegante, animaciones suaves y un gráfico de dona interactivo usando Chart.js.
- **Máquina del Tiempo (Time Machine) ⏱️:** ¿Qué pasaría si hubieras invertido $1,000 en Apple hace 5 años? Esta herramienta te permite simular inversiones pasadas y ver tus ganancias hipotéticas al día de hoy.
- **Persistencia Local:** Todo tu portafolio y tu dinero virtual se guardan automáticamente para que no pierdas tu progreso.

---

## 🚀 Guía de Instalación y Uso (Paso a Paso)

Sigue estos sencillos pasos para ejecutar la aplicación en tu propia computadora:

### 1. Descargar el código
Puedes clonar el repositorio usando Git:
```bash
git clone https://github.com/DiegoSa03/NextGenTrading.git
```
*(O simplemente haz clic en el botón verde "Code" arriba y selecciona "Download ZIP", luego descomprime la carpeta).*

### 2. Verificar que tienes Python
Necesitas tener Python 3 instalado. Puedes verificarlo abriendo tu terminal o línea de comandos y escribiendo:
```bash
python --version
```

### 3. Instalar las dependencias
Abre tu terminal, navega hasta la carpeta donde descargaste el proyecto y ejecuta el siguiente comando para instalar Flask y yfinance:
```bash
pip install -r requirements.txt
```

### 4. Ejecutar la Aplicación
Una vez instaladas las dependencias, enciende el servidor web ejecutando:
```bash
python app.py
```

### 5. Abrir en el Navegador
Abre tu navegador web favorito (Chrome, Edge, Safari) y ve a la siguiente dirección:
**[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

¡Listo! Ya puedes empezar a comprar acciones, viajar en el tiempo y ver crecer tu portafolio.

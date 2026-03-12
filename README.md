
# 📊 Benchmarking Automatizado de Proveedores Logísticos

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)

Dashboard interactivo desarrollado en **Python** para evaluar proveedores logísticos mediante un modelo multicriterio basado en KPIs operativos, económicos y de calidad. 

La herramienta genera rankings de desempeño por categoría y estima el riesgo operativo de cada proveedor para facilitar la toma de decisiones estratégicas.

---

## 🚀 Tecnologías utilizadas

* **Lenguaje:** Python
* **Interfaz:** Streamlit
* **Manipulación de Datos:** Pandas, NumPy
* **Visualización:** Plotly


## ⚙️ Instalación

### 1. Clonar el repositorio
```bash
git clone [https://github.com/tuusuario/benchmarking-proveedores.git](https://github.com/tuusuario/benchmarking-proveedores.git)
cd benchmarking-proveedores

```

### 2. Crear un entorno virtual (recomendado)

**Usando Conda:**

```bash
conda create -n benchmarking python=3.11
conda activate benchmarking

```

**Usando venv:**

```bash
python -m venv venv

```

**Activar entorno:**

* **Mac / Linux:** `source venv/bin/activate`
* **Windows:** `venv\Scripts\activate`

### 3. Instalar dependencias

```bash
pip install streamlit pandas numpy plotly

```

---

## 💻 Ejecución

Para lanzar la aplicación, ejecuta el siguiente comando en tu terminal:

```bash
streamlit run app.py

```

La aplicación se abrirá automáticamente en tu navegador en: `http://localhost:8501`

---

## 🛠️ Uso

1. **Filtros:** Selecciona la categoría de proveedores en el panel lateral.
2. **Personalización:** Ajusta los pesos de evaluación (ponderaciones) para analizar distintos escenarios de negocio.
3. **Análisis:** Visualiza el ranking generado automáticamente.
4. **Riesgo:** Revisa el desempeño por bloques y el nivel de riesgo asignado a cada proveedor.
5. **Exportación:** Descarga los resultados para informes o análisis adicionales.

---

## 📂 Estructura del Proyecto

```text
benchmarking-proveedores/
├── data/
│   └── data_mvp.csv      # Dataset principal
├── app.py                # Lógica de la aplicación Streamlit
└── README.md             # Documentación

```

---

💡 *Desarrollado para optimizar la cadena de suministro mediante análisis de datos.*


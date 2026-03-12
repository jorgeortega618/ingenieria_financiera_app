# 📈 Aplicación Avanzada de Ingeniería Económica y Financiera

![Python](https://img.shields.io/badge/Python-3.14-blue?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.1+-150458?style=flat&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.18+-3F4F75?style=flat&logo=plotly&logoColor=white)

Este repositorio contiene una aplicación de grado institucional, desarrollada como una herramienta monolítica modular, para resolver casos de negocio integrales relacionados con matemáticas financieras, estructuración de crédito y valoración de activos.

El proyecto está diseñado para funcionar como un motor interactivo en la web, ofreciendo una experiencia visual y analítica rigurosa dirigida a consultores y analistas económicos de **Jorge Ortega**.

---

## 🏛️ Arquitectura del Sistema

El pipeline metodológico se dividió respetando el patrón de **responsabilidad única (Single Responsibility Principle)** a nivel de módulos estructurales, lo que ayuda al mantenimiento, validación y testing de cada feature financiera de forma agnóstica sin interceptar el `__main__` entry-point general (`app.py`).

El marco de la UI fue construido nativamente usando componentes asíncronos de Streamlit, orquestado con visualización interactiva usando _Plotly_ sobre esquemas de colores corporativos. 

La estructura arbórea jerárquica es la siguiente:

```text
/ingenieria_financiera_app
│── app.py                      # Core Entry-point (Gestor de Estado y Componentes Nav)
│── requirements.txt            # Matriz de dependencias de la máquina virtual (Python)
│── .gitignore                  # Políticas de exclusión de binarios VCS
│── modules/                    # Sub-agentes de Negocio aislados en archivos .py
│   ├── tasas.py                # -> (1) Componente Conversor Dinámico
│   ├── tvm.py                  # -> (2) Componente Calculator del Valor del Dinero Temporal
│   ├── amortizacion.py         # -> (3) Generador de Sistemas de Préstamos (Francés/Alemán)
│   ├── fcf_depreciacion.py     # -> (4) Proyección DataGrid FCF Multi-año Iterativo
│   └── evaluacion_bonos.py     # -> (5) Evaluación Terminal VPN, TIR y Yield de Bonos
└── utils/                      # Clases Auxiliares
    └── plots.py                # Wrapper unificado de estandarización visual corporativa Plotly
```

---

## ⚙️ Análisis de Capacidades y Modulos

El stack numérico se basa en la computación en memoria iterativa y los algoritmos analíticos provenientes de los paquetes _pandas_ nativo y _numpy_financial_.

### Módulo 1. Conversión de Tasa de Interés
*   **Proceso Central:** Un framework para estandarización cruzada de cualquier tasa en `float8` de precisión. Invariablemente se eleva el parámetro a un espectro EA (Efectiva Anual) en vencimientos nominales o periódicos para despejar las conversiones sin margen de error.

### Módulo 2. Motor TVM (Time Value of Money)
*   Equivale y sustituye calculadoras financieras clásicas tipo HP-12C resolviendo para **VP (Valor Presente), VF, Pago o Renta (PMT), Tasa o Número de Periodos Continuos (n)**. Posee autogenerador dinámico del Flujo de Caja y vector de diagramas de caja graficado.

### Módulo 3. Estructurador de Tablas de Amortización Activa
*   Generador iterativo de cuadros con despliegue Dataframe sobre estructuras _Francés_ (Cuota Base) o _Alemán_ (Capital Base).
*   **Gestión de Riesgo:** Manejo inteligente de *Años de Gracia* ya sean estáticos o sumandos (intereses moratorios componibles al saldo). Salida habilitada a descarga CSV.

### Módulo 4. Evaluador Predictivo de Flujo de Efectivo Libre (FCF) y Estructura Fiscal
*   Modelado tridimensional en tablas temporales en función a 5 componentes (Ingresos, COGS, SG&A, CAPEX Adicional, y Working Capital KT).
*   Configurador pre-armado para simulación técnica de depreciación Lineal y Métodos de saldo declinantes (DDB/SYD).
*   Inyección de Data-Storytelling: Renderizado de Cascada Dinámica de Impuestos para observar la construcción terminal del NOPAT a FCF operativo en un chart tipo Waterfall.

### Módulo 5. Toma de Decisiones y Valoración (Bonos Corportativos y VPN/TIR)
*   Toma la memoria caché inter-estatal almacenada en el FCF (`st.session_state`) para cruzar su costo ponderado (WACC) con iteraciones logarítmicas con un fin: Perfil del VPN y comprobación del _Break Even_ cruzado con el Costo de Oportunidad de Capital.
*   **Renta Fija Custom:** Sistema de calculación independiente de bonos, Price Cleaned y Yield To Maturity (YTM). Arroja análisis de riesgos base con la Duración de Macaulay Activa y la Duración Modificada Exógena.

---

## 🖥️ Requerimientos Despliegue Local (Environment Setup)

Si usted es consultor o colaborador, puede instanciar el servidor en su ecosistema local y probar las capacidades ejecutando lo siguiente:

### Dependencias y Entorno
* **Python >3.10** recomendado
* **Streamlit**, **Pandas**, **Numpy-Financial**, **Plotly**

```bash
# 1. Clonar este repositorio público por medio de Git:
git clone https://github.com/jorgeortega618/ingenieria_financiera_app.git

# 2. Navegar al Directorio:
cd ingenieria_financiera_app

# 3. Instalación de Dependencias Core del Pipeline:
pip install -r requirements.txt

# 4. Compilación del Server Streamlit Local
streamlit run app.py
```

El servidor asignará por default el ambiente en `localhost:8501`. 

### Contacto y Redes
Desarrollado y Curado por **Jorge Ortega**. Para contacto sobre arquitectura de datos o validación financiera, usted puede referirse al desarrollador mediante este hub en GitHub `(jorgeortega618)`.

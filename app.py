import streamlit as st
from modules.tasas import render_tasas
from modules.tvm import render_tvm
from modules.amortizacion import render_amortizacion
from modules.fcf_depreciacion import render_fcf_depreciacion
from modules.evaluacion_bonos import render_evaluacion_bonos

# Configuración de página con tema oscuro por defecto
st.set_page_config(
    page_title="Ingeniería Económica App",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados (Dark Theme UI details)
st.markdown("""
<style>
    /* Styling to make headers pop */
    h1, h2, h3 {
        color: #1e3a8a !important;
        font-family: 'Inter', sans-serif;
    }
    .stButton>button {
        background-color: #1e3a8a;
        color: #ffffff;
        font-weight: bold;
        border-radius: 8px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1e40af;
        color: #f8fafc;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: transparent;
        color: #64748b;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        border-top: 1px solid #e2e8f0;
        z-index: 100;
    }
    .footer a {
        color: #1e3a8a;
        text-decoration: none;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("Calculadora de Ingeniería Económica")
st.markdown("Aplicación Web interactiva para análisis financiero, evaluación de proyectos y matemáticas financieras.")

st.sidebar.title("Navegación")
st.sidebar.markdown("Seleccione un módulo:")

modulo = st.sidebar.radio("Módulos de la aplicación", [
    "Inicio",
    "1. Conversión de Tasas",
    "2. Valor del Dinero en el Tiempo (TVM)",
    "3. Tablas de Amortización",
    "4. Flujo de Efectivo FCF y Depreciación",
    "5. Evaluación de Proyectos y Bonos"
])

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    <div style="margin-top: 20px; font-size: 14px; color: #64748b;">
        👨‍💻 Desarrollado por <b>Jorge Ortega</b><br>
        🔗 <a href="https://github.com/jorgeortega618/ingenieria_financiera_app" target="_blank" style="color: #1e3a8a; text-decoration: none;">Ver Repositorio GitHub</a>
    </div>
    """, 
    unsafe_allow_html=True
)

if modulo == "Inicio":
    st.markdown("### Seleccione un módulo en el menú lateral para comenzar.")
    
elif modulo == "1. Conversión de Tasas":
    render_tasas()
    
elif modulo == "2. Valor del Dinero en el Tiempo (TVM)":
    render_tvm()

elif modulo == "3. Tablas de Amortización":
    render_amortizacion()

elif modulo == "4. Flujo de Efectivo FCF y Depreciación":
    render_fcf_depreciacion()

elif modulo == "5. Evaluación de Proyectos y Bonos":
    render_evaluacion_bonos()

# Footer Global Desplegado al final de la página
st.markdown(
    """
    <div class="footer">
        Aplicación de Ingeniería Económica y Financiera &copy; 2026 | Desarrollado por <b>Jorge Ortega</b> | 
        <a href="https://github.com/jorgeortega618/ingenieria_financiera_app" target="_blank">Repositorio en GitHub</a>
    </div>
    """,
    unsafe_allow_html=True
)

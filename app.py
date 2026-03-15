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

# Estilos personalizados (Light/Clean Dashboard UI details)
st.markdown("""
<style>
    /* Styling to make headers pop */
    h1, h2, h3, h4 {
        color: #2B3674 !important;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
    }
    .stButton>button {
        background-color: #4318FF;
        color: #ffffff;
        font-weight: bold;
        border-radius: 12px;
        border: none;
        padding: 0.5rem 1rem;
        box-shadow: 0 4px 14px 0 rgba(67, 24, 255, 0.39);
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #3311DB;
        color: #ffffff;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(67, 24, 255, 0.4);
    }
    .box-container {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 20px;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.05);
        margin-bottom: 24px;
        border: 1px solid #E2E8F0;
    }
    /* Estilo barra superior y nav nativa de Streamlit */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #E2E8F0;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        color: #A3AED0;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        border-top: 1px solid #E2E8F0;
        z-index: 100;
    }
    .footer a {
        color: #4318FF;
        text-decoration: none;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("Calculadora de Ingeniería Económica")
st.markdown("<p style='color: #64748b; font-size: 1.1rem;'>Aplicación Web interactiva para análisis financiero, evaluación de proyectos y matemáticas financieras.</p>", unsafe_allow_html=True)

st.sidebar.title("Navegación")
st.sidebar.markdown("Seleccione un módulo:")

if "modulo_actual" not in st.session_state:
    st.session_state.modulo_actual = "Inicio"

st.sidebar.radio("Módulos de la aplicación", [
    "Inicio",
    "1. Conversión de Tasas",
    "2. Valor del Dinero en el Tiempo (TVM)",
    "3. Tablas de Amortización",
    "4. Flujo de Efectivo FCF y Depreciación",
    "5. Evaluación de Proyectos y Bonos"
], key="modulo_actual")

modulo = st.session_state.modulo_actual

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
    # Hero Section
    st.markdown("""
        <div style="background: linear-gradient(135deg, #4318FF 0%, #868CFF 100%); padding: 60px; border-radius: 20px; color: white; margin-bottom: 30px; box-shadow: 0 10px 20px rgba(67, 24, 255, 0.2); text-align: center;">
            <h1 style="color: white !important; margin-bottom: 15px; font-size: 3.5rem; font-weight: 800;">Analítica Financiera Avanzada</h1>
            <p style="font-size: 1.2rem; opacity: 0.9; max-width: 800px; margin: 0 auto;">Tome decisiones estratégicas con nuestra suite de herramientas de ingeniería económica. Evalúe proyectos, estructure deuda y optimice flujos de efectivo de manera precisa.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Casos de Uso del Portal")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="box-container" style="text-align:center;">', unsafe_allow_html=True)
        st.markdown("### 🔄 Tasas y TVM")
        st.markdown("<p style='color: #64748b; font-size: 0.95rem; min-height: 80px;'>Convierta tasas de interés complejas y analice el valor del dinero en el tiempo con flujos interactivos.</p>", unsafe_allow_html=True)
        st.button("Conversión de Tasas", on_click=lambda: st.session_state.update(modulo_actual="1. Conversión de Tasas"), use_container_width=True)
        st.button("Calculadora TVM", on_click=lambda: st.session_state.update(modulo_actual="2. Valor del Dinero en el Tiempo (TVM)"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="box-container" style="text-align:center;">', unsafe_allow_html=True)
        st.markdown("### 📊 Amortización")
        st.markdown("<p style='color: #64748b; font-size: 0.95rem; min-height: 80px;'>Proyecte esquemas de deuda y visualice la composición de capital e intereses en cada cuota financiada.</p>", unsafe_allow_html=True)
        st.button("Tabla Amortización", on_click=lambda: st.session_state.update(modulo_actual="3. Tablas de Amortización"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="box-container" style="text-align:center;">', unsafe_allow_html=True)
        st.markdown("### 📈 Evaluaciones")
        st.markdown("<p style='color: #64748b; font-size: 0.95rem; min-height: 80px;'>Cree proyecciones de flujo, calcule VPN, TIR y valore bonos corporativos e instrumentos al instante.</p>", unsafe_allow_html=True)
        st.button("Flujo de Efectivo", on_click=lambda: st.session_state.update(modulo_actual="4. Flujo de Efectivo FCF y Depreciación"), use_container_width=True)
        st.button("Valoración", on_click=lambda: st.session_state.update(modulo_actual="5. Evaluación de Proyectos y Bonos"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
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

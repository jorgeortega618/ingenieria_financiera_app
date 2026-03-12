import streamlit as st
import pandas as pd

def render_tasas():
    st.header("Módulo 1: Conversión de Tasas de Interés")
    st.markdown("Herramienta interactiva para la equivalencia de tasas Nominales, Efectivas y Periódicas.")

    # Tarjeta de estilo visual (colores y bordes para agrupar)
    st.markdown("""
        <style>
        .box-container {
            background-color: #1e293b;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #00ffcc;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="box-container">', unsafe_allow_html=True)
        st.subheader("Datos de Origen")
        tasa_origen_ui = st.number_input("Tasa de origen (%)", value=12.0, format="%.8f")
        tasa_origen = tasa_origen_ui / 100.0
        
        tipo_origen = st.selectbox("Tipo de Tasa Origen", ["Nominal", "Efectiva", "Periódica"])
        
        # Opciones de capitalización
        periodos = {
            "Anual": 1,
            "Semestral": 2,
            "Cuatrimestral": 3,
            "Trimestral": 4,
            "Bimestral": 6,
            "Mensual": 12,
            "Quincenal": 24,
            "Semanal": 52,
            "Diaria": 360
        }
        
        if tipo_origen in ["Nominal", "Periódica"]:
            periodo_idx = 5 # Mensual por defecto
            capitalizacion_origen = st.selectbox("Capitalización Origen", list(periodos.keys()), index=periodo_idx)
            m_origen = periodos[capitalizacion_origen]
        else: # Efectiva Anual
            m_origen = 1
            capitalizacion_origen = "Anual"

        anticipada_origen = st.checkbox("¿Es tasa anticipada? (Origen)", value=False)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="box-container" style="border-left: 5px solid #3b82f6;">', unsafe_allow_html=True)
        st.subheader("Configuración Destino")
        tipo_destino = st.selectbox("Tipo de Tasa Destino", ["Nominal", "Efectiva", "Periódica"], index=1)
        
        if tipo_destino in ["Nominal", "Periódica"]:
            capitalizacion_destino = st.selectbox("Capitalización Destino", list(periodos.keys()), index=5)
            m_destino = periodos[capitalizacion_destino]
        else: # Efectiva Anual
            m_destino = 1
            capitalizacion_destino = "Anual"

        anticipada_destino = st.checkbox("¿Es tasa anticipada? (Destino)", value=False)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    
    # --- LÓGICA MATEMÁTICA DE CONVERSIÓN ---
    # Paso 1: Llevar cualquier tasa origen a Efectiva Anual Vencida (EA)
    tasa_efectiva_anual = 0.0
    
    if anticipada_origen:
        # Se calcula la equivalente vencida en su respectivo periodo -> iv = ia / (1 - ia)
        if tipo_origen == "Nominal":
            tasa_periodica_ant = tasa_origen / m_origen
            tasa_periodica_ven = tasa_periodica_ant / (1 - tasa_periodica_ant)
            tasa_efectiva_anual = (1 + tasa_periodica_ven)**m_origen - 1
        elif tipo_origen == "Periódica":
            tasa_periodica_ven = tasa_origen / (1 - tasa_origen)
            tasa_efectiva_anual = (1 + tasa_periodica_ven)**m_origen - 1
        else: # Efectiva Anticipada
            tasa_efectiva_anual = tasa_origen / (1 - tasa_origen)
    else:
        if tipo_origen == "Nominal":
            tasa_periodica_ven = tasa_origen / m_origen
            tasa_efectiva_anual = (1 + tasa_periodica_ven)**m_origen - 1
        elif tipo_origen == "Periódica":
            tasa_efectiva_anual = (1 + tasa_origen)**m_origen - 1
        else:
            tasa_efectiva_anual = tasa_origen

    # Paso 2: Desde Efectiva Anual Vencida (EA) transformar al destino solicitado
    tasa_resultado = 0.0

    if tipo_destino == "Efectiva":
        tasa_resultado = tasa_efectiva_anual
    else:
        # Calcular periódica vencida destino a partir de la EA
        tasa_periodica_dest_ven = (1 + tasa_efectiva_anual)**(1/m_destino) - 1
        
        if anticipada_destino:
            tasa_periodica_dest_ant = tasa_periodica_dest_ven / (1 + tasa_periodica_dest_ven)
            if tipo_destino == "Nominal":
                tasa_resultado = tasa_periodica_dest_ant * m_destino
            else: # Periódica
                tasa_resultado = tasa_periodica_dest_ant
        else:
            if tipo_destino == "Nominal":
                tasa_resultado = tasa_periodica_dest_ven * m_destino
            else: # Periódica
                tasa_resultado = tasa_periodica_dest_ven

    # Renderizado
    st.markdown("### Resultado de la Conversión")
    
    label_origen = f"{tasa_origen_ui:.8f}% {tipo_origen} {'Anticipada' if anticipada_origen else 'Vencida'}"
    if tipo_origen != "Efectiva":
        label_origen += f" ({capitalizacion_origen})"
        
    label_destino = f"{tasa_resultado*100:.8f}% {tipo_destino} {'Anticipada' if anticipada_destino else 'Vencida'}"
    if tipo_destino != "Efectiva":
        label_destino += f" ({capitalizacion_destino})"

    st.success(f"{label_origen}  ➔  **{label_destino}**")

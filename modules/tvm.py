import streamlit as st
import pandas as pd
import numpy_financial as npf
import plotly.graph_objects as go
from utils.plots import apply_custom_theme

def render_tvm():
    st.header("Módulo 2: Valor del Dinero en el Tiempo (TVM)")
    st.markdown("Calculadora avanzada para despejar incógnitas de Valor Presente, Valor Futuro, Pagos, Tasa o Periodos.")

    # Tarjeta base
    st.markdown("""
        <style>
        .box-container {
            background-color: #1e293b;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #00ffcc;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="box-container">', unsafe_allow_html=True)
    incognita = st.selectbox("¿Qué parámetro desea calcular?", [
        "Valor Presente (VP)",
        "Valor Futuro (VF)",
        "Pago / Cuota Constante (PMT)",
        "Tasa de Interés por Periodo (i)",
        "Número de Periodos (Nper)"
    ])
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # Entradas según la incógnita
    with col1:
        st.subheader("Parámetros Conocidos")
        
        # VP
        if incognita != "Valor Presente (VP)":
            vp = st.number_input("Valor Presente (VP)", value=-1000.0, step=100.0)
        else:
            vp = None
            
        # VF
        if incognita != "Valor Futuro (VF)":
            vf = st.number_input("Valor Futuro (VF)", value=0.0, step=100.0)
        else:
            vf = None
            
        # PMT
        if incognita != "Pago / Cuota Constante (PMT)":
            pmt = st.number_input("Pago Constante (PMT)", value=0.0, step=10.0)
        else:
            pmt = None

    with col2:
        st.subheader("Tiempo y Tasa")
        
        # Nper
        if incognita != "Número de Periodos (Nper)":
            nper = st.number_input("Número de periodos (N)", value=12, step=1)
        else:
            nper = None
            
        # Tasa
        if incognita != "Tasa de Interés por Periodo (i)":
            tasa_ui = st.number_input("Tasa de interés periódica (%)", value=1.5, step=0.1)
            tasa = tasa_ui / 100.0
        else:
            tasa = None
            tasa_ui = None
            
        tipo_pago = st.selectbox("Momento del pago", ["Vencido (Al final del periodo)", "Anticipado (Al inicio del periodo)"])
        when = 1 if "Anticipado" in tipo_pago else 0

    st.markdown("---")
    
    # Calcular Resultado
    try:
        st.subheader("Resultado")
        if incognita == "Valor Presente (VP)":
            resultado = npf.pv(tasa, nper, pmt, vf, when)
            st.success(f"**Valor Presente (VP):** \$ {resultado:,.2f}")
            vp = resultado
            
        elif incognita == "Valor Futuro (VF)":
            resultado = npf.fv(tasa, nper, pmt, vp, when)
            st.success(f"**Valor Futuro (VF):** \$ {resultado:,.2f}")
            vf = resultado
            
        elif incognita == "Pago / Cuota Constante (PMT)":
            resultado = npf.pmt(tasa, nper, vp, vf, when)
            st.success(f"**Pago Constante (PMT):** \$ {resultado:,.2f}")
            pmt = resultado
            
        elif incognita == "Tasa de Interés por Periodo (i)":
            resultado = npf.rate(nper, pmt, vp, vf, when)
            if not pd.isna(resultado):
                st.success(f"**Tasa de interés periódica (i):** {resultado*100:,.4f}%")
            else:
                st.error("No se pudo converger a una tasa con los datos proporcionados. Revise los signos.")
            tasa = resultado
            
        elif incognita == "Número de Periodos (Nper)":
            resultado = npf.nper(tasa, pmt, vp, vf, when)
            if not pd.isna(resultado):
                st.success(f"**Número de periodos continuos (N):** {resultado:,.2f} periodos")
            else:
                st.error("Los flujos provistos nunca alcanzan el valor futuro con la tasa seleccionada.")
            nper = resultado if not pd.isna(resultado) else 0

    except Exception as e:
        st.error(f"Error en el cálculo: Revise las convenciones de signos (+ Entradas, - Salidas). Detalles: {e}")

    # Diagrama de Flujo de Efectivo
    st.markdown("### Diagrama de Flujos de Efectivo")
    st.info("Visualización de las entradas y salidas de dinero a lo largo del tiempo de la operación.")
    
    if nper is not None and not pd.isna(nper) and 0 < nper <= 120:
        n_periods = int(round(nper, 0))
        periodos_list = list(range(n_periods + 1))
        flujos = [0.0] * (n_periods + 1)
        
        # VP en el periodo 0
        if vp is not None and not pd.isna(vp):
            flujos[0] += vp
            
        # Pagos en los periodos intermedios
        if pmt is not None and not pd.isna(pmt) and pmt != 0:
            start_idx = 0 if when == 1 else 1
            end_idx = n_periods if when == 1 else n_periods + 1
            for p in range(start_idx, end_idx):
                if p < len(flujos):
                    flujos[p] += pmt
                    
        # VF en el periodo final
        if vf is not None and not pd.isna(vf) and vf != 0:
            flujos[-1] += vf
            
        df_flujos = pd.DataFrame({"Periodo": periodos_list, "Flujo": flujos})
        
        # Ocultar texto grande, color dinámico
        colores = ['#00ffcc' if val >= 0 else '#ef4444' for val in flujos]
        text_labels = [f"{v:,.2f}" if v != 0 else "" for v in flujos]
        
        fig = go.Figure(data=[
            go.Bar(
                x=df_flujos['Periodo'], 
                y=df_flujos['Flujo'], 
                marker_color=colores, 
                text=text_labels, 
                textposition='auto',
                hovertemplate="Periodo: %{x}<br>Monto: $%{y:,.2f}<extra></extra>"
            )
        ])
        
        fig.update_layout(
            title="Diagrama de Flujo de Caja (Inflows / Outflows)",
            xaxis_title="Periodo de tiempo (n)",
            yaxis_title="Monto Monetario ($)",
            showlegend=False
        )
        fig = apply_custom_theme(fig)
        st.plotly_chart(fig, use_container_width=True)
    else:
        if nper is not None and (pd.isna(nper) or nper > 120):
            st.warning("El diagrama no se despliega para más de 120 periodos por claridad visual o debido a parámetros incompatibles.")

import streamlit as st
import pandas as pd
import numpy_financial as npf
import plotly.graph_objects as go
from utils.plots import apply_custom_theme

def render_amortizacion():
    st.header("Módulo 3: Tablas de Amortización de Créditos")
    st.markdown("Generador avanzado de esquemas de pago de deudas (Cuota Fija o Abono Constante) con opciones de periodo de gracia.")

    # Style removido

    # Configurador de Deuda
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="box-container" style="border-left: 5px solid #00ffcc;">', unsafe_allow_html=True)
        st.subheader("Condiciones del Crédito")
        monto_prestamo = st.number_input("Monto del Préstamo (VP)", value=100000.0, step=1000.0, min_value=0.0)
        tasa_anual_ui = st.number_input("Tasa de Interés Nominal Anual (%)", value=12.0, step=0.5)
        tasa_mensual = (tasa_anual_ui / 100.0) / 12  # Asumiendo pagos mensuales

        plazo_meses = st.number_input("Plazo Total (Meses)", value=60, step=1, min_value=1)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="box-container" style="border-left: 5px solid #3b82f6;">', unsafe_allow_html=True)
        st.subheader("Configuración de Pago")
        sistema = st.selectbox("Sistema de Amortización", ["Francés (Cuota Fija)", "Alemán (Abono Constante a Capital)"])
        
        meses_gracia = st.number_input("Periodos de Gracia (Meses al inicio)", value=0, step=1, min_value=0, max_value=plazo_meses-1 if plazo_meses > 1 else 0)
        
        tipo_gracia = "Sin pago"
        if meses_gracia > 0:
            tipo_gracia = st.radio("Manejo de los intereses durante la gracia:", ["Gracia de Capital (Paga solo intereses)", "Gracia Total (Intereses se capitalizan al saldo)"])
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    
    # --- LOGICA DE GENERACION DE TABLA ---
    
    if st.button("Generar Tabla de Amortización", use_container_width=True):
        tabla = []
        saldo_inicial = monto_prestamo
        saldo_antes_amortizacion = saldo_inicial
        periodos_amortizacion = plazo_meses - meses_gracia
        
        if periodos_amortizacion <= 0:
            st.error("El número de periodos de gracia no puede ser igual o mayor al plazo total del crédito.")
            return

        # Calcular nueva cuota para el metodo frances antes de la iteracion
        if sistema == "Francés (Cuota Fija)":
            if meses_gracia > 0 and tipo_gracia == "Gracia Total (Intereses se capitalizan al saldo)":
                saldo_antes_amortizacion = saldo_inicial * ((1 + tasa_mensual)**meses_gracia)
                
            cuota_fija = npf.pmt(tasa_mensual, periodos_amortizacion, -saldo_antes_amortizacion)
            
        elif sistema == "Alemán (Abono Constante a Capital)":
            if meses_gracia > 0 and tipo_gracia == "Gracia Total (Intereses se capitalizan al saldo)":
                saldo_antes_amortizacion = saldo_inicial * ((1 + tasa_mensual)**meses_gracia)
                
            abono_capital = saldo_antes_amortizacion / periodos_amortizacion
            
        saldo = saldo_inicial
        
        # Llenar la tabla cronologicamente
        for mes in range(1, plazo_meses + 1):
            if mes <= meses_gracia:
                if tipo_gracia == "Gracia Total (Intereses se capitalizan al saldo)":
                    interes = saldo * tasa_mensual
                    cuota = 0
                    capital = 0
                    saldo += interes
                    saldo_inicio_mes = saldo - interes
                else: # Gracia de capital solo paga intereses
                    interes = saldo * tasa_mensual
                    cuota = interes
                    capital = 0
                    saldo_inicio_mes = saldo
            else:
                saldo_inicio_mes = saldo
                interes = saldo * tasa_mensual
                
                if sistema == "Francés (Cuota Fija)":
                    cuota = cuota_fija
                    capital = cuota - interes
                else: # Alemán
                    capital = abono_capital
                    cuota = capital + interes
                    
                saldo -= capital
                
                # Prevenir residual flotante pequeño final para no descuadrar a negativo
                if saldo < 0.01:
                    saldo = 0

            tabla.append({
                "Mes": mes,
                "Saldo Inicial": saldo_inicio_mes,
                "Cuota (Pago)": cuota,
                "Interés": interes,
                "Abono a Capital": capital,
                "Saldo Final": saldo
            })
            
        df = pd.DataFrame(tabla)
        
        # Mostrar KPIs analiticos
        st.subheader("Resumen del Crédito")
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Total Intereses Pagados", f"${df['Interés'].sum():,.2f}")
        kpi2.metric("Monto Total Entregado", f"${df['Cuota (Pago)'].sum():,.2f}")
        kpi3.metric("Tasa Efectiva Anual (TEA)", f"{((1+tasa_mensual)**12 - 1)*100:,.2f}%")
        
        # Visualizar dataframe interactivo de Pandas
        st.subheader("Cuadro de Amortización")
        st.dataframe(
            df.style.format({
                "Saldo Inicial": "${:,.2f}",
                "Cuota (Pago)": "${:,.2f}",
                "Interés": "${:,.2f}",
                "Abono a Capital": "${:,.2f}",
                "Saldo Final": "${:,.2f}"
            }), 
            use_container_width=True
        )

        # Crear opcion de descargar a CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar Tabla en CSV",
            data=csv,
            file_name='tabla_amortizacion.csv',
            mime='text/csv',
        )

        st.markdown("### Gráficos de Evolución de la Deuda")
        tab1, tab2 = st.tabs(["Composición de la Cuota Automática", "Evolución del Saldo Remanente"])
        
        with tab1:
            fig_comp = go.Figure(data=[
                go.Bar(name='Abono a Capital', x=df['Mes'], y=df['Abono a Capital'], marker_color='#3b82f6'),
                go.Bar(name='Interés de Periodo', x=df['Mes'], y=df['Interés'], marker_color='#ef4444')
            ])
            fig_comp.update_layout(
                barmode='stack', 
                title="Desagregación Histórica de las Cuotas",
                xaxis_title="Mes / Periodo", 
                yaxis_title="Monto ($)"
            )
            fig_comp = apply_custom_theme(fig_comp)
            st.plotly_chart(fig_comp, use_container_width=True)
            
        with tab2:
            fig_saldo = go.Figure()
            fig_saldo.add_trace(go.Scatter(x=df['Mes'], y=df['Saldo Final'], fill='tozeroy', mode='lines+markers', name='Saldo de la Deuda', line=dict(color='#00ffcc', width=3)))
            fig_saldo.update_layout(
                title="Caída del Saldo a Nivel Histórico",
                xaxis_title="Mes / Periodo", 
                yaxis_title="Monto del Saldo Remanente ($)"
            )
            fig_saldo = apply_custom_theme(fig_saldo)
            st.plotly_chart(fig_saldo, use_container_width=True)

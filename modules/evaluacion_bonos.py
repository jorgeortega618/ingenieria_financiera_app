import streamlit as st
import pandas as pd
import numpy_financial as npf
import plotly.graph_objects as go
from utils.plots import apply_custom_theme

def render_evaluacion_bonos():
    st.header("Módulo 5: Evaluación de Proyectos y Bonos Corporativos")
    
    # Style transferido
    
    tab_proy, tab_bonos = st.tabs(["Evaluación de Proyectos FCF", "Valoración de Bonos Financieros"])
    
    with tab_proy:
        st.subheader("Evaluación Financiera Basada en Flujos de Efectivo Libre (FCF)")
        
        # Checking if session state has FCF
        if 'fcf_proyectado' in st.session_state and len(st.session_state['fcf_proyectado']) > 0:
            flujos = st.session_state['fcf_proyectado']
            wacc_sugerido = st.session_state.get('wacc_tasa', 12.0)
            st.success(f"Confirmación: Flujos de Efectivo Libres del Módulo 4 cargados exitosamente (Horizonte: {len(flujos)-1} años).")
        else:
            flujos = [-50000, 15000, 20000, 25000, 30000, 10000]
            wacc_sugerido = 12.0
            st.warning("No se detectaron flujos en memoria provenientes del Módulo 4. Se utilizarán flujos de demostración comerciales. Genérelos en el Módulo 4 para un análisis íntegro.")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="box-container" style="border-left: 5px solid #00ffcc;">', unsafe_allow_html=True)
            wacc = st.number_input("Tasa de Descuento Institucional (WACC / TIO) (%)", value=wacc_sugerido, step=0.5) / 100
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="box-container" style="border-left: 5px solid #3b82f6;">', unsafe_allow_html=True)
            st.markdown(f"**Caja Inicial (Inversión):** ${flujos[0]:,.2f}")
            st.markdown(f"**Caja Final (Terminal/Salvamento):** ${flujos[-1]:,.2f}")
            st.markdown('</div>', unsafe_allow_html=True)

        # Calcular Metricas
        try:
            vpn = npf.npv(wacc, flujos)
            tir = npf.irr(flujos)
            
            # Rentabilidad
            st.markdown("---")
            st.subheader("Indicadores de Viabilidad y Rentabilidad")
            k1, k2, k3 = st.columns(3)
            
            # Evaluacion Logica para colorear
            vp_inflows = npf.npv(wacc, [max(0, f) for f in flujos])
            vpn_outflows = abs(npf.npv(wacc, [min(0, f) for f in flujos]))
            rbc = vp_inflows / vpn_outflows if vpn_outflows != 0 else 0
            
            k1.metric("Valor Presente Neto (VPN)", f"${vpn:,.2f}", f"Proyecto Viable" if vpn > 0 else "Destruye Valor", delta_color="normal" if vpn > 0 else "inverse")
            
            if not pd.isna(tir):
                k2.metric("Tasa Interna de Retorno (TIR)", f"{tir*100:,.2f}%", f"{((tir-wacc)*100):,.2f} pp sobre WACC" if (tir-wacc) > 0 else "Bajo WACC", delta_color="normal" if tir > wacc else "inverse")
            else:
                k2.metric("Tasa Interna de Retorno (TIR)", "Matemáticamente Compleja")
                
            # Calcular Payback simple
            acumulado = 0
            payback = -1
            for t, f in enumerate(flujos):
                acumulado += f
                if acumulado >= 0 and t > 0:
                    # Interpolación lineal para fracciones
                    flujo_prev = acumulado - f
                    fraccion = abs(flujo_prev) / f if f != 0 else 0
                    payback = (t - 1) + fraccion
                    break
                    
            if payback != -1:
                k3.metric("Periodo de Recuperación Promedio (Payback)", f"{payback:,.1f} años", f"Relación B/C: {rbc:.2f}x")
            else:
                k3.metric("Periodo de Recuperación Promedio (Payback)", "No Recupera la Inversión Inicial")
                
            # Grafico Perfil del VPN
            st.markdown("---")
            st.markdown("### Perfil del Valor Presente Neto (Sensibilidad a la Tasa de Descuento)")
            
            tasas_plot = [i / 1000.0 for i in range(1, 400, 5)] # 0.1% to 40%
            vpns_plot = [npf.npv(t, flujos) for t in tasas_plot]
            
            df_perfil = pd.DataFrame({"Tasa Descuento": tasas_plot, "VPN": vpns_plot})
            
            fig_perfil = go.Figure()
            fig_perfil.add_trace(go.Scatter(x=df_perfil['Tasa Descuento']*100, y=df_perfil['VPN'], mode='lines', fill='tozeroy', name='Curva VPN', line=dict(color='#00ffcc', width=3)))
            
            # Línea de Break-even
            fig_perfil.add_trace(go.Scatter(
                x=[df_perfil['Tasa Descuento'].min()*100, df_perfil['Tasa Descuento'].max()*100],
                y=[0, 0],
                mode="lines",
                name="Frontera de Rentabilidad (VPN = 0)",
                line=dict(color="#ef4444", width=2, dash="dash")
            ))
            
            # Punto TIR
            if not pd.isna(tir) and tir > 0 and tir < 0.5: # Mostrable solo si es razonable
                fig_perfil.add_trace(go.Scatter(
                    x=[tir*100], 
                    y=[0], 
                    mode='markers+text', 
                    name='TIR', 
                    text=[f"TIR: {tir*100:,.1f}%"],
                    textposition="top right",
                    marker=dict(color='#3b82f6', size=14, symbol="x")
                ))
                
            fig_perfil.update_layout(
                xaxis_title="Tasa de Descuento / TIO (%)",
                yaxis_title="Valor Presente Neto (VPN) Monetario",
                hovermode="x unified"
            )
            fig_perfil = apply_custom_theme(fig_perfil)
            st.plotly_chart(fig_perfil, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error procesando los flujos intermedios para la evaluación técnica: {e}")
            
    with tab_bonos:
        st.subheader("Herramienta de Valoración de Bonos de Renta Fija Corporativa")
        
        c_b1, c_b2 = st.columns(2)
        with c_b1:
            st.markdown('<div class="box-container" style="border-left: 5px solid #00ffcc;">', unsafe_allow_html=True)
            nominal = st.number_input("Valor Nominal / Par ($)", value=1000.0, step=100.0)
            tasa_cupon = st.number_input("Tasa Cupón Anual Asegurada (%)", value=8.0, step=0.1) / 100
            st.markdown('</div>', unsafe_allow_html=True)
            
        with c_b2:
            st.markdown('<div class="box-container" style="border-left: 5px solid #3b82f6;">', unsafe_allow_html=True)
            ytm_ui = st.number_input("Tasa Interna de Rendimiento Solicitada al Vencimiento (YTM) (%)", value=10.0, step=0.1) / 100
            n_bono = st.number_input("Horizonte Madurativo Restante (Años)", value=10, step=1)
            freq_pago = st.selectbox("Iteración de Pago Semestral/Anual del Cupón", ["Anual (1 Pago por Año)", "Semestral (2 Pagos por Año)"])
            m_bono = 1 if "Anual" in freq_pago else 2
            st.markdown('</div>', unsafe_allow_html=True)
            
        if st.button("Ejecutar Valoración de Precio Sucio/Limpio", use_container_width=True):
            n_periodos_bono = n_bono * m_bono
            ytm_periodica = ytm_ui / m_bono
            cupon_periodico = (nominal * tasa_cupon) / m_bono
            
            # Proyeccionar de flujos de caja del yield maturity de un bono tipico
            flujos_bono = [cupon_periodico] * n_periodos_bono
            flujos_bono[-1] += nominal # Devuelve principal (bullet debt structure)
            
            # Calcular Precio (VPN de los flujos del bono a la tasa YTM)
            precio_bono = sum([f / ((1 + ytm_periodica)**(t+1)) for t, f in enumerate(flujos_bono)])
            
            # Calcular Duración de Macaulay
            mac_dur_num = sum([(t+1) * (f / ((1 + ytm_periodica)**(t+1))) for t, f in enumerate(flujos_bono)])
            macaulay_duration = mac_dur_num / precio_bono
            # Normalizar de regreso a equivalencia de años
            macaulay_duration /= m_bono
            
            mod_duration = macaulay_duration / (1 + ytm_periodica)
            
            st.markdown("---")
            st.markdown("### Resultado Técnico de Negociación (Bond Pricing)")
            
            col_res1, col_res2, col_res3 = st.columns(3)
            
            # Definir si se vende a premio, descuento o a la par ex
            condicion = "Al Valor Par"
            color_c = "normal"
            if precio_bono < nominal:
                condicion = "Transa Con Descuento Operacional (Bajo Par)"
                color_c = "inverse"
            elif precio_bono > nominal:
                condicion = "Transa Con Prima Operacional (Sobre Par)"
                
            col_res1.metric("Precio Limpio Calculado del Bono", f"${precio_bono:,.2f}", condicion, delta_color=color_c)
            col_res2.metric("Duración de Macaulay Extendida", f"{macaulay_duration:,.2f} Años Efectivos", "Exposición Temporal/Riesgo Tasa")
            col_res3.metric("Duración Modificada Financiera", f"{mod_duration:,.2f} Años", f"-{mod_duration:,.2f}% delta per +1% cambio de YTM", delta_color="inverse")
            
            st.info("Nota: La métrica de **Duración Modificada** establece la sensibilidad volátil del principal de capital estructurado ante un choque exógeno en la tasa directriz del ecosistema de capital (YTM).")
            
            # Visualizar cascada simple para bond layout
            st.markdown("**Simulación de Esquema Estructurado Tranche de Pagos del Título:**")
            df_b = pd.DataFrame({
                "Periodo Despliegue de Pagos de Amortización": range(1, n_periodos_bono + 1),
                "Volumen Pactado": flujos_bono
            })
            st.bar_chart(df_b.set_index("Periodo Despliegue de Pagos de Amortización"), color="#00ffcc", use_container_width=True)

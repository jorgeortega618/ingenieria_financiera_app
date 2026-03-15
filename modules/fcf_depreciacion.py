import streamlit as st
import pandas as pd
import numpy_financial as npf
import plotly.graph_objects as go
from utils.plots import apply_custom_theme

def render_fcf_depreciacion():
    st.header("Módulo 4: Flujo de Efectivo Libre y Depreciación")
    st.markdown("Proyecte escenarios financieros definiendo horizontes de años, esquemas de depreciación y flujos operativos con cuadrículas editables.")

    # Style transferido

    # 1. Configuración General
    st.markdown('<div class="box-container" style="border-left: 5px solid #00ffcc;">', unsafe_allow_html=True)
    st.subheader("1. Configuración del Proyecto")
    col1, col2, col3 = st.columns(3)
    horizonte = col1.number_input("Horizonte de Proyección (Años)", min_value=1, max_value=20, value=5, step=1)
    tasa_impositiva = col2.number_input("Tasa de Impuestos (%)", min_value=0.0, max_value=100.0, value=30.0, step=0.1) / 100
    wacc_ui = col3.number_input("WACC / Tasa de Descuento (%)", min_value=0.0, max_value=100.0, value=12.0, step=0.1)
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. Configuración de Activos y Depreciación
    st.markdown('<div class="box-container" style="border-left: 5px solid #3b82f6;">', unsafe_allow_html=True)
    st.subheader("2. Activos de Capital y Tipo de Depreciación")
    col_d1, col_d2, col_d3 = st.columns(3)
    inversion_inicial = col_d1.number_input("Inversión Inicial de Activos (CAPEX Año 0)", min_value=0.0, value=50000.0, step=1000.0)
    valor_salvamento = col_d2.number_input("Valor Comercial de Salvamento (Año Final)", min_value=0.0, value=5000.0, step=1000.0)
    metodo_dep = col_d3.selectbox("Método de Depreciación", ["Línea Recta", "Suma de los Dígitos (SYD)", "Saldos Doblemente Declinantes (DDB)"])
    st.markdown('</div>', unsafe_allow_html=True)

    # Motor de Cálculo de Depreciación
    costo_depreciable = inversion_inicial - valor_salvamento
    depreciacion_anual = [0.0] * horizonte
    valor_libros = [inversion_inicial] * (horizonte + 1)

    if inversion_inicial > 0:
        for t in range(1, horizonte + 1):
            if metodo_dep == "Línea Recta":
                depreciacion_anual[t-1] = costo_depreciable / horizonte
            elif metodo_dep == "Suma de los Dígitos (SYD)":
                syd = sum(range(1, horizonte + 1))
                fraccion = (horizonte - t + 1) / syd
                depreciacion_anual[t-1] = costo_depreciable * fraccion
            elif metodo_dep == "Saldos Doblemente Declinantes (DDB)":
                tasa_ddb = 2 / horizonte
                if t == horizonte: # Ajuste contable al final para llegar al valor residual excato
                    dep_calculada = valor_libros[t-1] - valor_salvamento
                else:
                    dep_calculada = valor_libros[t-1] * tasa_ddb
                    if (valor_libros[t-1] - dep_calculada) < valor_salvamento:
                        dep_calculada = valor_libros[t-1] - valor_salvamento
                depreciacion_anual[t-1] = max(0, dep_calculada)
            
            valor_libros[t] = valor_libros[t-1] - depreciacion_anual[t-1]

    # Desplegar Cuadro Opcional de Depreciación
    with st.expander("Ver Programa de Depreciación Generado Automáticamente"):
        df_dep = pd.DataFrame({
            "Periodo (Año)": range(1, horizonte + 1),
            "Gasto por Depreciación Aplicado": depreciacion_anual,
            "Valor Contable en Libros (Final de Año)": valor_libros[1:]
        })
        st.dataframe(df_dep.style.format({"Gasto por Depreciación Aplicado": "${:,.2f}", "Valor Contable en Libros (Final de Año)": "${:,.2f}"}), use_container_width=True)

    # 3. Flujo Operativo Editable
    st.markdown("---")
    st.subheader("3. Proyección de Estado de Resultados y Capital de Trabajo Modificable")
    st.info("Nota: Edite libremente las celdas de la tabla para modelar los ingresos, costos y las necesidades de KT cada año del proyecto.")
    
    # Dataset Base Formulado
    base_data = {
        "Definición": ["Ingresos por Ventas Proyectados", "Costo de Ventas Directo (COGS)", "Gastos Operativos (SG&A)", "Nuevo CAPEX / Adiciones de Activos", "Ampliación de Capital de Trabajo (Δ KT)"]
    }
    for t in range(1, horizonte + 1):
        # Escenarios dummy predeterminados
        base_data[f"Año {t}"] = [
            round(100000.0 * (1.05**(t-1)), 0),  
            round(40000.0 * (1.05**(t-1)), 0),   
            round(20000.0 * (1.03**(t-1)), 0),   
            0.0,                       
            2000.0                     
        ]
        
    df_operativo = pd.DataFrame(base_data)
    edited_df = st.data_editor(df_operativo, hide_index=True, use_container_width=True)

    # 4. Consolidacion FCF
    st.markdown("---")
    st.subheader("4. Matriz Condensada de Flujo de Efectivo Libre (FCF)")
    
    fcf_table = []
    
    # Rastrear FCF por año
    fcf_table.append({
        "Año Métrica": "Año 0",
        "EBITDA": 0.0,
        "Gasto por Dep.": 0.0,
        "EBIT Operativo": 0.0,
        "Tasa Impuestos 30%": 0.0,
        "NOPAT Generado": 0.0,
        "(+) Depreciación (Non-cash)": 0.0,
        "(-) CAPEX": inversion_inicial,
        "(-) Δ KT": 0.0,
        "+ Salvamento Terminal": 0.0,
        "Flujo de Efectivo Libre (FCF)": -inversion_inicial
    })
    
    fcf_totales = [-inversion_inicial] 
    
    for t in range(1, horizonte + 1):
        col_name = f"Año {t}"
        ingresos = edited_df.loc[edited_df["Definición"] == "Ingresos por Ventas Proyectados", col_name].values[0]
        cogs = edited_df.loc[edited_df["Definición"] == "Costo de Ventas Directo (COGS)", col_name].values[0]
        sga = edited_df.loc[edited_df["Definición"] == "Gastos Operativos (SG&A)", col_name].values[0]
        capex_ext = edited_df.loc[edited_df["Definición"] == "Nuevo CAPEX / Adiciones de Activos", col_name].values[0]
        delta_kt = edited_df.loc[edited_df["Definición"] == "Ampliación de Capital de Trabajo (Δ KT)", col_name].values[0]
        
        depreciacion = depreciacion_anual[t-1]
        
        ebitda = ingresos - cogs - sga
        ebit = ebitda - depreciacion
        impuestos = max(0, ebit * tasa_impositiva) # Impuesto estimado base sobre rentabilidad
        nopat = ebit - impuestos
        
        fcf = nopat + depreciacion - capex_ext - delta_kt
        
        # Consideracion terminal
        salva_term = 0.0
        if t == horizonte:
            salva_term = valor_salvamento
            fcf += salva_term
            st.warning(f"Aviso: En el Año {horizonte} se adiciona Flujo de Caja Terminal por un Valor de Rescate de Salvamento Comercial (${valor_salvamento:,.2f}).")

        fcf_totales.append(fcf)
        
        fcf_table.append({
            "Año Métrica": f"Año {t}",
            "EBITDA": ebitda,
            "Gasto por Dep.": depreciacion,
            "EBIT Operativo": ebit,
            "Tasa Impuestos 30%": impuestos,
            "NOPAT Generado": nopat,
            "(+) Depreciación (Non-cash)": depreciacion,
            "(-) CAPEX": capex_ext,
            "(-) Δ KT": delta_kt,
            "+ Salvamento Terminal": salva_term,
            "Flujo de Efectivo Libre (FCF)": fcf
        })

    df_fcf = pd.DataFrame(fcf_table)
    st.dataframe(
        df_fcf.style.format(formatter="${:,.0f}", subset=df_fcf.columns[1:]),
        use_container_width=True
    )
    
    # Store FCF list globally for the other module 
    st.session_state['fcf_proyectado'] = fcf_totales
    st.session_state['wacc_tasa'] = wacc_ui
    
    # 5. Visualizacion Waterfall con Plotly de ultima cascada
    st.markdown("---")
    st.markdown(f"### Estructura en Cascada (Waterfall) del Efectivo en el Último Año (Año {horizonte})")
    
    ultimo_fcf = fcf_table[-1]
    
    labels_cas = ["Ingresos Brutos", "Descuentos Op. (COGS+SG&A)", "Total EBITDA", "Cargo de Depreciación", "Resultado EBIT", "Carga Impositiva", "Total NOPAT", "Reintegro Depreciación", "Ajustes de Adiciones (CAPEX/KT/Salvamento)", "FCF Periodo"]
    measures_cas = ["relative", "relative", "total", "relative", "total", "relative", "total", "relative", "relative", "total"]
    
    total_costos_op = abs(ultimo_fcf["EBITDA"] - ingresos) # Should match COGS + SGA indirectly
    ajustes_terminales = -ultimo_fcf["(-) CAPEX"] - ultimo_fcf["(-) Δ KT"] + ultimo_fcf["+ Salvamento Terminal"]
    
    values_cas = [
        ingresos, 
        -total_costos_op,
        ultimo_fcf["EBITDA"], 
        -ultimo_fcf["Gasto por Dep."], 
        ultimo_fcf["EBIT Operativo"], 
        -ultimo_fcf["Tasa Impuestos 30%"], 
        ultimo_fcf["NOPAT Generado"], 
        ultimo_fcf["(+) Depreciación (Non-cash)"], 
        ajustes_terminales, 
        ultimo_fcf["Flujo de Efectivo Libre (FCF)"]
    ]
    
    text_valores = [f"${abs(v):,.0f}" if v != 0 else "" for v in values_cas]
    
    # Fix 'total' elements to be 0 matching standard waterfall plotting config length unless explicit calculation logic applies.
    # Actually in plotly total items are calculated directly. We write 0 over them.
    for i, m in enumerate(measures_cas):
        if m == "total":
            values_cas[i] = 0

    fig_waterfall = go.Figure(go.Waterfall(
        name="Análisis de FCF", orientation="v",
        measure=measures_cas,
        x=labels_cas,
        textposition="outside",
        text=text_valores,
        y=values_cas,
        connector={"line": {"color": "rgb(80, 80, 80)", "width": 1.5}},
        decreasing={"marker": {"color": "#ef4444"}},
        increasing={"marker": {"color": "#10b981"}},
        totals={"marker": {"color": "#00ffcc"}}
    ))

    fig_waterfall.update_layout(
        title=f"Mecanismo Fiscal de Formación del Cierre Financiero (Año {horizonte})",
        showlegend=False,
        margin=dict(l=40, r=40, t=60, b=100) # Give extra bottom room
    )
    fig_waterfall = apply_custom_theme(fig_waterfall)
    st.plotly_chart(fig_waterfall, use_container_width=True)
    
    st.success("Cálculo Completado. Los Flujos de Efectivo Libres (FCF) han sido calculados de manera iterativa y almacenados en el Estado de Sesión en Memoria. Diríjase ahora al Módulo 5 (Evaluación de Proyectos y Bonos) para consolidar sus métricas terminales de ingeniería como VPN y TIR.")


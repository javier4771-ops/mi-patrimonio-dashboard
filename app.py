import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Patrimonio Familiar Javier y Blanca",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ESTILO CSS PERSONALIZADO (ALTO CONTRASTE Y MODO OSCURO PRO) ---
st.markdown("""
<style>
    /* Estilo fondo oscuro antracita */
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    
    /* Textos generales con alto contraste */
    p, span, label, div {
        color: #E2E8F0 !important;
        font-size: 15px;
    }
    
    /* Tarjetas KPI estilo Hero Pro */
    .kpi-card {
        background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%);
        border-radius: 14px;
        padding: 22px;
        border: 1px solid #334155;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
        margin-bottom: 15px;
    }
    
    .kpi-title {
        color: #94A3B8 !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    
    .kpi-value {
        font-size: 32px !important;
        font-weight: 800 !important;
        color: #FFFFFF !important;
    }
    
    .kpi-sub {
        font-size: 14px !important;
        font-weight: 600 !important;
        color: #38BDF8 !important;
        margin-top: 6px;
    }
    
    /* Tabs Navegación */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #1E293B;
        padding: 8px;
        border-radius: 12px;
        border: 1px solid #334155;
    }

    .stTabs [data-baseweb="tab"] {
        color: #94A3B8 !important;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background-color: #0284C7 !important;
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# --- INICIALIZACIÓN DE DATOS EN SESIÓN ---
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame([
        # Liquidez
        {"Categoría": "Liquidez", "Entidad": "Openbank", "Producto": "Cuenta Ahorro 1.5%", "Titular": "Javi", "Importe": 5700.0, "Tipo": "Activo", "Divisa": "EUR"},
        {"Categoría": "Liquidez", "Entidad": "ING", "Producto": "Cuenta Ahorro 1.5%", "Titular": "Javi", "Importe": 100.0, "Tipo": "Activo", "Divisa": "EUR"},
        {"Categoría": "Liquidez", "Entidad": "Trade Republic", "Producto": "Caja 2%", "Titular": "Javi", "Importe": 16.0, "Tipo": "Activo", "Divisa": "EUR"},
        {"Categoría": "Liquidez", "Entidad": "Cash", "Producto": "Efectivo", "Titular": "Javi", "Importe": 2500.0, "Tipo": "Activo", "Divisa": "EUR"},
        
        # Inversiones
        {"Categoría": "Inversión / Brokers", "Entidad": "Interactive Brokers", "Producto": "Acciones / ETFs", "Titular": "Javi", "Importe": 75810.0, "Tipo": "Activo", "Divisa": "USD"},
        {"Categoría": "Inversión / Brokers", "Entidad": "DEGIRO Javi", "Producto": "Acciones Europa", "Titular": "Javi", "Importe": 23500.0, "Tipo": "Activo", "Divisa": "EUR"},
        {"Categoría": "Inversión / Brokers", "Entidad": "Renta 4", "Producto": "TV Compounders", "Titular": "Javi", "Importe": 6800.0, "Tipo": "Activo", "Divisa": "EUR"},
        {"Categoría": "Inversión / Brokers", "Entidad": "Trade Republic", "Producto": "Cartera Acciones", "Titular": "Javi", "Importe": 3800.0, "Tipo": "Activo", "Divisa": "EUR"},
        {"Categoría": "Inversión / Brokers", "Entidad": "DEGIRO Blanca", "Producto": "Acciones Blanca", "Titular": "Blanca", "Importe": 1300.0, "Tipo": "Activo", "Divisa": "EUR"},
        
        # Cripto
        {"Categoría": "Criptoactivos", "Entidad": "Criptan", "Producto": "Satoshis / BTC", "Titular": "Javi", "Importe": 3050.0, "Tipo": "Activo", "Divisa": "EUR"},
        {"Categoría": "Criptoactivos", "Entidad": "Ledger", "Producto": "Satoshis / Cold Storage", "Titular": "Javi", "Importe": 2900.0, "Tipo": "Activo", "Divisa": "EUR"},
        
        # Pensiones
        {"Categoría": "Planes de Pensiones", "Entidad": "ING Direct", "Producto": "Plan Pensión Javi", "Titular": "Javi", "Importe": 18500.0, "Tipo": "Activo", "Divisa": "EUR"},
        {"Categoría": "Planes de Pensiones", "Entidad": "ING Direct", "Producto": "Plan Pensión Blanca", "Titular": "Blanca", "Importe": 15500.0, "Tipo": "Activo", "Divisa": "EUR"},
        {"Categoría": "Planes de Pensiones", "Entidad": "Openbank", "Producto": "Plan Pensión Javi", "Titular": "Javi", "Importe": 68.0, "Tipo": "Activo", "Divisa": "EUR"},
        
        # Pasivos
        {"Categoría": "Deudas / Hipoteca", "Entidad": "Banco Principal", "Producto": "Hipoteca Vivienda", "Titular": "Compartido", "Importe": 43800.0, "Tipo": "Pasivo", "Divisa": "EUR"}
    ])

df = st.session_state.data

# CÁLCULOS GENERALES
activos = df[df["Tipo"] == "Activo"]["Importe"].sum()
pasivos = df[df["Tipo"] == "Pasivo"]["Importe"].sum()
patrimonio_neto = activos - pasivos
liquidez = df[df["Categoría"] == "Liquidez"]["Importe"].sum()

# --- ENCABEZADO ---
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.title("🏛️ Patrimonio Familiar Javier y Blanca")
with col_head2:
    ocultar = st.checkbox("🙈 Ocultar Importes")

def fmt(valor, es_moneda=True):
    if ocultar:
        return "•••••• €" if es_moneda else "••••••"
    return f"{valor:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".") if es_moneda else f"{valor:,.2f}"

# --- NAVEGACIÓN ---
tab_patrimonio, tab_divisas, tab_posiciones, tab_historico = st.tabs([
    "📊 Panel Principal", "💱 Reparto & Titular", "⚙️ Gestionar Posiciones", "📈 Evolución Histórica"
])

# ==========================================
# PESTAÑA 1: PATRIMONIO
# ==========================================
with tab_patrimonio:
    # HERO CARD
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); border-radius: 18px; padding: 28px; border: 1px solid #38BDF8; margin-bottom: 24px;">
        <span style="color: #94A3B8; font-size: 16px; font-weight: 700; text-transform: uppercase;">PATRIMONIO NETO TOTAL</span>
        <h1 style="color: #FFFFFF; font-size: 52px; font-weight: 900; margin: 10px 0;">{fmt(patrimonio_neto)}</h1>
        <div style="display: flex; gap: 24px; margin-top: 14px;">
            <span style="color: #4ADE80; font-size: 17px; font-weight: 700;">▲ Activos Totales: {fmt(activos)}</span>
            <span style="color: #F87171; font-size: 17px; font-weight: 700;">▼ Hipoteca / Deuda: {fmt(pasivos)}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # KPIS SECUNDARIOS
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Liquidez Inmediata</div>
            <div class="kpi-value">{fmt(liquidez)}</div>
            <div class="kpi-sub">{(liquidez/activos*100):.1f}% del total</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        inversion = df[df["Categoría"] == "Inversión / Brokers"]["Importe"].sum()
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Bolsa e Inversiones</div>
            <div class="kpi-value">{fmt(inversion)}</div>
            <div class="kpi-sub">{(inversion/activos*100):.1f}% del total</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        pensiones = df[df["Categoría"] == "Planes de Pensiones"]["Importe"].sum()
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Planes de Pensiones</div>
            <div class="kpi-value">{fmt(pensiones)}</div>
            <div class="kpi-sub">{(pensiones/activos*100):.1f}% del total</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        cripto = df[df["Categoría"] == "Criptoactivos"]["Importe"].sum()
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Criptoactivos</div>
            <div class="kpi-value">{fmt(cripto)}</div>
            <div class="kpi-sub">{(cripto/activos*100):.1f}% del total</div>
        </div>
        """, unsafe_allow_html=True)

    # GRÁFICOS VISUALES MEJORADOS
    st.write("---")
    st.subheader("📌 Distribución Visual del Patrimonio")
    c_graf1, c_graf2 = st.columns(2)
    
    df_activos = df[df["Tipo"] == "Activo"]
    
    with c_graf1:
        fig_donut = px.pie(
            df_activos, 
            values='Importe', 
            names='Categoría', 
            hole=0.55,
            title="<b>Distribución por Categoría</b>",
            color_discrete_sequence=['#38BDF8', '#4ADE80', '#FACC15', '#F43F5E', '#A855F7']
        )
        fig_donut.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#0F172A', width=3)))
        fig_donut.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font=dict(color='#F8FAFC', size=14),
            showlegend=False
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        
    with c_graf2:
        df_entidad = df_activos.groupby("Entidad")["Importe"].sum().reset_index().sort_values("Importe", ascending=True)
        fig_bar = px.bar(
            df_entidad, 
            x='Importe', 
            y='Entidad', 
            orientation='h',
            title="<b>Capital por Banco / Entidad</b>",
            color='Importe',
            color_continuous_scale='Blues'
        )
        fig_bar.update_traces(marker_line_color='#0F172A', marker_line_width=2, opacity=0.9)
        fig_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font=dict(color='#F8FAFC', size=14),
            coloraxis_showscale=False,
            xaxis=dict(showgrid=True, gridcolor='#334155'),
            yaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

# ==========================================
# PESTAÑA 2: REPARTO POR DIVISA Y TITULAR
# ==========================================
with tab_divisas:
    st.subheader("💱 Desglose Avanzado por Divisa y Titular")
    c_div1, c_div2 = st.columns(2)
    
    with c_div1:
        df_div = df_activos.groupby("Divisa")["Importe"].sum().reset_index()
        fig_div = px.pie(
            df_div, values="Importe", names="Divisa", hole=0.5,
            title="<b>Reparto por Divisa</b>",
            color_discrete_sequence=['#0284C7', '#10B981', '#F59E0B']
        )
        fig_div.update_traces(textinfo='percent+label', marker=dict(line=dict(color='#0F172A', width=3)))
        fig_div.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#F8FAFC', size=14))
        st.plotly_chart(fig_div, use_container_width=True)
        
    with c_div2:
        df_tit = df.groupby(["Titular", "Tipo"])["Importe"].sum().reset_index()
        fig_tit = px.bar(
            df_tit, x="Titular", y="Importe", color="Tipo", barmode="group",
            title="<b>Patrimonio por Titular (Javi vs Blanca vs Compartido)</b>",
            color_discrete_map={"Activo": "#4ADE80", "Pasivo": "#F87171"}
        )
        fig_tit.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#F8FAFC', size=14),
            yaxis=dict(showgrid=True, gridcolor='#334155')
        )
        st.plotly_chart(fig_tit, use_container_width=True)

# ==========================================
# PESTAÑA 3: GESTIONAR POSICIONES (INTERACTIVA)
# ==========================================
with tab_posiciones:
    st.subheader("⚙️ Panel de Gestión Interactivo")
    st.write("Modifica cualquier campo con los desplegables, añade nuevas cuentas o actualiza importes. Al pulsar guardar, la app actualizará todos los gráficos.")
    
    # FORMULARIO
    with st.expander("➕ Añadir Nueva Cuenta, Banco o Activo"):
        with st.form("form_nueva_posicion"):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                f_cat = st.selectbox("Categoría", ["Liquidez", "Inversión / Brokers", "Criptoactivos", "Planes de Pensiones", "Deudas / Hipoteca"])
                f_ent = st.text_input("Banco / Entidad (ej. MyInvestor, Openbank)")
                f_prod = st.text_input("Producto / Concepto (ej. Depósito 3%, Fondo Indexado)")
            with col_f2:
                f_tit = st.selectbox("Titular", ["Javi", "Blanca", "Compartido"])
                f_imp = st.number_input("Importe (€)", min_value=0.0, value=1000.0, step=100.0)
                f_div = st.selectbox("Divisa", ["EUR", "USD", "GBP"])
            
            f_tipo = "Pasivo" if f_cat == "Deudas / Hipoteca" else "Activo"
            submitted = st.form_submit_button("💾 Guardar Posición")
            
            if submitted and f_ent:
                nueva_fila = {
                    "Categoría": f_cat, "Entidad": f_ent, "Producto": f_prod, 
                    "Titular": f_tit, "Importe": f_imp, "Tipo": f_tipo, "Divisa": f_div
                }
                st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([nueva_fila])], ignore_index=True)
                st.success(f"¡Posición en {f_ent} añadida!")
                st.rerun()

    # TABLA EDITABLE CON DESPLEGABLES
    st.write("### 📝 Editar Posiciones Existentes")
    
    cat_options = ["Liquidez", "Inversión / Brokers", "Criptoactivos", "Planes de Pensiones", "Deudas / Hipoteca"]
    titular_options = ["Javi", "Blanca", "Compartido"]
    tipo_options = ["Activo", "Pasivo"]
    divisa_options = ["EUR", "USD", "GBP"]

    df_edited = st.data_editor(
        st.session_state.data,
        column_config={
            "Categoría": st.column_config.SelectboxColumn("Categoría", options=cat_options, required=True),
            "Titular": st.column_config.SelectboxColumn("Titular", options=titular_options, required=True),
            "Tipo": st.column_config.SelectboxColumn("Tipo", options=tipo_options, required=True),
            "Divisa": st.column_config.SelectboxColumn("Divisa", options=divisa_options, required=True),
            "Importe": st.column_config.NumberColumn("Importe (€)", format="%.2f €", min_value=0.0)
        },
        num_rows="dynamic",
        use_container_width=True,
        key="data_editor_pro"
    )
    
    if st.button("💾 Guardar y Recalcular Todo"):
        st.session_state.data = df_edited
        st.success("¡Datos y gráficos actualizados correctamente!")
        st.rerun()

# ==========================================
# PESTAÑA 4: EVOLUCIÓN HISTÓRICA
# ==========================================
with tab_historico:
    st.subheader("📈 Evolución del Patrimonio Neto vs. Objetivo (2021 - 2026)")
    df_hist = pd.DataFrame([
        {"Año": 2021, "Patrimonio Real": 103593, "Objetivo 10%": 108808},
        {"Año": 2022, "Patrimonio Real": 110731, "Objetivo 10%": 119689},
        {"Año": 2023, "Patrimonio Real": 136804, "Objetivo 10%": 131658},
        {"Año": 2024, "Patrimonio Real": 137570, "Objetivo 10%": 144824},
        {"Año": 2025, "Patrimonio Real": 150835, "Objetivo 10%": 159307},
        {"Año": 2026, "Patrimonio Real": patrimonio_neto, "Objetivo 10%": 175237},
    ])
    
    fig_hist = go.Figure()
    fig_hist.add_trace(go.Scatter(
        x=df_hist["Año"], y=df_hist["Patrimonio Real"], 
        mode='lines+markers', name='Patrimonio Real (€)', 
        line=dict(color='#4ADE80', width=4),
        marker=dict(size=10, color='#4ADE80')
    ))
    fig_hist.add_trace(go.Scatter(
        x=df_hist["Año"], y=df_hist["Objetivo 10%"], 
        mode='lines+markers', name='Objetivo 10% Compuesto', 
        line=dict(color='#38BDF8', width=3, dash='dash')
    ))
    
    fig_hist.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        font=dict(color='#F8FAFC', size=14),
        yaxis=dict(showgrid=True, gridcolor='#334155'),
        xaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig_hist, use_container_width=True)

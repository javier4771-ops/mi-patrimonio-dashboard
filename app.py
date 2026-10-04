import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Portfolio & Financial Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ESTILO CSS PERSONALIZADO (MODO OSCURO PRO) ---
st.markdown("""
<style>
    /* Estilo oscuro antracita */
    .stApp {
        background-color: #0E1117;
        color: #E0E0E0;
    }
    
    /* Tarjetas KPI estilo Hero */
    .kpi-card {
        background-color: #1E222D;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #2A2E39;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin-bottom: 15px;
    }
    
    .kpi-title {
        color: #848E9C;
        font-size: 14px;
        font-weight: 500;
        margin-bottom: 8px;
    }
    
    .kpi-value {
        font-size: 28px;
        font-weight: 700;
        color: #FFFFFF;
    }
    
    .kpi-sub {
        font-size: 13px;
        color: #00C087;
        margin-top: 4px;
    }

    .kpi-negative {
        color: #FF3B30;
    }
    
    /* Tabs personalizados */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: #131722;
        padding: 8px;
        border-radius: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        color: #B2B9C0;
        border-radius: 6px;
        padding: 8px 16px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #2A2E39 !important;
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# --- INICIALIZACIÓN DE DATOS (ESTADO DE SESIÓN) ---
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

# CÁLCULOS PRINCIPALES
activos = df[df["Tipo"] == "Activo"]["Importe"].sum()
pasivos = df[df["Tipo"] == "Pasivo"]["Importe"].sum()
patrimonio_neto = activos - pasivos
liquidez = df[df["Categoría"] == "Liquidez"]["Importe"].sum()

# --- ENCABEZADO Y MODO PRIVACIDAD ---
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.title("Portfolio Dashboard")
with col_head2:
    ocultar = st.checkbox("🙈 Ocultar Importes")

def fmt(valor, es_moneda=True):
    if ocultar:
        return "•••••• €" if es_moneda else "••••••"
    return f"{valor:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".") if es_moneda else f"{valor:,.2f}"

# --- NAVEGACIÓN POR PESTAÑAS ---
tab_patrimonio, tab_divisas, tab_posiciones, tab_historico = st.tabs([
    "📊 Patrimonio", "💱 Por Divisa / Categoría", "⚙️ Gestionar Posiciones", "📈 Evolución Histórica"
])

# ==========================================
# PESTAÑA 1: PATRIMONIO (DASHBOARD PRINCIPAL)
# ==========================================
with tab_patrimonio:
    # HERO PATRIMONIO NETO
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1E222D 0%, #131722 100%); border-radius: 16px; padding: 24px; border: 1px solid #2A2E39; margin-bottom: 24px;">
        <span style="color: #848E9C; font-size: 16px; font-weight: 600;">PATRIMONIO NETO TOTAL</span>
        <h1 style="color: #FFFFFF; font-size: 48px; font-weight: 800; margin: 8px 0;">{fmt(patrimonio_neto)}</h1>
        <div style="display: flex; gap: 20px; margin-top: 12px;">
            <span style="color: #00C087; font-weight: 600;">▲ Activos: {fmt(activos)}</span>
            <span style="color: #FF3B30; font-weight: 600;">▼ Pasivos (Deuda): {fmt(pasivos)}</span>
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
            <div class="kpi-sub">{(liquidez/activos*100):.1f}% de activos</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        inversion = df[df["Categoría"] == "Inversión / Brokers"]["Importe"].sum()
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Inversiones & Bolsa</div>
            <div class="kpi-value">{fmt(inversion)}</div>
            <div class="kpi-sub">{(inversion/activos*100):.1f}% de activos</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        pensiones = df[df["Categoría"] == "Planes de Pensiones"]["Importe"].sum()
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Planes de Pensiones</div>
            <div class="kpi-value">{fmt(pensiones)}</div>
            <div class="kpi-sub">{(pensiones/activos*100):.1f}% de activos</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        cripto = df[df["Categoría"] == "Criptoactivos"]["Importe"].sum()
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Criptoactivos</div>
            <div class="kpi-value">{fmt(cripto)}</div>
            <div class="kpi-sub">{(cripto/activos*100):.1f}% de activos</div>
        </div>
        """, unsafe_allow_html=True)

    # GRÁFICOS INTERACTIVOS
    st.subheader("Distribución Visual")
    c_graf1, c_graf2 = st.columns(2)
    
    df_activos = df[df["Tipo"] == "Activo"]
    
    with c_graf1:
        fig_donut = px.pie(
            df_activos, 
            values='Importe', 
            names='Categoría', 
            hole=0.6,
            color_discrete_sequence=px.colors.qualitative.Dark24,
            title="Reparto por Categoría de Activo"
        )
        fig_donut.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font_color='#FFFFFF'
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        
    with c_graf2:
        fig_bar = px.bar(
            df_activos, 
            x='Entidad', 
            y='Importe', 
            color='Categoría',
            title="Importe por Entidad / Broker",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font_color='#FFFFFF',
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_bar, use_container_width=True)

# ==========================================
# PESTAÑA 2: POR DIVISA / CATEGORÍA
# ==========================================
with tab_divisas:
    st.subheader("Desglose por Divisa y Titular")
    c_div1, c_div2 = st.columns(2)
    
    with c_div1:
        df_div = df_activos.groupby("Divisa")["Importe"].sum().reset_index()
        fig_div = px.pie(df_div, values="Importe", names="Divisa", title="Distribución por Divisa")
        fig_div.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='#FFFFFF')
        st.plotly_chart(fig_div, use_container_width=True)
        
    with c_div2:
        df_tit = df.groupby("Titular")["Importe"].sum().reset_index()
        fig_tit = px.bar(df_tit, x="Titular", y="Importe", color="Titular", title="Distribución por Titular")
        fig_tit.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='#FFFFFF')
        st.plotly_chart(fig_tit, use_container_width=True)

# ==========================================
# PESTAÑA 3: POSICIONES (AÑADIR / EDITAR / ELIMINAR)
# ==========================================
with tab_posiciones:
    st.subheader("⚙️ Panel de Gestión de Posiciones")
    st.info("Aquí puedes modificar importes, añadir nuevos bancos o eliminar cuentas. Todos los cambios actualizan el Dashboard al instante.")
    
    # FORMULARIO PARA AÑADIR/EDITAR
    with st.expander("➕ Añadir Nueva Posición o Producto"):
        with st.form("form_nueva_posicion"):
            f_cat = st.selectbox("Categoría", ["Liquidez", "Inversión / Brokers", "Criptoactivos", "Planes de Pensiones", "Deudas / Hipoteca"])
            f_ent = st.text_input("Entidad / Banco (ej. Trade Republic, MyInvestor, ING)")
            f_prod = st.text_input("Producto / Detalle (ej. Deposit 3%, Cartera ETFs)")
            f_tit = st.selectbox("Titular", ["Javi", "Blanca", "Compartido"])
            f_imp = st.number_input("Importe (€)", min_value=0.0, value=1000.0, step=100.0)
            f_tipo = "Pasivo" if f_cat == "Deudas / Hipoteca" else "Activo"
            f_div = st.selectbox("Divisa", ["EUR", "USD", "GBP"])
            
            submitted = st.form_submit_button("Guardar Posición")
            if submitted and f_ent:
                nueva_fila = {
                    "Categoría": f_cat, "Entidad": f_ent, "Producto": f_prod, 
                    "Titular": f_tit, "Importe": f_imp, "Tipo": f_tipo, "Divisa": f_div
                }
                st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([nueva_fila])], ignore_index=True)
                st.success(f"¡Posición en {f_ent} añadida con éxito!")
                st.rerun()

    # EDITAR DATOS EXISTENTES
    st.write("### Tabla Interactiva de Posiciones")
    df_edited = st.data_editor(
        st.session_state.data, 
        num_rows="dynamic", 
        use_container_width=True,
        key="data_editor"
    )
    
    if st.button("💾 Guardar Cambios de la Tabla"):
        st.session_state.data = df_edited
        st.success("¡Datos actualizados correctamente!")
        st.rerun()

# ==========================================
# PESTAÑA 4: EVOLUCIÓN HISTÓRICA (GUÍA)
# ==========================================
with tab_historico:
    st.subheader("📈 Evolución Histórica de Patrimonio (2021 - 2026)")
    df_hist = pd.DataFrame([
        {"Año": 2021, "Patrimonio Real": 103593, "Objetivo 10%": 108808},
        {"Año": 2022, "Patrimonio Real": 110731, "Objetivo 10%": 119689},
        {"Año": 2023, "Patrimonio Real": 136804, "Objetivo 10%": 131658},
        {"Año": 2024, "Patrimonio Real": 137570, "Objetivo 10%": 144824},
        {"Año": 2025, "Patrimonio Real": 150835, "Objetivo 10%": 159307},
        {"Año": 2026, "Patrimonio Real": patrimonio_neto, "Objetivo 10%": 175237},
    ])
    
    fig_hist = go.Figure()
    fig_hist.add_trace(go.Scatter(x=df_hist["Año"], y=df_hist["Patrimonio Real"], mode='lines+markers', name='Patrimonio Real (€)', line=dict(color='#00C087', width=3)))
    fig_hist.add_trace(go.Scatter(x=df_hist["Año"], y=df_hist["Objetivo 10%"], mode='lines+markers', name='Objetivo 10% Compuesto', line=dict(color='#3B82F6', width=2, dash='dash')))
    
    fig_hist.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        font_color='#FFFFFF',
        title="Patrimonio Real vs. Objetivo del 10% Anual"
    )
    st.plotly_chart(fig_hist, use_container_width=True)

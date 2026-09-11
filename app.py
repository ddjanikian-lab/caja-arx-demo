import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, timedelta
import random

st.set_page_config(page_title="Gestión de Caja ARX - Demo", layout="wide", page_icon="💰")

# ============================================================
# DATOS DE EJEMPLO (simulan tu Excel)
# ============================================================

CUENTAS = [
    {"id": 1, "nombre": "Caja $N Ale", "tipo": "Caja"},
    {"id": 2, "nombre": "Caja $N Edu", "tipo": "Caja"},
    {"id": 3, "nombre": "Banco Ale", "tipo": "Banco"},
    {"id": 4, "nombre": "Saldo Bco", "tipo": "Banco"},
    {"id": 5, "nombre": "F Fijo Edu", "tipo": "Fondo Inversion"},
    {"id": 6, "nombre": "F Fima", "tipo": "Fondo Inversion"},
    {"id": 7, "nombre": "CH Importe", "tipo": "Chequera"},
    {"id": 8, "nombre": "Mutual Toju", "tipo": "Mutual"},
]

CONCEPTOS = [
    {"id": 1, "nombre": "INGRESOS FINANCIEROS", "tipo": "Ingreso"},
    {"id": 2, "nombre": "INGRESOS VENTAS ARX", "tipo": "Ingreso"},
    {"id": 3, "nombre": "INGRESOS EVENTOS ARX", "tipo": "Ingreso"},
    {"id": 4, "nombre": "INGRESOS IVA 50%", "tipo": "Ingreso"},
    {"id": 5, "nombre": "EGRESOS ADMINISTRATIVOS", "tipo": "Egreso"},
    {"id": 6, "nombre": "EGRESOS UNIFORMES ARX", "tipo": "Egreso"},
    {"id": 7, "nombre": "EGRESOS OPERATIVOS", "tipo": "Egreso"},
    {"id": 8, "nombre": "EGRESOS SALARIOS", "tipo": "Egreso"},
    {"id": 9, "nombre": "EGRESOS PROVEEDORES", "tipo": "Egreso"},
    {"id": 10, "nombre": "EGRESOS IMPUESTOS", "tipo": "Egreso"},
    {"id": 11, "nombre": "EGRESOS COMISIONES", "tipo": "Egreso"},
    {"id": 12, "nombre": "EGRESOS RETIRO", "tipo": "Egreso"},
]

# Generar movimientos de ejemplo
def generar_movimientos():
    movimientos = []
    descripciones_ingreso = [
        "INGRESOS FINANCIEROS Aporte Edu y Ale",
        "INGRESOS SUOEM",
        "INGRESOS SALON 9 DE JULIO",
        "INGRESOS LIVERPOOL",
        "INGRESOS RIVADAVIA",
        "INGRESOS ASTORIA",
        "INGRESOS EL PERLA",
        "INGRESOS LA BODEGA",
        "INGRESOS AOITA",
        "INGRESOS UNION ELECTRICA",
        "INGRESOS Agropecuaria Boiero",
        "INGRESOS DORINKA",
        "INGRESOS Scaglia",
        "INGRESOS Don Emilio",
        "INGRESOS Fiesta Trinitarios",
    ]
    descripciones_egreso = [
        "EGRESO ADM Tasa Formación SAS",
        "UNIFORMES Banda refractaria e hilo",
        "EGRESO ADM RNR Certificado Maxi",
        "EGRESO OPE Alquiler garita",
        "EGRESO ADM escribanía",
        "EGRESO SAL ARX Carballo Maximiliano",
        "EGRESO SAL ARX Farías Carlos",
        "EGRESO SAL ARX Roldán Carlos",
        "EGRESO PRO INSUMOS Poligar",
        "Descuento Banco",
        "Honorarios Cr. Fowler",
        "EGRESO FIN Fondo de inversión",
        "Retiro Socio Ale",
        "Retiro Socio Edu",
        "COMISION 20% Jorge Ramos",
    ]
    
    fecha_inicio = date(2024, 6, 1)
    for i in range(150):
        fecha = fecha_inicio + timedelta(days=random.randint(0, 300))
        es_ingreso = random.random() > 0.4
        if es_ingreso:
            concepto = random.choice([c for c in CONCEPTOS if c["tipo"] == "Ingreso"])
            descripcion = random.choice(descripciones_ingreso)
            monto = round(random.uniform(10000, 500000), 2)
        else:
            concepto = random.choice([c for c in CONCEPTOS if c["tipo"] == "Egreso"])
            descripcion = random.choice(descripciones_egreso)
            monto = round(random.uniform(5000, 300000), 2)
        
        cuenta = random.choice(CUENTAS)
        movimientos.append({
            "id": i + 1,
            "fecha": fecha,
            "cuenta_id": cuenta["id"],
            "cuenta_nombre": cuenta["nombre"],
            "concepto_id": concepto["id"],
            "concepto_nombre": concepto["nombre"],
            "billetera": random.choice(["$ N Ale", "$ N Edu", "Saldo Bco", "Banco Ale", "F Fijo Edu", "CH Importe"]),
            "descripcion": descripcion,
            "monto": monto,
            "tipo": concepto["tipo"],
            "unidad_negocio": random.choice(["ARX", "LA ESTACION"]),
            "notas": ""
        })
    return movimientos

if "movimientos" not in st.session_state:
    st.session_state.movimientos = generar_movimientos()

cuentas_df = pd.DataFrame(CUENTAS)
conceptos_df = pd.DataFrame(CONCEPTOS)
movimientos_df = pd.DataFrame(st.session_state.movimientos)

# ============================================================
# INTERFAZ
# ============================================================

st.title("💰 Sistema de Gestión - Módulo de Caja (Demo)")
st.caption("Esta es una demostración con datos de ejemplo. Los datos reales se cargarán desde tu Excel cuando conectemos la base de datos.")

st.sidebar.title("Menú")
st.sidebar.markdown("---")
opcion = st.sidebar.radio("Selecciona una opción:", 
                          ["📊 Dashboard", "➕ Nueva Transacción", "📜 Historial", "📈 Reportes", "⚙️ Configuración"])

# ---------- DASHBOARD ----------
if opcion == "📊 Dashboard":
    st.header("📊 Resumen General")
    
    # Calcular métricas
    total_ingresos = movimientos_df[movimientos_df["tipo"] == "Ingreso"]["monto"].sum()
    total_egresos = movimientos_df[movimientos_df["tipo"] == "Egreso"]["monto"].sum()
    saldo_neto = total_ingresos - total_egresos
    
    # Saldo por tipo de cuenta
    saldo_bancos = movimientos_df[
        (movimientos_df["cuenta_nombre"].isin(["Banco Ale", "Saldo Bco"])) & 
        (movimientos_df["tipo"] == "Ingreso")
    ]["monto"].sum() - movimientos_df[
        (movimientos_df["cuenta_nombre"].isin(["Banco Ale", "Saldo Bco"])) & 
        (movimientos_df["tipo"] == "Egreso")
    ]["monto"].sum()
    
    saldo_cajas = movimientos_df[
        (movimientos_df["cuenta_nombre"].isin(["Caja $N Ale", "Caja $N Edu"])) & 
        (movimientos_df["tipo"] == "Ingreso")
    ]["monto"].sum() - movimientos_df[
        (movimientos_df["cuenta_nombre"].isin(["Caja $N Ale", "Caja $N Edu"])) & 
        (movimientos_df["tipo"] == "Egreso")
    ]["monto"].sum()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💵 Total Ingresos", f"$ {total_ingresos:,.2f}")
    with col2:
        st.metric("💸 Total Egresos", f"$ {total_egresos:,.2f}")
    with col3:
        st.metric("🏦 Saldo Neto", f"$ {saldo_neto:,.2f}", delta=f"{saldo_neto:,.0f}")
    with col4:
        st.metric("🏧 Saldo Bancos", f"$ {saldo_bancos:,.2f}")
    
    st.markdown("---")
    
    col_izq, col_der = st.columns(2)
    
    with col_izq:
        st.subheader("📈 Evolución del Saldo Acumulado")
        df_ordenado = movimientos_df.sort_values("fecha").copy()
        df_ordenado["monto_firmado"] = df_ordenado.apply(
            lambda x: x["monto"] if x["tipo"] == "Ingreso" else -x["monto"], axis=1
        )
        df_ordenado["saldo_acumulado"] = df_ordenado["monto_firmado"].cumsum()
        fig_line = px.line(df_ordenado, x="fecha", y="saldo_acumulado", 
                          title="Saldo Acumulado en el Tiempo")
        st.plotly_chart(fig_line, use_container_width=True)
    
    with col_der:
        st.subheader("🥧 Distribución por Concepto")
        por_concepto = movimientos_df.groupby(["concepto_nombre", "tipo"])["monto"].sum().reset_index()
        fig_pie = px.pie(por_concepto[por_concepto["tipo"]=="Egreso"], 
                        values="monto", names="concepto_nombre",
                        title="Egresos por Concepto")
        st.plotly_chart(fig_pie, use_container_width=True)
    
    st.subheader("📋 Últimos 10 Movimientos")
    ultimos = movimientos_df.sort_values("fecha", ascending=False).head(10)
    st.dataframe(
        ultimos[["fecha", "cuenta_nombre", "concepto_nombre", "descripcion", "monto", "tipo"]],
        use_container_width=True, hide_index=True
    )

# ---------- NUEVA TRANSACCIÓN ----------
elif opcion == "➕ Nueva Transacción":
    st.header("➕ Registrar Movimiento")
    st.info("En esta demo, los movimientos se guardan temporalmente en memoria. Al conectar la base de datos, quedarán guardados de forma permanente.")
    
    with st.form("nueva_transaccion", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            fecha = st.date_input("Fecha *", value=date.today())
            cuenta_nombre = st.selectbox("Cuenta / Billetera *", cuentas_df["nombre"].tolist())
            tipo = st.selectbox("Tipo de Movimiento *", ["Ingreso", "Egreso"])
        
        with col2:
            conceptos_filtrados = conceptos_df[conceptos_df["tipo"]==tipo]["nombre"].tolist()
            concepto_nombre = st.selectbox("Concepto *", conceptos_filtrados)
            billetera = st.text_input("Billetera (opcional)", placeholder="Ej: $ N Ale")
        
        with col3:
            monto = st.number_input("Monto *", min_value=0.01, value=1000.0, step=100.0, format="%.2f")
            unidad_negocio = st.selectbox("Unidad de Negocio", ["ARX", "LA ESTACION", "Otra"])
        
        descripcion = st.text_area("Descripción / Detalle *", placeholder="Ej: EGRESO ADM Tasa Formación SAS")
        notas = st.text_area("Notas (opcional)")
        
        submitted = st.form_submit_button("💾 Guardar Movimiento", use_container_width=True)
        
        if submitted:
            if not descripcion:
                st.error("La descripción es obligatoria.")
            else:
                cuenta_id = cuentas_df[cuentas_df["nombre"]==cuenta_nombre]["id"].iloc[0]
                concepto_id = conceptos_df[conceptos_df["nombre"]==concepto_nombre]["id"].iloc[0]
                
                nuevo_id = max([m["id"] for m in st.session_state.movimientos], default=0) + 1
                st.session_state.movimientos.append({
                    "id": nuevo_id,
                    "fecha": fecha,
                    "cuenta_id": int(cuenta_id),
                    "cuenta_nombre": cuenta_nombre,
                    "concepto_id": int(concepto_id),
                    "concepto_nombre": concepto_nombre,
                    "billetera": billetera,
                    "descripcion": descripcion,
                    "monto": monto,
                    "tipo": tipo,
                    "unidad_negocio": unidad_negocio,
                    "notas": notas
                })
                movimientos_df = pd.DataFrame(st.session_state.movimientos)
                st.success(f"✅ Movimiento registrado: {descripcion} - $ {monto:,.2f}")
                st.balloons()

# ---------- HISTORIAL ----------
elif opcion == "📜 Historial":
    st.header("📜 Historial de Movimientos")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        fecha_desde = st.date_input("Desde", value=date.today() - timedelta(days=90))
    with col2:
        fecha_hasta = st.date_input("Hasta", value=date.today())
    with col3:
        cuenta_filtro = st.selectbox("Cuenta", ["Todas"] + cuentas_df["nombre"].tolist())
    with col4:
        tipo_filtro = st.selectbox("Tipo", ["Todos", "Ingreso", "Egreso"])
    
    texto_busqueda = st.text_input("🔍 Buscar en descripción o concepto", "")
    
    df_filtrado = movimientos_df.copy()
    df_filtrado = df_filtrado[
        (pd.to_datetime(df_filtrado["fecha"]).dt.date >= fecha_desde) &
        (pd.to_datetime(df_filtrado["fecha"]).dt.date <= fecha_hasta)
    ]
    
    if cuenta_filtro != "Todas":
        df_filtrado = df_filtrado[df_filtrado["cuenta_nombre"] == cuenta_filtro]
    if tipo_filtro != "Todos":
        df_filtrado = df_filtrado[df_filtrado["tipo"] == tipo_filtro]
    if texto_busqueda:
        df_filtrado = df_filtrado[
            df_filtrado["descripcion"].str.contains(texto_busqueda, case=False, na=False) |
            df_filtrado["concepto_nombre"].str.contains(texto_busqueda, case=False, na=False)
        ]
    
    st.markdown(f"**{len(df_filtrado)} movimientos encontrados**")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Total Ingresos", f"$ {df_filtrado[df_filtrado['tipo']=='Ingreso']['monto'].sum():,.2f}")
    with col_b:
        st.metric("Total Egresos", f"$ {df_filtrado[df_filtrado['tipo']=='Egreso']['monto'].sum():,.2f}")
    with col_c:
        neto = df_filtrado[df_filtrado['tipo']=='Ingreso']['monto'].sum() - df_filtrado[df_filtrado['tipo']=='Egreso']['monto'].sum()
        st.metric("Neto", f"$ {neto:,.2f}")
    
    st.dataframe(
        df_filtrado.sort_values("fecha", ascending=False)[
            ["fecha", "cuenta_nombre", "concepto_nombre", "descripcion", "billetera", "monto", "tipo"]
        ],
        use_container_width=True, hide_index=True
    )
    
    csv = df_filtrado.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Exportar a CSV", data=csv, file_name="movimientos.csv", mime="text/csv")

# ---------- REPORTES ----------
elif opcion == "📈 Reportes":
    st.header("📈 Análisis Financiero")
    
    col1, col2 = st.columns(2)
    with col1:
        fecha_desde = st.date_input("Desde", value=date.today() - timedelta(days=90))
    with col2:
        fecha_hasta = st.date_input("Hasta", value=date.today())
    
    df_rep = movimientos_df.copy()
    df_rep = df_rep[
        (pd.to_datetime(df_rep["fecha"]).dt.date >= fecha_desde) &
        (pd.to_datetime(df_rep["fecha"]).dt.date <= fecha_hasta)
    ]
    
    st.subheader("Resumen por Concepto")
    resumen = df_rep.groupby(["concepto_nombre", "tipo"]).agg(
        Total=("monto", "sum"),
        Cantidad=("id", "count")
    ).reset_index()
    st.dataframe(resumen, use_container_width=True, hide_index=True)
    
    col_izq, col_der = st.columns(2)
    
    with col_izq:
        st.subheader("Comparativa Ingresos vs Egresos")
        comparativa = df_rep.groupby("concepto_nombre").apply(
            lambda x: pd.Series({
                "Ingresos": x[x["tipo"]=="Ingreso"]["monto"].sum(),
                "Egresos": x[x["tipo"]=="Egreso"]["monto"].sum()
            })
        ).reset_index()
        fig = px.bar(comparativa, x="concepto_nombre", y=["Ingresos", "Egresos"], barmode="group")
        st.plotly_chart(fig, use_container_width=True)
    
    with col_der:
        st.subheader("Top 5 Conceptos con más Egresos")
        top_egresos = df_rep[df_rep["tipo"]=="Egreso"].groupby("concepto_nombre")["monto"].sum().nlargest(5).reset_index()
        fig_top = px.bar(top_egresos, x="monto", y="concepto_nombre", orientation="h")
        st.plotly_chart(fig_top, use_container_width=True)
    
    st.subheader("Evolución Mensual")
    df_rep["mes"] = pd.to_datetime(df_rep["fecha"]).dt.to_period("M").astype(str)
    mensual = df_rep.groupby(["mes", "tipo"])["monto"].sum().reset_index()
    fig_mes = px.bar(mensual, x="mes", y="monto", color="tipo", barmode="group")
    st.plotly_chart(fig_mes, use_container_width=True)

# ---------- CONFIGURACIÓN ----------
elif opcion == "⚙️ Configuración":
    st.header("⚙️ Configuración del Sistema")
    st.info("En esta demo, la configuración es de solo lectura. En la versión final podrás agregar, editar y eliminar cuentas y conceptos.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Cuentas")
        st.dataframe(cuentas_df, use_container_width=True, hide_index=True)
    with col2:
        st.subheader("Conceptos")
        st.dataframe(conceptos_df, use_container_width=True, hide_index=True)

st.sidebar.markdown("---")
st.sidebar.caption("Demo v1.0 · Datos de ejemplo")
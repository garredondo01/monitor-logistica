import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta, timezone
import base64
import os

# Configuración de página
st.set_page_config(page_title="Rotoplas - Monitor Embarques", layout="wide")

# Tu ID de Google Sheets
SHEET_ID = "19VBW2abjR0UrBZ8QmKbKl9LY00O6eu3lzpCSJqeajYk"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# Función para convertir la imagen local a base64
def get_base64_image(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

# Carga la imagen de Rotoplas
logo_base64 = get_base64_image("rotoplas-seeklogo.png")

if logo_base64:
    logo_html = f'<img src="data:image/png;base64,{logo_base64}" height="50" alt="Rotoplas Logo">'
else:
    logo_html = '<span style="color: #0072b9; font-size: 28px; font-weight: bold;">Rotoplas</span>'

# CSS Estilo Rotoplas - CON LÓGICA DE COLORES PARA TODA LA LÍNEA Y EFECTO INTERMITENTE
diseño_rotoplas = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Fondo principal */
    .stApp { 
        background-color: #0c172a; 
        color: white; 
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; 
    }
    
    /* Contenedor principal con márgenes de seguridad para TV */
    .tv-safe-layout {
        width: 96%;
        margin: 0 auto;
        padding-top: 10px;
    }
    
    /* Header */
    .rotoplas-header { 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        background-color: white; 
        color: #1a3c75; 
        padding: 8px 25px; 
        border-bottom: 2px solid #ccc; 
        border-radius: 4px;
        margin-bottom: 15px;
    }
    .rotoplas-logo-section { display: flex; align-items: center; }
    .rotoplas-title-section { font-size: 22px; font-weight: bold; text-transform: uppercase; text-align: center; flex-grow: 1; color: #0072b9; }
    .rotoplas-time-section { font-size: 20px; font-weight: bold; display: flex; align-items: center; color: #1a3c75; }
    .clock-icon { background-color: #0072b9; color: white; border-radius: 50%; width: 30px; height: 30px; display: flex; justify-content: center; align-items: center; margin-right: 10px; font-size: 16px; }
    
    /* TABLA OPTIMIZADA */
    .board-table { 
        width: 100%; 
        border-collapse: collapse; 
        font-size: 16px; 
    }
    .board-table thead tr { background-color: #0072b9; color: white; }
    
    /* Encabezados de columna */
    .board-table th { 
        padding: 12px 12px; 
        text-align: left; 
        font-weight: bold; 
        border-right: 1px solid rgba(255,255,255,0.2); 
        text-transform: uppercase; 
        font-size: 19px; 
    }
    
    .board-table tbody tr { border-bottom: 1px solid rgba(255,255,255,0.05); }
    
    /* Celdas de datos generales */
    .board-table td { padding: 12px 12px; font-weight: bold; text-transform: uppercase; color: white; border-right: 1px solid rgba(255,255,255,0.05); }
    
    /* Clase para centrar columnas específicas */
    .col-centro {
        text-align: center !important;
    }
    
    /* 🚨 ESTILOS DE ESTATUS PERSONALIZADOS (APLICADOS A TODA LA FILA O COLOR ESPECÍFICO) 🚨 */
    
    /* 1. UNIDAD CARGADA: Letras de toda la fila en color verde */
    .fila-unidad-cargada td {
        color: #2ecc71 !important;
    }
    
    /* 2. PROCESO DE CARGA: Letras de toda la fila en color amarillo */
    .fila-proceso-carga td {
        color: #f1c40f !important;
    }
    
    /* 3. PENDIENTE FACTURA: Letras en rojo y animación intermitente */
    .fila-pendiente-factura td {
        color: #e74c3c !important;
        animation: parpadeo 1.2s infinite;
    }
    
    /* 4. EN RAMPA: Letras en blanco (por defecto) */
    .fila-en-rampa td {
        color: #ffffff !important;
    }
    
    /* 5. PENDIENTE: Letras en blanco (por defecto) */
    .fila-pendiente td {
        color: #ffffff !important;
    }

    /* Animación para el parpadeo del texto rojo */
    @keyframes parpadeo {
        0% { opacity: 1.0; }
        50% { opacity: 0.2; }
        100% { opacity: 1.0; }
    }

    .rotoplas-footer { text-align: right; padding: 15px; color: rgba(255,255,255,0.6); font-size: 16px; font-weight: bold; }
</style>
"""
st.markdown(diseño_rotoplas, unsafe_allow_html=True)

placeholder_full = st.empty()

# Definimos el huso horario del Centro de México (UTC -6)
zona_cdmx = timezone(timedelta(hours=-6))

while True:
    try:
        # Hora y fecha real en base a Zona Centro de México
        ahora = datetime.now(zona_cdmx)
        hora_actual = ahora.strftime("%H:%M")
        fecha_actual_mexico = ahora.strftime("%d/%m/%Y")

        df = pd.read_csv(URL)
        df = df.fillna("")

        # Aseguramos limpiar los nombres de las columnas quitando espacios ocultos
        df.columns = [col.strip() for col in df.columns]

        # 🚨 FILTRO ELIMINAR ID: Quitamos la columna ID para que no se muestre en el monitor 🚨
        df = df.drop(columns=["ID"], errors="ignore")

        # Estructura con márgenes seguros para televisión
        html = '<div class="tv-safe-layout">'
        html += '<div class="rotoplas-header">'
        html += f'<div class="rotoplas-logo-section">{logo_html}<div style="font-size:12px; margin-left:12px; color:#555; font-weight:bold; border-left: 2px solid #ccc; padding-left: 8px;">Operaciones<br>Logísticas</div></div>'
        html += '<div class="rotoplas-title-section">MONITOR EMBARQUES COMPUESTOS</div>'
        html += f'<div class="rotoplas-time-section"><div class="clock-icon">🕒</div>{hora_actual}</div>'
        html += '</div>'
        
        # Generar encabezados de forma dinámica aplicando la clase de centrado
        html += '<table class="board-table"><thead><tr>'
        for columna in df.columns:
            nombre_upper = columna.upper()
            if "HORA" in nombre_upper or "LLEGADA" in nombre_upper or "STATUS" in nombre_upper or "FECHA" in nombre_upper:
                html += f'<th class="col-centro">{columna}</th>'
            else:
                html += f'<th>{columna}</th>'
        html += '</tr></thead><tbody>'

        # Generar filas filtrando por fecha actual
        for index, row in df.iterrows():
            
            # FILTRO POR FECHA:
            if "FECHA" in [c.upper() for c in df.columns]:
                idx_fecha = [c for c in df.columns if c.upper() == "FECHA"][0]
                fecha_fila = str(row[idx_fecha]).strip()
                
                if fecha_fila != fecha_actual_mexico and fecha_fila != "":
                    continue

            # Evaluar el STATUS de la fila actual para asignarle su clase a todo el <tr>
            clase_fila = ""
            status_celda_raw = ""
            
            if "STATUS" in [c.upper() for c in df.columns]:
                idx_status = [c for c in df.columns if c.upper() == "STATUS"][0]
                status_celda_raw = str(row[idx_status]).strip().upper()
                
                if "UNIDAD CARGADA" in status_celda_raw:
                    clase_fila = ' class="fila-unidad-cargada"'
                elif "PENDIENTE FACTURA" in status_celda_raw:
                    clase_fila = ' class="fila-pendiente-factura"'
                elif "PROCESO DE CARGA" in status_celda_raw:
                    clase_fila = ' class="fila-proceso-carga"'
                elif "EN RAMPA" in status_celda_raw:
                    clase_fila = ' class="fila-en-rampa"'
                elif "PENDIENTE" in status_celda_raw:
                    clase_fila = ' class="fila-pendiente"'

            html += f'<tr{clase_fila}>'
            for columna in df.columns:
                valor_celda = str(row[columna]).strip()
                nombre_col_upper = columna.upper()
                
                # Determinar si la columna requiere alineación centrada (Fecha, Horas, Status)
                es_col_centrada = "HORA" in nombre_col_upper or "LLEGADA" in nombre_col_upper or "STATUS" in nombre_col_upper or "FECHA" in nombre_col_upper
                clase_centro = ' class="col-centro"' if es_col_centrada else ""
                
                # 🚨 AGREGAR LA BANDERITA ACUADROS SI EL ESTATUS ES "EN RAMPA" 🚨
                if nombre_col_upper == "STATUS" and "EN RAMPA" in valor_celda.upper():
                    html += f'<td{clase_centro}>🏁 {valor_celda}</td>'
                else:
                    html += f'<td{clase_centro}>{valor_celda}</td>'
                    
            html += '</tr>'

        html += '</tbody></table>'
        html += f'<div class="rotoplas-footer">{fecha_actual_mexico}</div>'
        html += '</div>' # Cierre de tv-safe-layout

        with placeholder_full.container():
            st.markdown(html, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
    
    time.sleep(3)

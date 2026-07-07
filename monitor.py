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
    logo_html = f'<img src="data:image/png;base64,{logo_base64}" height="60" alt="Rotoplas Logo">'
else:
    logo_html = '<span style="color: #0072b9; font-size: 32px; font-weight: bold;">Rotoplas</span>'

# CSS Estilo Rotoplas
diseño_rotoplas = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #0c172a; color: white; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .rotoplas-header { display: flex; justify-content: space-between; align-items: center; background-color: white; color: #1a3c75; padding: 10px 30px; border-bottom: 2px solid #ccc; }
    .rotoplas-logo-section { display: flex; align-items: center; }
    .rotoplas-title-section { font-size: 26px; font-weight: bold; text-transform: uppercase; text-align: center; flex-grow: 1; color: #0072b9; }
    .rotoplas-time-section { font-size: 24px; font-weight: bold; display: flex; align-items: center; color: #1a3c75; }
    .clock-icon { background-color: #0072b9; color: white; border-radius: 50%; width: 35px; height: 35px; display: flex; justify-content: center; align-items: center; margin-right: 10px; font-size: 18px; }
    .board-table { width: 100%; border-collapse: collapse; font-size: 18px; }
    .board-table thead tr { background-color: #0072b9; color: white; }
    .board-table th { padding: 15px; text-align: left; font-weight: bold; border-right: 1px solid rgba(255,255,255,0.2); font-size: 20px;text-transform: uppercase; }
    .board-table tbody tr { border-bottom: 1px solid rgba(255,255,255,0.05); }
    .board-table tbody tr:nth-child(odd) { background-color: #0c172a; }
    .board-table tbody tr:nth-child(even) { background-color: #152d52; }
    .board-table td { padding: 18px 15px; font-weight: bold; text-transform: uppercase; color: white; border-right: 1px solid rgba(255,255,255,0.05); }
    .status-proceso { color: #f1c40f !important; }
    .status-cargado { color: #2ecc71 !important; }
    .status-por-llegar { color: #e74c3c !important; font-weight: bold;}
    .rotoplas-footer { text-align: right; padding: 20px; color: rgba(255,255,255,0.6); font-size: 18px; font-weight: bold; }
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
        fecha_actual_mexico = ahora.strftime("%d/%m/%Y") # Formato: DD/MM/AAAA

        df = pd.read_csv(URL)
        df = df.fillna("")

        # Aseguramos limpiar los nombres de las columnas quitando espacios ocultos
        df.columns = [col.strip() for col in df.columns]

        # Construcción directa de HTML
        html = '<div>'
        html += '<div class="rotoplas-header">'
        html += f'<div class="rotoplas-logo-section">{logo_html}<div style="font-size:14px; margin-left:15px; color:#555; font-weight:bold; border-left: 2px solid #ccc; padding-left: 10px;">Operaciones<br>Logísticas</div></div>'
        html += '<div class="rotoplas-title-section">MONITOR EMBARQUES COMPUESTOS</div>'
        html += f'<div class="rotoplas-time-section"><div class="clock-icon">🕒</div>{hora_actual}</div>'
        html += '</div>'
        
        # Generar encabezados de forma dinámica
        html += '<table class="board-table"><thead><tr>'
        for columna in df.columns:
            html += f'<th>{columna}</th>'
        html += '</tr></thead><tbody>'

        # Generar filas filtrando por fecha actual
        for index, row in df.iterrows():
            
            # FILTRO POR FECHA:
            # Buscamos si existe una columna llamada "FECHA".
            # Si existe, el código verifica que el contenido coincida con la fecha de hoy de México.
            if "FECHA" in [c.upper() for c in df.columns]:
                idx_fecha = [c for c in df.columns if c.upper() == "FECHA"][0]
                fecha_fila = str(row[idx_fecha]).strip()
                
                # Si la fecha de la fila no coincide con la de hoy, se la salta.
                if fecha_fila != fecha_actual_mexico and fecha_fila != "":
                    continue

            html += '<tr>'
            for columna in df.columns:
                valor_celda = str(row[columna]).strip()
                valor_upper = valor_celda.upper()
                
                # Lógica de colores para los STATUS habituales
                clase_status = ""
                if "PROCESO DE CARGA" in valor_upper:
                    clase_status = "status-proceso"
                elif "CARGADO" in valor_upper:
                    clase_status = "status-cargado"
                elif "POR LLEGAR" in valor_upper:
                    clase_status = "status-por-llegar"

                if clase_status:
                    html += f'<td class="{clase_status}">{valor_celda}</td>'
                else:
                    html += f'<td>{valor_celda}</td>'
                    
            html += '</tr>'

        html += '</tbody></table>'
        html += f'<div class="rotoplas-footer">{fecha_actual_mexico}</div>'
        html += '</div>'

        with placeholder_full.container():
            st.markdown(html, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
    
    time.sleep(3)

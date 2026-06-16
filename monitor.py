import streamlit as st
import pandas as pd
import time
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="OMA - Monitor de Operaciones", layout="wide")

# Tu ID de Google Sheets
SHEET_ID = "19VBW2abjR0UrBZ8QmKbKl9LY00O6eu3lzpCSJqeajYk"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# CSS Estilo OMA
diseño_oma = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #0c172a; color: white; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .oma-header { display: flex; justify-content: space-between; align-items: center; background-color: white; color: #1a3c75; padding: 10px 30px; border-bottom: 2px solid #ccc; }
    .oma-logo-section { font-size: 24px; font-weight: bold; display: flex; align-items: center; }
    .oma-logo-placeholder { color: #e31d2b; font-style: italic; margin-right: 10px; font-size: 30px; }
    .oma-title-section { font-size: 26px; font-weight: bold; text-transform: uppercase; text-align: center; flex-grow: 1; }
    .oma-time-section { font-size: 24px; font-weight: bold; display: flex; align-items: center; }
    .clock-icon { background-color: #3498db; color: white; border-radius: 50%; width: 35px; height: 35px; display: flex; justify-content: center; align-items: center; margin-right: 10px; font-size: 18px; }
    .board-table { width: 100%; border-collapse: collapse; font-size: 20px; }
    .board-table thead tr { background-color: #1e6cb3; color: white; }
    .board-table th { padding: 15px; text-align: left; font-weight: normal; border-right: 1px solid rgba(255,255,255,0.2); }
    .board-table tbody tr { border-bottom: 1px solid rgba(255,255,255,0.05); }
    .board-table tbody tr:nth-child(odd) { background-color: #0c172a; }
    .board-table tbody tr:nth-child(even) { background-color: #152d52; }
    .board-table td { padding: 18px 15px; font-weight: bold; text-transform: uppercase; color: white; border-right: 1px solid rgba(255,255,255,0.05); }
    .status-proceso { color: #f1c40f !important; }
    .status-cargado { color: #2ecc71 !important; }
    .status-por-llegar { color: #e74c3c !important; font-weight: bold;}
    .oma-footer { text-align: right; padding: 20px; color: rgba(255,255,255,0.6); font-size: 18px; font-weight: bold; }
</style>
"""
st.markdown(diseño_oma, unsafe_allow_html=True)

placeholder_full = st.empty()

while True:
    try:
        ahora = datetime.now()
        hora_actual = ahora.strftime("%H:%M")
        fecha_actual = ahora.strftime("%d/%m/%Y")

        df = pd.read_csv(URL)
        df = df.fillna("")

        # Construcción directa de HTML (Sin sangrías para evitar bloques de código Markdown)
        html = '<div>'
        html += '<div class="oma-header">'
        html += '<div class="oma-logo-section"><span class="oma-logo-placeholder">/</span> OMA<div style="font-size:12px; margin-left:5px; color:#555; font-weight:normal;">Operaciones Logísticas</div></div>'
        html += '<div class="oma-title-section">SALIDAS / DEPARTURES</div>'
        html += f'<div class="oma-time-section"><div class="clock-icon">L</div>{hora_actual}</div>'
        html += '</div>'
        
        html += '<table class="board-table"><thead><tr>'
        html += '<th>Hora<br><span style="font-size:12px;opacity:0.8;">Time</span></th>'
        html += '<th>Destino<br><span style="font-size:12px;opacity:0.8;">To</span></th>'
        html += '<th>Línea<br><span style="font-size:12px;opacity:0.8;">Carrier</span></th>'
        html += '<th>Unidad / Vuelo<br><span style="font-size:12px;opacity:0.8;">Unit / Flight</span></th>'
        html += '<th>Observación<br><span style="font-size:12px;opacity:0.8;">Remark (Status)</span></th>'
        html += '</tr></thead><tbody>'

        for index, row in df.iterrows():
            hora_llegada = row.get("HORA DE LLEGADA", "")
            destino = row.get("DESTINO", "")
            linea = row.get("LINEA", "")
            operador = row.get("OPERADOR", "")
            status_raw = str(row.get("STATUS", "")).strip().upper()

            clase_status = ""
            if "PROCESO DE CARGA" in status_raw:
                clase_status = "status-proceso"
            elif "CARGADO" in status_raw:
                clase_status = "status-cargado"
            elif "POR LLEGAR" in status_raw:
                clase_status = "status-por-llegar"

            html += '<tr>'
            html += f'<td>{hora_llegada}</td>'
            html += f'<td>{destino}</td>'
            html += f'<td>{linea}</td>'
            html += f'<td>{operador}</td>'
            html += f'<td class="{clase_status}">{status_raw}</td>'
            html += '</tr>'

        html += '</tbody></table>'
        html += f'<div class="oma-footer">{fecha_actual}</div>'
        html += '</div>'

        with placeholder_full.container():
            st.markdown(html, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error técnico real: {e}")
    
    time.sleep(3)
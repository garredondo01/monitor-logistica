import streamlit as st
import pandas as pd
import time
from datetime import datetime

# ==========================================
# CONFIGURACIÓN DE PÁGINA (PANTALLA COMPLETA)
# ==========================================
st.set_page_config(page_title="Rotoplas - Monitor de Embarques", layout="wide")

# CONFIGURACIÓN: Tu ID de Google Sheets ya integrado
SHEET_ID = "19VBW2abjR0UrBZ8QmKbKl9LY00O6eu3lzpCSJqeajYk"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# ==========================================
# DISEÑO CSS OPTIMIZADO PARA SMART TV (ESCALA 80%)
# ==========================================
diseño_rotoplas_tv = """
<style>
    /* Ocultar elementos de interfaz de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 1. Fondo de pantalla principal */
    .stApp {
        background-color: #0c172a; 
        color: white;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }

    /* 🚨 TRUCO MAESTRO PARA SMART TV 🚨
       Aplica un zoom del 80% a todo el contenedor del monitor 
       para que no se vea gigante en la televisión */
    .contenedor-tv {
        zoom: 80%; /* Puedes cambiar a 75% o 85% si necesitas ajustar más */
        -moz-transform: scale(0.8); /* Compatibilidad para otros navegadores */
        -moz-transform-origin: top center;
    }

    /* 2. Contenedor del Encabezado Principal */
    .header-monitor {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: white; 
        color: #0072CE; 
        padding: 15px 30px;
        border-bottom: 4px solid #0072CE; 
    }
    
    .logo-section-rotoplas {
        font-size: 36px;
        font-weight: 900; 
        display: flex;
        align-items: center;
        text-transform: uppercase;
        letter-spacing: -1px;
    }
    
    .title-section-main {
        font-size: 32px;
        font-weight: bold;
        text-transform: uppercase;
        text-align: center;
        flex-grow: 1;
        letter-spacing: 2px;
        color: #1a3c75; 
    }
    
    .time-section-right {
        font-size: 28px;
        font-weight: bold;
        display: flex;
        align-items: center;
        color: #1a3c75;
    }
    
    .clock-icon-blue {
        background-color: #0072CE;
        color: white;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-right: 10px;
        font-size: 20px;
    }

    /* 3. Estilo de la Tabla de Datos Principal */
    .board-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 24px; 
    }

    .board-table thead tr {
        background-color: #1e6cb3; 
        color: white;
    }
    
    .board-table th {
        padding: 20px 15px;
        text-align: left;
        font-weight: bold;
        text-transform: uppercase;
        border-right: 1px solid rgba(255,255,255,0.2);
    }
    
    .board-table tbody tr {
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    
    .board-table tbody tr:nth-child(odd) {
        background-color: #0c172a;
    }
    
    .board-table tbody tr:nth-child(even) {
        background-color: #152d52; 
    }

    .board-table td {
        padding: 22px 15px;
        font-weight: bold;
        text-transform: uppercase;
        color: white;
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    .status-proceso { color: #f1c40f !important; } 
    .status-cargado { color: #2ecc71 !important; } 
    .status-por-llegar { color: #e74c3c !important; font-weight: bold;} 

    .footer-date {
        text-align: right;
        padding: 20px;
        color: rgba(255,255,255,0.6);
        font-size: 20px;
        font-weight: bold;
    }
</style>
"""
st.markdown(diseño_rotoplas_tv, unsafe_allow_html=True)

placeholder_full = st.empty()

while True:
    try:
        ahora = datetime.now()
        hora_actual = SimulatedTime.strftime("%H:%M") if 'SimulatedTime' in globals() else ahora.strftime("%H:%M")
        fecha_actual = ahora.strftime("%d/%m/%Y")

        df = pd.read_csv(URL)
        df = df.fillna("")

        # Encapsulamos todo dentro de la clase 'contenedor-tv' para aplicar el zoom reducido
        html = '<div class="contenedor-tv">'
        html += '<div class="header-monitor">'
        html += '<div class="logo-section-rotoplas">Rotoplas</div>'
        html += '<div class="title-section-main">MONITOR DE EMBARQUES</div>'
        html += f'<div class="time-section-right"><div class="clock-icon-blue">L</div>{hora_actual}</div>'
        html += '</div>'
        
        html += '<table class="board-table"><thead><tr>'
        html += '<th>DESTINO</th>'
        html += '<th>LINEA</th>'
        html += '<th>OPERADOR</th>'
        html += '<th>HORA DE LLEGADA</th>'
        html += '<th>STATUS</th>'
        html += '</tr></thead><tbody>'

        for index, row in df.iterrows():
            destino = row.get("DESTINO", "")
            linea = row.get("LINEA", "")
            operador = row.get("OPERADOR", "")
            hora_llegada = row.get("HORA DE LLEGADA", "")
            status_raw = str(row.get("STATUS", "")).strip().upper()

            clase_status = ""
            if "PROCESO DE CARGA" in status_raw:
                clase_status = "status-proceso"
            elif "CARGADO" in status_raw:
                clase_status = "status-cargado"
            elif "POR LLEGAR" in status_raw:
                clase_status = "status-por-llegar"

            html += '<tr>'
            html += f'<td>{destino}</td>'
            html += f'<td>{linea}</td>'
            html += f'<td>{operador}</td>'
            html += f'<td>{hora_llegada}</td>'
            html += f'<td class="{clase_status}">{status_raw}</td>'
            html += '</tr>'

        html += '</tbody></table>'
        html += f'<div class="footer-date">{fecha_actual}</div>'
        html += '</div>' # Cerrar contenedor-tv

        with placeholder_full.container():
            st.markdown(html, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error técnico real: {e}")
    
    time.sleep(3)

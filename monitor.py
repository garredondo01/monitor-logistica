import streamlit as st
import pandas as pd
import time

# Configuración de página a pantalla completa
st.set_page_config(page_title="Monitor de Operaciones", layout="wide")

# CSS para el diseño de tablero logístico
diseño_logistica = """
<style>
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Fondo completamente negro */
    .stApp {
        background-color: #000000;
    }
    
    /* Estilo del título */
    .titulo {
        text-align: center;
        color: #f1c40f;
        font-family: 'Courier New', Courier, monospace;
        font-size: 36px;
        margin-bottom: 20px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 5px;
        border-bottom: 2px solid #333;
        padding-bottom: 10px;
    }
    
    /* Estilo de la tabla de datos */
    .board-table {
        width: 100%;
        border-collapse: collapse;
        font-family: 'Courier New', Courier, monospace;
        background-color: #0a0a0a;
    }
    .board-table th {
        background-color: #1a1a1a;
        color: #7f8c8d;
        padding: 12px;
        font-size: 16px;
        text-align: left;
        border-bottom: 3px solid #333;
    }
    
    /* Color de las celdas normales (Destino, Linea, etc) */
    .board-table td {
        padding: 12px;
        font-size: 22px;
        color: #f1c40f; /* Letra amarilla por defecto */
        border-bottom: 1px solid #222;
        font-weight: bold;
        text-transform: uppercase;
    }
    
    /* COLORES DINÁMICOS PARA LOS NUEVOS ESTATUS */
    .status-proceso { color: #f1c40f !important; } /* Amarillo */
    .status-cargado { color: #2ecc71 !important; } /* Verde brillante */
    .status-por-llegar { color: #e74c3c !important; animation: parpadeo 1.5s infinite; } /* Rojo con alerta */
    
    /* Efecto de parpadeo para los tráileres por llegar */
    @keyframes parpadeo {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
</style>
"""
st.markdown(diseño_logistica, unsafe_allow_html=True)

# CONFIGURACIÓN: Tu ID de Google Sheets
SHEET_ID = "19VBW2abjR0UrBZ8QmKbKl9LY00O6eu3lzpCSJqeajYk"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# Título
st.markdown('<div class="titulo">🚛 MONITOR DE EMBARQUES 🚛</div>', unsafe_allow_html=True)

# Espacio dinámico para la tabla
placeholder = st.empty()

while True:
    try:
        # Leer datos de Google Sheets
        df = pd.read_csv(URL)
        df = df.fillna("") # Rellenar celdas vacías
        
        # Construir la estructura HTML de la tabla
        html_tabla = '<table class="board-table">'
        html_tabla += '<tr><th>DESTINO</th><th>LINEA</th><th>OPERADOR</th><th>HORA DE LLEGADA</th><th>STATUS</th></tr>'
        
        # Recorrer fila por fila
        for index, row in df.iterrows():
            destino = row.get("DESTINO", "")
            linea = row.get("LINEA", "")
            operador = row.get("OPERADOR", "")
            hora = row.get("HORA DE LLEGADA", "")
            status = str(row.get("STATUS", "")).strip().upper()
            
            # LÓGICA DE COLORES EXACTA CON TUS ESTATUS
            clase_status = ""
            if "PROCESO DE CARGA" in status:
                clase_status = "status-proceso"
            elif "CARGADO" in status:
                clase_status = "status-cargado"
            elif "POR LLEGAR" in status:
                clase_status = "status-por-llegar"
                
            # Agregar la fila a la tabla HTML
            html_tabla += f'<tr>'
            html_tabla += f'<td>{destino}</td>'
            html_tabla += f'<td>{linea}</td>'
            html_tabla += f'<td>{operador}</td>'
            html_tabla += f'<td>{hora}</td>'
            html_tabla += f'<td class="{clase_status}">{status}</td>' # Se aplica el color aquí
            html_tabla += f'</tr>'
            
        html_tabla += '</table>'
        
        # Proyectar en la pantalla
        with placeholder.container():
            st.markdown(html_tabla, unsafe_allow_html=True)
            st.write(f"<p style='color:#555; text-align:right; font-family:monospace;'>Actualizado: {time.strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error técnico real: {e}")
    
    # Recargar cada 3 segundos
    time.sleep(3)
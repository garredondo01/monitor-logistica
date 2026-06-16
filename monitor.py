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
# DISEÑO CSS ESTILO "MONITOR INDUSTRIAL ROTOPLAS"
# ==========================================
# Basado en la interfaz de aeropuerto pero con identidad Rotoplas
diseño_rotoplas = """
<style>
    /* Ocultar elementos de interfaz de Streamlit para modo Kiosko */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 1. Fondo de pantalla principal (Azul Industrial Profundo) */
    .stApp {
        background-color: #0c172a; /* Azul casi negro de fondo */
        color: white;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }

    /* 2. Contenedor del Encabezado Principal (Franja blanca superior) */
    .header-monitor {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: white; /* Franja blanca superior */
        color: #0072CE; /* Texto azul corporativo Rotoplas */
        padding: 10px 30px;
        border-bottom: 3px solid #0072CE; /* Línea azul de acento */
    }
    
    .logo-section-rotoplas {
        font-size: 32px;
        font-weight: 900; /* Letra muy gruesa para el logo */
        display: flex;
        align-items: center;
        text-transform: uppercase;
        letter-spacing: -1px;
    }
    
    .subtitle-rotoplas {
        font-size: 12px;
        margin-left: 10px;
        color: #555;
        font-weight: normal;
        text-transform: none;
        letter-spacing: 0px;
    }
    
    .title-section-main {
        font-size: 28px;
        font-weight: bold;
        text-transform: uppercase;
        text-align: center;
        flex-grow: 1;
        letter-spacing: 2px;
        color: #1a3c75; /* Azul más oscuro para el título */
    }
    
    .time-section-right {
        font-size: 24px;
        font-weight: bold;
        display: flex;
        align-items: center;
        color: #1a3c75;
    }
    .clock-icon-blue {
        background-color: #3498db;
        color: white;
        border-radius: 50%;
        width: 35px;
        height: 35px;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-right: 10px;
        font-size: 18px;
    }

    /* 3. Estilo de la Tabla de Datos Principal */
    .board-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 20px; /* Tamaño de letra general */
    }

    /* 4. Encabezados de Columna (Franja azul claro) */
    .board-table thead tr {
        background-color: #1e6cb3; /* Azul medio de los headers */
        color: white;
    }
    .board-table th {
        padding: 15px;
        text-align: left;
        font-weight: bold;
        text-transform: uppercase;
        border-right: 1px solid rgba(255,255,255,0.2);
    }
    
    /* 5. Filas de Datos (Alternadas Azul oscuro / Azul medio) */
    .board-table tbody tr {
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    
    /* Fila Impar (Oscura) */
    .board-table tbody tr:nth-child(odd) {
        background-color: #0c172a;
    }
    
    /* Fila Par (Más clara, como en la imagen de referencia) */
    .board-table tbody tr:nth-child(even) {
        background-color: #152d52; /* Un azul ligeramente más claro */
    }

    .board-table td {
        padding: 18px 15px;
        font-weight: bold;
        text-transform: uppercase;
        color: white;
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    /* 6. ESTILOS DINÁMICOS PARA 'STATUS' (Mantenemos tus colores) */
    .status-proceso { color: #f1c40f !important; } /* Amarillo */
    .status-cargado { color: #2ecc71 !important; } /* Verde */
    .status-por-llegar { color: #e74c3c !important; font-weight: bold;} /* Rojo */

    /* 7. Pie de Página (Fecha) */
    .footer-date {
        text-align: right;
        padding:
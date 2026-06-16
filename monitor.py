import streamlit as st
import pandas as pd
import time
from datetime import datetime

# ==========================================
# CONFIGURACIÓN DE PÁGINA (PANTALLA COMPLETA)
# ==========================================
st.set_page_config(page_title="OMA - Monitor de Operaciones", layout="wide")

# CONFIGURACIÓN: Tu ID de Google Sheets ya integrado
SHEET_ID = "19VBW2abjR0UrBZ8QmKbKl9LY00O6eu3lzpCSJqeajYk"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# ==========================================
# NUEVO DISEÑO CSS ESTILO "OMA MONTERREY"
# ==========================================
# Basado al 100% en la imagen de referencia: fondo azul, texto blanco sans-serif.
diseño_oma = """
<style>
    /* Ocultar elementos de interfaz de Streamlit para modo Kiosko */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 1. Fondo de pantalla principal (Azul OMA Profundo) */
    .stApp {
        background-color: #0c172a; /* Azul casi negro de fondo */
        color: white;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }

    /* 2. Estilo del Contenedor del Encabezado Principal */
    .oma-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: white; /* Franja blanca superior */
        color: #1a3c75; /* Texto azul oscuro en el header blanco */
        padding: 10px 30px;
        border-bottom: 2px solid #ccc;
    }
    
    .oma-logo-section {
        font-size: 24px;
        font-weight: bold;
        display: flex;
        align-items: center;
    }
    /* Placeholder para logo, puedes poner una imagen aquí luego */
    .oma-logo-placeholder {
        color: #e31d2b; /* Rojo para el acento de OMA */
        font-style: italic;
        margin-right: 10px;
        font-size: 30px;
    }
    
    .oma-title-section {
        font-size: 26px;
        font-weight: bold;
        text-transform: uppercase;
        text-align: center;
        flex-grow: 1;
    }
    
    .oma-time-section {
        font-size: 24px;
        font-weight: bold;
        display: flex;
        align-items: center;
    }
    .clock-icon {
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
        font-weight: normal;
        text-transform: capitalize; /* "Hora", "Destino", etc. */
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
    
    /* Fila Par (Más clara, como en la imagen) */
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

    /* 6. ESTILOS DINÁMICOS PARA 'STATUS' (Adaptados del diseño anterior pero sin parpadeo retro) */
    .status-proceso { color: #f1c40f !important; } /* Amarillo para Proceso */
    .status-cargado { color: #2ecc71 !important; } /* Verde para Cargado */
    /* Usamos el color de OMA para 'A TIEMPO', en este caso blanco/verde está bien. Rojo para alertas. */
    .status-por-llegar { color: #e74c3c !important; font-weight: bold;} /* Rojo para Por Llegar */

    /* 7. Pie de Página (Fecha) */
    .oma-footer {
        text-align: right;
        padding: 20px;
        color: rgba(255,255,255,0.6);
        font-size: 18px;
        font-weight: bold;
    }
</style>
"""
# Inyectar el CSS
st.markdown(diseño_oma, unsafe_allow_html=True)

# Espacio dinámico que se actualizará
placeholder_full = st.empty()

# Bucle de actualización en tiempo real
while True:
    try:
        # 1. Obtener Hora y Fecha actuales para el diseño
        ahora = datetime.now()
        hora_actual = ahora.strftime("%H:%M")
        fecha_actual = ahora.strftime("%d/%m/%Y")

        # 2. Leer datos de Google Sheets
        df = pd.read_csv(URL)
        df = df.fillna("") # Rellenar celdas vacías

        # ==========================================
        # CONSTRUCCIÓN DE LA ESTRUCTURA HTML (OMA)
        # ==========================================
        contenido_html = "<div>"

        # A. EL ENCABEZADO (Franja Blanca)
        contenido_html += f"""
        <div class="oma-header">
            <div class="oma-logo-section">
                <span class="oma-logo-placeholder">/</span> OMA
                <div style="font-size:12px; margin-left:5px; color:#555; font-weight:normal;">Operaciones Logísticas</div>
            </div>
            <div class="oma-title-section">
                SALIDAS / SALIDAS
            </div>
            <div class="oma-time-section">
                <div class="clock-icon">L</div> {hora_actual}
            </div>
        </div>
        """

        # B. LA TABLA DE DATOS
        # Adaptamos los encabezados de tu Excel a los nombres de la imagen de referencia
        contenido_html += """
        <table class="board-table">
            <thead>
                <tr>
                    <th>Hora<br><span style="font-size:12px;opacity:0.8;">Time</span></th>
                    <th>Destino<br><span style="font-size:12px;opacity:0.8;">To</span></th>
                    <th>Línea<br><span style="font-size:12px;opacity:0.8;">Carrier</span></th>
                    <th>Unidad / Vuelo<br><span style="font-size:12px;opacity:0.8;">Unit / Flight</span></th>
                    <th>Observación<br><span style="font-size:12px;opacity:0.8;">Remark (Status)</span></th>
                </tr>
            </thead>
            <tbody>
        """

        # C. RECORRER FILAS Y APLICAR COLORES DINÁMICOS
        for index, row in df.iterrows():
            # Mapeo de tus columnas de Google Sheets
            hora_llegada = row.get("HORA DE LLEGADA", "")
            destino = row.get("DESTINO", "")
            linea = row.get("LINEA", "")
            operador = row.get("OPERADOR", "") # Usamos Operador como ID de Unidad/Vuelo
            status_raw = str(row.get("STATUS", "")).strip().upper()

            # Lógica de colores del Status (Mantenemos tu lógica anterior)
            clase_status = ""
            if "PROCESO DE CARGA" in status_raw:
                clase_status = "status-proceso"
            elif "CARGADO" in status_raw:
                clase_status = "status-cargado"
            elif "POR LLEGAR" in status_raw:
                clase_status = "status-por-llegar"

            # Construir la fila HTML
            contenido_html += f"""
                <tr>
                    <td>{hora_llegada}</td>
                    <td>{destino}</td>
                    <td>{linea}</td>
                    <td>{operador}</td>
                    <td class="{clase_status}">{status_raw}</td>
                </tr>
            """

        contenido_html += """
            </tbody>
        </table>
        """

        # D. EL PIE DE PÁGINA (Fecha)
        contenido_html += f"""
        <div class="oma-footer">
            {fecha_actual}
        </div>
        """

        contenido_html += "</div>" # Cerrar contenedor principal

        # 3. Proyectar todo el HTML en la pantalla
        with placeholder_full.container():
            st.markdown(contenido_html, unsafe_allow_html=True)
            
    except Exception as e:
        # Mostrar error si falla la conexión a Google Sheets
        st.error(f"Error técnico real: {e}")
    
    # Recargar cada 3 segundos
    time.sleep(3)
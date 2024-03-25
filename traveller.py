# example/st_app.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st. set_page_config(layout="wide")

conn = st.connection("gsheets", type=GSheetsConnection)

st.markdown("<h1 style='text-align: center;'>CUMA</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>METAL MANUFACTURING SA DE CV</h4>", unsafe_allow_html=True)

# Limpiar variables de forma RFQ 


# Inicializar variables, cliente_input, user_name

if 'client_input' not in st.session_state or 'user_name' not in st.session_state or 'descripcion' not in st.session_state or 'pm_asignado' not in st.session_state or 'rfq_inquiry_date' not in st.session_state or 'rfq_mail' not in st.session_state or 'numero_RFQ' not in st.session_state:
    st.session_state.client_input = ''
    st.session_state.user_name = ''
    st.session_state.descripcion = ''
    st.session_state.pm_asignado = ''
    st.session_state.rfq_inquiry_date = ''
    st.session_state.rfq_mail = ''
    st.session_state.numero_RFQ = ''  # Inicializar numero_RFQ aquí



# Mostrar dataframes RFQ_Control & Clientes_df

col_izq, col_der = st.columns([3, 1])

col_izq.subheader("RFQ control")
rfq_control = conn.read(worksheet="Master_plan",ttl=5)
rfq_control = rfq_control.dropna(how = 'all')
col_izq.write(rfq_control.tail(10))

#------------------------------------------------------------------------------------------

# Crear un DataFrame de ejemplo

df = pd.DataFrame(rfq_control)

# Función para extraer valores basados en el estado "Open"
def extract_values(df):
    # Filtrar el DataFrame por el estado "Open"
    open_data = df[df['Status'] == 'Open']
    if not open_data.empty:
        # Extraer los valores y asignarlos a las variables de sesión
        st.session_state['O.P'] = open_data.iloc[0]['O.P']
        st.session_state['O.C'] = open_data.iloc[0]['O.C']
        st.session_state['Cliente'] = open_data.iloc[0]['Cliente']
        st.session_state['Usuario'] = open_data.iloc[0]['Usuario']
        st.session_state['part_num'] = open_data.iloc[0]['part_num']
        st.session_state['Descripcion'] = open_data.iloc[0]['Descripcion']
        st.write("Valores extraídos exitosamente para el estado 'Open'.")
    else:
        st.write("No hay datos con el estado 'Open'.")

# Llamar a la función para extraer los valores
extract_values(df)

# Mostrar los valores extraídos
st.write("Valores extraídos:")
st.write("O.P:", st.session_state.get('O.P'))
st.write("O.C:", st.session_state.get('O.C'))
st.write("Cliente:", st.session_state.get('Cliente'))
st.write("Usuario:", st.session_state.get('Usuario'))
st.write("part_num:", st.session_state.get('part_num'))
st.write("Descripcion:", st.session_state.get('Descripcion'))

# -------------------------------------------------------------------------------------

# Boton de agregar operación nueva e ir incrementando el número de operacion / variable




# Entrada de dato para operación

def username():
    st.session_state.user_name = st.session_state.user_name_key
    st.session_state.user_name_key = ''

st.text_input('Nombre y apellido de usuario', key='user_name_key', on_change=username, placeholder="Proporciona nombre + apellido")

st.write(f'Nombre de usuario proporcionado: {st.session_state.user_name}')
st.divider()
    

# Entrada de dato para rfq_inquiry_date
def inquiry_date():
    st.session_state.rfq_inquiry_date = st.session_state.rfq_inquiry_date_key
    st.session_state.rfq_inquiry_date_key = None

rfq_inquiry_date = st.date_input("Fecha en que se solicita RFQ", format="DD.MM.YYYY", value=None, key='rfq_inquiry_date_key', on_change=inquiry_date)

st.write(f'Fecha en que se solicita la cotización {st.session_state.rfq_inquiry_date}')
st.divider()

# Entrada de dato para RFQ_email

def email_keywords():
    st.session_state.rfq_mail = st.session_state.rfq_mail_key
    st.session_state.rfq_mail_key = ''

rfq_mail = st.text_input("Palabras clave de correo", placeholder="Texto para buscar en correo", key='rfq_mail_key', on_change=email_keywords)

st.write(f'Texto clave a buscar en el correo: {st.session_state.rfq_mail}')
st.divider()

# Creación de status como primer status = open

st.session_state.order_status = "Open"

st.write("El status de la orden comienza en: ", st.session_state.order_status)

# Boton para crear RFQ

if st.button("Crear RFQ"):
     actualizar_consecutivo(st.session_state.client_input)
     st.success(f"Nuevo número de RFQ para el cliente {st.session_state.client_input}: {st.session_state.numero_RFQ}")

# Mostrar los datos a cargar

st.markdown("<h4 style='text-align: center;'>Datos a cargar </h4>", unsafe_allow_html=True)

new_data = {
    "RFQ_num": [st.session_state.numero_RFQ],
    "RFQ_mail": [st.session_state.rfq_mail],
    "RFQ_inquiry_date": [st.session_state.rfq_inquiry_date],
    "PM_asignado": [st.session_state.pm_asignado],
    "Cliente": [st.session_state.client_input],
    "Usuario":[st.session_state.user_name],
    "Descripcion": [st.session_state.descripcion],
    "Status": [st.session_state.order_status]
}   

my_df = pd.DataFrame(new_data)

st.write(my_df)
st.warning("Revisar si los datos están correctos para poder cargarlos al sistema y confirmar")


#Agregar datos a la base principal RFQ Control

add_data = st.button("Agregar datos" )


# Restablecer valores cuando se agregan datos a df
    
if add_data:
    rfq_control = rfq_control.append(my_df, ignore_index=True)
    st.header("New File")
    st.write(rfq_control)
    conn.update(worksheet="1 rfq control", data= rfq_control)

    







    
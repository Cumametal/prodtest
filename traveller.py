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
    
if 'tentative_delivery_date' not in st.session_state or 'number_of_operations'not in st.session_state or 'number_of_operations'not in st.session_state or 'selected_fabrication_order'not in st.session_state:
    st.session_state.tentative_delivery_date= ''
    st.session_state.number_of_operations= ''
    st.session_state.selected_fabrication_order= ''


# Mostrar dataframes Master_plan and selected_fabrication_order

st.subheader("Master Plan")
rfq_control = conn.read(worksheet="Master_plan",ttl=5)
rfq_control = rfq_control.dropna(how = 'all')
st.write(rfq_control.tail(15))

#------------------------------------------------------------------------------------------

# Crear un DataFrame de ejemplo

df = pd.DataFrame(rfq_control)

# Función para extraer valores basados en el estado "Open"
def extract_values(df):
    # Filtrar el DataFrame por el estado "Open"
    open_data = df[df['RFQ_status'] == 'Open']
    if not open_data.empty:
        # Guardar todas las columnas necesarias en session_state
        for column_name in ['purchase_order', 'fabrication_order', 'customer', 'user', 'part_num', 'description']:
            st.session_state[column_name] = open_data[column_name]

# Llamar a la función para guardar los valores
extract_values(df)

# Mostrar los datos guardados en un DataFrame
if 'purchase_order' in st.session_state:
    df_open_data = pd.DataFrame({
        'Purchase Order': st.session_state['purchase_order'],
        'Fabrication Order': st.session_state['fabrication_order'],
        'Customer': st.session_state['customer'],
        'User': st.session_state['user'],
        'Part Number': st.session_state['part_num'],
        'Description': st.session_state['description']
    })
    st.write(df_open_data)

else:
    st.write("No hay datos con el estado 'Open'.")

# Llamar a la función para extraer los valores
extract_values(df)

# Mostrar los valores extraídos
# st.write("Valores extraídos:")

# st.write("purchase_order:", st.session_state.get('purchase_order'))
# st.write("fabrication_order:", st.session_state.get('fabrication_order'))
# st.write("customer:", st.session_state.get('customer'))
# st.write("user:", st.session_state.get('user'))
# st.write("part_num:", st.session_state.get('part_num'))
# st.write("description:", st.session_state.get('description'))


# Boton de seleccionar orden de fabricación para editar

def fab_order():
    st.session_state.selected_fabrication_order = st.session_state.fab_order_key
    st.session_state.fab_order_key = None

if 'fabrication_order' in st.session_state:
    selected_fabrication_order = st.selectbox('Select Fabrication Order', st.session_state['fabrication_order'].unique(), index=None, placeholder="Selecciona numero de órden de fabricación", on_change=fab_order, key='fab_order_key' )
    st.write('Selected Fabrication Order:', st.session_state.selected_fabrication_order)

# -------------------------------------------------------------------------------------

#Entrada de fecha para fecha tentativa de entrega 
    
    
def tentative_deliverydate():
    st.session_state.tentative_delivery_date = st.session_state.tentative_deliverydate_key
    st.session_state.tentative_deliverydate_key = None

tentative_delivery_date = st.date_input("Fecha en que se solicita RFQ", format="DD.MM.YYYY", value=None, key='tentative_deliverydate_key', on_change=tentative_deliverydate)

st.write(f'Fecha tentativa de entrega {st.session_state.tentative_delivery_date}')
st.divider()


# Boton de agregar operación nueva e ir incrementando el número de operacion / variable



# Entrada de dato para operación



def create_operation_columns():
    # Generate column names based on number_of_operations
    for i in range(1, st.session_state.number_of_operations + 1):
        process_col = f"process_{i}"
        operation_status_col = f"operation_status{i}"
        machine_hr_col = f"machine_hr{i}"
        labour_hours_col = f"labour_hours{i}"
        picture_col = f"picture{i}"

        # Use the generated column names as needed
        st.write(process_col, operation_status_col, machine_hr_col, labour_hours_col, picture_col)

        # Create text inputs and camera input for each set of columns
        process_val = st.text_input(f"Process {i}")
        operation_status_val = st.text_input(f"Operation Status {i}")
        machine_hr_val = st.text_input(f"Machine HR {i}")
        labour_hours_val = st.text_input(f"labour_hours{i}")
        picture_val = st.file_uploader(f"Upload Picture {i}", type=['jpg', 'jpeg', 'png'])

def update_values():
    # Update the values for each set of columns
    for i in range(1, st.session_state.number_of_operations + 1):
        process_val = st.session_state.get(f"process_input_{i}", "")
        operation_status_val = st.session_state.get(f"operation_status_input_{i}", "")
        machine_hr_val = st.session_state.get(f"machine_hr_input_{i}", "")
        labour_hours_val = st.session_state.get(f"labour_hours_input_{i}", "")
        picture_val = st.session_state.get(f"picture_input_{i}", "")

        # Use the values as needed, for example, print them
        st.write(f"Process {i}: {process_val}")
        st.write(f"Operation Status {i}: {operation_status_val}")
        st.write(f"Machine HR {i}: {machine_hr_val}")
        st.write(f"labour_hours  {i}: {labour_hours_val}")
        if picture_val is not None:
            st.image(picture_val)

def num_of_op():
    st.session_state.number_of_operations = st.session_state.num_of_op_key

st.number_input("Numero de operaciones requeridas", value=None, key='num_of_op_key', on_change=num_of_op, placeholder="Escribe un número entero...",step= 1)
st.write(f'Numero de operaciones a cargar: {st.session_state.number_of_operations}')

if st.button("Create Columns"):
    create_operation_columns()

if st.button("Update Values"):
    update_values()


# Boton para crear RFQ

# if st.button("Crear RFQ"):
#      actualizar_consecutivo(st.session_state.Datos)
#      st.success(f"Nuevo número de RFQ para el cliente {st.session_state.Datos}: {st.session_state.numero_RFQ}")

# Mostrar los datos a cargar

st.markdown("<h4 style='text-align: center;'>Datos a cargar </h4>", unsafe_allow_html=True)

# new_data = {
#     "RFQ_num": [st.session_state.numero_RFQ],
#     "RFQ_mail": [st.session_state.rfq_mail],
#     "RFQ_inquiry_date": [st.session_state.rfq_inquiry_date],
#     "PM_asignado": [st.session_state.pm_asignado],
#     "Cliente": [st.session_state.Datos],
#     "Usuario":[st.session_state.user_name],
#     "Descripcion": [st.session_state.descripcion],
#     "Status": [st.session_state.order_status]
# }   

#my_df = pd.DataFrame(new_data)

#st.write(my_df)
st.warning("Revisar si los datos están correctos para poder cargarlos al sistema y confirmar")


#Agregar datos a la base principal RFQ Control

add_data = st.button("Agregar datos" )


# Restablecer valores cuando se agregan datos a df
    
# if add_data:
#     rfq_control = rfq_control.append(my_df, ignore_index=True)
#     st.header("New File")
#     st.write(rfq_control)
#     conn.update(worksheet="1 rfq control", data= rfq_control)

    







    
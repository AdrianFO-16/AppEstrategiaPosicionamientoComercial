import streamlit as st
from utils import *
BASE_URL = 'https://docs.google.com/spreadsheets/d/1TWvLP6ixEKneycy6uI28nJZ4i1Ho2UG8cVXKT9Wxluk/edit#gid=141709839'
st.session_state.EMAIL_COL = 'Dirección de correo electrónico'
st.session_state.DATE_COL = "Marca temporal"

def general():
    data = get_data()
    row = data.mean(axis = 0)
    name = "General"
    fig = radial_plot(row, name)
    st.session_state.plot = fig


def individual():
    data = get_data()
    correo = st.selectbox("Correo", data.index)
    row = data.loc[correo]
    name = row.name
    fig = radial_plot(row, name)
    st.session_state.plot = fig


def configuracion():
    st.session_state.plot = None
    st.info('Recuerda hacer la liga pública y con acceso a cualquier persona', icon = "ℹ️")
    url = st.text_input('Liga a la hoja de sheets', BASE_URL)

    if not url:
        return
    try:
        preview = fetch_data(url)
    except:
        st.error("Error cargando datos, revisa que el Url es valido")
        return
    
    st.dataframe(preview)
    st.info('Si no es la tabla que esperabas, genera de nuevo el link pero teniendo abierta la hoja de sheets correcta', icon = "ℹ️")
    date = st.date_input("Incluir respuestas a partir de:")
    st.button("Confirmar", on_click= load_data, args = [preview, date])

    adv = st.checkbox('Configuracion Avanzada')
    if adv:
        st.session_state.DATE_COL = st.text_input("Columna de fecha", st.session_state.DATE_COL, on_change=lambda: st.toast("Columna de fecha cambiada"))
        st.session_state.EMAIL_COL = st.text_input("Columna de correo", st.session_state.EMAIL_COL, on_change=lambda: st.toast("Columna de correo cambiada"))



st.set_page_config(layout="wide")
# Streamlit app
def main():

    page = st.sidebar.selectbox("Página", ["Configuración", 'General', "Individual"])

    HEADER = st.container()

    with HEADER:
        st.title('Diagnóstico de la Estrategia Posicionamiento Comercial')

    st.divider()

    BODY = st.container()
    with BODY:
        _, col, _ = st.columns([0.05, 0.7, 0.05], gap = "small")
        try:
            match page:
                case "General":
                    general()
                case "Individual":
                    individual()
                case "Configuración":
                    configuracion()
        except UserWarning:
            return
        
        plot = st.session_state.get('plot')
        if plot:
            st.plotly_chart(plot)

if __name__ == '__main__':
    main()

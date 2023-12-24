import streamlit as st
from utils import *

st.set_page_config(layout="wide", page_title = "Diagnóstico de la Estrategia de Posicionamiento Comercial", page_icon = "📊")
st.session_state.EMAIL_COL = 'Dirección de correo electrónico'
st.session_state.DATE_COL = "Marca temporal"
st.session_state.URL = ''

with open('./version.txt', 'r') as file:
    VERSION = file.read()

def show_plot(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        plot = st.session_state.get('plot')
        if plot:
            st.plotly_chart(plot)
    return wrapper

@show_plot
def general():
    status, data = get_data()
    if not status:
        return
    row = data.mean(axis = 0)
    name = "General"
    fig = radial_plot(row, name)
    st.session_state.plot = fig

@show_plot
def individual():
    status, data = get_data()
    if not status:
        return
    correo = st.selectbox("Correo", data.index)
    row = data.loc[correo]
    name = row.name
    fig = radial_plot(row, name)
    st.session_state.plot = fig


def configuracion():
    st.session_state.plot = None
    st.info('Recuerda hacer la liga pública y con acceso a cualquier persona', icon = "ℹ️")
    st.session_state.URL = st.text_input('Liga a la hoja de sheets', st.session_state.URL)

    if not st.session_state.URL:
        return
    try:
        preview = fetch_data(st.session_state.URL)
    except:
        st.error("Error cargando datos, revisa que el Url es valido")
        return
    
    st.dataframe(preview)
    st.info('Si no es la tabla que esperabas, genera de nuevo el link pero teniendo abierta la hoja de sheets correcta', icon = "ℹ️")
    col1, col2, _ = st.columns([0.25, 0.25, 1])
    from_date = col1.date_input("Incluir respuestas desde:")
    to_date = col2.date_input("hasta:")
    st.button("Confirmar", on_click= load_data, args = [preview, from_date, to_date])

    adv = st.checkbox('Configuracion Avanzada')
    if adv:
        st.session_state.DATE_COL = st.text_input("Columna de fecha", st.session_state.DATE_COL, on_change=lambda: st.toast("Columna de fecha cambiada"))
        st.session_state.EMAIL_COL = st.text_input("Columna de correo", st.session_state.EMAIL_COL, on_change=lambda: st.toast("Columna de correo cambiada"))



# Streamlit app
def main():


    footer=f"""<style>
.footer {{
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}}
</style>
<div class="footer">
<p style="float:right">Version {VERSION}</p>
</div>
"""

    HEADER = st.container()
    with HEADER:
        st.title('Diagnóstico de la Estrategia de Posicionamiento Comercial')
    st.divider()


    BODY = st.container()
    with BODY:
        conf, gen, ind = st.tabs(["Configuración", 'General', "Individual"])
        _, col, _ = st.columns([0.1, 1, 0.1], gap = "small")
        with col:
            with gen:
                general()
            with ind:
                individual()
            with conf:
                configuracion()
    st.markdown(footer,unsafe_allow_html=True)

            
if __name__ == '__main__':
    main()

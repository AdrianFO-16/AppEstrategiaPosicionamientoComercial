import re
import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def check_url(url):

    # Define a regular expression pattern
    pattern = r"https://docs\.google\.com/spreadsheets/d/(\w+)/edit(?:\?.*)?#gid=(\w+)"

    # Use re.search to find matches in the URL
    match = re.search(pattern, url)

    # Check if there is a match
    if match:
        # Extract placeholders from the matched groups
        doc_id = match.group(1)
        page_id = match.group(2)
        return doc_id, page_id
    
    return '',''
    
def confirm_data(preview):
    st.session_state.data = preview
    st.balloons()

def parse_url(url):
    result = check_url(url)
    if not result:
        raise UserWarning("Url Inválido ingresado")
    return f"https://docs.google.com/spreadsheets/d/{result[0]}/export?format=csv&gid={result[1]}"
    

def get_data():
    data = st.session_state.get('data')
    try:
        if len(data) == 0:
            st.warning('Error, no se han cargado los datos')
            return None, None
    except TypeError:
        st.warning('Error, no se han cargado los datos')
        return None, None
    return True, data

def fetch_data(url):
    return pd.read_csv(parse_url(url))

def process_data(data):
    data = data.drop([st.session_state.DATE_COL], axis = 1).set_index(st.session_state.EMAIL_COL)
    for col in data.columns:
        new_col = col
        data[new_col] = data[col].apply(lambda x: len(re.findall(r'\)', x)))
    return data


def load_data(data, from_date, to_date):
    # try:
        if from_date > to_date:
            st.error(f"La fecha de inicio {from_date} no puede ser después que la de fin {to_date}")
            return
        data = date_filter(data, st.session_state.DATE_COL, from_date, to_date)
        if len(data) == 0:
            st.error(f"No hay ninguna fila a entre: {from_date} y {to_date}")
            return
        data = process_data(data)
    # except Exception as e:
    #     st.error("Error cargando los datos, asegurate que es la tabla correcta")
    #     return
        st.success(f'{len(data)} filas cargadas correctamente')
        st.session_state.data = data.groupby(st.session_state.EMAIL_COL).mean()


def date_filter(data, col, from_date, to_date):
    col_date = pd.to_datetime(data[col], dayfirst=True).apply(lambda x: x.date())
    return data[(col_date >= from_date) & (col_date <= to_date)]


#https://community.plotly.com/t/polar-chart-fill-percent-of-aea-like-a-pie-chart/15984
def radial_plot(row, name):

    status, data = get_data()
    if not status:
        return
    
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=row.values.tolist() + [row.values[0]],
        theta=data.columns.tolist()  + [data.columns[0]],
        fill='none',
        name=name,
        hovertemplate = "%{theta}<br>Valor: %{r:.2f}",
        marker = dict(color = "rgba(0,0,0,0)", symbol = "diamond", size = 6, line = dict(color = 'black', width = 1.5)),
        line = dict(color = "black")

    ))

    colors = [(0.21, "#0096ed"), (0.18,'#f20079'), (0.14, '#00d900')]
    for i, col in enumerate(data.columns):
        op, color = colors[(i)//3]
        fig.add_trace(go.Barpolar(
            r =[5.5], 
            theta= [col], width=[1],
            marker_color = color,
            opacity=op,
            hoverinfo = 'none'
        ))

    # Update layout
    fig.update_layout(
        title= "Diagnóstico de la Estrategia de Posicionamiento Comercial",
        title_x = None,
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5.5],
                tickmode="array",
                ticktext= ['','DEF.', 'CONS.', "COMP.", "AGR.", ''],            

                tickvals= list(range(1,7)),            
                linecolor='rgba(0,0,0,0)',
                tickangle = 90,
                angle=90,
                gridcolor="rgba(255,255,255,1)",
                tickfont = dict(size = 12, color=  'black')
            ),
            angularaxis = dict(
                tickfont = dict(size= 12),
                linecolor = "black",
                linewidth = 0.5
            ),
            bgcolor="rgba(0,0,0,0.1)"

        ),
        showlegend=False,
        autosize= False,
        width= 1200,
        height = 600,
        margin=dict(l=20, r=80, t=100, b=80)
    )


    return fig

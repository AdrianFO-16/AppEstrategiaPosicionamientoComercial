import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp
import re
import streamlit as st

# Sample data for demonstration
data = pd.read_csv('https://docs.google.com/spreadsheets/d/1TWvLP6ixEKneycy6uI28nJZ4i1Ho2UG8cVXKT9Wxluk/export?format=csv&gid=141709839')

data = data.drop(["Marca temporal"], axis = 1).set_index('Dirección de correo electrónico')

res_cols = []
for col in data.columns:
    # new_col = f"res_{col[0]}"
    new_col = col
    data[new_col] = data[col].apply(lambda x: len(re.findall(r'\)', x)))
    res_cols.append(new_col)


st.set_page_config(layout="wide")
# Streamlit app
def main():
    st.title('Resultados de Diagnóstico de Posicionamiento Comercial')

    _, col, _ = st.columns([0.05, 0.7, 0.05], gap = "small")

    st.divider()

    page = st.sidebar.selectbox("Página", ['General', "Individual"])


    if page == "General":
        row = data.mean(axis = 0)
        name = "General"
    else:
        correo = col.selectbox("Correo", data.index)
        row = data.loc[correo]
        name = row.name

    # Plotting
    fig = go.Figure()


    fig.add_trace(go.Scatterpolar(
        r=row.values.tolist() + [row.values[0]],
        theta=data.columns.tolist()  + [data.columns[0]],
        fill='tonext',
        name=name,
        hovertemplate = "%{theta}<br>Valor: %{r:.2f}"

    ))

    # Update layout
    fig.update_layout(
        title= "Diagnóstico de Posicionamiento Comercial",
        title_x = None,
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickmode="array",
                tickvals= list(range(1,6)),            
                linecolor='rgba(0,0,0,0)',
                linewidth=20,
                gridcolor="rgba(255,255,255,1)",
            ),
            angularaxis = dict(
                tickfont = dict(size= 12),
                tickangle = 0,
            ),
            bgcolor="rgba(0,0,0,0.1)"

        ),
        showlegend=False,
        autosize= False,
        width= 1200,
        height = 600,
        margin=dict(l=20, r=80, t=100, b=80)
    )

    col.plotly_chart(fig)

if __name__ == '__main__':
    main()

import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home"
)
image = Image.open ('logo.jpg')
st.sidebar.image(image, width=320)
st.sidebar.markdown( '# Curry Company')
st.sidebar.markdown( '## Fastest Delivery in Town')
st.sidebar.markdown("""---""")
st.write('# Curry Company Growth Dashbord')

st.markdown(
    """
    Growth Dashboard foi construido para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
    ### Como utilizar esse Growth Dashboard
    - Visao Empresa:
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadores semanais de crescimento.
        - Visão Geográfica: Insights de geolocalização.
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento
    - Visão Restaurante:
        - Indicadores semanais de crescimento dos restaurantes
        ### Ask for help
            antoniojunior0210@hotmail.com
        """
)
    
    


#Libraries
import plotly.express as px
import folium
from haversine import haversine
#----------------------------------
#Bibliotecas
import pandas as pd
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import folium_static
#-----------------------------------------
         #FUNÇÕES
#------------------------------------------------------------------------
def country_map(df1):
    df_aux = (df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']]
                 .groupby(['City', 'Road_traffic_density'])
                 .median()
                 .reset_index())
    df_aux = df_aux.head()
    maps = folium.Map()
    for index, location_info in df_aux.iterrows():
        folium.Marker( [location_info['Delivery_location_latitude'],
                        location_info['Delivery_location_longitude']],
                        popup=location_info[['City', 'Road_traffic_density']]).add_to(maps)
    folium_static(maps, width=1024 , height=600 )
    return None

def order_share_by_week(df1):
    df_aux1 = df1.loc[:, ['ID', 'week_of_year']].groupby( 'week_of_year' ).count().reset_index()

    df_aux2 = (df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby( 'week_of_year').nunique().reset_index())
    
    df_aux = pd.merge( df_aux1, df_aux2, how='inner', on='week_of_year' )
    df_aux['order_by_delivery'] = df_aux['ID'] / df_aux['Delivery_person_ID']

                                        # gráfico
    fig = px.line( df_aux, x='week_of_year', y='order_by_delivery' )
    return fig
#-------------------------------------------------------------------------------
def order_by_week(df1):
    #criar a colunha semana
    df1['week_of_year'] = df1.loc[:, 'Order_Date'].dt.strftime('%U')
                                      
    # Agrupando as colunas de ID e semana do ano para fazer o grafico
    df_aux= df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
    #desenhando o grafico
    fig= px.line(df_aux, x= 'week_of_year', y='ID')
    #st.plotly_chart(fig, user_container_width=True)
            
    return fig
#-------------------------------------------------------------------------------------------------------
def traffic_order_city(df1):
            
    df_aux = (df1.loc[:, ['ID', 'City', 'Road_traffic_density']]
                         .groupby(['City', 'Road_traffic_density'])
                         .count()
                         .reset_index())
    fig= px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City')
    return fig
#-------------------------------------------------------------------
def traffic_order_share(df1):
    df_aux =  (df1.loc[:, ['ID', 'Road_traffic_density']]
                  .groupby( 'Road_traffic_density')
                  .count().reset_index())
                    
    df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum()

    fig= px.pie(df_aux, values='entregas_perc', names= 'Road_traffic_density')
    return fig
#-----------------------------------------------------------------------------    
def order_metric(df1):
         #selecao de linhas
    cols= ['ID', 'Order_Date']
      # Quantidade de pedidos por dia
    df_aux = df1.loc[:, cols].groupby( 'Order_Date' ).count().reset_index()
      
      #desenhando grafico
    fig=px.bar(df_aux, x='Order_Date', y='ID')
    return fig
#--------------------------------------------------------------------------------
            
def clean_code(df1):
    """Esta função tem a responsabilidade de fazer a limpeza do dataframe:
    Tipos de limpeza:
    1. Remoção dos dados NaN
    2. Mudança dos tipos da coluna dos dados
    3.Remoção dos espaços das variaveis
    4. Formatação da coluna de datas
    5. Limpeza da coluna de tempo (Remoção do texto da variavel numérica)
    Imput: Dataframe
    Output: Dataframe       
    """
    

    #Removendo os 'NaNs' das linhas
    linhas_selecionadas = df1['Delivery_person_Age'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = df1['multiple_deliveries'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()


    linhas_selecionadas = df1['Road_traffic_density'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()
    linhas_selecionadas = df1['Weatherconditions'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = df1['City'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = df1['Time_taken(min)'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = df1['Festival'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()


    #Limpando a coluna e deixando somente o numero para poder tirar a media
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split( 'min)' )[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    # Convertendo a coluna Delivery_person_Age para numero inteiro
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)

    # Convertendo a coluna RATINGS de texto para numero decimal
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float) 

    #CONVERTENDO A COLUNA "ORDER DATE" de texto para DATA:
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')
    #CONVERTENTO A COLUNA MULTIPLE PARA NUMERO INTEIRO
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

    # REMOVENDO ESPAÇO DENTRO DE UM TEXTO
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Delivery_person_ID'] = df1.loc[:, 'Delivery_person_ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()
    return df1
#---------------------------------------------------------------------------------------

#import dataset
df = pd.read_csv(r"C:\Users\itxha\Repos\curso_ftc\aulas\dataset\train.csv.csv")
#------------------------------------------------
#Limpando dados
df1 = clean_code(df)
#-------------------

#=======================================================================
#Barra Lateral
#=======================================================================

st.header(' Marketplace - Customer View')
st.sidebar.markdown( '# Curry Company')
image_path = 'logo.jpg'
image= Image.open('logo.png')
st.sidebar.image(image, width=300)
st.sidebar.markdown('### The Expert in Killing Your Hunger')
st.sidebar.markdown('##### Ask for the app, website or phone')

st.sidebar.markdown( '## Fastest Delivery in Town')
st.sidebar.markdown( """---""")

st.sidebar.markdown('## Select a data limit')

date_slider= st.sidebar.slider(' Up to what value?', 
                  value=pd.datetime(2022, 4, 13), 
                  min_value=pd.datetime(2022, 2, 11), 
                  max_value=pd.datetime(2022, 4, 6), 
                  format='DD-MM-YYYY')
st.sidebar.markdown( """---""")

traffic_options = st.sidebar.multiselect( 'What are the conditions of transit?', 
                        ['Low', 'Medium', 'High', 'Jam'],
                        default= ['Low', 'Medium', 'High', 'Jam'])
st.sidebar.markdown( """---""")
st.sidebar.markdown( '### Powered by Antonio Junior')

#filtro de data
linhas_selecionadas =df1['Order_Date'] < date_slider
df1=df1.loc[linhas_selecionadas, :]

#filtro de transito
linhas_selecionadas= df1['Road_traffic_density'].isin( traffic_options )
df1=df1.loc[linhas_selecionadas, :]



#=======================================================================
               #Layout streamlit  
#=======================================================================
tab1, tab2, tab3 = st.tabs(['Managerial View', 'Tactical View', 'Geographic View'] )
with tab1:
    with st.container():
                #desenhando grafico de linhas
        fig= order_metric(df1)
        st.subheader('Orders by day')
        st.plotly_chart(fig, user_container_width=True)

        
    with st.container():
        col1, col2= st.columns(2)
        with col1:
            fig= traffic_order_share(df1)
            st.subheader(' Traffic Order Share')
            st.plotly_chart(fig, user_container_width=True)
            
        with col2:
            fig =traffic_order_city(df1)
            st.subheader(' Traffic Order City' )
            st.plotly_chart(fig, user_container_width=True)
            
            
            
with tab2:
    with st.container():
        st.markdown( "# Order by Week")
        fig= order_by_week(df1)
        st.plotly_chart(fig, user_container_width=True)

    with st.container():
        st.markdown( "# Order Share by Week")
        fig= order_share_by_week(df1)
        st.plotly_chart(fig, user_container_width=True)
        
        
    
with tab3:
    st.markdown('##### Country Map')
    country_map(df1)

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
#=======================================================================
    #FUNCTIONS
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
#===================================================================================================
def top_delivers(df1, top_asc):
    df_aux = (df1.loc[:, ['Delivery_person_ID', 'Time_taken(min)', 'City']]
                 .groupby(['City', 'Time_taken(min)'])
                 .max()
                 .sort_values(['City', 'Time_taken(min)'], ascending=top_asc).reset_index())
            
    df_aux1 = df_aux.loc[df_aux['City'] == 'Metropolitian', :].head(10)
    df_aux2 = df_aux.loc[df_aux['City'] == 'Urban', :].head(10)
    df_aux3 = df_aux.loc[df_aux['City'] == 'Semi-Urban', :].head(10)
    df3 = pd.concat( [df_aux1, df_aux2, df_aux3] ).reset_index( drop=True )
            
    return df3
#---------------------------------------------------------------------------------------

#import dataset
df = pd.read_csv(r"C:\Users\itxha\train.csv.csv")
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
image= Image.open(image_path)
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
            

                #LAYOUT STREAMLIT
tab1, tab2, tab3 = st.tabs( ['Managerial view', '_', '_'] )

with tab1:
    with st.container():
        st.title('Overall Metrics')
        col1, col2, col3, col4= st.columns(4, gap= 'large')
        
        
        with col1:
            maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
            col1.metric('Older age', maior_idade)

            
            
            
        with col2:
            menor_idade= df1.loc[:, 'Delivery_person_Age'].min()
            col2.metric('Minor age', menor_idade)
             
            
            
        with col3:
            pior_condicao = df1.loc[:, 'Vehicle_condition'].max()
            col3.metric('Worst condition of the vehicle', pior_condicao)
            
            
            
        with col4:
            
            melhor_condicao= df1.loc[:, 'Vehicle_condition'].min()
            col4.metric('Best vehicle condition', melhor_condicao)
        
                    
    with st.container():
        
        st.markdown("""---""")
        st.title('Assements')
        col1, col2= st.columns(2)
        with col1:
            st.markdown('##### Average rating per courier')
            
            df_avg_ratings_por_delivery = (df1.loc[:, ['Delivery_person_ID',
                                           'Delivery_person_Ratings']]
                                              .groupby('Delivery_person_ID')
                                              .mean()
                                              .reset_index())
            st.dataframe(df_avg_ratings_por_delivery)


        with col2:
            st.markdown('##### Average rating by traffic density ')
            #agrupando pelo 'Road_traffic_density' e agregando as operações de media e desvio padrao com a funcao "agg" para o Dataframe
            df_avg_std_ratings_by_traffic = (df1.loc[:, ['Road_traffic_density', 'Delivery_person_Ratings']]
                                 .groupby('Road_traffic_density')
                                 .agg({'Delivery_person_Ratings':['mean', 'std']}))

            #mudando o nome das colunas 
            df_avg_std_ratings_by_traffic.columns = ['delivery_mean', 'delivery_std']

            #resetando o index 
            df_avg_std_ratings_by_traffic = df_avg_std_ratings_by_traffic.reset_index()
            st.dataframe(df_avg_std_ratings_by_traffic)
      
            st.markdown('##### Average rating by weather type')
            df_avg_std_ratings_by_traffic = (df1.loc[:, ['Weatherconditions', 'Delivery_person_Ratings']]
                                            .groupby('Weatherconditions')
                                            .agg({'Delivery_person_Ratings':['mean', 'std']}))

            #mudando o nome das colunas 
            df_avg_std_ratings_by_traffic.columns = ['delivery_mean', 'delivery_std']

            #resetando o index 
            df_avg_std_ratings_by_traffic = df_avg_std_ratings_by_traffic.reset_index()
            st.dataframe(df_avg_std_ratings_by_traffic)
    with st.container():
        st.markdown("""---""")
        st.title('Delivery Speed')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('##### Top fastest couriers')
            df3= top_delivers(df1, top_asc=True)
            st.dataframe(df3)
        
        with col2:
            st.markdown('##### Top slowest couriers')
            df3= top_delivers(df1, top_asc=False)
            st.dataframe( df3 )
            

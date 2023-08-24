import datetime
import pandas as pd
import requests
import streamlit as st
import plotly.express as px

st.beta_set_page_config( layout='wide') # to center tables

ZC = ['ACAPULCO', 'AGUASCALIENTES', 'APATZINGAN', 'CABORCA', 'CAMARGO', 'CAMPECHE', 'CANCUN', 'CARMEN', 'CASAS-GRANDES', 'CELAYA', 'CENTRO-ORIENTE', 'CENTRO-SUR', 'CHETUMAL', 'CHIHUAHUA', 'CHILPANCINGO', 'CHONTALPA', 'CIENEGA', 'COATZACOALCOS', 'COLIMA', 'CONSTITUCION', 'CORDOBA', 'CUAUHTEMOC', 'CUAUTLA', 'CUERNAVACA', 'CULIACAN', 'DURANGO', 'ENSENADA', 'FRESNILLO', 'GUADALAJARA', 'GUASAVE', 'GUAYMAS', 'HERMOSILLO', 'HUAJUAPAN', 'HUASTECA', 'HUATULCO', 'HUEJUTLA', 'IGUALA', 'IRAPUATO', 'IXMIQUILPAN', 'IZUCAR', 'JIQUILPAN', 'JUAREZ', 'LA-PAZ', 'LAGUNA', 'LAZARO-CARDENAS', 'LEON', 'LOS-ALTOS', 'LOS-CABOS', 'LOS-MOCHIS', 'LOS-RIOS', 'LOS-TUXTLAS', 'MANZANILLO', 'MATAMOROS', 'MATEHUALA', 'MAZATLAN', 'MERIDA', 'MEXICALI', 'MINAS', 'MONCLOVA', 'MONTEMORELOS', 'MONTERREY', 'MORELIA', 'MORELOS', 'MOTUL-TIZIMIN', 'NAVOJOA', 'NOGALES', 'NUEVO-LAREDO', 'OAXACA', 'OBREGON', 'ORIZABA', 'PIEDRAS-NEGRAS', 'POZA-RICA', 'PUEBLA', 'QUERETARO', 'REYNOSA', 'RIVIERA-MAYA', 'SABINAS', 'SALTILLO', 'SALVATIERRA', 'SAN-CRISTOBAL', 'SAN-JUAN-DEL-RIO', 'SAN-LUIS-POTOSI', 'SAN-MARTIN', 'SANLUIS', 'TAMPICO', 'TAPACHULA', 'TECAMACHALCO', 'TEHUACAN', 'TEHUANTEPEC', 'TEPIC-VALLARTA', 'TEZIUTLAN', 'TICUL', 'TIJUANA', 'TLAXCALA', 'TUXTLA', 'URUAPAN', 'VDM-CENTRO', 'VDM-NORTE', 'VDM-SUR', 'VERACRUZ', 'VICTORIA', 'VILLAHERMOSA', 'XALAPA', 'ZACAPU', 'ZACATECAS', 'ZAMORA', 'ZAPOTLAN', 'ZIHUATANEJO']
SISTEMAS = ['SIN','BCA', 'BCS']


def zonaPML(sistema,zona,año_i,mes_i,dia_i,año_f,mes_f,dia_f):
  #Información requerida
  base_url = "https://ws01.cenace.gob.mx:8082/SWPEND/SIM/"
  mercados = ['MDA']
  plot_df = pd.DataFrame()


  for mercado in mercados:
    #Peticion
    peticion = base_url + sistema + '/' + mercado +'/'+ zona +'/'+ año_i +'/'+ mes_i +'/'+ dia_i +'/'+ año_f +'/'+ mes_f +'/'+ dia_f + '/JSON'
    response = requests.get(peticion)
    x = response.json()
    results = x['Resultados'][0]
    pml_zone = results['Valores']
    mem_df = pd.DataFrame(pml_zone)

    #Formato de datos
    mem_df['fecha']  = pd.to_datetime(mem_df['fecha'])
    mem_df['hora']   = mem_df['hora'].astype(int)
    mem_df['pz']     = mem_df['pz'].astype(float)
    mem_df['pz_ene'] = mem_df['pz_ene'].astype(float)
    mem_df['pz_per'] = mem_df['pz_per'].astype(float)
    mem_df['pz_cng'] = mem_df['pz_cng'].astype(float)
    mem_df['Periodo'] = mem_df['fecha'].astype(str) + ' : '+ mem_df['hora'].astype(str)
    mem_df.index = mem_df['fecha']

    #Renombramos columnas
    mem_df.rename(columns={'pz':'Precio Zonal (MXN/MWh)',
                           'pz_ene':'Componente Energía (MXN/MWh)',
                           'pz_per':'Componente Pérdidas (MXN/MWh)',
                           'pz_cng':'Componente Congestión (MXN/MWh)'},inplace=True)
      
    #Creamos una columna con la información del mercado asociado a esa petición  
    if mercado == 'MDA':
      mem_df['mercado'] = 'MDA'
    else:
      mem_df['mercado'] = 'MTR'

    #Concatenamos el df obtenido de la petición en plot_df
    plot_df = pd.concat([plot_df,mem_df],ignore_index=True)
    print(mercado + ': Petición concretada')


  
  ## Graficar
  fig = px.line(plot_df, x='Periodo', y='Precio Zonal (MXN/MWh)',title = zona + fecha_i + fecha_f )
  st.plotly_chart(fig, use_container_width=True)
  # estadistica
  prom = plot_df['Precio Zonal (MXN/MWh)'].mean()
  maxv = plot_df['Precio Zonal (MXN/MWh)'].max()
  minv = plot_df['Precio Zonal (MXN/MWh)'].min()
  
  stat_dict = {'Medida':['Promedio', 'Máximo', 'Mínimo'],
               'MXN/MWh': [round(prom,2),round(maxv,2),round(minv,2)]}

  stat_df = pd.DataFrame.from_dict(stat_dict) 
  stat_df = stat_df.set_index('Medida')
  st.dataframe(stat_df)
  
  ### ----------- FIN DE LA FUNCION ---------------
  



hoy = datetime.date.today()
with st.sidebar:
  sistema = st.selectbox('Sistema',SISTEMAS)
  zona = st.selectbox('Zona de carga',ZC)
  fecha_i = st.date_input("Fecha inicial", 
                          hoy)
  fecha_f = st.date_input("Fecha final",
                          hoy)
             

zonaPML(sistema,
        zona,
        str(fecha_i.year),
        str(fecha_i.month).zfill(2),
        str(fecha_i.day).zfill(2),
        str(fecha_f.year),
        str(fecha_f.month).zfill(2),
        str(fecha_f.day).zfill(2))


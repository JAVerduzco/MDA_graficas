import pandas as pd
import requests
import streamlit as st
import datetime
from datetime import timedelta
#st.sidebar.header('Selección de datos')


def zonaPML(sistema, zona,año_i,mes_i,dia_i,año_f,mes_f,dia_f):
  start_date = datetime.date(int(año_i), int(mes_i), int(dia_i))
  end_date = datetime.date(int(año_f), int(mes_f), int(dia_f))
  date_difference = (end_date - start_date).days
  print(date_difference)
  if date_difference > 6:
    # error_dias = "Máximo 7 días por solicitud."
    # return error_dias
    raise ValueError("Máximo 7 días por solicitud.")
  if date_difference <= -1:
    # error_dias = "Máximo 7 días por solicitud."
    # return error_dias
    raise ValueError("Fecha inicial posterior a fecha final.")

  #Información requerida
  base_url = "https://ws01.cenace.gob.mx:8082/SWPEND/SIM/"
  #mercados = ['MDA','MTR']
  plot_df = pd.DataFrame()

  #for mercado in mercados:
    #Peticion
  peticion = base_url + sistema +'/' + 'MDA' +'/'+ zona +'/'+ año_i +'/'+ mes_i +'/'+ dia_i +'/'+ año_f +'/'+ mes_f +'/'+ dia_f + '/JSON'
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
  mem_df['periodo'] = mem_df['fecha'].astype(str) + ' : H'+ mem_df['hora'].astype(str)
  mem_df.index = mem_df['fecha']

    #Renombramos columnas
  mem_df.rename(columns={'pz':'Precio Zonal (MXN/MWh)',
                           'pz_ene':'Componente Energía (MXN/MWh)',
                           'pz_per':'Componente Pérdidas (MXN/MWh)',
                           'pz_cng':'Componente Congestión (MXN/MWh)'},inplace=True)
      
    #Columna con la información del mercado asociado a esa petición  
#    if mercado == 'MDA':
 #     mem_df['mercado'] = 'MDA'
  #  else:
   #   mem_df['mercado'] = 'MTR'

    #Concatenamos el df obtenido de la petición en plot_df
  plot_df = pd.concat([plot_df,mem_df],ignore_index=True)
  #print('MDA' + ': Petición concretada')

  #Graficamos plot_df una vez hayamos terminado el loop  
  import plotly.express as px
  
  #Escogemos el valor de la columna Precio Zonal 
  st.write(f"""
  ### {zona} del {dia_i}-{mes_i}-{año_i} al {dia_f}-{mes_f}-{año_f}
  """
  )
  #st.line_chart(plot_df, x='periodo', y='Precio Zonal (MXN/MWh)')
  fig = px.line(plot_df, x='periodo', y='Precio Zonal (MXN/MWh)',title= zona )
  st.plotly_chart(fig)
  st.write(f""" Datos del periodo:
           
   Promedio: {plot_df['Precio Zonal (MXN/MWh)'].mean()},
           
   Máximo: {plot_df['Precio Zonal (MXN/MWh)'].max()},


   Mínimo: {plot_df['Precio Zonal (MXN/MWh)'].min()}.""")
  #fig.show()
ZC = ['ACAPULCO', 'AGUASCALIENTES', 'APATZINGAN', 'CABORCA', 'CAMARGO', 'CAMPECHE', 'CANCUN', 'CARMEN', 'CASAS-GRANDES', 'CELAYA', 'CENTRO-ORIENTE', 'CENTRO-SUR', 'CHETUMAL', 'CHIHUAHUA', 'CHILPANCINGO', 'CHONTALPA', 'CIENEGA', 'COATZACOALCOS', 'COLIMA', 'CONSTITUCION', 'CORDOBA', 'CUAUHTEMOC', 'CUAUTLA', 'CUERNAVACA', 'CULIACAN', 'DURANGO', 'ENSENADA', 'FRESNILLO', 'GUADALAJARA', 'GUASAVE', 'GUAYMAS', 'HERMOSILLO', 'HUAJUAPAN', 'HUASTECA', 'HUATULCO', 'HUEJUTLA', 'IGUALA', 'IRAPUATO', 'IXMIQUILPAN', 'IZUCAR', 'JIQUILPAN', 'JUAREZ', 'LA-PAZ', 'LAGUNA', 'LAZARO-CARDENAS', 'LEON', 'LOS-ALTOS', 'LOS-CABOS', 'LOS-MOCHIS', 'LOS-RIOS', 'LOS-TUXTLAS', 'MANZANILLO', 'MATAMOROS', 'MATEHUALA', 'MAZATLAN', 'MERIDA', 'MEXICALI', 'MINAS', 'MONCLOVA', 'MONTEMORELOS', 'MONTERREY', 'MORELIA', 'MORELOS', 'MOTUL-TIZIMIN', 'NAVOJOA', 'NOGALES', 'NUEVO-LAREDO', 'OAXACA', 'OBREGON', 'ORIZABA', 'PIEDRAS-NEGRAS', 'POZA-RICA', 'PUEBLA', 'QUERETARO', 'REYNOSA', 'RIVIERA-MAYA', 'SABINAS', 'SALTILLO', 'SALVATIERRA', 'SAN-CRISTOBAL', 'SAN-JUAN-DEL-RIO', 'SAN-LUIS-POTOSI', 'SAN-MARTIN', 'SANLUIS', 'TAMPICO', 'TAPACHULA', 'TECAMACHALCO', 'TEHUACAN', 'TEHUANTEPEC', 'TEPIC-VALLARTA', 'TEZIUTLAN', 'TICUL', 'TIJUANA', 'TLAXCALA', 'TUXTLA', 'URUAPAN', 'VDM-CENTRO', 'VDM-NORTE', 'VDM-SUR', 'VERACRUZ', 'VICTORIA', 'VILLAHERMOSA', 'XALAPA', 'ZACAPU', 'ZACATECAS', 'ZAMORA', 'ZAPOTLAN', 'ZIHUATANEJO']
SISTEMAS = ['SIN','BCA', 'BCS']
with st.sidebar:
  sistema = st.selectbox('Sistema',SISTEMAS)
  zona = st.selectbox('Zona de carga',ZC)
  fecha_i = st.date_input(
    "Fecha inicial",
    )
  fecha_f = st.date_input(
    "Fecha final",
    )
#zonaPML(zona,'2023','03','09','2023','03','10')
zonaPML(sistema, zona,str(fecha_i.year),'0'+str(fecha_i.month),'0'+str(fecha_i.day),str(fecha_f.year),'0'+str(fecha_f.month),'0'+str(fecha_f.day))





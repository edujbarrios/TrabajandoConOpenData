from geopy.geocoders import Nominatim
import folium
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns

# Leemos el archivo de Excel en una dataframe de pandas
df_paroCAN = pd.read_excel("paroCAN.xlsx")
df_paroCANsort = pd.read_excel("paroCAN.xlsx")
oficinas = pd.read_excel("oficina empleo.xlsx")

geolocator = Nominatim(user_agent="maps")

with open("muni.json") as f:
    muni_json = json.load(f)

municipio = oficinas['municipioTxt']
dir = oficinas['direccion']
dirT = dir.str.cat(oficinas['nombre'], sep=',')

oficinas.sort_values(by='municipioTxt', inplace=True)

latitud = oficinas['theGeomY']
longitud = oficinas['theGeomX']

valor_mun = df_paroCAN['TOTAL']

#Relacionamos el número de oficinas de empleo con la tasa de paro de Canarias
plt.scatter(df_paroCAN['TOTAL'],oficinas['municipioTxt'])
plt.ylabel('Oficinas de empleo')
plt.xlabel('Tasa de paro')
plt.title('Relación entre número de oficinas de empleo y tasa de paro en Canarias por municipio', fontsize = 12, fontweight = 'bold')
plt.show()

#Tenemos en cuenta tanto el rango HOMBRES como MUJERES
#HOMBRES
df_paroCANsort.sort_values(by='TOTAL', inplace=True)

plt.title('Representacion del % de paro en HOMBRES por cada municipio',  y=1.5, fontsize = 20, fontweight = 'bold')
plt.pie(df_paroCANsort['HOMBRES'], autopct='%1.1f%%', 
        pctdistance=1.1, labeldistance=1.2, radius = 2, wedgeprops={'linewidth': 3}, 
        colors=sns.color_palette("GnBu_r", 35), shadow = True)

plt.legend(loc="center left",
          bbox_to_anchor=(2, -0.2, 1.5, 1),
           fancybox=True,
          labels =df_paroCANsort['Municipios']
)
plt.show()

#MUJERES
plt.title('Representacion del % de paro en MUJERES por cada municipio',  y=1.5, fontsize = 20, fontweight = 'bold')
plt.pie(df_paroCANsort['MUJERES'], autopct='%1.1f%%', 
        pctdistance=1.1, labeldistance=1.2, radius = 2, wedgeprops={'linewidth': 3}, 
        colors=sns.color_palette("BrBG_r", 35), shadow = True)

plt.legend(loc="center left",
          bbox_to_anchor=(2, -0.2, 1.5, 1),
           fancybox=True,
          labels =df_paroCANsort['Municipios']
)
plt.show()

#Tenemos en cuenta el rango TOTAL
plt.bar(municipio, df_paroCAN['TOTAL'], color="darkblue")
plt.xticks(rotation=90)
plt.xlabel('Municipio', fontsize = 12, fontweight = 'bold')
plt.ylabel('Numero de personas desempleada', fontsize = 12, fontweight = 'bold')
plt.show()

#Trabajamos con los datos de municipios
plt.plot(oficinas['municipioTxt'], df_paroCAN['HOMBRES'], color = 'tab:purple', label = 'HOMBRES')
plt.plot(oficinas['municipioTxt'], df_paroCAN['MUJERES'], color = 'tab:green', label = 'MUJERES')
plt.legend(loc = 'upper right')
plt.xlabel('Municipio', fontsize = 12, fontweight = 'bold')
plt.ylabel('Numero de personas desempleada', fontsize = 12, fontweight = 'bold')
plt.xticks(rotation=90)
plt.show()


#Mostramos el número de gente desempleada por años
oficinas.set_index('municipioTxt',inplace=True)
df_paroCAN.sort_index(inplace=True)
pivot_table = df_paroCAN[['TOTAL', 'HOMBRES', 'MUJERES']]

pivot_table.plot(kind='area', stacked=True)
plt.xlabel('Año', fontsize = 12, fontweight = 'bold')
plt.ylabel('Numero de personas desempleada', fontsize = 12, fontweight = 'bold')
plt.show()


# Crea un mapa centrado en las islas canarias
m = folium.Map(location=[28.2915637, -16.6291304], zoom_start=9)

# Definimos la limitación de los municipios
folium.GeoJson(
    muni_json,
    style_function=lambda feature: {
        'fillColor': '#ffff00',
        'color': 'black',
        'weight': 2,
        'dashArray': '5, 5'
    }
).add_to(m)

# Marcamos las ubicaciones de las oficinas de empleo en el mapa
for dir in dirT:
    location = geolocator.geocode(dir, timeout=10)
    folium.Marker([location.latitude, location.longitude], popup=dirT).add_to(m)

# Mostrar el mapa
m

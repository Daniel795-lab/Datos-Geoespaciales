#!/usr/bin/env python
# coding: utf-8

# # IMT2118 - Taller 2.
# 
# 
# ## 1. Aspectos generales.
# 
# - Fecha de entrega: 10 de septiembre 2020, 23:59.
# 
# - Formato de entrega: carpeta comprimida (.zip) incluyendo Jupyter Notebook con el desarrollo (puede utilizar este mismo notebook), y las capas o archivos vectoriales que haya generado como parte de su análisis. El objetivo es que **el Notebook pueda correr completamente dentro de la carpeta entregada**. 
# 
# - Vía de entrega: a través de Canvas, correo electrónico con archivo adjunto o link para descarga (enviar a la profesora cc. al ayudante del curso).
# 
# - El trabajo es invididual, y cada estudiante trabajará con una región de Chile, de acuerdo a lo asignado para la Tarea 1 e indicado en la siguiente tabla:
# 
# | Estudiante | Región |
# |------------|---------|
# |Vicente Agüero |  V|
# |Matías Alarcón |  VI|
# |Pablo Bahamondes| VII|
# |Beatriz Cuervo| VIII|
# |Trindad Gatica| IX|
# |David Quiroz| X|
# |Josefa Silva| XI|
# |Daniel Ugalde| XIII|
# |Gerardo Ureta| XIV|
# |Tomás Valenzuela | XVI |
# 
# - El Taller debe ser desarrollada en lenguaje de programación Python. Com parte de su trabajo, puede utilizar QGIS según le acomode para visualizar capas o realizar alguna operación espacial, pero para efectos de la entrega todo debe estar desarrollado en Python.
# 
# - Se sugiere hacer consultas y comentarios sobre el Taller a traves del Foro del curso creado en Google Groups.
# 
# 
# ## 2. Datos para el Taller.
# 
# Para el desarrollo de este Taller, utilizaremos los mismos conjuntos de datos requeridos para el desarrollo de la Tarea 1. El objetivo de esta actividad es preparar un subconjunto de datos correspondiente a la región asignada a cada estudiante, de manera de facilitar el resto del trabajo.
# 
# #### 2.1 Cartografía Censo 2017
# 
# http://www.censo2017.cl/resultados-precenso-2016/#1483043043443-4db741fa-4733
# 
# La cartografía censal incluye varias capas de utilidad para este análisis, como por ejemplo:
# 
# 1. REGION_C17: límites regionales
# 2. COMUNA_C17: límites comunales
# 3. MANZANA_IND_C17: manzanas en zonas urbanas
# 4. MANZANA_ALDEA_C17: manzanas en zonas rurales
# 5. ENTIDAD_C17: entidares rurales
# 6. LIMITE_URBANO_CENSAL_C17: límite de las zonas urbanas (dentro de la cual se encuentran las manzanas urbanas).
# 
# 
# #### 2.2 Red de hidrográfica de Chile.
# 
# Link: https://drive.google.com/file/d/1mHJI-pjI24-Ce45D5YVVt93nbcCox6ii/view?usp=sharing
# 
# Capa con todos los ríos, vertientes, lagos y otras fuentes de agua en Chile.
# 
# #### 2.3 Sistemas de Agua Potable Rural (APR).
# 
# Link: https://dga.mop.gob.cl/estudiospublicaciones/mapoteca/Paginas/default.aspx#cinco
# 
# Ubicación de los sistemas de APR administrados por el MOP. Para efectos de este análisis, asumiremos que la información está actualizada, y que estos son los únicos APR existentes, aunque en realidad existen algunos otros financiados por SUBDERE (pero la información georreferenciada no está disponible).
# 
# *Nota:* estas suposiciones revelan algunas de las falencias comúnmente encontradas en cuanto a disponibilidad de datos espaciales a nivel público y privado.
# 
# 
# #### 2.4 Territorios operacionales de empresas sanitarias.
# 
# Link: https://drive.google.com/file/d/1mHJI-pjI24-Ce45D5YVVt93nbcCox6ii/view?usp=sharing
# 
# Zonas concesionada a empresas sanitarias de acuerdo a información publicada por la Superintendencia de Servicios Sanitarios (SISS). Corresponde al territorio cubierto por redes públicas de agua potable.
# 
# ## 4. Desarrollo.
# 
# 1. A partir de las conjuntos de datos indicados arriba, genere un nuevo conjunto de capas acotados únicamente a la región con la cual le corresponde trabajar, todas en sistema de coordenadas UTM.
# 2. Genere una figura donde se superpongan todas las capas generadas. Ud. puede definir las propiedades de visualización de cada capa, y no se evaluarán criterios gráficos en la medida que el mapa general de capas superpuestas sea comprensible.
# 3. A partir de su nuevo conjunto de datos, realice los cálculos necesarios para completar la siguiente tabla:
# 
# | Campo | Valor |
# |------------|---------|
# |Área total (Ha)| 1539625.6686917464 |
# |Área total de zonas urbanas (Ha)| 83845.949733251 |
# |Área total de entidades rurales (Ha)| 1429642.874566 |
# |Población urbana| 6823859 |
# |Población rural| 263441 |
# 
# 
# 

# In[1]:


import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point
import pyproj


# In[2]:


print(gpd.__version__)


# In[3]:


print(pyproj.__version__)


# In[4]:


#función para transformar CRS SIRGAS - WGS84 UTM 19 sur
def cambiocrs(archivo,crt):
    gdf = gpd.read_file(archivo + '.shp')    
    with open(archivo + '.prj') as prj_file:
        crs = prj_file.read()
    gdf.crs = crs
    gdf2 = gdf.to_crs(crt)
    return gdf2


# In[5]:


#No funciona
cambiocrs('R13/REGION_C17', 'EPSG:32719').crs


# In[6]:


#Carga de datos
#Censo 2017
rm=gpd.read_file('R13/region_utm.shp')
comuna=gpd.read_file('R13/comuna_utm.shp')
rural=gpd.read_file('R13/manzana_aldea_utm.shp')
urbana=gpd.read_file('R13/manzana_ind_utm.shp')
entrural=gpd.read_file('R13/entidad_utm.shp')
lu=gpd.read_file('R13/lu_utm.shp')
#Otros
hidro=gpd.read_file('hidrografiaChile.gpkg')
apr=gpd.read_file('APR_DOH_Enero_2016/APR_DOH_Enero_2016.shp')
potable=gpd.read_file('territoriosOperacionalesSanitarias.gpkg')


# In[5]:


rm.crs


# In[6]:


apr.crs


# In[7]:


potable.crs


# In[8]:


hidro.crs


# In[9]:


len(hidro)


# In[10]:


str(rm['geometry'][0]) #coordenadas UTM


# In[11]:


hidro.plot()


# In[12]:


potable.plot()


# In[13]:


apr.plot()


# In[14]:


rm.plot()


# In[15]:


apr.within(rm)


# In[16]:


apr_rm=gpd.overlay(apr,rm, how='intersection')
apr_rm.plot()
len(apr_rm)


# In[17]:


hidro_rm=gpd.overlay(hidro,rm, how='intersection')
hidro_rm.plot()
len(hidro_rm)


# In[18]:


potable_rm=gpd.overlay(potable, rm, how='intersection')
potable_rm.plot()
len(potable_rm)


# In[26]:


fig=plt.figure(figsize=(10,10))
ax=fig.add_subplot(111)

ax.set_aspect('equal')
apr_rm.plot(ax=ax, color='r', markersize=3)
hidro_rm.plot(ax=ax, color='b', edgecolor='b', lw=0.5)
potable_rm.plot(ax=ax, color='g')
rm.plot(ax=ax, color='none', edgecolor='k', lw=1.5)

plt.show()


# In[47]:


#Exportación de datos
#formato Shapefile (ESRI)
apr_rm.to_file('productos/shp/apr_RM.shp')
hidro_rm.to_file('productos/shp/hidro_RM.shp')
potable_rm.to_file('productos/shp/potable_RM.shp')
rm.to_file('productos/shp/RM.shp')

#formato GeoJSON
apr_rm.to_file('productos/geojson/apr_RM.geojson', driver='GeoJSON')
hidro_rm.to_file('productos/geojson/hidro_RM.geojson', driver='GeoJSON')
potable_rm.to_file('productos/geojson/potable_RM.geojson', driver='GeoJSON')
rm.to_file('productos/geojson/RM.geojson', driver='GeoJSON')

#formato GeoPackage
apr_rm.to_file("productos/gpkg/package.gpkg", layer='apr', driver="GPKG")
hidro_rm.to_file("productos/gpkg/package.gpkg", layer='hidro', driver="GPKG")
potable_rm.to_file("productos/gpkg/package.gpkg", layer='potable', driver="GPKG")
rm.to_file("productos/gpkg/package.gpkg", layer='rm', driver="GPKG")


# In[48]:


area_rm=rm.area.sum()*0.0001


# In[49]:


print('El área de la Región Metropolitana es:', area_rm, 'Ha')


# In[50]:


area_urbana=urbana.area.sum()*0.0001


# In[51]:


print('El área urbana de la Región Metropolitana es:', area_urbana, 'Ha')


# In[52]:


area_entrural=entrural.area.sum()*0.0001


# In[53]:


print('El área de las entidades rurales de la Región Metropolitana es:', area_entrural, 'Ha')


# In[54]:


pob_urb=urbana['TOTAL_PERS']


# In[55]:


print('La población urbana de la Región Metropolitana es:', sum(pob_urb), 'habitantes')


# In[56]:


pob_rural=entrural['TOTAL_PERS']


# In[57]:


print('La población rural de la Región Metropolitana es:', sum(pob_rural), 'habitantes')


# In[58]:


#NO funciono
mask=apr.geometry.squeeze().within(rm)
print(mask.sum(),len(apr))

apr_rm2=apr[mask]


# In[59]:


type(apr.geometry.squeeze())


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 18:35:35 2022

@author: Yahir
"""

import pandas as pd
import pandasql as ps
import time 
import numpy as np
import re
from selenium import webdriver

aux=pd.DataFrame()
aux.to_excel("df_BA.xlsx",index=False)

def Buscador_Precios_Selenium_BA(producto):  
    ### ingresamos a la pagina web 
    path ="/usr/local/bin/chromedriver"
    #path= mipath
    driver=webdriver.Chrome(path)
    url= "https://www.bodegaaurrera.com.mx/productos?Ntt="+producto
    driver.get(url)
    
    ####### Accedemos a los elementos que contienen los datos que queremos de la pagina web 
    
    productos= driver.find_elements_by_class_name("grid_product__30OQa")
    
    ### accedemos a las urls almacenadas en la variable productos

    lista_urls=list()
    for i in range(len(productos)):
        try:
            lista_urls.append(productos[i].find_element_by_tag_name("a").get_attribute("href"))
        except:
            lista_urls.append(np.nan)
            
    ### accedemos a los nombres de los productos

    lista_nombres=list()
    for i in range(len(productos)):
        try:
            lista_nombres.append(productos[i].find_elements_by_tag_name("a")[1].text)
        except:
            lista_nombres.append(np.nan)
            
    lista_precios=list()
    lista_promos=list()
    for i in range(len(productos)):
        try:
            lista_precios.append(productos[i].find_elements_by_class_name("product_price__2NBjj")[0].text.split("\n")[0])
        except:
            lista_precios.append(np.nan)
        try:
            lista_promos.append(productos[i].find_elements_by_class_name("product_price__2NBjj")[0].text.split("\n")[1])
        except:
            lista_promos.append(np.nan)
            
    df_BA =pd.DataFrame({"nombre":lista_nombres,"url":lista_urls,"precio1":lista_promos,"precio2":lista_precios})
    df_BA["autoservicio"]="bodega aurrera"
    df_BA["marca"]= producto
    df_BA["fecha"]= time.strftime("%d/%m/%y")

    df_BA = df_BA[["fecha","autoservicio","marca","nombre","url","precio1","precio2"]]
    ## este filtro apenas se agrega

    #df_soriana = df_soriana[df_soriana['nombre'].astype(str).str.contains(r'\b{}\b'.format(producto), regex=True, case=False)]
    df_BA  =df_BA.reset_index(drop=True)

    datos_webscraper=pd.read_excel("df_BA.xlsx")

    datos_webscraper= pd.concat([datos_webscraper,df_BA],axis=0)

    datos_webscraper.to_excel("df_BA.xlsx",index=False)

    driver.quit()
    return df_BA

for productos in ["iphone","beats","laptop"]:
    Buscador_Precios_Selenium_BA(productos)

df_BA=pd.read_excel("df_BA.xlsx")
df_BA

def precios_floats(datos): 
    #### eliminamos el signo de pesos de ambas columnas
    
    for i in range(len(datos["precio1"])):
        try:
            datos["precio1"].iloc[i]=datos["precio1"].iloc[i].strip("$")
        except:
            pass
        
    for i in range(len(datos["precio2"])):
        try:
            datos["precio2"].iloc[i]=datos["precio2"].iloc[i].strip("$")
        except:
            pass
        
    
    ### quitamos la separacion de comas para miles
    
    datos["precio1"]=datos["precio1"].replace(",","",regex=True)
    datos["precio2"]=datos["precio2"].replace(",","",regex=True)
        
    ### convertimos los precios a numericos    
    datos['precio1'] = pd.to_numeric(datos['precio1'], errors='coerce')
    datos['precio2'] = pd.to_numeric(datos['precio2'], errors='coerce')

    datos.to_excel("df_BA_limpio.xlsx",index=False)
        
     ### visualizamos los tipos de datos
    print(datos.dtypes)
    return datos

precios_floats(df_BA)
df_BA=pd.read_excel("df_BA_limpio.xlsx")
df_BA
    


            

    
















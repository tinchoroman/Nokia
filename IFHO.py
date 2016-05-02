import pandas as pd
import numpy as np
import matplotlib as plt
from pandas import Series, DataFrame
import xlrd


def Nodes_List(df,NodeColumn):
    #Funcion que recibe un DataFrame y un string con nombre de columna de Nodos
    #Devuelve Lista con Nombre unico de nodos
    return df[NodeColumn].unique().tolist()

def IntraNodeIFHODataFrame(df,NodeName):
    #Funcion recibe DatFrame y string con nombre de Nodo
    # y devuelve DataFrame con celdas Source y targuet del nodo especificado
    return df[(df.Source_SITE==NodeName) & (df.Target_SITE == NodeName)]

def IntraNodeIFHOTable(df):

    return df[df.Neighbor == 'Yes'].groupby([df['Source WCEL Name'],df['Target WCEL Name']]).att.sum().unstack()

def IFHOdict(df,Nodelist=None):
    # Recibe DataFrame y listado de nodo. En caso de no especificar listado de nodo, lo obtiene del DataFrame
    # Devuelve diccionario con key en cada Nodo y value de Matriz de IFHO intra nodo
    if Nodelist == None:
        Nodelist = Nodes_List(df,'Source_SITE')

    Nodes_tables_dcit = {}

    for node in Nodelist:
        Intra_Node_IFHO_DataFrame = IntraNodeIFHODataFrame(df,node)
        Intra_Node_IFHO_table = IntraNodeIFHOTable(Intra_Node_IFHO_DataFrame)
        Nodes_tables_dcit[node] = Intra_Node_IFHO_table
    return Nodes_tables_dcit

def MissingNeighbor(df, NodeList=None):
    if Nodelist == None:
        Nodelist = Nodes_List(df, 'Source_SITE')

    Nodes_tables_dcit = {}

    for node in Nodelist:
        Intra_Node_IFHO_DataFrame = IntraNodeIFHODataFrame(df, node)
        Missing_Neig_df = Intra_Node_IFHO_DataFrame [Intra_Node_IFHO_DataFrame.Neighbor == 'No']

        #if len(Missing_Neig_df)>0:



        Intra_Node_IFHO_table = IntraNodeIFHOTable(Intra_Node_IFHO_DataFrame)
        Nodes_tables_dcit[node] = Intra_Node_IFHO_table
    return Nodes_tables_dcit




# Abrimos excel con info de IFHO en la sheet Data
data = pd.read_excel('C:\Users\Tincho\PycharmProjects\Nokia\excel\RSRAN044_-_IFHO_Adjacencies.xlsx',sheetname='Data')
data.info()

# Se Filtran las ultimas 2 columnas Unnamed y se renombra columna SITE y se agrega info Source y Target SITE
data = data.ix[:,:-2]
data.rename(columns={'SITE':'Source_SITE'},inplace=True)
data['Source_SITE'] = data['Source WCEL Name'].map(lambda x:x[:6])
data['Target_SITE'] = data['Target WCEL Name'].map(lambda x:x[:6])
data.info()
Nodes = Nodes_List(data,'Source_SITE')
IFHO_dict = IFHOdict(data,Nodes)
print IFHO_dict[IFHO_dict.keys()[0]]

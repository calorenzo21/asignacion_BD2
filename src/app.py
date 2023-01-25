import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import queries
from fuzzywuzzy import fuzz,process


# Funcion para obtener un DataFrame a partir de una consulta SQL
def get_dataFrame(sql: sqlite3.Connection, query: str) -> pd.DataFrame:
    query = sql.execute(query)
    cols = [column[0] for column in query.description]
    df = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
    return df

# Funcion para limpiar un DataFrame
def clean_dataFrame(df: pd.DataFrame) -> pd.DataFrame:
    df = df.apply(lambda x: x.str.lower() if x.dtype == "object" else x)
    df = df.dropna()
    for column in df.columns:
        df[column] = df[column].str.replace(r'\W', '', regex=True)
        df[column] = df[column].str.replace(r'\d', '', regex=True)
    for column in df.columns:
        df[column] = df[df[column].str.strip().astype(bool)]
    return df

# Funcion para verificar si un nombre es similar a otro
def isMatch (value, group):
    fuzzy = process.extractOne(value, group, scorer=fuzz.token_sort_ratio)[1]
    if (fuzzy >= 80):
        return True
    return False

# Funcion para obtener el valor mas frecuente de una lista
def most_frequent(List):
    counter = 0
    num = List[0]
     
    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency> counter):
            counter = curr_frequency
            num = i
    return num


# Funcion para dar respuesta a la pregunta 1
def pregunta1(sql: sqlite3.Connection) -> None:

    # Seleccionar todas las respuestas
    df = get_dataFrame(sql, queries.quest1_q1)

    # Graficar la cantidad de estudiantes que conocen el EIU
    if (len(df) > 0):
        df.groupby(['num_opcion']).size().plot(kind='bar', subplots=True)
        plt.title('Cantidad de estudiantes que conocen el EIU')
        plt.show()

    # Graficar el porcentaje de estudiantes que conocen el EIU
    if (len(df) > 0):
        df.groupby(['num_opcion']).size().plot(kind='pie', subplots=True, autopct='%1.1f%%')
        plt.title('Porcentaje de estudiantes que conocen el EIU')
        plt.show()

    # Seleccionar las respuestas de los estudiantes que conocen el EIU
    df = get_dataFrame(sql, queries.quest1_q2)

    # Graficar la distribucion de estudiantes que conocen el EIU por carrera
    if (len(df) > 0):
        df.groupby(['titulo']).size().plot(kind='bar', subplots=True)
        plt.title('Distribucion de estudiantes que SI conocen el EIU por Carrera')
        plt.show()

    # Graficar el porcentaje de estudiantes que conocen el EIU por carrera
    if (len(df) > 0):
        df.groupby(['titulo']).size().plot(kind='pie', subplots=True, autopct='%1.1f%%')
        plt.title('Distribucion de estudiantes que SI conocen el EIU por Carrera')
        plt.show()

    # Seleccionar las respuestas de los estudiantes que NO conocen el EIU
    df = get_dataFrame(sql, queries.quest1_q3)

    # Graficar la distribucion de estudiantes que NO conocen el EIU por carrera
    if (len(df) > 0):
        df.groupby(['titulo']).size().plot(kind='bar', subplots=True)
        plt.title('Distribucion de estudiantes que NO conocen el EIU por Carrera')
        plt.show()

    # Graficar el porcentaje de estudiantes que NO conocen el EIU por carrera
    if (len(df) > 0):
        df.groupby(['titulo']).size().plot(kind='pie', subplots=True, autopct='%1.1f%%')
        plt.title('Distribucion de estudiantes que NO conocen el EIU por Carrera')
        plt.show()

    # Seleccionar las respuestas de los estudiantes que conocen el EIU por semestre
    df = get_dataFrame(sql, queries.quest1_q4)

    # Graficar la distribucion de estudiantes que conocen el EIU por semestre
    if (len(df) > 0):
        df.groupby(['titulo']).size().plot(kind='bar', subplots=True)
        plt.title('Distribucion de estudiantes que SI conocen el EIU por Semestre')
        plt.show()

    # Graficar el porcentaje de estudiantes que conocen el EIU por semestre
    if (len(df) > 0):
        df.groupby(['titulo']).size().plot(kind='pie', subplots=True, autopct='%1.1f%%')
        plt.title('Distribucion de estudiantes que SI conocen el EIU por Semestre')
        plt.show()

    # Seleccionar las respuestas de los estudiantes que NO conocen el EIU por semestre
    df = get_dataFrame(sql, queries.quest1_q5)

    # Graficar la distribucion de estudiantes que NO conocen el EIU por semestre
    if (len(df) > 0):
        df.groupby(['titulo']).size().plot(kind='bar', subplots=True)
        plt.title('Distribucion de estudiantes que NO conocen el EIU por Semestre')
        plt.show()

    # Graficar el porcentaje de estudiantes que NO conocen el EIU por semestre
    if (len(df) > 0):
        df.groupby(['titulo']).size().plot(kind='pie', subplots=True, autopct='%1.1f%%')
        plt.title('Distribucion de estudiantes que NO conocen el EIU por Semestre')
        plt.show()


# Funcion para dar respuesta a la pregunta 2
def pregunta2 (sql: sqlite3.Connection) -> None:
    df = get_dataFrame(sql, queries.quest2_q1)
    if (len(df) > 0): df = clean_dataFrame(df)
    match = False
    groups = []

    # Se agrupan las respuestas que son similares basado en la distancia de Levenshtein
    for index in df.index:
        match = False
        for i in range(len(groups)):
            if (isMatch(df._get_value(index, 'respuesta'), groups[i])):
                match = True
                break
        if (match):
            groups[i].append(df._get_value(index, 'respuesta'))
        else:
            temp_group = [df._get_value(index, 'respuesta')]
            groups.append(temp_group)
            match = False

    # Se crea un dataframe para ingresar a las cualidades con su respectiva ocurrencia
    df_values = pd.DataFrame()

    # Ingreso de cualidades y ocurrencias
    for index in range(len(groups)):
        temp_df_row = pd.DataFrame({"Cualidades": [most_frequent(groups[index])],"Ocurrencias": [len(groups[index])]})
        df_values = df_values.append(temp_df_row)

    # Se ordena el dataframe por la cantidad de ocurrencias
    df_values = df_values.sort_values(by = 'Ocurrencias', ascending = False)
    df_values = df_values.reset_index(drop=True)
    df_values_first3 = df_values.head(3)

    # Se muestra el grafico de barras
    df_values.plot(kind='bar', x='Cualidades', y='Ocurrencias')    
    plt.title('Diagrama de Barras de las cualidades que debe poseer un EIU')
    plt.show()

    # Se muestra el grafico de barras
    df_values_first3.plot(kind='bar', x='Cualidades', y='Ocurrencias')    
    plt.title('Diagrama de Barras de las cualidades que debe poseer un EIU')
    plt.show()

# Funcion para dar respuesta a la pregunta 3
def pregunta3(sql: sqlite3.Connection) -> None:
    df = get_dataFrame(sql, queries.quest3_q1)
    if (len(df) > 0): df = clean_dataFrame(df)
    match = False
    groups = []

    # Se agrupan las respuestas que son similares basado en la distancia de Levenshtein
    for index in df.index:
        match = False
        for i in range(len(groups)):
            if (isMatch(df._get_value(index, 'respuesta'), groups[i])):
                match = True
                break
        if (match):
            groups[i].append(df._get_value(index, 'respuesta'))
        else:
            temp_group = [df._get_value(index, 'respuesta')]
            groups.append(temp_group)
            match = False

    # Se crea un dataframe para ingresar a los estudiantes mas votados y la cantidad de votos
    df_votes = pd.DataFrame()

    # Ingreso de estudiantes mas votados y la cantidad de votos
    for index in range(len(groups)):
        temp_df_row = pd.DataFrame({"Estudiante": [most_frequent(groups[index])],"Votos": [len(groups[index])]})
        df_votes = df_votes.append(temp_df_row)

    # Se ordena el dataframe por la cantidad de votos
    df_votes = df_votes.sort_values(by = 'Votos', ascending = False)
    df_votes = df_votes.reset_index(drop=True)
    df_votes_first15 = df_votes.head(15)

    # Se muestra el grafico de barras
    df_votes_first15.plot(kind='bar', x='Estudiante', y='Votos')    
    plt.title('Estudiantes postulados a EIU')
    plt.show()

def main() -> None:

    try:
        sql = sqlite3.connect('data/dataset_prueba_2.s3db')
        pregunta1(sql)
        pregunta2(sql)
        pregunta3(sql)
    except sqlite3.Error as e:
        print(e)
    finally:
        sql.close()

if __name__ == '__main__':
    main()
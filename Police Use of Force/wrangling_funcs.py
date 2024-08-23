import numpy as np
import pandas as pd
import datetime as dt


def get_data_type(df):
    """ Returns the data types of each column in dataframe as a dictionary"""
    float64_dtype = df.select_dtypes(include=['float64']).columns.to_list()
    int64_dtype = df.select_dtypes(include=['int64']).columns.to_list()
    object_dtype = df.select_dtypes(include=['object']).columns.to_list()
    return {'float64_dtype':float64_dtype,'int64_dtype':int64_dtype, 'object_dtype':object_dtype}

def category_to_numeric_convertor(df):
    '''This function converts the categorial features to numeric equivalents''' 
    object_dtype = df.select_dtypes(include=['object'])
    object_dtype_cat = object_dtype.apply(lambda col:col.astype('category'))
    object_dtype_categorized = object_dtype_cat.apply(lambda col:col.cat.codes)
    return object_dtype_categorized
def get_missing_data(df):
    '''This function returns missing percentage of each column in the original dataframe''' 
    missing_data = pd.concat([df.isna().sum(), 100 * df.isna().mean()], axis=1)
    missing_data.columns = ['count', 'missing %']
    return missing_data.sort_values(by='count', ascending=False)

def stringdate_to_datetime(df,date_columns):
    '''This function converts string date columns to the datetime format''' 
    df_new_datecol = df[date_columns].apply(lambda col:pd.to_datetime(col, format='mixed'))
    #df_new_datecol = df[date_columns]
    for col in date_columns:
        df_new_datecol[col] = pd.to_datetime(df_new_datecol[col].apply(lambda col:col.strftime("%Y-%m")),format="%Y-%m")
        #df_new_datecol[col]= pd.to_datetime(df_new_datecol[col],format="%Y-%m", errors='coerce').dt.strftime("%Y-%m")
    #https://stackoverflow.com/questions/58948809/why-do-i-get-valueerror-nattype-does-not-support-strftime-even-though-its-no
    df[date_columns] = df_new_datecol
    return df

def get_unique(df, text_to_search):
    '''This function returns missing percentage of each column in the original dataframe''' 
    Cols = [item for item in df.columns.tolist() if text_to_search in item]
    column_unique = {item : df[item].unique() for item in Cols}
    # number of unique items in each column of location type
    column_nunique = {item : df[item].nunique() for item in Cols}
    return column_unique, column_nunique

def get_xpercent_missing_data(df, percentage):
    '''This function returns missing percentage of each column in the original dataframe''' 
    missing_data = pd.concat([df.isna().sum(), 100 * df.isna().mean()], axis=1)
    missing_data.columns = ['count', 'missing %']
    missing_data = missing_data.sort_values(by='count', ascending=False)
    #missing_data = get_missing_data(df)
    ## missing values less than percent%
    col_lessthan_xperc = missing_data[~(missing_data['missing %'] > percentage)] 
    col_morethan_xperc = missing_data[missing_data['missing %'] > percentage] 
    return col_lessthan_xperc, col_morethan_xperc

def reverse_hot_encod(df, text_to_search, new_col_name):
    LocationTypeCols = [item for item in df.columns.tolist() if text_to_search in item]
    LocationTypeColsdf = df[LocationTypeCols].fillna(0).astype(int)
    df.drop(columns=LocationTypeCols, inplace=True)
    df[new_col_name] = pd.DataFrame(LocationTypeColsdf.columns[np.where(LocationTypeColsdf!=0)[1]])
    return df

# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 18:56:16 2022

@author: investree
"""

from connection import Engine
import pandas as pd 

class Processing:
    
    #Initialize connection to database
    def __init__(self,config_path,db_type,sql_type):
        self.engine = Engine(config_path,db_type,sql_type)
        self.connection = self.engine.get_engine()
        pass
    
    #Insert dataframe to destination table  
    def dataframe_to_table(self,data,schema,table_name):
        data.to_sql(table_name, 
                    self.connection, 
                    schema=schema, 
                    if_exists='append', 
                    index=False)
        return print('DF TO TABLE Success')
    
    #Remove null values in a column
    def remove_null(self,df,column_name):
        df = df[df[column_name].notna()]
        df.reset_index(drop=True, inplace=True)
        return df
    
    #Get time difference between two timestamp in hours
    def get_hours_diff(self,df,first_date,second_date,column_name):
        df[column_name] = (first_date - second_date) / pd.Timedelta(hours=1)
        return df[column_name]
    
    #Fix time difference below zero
    def fix_minus_hours(self,df,column):
        df[column] = df[column].map(lambda x: x+24 if x < 0 else x+0)
        return df[column]
        
    #Extract year or month from a date
    def date_to_ym(self,df,column,form):
        if form == 'year':
            col = df[column].map(lambda x: x[:4])
        elif form == 'month':
            col = df[column].map(lambda x: x[5:7])
        return col
        
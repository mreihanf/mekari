# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 15:08:19 2022

@author: investree
"""


import pandas as pd

#Create variable for today's date
import datetime
now = datetime.datetime.now()
today = now.strftime('%Y-%m-%d')

from processing import Processing
config_path = 'config.ini'
#Get connection for database with config file path, database name, and database type as parameters
p = Processing(config_path,'dwh','postgresql')

try:
    
    #Import CSV for Employees and Timesheets while parsing Timestamp
    employees = pd.read_csv('employees.csv')
    timesheets = pd.read_csv('timesheets.csv',parse_dates=['checkin', 'checkout'])
    
    #Drop rows with NULL Check In time or Check Out time
    timesheets = p.remove_null(timesheets, 'checkin') 
    timesheets = p.remove_null(timesheets, 'checkout')
    
    #Create column for time difference or working hours between checkin and checkout in hours
    timesheets['working_hours'] = p.get_hours_diff(timesheets,timesheets.checkout,timesheets.checkin,'working_hours')
    
    #Fix time difference that has a value below 0
    timesheets['working_hours'] = p.fix_minus_hours(timesheets, 'working_hours')
    
    #Create new column for Year and Month
    timesheets['year'] = p.date_to_ym(timesheets,'date','year') 
    timesheets['month'] = p.date_to_ym(timesheets,'date','month')
    
    #Join employees and timesheets table
    employee_timesheets = pd.merge(employees, timesheets, left_on='employe_id',right_on='employee_id', how='inner')
    
    #Create SUM of working hours per employee, branch, month, and year
    employee_timesheets=employee_timesheets.groupby(['year','month','branch_id','employee_id','salary'])['working_hours'].sum()
    employee_timesheets=employee_timesheets.reset_index()
    
    #Create SUM of salary and working hours per branch, month, and year
    employee_timesheets=employee_timesheets.groupby(['year','month','branch_id'])[['salary','working_hours']].sum()
    employee_timesheets=employee_timesheets.reset_index()
    
    #Create new column for salary per hour by dividing salary and working hours
    employee_timesheets['salary_per_hour'] = employee_timesheets['salary'] / employee_timesheets['working_hours']
    employee_timesheets=employee_timesheets[['year','month','branch_id','salary_per_hour']]
    
    #Create new column for data date
    employee_timesheets.insert(0, 'insert_date', today)
    
    #Apply function to insert from dataframe to table with dataframe name, schema, and table name as parameters
    p.dataframe_to_table(employee_timesheets,'sbx','salary')

except BaseException as error:
    #Return and error exactly as it is
    print('An exception occurred: {}'.format(error))

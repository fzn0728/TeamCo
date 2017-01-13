# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 14:30:27 2016

@author: ZFang
"""
import pandas as pd
import numpy as np

def concat_data(filename):
    '''Concate all excel sheets and organize them into a dataframe, and add necessary columns (Date, Year) for future use.
    
    Given a well-format excel sheet with fixed column names, extract the updated information and put 
    it into dataframe.
    
    Args:
        filename is the string format of excel file name

    Returns:
        A dataframe which contains all necessary informaton
    '''
    df_fund = pd.ExcelFile(filename)
    sheet_name = df_fund.sheet_names[0:5]
    index = list(range(0,len(df_fund.parse(sheet_name[1]).iloc[:,0])))
    columns = ['Date']
    df_data = pd.DataFrame(index = index, columns = columns)
    df_data['Date'] = df_fund.parse(sheet_name[1]).iloc[:,0]
    for i in range(0,len(sheet_name)):
        a = df_fund.parse(str(sheet_name[i])).drop('Date',1)
        df_data = pd.concat([df_data,a], axis = 1)
    # Generate year column for future calculation
    df_data['Year'] = pd.DatetimeIndex(df_data['Date']).year
    return df_data
    
    
    
def multiple_dfs(df_list, sheets, file_name, spaces):
    '''This function can put a list of dataframe into one excel sheet, concat row by row and also add title to each dataframe
    
    Args:
        df_list is the list of all dataframe
        sheets is the name of excel sheet
        file_name is the name of excel file
        spaces is the blank row between each dataframe output in the excel sheet
        
    Returns:
        An excel sheet with multi dataframe table in on single excel sheet
    '''
    writer = pd.ExcelWriter(file_name, engine = 'xlsxwriter')
    row = 0
    for dataframe in df_list:
        dataframe.to_excel(writer, sheet_name=sheets, startrow=row, startcol=0)
        worksheet = writer.sheets[sheets]
        worksheet.write_string(row,0, dataframe.name)
        row = row + len(dataframe.index) + spaces + 1
    writer.save()
    
    
    
    
def multiple_sheets(df_list, file_name):
    writer = pd.ExcelWriter(file_name, engine = 'xlsxwriter')
    for dataframe in df_list:
        dataframe.to_excel(writer, '%s' %dataframe.name)
    writer.save()
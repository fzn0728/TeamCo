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
    sheet_name = df_fund.sheet_names
    index = list(range(0,len(df_fund.parse(sheet_name[1]).iloc[:,0])))
    columns = ['Date']
    df_data = pd.DataFrame(index = index, columns = columns)
    df_data['Date'] = df_fund.parse(sheet_name[1]).iloc[:,0]
    for i in range(0,len(sheet_name)):
        a = df_fund.parse(str(sheet_name[i])).drop('Date',1)
        df_data = pd.concat([df_data,a], axis = 1)
    # Generate year column for future calculation
    # df_data['Year'] = pd.DatetimeIndex(df_data['Date']).year
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
    workbook  = writer.book
    # Initial Format
    format1 = workbook.add_format({'num_format': '#,###0.000'})
    format1.set_align('center')
    format2 = workbook.add_format({'num_format': '0.00%'})  
    format2.set_align('center')
    format3 = workbook.add_format({'num_format': 'General'})
    format3.set_align('center')
    format3.set_bold()
    
    # Paste dataframe
    for dataframe in df_list:
        dataframe.to_excel(writer, sheet_name=sheets, startrow=row, startcol=0)
        worksheet = writer.sheets[sheets]
        worksheet.write_string(row, 0, dataframe.name)
        row = row + len(dataframe.index) + spaces + 1
    # Change format
    worksheet.set_column('A:A', 45, format3)    
    worksheet.set_column('B:B', 23, format1)
    worksheet.set_column('C:C', 18, format1)
    worksheet.set_column('D:D', 18, format1)    
    worksheet.set_column('E:E', 18, format1)
    worksheet.set_column('F:F', 18, format1)
    worksheet.set_column('G:G', 18, format1)
    worksheet.set_column('H:H', 18, format1)
    worksheet.set_column('I:I', 18, format1)
    worksheet.set_column('J:J', 18, format1)
    worksheet.set_column('K:K', 18, format1)
    worksheet.set_row(1, 20, format2)
    worksheet.set_row(2, 20, format2)
    worksheet.set_row(3, 20, format2)
    worksheet.set_row(6, 20, format2)
    worksheet.set_row(7, 20, format2)
    worksheet.set_row(8, 20, format2)
    writer.save()
    
def multiple_sheets(df_list, file_name):
    '''This function could put rolling dataframe into different sheets within a single excel file
    
    Args:
        df_list is the list of all dataframe
        file_name is the name of excel file
    '''
    # d = {}
    writer = pd.ExcelWriter(file_name, engine = 'xlsxwriter')
    workbook  = writer.book
    # Initial Format
    format1 = workbook.add_format({'num_format': '#,###0.000'})
    format1.set_align('center')
    format2 = workbook.add_format({'num_format': '0.00%'})  
    format2.set_align('center')
    format3 = workbook.add_format({'num_format': 'General'})
    format3.set_align('center')
    format4 = workbook.add_format({'num_format': 'General'})
    format4.set_align('center')
    format4.set_bold()
    format4.set_border()
    format5 = workbook.add_format({'num_format': '#,###0.000'})
    format5.set_align('center')
    format5.set_border()
    # Paste dataframe
    for dataframe in df_list:
        dataframe.to_excel(writer, '%s' %dataframe.name)
        # d["{0}".format(dataframe)] = writer.sheets[dataframe.name]
        # d[dataframe].set_column('A:A', 35, format3)
        # d[dataframe].set_column('B:B', 18, format1)
        # d[dataframe].set_column('C:C', 18, format1)
        # d[dataframe].set_column('D:D', 18, format1)
        writer.sheets[dataframe.name].set_column('A:A', 26, format4)
        writer.sheets[dataframe.name].set_column('B:B', 23, format5)
        writer.sheets[dataframe.name].set_column('C:C', 23, format5)
        writer.sheets[dataframe.name].set_column('D:D', 23, format5)
        writer.sheets[dataframe.name].set_column('E:E', 23, format5)
        
    writer.save()
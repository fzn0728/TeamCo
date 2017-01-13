1. Performance Analysis

Given data from excel with certain format, get all major financial ratio and rolling ratio and other important graph 

• Fund_Analysis.py is the main file, please change data_file_path to your local path if you want to run the code, it will generate Fund Analysis.xlsx file which contains all dataframe and Rolling Ratio Figure and Radar Chart Result.pdf which has all charts.
• mod_basic_fin_ratio.py is the basic package for calculating basic ratio
• mod_financial_ratio.py is based on mod_basic_fin_ratio and add the format
• mod_rolling.py is the package for rolling data
• mod_input_output.py is the package for cleaning the data and output excel and pdf file
• mod_plot is the package for all the plotting.
• Fund Analysis.xlsx is the original data source. PS: I changed the format of xlsx a liitle bit(two parts, one is deleting one Russell 3000 index, since there are two, and the other is add 6 columns to market index to make sure that all index/fund/competitor have the same starting date.
• Test_data.xlsx is the testing data source, which I manually deleted some data sets to test its robustness
• Fund Analysis_cross check.xlsx is the original result which is used for cross checking.



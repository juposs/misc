# requirements:
1. collect all your pdf files your want to import/analyze into one folder and set  the variable 'pdf_directory' to that directory
2. provide a target csv/ods file you want the results to end up in, i provide a template for that, feel free to rename that to anything you like. Afterwards set the variable 'summary_file' to that path including the filename
3. fill the categories dictionary with your custom categories. Each key in the dictionary will end up as its own line in the summary file, where all strings defined in that key's values list are used to match the potentially different payments. You defintetely need to glance over your pdf's you want to import first to identify strings to want to match to. For instance, maybe you have a mobile phone contract with Vodafone and a second one with Telekom. But you still want both of those payments to be matched to the category "mobilephne". Or maybe you want to seperate/combine the gas you need for your car and other payments neccessary for your car.
Every payment not found within the value lists of all categories will be assinged to the "Other" category. So you can easily sort the table for that category and adjust your matching in the script for future imports, too. I've levt some example categories in to give you some ideas, feel free to use them or not.
4. Ensure the following pip packages are installed on the machine importing your pdf's: ezodf,  PyPDF2

# Further things to note
1. only tested and verified with the bank "Raiffeisenbank" and only german files since im using certain phrases to cut off stuff above and below actual payments, see line 71 - 75
2. currency is set to EUR - see line 135 for that
3. sheet names are defined in line 48 as "Übersicht" and 55 as "Buchungsübersicht"
4. make sure to empty our import directory from step 1 after the script was executed. It will add every payment a second time. The script is not smart enough to understand that the provided data has already been imported previously. So it's important to keep only files in that directory that have not yet been imported. Or you start a new file and import everything again of course.

# Possible imporovments in the future
## this will at least take care of 2 - 4 of the 'further things to note'
- more methods and functions to get a better structure and readability 
- move category definitions into its on file
- transform currency and sheet names into variables
- (eventually rename and) move all variables into its own file: summary_file, pdf_directory, cell_currency, summary_sheet_name, payments_sheet_name
- move all files that have been imported to a "imported" directory in the same path as "pdf_directory", if needed even create it
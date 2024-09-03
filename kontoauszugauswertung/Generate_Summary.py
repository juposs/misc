# TODO do some cleaning up, ie. seperating stuff into different methods/functions is probably a good idea

from PyPDF2 import PdfReader
import re
import os
from ezodf import Sheet, opendoc

summary_file="C:\\path\\to\\Summary.ods"
# pdf_directory = "C:\\Backup\\Nützliches\\Kontoauszugauswertung\\Kontoauszüge\\"
# NOTE directory to use to only load (new) pdfs, and dont read any other files
pdf_directory = "C:\\path\\to\\import_files\\"

doc = opendoc(summary_file)
# delete old sheets once we run the script again, or we end up with a bunch of empty sheets
# for index, sheet in enumerate(doc.sheets):
#     if "Übersicht" not in sheet.name and "Beispielmonat" not in sheet.name:
#         del doc.sheets[sheet.name]

# read all files from given directory above
pdf_files = os.listdir(pdf_directory)

for pdf_file in pdf_files:  
    # extract year and month from filename to be read
    year, number = pdf_file.split("_")[1:3]
    month = number.split(".")[1][1:]
    # new_sheet = doc.sheets[1].copy(newname=str(month)+"-"+str(year))
    # doc.sheets += new_sheet

    pdf = PdfReader(pdf_directory+pdf_file)

    # predefined category definitions
    # "Others" category is not meant to be filled, if there is stuff in "other" that is not supposed to be there, put it into a fitting other category or create a new one
    # TODO finetune category definitions
    # go through all the remaining "others" and try to further sort them in if wanted
    categories = {
        "Other" : [],
        "Car": [],
        "Rent": [],
        "Gas (Car)": [],
        "Heating": [],
        "Streaming Services": [],
        "Mobile phone": [],
        "Water": [],
        "Power": [],
    }

    # Switch to summary sheet and update list of categories if there has been any additions
    sheet = doc.sheets["Übersicht"]
    sheet.append_rows(len(categories.keys()))
    for index, category in enumerate(categories.keys()):
        sheet["A"+str(8+index)].set_value(category)
        doc.save()

    # change to the correct sheet thats needed according to the pdf currently being handeled
    sheet = doc.sheets["Buchungsübersicht"]

    parsed_data = []
    for page in pdf.pages:
        # dont go though content of last page, since thats no bookings whatsoever, just informational text
        if len(pdf.pages)-1 == pdf.get_page_number(page):
            break
        # some initial string parsing, to have each booking in a single string within one element of parsed_content
        # with multiple lines though
        content = page.extract_text()
        
        # remove everything above the first actual booking on each page, after initial parsing
        parsed_content = re.split(r'\n[0-9]{2}\.[0-9]{2}\. ', content.format())[1:]

        for each in parsed_content:
            # cut off appendix after last actual booking, which only goes into details of fees, the very last booking should be total fees that month
            if "neuer Kontostand vom " in each:
                parsed_data.append(each.split("neuer Kontostand vom ")[0])
            # now there still is the "Übertrag auf Blatt" at the end of each page, we need to get rid of
            elif "Übertrag auf Blatt " in each:
                parsed_data.append(each.split("Übertrag auf Blatt ")[0])
            else:
                parsed_data.append(each)
    
    # Get row count before adding new rows, so we know where to start inserting data
    previous_rowcount = sheet.nrows()
    # Append sheet by same number of rows that we have bookings
    sheet.append_rows(len(parsed_data))

    # now there is exactly one booking string in each string of parsed_data
    for index, each in enumerate(parsed_data):

        # Loop trhough all the categories and their definitions and assign them, defaulting to "Others" if nothing else is found
        assinged_category = "Other"
        for category in categories:
            for pattern in categories[category]:
                if pattern in each:
                    assinged_category = category
        
        # split off all different information into seperate variables, then fix the description again, to have a normal string back
        each = each.split("\n")

        date = each[0].split(" ")[0]
        description = each[0].split(" ")[1:-2]
        description = " ".join(description)
        amount = each[0].split(" ")[-2]
        booking_type = each[0].split(" ")[-1] # - (S) or + (H)
        
        # some bookings only have 1 or 2 lines, not the maximum of 5 in total
        if len(each) > 1:
            receipient = each[1].strip()
        else:
            receipient = ""
        if len(each) == 3:
            detailed_description = each[2].strip()
        elif len(each) >= 4:
            detailed_description = each[2].strip() + " " + each[3].strip()
        else:
            detailed_description = ""

        # Mesh all the detailed inforamtion for abooking into one variable, without any whitespaces, to put that into the excel file
        summarized_description = description.strip()+" "+detailed_description.strip()

        if booking_type == "S":
            amount = str("-"+amount)
        elif booking_type == "H":
            amount = str("+"+amount)

        # get rid of german formatted 1000 cut symbol ".", since cell formatting will fix that for us anyways, and it interferes with the next replace
        amount = amount.replace(".","")
        # replace german formatted cent operator "," by the us-style formatting ".", doesnt matter since cell formatting will fix that for us again anyways
        amount = amount.replace(",",".")

        sheet["A"+str(previous_rowcount+index)].set_value(date) # Date
        sheet["B"+str(previous_rowcount+index)].set_value(month) # Month
        sheet["C"+str(previous_rowcount+index)].set_value(year) # Year
        sheet["D"+str(previous_rowcount+index)].set_value(assinged_category) # Category
        sheet["E"+str(previous_rowcount+index)].set_value(receipient) # Receipient
        sheet["F"+str(previous_rowcount+index)].set_value(booking_type) # Type
        sheet["G"+str(previous_rowcount+index)].set_value(summarized_description) # Description
        sheet["H"+str(previous_rowcount+index)].set_value(amount, currency='EUR') # Amount
        doc.save()
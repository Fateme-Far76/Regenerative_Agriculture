import PyPDF2
import re
import csv 


def pdf_obj():

    # Open the PDF file
    pdf_file = open('uploaded.pdf', 'rb')

    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)

    return pdf_reader

def str_cleaner(str):
    '''
    Cleans a string by removing unnessecary spaces and empty elements.

    :str is the input string to be cleaned.

    :Returns result_line which is a list of cleaned elements from the input string.
    
    '''
    result_line = str.strip().split('  ')

    # Remove empty elements from the list 
    while '' in result_line:
        result_line.remove( '')

    # Strip spaces from each element in the list    
    for index in range (len(result_line)):
        result_line[index] = result_line[index].strip()

    return result_line    


def cleaner(list):
    '''
    Cleans a list of strings by applying the 'str_cleaner' function to each element.

    :list is a list of strings to be cleaned.

    :Returns line_list which is a new list containing the cleaned strings.
        
    '''

    line_list = []

    for match in list:
        result_line = str_cleaner(match) # Clean each string using 'str_cleaner' function
        line_list.append(result_line) # Add the cleaned string to the new list    
        
    return line_list
 

def organizer(line):
    '''
     Inserts an empty element at the beginning of the given line list.
    
    :line is a list representing a line of data.
        
    :Returns line which is the modified line list with an empty element inserted at the beginning.
    
    '''

    line.insert(0,'')

    return line 
 
def pdf_processor():
    pdf_reader = pdf_obj()

    pattern1 = r'^[a-zA-Z]+'  
    pattern2 = r'\s+[a-zA-Z]+-[a-zA-Z]+\s?[[a-zA-Z]+]?\s+[a-zA-Z]{1,2}\s{1}[a-zA-Z]+/[a-zA-Z]+\s+<?>?[\s{1}]?\d+,?[\d+]?\s+\d+,?[\d+]?\s-\s+\d+,?[\d+]?'  
    pattern3 = r'\s+[a-zA-Z]+/[a-zA-Z]+-[a-zA-Z]+\s+\d+,?[[\d]+]?\s+\d+,?[[\d]+]?\s-\s+\d+,?[[\d]+]?' 
    pattern4 = r'\s+[a-zA-Z]+\s\([a-zA-Z]+\)\s+\d+,?[\d+]?\s+<?>?[\s{1}]?\d+,?[\d+]?\s?-?\s?[\d+]?,?[\d+]?' 
    pattern5 = r'\s+[a-zA-Z]{1,2}-?[a-zA-Z]+\s?\(?.+?\)?\s+%\s+\d+,?\d*\s*<?>?\s?\d*,?\d*\s?-?\s?\d*,?\d*' 
    pattern6 = r'\s+[a-zA-Z]{1,2}-?[a-zA-Z]+[[\s]+]?[a-zA-Z]*[[\s]+]?%\s+<?\s?\d+,?\s?[[\d]+]?\s+<?>?\s?\d+,?[[\d]+]?\s?-?\s?\d*,?\d*' 
    pattern7 = r'\s+\w+\s?[a-zA-Z]*\s+[a-zA-Z]+\s?[a-zA-Z]*/?[a-zA-Z]*\s+\d+,?\d*\s+\d+,?\d*\s?-?\s?\d+,?\d*' 
    pattern8 = r'\s+[a-zA-Z]+-?[a-zA-Z]*\s\([a-zA-Z]+\)\s+[a-zA-Z]+\+/[a-zA-Z]+\s+\d+,?\d*\s+>?<?\s?\d+,?\d*'
        
    # Open the output CSV file for writing
    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Iterate over the pages of the PDF reader
        for page in pdf_reader.pages:
            # Extract the text from the page
            page_text = page.extract_text() 

            # Search for the "Resultaat" keyword and extract the text following it
            if 'Resultaat' in page_text:
                lines = page_text.split('\n')

                # Find the header line and the number from which the results lines start
                for i, line in enumerate(lines):
                    if 'Resultaat' in line: 
                        header = line 
                        result_start = i + 1
                        break

                row = str_cleaner(header) # Clean the header line

                if len(row)<6: # 6 is the number of expected columns 
                    header = lines[result_start] # Use the line after 'Resultaat' as the header
                    row = str_cleaner(header) # Clean the new header

                if row[0]!='Resultaat':
                    row.insert(0,'Resultaat') # Insert 'Resultaat' at the beginning of the row
                row.insert(1,'Mineral') # Insert 'Mineral' as the second element    
                writer.writerow(row) # Write the header row to the CSV file   
                
                for line in lines[result_start:]: 
                    matches = re.findall(pattern1, line)
                    matches2 = re.findall(pattern2, line)
                    matches3 = re.findall(pattern3, line)
                    matches4 = re.findall(pattern4, line)
                    matches5 = re.findall(pattern5, line)
                    matches6 = re.findall(pattern6,line)  
                    matches7 = re.findall(pattern7,line)
                    matches8 = re.findall(pattern8,line) 

                    if matches:
                        writer.writerow(matches) # Write the matched line to the CSV file

                    if matches2:
                        result_line = cleaner(matches2) 
                        for line in result_line:
                            row = organizer(line) # Modify the line using the organizer function
                            writer.writerow(row) # Write the modified line to the CSV file 
    
                    # Similar processing for other matches
                    elif matches3:
                        result_line = cleaner(matches3)
                        for line in result_line:
                            row = organizer(line)
                            row.insert(2,'')      
                            writer.writerow(row)
                            
                    elif matches4:
                        result_line = cleaner(matches4)
                        for line in result_line:
                            row = organizer(line)
                            row.insert(2,'')      
                            writer.writerow(row)
    
                    elif matches5:
                        result_line = cleaner(matches5)
                        for line in result_line:
                            row = organizer(line)
                            if 'Organische stof' in row:
                                if len(row)>4: # this line must only be consist of 3 elements
                                    row = row[:4]   
                            writer.writerow(row)

                    elif matches6:
                        result_line = cleaner(matches6)
                        for line in result_line:
                            row = organizer(line)   
                            writer.writerow(row)

                    elif matches7:
                        result_line = cleaner(matches7)
                        for line in result_line:
                            row = organizer(line)   
                            writer.writerow(row)

                    elif matches8:
                        result_line = cleaner(matches8)
                        for line in result_line:
                            row = organizer(line)   
                            writer.writerow(row)       
                break # Stop processing the pages because the results are in 1 page                
                

 
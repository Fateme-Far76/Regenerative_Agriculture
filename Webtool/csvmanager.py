import csv 

def csvorganaizer(): 

    # Open the input CSV file 
    with open('output.csv', 'r') as input_file:
        # Open the output CSV file for writing
        with open('csv_output.csv', 'w', newline='') as output_file:
            # Create CSV reader and writer objects
            csv_reader = csv.reader(input_file)
            csv_writer = csv.writer(output_file)

            header = next(csv_reader)
            csv_writer.writerow(header) # Write the header row to the CSV file  
    
            previous_title = ''    
            # Iterate over each row in the input CSV file
            for row in csv_reader:  
                column1 = row[0]  

                # Filling the first element of each row if neccessary  
                if column1 != '':
                    previous_title = column1
                else:
                    row[0] = previous_title    

                # Write the modified row to the output CSV file
                csv_writer.writerow(row)
 
 
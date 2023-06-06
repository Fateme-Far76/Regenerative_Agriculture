import os
from flask import Flask, render_template, request, send_file
import PyPDF2
import csv
import re

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Get the uploaded file
    pdf_file = request.files['pdf_file']

    # Save the uploaded file
    pdf_path = 'uploaded.pdf'
    pdf_file.save(pdf_path)

    # Convert the PDF file to CSV
    csv_path = convert_pdf_to_csv(pdf_path)

    # Render the template with a success message
    return render_template('index.html', message='Conversion successful')

def organizer(header,matched_line):
    for match in matched_line:
        result_line = match.strip().split('  ') 
        while '' in result_line:
            result_line.remove( '')
        for index in range (len(result_line)):
            result_line[index] = result_line[index].strip() 
        try:
            result_line.insert(0, header[0])
        except:
            result_line.insert(0,'') 
    return result_line

def convert_pdf_to_csv(pdf_path):
    pattern1 = r'^[a-zA-Z]+'
    pattern2 = r'\s+[a-zA-Z]+-[a-zA-Z]+\s?[[a-zA-Z]+]?\s+[a-zA-Z]{1,2}\s{1}[a-zA-Z]+/[a-zA-Z]+\s+<?>?[\s{1}]?\d+,?[\d+]?\s+\d+,?[\d+]?\s-\s+\d+,?[\d+]?'
    pattern3 = r'\s+[a-zA-Z]+/[a-zA-Z]+-[a-zA-Z]+\s+\d+,?[\d+]?\s+\d+,?[\d+]?\s-\s+\d+,?[\d+]?'
    pattern4 = r'\s+[a-zA-Z]+\s\([a-zA-Z]+\)\s+\d+,?[\d+]?\s+<?>?[\s{1}]?\d+,?[\d+]?\s?-?\s?[\d+]?,?[\d+]?'
    pattern5 = r'\s+[a-zA-Z]{1,2}-?[a-zA-Z]+\s?\(?.+?\)?\s+%\s+\d+,?[\d+]?'
    titels = ['Resultaat', 'Chemisch', 'Fysisch', 'Biologisch']

    # Open the PDF file
    pdf_file = open(pdf_path, 'rb')

    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)

    # Convert PDF to CSV and return the CSV file path
    csv_path = 'output.csv'
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if 'Resultaat' in page_text:
                lines = page_text.split('\n')
                for i, line in enumerate(lines):
                    if 'Resultaat' in line:
                        writer.writerow(['Resultaat'])
                        header = line
                        result_start = i + 1
                        break
                for line in lines[result_start:]:
                    matches = re.findall(pattern1, line)
                    matches2 = re.findall(pattern2, line)
                    matches3 = re.findall(pattern3, line)
                    matches4 = re.findall(pattern4, line)
                    matches5 = re.findall(pattern5, line)

                    if line.strip() in titels:
                        writer.writerow([line.strip()])

                    if matches2:
                        result_line = organizer(matches, matches2)
                        writer.writerow(result_line)

                    elif matches3:
                        result_line = organizer(matches, matches3)
                        result_line.insert(2, '')
                        writer.writerow(result_line)

                    elif matches4:
                        result_line = organizer(matches, matches4)
                        result_line.insert(2, '')
                        writer.writerow(result_line)

                    elif matches5:
                        result_line = organizer(matches, matches5)
                        writer.writerow(result_line)

    return csv_path


@app.route('/download')
def download():
    # Set the file path of the generated CSV
    csv_path = 'output.csv'

    # Send the CSV file as a download attachment
    return send_file(csv_path, as_attachment=True, attachment_filename='output.csv')


if __name__ == '__main__':
    app.run()


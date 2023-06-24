from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import random
import seaborn as sns 
from csvparser import csvparser, organic_compund, pH
from remover import csvremover
from csvmanager import csvorganaizer
from pdfparser import pdf_processor 

app = Flask(__name__)

# Disable caching
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

 
@app.route('/soil-data', methods=['GET', 'POST'])
def soil_data():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            return "No file uploaded"
        
        file = request.files['file']
        
        # Check if a file was selected
        if file.filename == '':
            return "No file selected"
        
        # Save the uploaded file
        file.save('uploaded.pdf')

        pdf_processor() 
        csvorganaizer()  
        csv_df = csvparser()
        organic_compund(csv_df)
        pH(csv_df)
        csvremover('output.csv')
        csvremover('csv_output.csv')

        # Render the 'second_page.html' template with the plots
        return render_template('analysis.html', plots=True, active_tab='soil-data')
    return render_template('analysis.html') 

if __name__ == '__main__':
    app.run()

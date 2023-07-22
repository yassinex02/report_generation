# Flask Report Generator

This is a simple Flask web application for generating customized PDF reports. The application allows users to select various filtering options such as product, frequency, day, start date, end date, and month. Based on the selected filters, the application generates 6 plots and incorporates them into a PDF report template that created from scratch on Canva .

## Features

- User-friendly web interface for selecting filters.
- Automatic generation of plots based on the selected filters.
- Customization of the PDF report, including date, frequency, author's name, comments.
- Downloadable PDF report with the generated plots and information.

## Requirements

- Python 3.x
- Flask
- Pandas
- PyPDF2
- ReportLab

## Usage
Open your web browser and go to http://localhost:5002 to access the web interface after running the app.py file
Usage
Visit the homepage (/) to access the filtering form.
Select the desired filters for the report (product, frequency, date, etc.).
Click on the "Generate Report" button to generate the PDF report.
The PDF report will be displayed, and you can click the "Download PDF" button to save it.
After downloading the pdf report , make sure to clear the cache afterwards so that the next time you try downloading a report with different filters , the right pdf will be downloaded

from flask import Flask, render_template, request, send_file, Response
from customise_template import customise
from functions import save_filters_to_json, filtering

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def result():
    product = request.form['product']
    frequency = request.form['frequency']

    if frequency == 'daily':
        selected_day = request.form['selected_day']
        save_filters_to_json(product, frequency, selected_day=selected_day)
    elif frequency == 'weekly':
        selected_start_date = request.form['selected_start_date']
        selected_end_date = request.form['selected_end_date']
        save_filters_to_json(product, frequency, selected_start_date=selected_start_date,
                             selected_end_date=selected_end_date)
    elif frequency == 'monthly':
        selected_month = request.form['selected_month']
        save_filters_to_json(product, frequency, selected_month=selected_month)
    else:
        save_filters_to_json(product, frequency)
    filtering()
    pdf_filename = customise()

    with open(pdf_filename, 'rb') as file:
        pdf_content = file.read()

    response = Response(pdf_content, content_type='application/pdf')
    response.headers['Content-Disposition'] = f'inline; filename={pdf_filename}'

    return response


if __name__ == '__main__':
    app.run(debug=True, port=5002)

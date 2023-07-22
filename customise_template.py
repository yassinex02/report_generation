

import io
import json
import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from functions import small_caps_to_title


def get_latest_trial_folder(plot_directory):
    all_folders = [f for f in os.listdir(plot_directory) if os.path.isdir(os.path.join(plot_directory, f))]
    trial_folders = [f for f in all_folders if f.startswith("trial_") and f[6:].isdigit()]
    sorted_trial_folders = sorted(trial_folders, key=lambda x: int(x[6:]), reverse=True)
    if sorted_trial_folders:
        return os.path.join(plot_directory, sorted_trial_folders[0])
    else:
        return None

def customise():
    with open('filters.json', 'r') as file:
        filters = json.load(file)

    date = '2022-07-21'
    name = 'Taha Yassine Moumni'

    # storing the filters in different variables
    product_selected = filters['product']
    frequency_selected = small_caps_to_title(filters['frequency'])
    day_selected = filters["selected_day"]
    start_week = filters["selected_start_date"]
    end_week = filters["selected_end_date"]
    month_selected = small_caps_to_title(filters["selected_month"])

    # Reading the pre-defined template
    my_temp = PdfReader(open("template.pdf", "rb"))

    # First page
    first_page = my_temp.pages[0]
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    ## Date of today
    font_name = "Times-Italic"
    font_size = 25
    can.setFont(font_name, font_size)
    can.drawString(230, 400, date)

    ## Frequency
    font_name = "Times-Roman"
    font_size = 25
    can.setFont(font_name, font_size)
    can.drawString(230, 450, frequency_selected + ' Report')

    ## Name of the author :
    font_name = "Times-Roman"
    font_size = 15
    can.setFont(font_name, font_size)
    can.drawString(420, 50, name)

    can.save()
    packet.seek(0)
    new_pdf = PdfReader(packet)
    first_page.merge_page(new_pdf.pages[0])

    # Second page
    second_page = my_temp.pages[1]
    packet2 = io.BytesIO()
    can2 = canvas.Canvas(packet2, pagesize=letter)

    # KPI
    font_name = "Times-Roman"
    font_size = 16
    can2.setFont(font_name, font_size)
    can2.drawString(120, 704, 'Process')  # Corrected the coordinates for "Process" text

    # Frequency
    font_name = "Times-Roman"
    font_size = 16
    can2.setFont(font_name, font_size)
    can2.drawString(460, 704, frequency_selected)  # Corrected the coordinates for frequency text

    # Qualite / Product:
    font_name = "Times-Roman"
    font_size = 16
    can2.setFont(font_name, font_size)
    can2.drawString(307, 704, product_selected)

    # Date:
    if day_selected:
        font_name = "Times-Roman"
        font_size = 16
        can2.setFont(font_name, font_size)
        can2.drawString(296, 656, day_selected)  # Corrected the coordinates for the date text
    elif month_selected:
        font_name = "Times-Roman"
        font_size = 16
        can2.setFont(font_name, font_size)
        can2.drawString(296, 656, month_selected)
    elif start_week and end_week:
        font_name = "Times-Roman"
        font_size = 16
        can2.setFont(font_name, font_size)
        can2.drawString(296, 640, start_week)
        font_name = "Times-Roman"
        font_size = 16
        can2.setFont(font_name, font_size)
        can2.drawString(296, 680, end_week)
    else:
        font_name = "Times-Roman"
        font_size = 16
        can2.setFont(font_name, font_size)
        can2.drawString(296, 656, 'Year 2023')

    # Rendement de poids labo :
    font_name = "Times-Roman"
    font_size = 16
    can2.setFont(font_name, font_size)
    can2.drawString(238, 562, '70%')

    # Cadence moyenne :
    font_name = "Times-Roman"
    font_size = 16
    can2.setFont(font_name, font_size)
    can2.drawString(550, 562, '50%')

    # Taux d'echontillonage ;
    font_name = "Times-Roman"
    font_size = 16
    can2.setFont(font_name, font_size)
    can2.drawString(185, 492, '90%')

    # Rendement de poids :
    font_name = "Times-Roman"
    font_size = 16
    can2.setFont(font_name, font_size)
    can2.drawString(500, 503, '20%')

    plot_directory = 'plots'
    latest_trial_folder = get_latest_trial_folder(plot_directory)

    if latest_trial_folder:
        # Update the plot_files to use plots from the latest trial folder
        plot_files = [f for f in os.listdir(latest_trial_folder) if f.lower().endswith('.png')]
    else:
        pass

    images_to_resize = [
        {'path': os.path.join(latest_trial_folder, plot_files[0]), 'x': 5, 'y': 200, 'width': 280, 'height': 175},
        {'path': os.path.join(latest_trial_folder, plot_files[1]), 'x': 310, 'y': 200, 'width': 280, 'height': 175}
    ]

    for i, img_data in enumerate(images_to_resize):
        image_path = img_data['path']
        x_coordinate = img_data['x']
        y_coordinate = img_data['y']
        image_width = img_data['width']
        image_height = img_data['height']

        image = ImageReader(image_path)
        original_width, original_height = image.getSize()
        aspect_ratio = original_width / original_height
        new_width = image_width
        new_height = int(new_width / aspect_ratio)
        can2.drawImage(image, x_coordinate, y_coordinate, width=new_width, height=new_height)

    can2.save()
    packet2.seek(0)
    new_pdf2 = PdfReader(packet2)
    second_page.merge_page(new_pdf2.pages[0])

    # Selecting third page
    third_page = my_temp.pages[2]
    packet3 = io.BytesIO()
    can3 = canvas.Canvas(packet3, pagesize=letter)

    remaining_plot_files = plot_files[2:]
    image_width = 280
    image_height = 225
    x_coordinate = 5
    y_coordinate = 200
    gap = 10
    images_to_resize = []

    for i, img_path in enumerate(remaining_plot_files):
        x = x_coordinate + ((image_width + gap) * (i % 2))
        y = y_coordinate + (image_height + gap) * (i // 2)
        images_to_resize.append({'path': os.path.join(latest_trial_folder, img_path), 'x': x, 'y': y, 'width': image_width,
                                 'height': image_height})



    for img_data in images_to_resize:
        image_path = img_data['path']
        x_coordinate = img_data['x']
        y_coordinate = img_data['y']
        image_width = img_data['width']
        image_height = img_data['height']

        image = ImageReader(image_path)
        original_width, original_height = image.getSize()
        aspect_ratio = original_width / original_height

        if aspect_ratio > 1:
            # Landscape-oriented image
            new_width = image_width
            new_height = int(new_width / aspect_ratio)
        else:
            # Portrait-oriented image
            new_height = image_height
            new_width = int(new_height * aspect_ratio)

        can3.drawImage(image, x_coordinate, y_coordinate, width=new_width, height=new_height)

    can3.save()
    packet3.seek(0)
    new_pdf3 = PdfReader(packet3)
    third_page.merge_page(new_pdf3.pages[0])

    # Selecting fourth page
    fourth_page = my_temp.pages[3]
    packet4 = io.BytesIO()
    can4 = canvas.Canvas(packet4, pagesize=letter)


    font_name = "Helvetica-Bold"
    font_size = 20
    can4.setFont(font_name, font_size)
    can4.drawString(100, 400, "Hello , this the comment of the report")
    can4.save()
    packet4.seek(0)
    new_pdf4 = PdfReader(packet4)
    fourth_page.merge_page(new_pdf4.pages[0])

    output = PdfWriter()
    output.add_page(first_page)
    output.add_page(second_page)
    output.add_page(third_page)
    output.add_page(fourth_page)

    for page in my_temp.pages[4:]:
        output.add_page(page)

    with open("final_report.pdf", "wb") as output_stream:
        output.write(output_stream)

    return "final_report.pdf"




from flask import Flask
import matplotlib.pyplot as plt
import os

app = Flask(__name__)


def get_trial_number():
    if not os.path.exists('trial_count.txt'):
        with open('trial_count.txt', 'w') as file:
            file.write('0')
        return 0

    with open('trial_count.txt', 'r') as file:
        trial_number = int(file.read())
    return trial_number


def update_trial_number(trial_number):
    with open('trial_count.txt', 'w') as file:
        file.write(str(trial_number + 1))
def generate_plots(df):
    if df.empty:
        print("No data recorded in this period.")
        return

    trial_number = get_trial_number()
    plot = 'plots'
    if not os.path.exists(plot):
        os.makedirs(plot)
    plot_directory = os.path.join('plots', f'trial_{trial_number}')
    if not os.path.exists(plot_directory):
        os.makedirs(plot_directory)


    # List of columns to plot
    columns_to_plot = ['Teneur PBL', 'Humidite', 'Chlore']

    for col in columns_to_plot:
        plt.figure(figsize=(8, 4))
        plt.plot(df['Date'], df[col])
        plt.xlabel('Date')
        plt.ylabel(col)
        plt.title(f'Line Plot of {col}')

        plot_filename = os.path.join(plot_directory, f'{col}_line.png')
        plt.savefig(plot_filename, format='png', bbox_inches='tight')
        plt.close()

        plt.figure(figsize=(8, 4))
        plt.bar(df['Date'], df[col])
        plt.xlabel('Date')
        plt.ylabel(col)
        plt.title(f'Bar Plot of {col}')

        plot_filename = os.path.join(plot_directory, f'{col}_bar.png')
        plt.savefig(plot_filename, format='png', bbox_inches='tight')
        plt.close()

    update_trial_number(trial_number)

    return trial_number

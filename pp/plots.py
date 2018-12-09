import csv
from os import listdir
from os.path import isfile
from re import search

import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.io as pio


def records_file_to_image(records_file_path, output_file_path):
    rows = pd.read_csv(records_file_path, header=None)
    trace_1 = go.Scatter(y=rows[0],
                       name='Herbivores')
    trace_2 = go.Scatter(y=rows[1],
                       name='Predators')
    trace_3 = go.Scatter(y=rows[2],
                       name='Plants')
    layout = go.Layout(title='Predator-Prey Model Populations',
                       plot_bgcolor='rgb(230, 230,230)',
                       showlegend=True)
    fig = go.Figure(data=[trace_1, trace_2, trace_3], layout=layout)

    pio.write_image(fig, output_file_path)


def records_to_images():
    found_records = [
        found.group(0) for found in
        [search('recorded_\d+.csv', file) for file in listdir('.')]
        if found
    ]
    missing_images = [
        (record, record[:-4] + '_image.png')
        for record in found_records
        if not isfile(record[:-4] + '_image.png')
    ]
    for record_file_path, output_file_path in missing_images:
        records_file_to_image(record_file_path, output_file_path)


if __name__ == "__main__":
    records_to_images()

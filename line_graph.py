#!/usr/bin/env python

import pygal

def twoline(file_name, title, line1, line1_label, line2, line2_label, x_labels):

    '''
    Line1 is a list of dat points

    Line2 is a list of data points

    x_labels are labels that correspond the data points in line1 and line2

    '''

    line_chart = pygal.Line(include_x_axis=True)

    line_chart.title = title
    line_chart.x_labels = x_labels
    line_chart.add(line1_label, line1)
    line_chart.add(line2_label, line2)

    line_chart.render_to_file(file_name)

    return True
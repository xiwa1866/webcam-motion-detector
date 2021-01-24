# this file is to load the csv file to bokeh graph on a web page
from motion_detector import df
from bokeh.plotting import figure, show, output_file

# initializing figure variable
p=figure(x_axis_type='datetime', height=100, width=500, title='Motion Graph')
p.yaxis.minor_tick_line_color=None
p.yaxis[0].ticker.desired_num_ticks=1
q=p.quad(left=df["Start"],right=df["End"],bottom=0,top=1, color='green')

# set output file and show the figure object on a web page
output_file("Graph.html")
show(p)


# this file is to load the csv file to bokeh graph on a web page
from motion_detector import df
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

#convert the times to str
df["Start_string"]=df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_string"]=df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")
# initializing figure variable
p=figure(x_axis_type='datetime', height=100, width=500, title='Motion Graph')
p.yaxis.minor_tick_line_color=None
p.yaxis[0].ticker.desired_num_ticks=1

hover=HoverTool(tooltips=[("Start","@Start_string"),("End","@End_string")])
p.add_tools(hover)

# create rectangles
q=p.quad(left="Start",right="End",bottom=0,top=1, color='green', source=ColumnDataSource(df))

# set output file and show the figure object on a web page
output_file("Graph.html")
show(p)



import numpy as np
import plotly
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
from GPUs import gpu_info
from multiprocessing import Process

# (*) Import module keep track and format current time
import datetime
import time

# todo: be able to interactivy select each satoshi.
# todo: see all gpus of a single satoshi plotted in the same graph on a seperat line
# todo: different color lines for each value. i.e temperature, etc. legend for each value
# todo: make hufter prove. make it startup on every satoshi automaticly.
# todo: extra bonus, overclock button,  give a warning when a gpu is not running.

def stream_ids():
    """
    :return: list of 'stream_ids'
    """
    plotly.tools.set_credentials_file(username='sehsucht', api_key='hnGBsUh06NKbqBMle8Mb', stream_ids=['enedfilzr5', 'd4krs93e0q'])
    stream_ids = tls.get_credentials_file()['stream_ids']

    return stream_ids


def plot():
    """
    create a figure plot
    """
    stream_id = stream_ids()
    stream_1 = dict(token=stream_id[0], maxpoints=1000)
    stream_2 = dict(token=stream_id[1], maxpoints=1000)

    trace1 = go.Scatter(
        x=[],
        y=[],
        mode='lines+markers',
        stream=stream_1)         # 1 per trace

    trace2 = go.Scatter(
        x=[],
        y=[],
        mode='lines+markers',
        stream=stream_2)  # 1 per trace

    layout = go.Layout(title='Time Series')

    fig = go.Figure(data=[trace1], layout=layout)
    unique_url = py.plot(fig, filename='render')
    # We will provide the stream link object the same token that's associated with the trace we wish to stream to
    #
    # # open the url
    # s1 = py.Stream(stream_id)
    #
    # connect 1 stream for 1 trace
    plot1 = connecter(stream_id[0])
    plot1.open_con()

    plot2 = connecter(stream_id[1])
    plot2.open_con()
    while True:
        plot1.write('temp')
        plot2.write('load')
    # raise ValueError('made it')
    # plot2 = connecter(stream_id[1], memory() )
    # plot2.write()


class connecter:

    def __init__(self, stream_id):
        self.s = py.Stream(stream_id)
        # self.y = y_axis


    def write(self, display):
        # Send data to your plot
        x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        if display == 'temp':
            y = temperature()
        elif display == 'load':
            y = memory()
        self.s.write(dict(x=x, y=y))
        #     Write numbers to stream to append current data on plot,
        #     write lists to overwrite existing data on plot
        time.sleep(5)

    def open_con(self):
        self.s.open()


def temperature():
    gpus = gpu_info()
    for gpu in gpus:
        percent = gpu.temperature
        return temp


def memory():
    gpus = gpu_info()
    for gpu in gpus:
        percent = gpu.memoryUsed / gpu.memoryTotal
        return percent

plot()


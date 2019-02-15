import numpy as np
import plotly
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
from GPUs import gpu_info


# todo: be able to interactivy select each satoshi.
# todo: see all gpus of a single satoshi plotted in the same graph on a seperat line
# todo: different color lines for each value. i.e temperature, etc. legend for each value
# todo: make hufter prove. make it startup on every satoshi automaticly.
# todo: extra bonus, overclock button,  give a warning when a gpu is not running.

def stream_ids():
    """
    :return: list of 'stream_ids'
    """
    plotly.tools.set_credentials_file(username='sehsucht', api_key='hnGBsUh06NKbqBMle8Mb', stream_ids=['enedfilzr5'])
    stream_ids = tls.get_credentials_file()['stream_ids']

    return stream_ids


def plot():
    """
    create a figure plot
    """
    stream_id = stream_ids()[0]
    stream_1 = dict(token=stream_id, maxpoints=1000)

    trace = go.Scatter(
        x=[],
        y=[],
        mode='lines+markers',
        stream=stream_1)         # 1 per trace

    layout = go.Layout(title='Time Series')

    fig = go.Figure(data=[trace], layout=layout)
    unique_url = py.plot(fig, filename='render')
    # We will provide the stream link object the same token that's associated with the trace we wish to stream to

    s = py.Stream(stream_id)

    return s


def connect():
    s = plot()
    # We then open a connection
    s.open()

    # (*) Import module keep track and format current time
    import datetime
    import time

    i = 0    # a counter
    k = 5    # some shape parameter

    # Delay start of stream by 5 sec (time to switch tabs)
    time.sleep(5)

    while True:

        # Current time on x-axis, random numbers on y-axis
        x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        y = temperature()

        # Send data to your plot
        s.write(dict(x=x, y=y))
        #     Write numbers to stream to append current data on plot,
        #     write lists to overwrite existing data on plot

        time.sleep(3)  # plot a point every second
    # Close the stream when done plotting
    s.close()


def temperature():
    gpus = gpu_info()
    for gpu in gpus:
        return gpu.load

connect()


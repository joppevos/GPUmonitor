import numpy as np
import plotly
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
from GPUs import gpu_info
from multiprocessing import Process
from plotly import tools
# (*) Import module keep track and format current time
import datetime
import time
import numpy as np


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

    fig = tools.make_subplots(rows=1, cols=2, subplot_titles=('Plot 1', 'Plot 2'))
    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 2)

    fig['layout'].update(height=800, width=1600, title='Satoshi3') # todo get name of slave socket.gethostname()

    fig['layout']['xaxis1'].update(title='Memory')
    fig['layout']['xaxis2'].update(title='Average temperature', range=[10, 50])

    unique_url = py.plot(fig, filename='render')
    write_trace()

def write_trace():

    stream_id = ['enedfilzr5', 'd4krs93e0q']
    s1 = py.Stream(stream_id[0])
    s1.open()

    s2 = py.Stream(stream_id[1])
    s2.open()
    while True:
        x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        y1 = memory()
        s1.write(dict(x=x, y=y1))

        y2 = temperature()
        y2 = int(y2)
        s2.write(dict(x=x, y=y2))

        time.sleep(5)


def temperature():
    """ returns average temperature of the GPUs"""
    gpus = gpu_info()
    average = []
    for gpu in gpus:
        temp = gpu.temperature
        if temp >= 10:
            print(f'Temperature of {gpu.name} is {gpu.temperature} ')
        average.append(gpu.temperature)

    temp_mean = np.array(average).mean()
    return temp_mean


def memory():
    gpus = gpu_info()
    for gpu in gpus:
        percent = gpu.memoryUsed / gpu.memoryTotal
        return percent
# write_trace()
plot()


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
    plotly.tools.set_credentials_file(username='sehsucht', api_key='hnGBsUh06NKbqBMle8Mb', stream_ids=['enedfilzr5', 'd4krs93e0q', 'f8thwyqzkq'])
    stream_ids = tls.get_credentials_file()['stream_ids']

    return stream_ids


def plot():
    """
    create a figure plot
    """
    stream_id = stream_ids()
    stream_1 = dict(token=stream_id[0], maxpoints=1000)
    stream_2 = dict(token=stream_id[1], maxpoints=1000)
    stream_3 = dict(token=stream_id[2], maxpoints=1000)

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

    trace3 = go.Scatter(
        x=[],
        y=[],
        mode='lines+markers',
        stream=stream_3)  # 1 per trace

    fig = tools.make_subplots(rows=2, cols=2)
    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 2)
    fig.append_trace(trace3, 2, 1)

    fig['layout'].update(height=800, width=800, title=f'{socket.gethostname()}') # todo get name of slave socket.gethostname()

    fig['layout']['xaxis1'].update(title='Memory')
    fig['layout']['xaxis2'].update(title='Average temperature')
    fig['layout']['xaxis3'].update(title='Average usageload')

    unique_url = py.plot(fig, filename='render')
    stream_id(stream_id)


def stream(stream_id):
    s1 = py.Stream(stream_id[0])
    s1.open()

    s2 = py.Stream(stream_id[1])
    s2.open()

    s3 = py.Stream(stream_id[2])
    s3.open()
    while True:
        x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        y1 = memory()
        s1.write(dict(x=x, y=y1))

        y2 = get('temp')
        s2.write(dict(x=x, y=y2))

        y3 = load()
        s3.write(dict(x=x, y=y3))

        time.sleep(5)


def temperature(input):
    """ returns average temperature of the GPUs"""
    gpus = gpu_info()
    average = []
    for gpu in gpus:
        temp = gpu.temperature
        if temp >= 80:
            # send message email
            print(f'Temperature of {gpu.name} is {gpu.temperature} ')
        average.append(gpu.temperature)
    temp_mean = np.array([average]).mean()
    return temp_mean


def memory():
    gpus = gpu_info()
    for gpu in gpus:
        percent = (gpu.memoryUsed / gpu.memoryTotal)*100
        return percent


def load():
    """ returns average load of the GPUs"""
    gpus = gpu_info()
    average = []
    for gpu in gpus:
        average.append(gpu.load)*100
    load_mean = np.array([average]).mean()
    return load_mean



plot()


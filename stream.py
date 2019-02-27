import numpy as np
import plotly
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
from gpus.GPUs import gpu_info
from multiprocessing import Process
from plotly import tools
import datetime
import time
import numpy as np
import socket

# todo: overclock button,  give a warning when a gpu is not running


def read_keys():
    api = ''
    tokens = []
    counter = 0
    username = ''
    with open('keys.txt', 'r') as f:
        for line in f:
            for word in line.split():
                if counter == 0:
                    username = word
                    counter += 1
                elif len(word) >= 12:
                    print(word)
                    api = word
                else:
                    tokens.append(word)
    return api, tokens, username


def stream_ids():
    """
    :return: list of 'stream_ids'
    """
    api, tokens, username = read_keys()
    print(tokens)
    plotly.tools.set_credentials_file(username=username, api_key=api, stream_ids=tokens)
    stream_ids = tls.get_credentials_file()['stream_ids']
    return stream_ids


def plot():
    """
    create a figure plot
    """
    name = [gpu.name for gpu in gpu_info()]
    driver = [gpu.driver for gpu in gpu_info()][0]
    id = [gpu.id for gpu in gpu_info()][0]

    stream_id = stream_ids()
    stream_1 = dict(token=stream_id[0], maxpoints=1000)
    stream_2 = dict(token=stream_id[1], maxpoints=1000)
    stream_3 = dict(token=stream_id[2], maxpoints=1000)

    trace1 = go.Scatter(
        x=[],
        y=[],
        mode='lines+markers',
        stream=stream_1,
        name=f'{(len(name))}X {name[0]}')       # 1 per trace

    trace2 = go.Scatter(
        x=[],
        y=[],
        mode='lines+markers',
        stream=stream_2,
        name='') # 1 per trace

    trace3 = go.Scatter(
        x=[],
        y=[],
        mode='lines+markers',
        stream=stream_3,
        name='')  # 1 per trace

    fig = tools.make_subplots(rows=2, cols=2)
    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 2)
    fig.append_trace(trace3, 2, 1)

    fig['layout'].update(height=800, width=800, title=f'{socket.gethostname()}')
    fig['layout']['xaxis1'].update(title='Memory')
    fig['layout']['xaxis2'].update(title='Temperature')
    fig['layout']['xaxis3'].update(title='Usage-load')

    unique_url = py.plot(fig, filename='render')
    stream()


def stream():
    stream_id = ['enedfilzr5', 'd4krs93e0q', 'f8thwyqzkq']
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

        y2 = temperature()
        s2.write(dict(x=x, y=y2))

        y3 = load()
        s3.write(dict(x=x, y=y3))

        time.sleep(3)


def temperature():
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
        percent = gpu.load*100
        average.append(percent)
    load_mean = np.array([average]).mean()
    return load_mean


plot()


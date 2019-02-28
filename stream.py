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
import time
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
                    api = word
                else:
                    tokens.append(word)
    return api, tokens, username


def stream_ids():
    """
    :return: list of 'stream_ids'
    """
    api, tokens, username = read_keys()
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
    num_trace = (len(gpu_info())+ 1 * 3) # range of traces needed for num gpu
    fig = tools.make_subplots(rows=2, cols=2)

    streams = []
    gpumap = {}

    for i in stream_id:
        temp = dict(token=i, maxpoints=1000)
        streams.append(temp)

    for gpu in gpu_info():
        #
        t = []
        for i in range(0, len(streams), 3):
            if i+2<len(streams):
                s1 = streams[i]
                s2 = streams[i+1]
                s3 = streams[i+2]
                t =[s1, s2, s3]
        gpumap[gpu.serial] = t

    for gpu in gpu_info():
        listofstreams = list(gpumap.get(gpu.serial))
        for i in range(len(listofstreams)):
            mem = go.Scatter(x=[], y=[], mode='lines+markers', stream=listofstreams[0], name='')  # 1 per trace
            temp = go.Scatter(x=[], y=[], mode='lines+markers', stream=listofstreams[1], name='')  # 1 per trace
            load = go.Scatter(x=[], y=[], mode='lines+markers', stream=listofstreams[2], name='')  # 1 per trace

            fig.append_trace(mem, 1, 1)
            fig.append_trace(temp, 1, 2)
            fig.append_trace(load, 2, 1)

    fig['layout'].update(height=800, width=800, title=f'{socket.gethostname()}')
    fig['layout']['xaxis1'].update(title='Memory')
    fig['layout']['xaxis2'].update(title='Temperature')
    fig['layout']['xaxis3'].update(title='Usage-load')

    # append individual gpus
    unique_url = py.plot(fig, filename='render')
    open_streams(stream_id, gpumap)


def open_streams(stream_id, gpumap):
    for s in stream_id:
        st = py.Stream(s)
        st.open()

    streamdict = {}
    start = time.time()
    for gpu in gpu_info():
        listofstreams = list(gpumap.get(gpu.serial))
        for i in range(len(listofstreams)):
            st0 = py.Stream(listofstreams[0]['token'])
            st1 = py.Stream(listofstreams[1]['token'])
            st2 = py.Stream(listofstreams[2]['token'])

            st0.open()
            st1.open()
            st2.open()

            streamdict[gpu.serial] = [st0, st1, st2]
    a = time.time()-start
    print(a)
    print(streamdict)

    while True:
        x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        for gpu in gpu_info():
            streamdict[gpu.serial][0].write(dict(x=x, y=memory(gpu.serial)))
            streamdict[gpu.serial][1].write(dict(x=x, y=temperature(gpu.serial)))
            streamdict[gpu.serial][2].write(dict(x=x, y=load(gpu.serial)))
            # st0.write(dict(x=x, y=memory(gpu.serial)))
            # st1.write(dict(x=x, y=temperature(gpu.serial)))
            # st2.write(dict(x=x, y=load(gpu.serial)))

        time.sleep(3)


def temperature(ids):
    """ returns average temperature of the GPUs"""
    gpus = gpu_info()
    result = {}
    for g in gpus:
        if g.serial == ids:
            result = g
            break
    print(result.temperature)
    return result.temperature


def memory(ids):
    gpus = gpu_info()
    result = {}
    for g in gpus:
        if g.serial == ids:
            result = g
            break
    percent = (result.memoryUsed / result.memoryTotal)*100
    return percent


def load(ids):
    """ returns average load of the GPUs"""
    gpus = gpu_info()
    result = {}
    for g in gpus:
        if g.serial == ids:
            result = g
            break
    return result.load


plot()


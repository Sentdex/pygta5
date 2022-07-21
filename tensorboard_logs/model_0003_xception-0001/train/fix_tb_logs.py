from turtle import color
import tensorflow as tf
from tensorflow.core.util.event_pb2 import Event
import struct
import os
import matplotlib.pyplot as plt
import mplcyberpunk
import numpy as np
import time

def moving_average(x, w):
    c = np.convolve(x, np.ones(w), 'valid') / w
    x = np.concatenate((x, np.array([c[-1]]*w)))
    c = np.convolve(x, np.ones(w), 'valid') / w

    return c

def smooth(scalars, weight):  # Weight between 0 and 1
    last = scalars[0]  # First value in the plot (first timestep)
    smoothed = list()
    for point in scalars:
        smoothed_val = last * weight + (1 - weight) * point  # Calculate smoothed value
        smoothed.append(smoothed_val)                        # Save it
        last = smoothed_val                                  # Anchor the last smoothed value

    return smoothed

files = os.listdir('.')
files.sort()
files = [file for file in files if 'tfevents' in file]

colors = [
    '#FE53BB',  # pink
    '#F5D300',  # yellow
    '#08F7FE',  # teal/cyan
    '#00ff41',  # matrix green
]
colors2 = [
    '#700143',  # pink
    '#706100',  # yellow
    '#016c70',  # teal/cyan
    '#00701c',  # matrix green
]

t1 = time.time()
loss_names = []
loss_metrics = {}
for rec in tf.data.TFRecordDataset([files]):
    ev = Event()
    ev.MergeFromString(rec.numpy())
    #print(ev)
    if ev.summary:
        #print(ev.step)
        for v in ev.summary.value:
            if 'loss' in v.tag:
                decoded = struct.unpack('f', v.tensor.tensor_content)[0]
                if v.tag not in loss_names:
                    loss_names.append(v.tag)
                    loss_metrics[v.tag] = []
                if len(loss_metrics[v.tag]) < 10:
                    loss_metrics[v.tag].append(decoded)
print(loss_names)


t2 = time.time()

print(t2-t1)
#exit()
with plt.style.context("cyberpunk"):
    #plt.style.use("cyberpunk")
    for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
        plt.rcParams[param] = '#000000'

    fig = plt.figure(2, figsize=(8*2, 7.5))
    plt.rcParams.update({'font.size': 30})
    fig.subplots_adjust(bottom=0.1, left=0.1, right=0.95, top=0.95)
    ax = fig.gca()
    #ax.get_xticklabels().set_fontsize(16)
    #ax.get_yticklabels().set_fontsize(16)


    t3 = time.time()
    moving_average_values = {}
    maxes = []
    moving_average_value = len(loss_metrics['loss']) // 1000
    print(moving_average_value)
    for loss_name, loss_value in loss_metrics.items():
        moving_average_values[loss_name] = moving_average(loss_value, 40 + moving_average_value)
        #moving_average_values[loss_name] = np.array(smooth(loss_value, 0.999))
        maxes.append(moving_average_values[loss_name].max())
        #plt.plot(loss_value, label=loss_name + '_background', color=colors[loss_names.index(loss_name)], alpha=0.1, ax=ax)
    max_value = max(maxes)

    t4 = time.time()

    axs = []
    plots = []
    for loss_name, loss_values in moving_average_values.items():
        plot = plt.plot(loss_values, label=loss_name, color=colors[loss_names.index(loss_name)])
        print(plot)
        #axs.append(plot)
        plots.append(plot[0])
        mplcyberpunk.make_lines_glow(lines=plot[0])
    leg = plt.legend(plots, loss_names, frameon=True, prop={'size': 36})
    leg.get_frame().set_edgecolor('#00ff41')

    '''
    moving_average_values = {}
    for loss_name, loss_value in loss_metrics.items():
        moving_average_values[loss_name] = np.array(moving_average(loss_value, 2000))
    for loss_name, loss_values in moving_average_values.items():
        plot = plt.plot(loss_values, label=loss_name + '_thinner', color=colors[loss_names.index(loss_name)])
    '''

    #mplcyberpunk.make_lines_glow()

    #plt.gcf().set_facecolor('#000000')

    # plt set max on y axis
    #ax.ylim(0, max_value * 1.1)
    index = len(moving_average_values['loss']) // 7
    value_at_point = moving_average_values['loss'][index]
    ax.axis(ymin=0, ymax=value_at_point * 1.8)
    t5 = time.time()
    plt.show()
    t6 = time.time()

    print(t2-t1, t3-t2, t4-t3, t5-t4, t6-t5)
    #time.sleep(10)
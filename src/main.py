from pathlib import Path
import queue

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd

MPL_THEME = Path("..", "lib", "mpl-styles", "dark.mplstyle")


def setup_plot():
    plt.style.use(MPL_THEME)
    fig = plt.figure(figsize=(12, 6))
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_yticks([0])
    ax.set_xlim([0, 44100])
    return fig, ax


def audio_callback(indata, frames, time, status):
    q.put(indata[::downsample, [0]])


def update_plot(frame):
    global plotdata
    while True:
        try:
            data = q.get_nowait()
        except queue.Empty:
            break
        shift = len(data)
        plotdata = np.roll(plotdata, -shift, axis=0)
        # Elements that roll beyond the last position are re-introduced
        plotdata[-shift:, :] = data
    for column, line in enumerate(lines_signal):
        line.set_ydata(plotdata[:, column])
    return lines_signal


if __name__ == "__main__":
    device_id = 0     # default audio device_id id
    window = 1000  # window for the data
    downsample = 1     # how much samples to drop
    channels = [1]   # a list of audio channels
    interval = 1     # this is update interval in miliseconds for plot
    device_info = sd.query_devices(device_id, "input")
    samplerate = device_info["default_samplerate"]          # -> 44100
    length = int(window*samplerate/(1000*downsample))   # -> 44100

    plotdata = np.zeros((length, len(channels)))
    q = queue.Queue()

    # Create plot.
    fig, ax = setup_plot()
    lines_signal = ax.plot(plotdata)

    # Microphone input
    stream = sd.InputStream(
        device=device_id,
        channels=max(channels),
        samplerate=samplerate,
        callback=audio_callback
    )
    ani = FuncAnimation(fig, update_plot, interval=interval, blit=True)
    with stream:
        plt.show()

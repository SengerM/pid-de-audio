import nicenquickplotlib as nq # https://github.com/SengerM/nicenquickplotlib
import sounddevice as sd
import numpy as np
import os
import time

os.system('clear')
# Parameters -----------------------------------------------------------
SIGNAL_FREQUENCY = 1000 # In Hertz.
SAMPLING_FREQUENCY = 48000 # Must be integer.
MIN_CHUNK_SIZE = 2**9 # Minimum chunk size.
# ----------------------------------------------------------------------

pure_samples = np.sin(2*np.pi*np.arange(SAMPLING_FREQUENCY/SIGNAL_FREQUENCY)*SIGNAL_FREQUENCY/SAMPLING_FREQUENCY)
while len(pure_samples) < MIN_CHUNK_SIZE:
	pure_samples = np.append(pure_samples, pure_samples)
pure_samples = pure_samples.transpose()

def callback(indata, outdata, frames, time, status):
	outdata[:] = pure_samples.reshape(len(pure_samples),1)
	

stream = sd.Stream(
	samplerate=SAMPLING_FREQUENCY, 
	callback=callback, 
	blocksize=len(pure_samples), 
	channels=1)

stream.start()
time.sleep(1)
stream.stop()

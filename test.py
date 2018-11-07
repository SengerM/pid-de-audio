import nicenquickplotlib as nq # https://github.com/SengerM/nicenquickplotlib
import sounddevice as sd
import numpy as np
import os
import time
from utils import *

os.system('clear')
# Parameters -----------------------------------------------------------
DESIRED_SNR = 90
SIGNAL_FREQUENCY = 1000 # In Hertz.
SAMPLING_FREQUENCY = 48000 # Must be integer.
MIN_CHUNK_SIZE = 2**9 # Minimum chunk size.
# ----------------------------------------------------------------------

PURE_SAMPLES = np.sin(2*np.pi*np.arange(SAMPLING_FREQUENCY/SIGNAL_FREQUENCY)*SIGNAL_FREQUENCY/SAMPLING_FREQUENCY)
while len(PURE_SAMPLES) < MIN_CHUNK_SIZE:
	PURE_SAMPLES = np.append(PURE_SAMPLES, PURE_SAMPLES)
PURE_SAMPLES = PURE_SAMPLES.transpose()

def get_amplitud():
	amplitud = 0
	while True:
		error_signal = yield amplitud
		amplitud += error_signal

def create_callback(): # Esto es una función que devuelve una funcion...
	amplitudegen = get_amplitud() # "amplitudgen" es un objeto (o algo así) que queda instanciado en algún lugar mágico en el más allá.
	def callback(indata, outdata, frames, time, status): # Prototipo del callback de sounddevice.
		error_signal = DESIRED_SNR - calculate_SNR(indata)
		amplitud = amplitudegen.send(error_signal)
		outdata[:] = amplitud/100*PURE_SAMPLES.reshape(len(PURE_SAMPLES),1)
	return callback

stream = sd.Stream(
	samplerate=SAMPLING_FREQUENCY, 
	callback=create_callback(), 
	blocksize=len(PURE_SAMPLES), 
	channels=1)

stream.start()
time.sleep(1)
stream.stop()

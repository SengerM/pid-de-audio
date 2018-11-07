import nicenquickplotlib as nq # https://github.com/SengerM/nicenquickplotlib
import sounddevice as sd
import numpy as np
import os
import time
from utils import *
from pid import *

# Parameters -----------------------------------------------------------
DESIRED_SNR = 40 # Not dB!
SIGNAL_FREQUENCY = 1000 # In Hertz.
SAMPLING_FREQUENCY = 48000 # Must be integer.
MIN_CHUNK_SIZE = 2**9 # Minimum chunk size.
# ----------------------------------------------------------------------

PURE_SAMPLES = np.sin(2*np.pi*np.arange(SAMPLING_FREQUENCY/SIGNAL_FREQUENCY)*SIGNAL_FREQUENCY/SAMPLING_FREQUENCY)
while len(PURE_SAMPLES) < MIN_CHUNK_SIZE:
	PURE_SAMPLES = np.append(PURE_SAMPLES, PURE_SAMPLES)
PURE_SAMPLES = PURE_SAMPLES.transpose()

def create_callback(): # Esto es una función que devuelve una funcion... Es la "función constructora".
	pid = PID(kP=0, kI=0.001) # El objeto "pid" es instanciado y luego queda viviendo en un lugar mágico del más allá.
	pid.set_point = (DESIRED_SNR - 20)/100
	def callback(indata, outdata, frames, time, status): # Prototipo del callback de sounddevice.
		SNR = calculate_SNR(indata.transpose()[0])
		error_signal = DESIRED_SNR - SNR
		amplitude = (pid.get_control(error_signal) + 1)/2
		outdata[:] = amplitude*PURE_SAMPLES.reshape(len(PURE_SAMPLES),1)
		print('SNR={:.2f}   '.format(SNR) + 'e={:.2f}   '.format(error_signal) + 'a={:.3f}   '.format(amplitude))
	return callback

stream = sd.Stream(
	samplerate=SAMPLING_FREQUENCY, 
	callback=create_callback(), 
	blocksize=len(PURE_SAMPLES), 
	channels=1)

stream.start()
time.sleep(10)
stream.stop()

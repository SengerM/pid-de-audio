import nicenquickplotlib as nq # https://github.com/SengerM/nicenquickplotlib
import sounddevice as sd
import numpy as np
import os
import time

os.system('clear')
# Parameters -----------------------------------------------------------
SIGNAL_FREQUENCY = 1000 # In Hertz.
SAMPLING_FREQUENCY = 48000 # Must be integer.
# ----------------------------------------------------------------------

def callback(indata, outdata, frames, time, status):
	outdata[:] = np.sin([2*np.pi*np.arange(SAMPLING_FREQUENCY/SIGNAL_FREQUENCY)*SIGNAL_FREQUENCY/SAMPLING_FREQUENCY]).transpose()

stream = sd.Stream(
	samplerate=SAMPLING_FREQUENCY, 
	callback=callback, 
	blocksize=len(np.sin(2*np.pi*np.arange(SAMPLING_FREQUENCY/SIGNAL_FREQUENCY)*SIGNAL_FREQUENCY/SAMPLING_FREQUENCY)), 
	channels=1)

stream.start()
time.sleep(2)
stream.stop()

# ~ samples = np.sin(2*np.pi*np.arange(SAMPLING_FREQUENCY/SIGNAL_FREQUENCY)*SIGNAL_FREQUENCY/SAMPLING_FREQUENCY)
# ~ # Create the output samples ---------------------
# ~ output_samples = samples
# ~ for k in range(N_CYCLES-1):
	# ~ output_samples = np.append(output_samples, samples)
# ~ # Play and record samples -----------------------
# ~ sd.play(output_samples, SAMPLING_FREQUENCY, loop=True)
# ~ recorded_samples = sd.rec(int(1*SAMPLING_FREQUENCY), samplerate=SAMPLING_FREQUENCY, channels=2)
# ~ recorded_samples = np.transpose(recorded_samples)
# ~ time_axis = np.linspace(0,N_CYCLES/SIGNAL_FREQUENCY,len(recorded_samples[0]))

# ~ nq.plot(time_axis, recorded_samples[0])
# ~ nq.show()

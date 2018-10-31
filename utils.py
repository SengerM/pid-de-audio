import numpy as np

def calculate_SNR(samples):
	fft = np.absolute(np.fft.rfft(samples))
	return fft[fft.argmax()]/fft.mean()

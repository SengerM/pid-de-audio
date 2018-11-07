import time
import numpy as np

class PID:
	def __init__(self, kP = 1, kI = 0, kD = None):
		self.control = 0 # Real number between -1 and 1
		self.__set_point = 0 # Real number between -1 and 1
		self.sensor = [0,0] # Sensor input, real numbers between -1 and 1
		self.kP = kP
		self.kI = kI
		if kD is not None:
			raise ValueError('"kD" is not yet implemented!')
		self.kD = kD
		self.error_integral = 0
		self.last_time_control = time.time()
	
	@property
	def set_point(self):
		return self.__self_point
	@set_point.setter
	def set_point(self, sp):
		if sp < -1 or sp > 1:
			raise ValueError('"set_point" must be between -1 and 1')
		self.__set_point = sp
		
	def print_config(self):
		print('kP=' + str(self.kP) + '    kI=' + str(self.kI) + '    kD=' + str(self.kD))
		print('set_point=' + str(self.__set_point))
		
	def get_control(self, sensor):
		now = time.time()
		if sensor > 2:
			sensor = 2
		if sensor < -2:
			sensor = -2
		self.sensor[1] = self.sensor[0]
		self.sensor[0] = sensor
		error = self.__set_point - self.sensor[0]
		self.error_integral += error
		self.control = self.kP*error + self.kI*self.error_integral
		self.last_time_control = now
		if self.control < -1:
			self.control = -1
		if self.control > 1:
			self.control = 1
		# ~ print('e={:.2f}   '.format(error) + 'c={:.3f}   '.format(self.control))
		# ~ print('I='+str(self.error_integral))
		return self.control

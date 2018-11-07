import time
import numpy as np

class PID:
	def __init__(self, kP = 1, kI = 0, kD = 0):
		self.control = 0 # Real number between -1 and 1
		self.__set_point = 0 # Real number between -1 and 1
		self.kP = kP
		self.kI = kI
		self.kD = kD
		self.error = [0,0]
		self.error_integral = 0
		self.last_time_control = 0
	
	@property
	def set_point(self):
		return self.__self_point
	@set_point.setter
	def set_point(self, sp):
		if sp < -1 or sp > 1:
			raise ValueError('"set_point" must be between -1 and 1')
		self.__set_point = sp
		
	def get_control(self, error):
		now = time.time()
		self.error[1] = self.error[0]
		self.error[0] = error
		self.error_integral += self.error[0]
		self.control = self.kP*self.error[0] + self.kI*self.error_integral + self.kD*(self.error[0] - self.error[1])/(now-self.last_time_control)
		last_time_control = now
		if self.control < -1:
			self.control = -1
		if self.control > 1:
			self.control = 1
		return self.control

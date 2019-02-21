from threading import * # threading
import RPi.GPIO as GPIO
import RPi.GPIO as io 
import time

class _Getch:
	def __init__(self):
		self.impl = _GetchUnix()
	def __call__(self):
		return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class GY2TCar:
	_CENTER = 97
	_MAX_LEFT = 130
	_MAX_RIGHT = 70
	_RELAY_CONTROL_PIN = 23 # relay control signal for go forward
	_RELAY_CONTROL_PIN_BACK= 3 # relay control signal for go backward

	def update(self, angle):
		#print "Updated angle:", angle
		duty = float(angle) / 10.0 + 2.5
		self.pwm.ChangeDutyCycle(duty)

	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(2, GPIO.OUT)

		self.pwm = GPIO.PWM(2, 100)
		self.pwm.start(5)
		GPIO.setwarnings(False)

		# dc motor
		io.setmode(io.BCM) 
		self.power_pin = self._RELAY_CONTROL_PIN 
		self.geri_pin = self._RELAY_CONTROL_PIN_BACK 
                
		io.setup(self.power_pin, io.OUT)
		io.setup(self.geri_pin, io.OUT) 
                
		io.output(self.power_pin, False)        
		io.output(self.geri_pin, False)

		self.update(self._CENTER)
		self.current_angle = self._CENTER

	def play(self):
		getch = _Getch()

		while True:
			inp = getch()

			if inp == "w": # Go forward
				io.output(self.geri_pin,False)
				io.output(self.power_pin, True)
			elif inp == "s": # Stop
				io.output(self.power_pin, False)
				io.output(self.geri_pin,False)
			elif inp == "r": #go backward
				io.output(self.power_pin, False)
				io.output(self.geri_pin,True)
			elif inp == "a": # Go left
				self.update(self._MAX_LEFT)
				# time.sleep(1);  #optional
			elif inp == "d": # Go right
				self.update(self._MAX_RIGHT)
				# time.sleep(1);
			elif inp == "e":
				self.update(self._CENTER)
			elif inp == "q":
				print ("Exit!")
				io.output(self.power_pin, False)
				break
		GPIO.cleanup()

if __name__ == '__main__':
	car = GY2TCar()
	car.play()


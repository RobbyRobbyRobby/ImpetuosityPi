from time import sleep
import busio
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
from enum import Enum
import RPi.GPIO as GPIO
from sshkeyboard import listen_keyboard

doTests = False

class MotorChannelRequest(Enum):
	BOTH = 1
	LEFT = 2
	RIGHT = 3

class MotorDirectionRequest(Enum):
	FORWARD = 1
	BACKWARD = 2

class ServoControl:
	freq = 50
	angleMin = 10
	angleMax = 170
	angleCentre = 90

	angleCurrent = 90

	allStop = False

	servoRearLeft = None
	servoFrontLeft = None
	servoRearRight = None
	servoFrontRight = None
	servoCameraPan = None
	servoCameraTilt = None

	anglePanCurrent = 175
	angleTiltCurrent = 45

	i2c = None
	pca = None

	moving = False

	def __init__(self):

		self.i2c = busio.I2C(SCL, SDA)
		self.pca = PCA9685(self.i2c)
		self.pca.frequency = self.freq

		self.servoRearLeft = servo.Servo(self.pca.channels[0])
		self.servoFrontLeft = servo.Servo(self.pca.channels[1])
		self.servoRearRight = servo.Servo(self.pca.channels[14])
		self.servoFrontRight = servo.Servo(self.pca.channels[15])

		self.servoCameraPan = servo.Servo(self.pca.channels[4])
		#lower = pan -> righ
		self.servoCameraTilt = servo.Servo(self.pca.channels[5])
		#lower = tilt back/up ^

	def SetWheelAngle(self, requestedAngle):
		if (requestedAngle >= self.angleMin and
    	    	    requestedAngle <= self.angleMax):
			self.servoRearLeft.angle = 180 - requestedAngle
			self.servoFrontLeft.angle = requestedAngle
			self.servoRearRight.angle = 180 - requestedAngle
			self.servoFrontRight.angle = requestedAngle

	def AllStop(self):
		self.allStop = True;
		print("servos stop requested at", self.angleCurrent)
		moving = False

	def SetPanTilt(self, pan, tilt):
		#lower = pan -> right
		#lower = tilt back/up ^

		self.anglePanCurrent = pan
		self.angleTiltCurrent = tilt

		self.servoCameraPan.angle = self.anglePanCurrent
		self.servoCameraTilt.angle = self.angleTiltCurrent

	def PanTiltBy(self, panBy, tiltBy):
		#lower = pan -> right
		#lower = tilt back/up ^
		self.anglePanCurrent = self.anglePanCurrent + panBy
		self.angleTiltCurrent = self.angleTiltCurrent + tiltBy

		if (self.anglePanCurrent > self.angleMax):
			self.anglePanCurrent = self.angleMax
		if (self.anglePanCurrent < self.angleMin):
			self.anglePanCurrent = self.angleMin
		if (self.angleTiltCurrent > self.angleMax):
			self.angleTiltCurrent = self.angleMax
		if (self.angleTiltCurrent < self.angleMin):
			self.angleTiltCurrent = self.angleMin

		self.servoCameraPan.angle = self.anglePanCurrent
		self.servoCameraTilt.angle = self.angleTiltCurrent

	def PanWheelsTest(self, qty, returnToCentre):
		i = 0
		self.allStop = False
		self.angleCurrent = self.angleMin

		while (i < qty):
			if (self.angleCurrent <= self.angleMax):
				self.angleCurrent = self.angleCurrent + 0.5
			if (self.angleCurrent >= self.angleMax):
				self.angleCurrent = self.angleMin
				i = i + 1
				print(i)

			self.SetWheelAngle(self.angleCurrent)
			sleep(0.02)

			if (self.servoAllStop):
				self.servoAllStop = False
				print("ServoAllStopCalled")
				break
		self.moving = False

		if (returnToCentre):
			self.CentreWheels()

	def Pivot(self, pivotBy, stepDelay = 0.025):
		if (not self.moving):

			self.moving = True
			self.allStop = False

			while (not self.allStop):
				self.angleCurrent = self.angleCurrent + pivotBy

				if (self.angleCurrent >= self.angleMax):
					self.angleCurrent = self.angleMax
					self.allStop = True

				if (self.angleCurrent <= self.angleMin):
					self.angleCurrent = self.angleMin
					self.allStop = True

				self.SetWheelAngle(self.angleCurrent)
				sleep(stepDelay)
			self.allStop = False
			print("stopped at ", self.angleCurrent)
			self.moving = False

	def CentreWheels(self):
		self.SetWheelAngle(self.angleCentre)
		self.angleCurrent = self.angleCentre
		self.AllStop()

class DriveControl:
	driveLeftForwardPin = 27
	driveLeftBackwardPin = 22
	driveLeftEnablePin = 13
	driveLeftPWM = None

	driveRightForwardPin = 23
	driveRightBackwardPin = 24
	driveRightEnablePin = 18
	driveRightPWM = None

	servoControl = None
	#pwmFreq = 500
	pwmFreq = 1000

	def SetupDriveMotorControl(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.driveLeftForwardPin, GPIO.OUT)
		GPIO.setup(self.driveLeftBackwardPin, GPIO.OUT)
		GPIO.setup(self.driveLeftEnablePin, GPIO.OUT)
		GPIO.setup(self.driveRightForwardPin, GPIO.OUT)
		GPIO.setup(self.driveRightBackwardPin, GPIO.OUT)
		GPIO.setup(self.driveRightEnablePin, GPIO.OUT)

		GPIO.output(self.driveLeftForwardPin, GPIO.LOW)
		GPIO.output(self.driveLeftBackwardPin, GPIO.LOW)
		GPIO.output(self.driveRightForwardPin, GPIO.LOW)
		GPIO.output(self.driveRightBackwardPin, GPIO.LOW)

		self.driveLeftPWM = GPIO.PWM(self.driveLeftEnablePin, self.pwmFreq)
		self.driveLeftPWM.start(0)
		self.driveRightPWM = GPIO.PWM(self.driveRightEnablePin, self.pwmFreq)
		self.driveRightPWM.start(0)

	def AllStop(self):
		GPIO.output(self.driveLeftForwardPin, GPIO.LOW)
		GPIO.output(self.driveLeftBackwardPin, GPIO.LOW)
		GPIO.output(self.driveRightForwardPin, GPIO.LOW)
		GPIO.output(self.driveRightBackwardPin, GPIO.LOW)
		self.driveLeftPWM.start(0)
		self.driveRightPWM.start(0)

	def SetDrivePower(self, Channel, Direction, Power=100):
		validRequest = False

		GPIO.output(self.driveLeftForwardPin, GPIO.LOW)
		GPIO.output(self.driveLeftBackwardPin, GPIO.LOW)
		GPIO.output(self.driveRightForwardPin, GPIO.LOW)
		GPIO.output(self.driveRightBackwardPin, GPIO.LOW)

		#print("setting motors to:",Channel, Direction, Power)
		if (Channel == MotorChannelRequest.BOTH or
	    	    Channel == MotorChannelRequest.LEFT):

			powerLeft = Power

			if (servoControl.angleCurrent < 75):
				powerLeft = powerLeft - 90 +  servoControl.angleCurrent

			if (Direction == MotorDirectionRequest.FORWARD):
				GPIO.output(self.driveLeftForwardPin, GPIO.HIGH)
			else:
				GPIO.output(self.driveLeftBackwardPin, GPIO.HIGH)

			validRequest = True

		if (Channel == MotorChannelRequest.BOTH or
	    	    Channel == MotorChannelRequest.RIGHT):

			powerRight = Power

			if (servoControl.angleCurrent > 105):
				powerRight = powerRight - servoControl.angleCurrent + 90

			if (Direction == MotorDirectionRequest.FORWARD):
				GPIO.output(self.driveRightForwardPin, GPIO.HIGH)
			else:
				GPIO.output(self.driveRightBackwardPin, GPIO.HIGH)

			validRequest = True

		self.driveLeftPWM.start(powerLeft)
		self.driveRightPWM.start(powerRight)

		print("Drive", Direction, "using motor", Channel, "chanel(s)")
		print("Angle", servoControl.angleCurrent)
		print("Left Power", powerLeft, "Right Power",powerRight)

		if (not validRequest):
			print("Bad Motor Power Request")
			DriveAllStop()

	def Test(self):
		print("Test Forward")
		self.SetDrivePower(MotorChannelRequest.BOTH, MotorDirectionRequest.FORWARD)
		sleep(1)
		print("Test Backward")
		self.SetDrivePower(MotorChannelRequest.BOTH, MotorDirectionRequest.BACKWARD)
		sleep(1)
		self.AllStop()
		print("Drive Test Complete")

#----------------------
# Keyboard input
#----------------------

def keyPressed(key):
	print("Pressed: ", key)
	if (key == "w"):
		driveControl.SetDrivePower(MotorChannelRequest.BOTH, MotorDirectionRequest.FORWARD)
	if (key == "x"):
		driveControl.SetDrivePower(MotorChannelRequest.BOTH, MotorDirectionRequest.BACKWARD)
	if (key == "s"):
		driveControl.AllStop()
	if (key == "a"):
		servoControl.AllStop()
		servoControl.Pivot(-1)
	if (key == "d"):
		servoControl.AllStop()
		servoControl.Pivot(1)
	if (key == "c"):
		servoControl.AllStop()
		servoControl.CentreWheels()
	if (key == "z"):
		servoControl.AllStop()
	if (key == "up"):
		servoControl.AllStop(0,10)
	if (key == "down"):
		servoControl.PanTiltBy(0,-10)
	if (key == "left"):
		servoControl.PanTiltBy(-10,0)
	if (key == "right"):
		servoControl.PanTiltBy(10, 0)

#def keyReleased(key):
#	print("released: ", key)
#	if (key == "w"):
#		driveControl.AllStop()
#	if (key == "s"):
#		driveControl.AllStop()
#	if (key == "a"):
#		servoControl.AllStop()
#	if (key == "d"):
#		servoControl.AllStop()

#----------------------
# Execution Point
#----------------------

ready = False
driveControl = None
servoControl = None

while (True):
	if (not ready):
		print("setup")

		servoControl = ServoControl()
		driveControl = DriveControl()
		driveControl.servoControl = servoControl
		driveControl.SetupDriveMotorControl()
		ready = True

		servoControl.AllStop()
		servoControl.CentreWheels()

		servoControl.SetPanTilt(175, 75)

		if (doTests): 
			driveControl.Test() 
			servoControl.PanWheelsTest(1,True)
		listen_keyboard(on_press=keyPressed)

#	if (keyboard.is_pressed("right")):
#		print("right")
#		listener = keyboard.Listener(on_press = on_press)
#		listener.start()

#	event = keyboard.read_event()
#	if (event.event_type == keyboard.KEY_DOWN):
#		print(event.name)

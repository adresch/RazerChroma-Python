import struct
import numpy as np
import time
import json
import requests
import threading
requests.packages.urllib3.disable_warnings()

EChromaSDKDeviceTypeEnum = {'DE_1D': 0, 
	'DE_2D': 1
}

EChromaSDKDevice1DEnum = {
  'DE_ChromaLink': 0,
  'DE_Headset': 1,
  'DE_Mousepad': 2,
  'DE_MAX': 3
};

EChromaSDKDevice2DEnum = {
  'DE_Keyboard': 0,
  'DE_Keypad': 1,
  'DE_Mouse': 2,
  'DE_MAX': 3
}

EChromaSDKDeviceEnum = {
  'DE_ChromaLink': 0,
  'DE_Headset': 1,
  'DE_Keyboard': 2,
  'DE_Keypad': 3,
  'DE_Mouse': 4,
  'DE_Mousepad': 5,
  'DE_MAX': 6
};

COLORS = {
	'RED': 225,
	'GREEN': 65280,
	'BLUE': 16711680,
	'ORANGE': 35071,
	'MAGENTA': 16711935,
	'CYAN': 16776960,
	'WHITE': 16777215,
}

class Heartbeat(object):
    def __init__(self, URI: str):
        try:
            self.URI = URI
            self.go = True
            thread = threading.Thread(target=self.run, args=())
            thread.daemon = True
            thread.start()
        except:
            # TODO Add proper exception handling
            print('Unexpected Error!')
            raise

    def stop(self):
        self.go = False

    def run(self):
        try:
            while self.go:
                requests.put(self.URI + '/heartbeat',  verify=False).json()
                time.sleep(10)
        except:
            # TODO Add proper exception handling
            print('Unexpected Error!')
            raise

class ChromaAppInfo:
    def __init__(self):
        # TODO add proper init-function
        pass

    Title = ""
    Description = ""
    DeveloperName = ""
    DeveloperContact = ""
    SupportedDevices = []
    Category = ""


class ChromaApp:
    def __init__(self, Info: ChromaAppInfo):
        try:
            url = 'https://chromasdk.io:54236/razer/chromasdk'

            payload = {
                "title": Info.Title,
                "description": Info.Description,
                "author": {
                    "name": Info.DeveloperName,
                    "contact": Info.DeveloperContact
                },
                "device_supported": Info.SupportedDevices,
                "category": Info.Category
            }
            json_response = requests.post(url=url, json=payload, verify=False)
            response = json.loads(json_response.text)
            self.SessionID, self.URI = response["sessionid"], response["uri"]
            print(self.URI)
            self.heartbeat = Heartbeat(self.URI)
            #self.Keyboard = Keyboard(self.URI)
            #self.Mouse = Mouse(self.URI)
            #self.Mousepad = Mousepad(self.URI)
            #self.Headset = Headset(self.URI)
            #self.ChromaLink = ChromaLink(self.URI)
            #elf.BcaHandler = ChromaBcaHandler()
        except:
            # TODO Add proper exception handling
            print('Unexpected Error!')
            raise

    def Version(self):
        try:
            return requests.get(url='http://localhost:54235/razer/chromasdk').json()['version']
        except:
            # TODO Add proper exception handling
            print('Unexpected Error!')
            raise

    def __del__(self):
        print('Im dying')
        #self.heartbeat.stop()
        #requests.delete(self.URI)

class ChromaAnimationFile:
	def __init__(self, FileName):
		try:
			self.readIndex = 0
			self.readSize = 4
			self.FileName = FileName
			arrayBuffer = []
			with open(FileName, "rb") as f:
				while (byte := f.read(1)):
					arrayBuffer.append(byte)
			self.arrayBuffer = arrayBuffer
			self.version = int.from_bytes(b''.join(arrayBuffer[self.readIndex:self.readSize]), byteorder='little', signed=False)
			self.readIndex += self.readSize
			self.readSize = 1
			self.deviceType = int.from_bytes(b''.join(arrayBuffer[self.readIndex:self.readIndex + self.readSize]), byteorder='little', signed=False)
			print("Version: "+ str(self.version))
			print("DeviceType: "+ str(self.deviceType))
			self.readIndex += self.readSize
		except:
			# TODO Add proper exception handling
			print('Unexpected Error!')
			raise

class ChromaAnimationParameters:
	def __init__(self):
		pass

	def getMaxLeds(device):
		if device == EChromaSDKDevice1DEnum["DE_ChromaLink"]:
			return 5
		elif device == EChromaSDKDevice1DEnum["DE_Headset"]:
			return 5
		elif device == EChromaSDKDevice1DEnum["DE_Mousepad"]:
			return 15
		else:
			print('getMaxLeds: Invalid device!')

	def getMaxRow(device):
		if device == EChromaSDKDevice2DEnum["DE_Keyboard"]:
			return 6
		elif device == EChromaSDKDevice2DEnum["DE_Keypad"]:
			return 4
		elif device == EChromaSDKDevice2DEnum["DE_Mouse"]:
			return 9
		else:
			print('getMaxRow: Invalid device!')

	def getMaxColumn(device):
		if device == EChromaSDKDevice2DEnum["DE_Keyboard"]:
			return 22
		elif device == EChromaSDKDevice2DEnum["DE_Keypad"]:
			return 5
		elif device == EChromaSDKDevice2DEnum["DE_Mouse"]:
			return 7
		else:
			print('getMaxColumn: Invalid device!')
		

class ChromaAnimationFrame1D(object):
	Duration = 0.1
	Colors = ""
	def __init__(self):
		pass

class ChromaAnimationFrame2D(object):
	Duration = 0.1
	Colors = []
	def __init__(self):
		pass

class ChromaEffect(object):
	def __init__(self, URI):
		self.URI = URI

	def createKeyboardEffect(self, effect, data):

		if (effect == "CHROMA_NONE"):
			obj = {"effect": effect}
		elif (effect == "CHROMA_CUSTOM"):
			obj = {"effect": effect, "param": data}
		elif (effect == "CHROMA_STATIC"):
			obj = {"effect": effect, "param": data}
		elif (effect == "CHROMA_CUSTOM_KEY"):
			pass
			#var color = { "color": data, "key": data };
			#jsonObj = JSON.stringify({ effect: effect, param: color });

		to_json = json.dumps(obj)
		
		payload = to_json
		url = self.URI+"/keyboard"

		headers = {
	  	'content-type': 'application/json',
		}
		response = requests.request("PUT", url, headers=headers, data = payload, verify=False)

	def createKeypadEffect(self, effect, data):
		if (effect == "CHROMA_NONE"):
			obj = {"effect": effect}
		elif (effect == "CHROMA_CUSTOM"):
			obj = {"effect": effect, "param": data}
		elif (effect == "CHROMA_STATIC"):
			obj = {"effect": effect, "param": data}

		to_json = json.dumps(obj)
		
		payload = to_json
		url = self.URI+"/keypad"

		headers = {
	  	'content-type': 'application/json',
		}
		response = requests.request("PUT", url, headers=headers, data = payload, verify=False)

	def createMouseEffect(self, effect, data):
		if (effect == "CHROMA_NONE"):
			obj = {"effect": effect}
		elif (effect == "CHROMA_CUSTOM2"):
			obj = {"effect": effect, "param": data}
		elif (effect == "CHROMA_STATIC"):
			obj = {"effect": effect, "param": data}

		to_json = json.dumps(obj)
		
		payload = to_json
		url = self.URI+"/mouse"

		headers = {
	  	'content-type': 'application/json',
		}
		response = requests.request("PUT", url, headers=headers, data = payload, verify=False)

	def createChromaLinkEffect(self, effect, data):
		if (effect == "CHROMA_NONE"):
			obj = {"effect": effect}
		elif (effect == "CHROMA_CUSTOM"):
			obj = {"effect": effect, "param": data}
		elif (effect == "CHROMA_STATIC"):
			obj = {"effect": effect, "param": data}
		to_json = json.dumps(obj)
		
		payload = to_json
		url = self.URI+"/chromalink"

		headers = {
	  	'content-type': 'application/json',
		}
		response = requests.request("PUT", url, headers=headers, data = payload, verify=False)

	def createHeadsetEffect(self, effect, data):
		if (effect == "CHROMA_NONE"):
			obj = {"effect": effect}
		elif (effect == "CHROMA_CUSTOM"):
			obj = {"effect": effect, "param": data}
		elif (effect == "CHROMA_STATIC"):
			obj = {"effect": effect, "param": data}
		to_json = json.dumps(obj)
		
		payload = to_json
		url = self.URI+"/headset"

		headers = {
	  	'content-type': 'application/json',
		}
		response = requests.request("PUT", url, headers=headers, data = payload, verify=False)

	def createMousepadEffect(self, effect, data):
		if (effect == "CHROMA_NONE"):
			obj = {"effect": effect}
		elif (effect == "CHROMA_CUSTOM"):
			obj = {"effect": effect, "param": data}
		elif (effect == "CHROMA_STATIC"):
			obj = {"effect": effect, "param": data}
		to_json = json.dumps(obj)
		
		payload = to_json
		url = self.URI+"/mousepad"

		headers = {
	  	'content-type': 'application/json',
		}
		response = requests.request("PUT", url, headers=headers, data = payload, verify=False)


class ChromaAnimation1D:
	UseChromaCustom = False
	Run = True

	def __init__(self, animationName):
		self.animationName = animationName

	def openAnimation(self, arrayBuffer, readIndex):

		readSize = 1

		self.device = int.from_bytes(b''.join(arrayBuffer[readIndex:readIndex + readSize]), byteorder='little', signed=False)

		readIndex += readSize
		readSize = 4
		self.frameCount = int.from_bytes(b''.join(arrayBuffer[readIndex:readIndex + readSize]), byteorder='little', signed=False)
		readIndex += readSize

		self.MaxLeds = ChromaAnimationParameters.getMaxLeds(self.device)

		self.frames = []
		for index in range(self.frameCount):
			readSize = 4
			frame = ChromaAnimationFrame1D()
			frame.Duration,  = struct.unpack('f', b''.join(arrayBuffer[readIndex:readIndex + readSize]))
			readIndex += readSize
			readSize = 4 * self.MaxLeds 
			tmp_colors = np.frombuffer(b''.join(arrayBuffer[readIndex:readIndex + readSize]), dtype=np.uint32)
			readIndex += readSize
			frame.Colors = [0] * self.MaxLeds
			for i in range(self.MaxLeds):
				frame.Colors[i] = int(tmp_colors[i])
			
			self.frames.append(frame)

	def playAnimation(self, URI, duration=0, loop=True):
		#TODOO implement stop function and add Animation Information
		self.isRunning = True
		self.effect = ChromaEffect(URI)
		self.playFrames(duration, loop)

		

	def playFrames(self, duration=0, loop=True):
		for i in range(self.frameCount):
			if duration != 0:
				self.frames[i].Duration = duration

			if self.device == EChromaSDKDevice1DEnum["DE_ChromaLink"]:
				self.effect.createChromaLinkEffect("CHROMA_CUSTOM", self.frames[i].Colors)
			elif self.device == EChromaSDKDevice1DEnum["DE_Headset"]:
				self.effect.createHeadsetEffect("CHROMA_CUSTOM", self.frames[i].Colors)
			elif self.device == EChromaSDKDevice1DEnum["DE_Mousepad"]:
				self.effect.createMousepadEffect("CHROMA_CUSTOM", self.frames[i].Colors)
			else:
				print("Unknown device type")

			time.sleep(self.frames[i].Duration)
		if loop == True and self.Run == True:
			self.playFrames(duration, loop)
		else:
			self.applyChromaNoneEffect()

	def applyChromaNoneEffect(self):
		self.isRunning = False
		if self.device == EChromaSDKDevice1DEnum["DE_ChromaLink"]:
			self.effect.createChromaLinkEffect("CHROMA_NONE", "")
		elif self.device == EChromaSDKDevice1DEnum["DE_Headset"]:
			self.effect.createHeadsetEffect("CHROMA_NONE", "")
		elif self.device == EChromaSDKDevice1DEnum["DE_Mousepad"]:
			self.effect.createMousepadEffect("CHROMA_NONE", "")
		else:
			print("Unknown device type")

	def stop(self):
		self.Run = False

class ChromaAnimation2D:
	UseChromaCustom = False
	Run = True

	def __init__(self, animationName):
		self.animationName = animationName

	def openAnimation(self, arrayBuffer, readIndex):

		readSize = 1
		self.device = int.from_bytes(b''.join(arrayBuffer[readIndex:readIndex + readSize]), byteorder='little', signed=False)

		readIndex += readSize
		readSize = 4
		self.frameCount = int.from_bytes(b''.join(arrayBuffer[readIndex:readIndex + readSize]), byteorder='little', signed=False)
		readIndex += readSize

		self.maxRow = ChromaAnimationParameters.getMaxRow(self.device)
		self.maxColumn = ChromaAnimationParameters.getMaxColumn(self.device)

		self.frames = []
		for index in range(self.frameCount):
			readSize = 4
			frame = ChromaAnimationFrame2D()
			frame.Duration,  = struct.unpack('f', b''.join(arrayBuffer[readIndex:readIndex + readSize]))
			readIndex += readSize
			readSize = 4 * self.maxRow * self.maxColumn

			tmp_colors = np.frombuffer(b''.join(arrayBuffer[readIndex:readIndex + readSize]), dtype=np.uint32)
			readIndex += readSize
			colors = [0] * self.maxRow
			for i in range(self.maxRow):
				colors[i] = [0] * self.maxColumn
				for j in range(self.maxColumn):
					colors[i][j] = int(tmp_colors[i * self.maxColumn + j])
			
			frame.Colors = colors
			self.frames.append(frame)

	def playAnimation(self, URI, duration=0, loop=True):
		#TODOO implement stop function and add Animation Information
		self.isRunning = True
		self.effect = ChromaEffect(URI)
		self.playFrames(duration, loop)
		#thread = threading.Thread(target=self.playFrames, args=(loop,duration))
		#thread.daemon = True
		#thread.start()

	def playFrames(self, duration=0, loop=True):
		for i in range(self.frameCount):
			
			if duration != 0:
				self.frames[i].Duration = duration

			if self.device == EChromaSDKDevice2DEnum["DE_Keyboard"]:
				if self.UseChromaCustom == True:
					self.effect.createKeyboardEffect("CHROMA_CUSTOM_KEY", self.frames[i].Colors)
				else:
					self.effect.createKeyboardEffect("CHROMA_CUSTOM", self.frames[i].Colors)
			elif self.device == EChromaSDKDevice2DEnum["DE_Keypad"]:
				self.effect.createKeypadEffect("CHROMA_CUSTOM", self.frames[i].Colors)
			elif self.device == EChromaSDKDevice2DEnum["DE_Mouse"]:
				self.effect.createMouseEffect("CHROMA_CUSTOM2", self.frames[i].Colors)
			else:
				print("Unknown device type")

			time.sleep(self.frames[i].Duration)
		if loop == True and self.Run == True:
			self.playFrames(duration, loop)
		else:
			self.applyChromaNoneEffect()


	def applyChromaNoneEffect(self):
		self.isRunning = False
		if self.device == EChromaSDKDevice2DEnum["DE_Keyboard"]:
			self.effect.createKeyboardEffect("CHROMA_NONE", "")
		elif self.device == EChromaSDKDevice2DEnum["DE_Keypad"]:
			self.effect.createKeypadEffect("CHROMA_NONE", "")
		elif self.device == EChromaSDKDevice2DEnum["DE_Mouse"]:
			self.effect.createMouseEffect("CHROMA_NONE", "")
		else:
			print("Unknown device type")


	def stop(self):
		self.Run = False

	def isRunning(self):
		return self.isRunning

class ChromaAnimation:
	#init ChromaAnimation Object
	def __init__(self, APP, deviceType):
		self.APP = APP
		self.deviceType = deviceType

	def AnimationParams(self, AnimationPath, duration=0, loop=True):
		self.AnimationType = "CHROMA_CUSTOM"
		self.File = ChromaAnimationFile(AnimationPath)
		self.duration = duration
		self.loop = loop
		if self.File.version != 1:
			print("Unsupported Animation version!")
			exit()

		if self.File.deviceType == EChromaSDKDeviceTypeEnum["DE_1D"]:
			self.animation = ChromaAnimation1D(AnimationPath)
			self.animation.openAnimation(self.File.arrayBuffer, self.File.readIndex)
			pass
		elif self.File.deviceType == EChromaSDKDeviceTypeEnum["DE_2D"]:
			self.animation = ChromaAnimation2D(AnimationPath)
			self.animation.openAnimation(self.File.arrayBuffer, self.File.readIndex)

	def playAnimation(self):
		thread = threading.Thread(target=self.animation.playAnimation, args=(self.APP.URI, self.duration, self.loop))
		thread.name = self.deviceType
		thread.daemon = True
		thread.start()

		#self.animation.playAnimation(self.APP.URI, self.duration, self.loop)
	
	def stop(self):
		self.animation.stop()

	
if __name__ == '__main__':

	Info = ChromaAppInfo()
	Info.DeveloperName = 'Antoine Dresch'
	Info.DeveloperContact = 'antoine.dresch@nexioh.eu'
	Info.Category = 'application'
	Info.SupportedDevices = ['keyboard', 'mouse', 'mousepad', 'headset', 'keypad', 'chromalink']
	Info.Description = 'Python Script for playing Chroma animations'
	Info.Title = 'Python Chroma'

	App = ChromaApp(Info)
	
	duration = 0.2

	#Create 1D Object
	ChromaLinkAnimation = ChromaAnimation(App, "chromaLink")
	ChromaLinkAnimation.AnimationParams("./Animations/Wave_ChromaLink.chroma", duration, True)

	HeadsetAnimation = ChromaAnimation(App, "headset")
	HeadsetAnimation.AnimationParams("./Animations/Wave_Headset.chroma", duration, True)

	MousepadAnimation = ChromaAnimation(App, "mousepad")
	MousepadAnimation.AnimationParams("./Animations/Wave_Mousepad.chroma", duration, True)
	
	#Create 2D Object
	KeyboardAnimation = ChromaAnimation(App, "keyboard")
	KeyboardAnimation.AnimationParams("./Animations/Wave_Keyboard.chroma", duration, True)

	KeypadAnimation = ChromaAnimation(App, "keypad")
	KeypadAnimation.AnimationParams("./Animations/Wave_Keypad.chroma", duration, True)

	MouseAnimation = ChromaAnimation(App, "mouse")
	MouseAnimation.AnimationParams("./Animations/Wave_Mouse.chroma", duration, True)


	#Run 1D Animations
	#ChromaLinkAnimation.playAnimation()
	#HeadsetAnimation.playAnimation()
	#MousepadAnimation.playAnimation()
	#Run 2D Animations
	KeyboardAnimation.playAnimation()
	#KeypadAnimation.playAnimation()
	#MouseAnimation.playAnimation()


	'''
	for t in threading.enumerate():
		print(t)
	
	'''
	i = 0
	while True:
		if i == 3:
			pass
			#print("STOP")
			KeyboardAnimation.stop()
		i+=1
		time.sleep(1)

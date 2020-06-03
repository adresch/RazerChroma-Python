import struct
import numpy as np
import time
import json
import requests
import threading
import signal
import sys

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

#credits goes to https://github.com/chroma-sdk/chroma-python
class ChromaColor:
    _red = 0
    _blue = 0
    _green = 0

    def __init__(self, red=None, green=None, blue=None, hexcolor=None):
        try:
            self.set(red=red, green=green, blue=blue, hexcolor=hexcolor)

        except:
            # TODO Add proper exception handling
            print("Unexpected Error!")
            raise

    def set(self, red=None, green=None, blue=None, hexcolor=None):
        try:
            if None not in (red, blue, green):
                if not 0 <= red <= 255:
                    raise ValueError('Red-value out of range!')
                if not 0 <= green <= 255:
                    raise ValueError('Green-value out of range!')
                if not 0 <= blue <= 255:
                    raise ValueError('Blue-value out of range!')

                self._red = int(red)
                self._green = int(green)
                self._blue = int(blue)
                return True

            elif hexcolor is not None:
                if hexcolor[0] == '#':
                    color = hexcolor[1:]
                elif hexcolor[0] == '0' and hexcolor[1] == 'x':
                    color = hexcolor[2:]
                else:
                    raise ValueError('Is not Hex-Value!')
                tmp = int(color, 16)

                self._blue = tmp & 255
                self._green = (tmp >> 8) & 255
                self._red = (tmp >> 16) & 255
                return True
        except:
            # TODO Add proper exception handling
            print('Unexpected Error!')
            raise

    def getHexBGR(self):
        try:
            return '%02x%02x%02x' % (self._blue, self._green, self._red)
        except:
            # TODO Add proper exception handling
            print('Unexpected Error!')
            raise


#credits goes to https://github.com/chroma-sdk/chroma-python
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

#credits goes to https://github.com/chroma-sdk/chroma-python
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

#credits goes to https://github.com/chroma-sdk/chroma-python
class ChromaPythonApp:
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
            self.Keyboard = Keyboard(self.URI)
            self.Keypad = Keypad(self.URI)
            self.Mouse = Mouse(self.URI)
            self.Mousepad = Mousepad(self.URI)
            self.Headset = Headset(self.URI)
            self.ChromaLink = ChromaLink(self.URI)
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

    def stop(self, a='', b=''):
        print('Closing App')
        self.heartbeat.stop()
        requests.delete(self.URI, verify=False)
        sys.exit(0)


class ChormaDevices:
    def __init__(self):
        self.runningAnimation = False
        self.UseChromaCustom = False
        pass

    def setUri(self, URI):
        self.URI = URI

    def setMaxRow(self, maxRow):
        self.maxRow = maxRow

    def setMaxColumn(self, maxColumn):
        self.maxColumn = maxColumn

    def setMaxLed(self, maxLed):
        self.maxLed = maxLed

    def setDeviceDimensionType(self, deviceDimensionType):
        self.deviceDimensionType = deviceDimensionType

    def loadAnimationFile(self, fileName):
        try:
            self.readIndex = 0
            self.readSize = 4
            self.fileName = fileName
            arrayBuffer = []
            with open(fileName, "rb") as f:
                while (byte := f.read(1)):
                    arrayBuffer.append(byte)
            self.arrayBuffer = arrayBuffer
            self.version = int.from_bytes(b''.join(arrayBuffer[self.readIndex:self.readSize]), byteorder='little', signed=False)
            self.readIndex += self.readSize
            self.readSize = 1
            self.deviceType = int.from_bytes(b''.join(arrayBuffer[self.readIndex:self.readIndex + self.readSize]), byteorder='little', signed=False)
            self.readIndex += self.readSize
            
            #print("Version: "+ str(self.version))
            #print("DeviceType: "+ str(self.deviceType))

            if self.deviceType != self.deviceDimensionType:
                raise ValueError("It Looks like the Animation file does not fit the device dimenstions")

            if self.deviceType == EChromaSDKDeviceTypeEnum["DE_1D"]:
                self.readSize = 1

                self.device = int.from_bytes(b''.join(self.arrayBuffer[self.readIndex:self.readIndex + self.readSize]), byteorder='little', signed=False)

                self.readIndex += self.readSize
                self.readSize = 4
                self.frameCount = int.from_bytes(b''.join(self.arrayBuffer[self.readIndex:self.readIndex + self.readSize]), byteorder='little', signed=False)
                self.readIndex += self.readSize

                self.frames = []
                for index in range(self.frameCount):
                    self.readSize = 4
                    frame = ChromaAnimationFrame1D()
                    frame.Duration,  = struct.unpack('f', b''.join(self.arrayBuffer[self.readIndex:self.readIndex + self.readSize]))
                    self.readIndex += self.readSize
                    self.readSize = 4 * self.maxLed
                    tmp_colors = np.frombuffer(b''.join(self.arrayBuffer[self.readIndex:self.readIndex + self.readSize]), dtype=np.uint32)
                    self.readIndex += self.readSize
                    frame.Colors = [0] * self.maxLed
                    for i in range(self.maxLed):
                        frame.Colors[i] = int(tmp_colors[i])
                    
                    self.frames.append(frame)
            
            elif self.deviceType == EChromaSDKDeviceTypeEnum["DE_2D"]:
                self.readSize = 1
                self.device = int.from_bytes(b''.join(self.arrayBuffer[self.readIndex:self.readIndex + self.readSize]), byteorder='little', signed=False)

                self.readIndex += self.readSize
                self.readSize = 4
                self.frameCount = int.from_bytes(b''.join(self.arrayBuffer[self.readIndex:self.readIndex + self.readSize]), byteorder='little', signed=False)
                self.readIndex += self.readSize

                self.frames = []
                for index in range(self.frameCount):
                    self.readSize = 4
                    frame = ChromaAnimationFrame2D()
                    frame.Duration,  = struct.unpack('f', b''.join(self.arrayBuffer[self.readIndex:self.readIndex + self.readSize]))
                    self.readIndex += self.readSize
                    self.readSize = 4 * self.maxRow * self.maxColumn

                    tmp_colors = np.frombuffer(b''.join(self.arrayBuffer[self.readIndex:self.readIndex + self.readSize]), dtype=np.uint32)
                    self.readIndex += self.readSize
                    colors = [0] * self.maxRow
                    for i in range(self.maxRow):
                        colors[i] = [0] * self.maxColumn
                        for j in range(self.maxColumn):
                            colors[i][j] = int(tmp_colors[i * self.maxColumn + j])
                    
                    frame.Colors = colors
                    self.frames.append(frame)
        except:
            # TODO Add proper exception handling
            print('Error loading AnimationFile')
            raise

    def playAnimation(self, loop = True, customDuration = 0):
        #playFrames(self, loop = True, customDuration = 0)
        self.runningAnimation = True
        thread = threading.Thread(target=self.playFrames, args=(loop,customDuration))
        thread.daemon = True
        thread.start()

    def playFrames(self, loop = True, customDuration = 0):
        self.runningAnimation = 1
        try:
            if self.frames:
                for i in range(self.frameCount):
                    if self.runningAnimation == False:
                        break
                    if customDuration != 0:
                        self.frames[i].Duration = customDuration
                    

                    if self.deviceType == EChromaSDKDeviceTypeEnum["DE_2D"]:
                        if self.device == EChromaSDKDevice2DEnum["DE_Keyboard"] and self.UseChromaCustom == True:
                            self.playEffect("CHROMA_CUSTOM_KEY", self.frames[i].Colors)
                        elif self.device == EChromaSDKDevice2DEnum["DE_Mouse"]:
                            self.playEffect("CHROMA_CUSTOM2", self.frames[i].Colors)
                        else:
                            self.playEffect("CHROMA_CUSTOM", self.frames[i].Colors)
                    if self.deviceType == EChromaSDKDeviceTypeEnum["DE_1D"]:
                        self.playEffect("CHROMA_CUSTOM", self.frames[i].Colors)

                    time.sleep(self.frames[i].Duration)
                
                if loop == True and self.runningAnimation != 0:
                    self.playAnimation(loop, customDuration)
                else:
                    self.applyChromaNoneEffect()
            else:
                raise ValueError("It Looks like the no Animation file has been loaded, consider using loadAnimationFile()")
        except:
            # TODO Add proper exception handling
            print('Error playing Animation')
            raise

    def applyChromaNoneEffect(self):
        self.playEffect("CHROMA_NONE")

    def applyChromaStaticColor(self, color):
        self.playEffect("CHROMA_STATIC", int(color.getHexBGR(), 16))

    def stop(self):
        self.runningAnimation = 0


class Keyboard(ChormaDevices):
    """docstring for Keyboard"""
    def __init__(self, URI):
        super(Keyboard, self).__init__()
        self.setUri(URI)
        self.setMaxRow(6)
        self.setMaxColumn(22)
        self.setDeviceDimensionType(EChromaSDKDeviceTypeEnum["DE_2D"])

    def playEffect(self, effect, data=""):
        if (effect == "CHROMA_NONE"):
            obj = {"effect": effect}
        elif (effect == "CHROMA_CUSTOM"):
            obj = {"effect": effect, "param": data}
        elif (effect == "CHROMA_STATIC"):
            color = {"color": data} 
            obj = {"effect": effect, "param": color}
        elif (effect == "CHROMA_CUSTOM_KEY"):
            obj = {"effect": effect, "param": data}

        payload = json.dumps(obj)
        url = self.URI+"/keyboard"
        headers = {
        'content-type': 'application/json',
        }
        response = requests.request("PUT", url, headers=headers, data = payload, verify=False)

class Keypad(ChormaDevices):
    """docstring for Keyboard"""
    def __init__(self, URI):
        super(Keypad, self).__init__()
        self.setUri(URI)
        self.setMaxRow(4)
        self.setMaxColumn(5)
        self.setDeviceDimensionType(EChromaSDKDeviceTypeEnum["DE_2D"])

    def playEffect(self, effect, data=""):
        if (effect == "CHROMA_NONE"):
            obj = {"effect": effect}
        elif (effect == "CHROMA_CUSTOM"):
            obj = {"effect": effect, "param": data}
        elif (effect == "CHROMA_STATIC"):
            color = {"color": data} 
            obj = {"effect": effect, "param": color}

        payload = json.dumps(obj)
        url = self.URI+"/keypad"

        headers = {
        'content-type': 'application/json',
        }
        response = requests.request("PUT", url, headers=headers, data = payload, verify=False)

class Mouse(ChormaDevices):
    """docstring for Keyboard"""
    def __init__(self, URI):
        super(Mouse, self).__init__()
        self.setUri(URI)
        self.setMaxRow(9)
        self.setMaxColumn(7)
        self.setDeviceDimensionType(EChromaSDKDeviceTypeEnum["DE_2D"])

    def playEffect(self, effect, data=""):
        if (effect == "CHROMA_NONE"):
            obj = {"effect": effect}
        elif (effect == "CHROMA_CUSTOM2"):
            obj = {"effect": effect, "param": data}
        elif (effect == "CHROMA_STATIC"):
            color = {"color": data} 
            obj = {"effect": effect, "param": color}

        payload = json.dumps(obj)
        url = self.URI+"/mouse"

        headers = {
        'content-type': 'application/json',
        }
        response = requests.request("PUT", url, headers=headers, data = payload, verify=False)

class Mousepad(ChormaDevices):
    """docstring for Keyboard"""
    def __init__(self, URI):
        super(Mousepad, self).__init__()
        self.setUri(URI)
        self.setMaxLed(15)
        self.setDeviceDimensionType(EChromaSDKDeviceTypeEnum["DE_1D"])

    def playEffect(self, effect, data=""):
        if (effect == "CHROMA_NONE"):
            obj = {"effect": effect}
        elif (effect == "CHROMA_CUSTOM"):
            obj = {"effect": effect, "param": data}
        elif (effect == "CHROMA_STATIC"):
            color = {"color": data} 
            obj = {"effect": effect, "param": color}

        payload = json.dumps(obj)
        url = self.URI+"/mousepad"

        headers = {
        'content-type': 'application/json',
        }
        response = requests.request("PUT", url, headers=headers, data = payload, verify=False)

class Headset(ChormaDevices):
    """docstring for Keyboard"""
    def __init__(self, URI):
        super(Headset, self).__init__()
        self.setUri(URI)
        self.setMaxLed(5)
        self.setDeviceDimensionType(EChromaSDKDeviceTypeEnum["DE_1D"])

    def playEffect(self, effect, data=""):
        if (effect == "CHROMA_NONE"):
            obj = {"effect": effect}
        elif (effect == "CHROMA_CUSTOM"):
            obj = {"effect": effect, "param": data}
        elif (effect == "CHROMA_STATIC"):
            color = {"color": data} 
            obj = {"effect": effect, "param": color}

        payload = json.dumps(obj)
        url = self.URI+"/headset"

        headers = {
        'content-type': 'application/json',
        }
        response = requests.request("PUT", url, headers=headers, data = payload, verify=False)

class ChromaLink(ChormaDevices):
    """docstring for Keyboard"""
    def __init__(self, URI):
        super(ChromaLink, self).__init__()
        self.setUri(URI)
        self.setMaxLed(5)
        self.setDeviceDimensionType(EChromaSDKDeviceTypeEnum["DE_1D"])

    def playEffect(self, effect, data=""):
        if (effect == "CHROMA_NONE"):
            obj = {"effect": effect}
        elif (effect == "CHROMA_CUSTOM"):
            obj = {"effect": effect, "param": data}
        elif (effect == "CHROMA_STATIC"):
            color = {"color": data} 
            obj = {"effect": effect, "param": color}

        payload = json.dumps(obj)
        url = self.URI+"/chromalink"

        headers = {
        'content-type': 'application/json',
        }
        response = requests.request("PUT", url, headers=headers, data = payload, verify=False)

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



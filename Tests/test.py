from chromapythonapp import *

Info = ChromaAppInfo()
Info.DeveloperName = 'Antoine Dresch'
Info.DeveloperContact = 'antoine.dresch@nexioh.eu'
Info.Category = 'application'
Info.SupportedDevices = ['keyboard', 'mouse', 'mousepad', 'headset', 'keypad', 'chromalink']
Info.Description = 'Python Script for playing Chroma animations'
Info.Title = 'Python Chroma'

App = ChromaPythonApp(Info)

signal.signal(signal.SIGINT, App.stop)

print("Starting the app")
time.sleep(2)
print("App is started")


print("Lets Put a different static color on each device for 10s")
#ChromaColor(R,G,B)
App.Keyboard.applyChromaStaticColor(ChromaColor(255,0,0))
App.Keypad.applyChromaStaticColor(ChromaColor(0,255,0))
App.Mouse.applyChromaStaticColor(ChromaColor(0,0,255))
App.ChromaLink.applyChromaStaticColor(ChromaColor(255,255,0))
App.Mousepad.applyChromaStaticColor(ChromaColor(0,255,255))
App.Headset.applyChromaStaticColor(ChromaColor(0,255,255))

time.sleep(10)

print("removing static colors from all the devices")
App.Keyboard.applyChromaNoneEffect()
App.Keypad.applyChromaNoneEffect()
App.Mouse.applyChromaNoneEffect()
App.ChromaLink.applyChromaNoneEffect()
App.Mousepad.applyChromaNoneEffect()
App.Headset.applyChromaNoneEffect()

time.sleep(2)

duration = 0.02

print("Lets load some animations")
App.Keyboard.loadAnimationFile("./Animations/Wave_Keyboard.chroma")
App.Keypad.loadAnimationFile("./Animations/Wave_Keypad.chroma")
App.Mouse.loadAnimationFile("./Animations/Wave_Mouse.chroma")
App.ChromaLink.loadAnimationFile("./Animations/Wave_ChromaLink.chroma")
App.Mousepad.loadAnimationFile("./Animations/Wave_Mousepad.chroma")
App.Headset.loadAnimationFile("./Animations/Wave_Headset.chroma")

print("Lets play the same animation on each device for 10 seconds")
#duration argument is optional.
App.Keyboard.playAnimation(True, duration)
App.Keypad.playAnimation(True, duration)
App.Mouse.playAnimation(True, duration)
App.ChromaLink.playAnimation(True, duration)
App.Mousepad.playAnimation(True, duration)
App.Headset.playAnimation(True, duration)

while True:
	time.sleep(10)
	print("Stopping all the animation")
	App.Keyboard.stop()
	App.Keypad.stop()
	App.Mouse.stop()
	App.ChromaLink.stop()
	App.Mousepad.stop()
	App.Headset.stop()
	print("Everything is looking good!")
	App.stop()
	pass
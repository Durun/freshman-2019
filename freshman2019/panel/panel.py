import RPi.GPIO as GPIO
import time

class Panel(object):

	def __init__(self):
		#各種GPIOピンの設定
		PIN_LED = 9
		PIN_BTN = 10
		PIN_PWR = 18
		PIN_TMP_UP = 14
		PIN_TMP_DN = 15

		#ピンに対する入出力の設定	
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(PIN_LED,GPIO.OUT)
		GPIO.setup(PIN_BTN,GPIO.IN)
		GPIO.setup(PIN_PWR,GPIO.OUT)
		GPIO.setup(PIN_TMP_UP,GPIO.OUT)
		GPIO.setup(PIN_TMP_DN,GPIO.OUT)

		#基板上ボタンイベントの検知
		GPIO.setup(PIN_BTN,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
		GPIO.add_event_detect(PIN_BTN,GPIO.FALLING,bouncetime=300)
		GPIO.add_event_callback(PIN_BTN,SystemPowerButton)


	#--------------------------------------------
	#システム電源ボタンが押されたときの割り込み関数
	#--------------------------------------------
	def SystemPowerButton(channel):
		#TODO:オートモードをオンまたはオフにする
		#TODO:本体LEDをつけたり消したりする	


	#--------------------------------------------
	#本体電源ボタンを押す
	#--------------------------------------------
    def push_power_button(self):
    	GPIO.output(PIN_PWR,GPIO.HIGH)
    	sleep(1)
    	GPIO.output(PIN_PWR,GPIO.LOW)
    	sleep(1)


	#--------------------------------------------
	#温度変更ボタンを押す
	#--------------------------------------------
    def change_temperature(self, dtemp: int):
    	pushtimes = abs(dtemp)

    	if(dtemp < 0):
    		pin = PIN_TMP_DN
    	else
    		pin = PIN_TMP_UP

    	for i in range(pushtimes):
    		GPIO.output(pin,GPIO.HIGH)
    		sleep(1)
    		GPIO.output(pin,GPIO.LOW)
    		sleep(0.5)


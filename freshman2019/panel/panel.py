import RPi.GPIO as GPIO
import time

class Panel(object):

	def __init__(self):
		#各種GPIOピンの設定
		PIN_LED = 2
		PIN_BTN = 3
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

		#システム電源ボタンイベントの検知
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
    def push_power_button(self) -> None:
    	#TODO:ソレノイド操作		
        raise NotImplementedError()


	#--------------------------------------------
	#温度変更ボタンを押す
	#--------------------------------------------
    def change_temperature(self, dtemp: int) -> None:
    	#TODO:ソレノイド操作	
        raise NotImplementedError()

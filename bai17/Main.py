#!/usr/bin/python 
# coding: utf8

#################################################
#         © Keysight Technologies 2019 
#
# PROPRIETARY RIGHTS of Keysight Technologies are 
# involved in the subject matter of this software. 
# All manufacturing, reproduction, use, and sales 
# rights pertaining to this software are governed 
# by the license agreement. The recipient of this 
# code implicitly accepts the terms of the license. 
#
###################################################
#
# FILE NAME  :  M1_L5_T3a_TempHumidity_LCD.py      
# DESCRIPTION:  This program retrieves temperature 
#               and humidity data from SensorTag, 
#				and displays it on the Putty
#				window and the U3811A LCD display.
# NOTE       :  Replace the SensorTag address
#				with your SensorTag's MAC address
#
# #################################################
import os
import sys
import time
import M1_L5_LCD_Fun as LCD
from bluepy import sensortag
import M1_L7_Pressure_Fun as Pres
import requests
import paho.mqtt.client as mqtt
import csv

city,api_key= "Hanoi, Vietnam","db573acb1d90981a42358c1b08024c9f"

savedata = []
def SaveData(row):
  savedata.append(row)
  with open('data.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(savedata)

def GetWeather(city, api_key):
  base_url = "http://api.openweathermap.org/data/2.5/weather"
  params = {"q": city,"appid": api_key}
  while 1:
    response = requests.get(base_url, params=params)
    data = response.json()
    if response.status_code == 200:
      weather = data["weather"][0]["description"]
      temperature = data["main"]["temp"]
      humidity = data["main"]["humidity"]
      print("Kinh do: " ,data['coord']['lon'])
      print("Vi do: " ,data['coord']['lat'])
      print("Thoi tiet tai " + str(city) + ": " + str(weather))
      break

LCD.LCD_init()
LCD.LCD_clear()

print "\nPreparing to connect..."
print "You might need to press the side button on Sensor Tag within 2 seconds..."
time.sleep(1.0)

tag = sensortag.SensorTag('54:6C:0E:53:2C:0A')
tag.humidity.enable()
tag.lightmeter.enable()
luxThreshold = 1500

while (1):
	tag.waitForNotifications(1.0)
	data1 = tag.humidity.read()
	temperature = abs(data1[0])
	humidity = abs(data1[1])
	data2 = tag.lightmeter.read()
	lux = data2
	PresData = int(Pres.Pressure_read()[0])
	print "Anh sang:" + str(lux) + " Nhiet do:" + str(temperature) + " Do am:" + str(humidity) + " Ap suat:" + str(PresData)
	disp1 = "{:.1f}".format(temperature) + "C, " + "{:.1f}".format(humidity) + "%RH"
	
	row = [temperature, humidity, lux, PresData]
	SaveData(row)
	
	
	# LCD.LCD_clear()
	LCD.LCD_print(disp1)
	disp2 = "{:3.0f}".format(lux) + " Lux" + str(PresData) + "Bar"
	# LCD.LCD_print(disp2)
	# time.sleep(0.5)
	
	# LCD.LCD_clear()
	LCD.LCD_print2(disp2)
	# time.sleep(0.5)
	
	output = os.system("./button")
	print(output)
	if(output == 256):
		luxThreshold = luxThreshold + 100
	elif(output== 512):
		luxThreshold = luxThreshold - 100
	if(luxThreshold>1500):
		GetWeather(city,api_key)
		output_relay = os.system("./RELAY")
	else: output_relay = os.system("./RELAY_1")
		
tag.disconnect()
del tag
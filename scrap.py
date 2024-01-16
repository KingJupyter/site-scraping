from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import soundfile
import speech_recognition as sr
import os
import random
import urllib
import pandas as pd
import numpy as np
import certifi
import math
from tkinter import *
from tkinter import messagebox
from datetime import datetime, timedelta
import ssl
import csv 

ssl._create_default_https_context = ssl._create_unverified_context

class Window(Frame):
    
    def __init__(self, master=None):
        Frame.__init__(self, master)        
        self.master = master
        self.pack(fill=BOTH, expand=1)

        label_frame3 = LabelFrame(self, text='Input Search Keyword', height=50, width=200)
        label_frame3.place(x=15,y=10)
        self.username = Entry(self, bd=1)
        self.username.place(x=90,y=30,width=110)
        text6 = Label(self, text="Hungarian")
        text6.place(x=20,y=30)
        
        
        # create button, link it to clickExitButton()
        start_button = Button(self, text="Start", command=self.clickStartButton)
        start_button.place(x=20, y=85, width=80)
        close_button = Button(self, text="Pause", command=self.clickExitButton)
        close_button.place(x=130, y=85, width=80)
    
   
        
    def clickStartButton(self):
        
        username = self.username.get()
        
        print(username)
        # Go to site
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome()
        statusbar.config(text="Tool is running!")
        app.update()
        driver.get('https://www.infobel.com/en/hungary/')
        
        c = driver.find_element("xpath", "//*[@id='sd-cmp']/div[2]/div[1]/div/div/div/div/div/div[2]/div[1]/button[3]/span")
        if c:
            c.click()
        else:
            pass    
            

        # Press the sell button
        companyBtn = driver.find_element("xpath", "//*[@id='search-form-header']/div[1]/span/span/span[1]")
        companyBtn.click()
        
        time.sleep(2)
        
        personBtn = driver.find_element("xpath", "//*[@id='search-type-select-header_listbox']/li[2]")
        personBtn.click()
        
        name_input = driver.find_element("xpath", "//*[@id='residential-search-term-input-header']")
        name_input.send_keys(username)
        
        
        time.sleep(2)

        while True:
            try:
                searchBtn = driver.find_element("xpath", "//*[@id='btn-search-header']")
                time.sleep(1)
                searchBtn.click()
                time.sleep(5)
                break       
            except:
                statusbar.config(text="Now I press searchBtn!")
                app.update() 


        frame = driver.find_element(By.XPATH, "//iframe[@title='reCAPTCHA']")
        print(frame)
        driver.switch_to.frame(frame)
        if frame:
            driver.find_element("xpath", "//*[@id='recaptcha-anchor']/div[1]").click()
            driver.switch_to.default_content()
            time.sleep(1)
            frames=driver.find_elements(By.TAG_NAME, "iframe")
            print("this is the frames: ", frames)
            time.sleep(2)
            driver.switch_to.frame(frames[-1])
            time.sleep(5)

            while True:
                try:
                    driver.find_element(By.ID, "recaptcha-audio-button").click()
                    break
                except:
                    statusbar.config(text="Can not evade captcha! Closing!")
                    app.update()
                    driver.quit()
                
            time.sleep(2)
            statusbar.config(text="Evading Captcha...")
            app.update()

            # Click the play button
            driver.switch_to.default_content()   
            frames= driver.find_elements(By.TAG_NAME, "iframe")
            driver.switch_to.frame(frames[-1])
            time.sleep(2)
            driver.find_element(By.XPATH, "//*[@id=':2']").click()
            print('clicked clidked')

            #get the mp3 audio file
            src = driver.find_element(By.ID, "audio-source").get_attribute("src")
            # print("[INFO] Audio src: %s"%src)   

            #download the mp3 audio file from the source
            file_path = os.path.join(os.getcwd(), "captcha.wav")
            # print(file_path)
            urllib.request.urlretrieve(src, file_path)

            data,samplerate=soundfile.read('captcha.wav')
            soundfile.write('new.wav',data,samplerate, subtype='PCM_16')
            r=sr.Recognizer()

            while True:
                try:
                    with sr.AudioFile("new.wav") as source:
                        audio_data=r.record(source)
                        text=r.recognize_google(audio_data)
                        driver.find_element(By.ID, "audio-response").send_keys(text)
                        time.sleep(2)
                        driver.find_element(By.ID, "recaptcha-verify-button").click()
                        break
                except:
                    statusbar.config(text="Error in Evade captcha.")
                    app.update()
                    driver.quit()
                    

            # Click the verify button
        statusbar.config(text="Successfully evaded!")
        app.update()
        time.sleep(2)
        statusbar.config(text="Searching People...")
        app.update()

        driver.switch_to.default_content() 
        driver.find_element("xpath", "//*[@id='abuse-validation-form']/button").click()

        
        ul = driver.find_element(By.XPATH, "//ul[@class='pagination']")
        li = ul.find_elements(By.TAG_NAME, 'li')[-1]
        a = li.find_element(By.TAG_NAME, 'a')
 
        # next_button = driver.find_element("xpath", "/html/body/div[3]/div[1]/div/div[4]/div[2]/div/div/ul/li[16]/a")
        items_list = []

        while a:
            numberShow = driver.find_elements(By.XPATH, "//span[text()='Display phone']")
            for span in numberShow:
                span.click()

            time.sleep(3)

            person_items = driver.find_elements(By.XPATH, "//div[@class='customer-item-info']")
            print(len(person_items))
            for person_item in person_items:
                items = person_item.find_elements(By.XPATH, "//span[@class='detail-text' and not(text()='Display phone')]")
            print(len(items))
            for item in items:
                # print(item.text)
                items_list.append(item.text)

            time.sleep(2)

            

            ul = driver.find_element(By.XPATH, "//ul[@class='pagination']")
            li = ul.find_elements(By.TAG_NAME, 'li')[-1]
            try:
                a = li.find_element(By.TAG_NAME, 'a')
            except:
                break

            a.click()
            time.sleep(3)

        statusbar.config(text="Exporting to CSV...")
        app.update()
        csv_file = 'output.csv'

        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Address', 'PhoneNumber'])  # Write header row 
            for i in range(0, len(items_list), 2):
                address = items_list[i]
                phone_number = items_list[i + 1]
                writer.writerow([address, phone_number])

        print("Data saved to CSV file.")
        
        print('all done! You are genious!!!')
        
        statusbar.config(text="Successful! You're genious!")
        app.update()
        
    def clickExitButton(self):
        exit()

root = Tk()
app = Window(root)
statusbar = Label(app, text="Let's go bro!", bd=1, relief=SUNKEN, anchor=E)
statusbar.pack(side=BOTTOM, fill=X)
root.wm_title("gameclub.jp")
root.geometry("230x150+1100+400")
root.resizable(False, False)
root.mainloop()
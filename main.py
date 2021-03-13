#!/usr/bin/env python3
# Minimal version of Duino-Coin PC Miner, useful for developing own apps. Created by revox 2020-2021
# Modified by Alicia426 to run with kivy
import socket
import hashlib
import urllib.request
import time
import os
import babylog
import sys  # Only python3 included libraries
# Kivy Imports
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox

# Disabling False positive about Button
# pylint: disable=E1101


class Miner:
    def __init__(self, username, UseLowerDiff):
        self.soc = socket.socket()
        self.soc.settimeout(10)
        self.username = username
        self.UseLowerDiff = UseLowerDiff
        self.status = 'garbageval'

    def mine(self):
        current_buffer = ''
        if self.UseLowerDiff:
            self.soc.send(
                bytes("JOB," + str(self.username) + ",MEDIUM", encoding="utf8")
            )  # Send job request for lower difficulty
        else:
            self.soc.send(
                bytes("JOB," + str(self.username), encoding="utf8")
            )  # Send job request
        job = self.soc.recv(1024).decode()  # Get work from pool
        # Split received data to job (job and difficulty)
        job = job.split(",")
        difficulty = job[2]

        # Calculate hash with difficulty
        for result in range(100 * int(difficulty) + 1):
            ducos1 = hashlib.sha1(
                str(job[0] + str(result)).encode("utf-8")
            ).hexdigest()  # Generate hash
            if job[1] == ducos1:  # If result is even with job
                self.soc.send(
                    bytes(str(result) + ",,Minimal_PC_Miner", encoding="utf8")
                )  # Send result of hashing algorithm to pool
                # Get feedback about the result
                feedback = self.soc.recv(1024).decode()
                if feedback == "GOOD":  # If result was good
                    current_buffer = "Accepted share: " + \
                        str(result)+' '+"Difficulty: "+str(difficulty)
                    break
                elif feedback == "BAD":  # If result was bad
                    current_buffer = "Rejected share: " + \
                        str(result)+' '+"Difficulty: "+str(difficulty)
                    break
        return current_buffer

    def requestAndMine(self):
        try:
            # This sections grabs pool adress and port from Duino-Coin GitHub file
            serverip = "https://raw.githubusercontent.com/revoxhere/duino-coin/gh-pages/serverip.txt"  # Serverip file
            with urllib.request.urlopen(serverip) as content:
                content = (
                    content.read().decode().splitlines()
                )  # Read content and split into lines
            pool_address = content[0]  # Line 1 = pool address
            pool_port = content[1]  # Line 2 = pool port

            # This section connects and logs user to the server
            # Connect to the server
            self.soc.connect((str(pool_address), int(pool_port)))
            server_version = self.soc.recv(3).decode()  # Get server version
            babylog.status("Server is on version: "+str(server_version))
            # Mining section
            while True:
                buff = self.mine()
                if 'Accepted' in buff:
                    babylog.status(buff)
                    self.status = buff
                elif 'Rejected' in buff:
                    babylog.warn(buff)
                    self.status = buff
                else:
                    babylog.warn('Empty buffer, likely error')

        except Exception as e:
            babylog.error("Error occured: " + str(e) + ", restarting in 5s.")
            time.sleep(5)
            self.requestAndMine()


class AppLayout(GridLayout):
    def __init__(self, **kwargs):
        super(AppLayout, self).__init__(**kwargs)
        self.cols = 1

        self.inside = GridLayout()
        self.inside.cols = 1

        self.inside.add_widget(Label(text='DuinoCoin Username:', font_size=30))
        self.name = TextInput(multiline=False)
        self.inside.add_widget(self.name)

        self.inside.add_widget(
            Label(text='Use lower diffuculty? Yes/No', font_size=30))
        self.last_name = TextInput(multiline=False)
        self.inside.add_widget(self.last_name)

        self.add_widget(self.inside)

        self.submit = Button(text='Start Mining', font_size=30)
        self.submit.bind(on_press=self.pressed)
        self.add_widget(self.submit)

    def pressed(self, instance):
        fname = self.name.text
        lname = self.last_name.text
        # print(fname,lname)
        negatives = ['no', 'false', 'n', 'nope']
        if lname.lower() in negatives:
            boolUseLowerDiff = False
        else:
            boolUseLowerDiff = True
        # Fetches the username and difficulty
        babylog.status('Mining for '+fname)
        babylog.status('Using Lower Mining Difficulty: '+lname)
        miner = Miner(fname, boolUseLowerDiff)
        miner.requestAndMine()


class DuinoCoinMinerApp(App):
    def build(self):
        return AppLayout()


if __name__ == "__main__":
    babylog.start()
    DuinoCoinMinerApp().run()

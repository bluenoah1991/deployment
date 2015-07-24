#!/usr/bin/python

import mqtt.client as mqtt

client = mqtt.Client()
client.connect('localhost', 1883, 60)


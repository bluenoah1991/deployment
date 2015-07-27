#!/usr/bin/python

import mqtt.client as mqtt

client = mqtt.Client()
client.connect('localhost', 1883, 60)
client.publish('TEST/123', 'hello111')

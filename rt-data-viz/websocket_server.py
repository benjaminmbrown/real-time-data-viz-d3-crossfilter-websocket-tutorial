import time
import random
import json
import datetime
import os
from tornado import websocket, web, ioloop
from datetime import timedelta
from random import randint

paymentTypes = ["cash", "tab", "visa","mastercard","bitcoin"]
namesArray = ['Ben', 'Jarrod', 'Vijay', 'Aziz']


class WebSocketHandler(websocket.WebSocketHandler):
  # Addition for Tornado as of 2017, need the following method
  # per: http://stackoverflow.com/questions/24851207/tornado-403-get-warning-when-opening-websocket/25071488#25071488
  def check_origin(self, origin):
    return True

  #on open of this socket
  def open(self):
    print ('Connection established.')
    #ioloop to wait for 3 seconds before starting to send data
    ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=3), self.send_data)

 #close connection
  def on_close(self):
    print ('Connection closed.')

  # Our function to send new (random) data for charts
  def send_data(self):
    print ("Sending Data")
    #create a bunch of random data for various dimensions we want
    qty = random.randrange(1,4)
    total = random.randrange(30,1000)
    tip = random.randrange(10, 100)
    payType = paymentTypes[random.randrange(0,4)]
    name = namesArray[random.randrange(0,4)]
    spent = random.randrange(1,150);
    year = random.randrange(2012,2016)

    #create a new data point
    point_data = {
    	'quantity': qty,
    	'total' : total,
    	'tip': tip,
    	'payType': payType,
    	'Name': name,
    	'Spent': spent,
    	'Year' : year,
    	'x': time.time()
    }

    print (point_data)

    #write the json object to the socket
    self.write_message(json.dumps(point_data))

    #create new ioloop instance to intermittently publish data
    ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=1), self.send_data)

if __name__ == "__main__":
  #create new web app w/ websocket endpoint available at /websocket
  print ("Starting websocket server program. Awaiting client requests to open websocket ...")
  application = web.Application([(r'/static/(.*)', web.StaticFileHandler, {'path': os.path.dirname(__file__)}),
                                 (r'/websocket', WebSocketHandler)])
  application.listen(8001)
  ioloop.IOLoop.instance().start()

#!flask/bin/python
# Importing the threading and time  
# modules 
import threading 
import time 

import os

from flask import Flask
app = Flask(__name__)
from flask import Flask
from flask import request


# Inherting the base class 'Thread' 
class AsyncWrite(threading.Thread):  
  
    def __init__(self, text, out): 
  
        # calling superclass init 
        threading.Thread.__init__(self)  
        self.text = text 
        self.out = out 
  
    def run(self): 
  
        f = open(self.out, "a") 
        f.write(self.text + '\n') 
        f.close() 
  
        print("Finished background file write to", 
                                         self.out) 


app = Flask(__name__)
@app.route('/nlp_ingredients', methods=['POST'])
def post():
    print(request.is_json)
    content = request.get_json()
    #print(content)
    f = open("input.txt", "w")
    ingredients = content['ingredients']

    background = AsyncWrite(ingredients, 'input.txt') 
    background.start() 
  
    # wait till the background thread is done 
    background.join()  
    print("Waited until thread was complete")
    

    os.system("python bin/parse-ingredients.py input.txt > results.txt")
    os.system("python bin/convert-to-json.py results.txt > results.json")

    file = open("results.json", "r") 
    json =  file.read() 
    print json

    return json
app.run(host='0.0.0.0', port=5000)



  

  


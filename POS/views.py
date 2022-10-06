"""
Routes and views for the flask application.
"""

from datetime import datetime, timedelta
from flask import render_template
import requests
from flask import session
from flask import g
from flask import redirect
from flask import url_for
from POS import app
from POS.service.db import product_db
from flask import request
import time
from PIL import Image
#from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
#from keras.models import load_model
from bs4 import BeautifulSoup
import numpy as np
import cv2


from pymongo import MongoClient
Client = MongoClient()
db = Client.FruitDeduction
item_collection = db.Items
order_collection = db.Orders

#model = load_model('FV.h5')
labels = {0: 'apple', 1: 'banana', 2: 'beetroot', 3: 'bell pepper', 4: 'cabbage', 5: 'capsicum', 6: 'carrot', 7: 'cauliflower', 8: 'chilli pepper', 9: 'corn', 10: 'cucumber', 11: 'eggplant', 12: 'garlic', 13: 'ginger', 14: 'grapes', 15: 'jalepeno', 16: 'kiwi', 17: 'lemon', 18: 'lettuce',
          19: 'mango', 20: 'onion', 21: 'orange', 22: 'paprika', 23: 'pear', 24: 'peas', 25: 'pineapple', 26: 'pomegranate', 27: 'potato', 28: 'raddish', 29: 'soy beans', 30: 'spinach', 31: 'sweetcorn', 32: 'sweetpotato', 33: 'tomato', 34: 'turnip', 35: 'watermelon'}

fruits = ['Apple','Banana','Bello Pepper','Chilli Pepper','Grapes','Jalepeno','Kiwi','Lemon','Mango','Orange','Paprika','Pear','Pineapple','Pomegranate','Watermelon']
vegetables = ['Beetroot','Cabbage','Capsicum','Carrot','Cauliflower','Corn','Cucumber','Eggplant','Ginger','Lettuce','Onion','Peas','Potato','Raddish','Soy Beans','Spinach','Sweetcorn','Sweetpotato','Tomato','Turnip']


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title = "Page Not Found"), 404

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )


@app.route('/scan')
def scan():
    """Renders the scan page."""
    return render_template(
        'scan.html',
        title='scan',
        year=datetime.now().year
    )

@app.route('/scan', methods = ["POST"])
def deduct_image():
    #deducted_image = run()
    deducted_image = "Apple"
    item = item_collection.find_one({"Fruti Name":deducted_image})
    #get weight from weight machine
    weight = 1.2
    print("deducted fruit is: ", deducted_image)

    product_details = [[deducted_image, 1.2, item["Price"], 1.2*int(item["Price"])]]
    total_bill_amount = 100
    return render_template(
    'bill.html',
    title = "Billing Page",
    details = product_details,
    total_bill = total_bill_amount
    )



def take_photo():
    try:
        cap = cv2.VideoCapture(0)
        total = 1
        for i in range(total):
            # Capture frame-by-frame
            ret, frame = cap.read()
            #if cv2.waitKey(1) & 0xFF == ord('y'): #save on pressing 'y' 
            cv2.imwrite('C:/Users/91990/Downloads/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/c1.jpg',frame)
            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Display the resulting frame
            cv2.imshow('frame',gray)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()
    except Exception as e:
        print("Can't able to take photo")
        print(e)


def process_img(img_path):
    try:
        img=load_img(img_path,target_size=(224,224,3))
        img=img_to_array(img)
        img=img/255
        img=np.expand_dims(img,[0])
        answer=model.predict(img)
        y_class = answer.argmax(axis=-1)
        print(y_class)
        y = " ".join(str(x) for x in y_class)
        y = int(y)
        res = labels[y]
        print(res)
        return res.capitalize()
    except Exception as e:
        print("Can't able to process photo")
        print(e)

def run():
    try:
        print("taking photo")
        take_photo()
        time.sleep(3)
        deducted_image = process_img("C:/Users/91990/Downloads/Fruit_Vegetable_Recognition-master/Fruit_Vegetable_Recognition-master/c1.jpg")
        return deducted_image 
    except Exception as e:
        print("Can't able to run")
        print(e)


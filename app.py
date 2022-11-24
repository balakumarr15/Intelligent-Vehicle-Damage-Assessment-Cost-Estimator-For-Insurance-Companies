import os
import numpy as np
import uuid
import flask
import urllib
from PIL import Image
from tensorflow.keras.models import load_model
from flask import Flask , render_template  , request , send_file
from tensorflow.keras.preprocessing.image import load_img , img_to_array

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model1 = load_model(os.path.join(BASE_DIR , 'body.h5'))
model2 = load_model(os.path.join(BASE_DIR , 'level.h5'))


ALLOWED_EXT = set(['jpg' , 'jpeg' , 'png' , 'jfif', 'JPG', 'JPEG', 'PNG', 'JFIF'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXT

# classes = ['airplane' ,'automobile', 'bird' , 'cat' , 'deer' ,'dog' ,'frog', 'horse' ,'ship' ,'truck']
classes1 = ['Front' ,'Rear', 'Side']
classes2 = ['Mild' ,'Moderate', 'Severe']


def predict(filename , model, dict_result):
    img = load_img(filename , target_size = (224 , 224))
    img = img_to_array(img)
    img = img.reshape(1 , 224 ,224 ,3)

    img = img.astype('float32')
    img = img/255.0
    result = np.argmax(model.predict(img), axis=1)


    # for i in range(3):
    #     dict_result1[body_result[0][i]] = classes1[i]
    #     dict_result2[level_result[0][i]] = classes2[i]

    # res = body_result[0]
    # res.sort()
    # res = res[::-1]
    # prob = res[:3]
    
    # prob_result = []
    # class_result = []
    # for i in range(3):
    #     prob_result.append((prob[i]*100).round(2))
    #     class_result.append(dict_result[prob[i]])

    return dict_result[result[0]]




@app.route('/')
def home():
        return render_template("index.html")

@app.route('/success' , methods = ['GET' , 'POST'])
def success():
    error = ''
    dict_result1 = {0: 'Front', 1: 'Rear', 2: "Side"}
    dict_result2 = {0: 'Minor', 1: 'Moderate', 2: "Severe"}
    target_img = os.path.join(os.getcwd() , 'static/images')
    if request.method == 'POST':
        if(request.form):
            link = request.form.get('link')
            try :
                resource = urllib.request.urlopen(link)
                unique_filename = str(uuid.uuid4())
                filename = unique_filename+".jpg"
                img_path = os.path.join(target_img , filename)
                output = open(img_path , "wb")
                output.write(resource.read())
                output.close()
                img = filename

                body_result = predict(img_path , model1, dict_result1)
                level_result = predict(img_path , model2, dict_result2)

                if(body_result == "Front" and level_result == "Minor"):
                    value = "3000 - 5000 INR"
                elif(body_result == "Front" and level_result == "Moderate"):
                    value = "6000 - 8000 INR"
                elif(body_result == "Front" and level_result == "Severe"):
                    value = "9000 - 11000 INR"
                elif(body_result == "Rear" and level_result == "Minor"):
                    value = "4000 - 6000 INR"
                elif(body_result == "Rear" and level_result == "Moderate"):
                    value = "7000 - 9000 INR"
                elif(body_result == "Rear" and level_result == "Severe"):
                    value = "11000 - 13000 INR"
                elif(body_result == "Side" and level_result == "Minor"):
                    value = "6000 - 8000 INR"
                elif(body_result == "Side" and level_result == "Moderate"):
                    value = "9000 - 11000 INR"
                elif(body_result == "Side" and level_result == "Side"):
                    value = "12000 - 15000 INR"
                else:
                    value = "16000 - 30000 INR"
                
                predictions = {
                      "body":body_result,
                        "level":level_result,
                        "cost":value
                }

            except Exception as e : 
                print(str(e))
                error = 'This image from this site is not accesible or inappropriate input'

            if(len(error) == 0):
                return  render_template('success.html' , img  = img , predictions = predictions)
            else:
                app.route('')
                return render_template('index.html' , error = error) 

            
        elif (request.files):
            file = request.files['file']
            if file and allowed_file(file.filename):
                file.save(os.path.join(target_img , file.filename))
                img_path = os.path.join(target_img , file.filename)
                img = file.filename

                body_result = predict(img_path , model1, dict_result1)
                level_result = predict(img_path , model2, dict_result2)

                if(body_result == "Front" and level_result == "Minor"):
                    value = "3000 - 5000 INR"
                elif(body_result == "Front" and level_result == "Moderate"):
                    value = "6000 - 8000 INR"
                elif(body_result == "Front" and level_result == "Severe"):
                    value = "9000 - 11000 INR"
                elif(body_result == "Rear" and level_result == "Minor"):
                    value = "4000 - 6000 INR"
                elif(body_result == "Rear" and level_result == "Moderate"):
                    value = "7000 - 9000 INR"
                elif(body_result == "Rear" and level_result == "Severe"):
                    value = "11000 - 13000 INR"
                elif(body_result == "Side" and level_result == "Minor"):
                    value = "6000 - 8000 INR"
                elif(body_result == "Side" and level_result == "Moderate"):
                    value = "9000 - 11000 INR"
                elif(body_result == "Side" and level_result == "Side"):
                    value = "12000 - 15000 INR"
                else:
                    value = "16000 - 30000 INR"


                predictions = {
                      "body":body_result,
                        "level":level_result,
                        "cost":value
                }

            else:
                error = "Please upload images of jpg , jpeg and png extension only"

            if(len(error) == 0):
                return  render_template('success.html' , img  = img , predictions = predictions)
            else:
                app.route('')
                return render_template('index.html' , error = error)

    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug = True)



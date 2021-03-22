# ------------------------------------------------
# Program by Denis Astahov
#
#
# Version      Date           Info
# 1.0          13-Dec-2019    Initial Version
#
# ----------------------------------------------
from flask import Flask, render_template,request
import boto3
import dotenv
import os
from werkzeug.utils import secure_filename

S3_KEY      = os.getenv('aws_access_key_id')
S3_SECRET  = os.getenv('aws_secret_access_key')
aws_region ='eu-west-2'
S3_BUCKET='fish-classification-bucket'


s3_resource = boto3.resource(
   "s3",
   aws_access_key_id=S3_KEY,
   aws_secret_access_key=S3_SECRET
)

application = Flask(__name__)
app = application

def get_result(response):
    s=[]
    s.append('Detected labels :' )
    s.append("\n")
    for label in response['Labels']:
        s.append ("Label: " + label['Name'])
        s.append("\n")
        s.append ("Confidence: " + str(label['Confidence']))
        s.append("\n")
        s.append ("Instances:")
        s.append("\n")
        for instance in label['Instances']:
            s.append ("  Bounding box")
            s.append("\n")
            s.append  ("    Top: " + str(instance['BoundingBox']['Top']))
            s.append("\n")
            s.append  ("    Left: " + str(instance['BoundingBox']['Left']))
            s.append("\n")
            s.append  ("    Width: " +  str(instance['BoundingBox']['Width']))
            s.append("\n")
            s.append  ("    Height: " +  str(instance['BoundingBox']['Height']))
            s.append("\n")
            s.append  ("  Confidence: " + str(instance['Confidence']))
            s.append("\n")

        s.append("\n")
        s.append("Parents:")
        for parent in label['Parents']:
            s.append("   " + parent['Name'])
        s.append ("----------")
        s.append("\n")
    return ''.join(s)

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to .s3/<bucetname>/test
        Key = 'test/{}'.format(secure_filename(f.filename))
        s3_resource.Bucket(S3_BUCKET).put_object(Key=Key,Body=f)
        
        # Make prediction
       
        
        client=boto3.client('rekognition','eu-west-2')
        response = client.detect_labels(Image={'S3Object':{'Bucket':S3_BUCKET,'Name':Key}},
        MaxLabels=10)
       

        print(str(len(response['Labels'])))
        result = get_result(response)               # Convert to string
        return result
        
       
       

    return None

#--------Main------------------
if __name__ == "__main__":
    application.debug = True
    application.run()
#------------------------------
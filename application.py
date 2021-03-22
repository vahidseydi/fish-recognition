# ------------------------------------------------
# Program by Denis Astahov
#
#
# Version      Date           Info
# 1.0          13-Dec-2019    Initial Version
#
# ----------------------------------------------
from flask import Flask, render_template
import boto3
import dotenv
import os

aws_access_key_id      = os.gevent('aws_access_key_id')
aws-secret-access-key  = os.gevent('aws-secret-access-key')
aws-region ='eu-west-2'
S3_BUCKET='fish-classification-bucket'

application = Flask(__name__)


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
        s3_resource = boto3.resource('s3')
        Key = 'test/{}'.format(secure_filename(f.filename))
        s3_resource.Bucket(S3_BUCKET).put_object(Key=Key,Body=f)
        
        # Make prediction
       
        '''
        client=boto3.client('rekognition','eu-west-2')
        response = client.detect_labels(Image={'S3Object':{'Bucket':S3_BUCKET,'Name':Key}},
        MaxLabels=10)
       

        print(str(len(response['Labels'])))
        result = get_result(response)               # Convert to string
        return result
        '''
        return "hello"
       

    return None

#--------Main------------------
if __name__ == "__main__":
    application.debug = True
    application.run()
#------------------------------
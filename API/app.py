from flask import Flask, jsonify, request, abort
from functools import wraps
import machineLearning.machPy as machPy
import simplejson as json

app = Flask(__name__)

def match_api_keys(key, ip):
   '''
   Match API keys and discard ip
   @param key: API key from request
   @param ip: remote host IP to match the key.
   @return: boolean
   '''

   if key is None:
      return False

   #API KEY
   api_key = 'Bearer 123'

   #if api_key is None:
   #   return False

   #elif api_key.ip == "0.0.0.0":   # 0.0.0.0 means all IPs.
   #   return True

   #elif api_key.key == key and api_key.ip == ip:
   #   return True

   if api_key == key:
    return True

   return False
   
def require_app_key(f):
   '''
   Decorator function to verify the if the request contains the correct API key.

   @param f: flask function
   @return: decorator, return the wrapped function or abort json object.
   '''

   @wraps(f)
   def decorated(*args, **kwargs):
      if match_api_keys(request.headers.get('Authorization'), request.remote_addr):
         return f(*args, **kwargs)
      else:
         abort(401)
      return decorated
   return decorated

#Routes
@app.route('/')
def index():
    '''
    Index

    @return: string, return the project name.
    '''
    return 'Wi-Fi Fingerprints API'

@app.route('/currentPosition', methods=['POST'])
@require_app_key
def getCurrentPosition():
    '''
    Gets current position based on a fingerprint array.

    @return: string, return the most commom class in models prediction.
    '''

    fingerprints = json.loads(request.data)
    return machPy.getCurrentPositionMultiple(fingerprints)

@app.route('/addFingerprints', methods=['POST'])
@require_app_key
def addFingerprints():
    '''
    Insert new fingerprints into database.

    @return: string, return the most commom class in models prediction.
    '''

    fingerprints = json.loads(request.data)
    return machPy.getCurrentPositionMultiple1(fingerprints, request.args['class'])

if __name__ == '__main__':
    #app.run(debug=True, host='192.168.4.12')
    app.run(debug=True)
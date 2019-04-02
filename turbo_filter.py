import json
import base64
import cv2
import requests
import subprocess
import os
import glob
import urllib3
import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #suppress WARNING
# input
cwd = os.getcwd()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] =cwd + r'\service-account_file.json'
min_criterion = 0.1 #tweak confidence for result
files = glob.glob('./wr/*.jpg')
print(files)
#file = './wr/2.jpg'
wr_items = []
# get credentials
for file in files :
    token = subprocess.Popen("gcloud auth application-default print-access-token",  stdout=subprocess.PIPE, shell=True).stdout.read().rstrip().decode('utf-8')
    cred = token
    # Pass the image data to an encoding function.

    with open(file, "rb") as image_file:
        encoded_img = base64.b64encode(image_file.read()).decode('utf-8')



    # curl with Google API
    headers = {
        'Authorization': 'Bearer %s'%cred ,#'Bearer xxxxx',
        'Content-Type': 'application/json'
    }

    entities = '[  \'kg:/m/01s56h\',\n\'kg:/m/027k4k\',\n\'kg:/m/027wrc\',\n\'kg:/m/03c_kl\',\n\'kg:/m/03hw3\',\n\'kg:/m/03w1t0\',\n\'kg:/m/04sf1h\',\n\'kg:/m/059s10\',\n\'kg:/m/06rrc\',\n\'kg:/m/0h62vyn\',\n\'kg:/m/0h8m1sw\',\n\'kg:/m/0h8mfkx\',\n\'kg:/m/0hgrj75\',\n\'kg:/m/0hgs839\',\n\'kg:/m/0hgs9bq\',\n\'kg:/m/0hgsbhn\',\n\'kg:/m/0hgsbw3\',\n\'kg:/m/0hgsf5m\',\n\'kg:/m/0l_yv\',\n\'kg:/m/032ltr\',\n\'kg:/m/03nn83\',\n\'kg:/m/03qkxs7\',\n\'kg:/m/048dyx\',\n\'kg:/m/0gfgss9\',\n\'kg:/m/09kjlm\',\n\'kg:/m/03nfch\',\n\n\n\'kg:/m/02sb4j\',\n\'kg:/m/0h8k3ng\',\n\'kg:/m/013s93\',\n\'kg:/m/072jc1\',\n\'kg:/m/025xryy\',\n\'kg:/m/019b80\',\n\n\n\'kg:/m/01cmb2\',\n\'kg:/m/02wv6h6\',\n\'kg:/m/0hgnvwy\',\n\'kg:/m/01bfm9\',\n\'kg:/m/0hgpbgq\',\n\'kg:/m/08k64l\',\n\'kg:/m/0cp1w6l\',\n\'kg:/m/0hgn_pr\',\n\'kg:/m/0hgr6\',\n\'kg:/m/02rr7b7\',\n\'kg:/m/0fly7\',\n\'kg:/m/04nk84\',\n\n\n\'kg:/m/01d40f\',\n\'kg:/m/01xqvb\',\n\'kg:/m/02c66t\',\n\'kg:/m/02jt0t\',\n\'kg:/m/05sfw_\',\n\'kg:/m/06hwcd\',\n\'kg:/m/0hgrh95\',\n\'kg:/m/0hgsb5g\',\n\'kg:/m/0hgsh7k\',\n\n\n\'kg:/m/04jq15f\',\n\'kg:/m/078bm7\',\n\'kg:/m/080hkjn\',\n\'kg:/m/08ry3v\',\n\'kg:/m/0hf58v5\',\n\'kg:/m/0hgryjx\',\n\'kg:/m/0hgrzkp\',\n\'kg:/m/0n5v01m\',\n\'kg:/m/01xf5\',\n\'kg:/m/01940j\',\n\n\n\'kg:/m/01wyb3\',\n\'kg:/m/01xygc\',\n\'kg:/m/03tvvb\',\n\'kg:/m/032b3c\',\n\'kg:/m/0dly90\',\n\'kg:/m/01sdv7\',\n\'kg:/m/04xz_5\',\n\'kg:/m/01xyhv\',\n\'kg:/m/027q1m\',\n\'kg:/m/05trrf\',\n\'kg:/m/06hd76\',\n\'kg:/m/047vlmn\',\n\n\n\'kg:/m/0hgs8s2\',\n\'kg:/m/0hgslft\',\n\'kg:/m/017ftj\',\n\'kg:/m/0404d  \',\n\'kg:/m/02h19r \',\n\'kg:/m/02dl1y   \',\n\'kg:/m/02wbtzl \',\n\'kg:/m/06t241   \',\n\'kg:/m/0hgs54_\',\n\'kg:/m/01n5_8\',\n\'kg:/m/0174n1 \',\n\'kg:/m/0h8m0th\',\n\'kg:/m/0h8m5r9\',\n\'kg:/m/0hgp5bc\',\n\'kg:/m/0hgr9by\',\n\'kg:/m/0176mf\',\n\'kg:/m/02_vjy\',\n\'kg:/m/01r546\',\n\'kg:/m/01xdjk\']'

    data = '{ \'image_entities_request\': {\n                \'image\': {\n                    \'content\': \'%s\'\n                 },\n                 \'mids\': {\n                    \'entity_ids\': %s\n                 }\n             }\n          }' %(encoded_img, entities)

    response = requests.post('https://aiworkshop.googleapis.com/xxx', headers=headers, data=data, verify=True).json()
    print(response)
    # response

    keys = ['confidence', 'entityId']
    #[x.get(key) for x in response.get('imageEntitiesResponse').get('entityPredictions') for key in keys]
    #max([x.get('confidence') for x in response.get('imageEntitiesResponse').get('entityPredictions')])

    # [x for x in response.get('imageEntitiesResponse').get('entityPredictions') if x.get('confidence')== \
    # max([x.get('confidence') for x in response.get('imageEntitiesResponse').get('entityPredictions')])]
    import entities_map
    mapped_dict = entities_map.create_dict()


    #max confidence and key entity:
    def get_result(response):
        '''returns the item category with the hight confidence'''
        if response.get('imageEntitiesResponse') == None:
            item = 'None'
        elif [x.get(key) for x in [x for x in response.get('imageEntitiesResponse').get('entityPredictions') if x.get('confidence') == \
            max([x.get('confidence') for x in response.get('imageEntitiesResponse').get('entityPredictions')])] for key in keys ][0] >min_criterion:
            response_id = [x.get(key) for x in [x for x in response.get('imageEntitiesResponse').get('entityPredictions') if x.get('confidence') == \
                max([x.get('confidence') for x in response.get('imageEntitiesResponse').get('entityPredictions')])] for key in keys ][1]
            item = mapped_dict.get(response_id)
        else:
            item = 'low_confidence'
        return(item)
    item_name = get_result(response)
    wr_items.append([file,item_name])
    time.sleep(5)
    print(item_name,file)

wr_items

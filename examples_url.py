import os
#import urllib3
#import urllib.request
import requests
from f_bidr import read_logical_records


dataFolder = os.environ['HOME']+"/bidr_data/"

#BIDR
url_root = 'http://pds-geosciences.wustl.edu/mgn/mgn-v-rdrs-5-bidr-full-res-v1/'
url_folder = ['MG_4001/F0376_3/']
url_file = 'FILE_15'

'''
#CBIDR
url_root = 'http://pds-geosciences.wustl.edu/mgn/mgn-v-rdrs-5-c-bidr-v1/'
url_folder = ['MG_3101/C0376_03/']
url_file = 'IM2.DAT'
'''

# makes folder for data in user's home directory (only if it doesn't exist)
def create_dir(filepath):
    directory = os.path.dirname(filepath)
    if not os.path.exists(directory):
        os.makedirs(directory)
create_dir(dataFolder)


for i in url_folder:
    create_dir(dataFolder+i)
    #creates subfolder if one doesn't exist
    url = url_root+i+url_file
    print('Retrieving file from ', url)
    r = requests.get(url) # create HTTP response object
    filepath = dataFolder+i+'/'+url_file
    print('File saved in ', filepath)
    with open(filepath,'wb') as f: 
         f.write(r.content) 
            

import os
#import urllib3
#import urllib.request
import requests
from f_bidr import read_logical_records

# These three are for creating and viewing an image, and nothing else.
import matplotlib.pyplot as plt
import matplotlib
import numpy as np


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

#if folder for data in user's home directory (only if it doesn't exist)

dataFolder = os.environ['HOME']+"/bidr_data/"
def create_dir(filepath):
    directory = os.path.dirname(filepath)
    if not os.path.exists(directory):
        os.makedirs(directory)

        
            
        
#creates bidr_data folder if one does not exist in user's home directory
create_dir(dataFolder)

#saves the original file in the appropriate subdirectory
for i in url_folder:
    create_dir(dataFolder+i)   #creates subfolder if one doesn't exist
    url = url_root+i+url_file
    filepath = dataFolder+i+url_file
    if os.path.exists(filepath) == True:
        print('File Exists. Generating image file.')
    else:
        print('Retrieving file from ', url)
        r = requests.get(url) 
        print('File saved in ', filepath)
        with open(filepath,'wb') as f:
            f.write(r.content) 
            


    # Let's start off with MG_4001/F0376_3/FILE_15.
    # FILE_15 in now my root directory $HOME/bidr_data/MG_4001/F0376_3/

    with open(filepath, 'rb') as f:
         contents = f.read()

    # Files 12-19 of the magellan data (in any given folder) are a series
    # of one or more "logical records", these unrelated chunks of
    # information. For getting started, that just means one thing: you can
    # choose how much of the file you read in. The largest files are
    # ~100MB and consist of ~5000 logical records (FILE_15 are the
    # largest, always).

    # Let's look at two records to start. When you use this on your own,
    # you can leave out the number of records to read to just read them
    # all. A warning: that can take up to 30 seconds.
    records = read_logical_records(contents, 2)

    # The actual image data is contained in records['data_block']. It's an
    # array of lines of pixels---with extra information. The extra info
    # describes how many "filler pixels" are at the beginning and end of a
    # given line (slightly more to this story).

    # The first line of pixels in the first logical record is:
    records[0]['data_block'][0]['line']

    # We can use these lines of pixels to make an image. Let's get just
    # the lines out:
    lines = [x['line'] for x in records[0]['data_block']]

    # There's 52 lines of pixels, and 512 pixels in each line. Creating an
    # image (this way) is making an array out of them, and interpreting
    # them as a grayscale image.
    gray = matplotlib.cm.get_cmap('gray')
    image = np.array(lines)
    image_url = filepath+'.png'
    plt.imsave(image_url, image, cmap=gray)

    # Go oogle that. It's so teasingly somewhere between TV static and
    # drab planet surface. 

    # This is image metadata:
    info = records[0]['secondary_header']['annotation_block']['label']
    
    # You may have questions about whether or not
    # this is correct. I do too. There are helpful references and
    # information both in the logical record, and in the BIDR report which
    # is in papers+documents/MGN-FBIDR-SIS-SDPS-101-RevE.pdf
    # - Page 48 talks about the actual image data. You'll find that there
    #   are two types of images (really four), and their data is
    #   interpreted differently. I don't currently have anything written
    #   to interpret single-look data (but FILE_15 is multi-look data,
    #   which I can work with right now)
    # - Page 50 speaks more about how pixel intensity is derived.
    # - Explanations of the fields of `info` are on page 39. Aside from
    #   printing info out to explore information contained within, you can
    #   look at annotation_labels['image-data'] from f_bidr.py for a list
    #   of the field names in the info dictionary. For instance,
    #   info['line_count'] is the number of lines in the image, and the
    #   field name is the same as given in annotation_labels['image-data'].

    # A last note: there may be some traps you'll fall into. 
    # - For one, if you look at info['line_length'], you'll find it's 516,
    #   as opposed to the 512 I told you. I've read everything in from the
    #   binary file as given; there really are 516 bytes in each image
    #   line, but the 1st four bytes specify the first and last non-filler
    #   pixels. They're not pixels at all.
    # - Not all the information that's read is interpreted usefully, like
    #   times

    print('Image generated: ', image_url )

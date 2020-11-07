import numpy as np 
import pandas as pd
import requests

# create dataframe from dataset csv file
df = pd.read_csv("faceexp-comparison-data-test-public.csv")

# get numpy arrays full of links
links1 = df.iloc[:,0].to_numpy()
links2 = df.iloc[:,5].to_numpy()
links3 = df.iloc[:,10].to_numpy()
# concatenate
links = np.hstack((links1,links2,links3))

# initialize loop variables
currlink = links[0]
iter = 0

# go to every link
for link in links:

  if link != currlink:  # don't download image again
    imgname = "images/img" + str(iter) + ".jpg"

    # download the image with requests
    with open(imgname, 'wb') as handle:
        response = requests.get(link, stream=True)
        if not response.ok:
            print(response, iter)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block) # save the file


    iter = iter+1 # to name files
  
  # temporary break point (remove to download entire dataset)
  if iter == 20:
    break

  currlink = link   # advance to the next link
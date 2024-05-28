# JSON Visualizer
# Convert this:
![image](https://github.com/avezshariq/json_visualizer/assets/79614977/c157e9fd-922b-4d04-988a-9b3b5974f50c)
# Into this:
![image](https://github.com/avezshariq/json_visualizer/assets/79614977/4d17127c-bdde-4bd3-8b79-d4b8199535d2)

Opening a JSON file and getting an understanding of its structure can be pretty daunting sometimes, especially if it involves a huge amount of data. This program helps visualise the tree of the JSON file. It can be used to get some useful information like:
1. Structure of the JSON file
2. Number of levels or depth of the file
3. Where the metadata is and where the actual data is
4. Pictorial representation which is easier to understand

## Steps
1. Reads the JSON file
2. Gets all useful information such as levels, names etc..
3. Creates an HTML file containing the structure

**Examples present as 'data.json' and 'data.html'**

# How to Use
This repo is created for online use. If you want to use it online, go to:
https://avez-json-visualizer.glitch.me/
If you want to use it on local machine 
1. Download the `json_visualizer.py`
2. Then do `from json_visualizer import json_visualizer`
3. Finally you can `html_file = json_visualizer('filename.json', True)`




from flask import Flask, request, render_template
import os
from json_visualizer import json_visualizer

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        uploaded_file.save(os.path.join(app.instance_path, 'the_uploaded_data.json'))
        file_path = os.path.join(app.instance_path, 'the_uploaded_data.json')
        html_content = json_visualizer(file_path, False)
        return html_content
    return render_template('index.html')

if __name__ == '__main__':
    # Create the instance folder if it doesn't exist
    os.makedirs(app.instance_path, exist_ok=True)
    app.run(debug=True)

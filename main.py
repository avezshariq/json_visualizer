from flask import Flask, render_template, request
import json
from json_visualizer import json_visualizer

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home() -> str:
    if request.method == 'POST':
        file = request.files['file']
        file_content = file.read()
        data = json.loads(file_content)
        the_html = json_visualizer(data, False)
        return the_html

    return render_template('index.html')


if __name__ == '__main__':
    app.run()
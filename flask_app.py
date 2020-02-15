# pip install flask

import extract_git
import extract_jira
import extract_jenkins
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/git/<status>/<n_days>')
def get_git_data(status, n_days):
    return jsonify(extract_git.p2_git(status, n_days))


@app.route('/jira/<status>')
def get_jira_data(status):
    return jsonify(extract_jira.p2_jira(status))


@app.route('/jenkins')
def get_jenkins_data():
    return jsonify(extract_jenkins.p2_jenkins())

# @app.route('/snow/<env>')
# def get_snow_data(env):
#     return jsonify(extract_snow.p2_snow(env))


@app.route('/')
def greet():
    return 'Hello-Welcome to Autodesk'


if __name__ == '__main__':
    app.run(debug=True)

# Annotation App for Hate speech Text data 🫶 

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)


## Introduction
A web app that lets you re-label records with new labels. This app makes it easier to add comments and gets rid of the need for expensive tools. The annotations are saved in real time in a connected Google Sheet, which means that multiple people can annotate at the same time (up to the limit of the Google API’s request).  The app consists of a start page, an annotation area, and an interview area. This app can be adapted for any text annotation task.

## Features
- User-friendly web interface for efficient annotation.
- Real-time storage of annotations in a connected Google Sheet.
- Simultaneous collaboration for multiple users (subject to Google API’s requeste limits).

## Installation
Install the required dependencies:

`pip install -r requirements.txt`

Obtain Google Sheet API access:
- Log in to BigQuery and retrieve the corresponding API credentials.
- Save the JSON file containing the credentials.
- Add the JSON file to your folder and add the path to the file within the function.py file --> get_credential(self)

## Usage
```python app.py ```

or hosted it online on the [StreamlitCloud]([https://www.example.com](https://streamlit.io/cloud)) ☁️

You are welcome to change this template to fit your project and its needs 😋
## Website

Check out the [Annotation Web App](https://share.streamlit.io/raisarom/text_annotation_webapp/main/Hate_app.py) to see what it looks like 🎉


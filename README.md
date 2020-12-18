# Balr Twitter Dashboard

## Front-end 

#### Flask boiler plate used (https://flask-admin-boilerplate.herokuapp.com/) all credit goes to them for the design of the front end.

### Installation 
- from ./front-end run
```bash 
pip install -r requirements.txt
```

in command line
```cmd
python app.py
```

### Endpoints
- This project is a single dashboard screen, once running the app.py file the URL provided form the flask app is the only end point active in this file. 

## Back-end 

- Twitter data sourced using Tweepy and stored on AWS DynamoDB. 
- If you are wanting to replicate this code, you will need to set up
1. AWS account
2. Twitter API credentials 

### Installation
- from ./back-end run 
``` bash
pip install -r requirements.txt
```

in command line 
```cmd 
python main.py
```

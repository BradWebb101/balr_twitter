# Personal Project Portfolio

This project is a dashboard I built, with data from Twitter using #BALR. BALR is a dutch lifestyle brand https://www.balr.com/  

## Screenshot

![alt text](./readme_images/screenshot.PNG "Title")

## Project Example

<!-- [Website](https://bradwebb101.com) -->
TBA

## Things i borrowed

- HTML template https://startbootstrap.com/theme/sb-admin-2

## How is it built

### Front end

- This project is built on HTML and Vanilla Javascript. I used SB Admin 2 template for the dashboard.

### Back end

- This site is built as a serverless application, it uses AWS Lambda, S3, DynamoDB, API Gateway and Cloudfront.
- The back end is written in Python, using Tweepy to get data from the Twitter API and Boto3 to connect to Dynamo DB.
  
## Infrastructure

![infrastrucure](./readme_images/infrastructure.png)

## Downloading and usage

### Front-end
As this project is just HTML and Vanilla JS, the only dependency on the front end is a web browser. 

### Back-end
Clone this repo 

``` git
git clone https://github.com/BradWebb101/balr_twitter.git .
```

Install dependancies

``` pip
pip install -r requirments.txt
```

- You will need to set up Twitter API credentials with Twitter.
- You will need to set up an AWS account, and set up a table in DynamoDB called 'balr_twitter'
- Environment variables needed in .env file
  - API_KEY: Twitter api key
  - API_KEY_SECRET: Twitter api secret key
  - BEARER_TOKEN: Twitter api bearer token
  - ACCESS_TOKEN: Twitter api access token
  - ACCESS_TOKEN_SECRET: Twitter api secret token
  - AWS_ACCESS_KEY_ID: AWS access key
  - AWS_SECRET_ACCESS_KEY: AWS secret key
  - AWS_DEFAULT_REGION: Aws default region

All environment variable are the same as the ones in the AWS and Twitter API documentation.

Run back end code

``` python
python main.py
```

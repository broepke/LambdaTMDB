import requests # Available via AWS Lambda Layer
import json # Available via AWS Lambda Layer
import os # Available via AWS Lambda Layer
import logging # Available via AWS Lambda Layer
import boto3 # Available via AWS Lambda Layer
import pandas as pd # Available via AWS Lambda Layer
import numpy as np # Available via AWS Lambda Layer
from botocore.session import Session
from botocore.config import Config

import tmdbsimple as tmdb # https://github.com/celiao/tmdbsimple

# max_attempts: retry count / read_timeout: socket timeout / connect_timeout: new connection timeout
s = Session()
c = s.create_client('s3', config=Config(connect_timeout=20, read_timeout=60, retries={'max_attempts': 10}))

# Logging events are sent to CloudWatch Logs
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_tmdb_api_key():
    """Use the AWS secrets manager (chanced as Lambda Layer) to get the TMDB API key.

    Returns:
        str: TMDB_API_KEY
    """
    
    headers = {"X-Aws-Parameters-Secrets-Token": os.environ.get("AWS_SESSION_TOKEN")}

    secrets_extension_endpoint = (
        "http://localhost:"
        + "2773"
        + "/secretsmanager/get?secretId="
        + "<< your secrets arn >>"
    )

    r = requests.get(secrets_extension_endpoint, headers=headers)
    secret = json.loads(r.text)["SecretString"]
    secret = json.loads(secret)
    TMDB_API_KEY = secret["TMDB_API"]

    return TMDB_API_KEY

def write_to_s3(df, type, imdb_id):
    
    """
    Wite a dataframe to S3 as JSON

    Parameters:
    
    df: dataframe to write
    type: type of data (crew or credits)
    imdb_id: imdb id of the movie
    
    Returns:
        "Success" upon completion
    """    
    
    # Output the Credits to S3
    output = json.loads(df.to_json(orient='records'))
    
    string = str(output)
    encoded_string = string.encode("utf-8")

    bucket_name = "lambda-tmdb"
    file_name = "out.json"
    s3_path = "output/" + type + "/" + imdb_id + "-" + type + "-" + file_name

    s3 = boto3.resource('s3')
    object = s3.Object(bucket_name, s3_path)
    object.put(Body=encoded_string)
    
    return "Success"

def lambda_handler(event, context):
    
    """
    Call like this: Gateway URL + ?ids=tt0162346&ids=tt0326900
    """
    
    # Get the IDs from the Query String
    params = event["multiValueQueryStringParameters"]
    
    id_list = params['ids']
 
    
    # Get credentials from from Secrets Manager
    KEY = get_tmdb_api_key()
    
    tmdb.REQUESTS_TIMEOUT = (25)
    tmdb.API_KEY = KEY
    
    for i in range(len(id_list)):

        imdb_id = id_list[i]
        
        logging.info(f"RUN OF IMDB ID: {imdb_id}")
        
        movie = tmdb.Find(id=imdb_id).info(external_source='imdb_id')
        if movie['movie_results'] == []:
            logging.info(f"NO MOVIE FOUND: {imdb_id}")
            
        else:
            movie_id = movie['movie_results'][0]['id']
            movie = tmdb.Movies(movie_id)
        
 
            credits = movie.credits()
            keyValList = ['Visual Effects']
            res = [d for d in credits['crew'] if d['known_for_department'] in keyValList]
            df = pd.DataFrame(res)
            df.fillna('None', inplace=True)
           
            if len(df) == 0:
                logging.info(f"NO CREW FOUND: {imdb_id}")
            else:
                df_crew = df.drop(columns='credit_id')
                df_credits = df[['id', 'credit_id']]
                
                # As long as the movie has people, write it to S3
                write_to_s3(df_crew, "crew", imdb_id)
                logging.info("CREW ADDED TO S3")
                
                write_to_s3(df_credits, "credits", imdb_id)
                logging.info("CREDITS ADDED TO S3")
        

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": "Success",
    }

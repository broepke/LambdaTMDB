# delete the old zip
rm tmdb-deployment-package.zip

# change the directory to the site-packagaes directory and zip the contents
cd venv/lib/python3.9/site-packages

# Explicitly add the tmdbsimple package folders needed for the lambda function
zip -r ../../../../tmdb-deployment-package.zip tmdbsimple tmdbsimple-2.9.1.dist-info

# change back to the root directory and add the needed python files
cd ../../../../
zip -g tmdb-deployment-package.zip lambda_function.py lambda_helper_functions.py

# deploy to AWS Lambda
#aws lambda update-function-code --function-name my-test-function --zip-file fileb://tmdb-deployment-package.zip

aws lambda update-function-code --function-name lamba-tmdb --zip-file fileb://tmdb-deployment-package.zip

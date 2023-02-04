# LambaTMDB
 
## Introduction to ETL with AWS Lambda

When it comes time to build an ETL pipeline, many options exist. You can use a tool like [Astronomer]({filename}astrointro.md) or [Prefect](http://prefect.io) for Orchestration, but you will also need somewhere to run the compute. With this, you have a few options:

* Virtual Machine (VM) like AWS EC2
* Container services like AWS ECS or AWS Fargate
* Apache Spark like AWS EMR (Elastic Map Reduce)
* Serverless Computing like AWS Lambda

Each of these has its advantages. If you're looking for simplicity in setup, maintenance, and cost, you can run *simple* jobs with** AWS Lambdas** or Serverless Computing.

Notice I said **simple**. AWS Lambdas are not meant for compute-intensive or long-running jobs. They're suitable for executing small amounts of code that take minutes versus hours.

## What is AWS Lambda and Serverless Computing?

A Lambda function in AWS is a piece of code that is executed in response to an event. The event can be a request to an API endpoint, a file being uploaded to an S3 bucket, or a scheduled event. The code is executed, and the results are returned. Here is a great description of how it works from [AWS](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html):

>Lambda runs your function only when needed and scales automatically, from a few daily requests to thousands per second. You pay only for the computing time you consume—there is no charge when your code is not running. For more information, see AWS Lambda Pricing.

A Lambda function is a wonderful way to think about ETL for smaller jobs that need to run frequently. Such as on a trigger, like an API call, or nightly on a schedule. It also allows you to orchestrate multiple Lambda functions to create a more complex ETL pipeline.

Let's dive into creating our first Lambda function.

Read more here: [How to Setup a Simple ETL Pipeline with AWS Lambda for Data Science](https://www.dataknowsall.com/lambdaetl.html)
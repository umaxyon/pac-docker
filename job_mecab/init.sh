#!/bin/bash
aws s3 cp s3://kabupac.system/PacPac.csv /root/dict/
cd /root/ja-tokenizer
source env/bin/activate
fab setup
fab makezip
aws s3 cp /root/ja-tokenizer/lambda_function.zip s3://kabupac.system/
aws lambda delete-function --region ap-northeast-1 \
                           --function-name MecabFunc
aws lambda create-function --region ap-northeast-1 \
                           --function-name MecabFunc \
                           --runtime python2.7 \
                           --code S3Bucket=kabupac.system,S3Key=lambda_function.zip \
                           --role arn:aws:iam::007575903924:role/cloud9-Job001-Job001Role-NQ27F73FEWTL \
                           --handler lambda_function.lambda_handler
# Specification: AWS_s3_upload

## Expected Functionality
This project implements Aws S3 Upload.

boto3 (pip install boto3) <br />
- Specify both ACCESS_KEY and SECRET_KEY. You can get them both on your AWS account in "My Security Credentials" section. <br />
- Specify the local file name, bucket name and the name that you want the file to have inside s3 bucket using LOCAL_FILE, BUCKET_NAME and S3_FILE_NAME variables. <br />

## Input
- User inputs as required by the application
- Configuration parameters as needed

## Expected Output
- Results based on the application's functionality
- Status messages and feedback to the user

## Usage
```bash
python app.py
```

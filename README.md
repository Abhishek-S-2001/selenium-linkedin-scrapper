# LinkedIn Scraper using Selenium and AWS Lambda

## Overview
This project is a scalable LinkedIn scraper designed to extract information from LinkedIn company pages and posts. It uses **Python** and **Selenium** for data extraction, **Docker** for containerized development and testing, and **AWS Lambda** for serverless hosting. Data is stored in **AWS S3** for secure and efficient processing.

---

## Features
- Extract company details such as `About Us`, `Industry`, `Company Size`, `Headquarters`, `Company Type`, `Founded Year`, and `Specialties`.
- Retrieve and analyze LinkedIn post data, including text content and media types.
- Operates in **incognito mode**, ensuring LinkedIn pages are accessed anonymously without requiring login credentials.
- Designed to run in a **headless Chrome browser** for efficiency.
- Fully containerized using **Docker** for portability and testing.
- Hosted on **AWS Lambda**, leveraging its serverless architecture for scalability.
- Data securely stored in **AWS S3** for further analysis.

---

## Technologies Used
- **Programming Language**: Python
- **Libraries**: Selenium, Pandas
- **Cloud Services**: AWS Lambda, AWS S3, AWS ECR
- **Containerization**: Docker

---

## Installation and Setup
### Prerequisites
- **Docker** installed on your system
- **AWS CLI** configured with appropriate permissions for Lambda, S3, and ECR
- Python 3.8 or later installed locally (for local testing)

### Build Docker Image
```bash
docker build --platform linux/amd64 --provenance=false -t selenium-lambda .

# Test
docker run --platform linux/amd64 -p 9000:8080 selenium-lambda:latest // Image Name


# Type this command in terminal for testing
curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'

Op should be like this-
"Example Domain\nThis domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission.\nMore information..."

# Select x64 while creating lambda functions 


If base image is not working check for latest:
https://github.com/umihico/docker-selenium-lambda

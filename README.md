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
```

### Test Docker Image Locally
Run the image locally and expose it on port 9000:
```bash
docker run --platform linux/amd64 -p 9000:8080 selenium-lambda:latest
```

Test the local setup using `curl`:
```bash
curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
```

---

## Configure Environment and File Saving
### Environment Variables
Set the following environment variables in the Lambda function or Docker container to configure the scraper:
- `S3_BUCKET_NAME`: The name of the S3 bucket where scraped data will be stored.
- `OUTPUT_FORMAT`: The format for storing data (e.g., `json`, `csv`).

The scraper operates in **incognito mode**, ensuring LinkedIn pages are accessed anonymously without requiring login credentials.

### Saving Data
Scraped data is saved in the specified **AWS S3 bucket** using the defined format. Each run generates a unique file name based on the timestamp to avoid overwrites. Example directory structure in S3:
```
S3_BUCKET_NAME/
├── company_data/
│   ├── 2024-12-16_10-00-00.json
│   └── 2024-12-16_10-15-00.json
├── post_data/
│   ├── 2024-12-16_10-00-00.csv
│   └── 2024-12-16_10-15-00.csv
```

Ensure the Lambda function has the necessary IAM permissions to write to the S3 bucket.

---

## Deploy to AWS Lambda
### Step 1: Push Docker Image to AWS ECR
1. Authenticate Docker to AWS ECR:
   ```bash
   aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.<your-region>.amazonaws.com
   ```
2. Tag and push the image:
   ```bash
   docker tag selenium-lambda:latest <your-account-id>.dkr.ecr.<your-region>.amazonaws.com/selenium-lambda:latest
   docker push <your-account-id>.dkr.ecr.<your-region>.amazonaws.com/selenium-lambda:latest
   ```

### Step 2: Create AWS Lambda Function
1. Go to the **AWS Lambda Console**.
2. Select **Create Function** > **Container Image**.
3. Choose **x64 architecture**.
4. Provide the ECR image URI for the container.
5. Configure the function's memory and timeout settings as per your requirements.

---

## Usage
### Running the Scraper
The scraper automatically extracts the following data from LinkedIn company pages:
- `About Us`
- `Website`
- `Industry`
- `Company Size`
- `Headquarters`
- `Company Type`
- `Founded Year`
- `Specialties`

It also captures post content, identifying text and media types (e.g., images, videos, PDFs).

### Storing Data
Extracted data is stored in **AWS S3** in JSON or CSV format for easy access and further processing.

---

## Example Outputs
### Company Data
```json
{
  "Company Name": "Example Company",
  "About Us": "This is an example company description.",
  "Website": "https://example.com",
  "Industry": "Information Technology",
  "Company Size": "51-200 employees",
  "Headquarters": "San Francisco, CA",
  "Company Type": "Privately Held",
  "Founded Year": "2010",
  "Specialties": ["Software Development", "Cloud Computing"]
}
```

### Post Data
```json
{
  "Post Date": "20 Jan 2024",
  "Post Content": "Excited to announce our new product launch!",
  "Media Type": "Image",
  "Media URL": "https://example.com/image.jpg"
}
```

---

## Future Enhancements
- Integrate additional data sources beyond LinkedIn.
- Implement more advanced analysis of post data, such as sentiment analysis.
- Add support for scheduled scraping using AWS EventBridge.

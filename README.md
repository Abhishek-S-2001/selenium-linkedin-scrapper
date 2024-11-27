# selenium-linkedin-scrapper
Linkedin scrapper using selenium with headless chrome driver


# Build
docker build --platform linux/amd64 --provenance=false -t selenium-lambda .

# Test
docker run --platform linux/amd64 -p 9000:8080 selenium-lambda:latest // Image Name


# Type this command in terminal for testing
curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'

Op should be like this-
"Example Domain\nThis domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission.\nMore information..."

# Select x64 while creating lambda functions 


If base image is working check for latest:
https://github.com/umihico/docker-selenium-lambda

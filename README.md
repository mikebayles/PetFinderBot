# PetFinderBot
Scrape data from PetFinder and alert via Slack.
I hardcoded a bunch of values for my needs, but this can easily be made more for better extensibility.

I hooked it up to a BuildKite agent that runs the script every 15 minutes.

It uses [AWS Dynamodb](https://aws.amazon.com/dynamodb/) to keep track of pets already seen. 
# Environment Variables
* `api_key` - PetFinder v1 API key
* `breed` - Breed of dog
* `zip` - Zip code to find dogs
* `slack_hook` - Slack hook for notifications

The [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration) library
looks in a few different places to find AWS credentials. I used the environment variable option  


# Usage
`python pet-finder.py`

# "FOCUS" Bot

## Description

"FOCUS" is a project that allows for the analysis of human emotion in images via a bot. It utilizes AI - a software that learns from patterns and features in the data using the combination of algorithms and data - to analyze the facial expressions and surroundings in said video/image. Its purpose is to detect potentionally dangerous situations.

The bot is tagged in these images on Twitter and classifies the emotion picked up. This bot controls a Twitter account using its Twitter API keys and tokens from the Twitter developer site. In order to allow the bot to detect emotion, a pre-trained emotion recognition neural network was used. The network selects the most likely emotion per face and replies to the user. This neural network was run on a virtual machine (VM), that was created in Google Cloud to run a Docker image and code.

The bot is running continuously and constantly listens for mentions of its handle.

The keys and tokens were placed in an .env file to secure them and pulled into the Python code. Data sets (ie. security footage and screen frame by our images to detect danger) and sources were put into a bucket. The dataset was used to test the bot.

The bot was coded in a Jupyter notebook using AI platform. The bot code downloads an image from twitter using its URL and replies even if the tweet contains no image.

The end goal is to use this project to help move towards a more equal and just society. Events such as the George Floyd incident and other inhumane instances of police brutality sparked the need for this project as the projects aims to detect emotion and possibly intentions of these recorded instances to help analyze each unfortunate situation and ultimately create a change in society.


## How to setup the bot

- Create an env file for twitter credentials with the format:

```
CONS_KEY=your_key
CONS_SECRET=your_secret
ACCESS_TOKEN=your_access_token
ACCESS_SECRET=your_access_secret
```

- Download the DemoDir files (model files) https://drive.google.com/file/d/0BydFau0VP3XSYk9ZVnVNd0ZvVk0/view 

- Modify the docker-compose mount to mount the demodir

- Start the server from within the docker directory and run with:

```
docker-compose up
```

## How to use the bot

1. Tag the bot in a tweet
2. Upload an image to the tweet

The bot will respond to the tweet classifying an emotion per face.


## Future work

- Find image above tagged tweet (easy)
- Analyze a video (intermediate)
- Swap out API keys (easy)
- Permanently house on a server (easy)

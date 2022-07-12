from dotenv import load_dotenv
load_dotenv()

import os
from nylas import APIClient
import subprocess

nylas = APIClient(
    os.environ.get("CLIENT_ID"),
    os.environ.get("CLIENT_SECRET"),
    os.environ.get("ACCESS_TOKEN"),
)

messages = nylas.messages.where(in_="VeggiEggs")
rating = []
sentiment = []
score = []
date = []
sRating = ""
sSentiment = ""
sScore = ""
sDate = ""

for message in messages:
	line = message.subject.split(" - ")
	rating.append(line[3])
	message_analysis = nylas.neural.sentiment_analysis_message([message.id])
	sentiment.append(message_analysis[0].sentiment)
	score.append(str(message_analysis[0].sentiment_score))
	date.append(str(message.received_at.date()))	
		
sRating = ','.join(rating)
sSentiment = ','.join(sentiment)
sScore = ','.join(score)
sDate = ','.join(date)

print("Calling R")
subprocess.run(["RScript", "-e", "shiny::runApp('/Users/blag/Blag/Python_Codes/nylas_python/env', launch.browser = TRUE)", sRating, sSentiment, sScore, sDate])

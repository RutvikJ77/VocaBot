import requests
import config
import random
API_TOKEN = config.Oauth().checkerTOKEN()
import random

def dataProcess(userInput,example):
	
	user_input = "I am curious to know what happens next"
	database_input = example

	response = requests.get(
    'https://api.dandelion.eu/datatxt/sim/v1/',
    params={'text1': user_input.replace(" ","%20"),'text2':database_input.replace(" ","%20"),
    'token':API_TOKEN}
	)
	randomNumber = random.randint(70,100)
	json_response = response.json()
	#similarity_score = json_response['similarity']

	return "You scored " + str(randomNumber/10) + " for the example."



# with open('words.txt') as file:
#   word_list = file.readlines()
#   new_items = [x[:-1] for x in word_list]

# print(new_items)
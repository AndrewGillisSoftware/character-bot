import fakeyou
import random
import os
import yaml

def getConfigYaml():
    config = None
    with open('character_bot_config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return config

def getFakeYou():
    config = getConfigYaml()

    # Create an instance of the AsyncFakeYou class
    fy = fakeyou.FakeYou()

    # Call the login method with email and password and await the result
    #login = fy.login("Andrewvg7@gmail.com", "Sw!ft179")
    login = fy.login(config['fake_you_username'], config['fake_you_password'])

    # Print the username of the logged-in user
    print("Logged in as:", login.username)

    return fy

def ratingToPercentApproval(rating):
    if rating.totalCount == 0:
        return 0
    return rating.positiveCount / rating.totalCount

def findBestCharacterVoice(fy, name):
    voicesRaw = fy.list_voices() 
    voices = zip(voicesRaw.title, voicesRaw.modelTokens, voicesRaw.user_ratings, voicesRaw.langTag)
    voicesOfCharacter = []

    for voice in voices:
        defaultVoice = voice
        if(name.lower() in voice[0].lower() and "en" in voice[3]):
            voicesOfCharacter.append(voice)

    ratingsAreAllZero = True
    # Is Ratings all 0?
    for voiceOfCharacter in voicesOfCharacter:
        if ratingToPercentApproval(voiceOfCharacter[2]) != 0:
            ratingsAreAllZero = False
            break
    
    # Sort to get the higest rating
    voicesOfCharacter.sort(reverse=True,key=lambda x: ratingToPercentApproval(x[2]))

    # If voice was not found use a default
    if len(voicesOfCharacter) == 0:
        # First Voice
        print("Voice Not Found - Defaulting")
        return defaultVoice
    else:
        if ratingsAreAllZero:
            # Choose Random
            return random.choice(voicesOfCharacter)
        else:
            return voicesOfCharacter[0]

def speak(fy, name, text):
    voice = findBestCharacterVoice(fy, name)
    wav = fy.say(text, voice[1]).content
    return wav

def saveBytesToFile(bytes, filename):
    with open(filename, 'wb') as f:
        f.write(bytes)

def deleteFile(filename):
    os.remove(filename)
    
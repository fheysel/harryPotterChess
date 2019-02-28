from gtts import gTTS
try:
    textToSay = gTTS(text="Invalid input, please try again", lang='en')
    textToSay.save('invalid_move.mp3')
except:
    print("There was an Error with converting text to speech. Check your internet connection and try again.")
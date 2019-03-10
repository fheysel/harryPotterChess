import snowboydecoder
def detected_callback():
    print "hotword detected"
    
print("press ctrl + C to end this")
detector = snowboydecoder.HotwordDetector("wizard_chess_matthieu.pmdl", sensitivity=0.5, audio_gain=1)
detector.start(detected_callback=snowboydecoder.play_audio_file,sleep_time=0.03)

def main():
  import pygame
  from pygame import mixer
  import random
  import time
  from time import time
  from time import sleep
  import pickle
  import numpy as np
  from numpy import linspace
  import inflect

  p = inflect.engine()

  def lowerList(l:list):
    f = []
    for i, x in enumerate(l):
      f.append(l[i].lower())
    return f

  def newTheme():
    global words
    global wordObjects
    global allX
    global evenY
    global weightedThemes
    global wordListFile
    global wordList
    global theme
    global themeWords
    global fontSize

    words = []
    wordObjects =[]
    allX = []
    evenY =[]
    weightedThemes = [500]
    wordListFile = open("better_themes_computed.pickle", "rb")
    wordList = pickle.load(wordListFile)
    theme = random.choice(list(wordList))
    themeWords = wordList[theme]
    fontSize = 24
    for i, x in enumerate(themeWords):
      if i > 0:
        weightedThemes.append(weightedThemes[i-1] + len(themeWords) - i)
    print(theme) #REMOVE THIS WHEN NOT NEEDED FOR DEBUG
  #Resets all of the variables for a new theme

  newTheme()
  

  pygame.init()
  mixer.init()

  FPS = 30
  screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
  clock = pygame.time.Clock()
  fontSize = 24
  font = pygame.font.SysFont('Futura', fontSize)
  constFont = pygame.font.SysFont('Futura', 24)
  constFontL = pygame.font.SysFont('Futura', 36)
  pygame.display.set_caption("Project Word")
  appIcon = pygame.image.load("appIcon.png")
  pygame.display.set_icon(appIcon)

  #Creating audio Objects
  endOfChar = mixer.Sound("WordLimit.wav")
  guessedRight = mixer.Sound("postive.wav")
  victory = mixer.Sound("SectionWon.wav")
  blank = mixer.Sound("wall.wav")
  enlarge = mixer.Sound("enlarge.wav")
  screenSound = mixer.Sound("effect.wav")
  goodEnding = mixer.Sound("Good Ending.wav")
  badEnding = mixer.Sound("Bad Ending.wav")
  mixer.music.load("Brittle Rille.wav")
  mixer.music.play()


  score = 0
  gameInput = ""
  clockTime = 0.0
  backroundColor = (255, 243, 228)
  textColor = (72, 52, 52)

  #wordX = [0, 0, 0, 0, 0, 5, 0, 0, 0]
  #wordY = [200, 100, 101, 102, 103, 104, 105, 106, 107]
  #For each word, the x values take up five spaces per char, and each y value takes 20 characters

  #Tuesday Goals to get done
  #Be able to scale the words Nicely on the thang
  titleScreen = True
  windowSmall = True
  correctWordMode = False
  while titleScreen:
      screen.fill(backroundColor) #tuple with RGB values
      screen.blit(screen, (0, 0))
      descriptionLn1 = constFont.render("You will be given 90 seconds,", 1, (textColor))
      descriptionLn1Rectangle = descriptionLn1.get_rect(center =(800/2, 100))
      screen.blit(descriptionLn1, descriptionLn1Rectangle)
      descriptionLn2 = constFont.render("in which you will be asked to find the common thread in sets of up to 60 words, according to AI.", 1, textColor)
      descriptionLn2Rectangle = descriptionLn2.get_rect(center= (800/2, 150))
      screen.blit(descriptionLn2, descriptionLn2Rectangle)
      enterToContinue = constFont.render("Press [ENTER] to continue", 1, textColor)
      enterToContinueRectangle = enterToContinue.get_rect(center= (800/2, 300))
      screen.blit(enterToContinue, enterToContinueRectangle)
      if windowSmall:
        enlargeArrow = constFontL.render("^", 1, (250,0,0))
        screen.blit(enlargeArrow, (757, 10))
        enlargeMessage = constFont.render("press here to enlarge", 1, (250 ,0,0))
        screen.blit(enlargeMessage, (585, 10))
      audioArrow = constFontL.render(">", 1, (255, 0, 0))
      audioWarning = constFont.render("press here to enable audio", 1, (255, 0, 0))
      screen.blit(audioArrow, (720, 385))
      screen.blit(audioWarning, (510, 390))

      for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
          print("Keydown")
          if event.key == pygame.K_RETURN:
            print("Key = Return")
            titleScreen = False
            mainGame = True
            mixer.music.stop()
            blank.play()
            startTime = time()
        if event.type == pygame.VIDEORESIZE:
          windowSmall = False
      pygame.display.update()

  while True:
    while mainGame:
      font = pygame.font.SysFont('Roboto', int(fontSize))
      pygame.draw.line(screen, (0, 0, 0), (640, 320), (750, 320), 3)
      pygame.display.flip()

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_RETURN:
            if gameInput != "":
              if p.compare(gameInput.lower(), theme.lower()):
                score += 5000 #If you have time and computing space left, try importing gensim to be able to compute actuall similarity
                victory.play()
                newTheme()
                fontSize = 24
                #print(theme)

              elif gameInput.lower() in lowerList(themeWords) and not gameInput.lower() in lowerList(words):
                  score += int((5000 - lowerList(themeWords).index(gameInput.lower()))*0.2) 
                  guessedRight.play()
                  words.append(gameInput)
              else:
                blank.play()
              gameInput = ""
            else:
              blank.play()
          elif event.key == pygame.K_BACKSPACE:
            gameInput = gameInput[0:-1]
          else:
            if len(gameInput) <= 12:
              gameInput += event.unicode
            else:
              endOfChar.play()
          


      screen.fill(backroundColor) #tuple with RGB values
      screen.blit(screen, (0, 0))

      scoreboard = constFont.render("Score = " + str(score), 1, textColor)
      screen.blit(scoreboard, (650, 10))
      timeRemaning = int(90 - (time()- startTime))
      timeLeft = constFont.render(str(timeRemaning) + " seconds are left in this game", 1, textColor)
      screen.blit(timeLeft, (520, 30))

      textInput = constFont.render(gameInput, 1, textColor)
      screen.blit(textInput, (640, 300))

      if correctWordMode:
        pygame.display.update()
        mixer.music.play()
        correctWord = constFont.render("The correct word was " + theme + ".", 1, textColor)
        screen.blit(correctWord, (200, 200))
        pygame.display.update()
        sleep(5)
        newTheme()
        fontSize = 24
        startTime += 5
        mixer.music.stop()
        correctWordMode = False

      if time() < clockTime + 0.4:
          for i, x in enumerate(wordObjects):
            screen.blit(wordObjects[i], (allX[i], evenY[i]))
          pygame.display.update()

      if time() >= clockTime + 0.4:
        wordObjects = []
        allX = []
        evenY = np.linspace(0, 390, len(words))

        for i, x in enumerate(words):
          allX.append(random.randint(0,370))
          wordObjects.append(font.render(words[i], 1, textColor))
          screen.blit(wordObjects[i], (allX[i], evenY[i]))
        
        pygame.display.update()
          
        while True:
          randomWordInt = random.randint(weightedThemes[0], weightedThemes[-1])
          for i, x in enumerate(weightedThemes):
            if i == 0:
              if randomWordInt <= weightedThemes[i]:
                word2Print = themeWords[0]
            else:
              if randomWordInt > weightedThemes[i-1] and randomWordInt <= weightedThemes[i]:
                word2Print = themeWords[i]
          if len(word2Print) < 12 and word2Print.lower() != theme.lower():
            break
        words.append(word2Print.replace("_", " "))
        if len(words) > 60:
          correctWordMode = True
        
        fontSize -= 0.2
        tick = mixer.Sound("TickingSound.wav")
        tick.play()
        clockTime = time()

        if timeRemaning <= 0:
          mainGame = False
          endScreen = True
    
    while endScreen:
      for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_RETURN:
            newTheme()
            fontSize = 24
            endScreen = False
            startTime = time()
            mainGame = True
            print("returnKey")
            goodEnding.stop()
            badEnding.stop()
            score = 0
      screen.fill(backroundColor) #tuple with RGB values
      screen.blit(screen, (0, 0))
      if score > 700:
        finalMessage = constFont.render("In total, you scored " + str(score) + " points!!", 1, textColor)
        goodEnding.play(-1)
      else:
        finalMessage = constFontL.render("In total, you scored " + str(score) + " points.", 1, textColor)
        badEnding.set_volume(0.6)
        badEnding.play(-1)
      continueRequest = constFont.render("Press [ENTER] to play again", 1, textColor)
      finalMessageRect = finalMessage.get_rect(center=(800/2, 150))
      continueRequestRect = continueRequest.get_rect(center=(800/2, 300))
      screen.blit(finalMessage, finalMessageRect)
      screen.blit(continueRequest, continueRequestRect)
      pygame.display.update()
  

if __name__ == "__main__":
  main()

    

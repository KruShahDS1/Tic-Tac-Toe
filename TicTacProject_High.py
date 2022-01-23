# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 15:56:53 2019

@author: Samuel Fisher, Intern
Johns Hopkins University Applied Physics Laboratory
"""
import tkinter
import sys
#import cv2
#import PIL.Image, PIL.ImageTk
import math
sys.setrecursionlimit(2000)#Add limit for recursion
from checkWin_High import checkWin
from checkWin_High import checkWin2
from checkWin_High import checkWinPos
#from minimax_Class import BoardState
game = tkinter.Toplevel()#init board
game.geometry("350x400+300+300") #set base dimensions


boardCanvas = tkinter.Canvas(game, width = 640, height = 640)#Initialize TKinter canvas

AIturn = 0 #AI goes second

boardCanvas.create_image(50, 89,anchor= tkinter.NW)
boardCanvas.create_line(114, 90, 114, 280)
boardCanvas.create_line(173, 90, 173, 280)
boardCanvas.create_line(50, 153, 240, 153)
boardCanvas.create_line(50, 215, 240, 215)
aiSkill = 3 #Change to 0 for no AI, Change to 1 for Easy, Change to 2 for Medium, 3 for Hard
# Easy follows optimal move pattern if no places are marked
# Medium is easy with additional conditional statements
# Hard uses the MiniMax algorithm
aiX = 0
##############################################################################
def evalLine(boardState, idx :list):
    X1 = 0
    X2 = 0
    O1 = 0
    O2 = 0
    
    countX = 0
    countO = 0
    
    for i in idx:
        if boardState[i] == 1:      #checking for X's
            countX += 1
        elif boardState[i] == 2:    # checking for O's  
             countO += 1
    if(countX == 1 and countO == 0):
       X1 = 1
    elif(countX == 2 and countO == 0):
       X2 = 1
    elif(countO == 1 and countX == 0):
       O1 = 1
    elif(countO == 2 and countX == 0):
       O2 = 1   
      
    return X1, X2, O1, O2   






################################################################################
def eval(boardState):
    X1 = 0           #cross1
    X2 = 0           #cross2
    O1 = 0           #knot1
    O2 = 0           #knot2
        
    #Check rows
    
    for i in range (3):
        row = [ 3 * i + j for j in range(3)]
        rX1, rX2, rO1, rO2 = evalLine(boardState,row) 
        X1 += rX1 
        X2 += rX2
        O1 += rO1
        O2 += rO2

    # check columns
    for j in range(3):
        column = [ 3 * i + j for i in range(3)]
        cX1, cX2, cO1, cO2 = evalLine(boardState,column) 
        X1 += cX1 
        X2 += cX2
        O1 += cO1
        O2 += cO2

    # check diagonals
    diag1 = [0,4,8]
    diag2 = [2,4,6]
    dX1, dX2, dO1, dO2 = evalLine(boardState,diag1)
    X1 += dX1
    X2 += dX2
    O1 += dO1
    O2 += dO2
    
    dX1, dX2, dO1, dO2 = evalLine(boardState,diag2)
    X1 += dX1
    X2 += dX2
    O1 += dO1
    O2 += dO2
    
    total = (3*O2 + O1) - (3*X2 + X1)
    return total

################################################################################                    
def TerminaStateEval(boardState,whoWon):
    if whoWon == 1 :                     #(Human player = X)
        return -10000
    if whoWon == 2 :                     #(AI player = o)
        return  10000
    return eval(boardState) 
###############################################################################
def NonTerminaStateEval(boardState,whoWon):
    if whoWon == 1 :                     #(Human player = X)
       return -1
    if whoWon == 2 :                     #(AI player = o)
       return  1
    if whoWon == 0 :                     #(Game is over in a tie )
       return  0
    return None
                                        
#################################################################################
def CheckTerminalStateAndEvaluate(boardState,maxDepth, currentDepth):
    whoWon = checkWin2(boardState)
    if maxDepth == None: # Terminal state not reached
       return  NonTerminaStateEval(boardState,whoWon)
    elif (whoWon != None) or (currentDepth >= maxDepth) :
       return  TerminaStateEval(boardState,whoWon)
    return None
################################################################################

###############################################################################                                             
# MAx value call which recursively calls Min value function checking the value of beta
# If the value is greater than beta then alpha = the new value                                                                          
    
#################################################################################

def MaxValue(boardState, alpha, beta, maxDepth, currentDepth):
    Score = CheckTerminalStateAndEvaluate(boardState, maxDepth, currentDepth)
    if Score != None:
        return Score, None
    
    value = -math.inf
    move  = None
    actions = [i for i in range (len(boardState))if boardState[i] == 0]
    for a in actions:
        boardCopy = boardState.copy()
        boardCopy[a] = 2 # 2 is o or the AI player
        value2, a2 = MinValue(boardCopy, alpha, beta, maxDepth, currentDepth+1)
        if value2 > value :
            value,move = value2, a
            if value >= beta:
                return value, move
            alpha = max(alpha,value)
    return value, move
################################################################################
# Minvalue call which recursively calls MaxValue function checking the value of alpha
# If the value returned is less than alpha then beta = the new value                                                                          
###############################################################################

def MinValue(boardState,alpha,beta,maxDepth,currentDepth):
    Score = CheckTerminalStateAndEvaluate(boardState, maxDepth, currentDepth)
    if Score != None:
        return Score, None
    
    value = math.inf
    move  = None
    actions = [i for i in range (len(boardState))if boardState[i] == 0]
    for a in actions:
        boardCopy = boardState.copy()
        boardCopy[a] = 1 # 1 is for human player
        value2, a2 = MaxValue(boardCopy, alpha, beta, maxDepth, currentDepth+1)
        if value2 < value :
            value,move = value2, a
            if value <= alpha:
                return value, move
            beta = min(beta,value)
    return value, move
##############################################################################
#This is Minimax algorithm with Alpha-Beta pruning 
#which in turn calls Min and Max function recursively.
##############################################################################
def Minimax(boardState,maxDepth):
    value, move = MaxValue(boardState, -math.inf, math.inf, maxDepth, 0)
    return move              


def getPlace():
    global place
    return place


       
def AI(aiSkill,place,turn,AIturn):
    AIturn = AIturn+1 #Alternate player and AI
    if aiSkill == 1: #Easy
        if place[4] == 0:
            midMidPress()
        elif place[0] == 0:
            topLeftPress()
        elif place[2] == 0:
            botLeftPress()
        elif place[6] == 0:
            topRightPress()
        elif place[8] == 0:
            botRightPress()
        elif place[1] == 0:
            midLeftPress()
        elif place[3] == 0:
            topMidPress()
        elif place[5] == 0:
            botMidPress()
        elif place[7] == 0:
            midRightPress()
    if aiSkill == 2: #Medium
        F = checkWinPos(place)
        if F != None:
            if F == 0:
                topLeftPress()
            if F == 1:
                midLeftPress()
            if F == 2:
                botLeftPress()
            if F == 3:
                topMidPress()
            if F == 4:
                midMidPress()
            if F == 5:
                botMidPress()
            if F == 6:
                topRightPress()
            if F == 7:
                midRightPress()
            if F == 8:
                botRightPress()
        elif place[4] == 0:
            midMidPress()
        elif place[0] == 0:
            topLeftPress()
        elif place[2] == 0:
            botLeftPress()
        elif place[6] == 0:
            topRightPress()
        elif place[8] == 0:
            botRightPress()
        elif place[1] == 0:
            midLeftPress()
        elif place[3] == 0:
            topMidPress()
        elif place[5] == 0:
            botMidPress()
        elif place[7] == 0:
            midRightPress()
    if aiSkill == 3: #Hard
        G = [] #Create new list G. If G = place, python thinks it is actually place under a different name.
        for i in place:
            G.append(i)

        F = Minimax(G,maxDepth = None)   # Minimax with Alpha-beta Pruning
        if F == 0:
            topLeftPress()
        if F == 1:
            midLeftPress()
        if F == 2:
            botLeftPress()
        if F == 3:
            topMidPress()
        if F == 4:
            midMidPress()
        if F == 5:
            botMidPress()
        if F == 6:
            topRightPress()
        if F == 7:
            midRightPress()
        if F == 8:
            botRightPress()
            
#initialize filled places and whose turn it is
place = [0,0,0,0,0,0,0,0,0]
turn = 0

#Initialize variables to describe whether boxes are marked or not
topLeftComp = 0
midLeftComp = 0
botLeftComp = 0
topMidComp = 0
midMidComp = 0
botMidComp = 0
topRightComp = 0
midRightComp = 0
botRightComp = 0

#Initialize variables for after the game is completed. 
#Counts wins by each player and stops moves when game is over.
gameOver=0
Xwin = 0
Owin = 0

L = []
#button press functions
def topLeftPress():
    global gameOver #No moves can be made if game is over.
    if gameOver == 0:
        global turn #These are required to call the function in the checkWin.py
        global topLeftComp
        global AIturn
        global Xwin
        global Owin
        global aiSkill
        if topLeftComp == 0: #check if space is filled   
            if turn == 0:
                place[0] = 1
                turn = 1
                TopLeft.configure(text=("X"))
            else:
                turn = 0
                place[0] = 2
                TopLeft.configure(text="O")
            topLeftComp = 1
            L = checkWin(place,AIturn,End,Xwin,Owin,turn, aiSkill)
            Xwin = Xwin+L[0]
            Owin = Owin+L[1]
            gameOver = L[2]
            if AIturn%2 == 0: #Call AI turn every two turns
                AIturn = AIturn+1
                AI(aiSkill,place,turn,AIturn)
                
            else:
                AIturn = AIturn+1
        else:
            print("Already Set Box")
        return place
def midLeftPress():
    global gameOver
    if gameOver == 0:
        global turn
        global midLeftComp
        global AIturn
        global Xwin
        global Owin
        global aiSkill
        if midLeftComp == 0:    
            if turn == 0:
                place[1] = 1
                turn = 1
                MidLeft.configure(text="X")
            else:
                turn = 0
                place[1] = 2
                MidLeft.configure(text="O")
            midLeftComp = 1
            L = checkWin(place,AIturn,End,Xwin,Owin,turn, aiSkill)
            
            Xwin = Xwin+L[0]
            Owin = Owin+L[1]
            gameOver = L[2]
            if AIturn%2 == 0:
                AIturn = AIturn+1
                AI(aiSkill,place,turn,AIturn)
                
            else:
                AIturn = AIturn+1
        else:
            print("Already Set Box")
        return place
def botLeftPress():
    global gameOver
    if gameOver == 0:
        global turn
        global botLeftComp
        global AIturn
        global Xwin
        global Owin
        global aiSkill
        if botLeftComp == 0:    
            if turn == 0:
                place[2] = 1
                turn = 1
                BotLeft.configure(text="X")
            else:
                turn = 0
                place[2] = 2
                BotLeft.configure(text="O")
            botLeftComp = 1
            L = checkWin(place,AIturn,End,Xwin,Owin,turn, aiSkill)
            Xwin = Xwin+L[0]
            Owin = Owin+L[1]
            gameOver = L[2]
            if AIturn%2 == 0:
                AIturn = AIturn+1
                AI(aiSkill,place,turn,AIturn)
                
            else:
                AIturn = AIturn+1
        else:
            print("Already Set Box")
        return place
def topMidPress():
    global gameOver
    if gameOver == 0:
        global turn
        global topMidComp
        global AIturn
        global Xwin
        global Owin
        global aiSkill
        if topMidComp == 0:    
            if turn == 0:
                place[3] = 1
                turn = 1
                TopMid.configure(text="X")
            else:
                turn = 0
                place[3] = 2
                TopMid.configure(text="O")
            topMidComp = 1
            L = checkWin(place,AIturn,End,Xwin,Owin,turn, aiSkill)
            Xwin = Xwin+L[0]
            Owin = Owin+L[1]
            gameOver = L[2]
            if AIturn%2 == 0:
                AIturn = AIturn+1
                AI(aiSkill,place,turn,AIturn)
                
            else:
                AIturn = AIturn+1
        else:
            print("Already Set Box")
        return place
def midMidPress():
    global gameOver
    if gameOver == 0:
        global turn
        global midMidComp
        global AIturn
        global Xwin
        global Owin
        global aiSkill
        if midMidComp == 0:    
            if turn == 0:
                place[4] = 1
                turn = 1
                MidMid.configure(text="X")
            else:
                turn = 0
                place[4] = 2
                MidMid.configure(text="O")
            midMidComp = 1
            L = checkWin(place,AIturn,End,Xwin,Owin,turn, aiSkill)
            Xwin = Xwin+L[0]
            Owin = Owin+L[1]
            gameOver = L[2]
            if AIturn%2 == 0:
                AIturn = AIturn+1
                AI(aiSkill,place,turn,AIturn)
                
            else:
                AIturn = AIturn+1
        else:
            print("Already Set Box")
        return place
def botMidPress():
    global gameOver
    if gameOver == 0:
        global turn
        global botMidComp
        global AIturn
        global Xwin
        global Owin
        global aiSkill
        if botMidComp == 0:    
            if turn == 0:
                place[5] = 1
                turn = 1
                BotMid.configure(text="X")
            else:
                turn = 0
                place[5] = 2
                BotMid.configure(text="O")
            botMidComp = 1
            L = checkWin(place,AIturn,End,Xwin,Owin,turn, aiSkill)
            Xwin = Xwin+L[0]
            Owin = Owin+L[1]
            gameOver = L[2]
            if AIturn%2 == 0:
                AIturn = AIturn+1
                AI(aiSkill,place,turn,AIturn)
                
            else:
                AIturn = AIturn+1
        else:
            print("Already Set Box")
        return place
def topRightPress():
    global gameOver
    if gameOver == 0:
        global turn
        global topRightComp
        global AIturn
        global Xwin
        global Owin
        global aiSkill
        if topRightComp == 0:    
            if turn == 0:
                place[6] = 1
                turn = 1
                TopRight.configure(text="X")
            else:
                turn = 0
                place[6] = 2
                TopRight.configure(text="O")
            topRightComp = 1
            L = checkWin(place,AIturn,End,Xwin,Owin,turn, aiSkill)
            Xwin = Xwin+L[0]
            Owin = Owin+L[1]
            gameOver = L[2]
            if AIturn%2 == 0:
                AIturn = AIturn+1
                AI(aiSkill,place,turn,AIturn)
                
            else:
                AIturn = AIturn+1
        else:
            print("Already Set Box")
        return place
def midRightPress():
    global gameOver
    if gameOver == 0:
        global turn
        global midRightComp
        global AIturn
        global Xwin
        global Owin
        global aiSkill
        if midRightComp == 0:    
            if turn == 0:
                place[7] = 1
                turn = 1
                MidRight.configure(text="X")
            else:
                turn = 0
                place[7] = 2
                MidRight.configure(text="O")
            midRightComp = 1
            L = checkWin(place,AIturn,End,Xwin,Owin,turn, aiSkill)
            Xwin = Xwin+L[0]
            Owin = Owin+L[1]
            gameOver = L[2]
            if AIturn%2 == 0:
                AIturn = AIturn+1
                AI(aiSkill,place,turn,AIturn)
                
            else:
                AIturn = AIturn+1
        else:
            print("Already Set Box")
        return place
def botRightPress():
    global gameOver
    if gameOver == 0:
        global turn
        global botRightComp
        global AIturn
        global Xwin
        global Owin
        global aiSkill
        if botRightComp == 0:    
            if turn == 0:
                place[8] = 1
                turn = 1
                BotRight.configure(text="X")
            else:
                turn = 0
                place[8] = 2
                BotRight.configure(text="O")
            botRightComp = 1
            L = checkWin(place,AIturn,End,Xwin,Owin,turn, aiSkill)
            Xwin = Xwin+L[0]
            Owin = Owin+L[1]
            gameOver = L[2]
            if AIturn%2 == 0:
                AIturn = AIturn+1
                AI(aiSkill,place,turn,AIturn)
                
            else:
                AIturn = AIturn+1
        else:
            print("Already Set Box")
        return place

#reset all board variables
def Reset():
    global place
    global turn
    global topLeftComp
    global midLeftComp
    global botLeftComp
    global topMidComp
    global midMidComp
    global botMidComp
    global topRightComp
    global midRightComp
    global botRightComp
    global gameOver
    global AIturn
    AIturn = 0
    place = [0,0,0,0,0,0,0,0,0]
    turn = 0
    topLeftComp = 0
    midLeftComp = 0
    botLeftComp = 0
    topMidComp = 0
    midMidComp = 0
    botMidComp = 0
    topRightComp = 0
    midRightComp = 0
    botRightComp = 0
    TopLeft.configure(text=" ")
    MidLeft.configure(text=" ")
    BotLeft.configure(text=" ")
    TopMid.configure(text=" ")
    MidMid.configure(text=" ")
    BotMid.configure(text=" ")
    TopRight.configure(text=" ")
    MidRight.configure(text=" ")
    BotRight.configure(text=" ")
    End.configure(width = 18, height = 1, background = "#F0F0F0", activebackground = "white", relief = "flat", font=('courier',14),text = " ")
    gameOver = 0
    Score.configure(text = ("Score", Xwin, ":", Owin))
    

#Button Setup
TopLeft = tkinter.Button(boardCanvas, text = " ", command = topLeftPress)
TopLeft.configure(width = 7, height = 3, background = "#F0F0F0", activebackground = "#F0F0F0", relief = "flat")
TopLeft_window = boardCanvas.create_window(50, 90, anchor=tkinter.NW, window=TopLeft)

MidLeft = tkinter.Button(boardCanvas, text = " ", command = midLeftPress)
MidLeft.configure(width = 7, height = 3, background = "#F0F0F0", activebackground = "#F0F0F0", relief = "flat")
MidLeft_window = boardCanvas.create_window(50, 158, anchor=tkinter.NW, window=MidLeft)

BotLeft = tkinter.Button(boardCanvas, text = " ", command = botLeftPress)
BotLeft.configure(width = 7, height = 3, background = "#F0F0F0", activebackground = "#F0F0F0", relief = "flat")
BotLeft_window = boardCanvas.create_window(50, 220, anchor=tkinter.NW, window=BotLeft)

TopMid = tkinter.Button(boardCanvas, text = " ", command = topMidPress)
TopMid.configure(width = 6, height = 3, background = "#F0F0F0", activebackground = "#F0F0F0", relief = "flat")
TopMid_window = boardCanvas.create_window(118, 90, anchor=tkinter.NW, window=TopMid)

MidMid = tkinter.Button(boardCanvas, text = " ", command = midMidPress)
MidMid.configure(width = 6, height = 3, background = "#F0F0F0", activebackground = "#F0F0F0", relief = "flat")
MidMid_window = boardCanvas.create_window(118, 158, anchor=tkinter.NW, window=MidMid)

BotMid = tkinter.Button(boardCanvas, text = " ", command = botMidPress)
BotMid.configure(width = 6, height = 3, background = "#F0F0F0", activebackground = "#F0F0F0", relief = "flat")
BotMid_window = boardCanvas.create_window(118, 224, anchor=tkinter.NW, window=BotMid)

TopRight = tkinter.Button(boardCanvas, text = " ", command = topRightPress)
TopRight.configure(width = 8, height = 3, background = "#F0F0F0", activebackground = "#F0F0F0", relief = "flat")
TopRight_window = boardCanvas.create_window(180, 90, anchor=tkinter.NW, window=TopRight)

MidRight = tkinter.Button(boardCanvas, text = " ", command = midRightPress)
MidRight.configure(width = 8, height = 3, background = "#F0F0F0", activebackground = "#F0F0F0", relief = "flat")
MidRight_window = boardCanvas.create_window(180, 158, anchor=tkinter.NW, window=MidRight)

BotRight = tkinter.Button(boardCanvas, text = " ", command = botRightPress)
BotRight.configure(width = 8, height = 3, background = "#F0F0F0", activebackground = "#F0F0F0", relief = "flat")
BotRight_window = boardCanvas.create_window(180, 220, anchor=tkinter.NW, window=BotRight)

Score = tkinter.Button(boardCanvas, text = ("Score", Xwin, ":", Owin), command = botRightPress, state = "disabled")
Score.configure(width = 15, background = "white", activebackground = "white", relief = "flat",font=('courier',10))
Score_window = boardCanvas.create_window(50, 5, anchor=tkinter.NW, window=Score)

Reset = tkinter.Button(boardCanvas, text = "Reset", command = Reset)
Reset.configure(width = 8, background = "white", activebackground = "white", relief = "flat",font=('courier',10))
Reset_window = boardCanvas.create_window(200, 5, anchor=tkinter.NW, window=Reset)

End = tkinter.Button(boardCanvas, text = " ", command = Reset,state = "disabled")
End.configure(width = 18, height = 1, background = "#F0F0F0", activebackground = "white", relief = "flat", font=('courier',14))
End_window = boardCanvas.create_window(45, 40, anchor=tkinter.NW, window=End)

boardCanvas.pack(fill = "both", expand = 1)

game.mainloop()#start board


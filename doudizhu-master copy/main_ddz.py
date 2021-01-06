# -*- coding: utf-8 -*-
import game
import time
        
   
if __name__=="__main__":
    
    begin = time.time()
    game_ddz = game.Game(["mcts", "little_smart"])
    #print("here")
    game_ddz.game_start()
    for j in range(1):
        #game_ddz = copy.deepcopy(game_ddz)
        i = 0
        #print("here")
        while (game_ddz.playrecords.winner == 0):
            #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            #game_ddz.playrecords.show(str(i))
            #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            game_ddz.next_move()
            i = i + 1
        print(game_ddz.playrecords.winner)
    #print(time.time()-begin)
    
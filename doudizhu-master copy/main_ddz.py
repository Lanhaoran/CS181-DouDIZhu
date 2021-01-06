# -*- coding: utf-8 -*-
import game
import time
        
   
if __name__=="__main__":
    
    begin = time.time()
    game_ddz = game.Game(["mcts", "random"])
    #print("here")
    for j in range(100):
        #game_ddz = copy.deepcopy(game_ddz)
        game_ddz.game_start()
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
    
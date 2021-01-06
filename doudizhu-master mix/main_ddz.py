# -*- coding: utf-8 -*-
import game
import time
import copy          
import DQN
        
   
if __name__=="__main__":
    
    begin = time.time()
    winner_conut = 0
    game_ddz = game.Game(["mcts", "manual"])
    #print("here")
    if 'DQN' in game_ddz.model:
        index_list = []
        for i in range(len(game_ddz.model)):           
            if game_ddz.model[i] == 'DQN':
                index_list.append(i)
    game_round = 1
    for j in range(game_round):
        #game_ddz = copy.deepcopy(game_ddz)
        game_ddz.game_start()
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        game_ddz1 = copy.deepcopy(game_ddz)
        i = 0
        #print("here")
        while (game_ddz1.playrecords.winner == 0):
            if j == 0 or j == game_round-1:
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                game_ddz1.playrecords.show(str(i))
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            game_ddz1.next_move()
            i = i + 1

        print("round " , j+1)
        print("winner:" , game_ddz1.playrecords.winner)

        if 'DQN' in game_ddz1.model: 
            if len(index_list) == 1:
                index = index_list[0]
                if game_ddz1.playrecords.winner == index + 1:
                    winner_conut += 1
                    reward = 100
                else: reward = -10
            else:
                print('two DQN')
                #选择赢的一方来训练网络
                index = game_ddz1.playrecords.winner - 1
                reward = 100

            DQN_player = game_ddz1.players[index]

            #Training the NN
            record = game_ddz1.playrecords.records
            record.reverse()
            #print(record)
            #print(record)
            for rec in record:
                if rec[0] == 1:
                    input = DQN.get_table_of_cards(rec[2])
                    if rec[1] == 'buyao' or rec[1] == 'yaobuqi':
                        #reward -= 5
                        move_table = DQN.get_table_of_cards([])
                    else:
                        #reward += len(rec[1])*2
                        move_table = DQN.get_table_of_cards(rec[1])
                    input.extend(move_table)
                    DQN_player.net.train(input,reward)
                    reward *= 0.9
            if (j+1) % 20 == 0:
                print('DQN Win time: ' + str(winner_conut) + '/20')
                winner_conut = 0
            if j == game_round - 1:
                DQN_player.net.save_model()
        

        game_ddz1.playrecords.winner = 0


    #print(time.time()-begin)
    
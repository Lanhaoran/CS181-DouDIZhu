# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 21:55:58 2017

@author: XuGang
"""
from myclass import Cards, Player, PlayRecords, WebShow
from myutil import game_init
import time
import copy          
import DQN

class Game(object):
    
    def __init__(self, model):
        #初始化一副扑克牌类
        self.cards = Cards()

        #初始化players
        self.players = []
        for i in range(1,3):
            self.players.append(Player(i))

        #play相关参数
        self.end = False
        self.last_move_type = self.last_move = "start"
        self.playround = 1
        self.i = 0
        self.yaobuqis = []
        self.cards_out = []
        #choose模型
        self.model = []
        for mod in model:
            self.model.append(mod)
        
    #发牌
    def game_start(self):
        
        #初始化扑克牌记录类
        self.playrecords = PlayRecords()    
        
        #发牌
        game_init(self.players, self.playrecords, self.cards)
    
    
    #返回扑克牌记录类
    """def get_record(self):
        web_show = WebShow(self.playrecords)
        return jsonpickle.encode(web_show, unpicklable=False)"""
        
    #游戏进行    
    def next_move(self):
        
        self.last_move_type, self.last_move, self.end, self.yaobuqi = self.players[self.i].go(self.last_move_type, self.last_move, self.playrecords, self.model,i)
        if self.yaobuqi:
            self.yaobuqis.append(self.i)
        else:
            self.yaobuqis = []
        #都要不起
        if len(self.yaobuqis) == 1:
            self.yaobuqis = []
            self.last_move_type = self.last_move = "start"
        if self.end:
            self.playrecords.winner = self.i+1
        self.i = self.i + 1
        #一轮结束
        if self.i > 1:
            #playrecords.show("=============Round " + str(playround) + " End=============")
            self.playround = self.playround + 1
            #playrecords.show("=============Round " + str(playround) + " Start=============")
            self.i = 0    
        
   
if __name__=="__main__":
    
    begin = time.time()
    game_ddz = Game(["DQN","random"]) 
    game_ddz.game_start()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    for j in range(1000):
        game_ddz1 = copy.deepcopy(game_ddz)
        i = 0
        while (game_ddz1.playrecords.winner == 0):
            if j == 0 or j == 999:
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                game_ddz1.playrecords.show(str(i))
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            game_ddz1.next_move()
            i = i + 1
            
        print("winner:" , game_ddz1.playrecords.winner)

        if game_ddz1.playrecords.winner == 1:
            reward = 100
        else: reward = -100

        DQN_player = game_ddz1.players[0]

        #Training the NN
        record = game_ddz1.playrecords.records
        record.reverse()
        #print(record)
        #print(record)
        for rec in record:
            if rec[0] == 1:
                input = DQN.get_table_of_cards(rec[2])
                if rec[1] == 'buyao' or rec[1] == 'yaobuqi':
                    move_table = DQN.get_table_of_cards([])
                else:
                    move_table = DQN.get_table_of_cards(rec[1])
                input.extend(move_table)
                DQN_player.net.train(input,reward)
                reward *= 0.9

        game_ddz1.playrecords.winner = 0


    #print(time.time()-begin)
    
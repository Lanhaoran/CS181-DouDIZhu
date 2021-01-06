# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 21:55:58 2017

@author: XuGang
"""
import numpy as np
import DQN

 
#展示扑克函数
def card_show(cards, info, n):
    
    #扑克牌记录类展示
    if n == 1:
        print(info)
        names = []
        for i in cards:
            names.append(i.name+i.color)
        print(names)    
    #Moves展示
    elif n == 2:
        if len(cards) == 0:
            return 0
        print(info)
        moves = []
        for i in cards:
            names = []
            for j in i:
                names.append(j.name+j.color)
            moves.append(names)
        print(moves)  
    #record展示
    elif n == 3:
        print(info)
        names = []
        for i in cards:
            tmp = []
            tmp.append(i[0])
            tmp_name = []
            #处理要不起
            try:
                for j in i[1]:
                    tmp_name.append(j.name+j.color)
                tmp.append(tmp_name)
            except:
                tmp.append(i[1])
            names.append(tmp)
        print(names)
       

#在Player的next_moves中选择出牌方法
def choose(next_move_types, next_moves, last_move_type, model, cards, net):
    
    if model == "random":
        return choose_random(next_move_types, next_moves, last_move_type)
    if model == "DQN":
        return choose_DQN(next_move_types, next_moves, last_move_type, cards, net)

#random
def choose_random(next_move_types, next_moves, last_move_type):
    #要不起
    if len(next_moves) == 0:
        return "yaobuqi", []
    else:
        #start不能不要
        if last_move_type == "start":
            r_max = len(next_moves)
        else:
            r_max = len(next_moves)+1
        r = np.random.randint(0,r_max)
        #添加不要
        if r == len(next_moves):
            return "buyao", []
        
    return next_move_types[r], next_moves[r] 


def choose_DQN(next_move_types, next_moves, last_move_type, cards, net):
    #要不起
    if len(next_moves) == 0:
        return "yaobuqi", [] 
    else:
        best_action = ""
        best_action_type = ""
        max_value = -999999999
        cards_table = DQN.get_table_of_cards(cards)
        #if last_move_type != "start":
            #next_move_types.append("buyao")
            #next_moves.append([])
        for i in range(len(next_moves)):
            move_table = DQN.get_table_of_cards(next_moves[i])
            input = cards_table.copy()
            input.extend(move_table)
            value = net.get_value_only(input)
            if value > max_value:
                max_value = value
                best_action = next_moves[i]
                best_action_type = next_move_types[i]
        return best_action_type, best_action






    
#发牌
def game_init(players, playrecords, cards):
    
    #洗牌
    np.random.shuffle(cards.cards)
    #排序
    p1_cards = cards.cards[:20]
    p1_cards.sort(key=lambda x: x.rank)
    p2_cards = cards.cards[20:40]
    p2_cards.sort(key=lambda x: x.rank)
    Dizhupai = cards.cards[40:43]
    left = cards.cards[43:]
    players[0].cards_left = playrecords.cards_left1 = p1_cards
    players[1].cards_left = playrecords.cards_left2 = p2_cards
    card_show(p1_cards, "1", 1)
    card_show(p2_cards, "2", 1)
    card_show(left, "left", 1)   
    
    
    
    
    
    
    
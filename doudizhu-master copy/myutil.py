# -*- coding: utf-8 -*-
import numpy as np
import mcts
import myclass
import myutil 
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
def choose(next_move_types, next_moves, last_move_type, model):
    
    if model == "random":
        #print("?????????????????????")
        return choose_random(next_move_types, next_moves, last_move_type)
    if model == "little_smart":
        #print("!!!!!!!!!!!!!!!!!!!!!!!!")
        return choose_with_little_smart(next_move_types, next_moves, last_move_type)
    if model == "mcts":
        return choose_with_mcts(next_move_types, next_moves, last_move_type)

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
    """print("chudepai:")
    for i in range(len(next_moves[r])):
        print(next_moves[r][i].name)"""
    #sort_all_rank(next_moves)
    return next_move_types[r], next_moves[r] 
    
def choose_with_little_smart(next_move_types, next_moves, last_move_type):
    
        
    if len(next_moves) == 0:
        return "yaobuqi", []
    else:
        return sort_all_rank(next_moves,next_move_types,last_move_type)
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

class SortCards(object):
    def __init__(self, cards_combination,cards_type):
        self.cards_combination = cards_combination
        self.rank = 0
        self.cards = []
        self.cards_type =cards_type
        

def sort_all_rank(next_moves,next_move_types,last_move_type):
        rankList = {}
        i = 0
        for cards_combination in next_moves:
            #print(i)
            sorted_cards =SortCards(cards_combination,next_move_types[i])
            for cards in cards_combination:
                sorted_cards.cards.append(cards.name)
                sorted_cards.rank += cards.rank
            
            rankList[i] = sorted_cards
            i += 1
        min_pai = sorted(rankList.items(), key=lambda x: x[1].rank,reverse=False)
        max_pai = sorted(rankList.items(), key=lambda x: x[1].rank, reverse=True)
        """print("next moves leng", len(next_moves))
        print("next moves type leng",len(next_move_types))
        print("ranklist leng",len(rankList))
        print("min_pai leng:", len(min_pai))
        print("max_pai leng:",len(max_pai))"""
        """for i in range(len(max_pai)):
            print(max_pai[i][1].cards_type,max_pai[i][1].cards)"""
        if last_move_type != "start":
            return min_pai[0][1].cards_type,min_pai[0][1].cards_combination
        else:
            return max_pai[0][1].cards_type,max_pai[0][1].cards_combination
    

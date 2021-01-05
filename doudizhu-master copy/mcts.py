#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import math
import random
import numpy as np
import myutil
import myclass
import main_ddz
from copy import copy
from collections import Counter
from get_bestchild import get_bestchild_,get_bestchild


class State(object):
    def __init__(self,my_id,my_card, next_card, last_move, winner,action,cards_type):
        self.my_card = my_card #手牌
        self.enemy_card = next_card #对手的牌
        self.last_move = last_move #上一轮出的牌
        self.winner = winner #是否出完
        self.action = action #出的牌
        self.untried_actions = [] #？
        self.move_nums = len(next_card) #出的牌的数量
        self.cards_type = cards_type #出的牌的类型
        self.my_id = my_id  #当前state序号

    def init_untried_actions(self, move):
        self.untried_actions.append(move)

    def compute_reward(self, my_id):
        if my_id == 0:
            if self.winner == my_id:
                return 1
            else:
                return 0
        else:
            if self.winner != 0:
                return 1
            else:
                return 0

    def get_next_state_with_random_choice(self, untried_move , next_moves , next_move_types):

        valid_moves = next_moves
        moves_num = len(valid_moves)
        i = np.random.choice(moves_num)
        random_move = valid_moves[i]
        random_move_type =next_move_types[i]
        for move in random_move:
          self.my_card.remove(move)
        next_id = (self.my_id + 1) % 2
        enemy_card = self.enemy_card
        my_card =self.my_card
        #  判断出完牌游戏是否结束
        winner = self.my_id
        if len(self.my_card) != 0:
          winner = -1 
        #  如果选择不出， 下家的last_move等于自家的last_move
        if random_move_type in ["yaobuqi","buyao"]:
            last_move = "start"
        else:
          last_move = random_move
        
        next_state = State(next_id, enemy_card, my_card,last_move, winner,  random_move, random_move_type)
        return next_state

    


class Node(object):
  """
  蒙特卡罗树搜索的树结构的Node，包含了父节点和直接点等信息，还有用于计算UCB的遍历次数和quality值，还有游戏选择这个Node的State。
  """

  def __init__(self,parent,state):
    self.parent = parent
    self.children = []

    self.visit_times = 0
    self.quality_value = 0.0

    self.state = state

  def get_state(self):
    return self.state

  def get_parent(self):
    return self.parent

  def get_children(self):
    return self.children

  def get_visit_times(self):
    return self.visit_times

  def set_visit_times(self, times):
    self.visit_times = times

  def visit_times_add_one(self):
    self.visit_times += 1

  def get_quality_value(self):
    return self.quality_value

  def set_quality_value(self, value):
    self.quality_value = value

  def quality_value_add_n(self, n):
    self.quality_value += n

  def is_all_expand(self):
        if len(self.children) < self.state.moves_num:
            return False
        return True

  def add_child(self, sub_node):
    sub_node.set_parent(self)
    self.children.append(sub_node)

  def __repr__(self):
    return "Node: {}, Q/N: {}/{}, state: {}".format(
        hash(self), self.quality_value, self.visit_times, self.state)
  
  def expand(self):
    #need to be finished!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if self.state.try_flag == 0:
            valid_moves = get_moves(self.state.my_card, self.state.last_move)
            for move in valid_moves:
                self.state.init_untried_actions(move)
            self.state.try_flag = 1

        moves_num = len(self.state.untried_actions)
        i = np.random.choice(moves_num)
        untried_move = self.state.untried_actions[i].copy()
        while self.state.is_buchu(untried_move) and self.state.last_pid == self.state.my_id:
            i = np.random.choice(moves_num)
            untried_move = self.state.untried_actions[i].copy()

        new_state = self.get_state().get_next_state_with_random_choice(untried_move)
        del self.state.untried_actions[i]
        sub_node = Node(self, new_state)
        self.add_child(sub_node)
        return sub_node


def tree_policy(node, my_id):
    while node.state.winner == -1:
        if node.is_all_expand():
            node = get_bestchild(node, my_id)
        else:
            sub_node = node.expand()
            return sub_node
    return node


def default_policy(node,my_id):
  """
  蒙特卡罗树搜索的Simulation阶段，输入一个需要expand的节点，随机操作后创建新的节点，返回新增节点的reward。注意输入的节点应该不是子节点，而且是有未执行的Action可以expend的。
  基本策略是随机选择Action。
  """

  current_state = node.get_state()
  #  随机出牌直到游戏结束
  while current_state.winner == -1:
      current_state = current_state.get_next_state_with_random_choice(None)
  final_state_reward = current_state.compute_reward(my_id)
  return final_state_reward





def best_child(node):
  """
  使用UCB算法，权衡exploration和exploitation后选择得分最高的子节点，注意如果是预测阶段直接选择当前Q值得分最高的。
  """

  visit = np.array([n.visit for n in node.children])
  reward = np.array([n.reward for n in node.children])
  values = reward / visit
  index = np.where(values == np.max(values))
  nodes = np.array(node.children)[index]
  if len(nodes) == 1:
      return nodes[0]
  else:
      return np.random.choice(nodes)


def backup(node, reward):
  """
  蒙特卡洛树搜索的Backpropagation阶段，输入前面获取需要expend的节点和新执行Action的reward，反馈给expend节点和上游所有节点并更新对应数据。
  """

  # Update util the root node
  while node != None:
    # Update the visit times
    node.visit_times_add_one()

    # Update the quality value
    node.quality_value_add_n(reward)

    # Change the node to the parent node
    node = node.parent





class MCTSModel(myclass.Cards, myclass.Player,main_ddz.Game):
  def __init__(self,player_id):
    super(MCTSModel, self).__init__(player_id)
    root = Node(None, None)
    self.current_node = root
  
  def choose_with_mcts(self, state, next_moves, next_move_types, last_move):
    
      root = Node(None, None)
      self.current_node = root
    
      """for child in self.current_node.get_children():
        if self.compare(child.state.action,last_move):
          self.current_node = child"""
      enemy_cards = self.playrecords.cards_left2
      my_card = self.playrecords.cards_left1
      my_id = (self.player_id + 1) % 2
      state_ = State(my_id,enemy_cards, my_card, last_move, -1, None,next_move_types)
      self.current_node.set_state(state_)

      computation_budget = 2000
      for _ in range(computation_budget):
          expand_node = tree_policy(self.current_node,self.player_id)
          reward = default_policy(expand_node,self.player_id)
          backup(expand_node, reward)

      best_next_node = get_bestchild_(self.current_node)
      new_move = best_next_node.get_state().action
      self.current_node = best_next_node
      new_move_type = best_next_node.get_state().cards_type
      
      return new_move_type,new_move 
      
        
      
  
  @staticmethod
    #  用于比较两个无序的list
  def compare(s, t):
      return Counter(s) == Counter(t)




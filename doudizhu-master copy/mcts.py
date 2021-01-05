#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import math
import random
import numpy as np
import game
import myclass
from copy import copy
from get_bestchild import get_bestchild_,get_bestchild


class State(object):
    def __init__(self, my_id, my_card, next_card, winner, action, cards_type, move_nums, last_move_type,next_moves,next_move_types):
        self.my_id = my_id  #当前state序号
        self.my_card = my_card #手牌
        self.enemy_cards = next_card #对手的牌
        self.winner = winner #是否出完
        self.action = action  #出的牌
        self.cards_type = cards_type  #出的牌的类型
        self.move_nums = move_nums  #判断是否all_expand
        self.last_move_type =last_move_type
        self.untried_actions = []  #
        self.untried_action_types = []
        self.next_moves =next_moves
        self.next_move_types =next_move_types
    def init_untried_actions(self, move):
        self.untried_actions.append(move)

    def init_untried_action_types(self, types):
      self.untried_action_types.append(types)
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

    def get_next_state_with_random_choice(self, untried_move ,untried_move_type, next_moves , next_move_types,move_nums):

        valid_moves = next_moves
        move_nums = len(valid_moves)
        i = np.random.choice(move_nums)
        random_move = valid_moves[i]
        random_move_type = next_move_types[i]
        if untried_move != None:
          random_move = untried_move
          random_move_type =untried_move_type
        for move in random_move:
          self.my_card.remove(move)
        next_id = (self.my_id + 1) % 2
        enemy_cards = self.enemy_cards
        my_card =self.my_card
        #  判断出完牌游戏是否结束
        winner = self.my_id
        if len(self.my_card) != 0:
          winner = -1 
        #  如果选择不出， 下家的last_move等于自家的last_move
        if random_move_type in ["yaobuqi","buyao"]:
            last_move_type = "start"
        else:
          last_move_type = random_move_type
        
        next_state = State(next_id, my_card, enemy_cards, winner, random_move, random_move_type,move_nums,last_move_type,next_moves,next_move_types)
        return next_state

    


class Node(object):
  """
  蒙特卡罗树搜索的树结构的Node，包含了父节点和直接点等信息，还有用于计算UCB的遍历次数和quality值，还有游戏选择这个Node的State。
  """

  def __init__(self,parent,state):
    self.parent = parent
    self.state = state
    self.children = []

    self.visit_times = 0
    self.quality_value = 0.0

    

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
        if len(self.children) < self.state.move_nums:
            return False
        return True

  def add_child(self, sub_node):
    self.children.append(sub_node)

  def set_state(self, state):
    self.state = state
    
  def __repr__(self):
    return "Node: {}, Q/N: {}/{}, state: {}".format(
        hash(self), self.quality_value, self.visit_times, self.state)
  
  def expand(self, next_moves, next_move_types):
    
    if len(next_moves) != 0:
      valid_moves = next_moves
      for i in range(len(valid_moves)):
          self.state.init_untried_actions(valid_moves[i])
          self.state.init_untried_action_types(next_move_types[i])
      move_nums = len(self.state.untried_actions)
      i = np.random.choice(move_nums)
      untried_move = self.state.untried_actions[i]
      untried_move_type = next_move_types[i]
      new_state = self.get_state().get_next_state_with_random_choice(untried_move,untried_move_type,next_moves,next_move_types,move_nums)
      del self.state.untried_actions[i]
      del self.state.untried_action_types[i]
      #print("nextmoves:",next_moves)
      sub_node = Node(self, new_state)
      self.add_child(sub_node)
      return sub_node
    else:
      new_state = State((self.state.my_id + 1) % 2, self.state.my_card, self.state.enemy_cards, -1, None, "yaobuqi",0,None,next_moves,next_move_types)
      sub_node = Node(self, new_state)
      self.add_child(sub_node)
      return sub_node


def tree_policy(node, my_id):
    while node.state.winner == -1:
        if node.is_all_expand():
            node = get_bestchild(node, my_id)
        else:
            sub_node = node.expand(node.state.next_moves,node.state.next_move_types)
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
      current_state = current_state.get_next_state_with_random_choice(node.state.untried_actions,node.state.untried_action_types,node.state.next_move_types,node.state.next_move_types,node.state.move_nums)
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





class MCTSModel(myclass.Cards,myclass.Player,game.Game,myclass.PlayRecords):
  def __init__(self):
    super(MCTSModel, self).__init__()
    root = Node(None, None)
    self.current_node = root
  
  def choose_with_mcts(self, next_moves, next_move_types,last_move_type,my_cards,enemy_cards,player_id):
    
      root = Node(None, None)
      self.current_node = root
    
      """for child in self.current_node.get_children():
        if self.compare(child.state.action,last_move):
          self.current_node = child"""
      enemy_cards = enemy_cards
      my_card = my_cards
      my_id = player_id
      print("id",my_id)
      state_ = State(my_id, my_card, enemy_cards,  -1, None, next_move_types, len(next_moves),last_move_type,next_moves,next_move_types)
      print("len:",len(next_moves))
      self.current_node.set_state(state_)

      computation_budget = 2000
      for _ in range(computation_budget):
          expand_node = tree_policy(self.current_node, my_id)
          print("expand:",expand_node.state.untried_action_types)
          reward = default_policy(expand_node,my_id)
          backup(expand_node, reward)

      best_next_node = get_bestchild_(self.current_node)
      new_move = best_next_node.get_state().action
      self.current_node = best_next_node
      new_move_type = best_next_node.get_state().cards_type
      
      return new_move_type,new_move 
      

    




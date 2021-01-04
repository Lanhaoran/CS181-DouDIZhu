#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import math
import random
import numpy as np
import myutil
import myclass
from copy import copy
from myclass import Cards
AVAILABLE_CHOICES = [1, -1, 2, -2]
AVAILABLE_CHOICE_NUMBER = len(AVAILABLE_CHOICES)
MAX_ROUND_NUMBER = 10


class State(object):
    def __init__(self, my_id, my_card, next_card, next_next_card, last_move, winner, moves_num, action, last_p):
        self.my_id = my_id
        self.my_card = my_card
        self.next_card = next_card
        self.next_next_card = next_next_card
        self.last_move = last_move
        self.winner = winner
        self.moves_num = moves_num
        self.action = action
        self.last_pid = last_p
        self.untried_actions = []
        self.try_flag = 0

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

    def get_next_state_with_random_choice(self, untried_move):

        #  下家变自家，下下家变下家，自家变下下家
        valid_moves = myclass.get_next_moves(self.my_card, self.last_move)
        moves_num = len(valid_moves)
        i = np.random.choice(moves_num)
        tmp = valid_moves[i].copy()
        if untried_move is not None:
            tmp = untried_move
        while self.is_buchu(tmp) and self.last_pid == self.my_id:
            i = np.random.choice(moves_num)
            tmp = valid_moves[i].copy()
        move = []
        next_next_card = self.my_card.copy()
        for k in Card.all_card_name:
            move.extend([int(k)] * tmp.get(k, 0))
            next_next_card[k] -= tmp.get(k, 0)

        my_id = (self.my_id + 1) % 3
        my_card = self.next_card.copy()
        next_card = self.next_next_card.copy()
        #  判断出完牌游戏是否结束
        winner = self.my_id
        for lis in next_next_card.values():
            if lis != 0:
                winner = -1
                break
        last_move = move.copy()
        last_p = self.my_id
        #  如果选择不出， 下家的last_move等于自家的last_move
        if len(move) == 0:
            last_p = self.last_pid
            last_move = self.last_move.copy()
        if len(move) == 0 and self.last_pid == my_id:
            last_move = []
        valid_moves_ = get_moves(my_card, last_move)
        moves_num_ = len(valid_moves_)
        next_state = State(my_id, my_card, next_card, next_next_card, last_move, winner, moves_num_, move, last_p)
        return next_state

    @staticmethod
    def is_buchu(move):
        for k in Cards.all_card_name:
            if move.get(k) != 0:
                return False
        return True


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


def tree_policy(node):
  """
  蒙特卡罗树搜索的Selection和Expansion阶段，传入当前需要开始搜索的节点（例如根节点），根据exploration/exploitation算法返回最好的需要expend的节点，注意如果节点是叶子结点直接返回。
  基本策略是先找当前未选择过的子节点，如果有多个则随机选。如果都选择过就找权衡过exploration/exploitation的UCB值最大的，如果UCB值相等则随机选。
  """

  # Check if the current node is the leaf node
  while node.get_state().is_terminal() == False:

    if node.is_all_expand():
      node = best_child(node, True)
    else:
      # Return the new sub node
      sub_node = expand(node)
      return sub_node

  # Return the leaf node
  return node


def default_policy(node,my_id):
  """
  蒙特卡罗树搜索的Simulation阶段，输入一个需要expand的节点，随机操作后创建新的节点，返回新增节点的reward。注意输入的节点应该不是子节点，而且是有未执行的Action可以expend的。
  基本策略是随机选择Action。
  """

  # Get the state of the game
  current_state = node.get_state()

  # Run until the game over
  while current_state.winner == -1:

    # Pick one random action to play and get next state
    current_state = current_state.get_next_state_with_random_choice(None)

  final_state_reward = current_state.compute_reward(my_id)
  return final_state_reward


def expand(node,next_moves):
  """
  输入一个节点，在该节点上拓展一个新的节点，使用random方法执行Action，返回新增的节点。注意，需要保证新增的节点与其他节点Action不同。
  """

  valid_moves = next_moves
  for cards_combination in valid_moves:
      node.state.init_untried_actions(cards_combination)

  moves_num = len(next_moves)
  i = np.random.choice(moves_num)
  untried_move = node.state.untried_actions[i].copy()


  return sub_node


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


def monte_carlo_tree_search(node):
  """
  实现蒙特卡洛树搜索算法，传入一个根节点，在有限的时间内根据之前已经探索过的树结构expand新节点和更新数据，然后返回只要exploitation最高的子节点。
  蒙特卡洛树搜索包含四个步骤，Selection、Expansion、Simulation、Backpropagation。
  前两步使用tree policy找到值得探索的节点。
  第三步使用default policy也就是在选中的节点上随机算法选一个子节点并计算reward。
  最后一步使用backup也就是把reward更新到所有经过的选中节点的节点上。
  进行预测时，只需要根据Q值选择exploitation最大的节点即可，找到下一个最优的节点。
  """

  computation_budget = 2

  # Run as much as possible under the computation budget
  for i in range(computation_budget):

    # 1. Find the best node to expand
    expand_node = tree_policy(node)

    # 2. Random run to add node and get reward
    reward = default_policy(expand_node)

    # 3. Update all passing nodes with reward
    backup(expand_node, reward)

  # N. Get the best next node
  best_next_node = best_child(node, False)

  return best_next_node


def main():
  # Create the initialized state and initialized node
  init_state = State()
  init_node = Node()
  init_node.set_state(init_state)
  current_node = init_node

  # Set the rounds to play
  for i in range(10):
    print("Play round: {}".format(i + 1))
    current_node = monte_carlo_tree_search(current_node)
    print("Choose node: {}".format(current_node))




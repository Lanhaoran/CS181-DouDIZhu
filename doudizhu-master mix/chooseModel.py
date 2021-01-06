import myutil
import random


def choose(next_move_types, next_moves, last_move_type, model,my_cards,enemy_cards,player_id,net):
    from mcts import MCTSModel
    if model == "random":
        #print("?????????????????????")
        return myutil.choose_random(next_move_types, next_moves, last_move_type)
    if model == "little_smart":
        #print("!!!!!!!!!!!!!!!!!!!!!!!!")
        return myutil.choose_with_little_smart(next_move_types, next_moves, last_move_type)
    if model == "mcts":
        prop = random.randint(1,100)
        if prop > 79:
            myutil.choose_random(next_move_types, next_moves, last_move_type)
        if len(next_move_types) == 0:
            return "yaobuqi",[]
        mc = MCTSModel()
        return mc.choose_with_mcts(next_moves, next_move_types, last_move_type,my_cards,enemy_cards,player_id)
    if model == "DQN":
        return myutil.choose_DQN(next_move_types, next_moves, last_move_type, my_cards, net)
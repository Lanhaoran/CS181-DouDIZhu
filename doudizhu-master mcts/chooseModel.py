import myutil
def choose(next_move_types, next_moves, last_move_type, model,my_cards,enemy_cards,player_id):
    from mcts import MCTSModel
    if model == "random":
        #print("?????????????????????")
        return myutil.choose_random(next_move_types, next_moves, last_move_type)
    if model == "little_smart":
        #print("!!!!!!!!!!!!!!!!!!!!!!!!")
        return myutil.choose_with_little_smart(next_move_types, next_moves, last_move_type)
    if model == "mcts":
        if len(next_move_types) == 0:
            return "yaobuqi",[]
        mc = MCTSModel()
        return mc.choose_with_mcts(next_moves, next_move_types, last_move_type,my_cards,enemy_cards,player_id)
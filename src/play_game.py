from ai_poker.table import Table
from ai_poker.templates import simulate, BasicPlayer
from sklearn.ensemble import GradientBoostingRegressor

if __name__ == '__main__':

    t = Table(small_bind=1, big_blind=2, max_buy_in=200)

    players = []
    for i in range(5):
        
        #create BasicPlayer that uses GradientBoostingRegressor as machine learning model
        #with wealth of 1 million and 10 discrete choices for raising,
        #with each raise choice .7 times the next largest raise choice
        #Player forgets training samples older than 100,000
        r = GradientBoostingRegressor()
        name = 'Player ' + str(i+1)
        p = BasicPlayer(name=name, reg=r, bankroll=10**6, n_raises=1000, r_factor=0.7, memory=10**5)
        players.append(p)

    r = GradientBoostingRegressor()
    name = 'Player ' + str(i+1)
    p = BasicPlayer(name="User", reg=r, bankroll=10**6, n_raises=1000, r_factor=0.7, memory=10**5)
    players.append(p)

    for p in players: t.add_player(p)

    #simulate 'n_hands' hands
    #begin training after 'first_train' hands
    #before which players take random actions and explore state space
    #players train every 'n_train' hands after 'first_train'
    #players cash out/ buy in every 'n_buy_in' hands
    #table narrates each hands if 'vocal' is True
    
    print("Select table level of difficulty between:\n1.Beginner\n2.Intermediate\n3.Expert\n4.Ultimate Poker Star\n")
    ai_difficulty = int(input("Difficulty: "))

    if ai_difficulty == 1:
        simulate(t, n_hands=10000, first_train=2000, n_train=1000, n_buy_in=10)
    elif ai_difficulty == 2:
        simulate(t, n_hands=30000, first_train=2000, n_train=1000, n_buy_in=10)
    elif ai_difficulty == 3:
        simulate(t, n_hands=50000, first_train=2000, n_train=1000, n_buy_in=10)
    elif ai_difficulty == 4:
        simulate(t, n_hands=100000, first_train=2000, n_train=1000, n_buy_in=10)
    else:
        simulate(t, n_hands=100000, first_train=2000, n_train=1000, n_buy_in=10)
    
    simulate(t, n_hands=10000, n_buy_in=10000000, vocal=True)
    
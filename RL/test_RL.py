#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module to test the Agent class
"""

# Local imports
from RL.agent import Agent
from RL.environment import Environment

__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
	Test the execution of the Agent class.
"""
if __name__ == "__main__":
    agent = Agent()
    # Iterate the game
    episodes = 10
    for e in range(episodes):
        # reset state in the beginning of each game
        env = Environment(agent)
        # time_t represents each frame of the game
        # Our goal is to keep the pole upright as long as possible until score of 500
        # the more time_t the more score

        while(not env.is_finished()):
            # turn this on if you want to render
            # env.render()
            # Decide action
            env.doTurn()
            #action = agent.act(state)
            # Advance the game to the next frame based on the action.
            # Reward is 1 for every frame the pole survived
            #next_state, reward, done, _ = env.step(action)
            # Remember the previous state, action, reward, and done
            #agent.remember(state, action, reward, next_state, done)
            # make next_state the new current state for the next frame.
            #state = next_state
            # done becomes True when the game ends
            # ex) The agent drops the pole

        agent.replay()

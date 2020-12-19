import mdptoolbox
from mdptoolbox.mdp import ValueIteration, QLearning, PolicyIteration
from mdptoolbox.example import forest
import numpy as np
import random
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

Gamma = 0.9
S = 500
P, R = forest(S=S, r1=10,r2=50, p=0.1, is_sparse=False)

def optimal_value_iteration(mdp, V0, num_iterations, epsilon=0.0001):
    V = np.zeros((num_iterations + 1, mdp.S))
    V[0][:] = np.ones(mdp.S) * V0
    X = np.zeros((num_iterations + 1, mdp.A, mdp.S))
    star = np.zeros((num_iterations + 1, mdp.S))
    for k in range(num_iterations):
        for s in range(mdp.S):
            for a in range(mdp.A):
                X[k + 1][a][s] = mdp.R[a][s] + mdp.discount * np.sum(mdp.P[a][s].dot(V[k]))
            star[k + 1][s] = (np.argmax(X[k + 1, :, s]))
            V[k + 1][s] = np.max(X[k + 1, :, s])

        if (np.max(V[k + 1] - V[k]) - np.min(V[k + 1] - V[k])) < epsilon:
            V[k + 1:] = V[k + 1]
            star[k + 1:] = star[k + 1]
            X[k + 1:] = X[k + 1]
            break
        else:
            pass

    return star, V, X
V0 = np.zeros(3)
mdp = mdptoolbox.mdp.FiniteHorizon(P, R, 0.9, 1)
star, V, X = optimal_value_iteration(mdp, V0, 1, epsilon=0.0001)
print(star)
print(V)
print(X)

def epsilon_greedy_exploration(Q, epsilon, num_actions):
    def policy_exp(state):
        probs = np.ones(num_actions, dtype=float) * epsilon / num_actions
        best_action = np.argmax(Q[state])
        probs[best_action] += (1.0 - epsilon)
        return probs
    return policy_exp

def q_learning(mdp, num_episodes, T_max, epsilon=0.01):
    Q = np.zeros((mdp.S, mdp.A))
    episode_rewards = np.zeros(num_episodes)
    policy = np.ones(mdp.S)
    V = np.zeros((num_episodes, mdp.S))
    N = np.zeros((mdp.S, mdp.A))
    for i_episode in range(num_episodes):
        # epsilon greedy exploration
        greedy_probs = epsilon_greedy_exploration(Q, epsilon, mdp.A)
        state = np.random.choice(np.arange(mdp.S))
        for t in range(T_max):
            # epsilon greedy exploration
            action_probs = greedy_probs(state)
            action = np.random.choice(np.arange(len(action_probs)), p=action_probs)
            next_state, reward = playtransition(mdp, state, action)
            episode_rewards[i_episode] += reward
            N[state, action] += 1
            alpha = 1 / (t + 1) ** 0.8
            best_next_action = np.argmax(Q[next_state])
            td_target = reward + mdp.discount * Q[next_state][best_next_action]
            td_delta = td_target - Q[state][action]
            Q[state][action] += alpha * td_delta
            state = next_state
        V[i_episode, :] = Q.max(axis=1)
        policy = Q.argmax(axis=1)

    return V, policy, episode_rewards, N

print("====== Policy iteration ======")
Pi = mdptoolbox.mdp.PolicyIteration(P, R, 0.9)
Pi.run()
print(Pi.policy)
print(Pi.V)
print(Pi.iter)
print(Pi.time)

print("====== Value iteration ======")
Vi = mdptoolbox.mdp.ValueIteration(P, R, 0.9)
Vi.run()
print(Vi.policy)
print(Vi.iter)
print(Vi.V)
print(np.max(Vi.V))
print(Vi.time)
#print(Vi.R)

print("====== Q learning ======")
Ql = mdptoolbox.mdp.QLearning(P, R, 0.9,1000000)
Ql.run()
print(Ql.policy)
print(Ql.V)
print(np.max(Ql.V))
print(Ql.time)

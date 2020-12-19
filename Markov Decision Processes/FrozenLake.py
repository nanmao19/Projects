import time
import gym
import torch
import time
from gym.envs.registration import register
register(
    id='FrozenLakeNotSlippery-v0',
    entry_point='gym.envs.toy_text:FrozenLakeEnv',
    kwargs={'map_name' : '4x4', 'is_slippery': False},
)
import numpy as np
import gym
import seaborn as sns
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

env = gym.make('FrozenLake-v0', is_slippery=False)

# Greedy policy to choose the next action
def choose_best_action(env, V, s, gamma):
    a_best = None
    q_best = float('-inf')
    nb_actions = env.action_space.n
    for a in range (0, nb_actions):
        env.env.s = s # go to state s
        s_next, r, done, info = env.step(a) #take the action a
        q = r + gamma * V[s_next] # compute the value future value after taking action a
        if q > q_best:
            q_best = q
            a_best = a
    return a_best

print("### value iteration ###")
# value iteration algorithm
#def compute_value_iteration(env = gym.make('FrozenLakeNotSlippery-v0'), gamma=.9, v_delta_threshold=.01, V = None, verbose=True):
def compute_value_iteration(env=env, gamma=.9, v_delta_threshold=.001, V=None, verbose=True):
    env.reset()
    nb_actions = env.action_space.n
    nb_states = env.observation_space.n
    # values vector
    if V == None:
        V = np.zeros([nb_states])
    # policy vector
    P = np.zeros([nb_states], dtype=int)
    iteration = 0

    while True:
        v_delta = 0
        #print(iteration)
        for s in range (0, nb_states):
            v_previous = V[s]
            a_best = choose_best_action(env, V, s, gamma) # find an action with the highest future reward
            env.env.s = s # go to the state s
            s_next, r, done, info = env.step(a_best) #take the best action
            V[s] = r + gamma * V[s_next] # update the value of the state
            #rewards = np.append(rewards,r)
            P[s] = a_best # store the best action in the policy vector for the state
            v_delta = max(v_delta, np.abs(v_previous - V[s])) # calculate the rate of value improvment for the state
        iteration += 1
        if v_delta < v_delta_threshold:
            if verbose:
                print (iteration,' iterations done')
            break
    return V, P
t0=time.time()
V_4, final_actions= compute_value_iteration()
t1=time.time()
V4 = np.reshape(V_4, (4,4))
print("Value Function from value iteration")
print(V4)
print(final_actions)
print("time:", t1-t0)
result = []
for i in range (len(final_actions)):
    if final_actions[i] == 0:
        result = np.append(result, '<')
    elif final_actions[i] == 1:
        result = np.append(result, '>')
    elif final_actions[i] == 2:
        result = np.append(result, 'v')
    elif final_actions[i] == 3:
        result = np.append(result, '^')
print(np.reshape(result, (4,4)))


print("### policy iteration ###")
# function for performing policy iteration
#def compute_policy_iteration(env=gym.make('FrozenLakeNotSlippery-v0'),gamma=.9, v_delta_threshold=.01,P=None, verbose=True):
def compute_policy_iteration(env=env, gamma=.9, v_delta_threshold=.01,P=None, verbose=True):
    env.reset()
    nb_actions = env.action_space.n
    nb_states = env.observation_space.n
    # values vector
    V = np.zeros([nb_states])
    # policy vector
    if P == None:
        P = np.random.choice(nb_actions, size=nb_states)

    max_iterations = 200000
    iteration = 0
    vd = []
    for i in range(max_iterations):

        # policy evaluation
        while True:
            v_delta = 0
            for s in range(0, nb_states):
                v_previous = V[s]
                env.env.s = s  # go to state s
                s_next, r, done, info = env.step(P[s])  # take the action recommended by policy
                V[s] = r + gamma * V[s_next]  # update value after applying policy
                v_delta = max(v_delta,
                              np.abs(v_previous - V[s]))  # calculate the rate of value improvment for the state
                vd = np.append(vd, v_delta)
            if v_delta < v_delta_threshold:
                break

        # policy improvement
        policy_stable = True
        for s in range(0, nb_states):
            a_old = P[s]  # ask policy for action to perform
            a_best = choose_best_action(env, V, s, gamma)  # find an action with the highest future reward
            P[s] = a_best  # store the best action in the policy vector for the state
            if a_old != a_best:
                policy_stable = False

        if policy_stable:
            break

        iteration += 1
    if verbose:
        print(iteration, ' iterations done')
    return V, P, vd
t0=time.time()
Vp_4, final_actions, delta = compute_policy_iteration()
t1=time.time()
print("time:", t1-t0)
V4 = np.reshape(Vp_4, (4,4))
print("Value Function from policy iteration")
print(V4)
result = []
for i in range (len(final_actions)):
    if final_actions[i] == 0:
        result = np.append(result, '<')
    elif final_actions[i] == 1:
        result = np.append(result, '>')
    elif final_actions[i] == 2:
        result = np.append(result, 'v')
    elif final_actions[i] == 3:
        result = np.append(result, '^')
print(np.reshape(result, (4,4)))

print("### Q-Learning ###")
env = gym.make('FrozenLakeNotSlippery-v0')

# Total number of States and Actions
number_of_states = env.observation_space.n
number_of_actions = env.action_space.n
num_episodes = 1000
steps_total = []
rewards_total = []
egreedy_total = []
gamma = 0.9

learning_rate = 0.9
egreedy = 0.7
egreedy_final = 0.1
egreedy_decay = 0.999
Q = torch.zeros([number_of_states, number_of_actions])
t0=time.time()
for i_episode in range(num_episodes):

    # resets the environment
    state = env.reset()
    step = 0
    while True:

        step += 1
        random_for_egreedy = torch.rand(1)[0]
        if random_for_egreedy > egreedy:
            random_values = Q[state] + torch.rand(1, number_of_actions) / 1000
            action = torch.max(random_values, 1)[1][0]
            action = action.item()
        else:
            action = env.action_space.sample()
        if egreedy > egreedy_final:
            egreedy *= egreedy_decay

        new_state, reward, done, info = env.step(action)

        # Filling the Q Table
        Q[state, action] = reward + gamma * torch.max(Q[new_state])

        # Setting new state for next action
        state = new_state

        if done:
            steps_total.append(step)
            rewards_total.append(reward)
            egreedy_total.append(egreedy)
            break
t1=time.time()
print("time:", t1-t0)
print("Percent of episodes finished successfully: {0}".format(sum(rewards_total[:])/1000))
plt.figure(figsize=(12,5))
plt.title("Rewards")
plt.bar(torch.arange(len(rewards_total)), rewards_total, alpha=0.6,width=5)
plt.savefig("rewards.png")
plt.show()

plt.figure(figsize=(12,5))
plt.title("Steps")
plt.bar(torch.arange(len(steps_total)), steps_total, alpha=0.6, width=5)
plt.savefig("steps.png")
plt.show()
import os
import sys

from pprint import pprint

from draco.spec import *
from draco.learn.helper import *
from draco.run import run

from draco.learn import data_util

import logging

import copy

def discriminative_learning(train_data, initial_weights, learning_rate=0.01, max_iter=100):
    """ discriminative learning for mln from partial and full specs """

    weights = {}
    for k in initial_weights:
        weights[k] = initial_weights[k] * 50

    pprint(weights)
    logging.disable(logging.CRITICAL)

    t = 0
    while t < max_iter:
        print("[Iteration] {}".format(t))
        for case in train_data:
            partial_spec, full_spec = train_data[case][0], train_data[case][1]
            draco_rec = run(partial_spec, constants=weights, silence_warnings=True)

            pprint("=============")
            pprint(case)

            map_state = count_violations(draco_rec)
            truth_state = count_violations(full_spec)

            pprint(map_state)
            pprint(truth_state)
            # get the names of violated rules in two specs
            violated_rules = set(list(map_state.keys()) + list(truth_state.keys()))

            for r in violated_rules:
                # get the num violations of the rule r
                n1 = map_state.get(r, 0)
                n2 = truth_state.get(r, 0)

                # since our weights are costs and we want to minimize the loss
                weights[r + "_weight"] += (n1 - n2)

            # the solution generated by visrec solution
            #print(draco_rec.to_vegalite_json())
        break
        t += 1

    pprint(weights)

def pairwise_learning(train_pairs, initial_weights, learning_rate=0.01, max_iter=100):
    """ discriminative learning for mln from partial and full specs """

    weights = {}
    for k in initial_weights:
        weights[k] = 0

    logging.disable(logging.CRITICAL)

    t = 0
    while t < max_iter:
        print("[Iteration] {}".format(t))
        for case in train_data:
            neg_spec, pos_spec = train_data[case][0], train_data[case][1]

            neg_state = count_violations(neg_spec)
            pos_state = count_violations(pos_spec)

            # get the names of violated rules in two specs
            violated_rules = set(list(neg_state.keys()) + list(pos_state.keys()))

            for r in violated_rules:
                # get the num violations of the rule r
                n1 = neg_state.get(r, 0)
                n2 = pos_state.get(r, 0)

                # since our weights are costs and we want to minimize the loss
                weights[r + "_weight"] += (n1 - n2)

            # the solution generated by visrec solution
            #print(draco_rec.to_vegalite_json())

        t += 1

    pprint(weights)


if __name__ == '__main__':
    train_data = data_util.load_partial_full_data()
    #weights = discriminative_learning(train_data, current_weights())

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys as trans
import random
import csv

def fill_people():
    people=set()
    with open('people.csv', newline='') as csvfile:
        for row in csvfile:
            people.add(row.strip())
    return people

def create_tuples():
    people=fill_people()
    left=people.copy()
    first=random.choice(tuple(left))
    choice=first
    tuples=[]
    left.remove(choice)
    while len(left) > 0:
        prev=choice
        choice=random.choice(tuple(left))
        left.remove(choice)
        tuples.append((prev, choice))
    tuples.append((choice, first))
    return tuples

def main():
    tuples=create_tuples()
    with open('tuples.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for t in tuples:
            print("%s -> %s" % (t[0], t[1]))
            writer.writerow(t)

if __name__ == "__main__":
    main()

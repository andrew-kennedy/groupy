#!/usr/bin/env python3
from fuzzywuzzy import fuzz
from fuzzywuzzy import utils as fuzzutils
from fuzzywuzzy import process
from itertools import zip_longest
from collections import namedtuple
from random import shuffle
import csv


def main():
    people = set(person for person in
                 read_csv_data('FallRetreat2015Registrantsv2.csv'))
    peopleNames = [person.full_name for person in people]
    matchedMales = set()
    usedPeople = set()
    matchedFemales = set()
    print(len(people))

    # create a set of subsets of roommate matches, including sets of 1
    for person in people:
        matchedRoommates = fuzzy_match_roommates(peopleNames, person.roommates)
        nodeSet = set()
        if person not in usedPeople:
            nodeSet.add(person)
            usedPeople.add(person)
            for name in matchedRoommates:
                node = node_from_name(people, name)
                if node and node not in usedPeople:
                    nodeSet.add(node)
                    usedPeople.add(node)
            # set done being altered, freeze it for hashability
            nodeSet = frozenset(nodeSet)
            if person.gender == 'Male':
                matchedMales.add(nodeSet)
            else:
                matchedFemales.add(nodeSet)

    soloMales = set()
    pairedMales = set()
    soloFemales = set()
    pairedFemales = set()
    for s in matchedMales:
        if len(s) > 1:
            pairedMales.add(s)
        else:
            soloMales.add(*s)

    for s in matchedFemales:
        if len(s) > 1:
            pairedFemales.add(s)
        else:
            soloFemales.add(*s)

    soloMales = list(soloMales)
    pairedMales = list(pairedMales)
    soloFemales = list(soloFemales)
    pairedFemales = list(pairedFemales)

    shuffle(soloMales)
    shuffle(pairedMales)
    shuffle(soloFemales)
    shuffle(pairedFemales)

    print(len(soloMales))
    print(len(pairedMales))
    print(len(soloFemales))
    print(len(pairedFemales))

    maleRooms = list()
    femaleRooms = list()
    # while pairedMales and len(soloMales) >= 2:
    #     maleRooms.append((*pairedMales.pop(), soloMales.pop(),
    #                      soloMales.pop()))
    # while pairedMales:  # soloMales ran out
    #     if soloMales:
    #         maleRooms.append((*pairedMales.pop(), soloMales.pop()))
    #     else:
    #         maleRooms.append((*pairedMales.pop(), *pairedMales.pop()))
    # while len(soloMales) >= 4:  # no more pairs
    #     maleRooms.append((soloMales.pop(), soloMales.pop(), soloMales.pop(),
    #                      soloMales.pop()))
    # rl = list()
    # while soloMales:
    #     rl.append(soloMales.pop())
    # maleRooms.append(tuple(rl))
    #
    while pairedFemales and len(soloFemales) >= 2:
        femaleRooms.append((*pairedFemales.pop(), soloFemales.pop(),
                           soloFemales.pop()))
    while pairedFemales:  # soloMales got too short
        if soloFemales:
            femaleRooms.append((*pairedFemales.pop(), soloFemales.pop()))
        else:
            femaleRooms.append((*pairedFemales.pop(), *pairedFemales.pop()))
    while len(soloFemales) >= 4:  # no more pairs
        femaleRooms.append((soloFemales.pop(), soloFemales.pop(),
                           soloFemales.pop(), soloFemales.pop()))
    fl = list()
    while soloFemales:
        fl.append(soloFemales.pop())
    femaleRooms.append(tuple(fl))

    write_csv_data("test.csv", maleRooms, femaleRooms)


def write_csv_data(path, maleRoomList, femaleRoomList):
    with open(path, 'w') as data:
        writer = csv.writer(data)
        writer.writerow(PersonNode._fields)
        for room in maleRoomList:
            for person in room:
                writer.writerow(person)
            writer.writerow("")
        writer.writerow("")
        for room in femaleRoomList:
            for person in room:
                writer.writerow(person)
            writer.writerow("")


def node_from_name(people, name):
    matchedNodes = [p for p in people if p.full_name == name]
    if matchedNodes:
        return matchedNodes[0]
    else:
        return None


def read_csv_data(path):
    with open(path, 'rU') as data:
        # skip the header
        data.readline()
        reader = csv.reader(data)
        for row in map(PersonNode._make, reader):
            yield row


def fuzzy_match_roommates(nameList, roommateString):
    bestMatches = set()
    splitString = roommateString.split()
    it = iter(splitString)
    zippedNames = [a + " " + b for a, b in zip_longest(it, it, fillvalue="")]
    for name in zippedNames:
        bestMatches.add(process.extractOne(name, nameList, score_cutoff=90))
    bestMatches = set(x[0] for x in bestMatches if x is not None)
    return bestMatches


fields = ['first_name', 'last_name', 'email', 'phone', 'gender',
          'roommates']


class PersonNode(namedtuple('PersonNode_', fields)):
    """
    A class representing a person in a graph of friends/roommates. The data is
    all immutable and these are extra properties.
    """

    @property
    def full_name(self):
        return (self.first_name + " " + self.last_name).lower()


if __name__ == '__main__':
    main()

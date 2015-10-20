#!/usr/bin/env python3
from fuzzywuzzy import fuzz
from fuzzywuzzy import utils as fuzzutils
from fuzzywuzzy import process
from itertools import zip_longest
from collections import namedtuple
from random import shuffle
import csv


def main():
    attendees = set(person for person in
                    read_csv_data('data/Master Spreadsheet.csv'))
    leaders = set(person for person in
                  read_csv_data('data/DgroupLeaders.csv'))
    leaderNames = set(person.full_name for person in leaders)
    print(len(attendees))
    print(len(leaders))
    # remove the leaders from the attendees
    attendees = attendees.difference(
        person_set_from_name_set(leaderNames, attendees))
    maleAttendees = [person for person in attendees if person.gender == 'Male']
    femaleAttendees = [person for person in attendees
                       if person.gender == 'Female']
    shuffle(maleAttendees)
    shuffle(femaleAttendees)
    maleLeaders = [person for person in leaders if person.gender == 'Male']
    femaleLeaders = [person for person in leaders if person.gender == 'Female']
    shuffle(maleLeaders)
    shuffle(femaleLeaders)
    maleLeads = {}
    femaleLeads = {}
    maleLeads['junior'] = [person for person in maleLeaders if
                           person.year == 'Junior']
    maleLeads['senior'] = [person for person in maleLeaders if
                           person.year != 'Junior']
    femaleLeads = {}
    femaleLeads['junior'] = [person for person in femaleLeaders if
                             person.year == 'Junior']
    femaleLeads['senior'] = [person for person in femaleLeaders if
                             person.year != 'Junior']
    males = {}
    females = {}
    males['freshman'] = [person for person in maleAttendees if
                         person.year == 'Freshman']
    males['sophomore'] = [person for person in maleAttendees
                          if person.year == 'Sophomore']
    males['junior'] = [person for person in maleAttendees
                       if person.year == 'Junior']
    males['senior'] = [person for person in maleAttendees if
                       person.year != 'Freshman' and
                       person.year != 'Sophomore' and
                       person.year != 'Junior']
    females['freshman'] = [person for person in femaleAttendees
                           if person.year == 'Freshman']
    females['sophomore'] = [person for person in femaleAttendees
                            if person.year == 'Sophomore']
    females['junior'] = [person for person in femaleAttendees
                         if person.year == 'Junior']
    females['senior'] = [person for person in femaleAttendees if
                         person.year != 'Freshman' and
                         person.year != 'Sophomore' and
                         person.year != 'Junior']
    calculate_ratios(femaleLeads, females)
    calculate_ratios(maleLeads, males)

    maleGroups = create_groups(maleLeaders, males)
    femaleGroups = create_groups(femaleLeaders, femaleAttendees)
    write_csv_data('output/discussionGroups.csv', maleGroups, femaleGroups)


def shuffle_all(leaders, attendees):
    shuffle(leaders['junior'])
    shuffle(leaders['senior'])
    shuffle(attendees['freshman'])
    shuffle(attendees['sophomore'])
    shuffle(attendees['junior'])
    shuffle(attendees['senior'])


def create_groups(leaders, members):
    groups = []
    while leaders:
        group = []
        group.append(leaders.pop())
        while len(group) < 4:
            for item in shuffle(members.items()):
                if item[0] not group[0].year:
                    group
        groups.append(group)
    return groups


def person_set_from_name_set(nameSet, personSet):
    retSet = set()
    for person in personSet:
        if person.full_name in nameSet:
            retSet.add(person)
    return retSet


def calculate_ratios(leadersDict, attendeesDict):
    total = (len(leadersDict['junior']) +
             len(leadersDict['senior']) +
             len(attendeesDict['freshman']) +
             len(attendeesDict['sophomore']) +
             len(attendeesDict['junior']) +
             len(attendeesDict['senior']))
    print("total is " + str(total))
    attendeesDict['freshmanRatio'] = len(attendeesDict['freshman']) / total
    attendeesDict['sophomoreRatio'] = len(attendeesDict['sophomore']) / total
    attendeesDict['juniorRatio'] = (len(attendeesDict['junior']) +
                                    len(leadersDict['junior'])) / total
    attendeesDict['seniorRatio'] = (len(attendeesDict['senior']) +
                                    len(leadersDict['senior'])) / total


def write_csv_data(path, maleGroups, femaleGroups):
    with open(path, 'w') as data:
        writer = csv.writer(data)
        writer.writerow(PersonNode._fields)
        for group in maleGroups:
            for person in group:
                writer.writerow(person)
            writer.writerow("")
        writer.writerow("")
        for group in femaleGroups:
            for person in group:
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
          'year']


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

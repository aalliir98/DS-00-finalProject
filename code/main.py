import json
import queue
from collections import defaultdict


class user:

    def __init__(self, id, name, dateOfBirth, universityLocation, field, workplace, specialties, connectionId):
        self.id = id
        self.name = name
        self.dateOfBirth = dateOfBirth
        self.universityLocation = universityLocation
        self.field = field
        self.workplace = workplace
        self.specialities = specialties
        self.connectionId = connectionId
        self.priority = 0
        self.connectionDegree = 0

    def __lt__(self, other):
        return self.priority > other.priority


if __name__ == '__main__':

    with open("users.json", 'r') as file:
        file_data = json.load(file)

    users = {p["id"]: user(p["id"], p["name"], p["dateOfBirth"], p["universityLocation"], p["field"], p["workplace"],
                           p["specialties"], p["connectionId"]) for p in file_data}

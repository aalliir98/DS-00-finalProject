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

class Graph:

    def __init__(self):
        self.graph = defaultdict(list)

    def addEdge(self, u, v):
        for id in v:
            self.graph[u].append(int(id))

    def BFS(self, s):
        h = s
        visited = [False] * (max(self.graph) + 1)
        queue = [s]
        visited[s] = True
        connections = {}
        while queue:
            s = queue.pop(0)
            a = self.minEdgeBFS(h, s)
            if a <= 5 and a != 0 and a != 1:
                connections[s] = a
                # print(s, end=" ")
            for i in self.graph[s]:
                if not visited[i]:
                    queue.append(i)
                    visited[i] = True
        return connections

    def minEdgeBFS(self, u, v):
        visited = [0] * (max(self.graph) + 1)
        distance = [0] * (max(self.graph) + 1)
        Q = queue.Queue()
        distance[u] = 0
        Q.put(u)
        visited[u] = True
        while not Q.empty():
            x = Q.get()

            for i in range(len(self.graph.get(x))):
                if visited[self.graph.get(x)[i]]:
                    continue

                distance[self.graph.get(x)[i]] = distance[x] + 1
                Q.put(self.graph.get(x)[i])
                visited[self.graph.get(x)[i]] = 1
        return distance[v]

if __name__ == '__main__':

    with open("users.json", 'r') as file:
        file_data = json.load(file)

    users = {p["id"]: user(p["id"], p["name"], p["dateOfBirth"], p["universityLocation"], p["field"], p["workplace"],
                           p["specialties"], p["connectionId"]) for p in file_data}

    g = Graph()
    for p in users:
        g.addEdge(int(users[p].id), users[p].connectionId)
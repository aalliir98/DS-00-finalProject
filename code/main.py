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
        self.graph[u] = v

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

def setPriority(user1, user2, speciality, field, university, workplace):
    i = 0
    for x in user2.specialities:
        if x in user1.specialities:
            i += 1
    user2.priority += (speciality * i)
    if user1.field == user2.field:
        user2.priority += field
    if user1.universityLocation == user2.universityLocation:
        user2.priority += university
    if user1.workplace == user2.workplace:
        user2.priority += workplace
    user2.priority -= user2.connectionDegree


def show(user1, p):
    print(f"{p + 1}) priority: [{user1.priority}] Id: [{user1.id}] Name: [{user1.name}] Date of birth: "
          f"[{user1.dateOfBirth}] Field: [{user1.field}] University: [{user1.universityLocation}] Work place: "
          f"[{user1.workplace}] Specialities: {user1.specialities} Connection Ids: {user1.connectionId}")


def find_connection(users, id ,g):
    if id in users:
        user1 = users[id]
        connections = g.BFS(int(id))
        list = []
        print("""
Enter a number between 0 and 10
                            """)
        speciality = int(input("speciality:"))
        field = int(input("field:"))
        university = int(input("university:"))
        workplace = int(input("workplace:"))
        for p in connections:
            s = users[str(p)]
            s.connectionDegree = connections[p]
            s.priority = 0
            setPriority(user1, s, speciality, field, university, workplace)
            list.append((s.priority, s))
        list.sort(reverse=True)
        for p in range(len(list)):
            if p < 20:
                show(list[p][1], p)

        do2 = input("do you want connect anyone?(y/n)")
        if do2 == "y":
            a = int(input("how many? "))
            for i in range(a):
                id = int(input("Enter id: "))
                if str(id) in users:
                    user1.connectionId.append(id)
                    g.graph[id].append(int(user1.id))
            g.graph[int(user1.id)] = user1.connectionId
            print("connection finished")

    else:
        print("there isn't any account with this id in linkedin")


def register_findConnection(user, users):
    list = []
    i=0
    for p in users:
        if i <20:
            s = users[p]
            s.priority = 0
            s.connectionDegree = 0
            setPriority(user, s, 10, 7, 5, 3)
            list.append((s.priority, s))
    list.sort(reverse=True)
    for p in range(len(list)):
        if p < 20:
            show(list[p][1], p)


def register(users, g):
    id = input("Id: ")
    if id not in users:
        name = input("name: ")
        date = input("date of birth: ")
        university = input("university: ")
        field = input("field: ")
        workplace = input("workplace: ")
        speciality = []
        connections1 = []
        for x in range(int(input("how many speciality: "))):
            speciality.append(input(str(x + 1) + ") "))
        print("which person do you want to connect?")
        user2 = user(id, name, date, university, field, workplace, speciality, connections1)
        register_findConnection(user2, users)
        print("how many?")
        for i in range(int(input())):
            connections1.append(int(input("Enter id: ")))

        user2.connectionId = connections1

        for i in user2.connectionId:
                g.graph[i].append(int(user2.id))
        g.addEdge(int(user2.id), user2.connectionId)
        users[user2.id] = user2
        print("account created")
    else:
        print("there is another account with this id")

if __name__ == '__main__':
    try:
        with open("users2.json", 'r') as file:
            file_data = json.load(file)

        users = {p["id"]: user(p["id"], p["name"], p["dateOfBirth"], p["universityLocation"], p["field"], p["workplace"],
                               p["specialties"], list(map(int, p["connectionId"]))) for p in file_data}

        g = Graph()
        for p in users:
            g.addEdge(int(users[p].id), users[p].connectionId)

        print("welcome to my linkedin")
        user1 = None
        while True:
            print("""      
what do you want to do?
1) see the list of connections
2) register an connect
3) save in file
                """)
            do = input()
            if do == "1":
                id = input("Enter id: ")
                find_connection(users, id, g)
            elif do == "2":
                register(users, g)
            elif do =="3":
                list1 = []
                dict1 = {}
                for p in users:
                    dict1 = {"id": users[p].id, "name": users[p].name, "dateOfBirth": users[p].dateOfBirth, "universityLocation": users[p].universityLocation, "field": users[p].field, "workPlace": users[p].specialities, "connectionId" : users[p].connectionId}
                    list1.append(dict1)
                with open("sample.json", "w") as outfile:
                    json.dump(list1, outfile)
    except Exception:
        print("")
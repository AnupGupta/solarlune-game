__author__ = 'SolarLune'

from bge import logic, render

import mathutils

import math, time


class Node():

    def __init__(self, obj):

        self.obj = obj

        self.obj['nm_node'] = self  # Place yourself in the "owner" game object

        self.position = self.obj.worldPosition

        self.neighbors = []

        self.cost = 1

        self.parent = None  # Parent node for path-finding

        #self.g_score = 0
        #self.f_score = 0
        #self.h_score = 0

    def __get_cost(self):

        if 'nm_cost' in self.obj:

            return self.obj['nm_cost']

        return self._cost

    def __set_cost(self, value):

        self._cost = value

    cost = property(__get_cost, __set_cost)

class NodeMap():

    def __init__(self):

        self.nodes = []

    def add_node(self, node):

        self.nodes.append(node)

    def remove_node(self, node):

        self.nodes.remove(node)

    def update_neighbors(self, min_dist=0, max_dist=9999, max_connections=9999):

        cont = logic.getCurrentController()
        obj = cont.owner

        evaluated = []

        for n in self.nodes:

            for m in self.nodes:

                if n != m and not m in evaluated:

                    d = (n.position - m.position).magnitude

                    if max_dist >= d >= min_dist:

                        ray = obj.rayCast(n.position, m.position, 0, 'nm_solid', 1, 1)

                        if not ray[0]:

                            if len(n.neighbors) < max_connections and len(m.neighbors) < max_connections:

                                n.neighbors.append(m)
                                m.neighbors.append(n)

            evaluated.append(n)

    def get_closest_node(self, position):

        cont = logic.getCurrentController()

        obj = cont.owner

        sorted_nodes = self.nodes[:]

        sorted_nodes.sort(key=lambda n: (n.position - position).magnitude)

        closest = None

        for n in sorted_nodes:

            ray = obj.rayCast(n.position, position, 0, 'nm_solid', 1, 1, 1)

            if not ray[0]:

                closest = n

                break

        return closest

    def path_to(self, ending_point, starting_point=None, max_check_num=1000):

        if starting_point is None:

            starting_point = logic.getCurrentController().owner.worldPosition.copy()

        goal = self.get_closest_node(ending_point)
        starting_node = self.get_closest_node(starting_point)

        if not goal:

            print("ERROR: GOAL POSITION CANNOT BE REACHED FROM ANY NODE ON MAP.")
            return

        if not starting_node:

            print("ERROR: STARTING NODE CANNOT BE REACHED FROM ANY NODE ON MAP.")
            return

        def get_g_score(node):

            return (starting_node.obj.position - node.obj.position).magnitude

        def get_h_score(node):

            return (node.obj.position - goal.obj.position).magnitude

        def get_f_score(node):

            return get_g_score(node) + get_h_score(node) + node.cost

        open_list = [starting_node]
        closed_list = []

        exit_loop = False

        for x in range(max_check_num):

            open_list.sort(key=get_f_score)

            current_node = open_list.pop(0)
            closed_list.append(current_node)

            for neighbor in current_node.neighbors:

                if neighbor in closed_list:

                    continue

                if neighbor not in open_list:

                    neighbor.parent = current_node

                    open_list.append(neighbor)

                    if neighbor == goal:

                        print("A Path has been found!")

                        exit_loop = True

                        break

                #else:

                    #if get_g_score(current_node) + neighbor.g_score < neighbor.g_score

                    #costs[neighbor] = {'F':get_f_score(neighbor), 'G':get_g_score(neighbor), 'H':get_h_score()}

                #else:

                #    if get_g_score(neighbor)

            if exit_loop:

                break

        path = []

        target_square = goal

        for x in range(1000):

            path.append(target_square)

            if target_square == starting_node:

                break

            target_square = target_square.parent

        return path

    def debug_node_connections(self):

        for node in self.nodes:

            for neighbor in node.neighbors:

                render.drawLine(node.position, neighbor.position, [1, 0, 0])

    def debug_node_path(self, path):

        #print("______")

        for node in path:

            #print(node.obj)

            s = abs(math.sin(time.clock() * math.pi))

            node.obj.color = [s, s, s, 1]
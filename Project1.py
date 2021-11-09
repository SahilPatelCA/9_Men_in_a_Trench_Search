import sys
import time
import heapq


class Node(object):  # Node class. Includes all node attributes
    def __init__(self):

        self.state = []
        self.parent = None

    def set_State(self, state):  # stores current state (array) at the node
        self.state = state

    def set_Parent(self, parent):  # stores the parent of the current node
        self.parent = parent

    def set_Weight(self, weight):  # stores the weight g(n) + f(n) of current node
        self.weight = weight

    def set_Depth(self, depth):  # stores the depth of the current Node
        self.depth = depth

    def set_Time(self, time):  # stores the time at which the current node was searched
        self.time = time

    # stores the number of nodes expanded until the current node
    def set_NodesExpanded(self, numExpanded):
        self.nodesExpanded = numExpanded

    def __lt__(self, w2):  # this overrides the < opporator for node comparison. Forces comparison of the node.weight
        if self.weight < w2.weight:
            return True
        else:
            return False

    def __gt__(self, w2):  # this overrides the > opporator for node comparison. Forces comparison of the node.weight
        if self.weight > w2.weight:
            return True
        else:
            return False


def ProjectStart():
    # Initial starting state
    trenchOrder = [0, 2, 3, 4, 0, 5, 6, 0, 7, 8, 0, 9, 1]

    # Semi-solved starting state (for testing)
    Depth14 = [1, 2, 0, 0, 0, 0, 3, 5, 4, 6, 8, 7, 9]

    searchType = input(
        "What Search would you like? Type '1' for Uniform Cost Search, '2' for A* Misplaced Tile Heurisitic, or '3' for A* Manhattan Distance Heuristic:\n")

    # searchType is equal to the heuristic value
    global start
    global end
    start = time.time()
    # passes in the list and heuristic value
    General_Search(Depth14, int(searchType))
    # end = time.time()
    # print("Total Time: {}".format(end-start))  # prints total time of search
    print()
    return


def General_Search(puzzle, heuristic):
    ans = [1, 2, 3, 4, 0, 5, 6, 0, 7, 8, 0, 9, 0]  # Goal state
    # initiates the starting node to default values before entering loop
    Node_Start = Node()
    Node_Start.set_State(puzzle)
    Node_Start.set_Depth(0)
    Node_Start.set_Time(0)
    Node_Start.set_NodesExpanded(0)
    flag = False
    currLevel = 0
    queue = []
    expandArr = []
    nodeCount = 0
    maxQueueSize = 0
    prntArr = []
    currHeuristic = 0
    # array of dictionaries. Each indicy is the dictionary for the nodes at a specific depth
    dicArr = [{}] * 69

    # queue.append(Node_Start)
    heapq.heappush(queue, (0, Node_Start))

    while len(queue) > 0:
        flag = False  # reset flag
        if len(queue) > maxQueueSize:  # always updating the size of maxQueueSize
            maxQueueSize = len(queue)

          # Set the first state in the queue to currNode
        currNode = heapq.heappop(queue)[1]

        # checks if the state has been seen already. If so, skips the rest of the loop and restarts on next node.
        for i in range(currNode.depth):
            if str(currNode.state) in dicArr[i].keys():
                flag = True
                break
        if flag:
            continue
        else:
            # adds the current state to the dictionary array (dicArr), more specifically to the dictionary at the indicy of the node's depth
            dicArr[currNode.depth][str(currNode.state)] = currNode.depth

        # checks if reach a new depth level
        if currNode.depth > currLevel:
            # "deletes" all dictionaries in indicies 10 less than current indicy (depth)
            if currNode.depth >= 10:
                dicArr[currNode.depth - 10] = {}
            currLevel = currNode.depth

        # Runs if goal state is found
        if currNode.state == ans:
            end = time.time()
            # loops backwards tracing goal states parents until reaching start node
            while currNode.parent != None:
                prntArr.append(currNode)
                currNode = currNode.parent

            # Print starting state information
            print_Trench(Node_Start.state)
            print("Current Depth: ", 0)
            print("Time elapsed: ", Node_Start.time)
            print("Current Nodes Expanded: ", Node_Start.nodesExpanded)
            print("\n\n")

            # loop through prntArr and print out the desired information for each node on the Solution Path
            for n in reversed(prntArr):
                hn = int(n.weight) - int(n.depth)
                gn = n.depth
                print("The best state to expand is below with g(n) == ",
                      gn, " and h(n) == ", hn, "\n")
                print_Trench(n.state)
                print("Current Depth: ", n.depth)
                print("Time elapsed: ", n.time)
                print("Current Nodes Expanded: ", n.nodesExpanded)
                print("\n\n")

            print("Max Queue Size: ", maxQueueSize)
            print("\n\n")
            break

        # returns an array of all possible child state arrays
        expandArr = expand_State(currNode.state)
        # nodeCount = number of nodes expanded (searched)
        nodeCount += 1

        # append each new child state to the queue
        while len(expandArr) > 0:
            tmpNode = Node()
            tmpNode.set_State(expandArr.pop())
            tmpNode.set_Parent(currNode)
            tmpNode.set_NodesExpanded(nodeCount)
            tmpNode.set_Time(time.time() - start)

            if heuristic == 1:
                # UCS
                currHeuristic = 0
            elif heuristic == 2:
                # A* Misplaced Tile
                currHeuristic = get_Heuristic_Tile(tmpNode.state)
            elif heuristic == 3:
                # A* Manhattan Distance
                currHeuristic = get_Heuristic(tmpNode.state)

            tmpNode.set_Depth(int(currNode.depth) + 1)
            tmpNode.set_Weight(currHeuristic + tmpNode.depth)
            heapq.heappush(queue, (int(tmpNode.weight), tmpNode))
            # queue.append(tmpNode)

    return


def get_Heuristic_Tile(currState):
    ans = 0
    for i in range(0, 11):
        if (i == 4) or (i == 7) or (i == 10):
            continue
        if currState[i] != (i+1):
            ans += 1

    return ans


def get_Heuristic(currState):
    ans = 0
    tmpVal = 0
    d = {1: 0, 2: 1, 3: 2, 4: 3, 5: 5, 6: 6, 7: 8, 8: 9, 9: 11}
    for i in range(1, 10):

        tmpIndex = currState.index(i)
        if tmpIndex == 4 or tmpIndex == 7 or tmpIndex == 10:
            tmpIndex -= 1
            tmpVal = tmpIndex - d[i]
            if tmpVal < 0:
                tmpVal *= -1
            tmpVal += 1
        else:
            tmpVal = tmpIndex - d[i]
            if tmpVal < 0:
                tmpVal *= -1

        if 4 > min(tmpIndex, d[i]) and 4 < max(tmpIndex, d[i]):
            tmpVal -= 1
        if 7 > min(tmpIndex, d[i]) and 7 < max(tmpIndex, d[i]):
            tmpVal -= 1
        if 10 > min(tmpIndex, d[i]) and 10 < max(tmpIndex, d[i]):
            tmpVal -= 1
        ans += tmpVal
    return ans


def expand_State(currState):
    tmp = []
    returnArr = []

    for i in range(len(currState)):
        tmp = currState[:]
        j = i
        if currState[i] == 0:
            continue
        # case for index 0 (can only go right)
        if i == 0:
            while tmp[j+1] == 0:
                if (j+1 == 4 and tmp[j+1] == 0) or (j+1 == 7 and tmp[j+1] == 0) or (j+1 == 10 and tmp[j+1] == 0):
                    break
                elif(j+1 == 4 and tmp[j+1] != 0) or (j+1 == 7 and tmp[j+1] != 0) or (j+1 == 10 and tmp[j+1] != 0):
                    if tmp[j+2] == 0:
                        tmp[j+2], tmp[j] = tmp[j], tmp[j+2]
                        j += 2

                tmp[j+1], tmp[j] = tmp[j], tmp[j+1]
                j += 1
            returnArr.append(tmp)
            tmp = currState[:]

        # covers all positions with 2 possible moves (left or right)
        if i == 1 or i == 2:
            while tmp[j-1] == 0 and (j-1 >= 0):
                if(j-1 == 4) or (j-1 == 7) or (j-1) == 10:
                    if(tmp[j-2] == 0):
                        tmp[j-2], tmp[j] = tmp[j], tmp[j-2]
                        j -= 2
                        if(tmp[j+1] == 0):
                            break
                        else:
                            continue
                tmp[j-1], tmp[j] = tmp[j], tmp[j-1]
                j -= 1
            returnArr.append(tmp)
            tmp = currState[:]

            while tmp[i+1] == 0 and (j+1 <= 12):
                if (j+1 == 4 and tmp[j+1] == 0) or (j+1 == 7 and tmp[j+1] == 0) or (j+1 == 10 and tmp[j+1] == 0):
                    break
                elif(j+1 == 4 and tmp[j+1] != 0) or (j+1 == 7 and tmp[j+1] != 0) or (j+1 == 10 and tmp[j+1] != 0):
                    if tmp[j+2] == 0:
                        tmp[j+2], tmp[j] = tmp[j], tmp[j+2]
                        j += 2
                tmp[i+1], tmp[i] = tmp[i], tmp[i+1]
                j += 1
            returnArr.append(tmp)
            tmp = currState[:]

        # Move left 2 or right 1
        if i == 5 or i == 8 or i == 11:
            if tmp[i-2] == 0:
                tmp[i-2], tmp[i] = tmp[i], tmp[i-2]
                returnArr.append(tmp)
                tmp = currState[:]
            while tmp[i+1] == 0 and (j+1 <= 12):
                if (j+1 == 4 and tmp[j+1] == 0) or (j+1 == 7 and tmp[j+1] == 0) or (j+1 == 10 and tmp[j+1] == 0):
                    break
                elif(j+1 == 4 and tmp[j+1] != 0) or (j+1 == 7 and tmp[j+1] != 0) or (j+1 == 10 and tmp[j+1] != 0):
                    if tmp[j+2] == 0:
                        tmp[j+2], tmp[j] = tmp[j], tmp[j+2]
                        j += 2
                tmp[i+1], tmp[i] = tmp[i], tmp[i+1]
                j += 1
            returnArr.append(tmp)
            tmp = currState[:]

        # covers all positions with 3 possible moves (left, up (hole), right)
        if i == 3 or i == 6 or i == 9:
            if currState[i-1] == 0:
                tmp[i-1], tmp[i] = tmp[i], tmp[i-1]
                returnArr.append(tmp)
                tmp = currState[:]
            if currState[i+1] == 0:
                tmp[i+1], tmp[i] = tmp[i], tmp[i+1]
                returnArr.append(tmp)
                tmp = currState[:]
            if currState[i+2] == 0:
                tmp[i+2], tmp[i] = tmp[i], tmp[i+2]
                returnArr.append(tmp)
                tmp = currState[:]

        # covers all hole positions
        if i == 4 or i == 7 or i == 10:
            if currState[i-1] == 0:
                tmp[i-1], tmp[i] = tmp[i], tmp[i-1]
                returnArr.append(tmp)
                tmp = currState[:]
        # covers last position
        if i == 12:
            while tmp[j-1] == 0 and (j-1 >= 0):
                if(j-1 == 4) or (j-1 == 7) or (j-1) == 10:
                    if(tmp[j-2] == 0):
                        tmp[j-2], tmp[j] = tmp[j], tmp[j-2]
                        j -= 2
                        if(tmp[j+1] == 0):
                            break
                        else:
                            continue
                tmp[j-1], tmp[j] = tmp[j], tmp[j-1]
                j -= 1
            returnArr.append(tmp)
            tmp = currState[:]

    return returnArr


def print_Trench(trench_arr):
    x = " "
    arrTop = [x, x, x, 0, x, 0, x, 0, x, x]

    # set each indicy at 4,7,10 to the respective values in Trench_arr and then remove the indicies from the array.
    arrTop[3] = trench_arr[4]
    arrTop[5] = trench_arr[7]
    arrTop[7] = trench_arr[10]
    trench_arr.pop(4)
    trench_arr.pop(6)
    trench_arr.pop(8)

    for i in range(len(trench_arr)):
        print(arrTop[i], end=" ")
    print()
    for i in range(len(trench_arr)):
        print(trench_arr[i], end=" ")
    print("\n")
    return


if __name__ == '__main__':
    ProjectStart()

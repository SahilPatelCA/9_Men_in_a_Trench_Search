import sys
import time
import heapq


class Node(object):
    def __init__(self):

        self.state = []
        self.parent = None

    def set_State(self, state):
        self.state = state

    def set_Parent(self, parent):
        self.parent = parent

    def set_Weight(self, weight):
        self.weight = weight

    def set_Depth(self, depth):
        self.depth = depth

    def __lt__(self, w2):
        if self.weight < w2.weight:
            return True
        else:
            return False

    def __gt__(self, w2):
        if self.weight > w2.weight:
            return True
        else:
            return False


def ProjectStart():
    # problemBase = input(
    #     "Would you like to use the default puzzle or input your own? Enter '1' default or '2' custom:\n")
    # if problemBase == 1:
    #     # zero's represent blank spaces in the trench.
    #     trenchOrder = [0, 2, 3, 4, 0, 5, 6, 0, 7, 8, 0, 9, 1]
    # else:
    #     # allows the user to input one 13 number long string that mimicks the puzzle
    #     trenchOrder = list(map(int, input(
    #         "Enter the numbers 1-9 (using 0 for empty spots) (remember the indexs 4, 7, and 10 represent the holes in the trench). \n For example:[0,2,3,4,0(hole),5,6,0(hole),7,8,0(hole),9,1]: ").strip().split()))[:13]
    trenchOrder = [0, 2, 3, 4, 0, 5, 6, 0, 7, 8, 0, 9, 1]
    test = [1, 2, 3, 4, 0, 5, 6, 0, 7, 0, 8, 9, 0]
    testCorrect = [1, 2, 3, 4, 0, 5, 6, 0, 7, 8, 0, 9, 0]
    testing = [1, 2, 0, 0, 0, 0, 3, 5, 4, 6, 8, 7, 9]

    searchType = input(
        "What Search would you like? Type '1' for Uniform Cost Search, '2' for A* Misplaced Tile Heurisitic, or '3' for A* Manhattan Distance Heuristic:\n")

    # searchType is equal to the heuristic value

    start = time.time()
    # passes in the list and heuristic value
    General_Search(testing, searchType)
    end = time.time()
    print("Total Time: {}".format(end-start))  # prints total time of search
    return


def General_Search(puzzle, heuristic):
    ans = [1, 2, 3, 4, 0, 5, 6, 0, 7, 8, 0, 9, 0]  # Goal state
    Node_Start = Node()
    Node_Start.set_State(puzzle)
    Node_Start.set_Depth(0)
    queue = []
    expandArr = []
    nodeCount = 0
    maxQueueSize = 0
    depthCount = 0
    prntArr = []
    repeatStates = {}
    currHeuristic = 0

    # queue.append(Node_Start)
    heapq.heappush(queue, (0, Node_Start))

    while len(queue) > 0:

        if len(queue) > maxQueueSize:  # always updating the size of maxQueueSize
            maxQueueSize = len(queue)

        # currNode = queue.pop(0)  # Set the first state in the queue to currNode
        currNode = heapq.heappop(queue)[1]

        nodeCount += 1

        # checks if the state has been seen already. If so, skips the rest of the loop and restarts on next node.
        repeatStates[str(currNode.state)] = repeatStates.get(
            str(currNode.state), 0) + 1
        if repeatStates[str(currNode.state)] > 1:
            continue

        if currNode.state == ans:
            depthCount = currNode.depth
            # loops backwards tracing goal states parents until reaching start node
            while currNode.parent != None:
                # prntArr.append(currNode.state)
                hn = int(currNode.weight) - int(currNode.depth)
                gn = currNode.depth
                print("The best state to expand is below with g(n) == ",
                      gn, " and h(n) == ", currNode.weight)
                print_Trench(currNode.state)
                print("Current Depth: ", depthCount)
                depthCount -= 1
                print("\n\n")
                currNode = currNode.parent

            # while len(prntArr) > 0:
            #     print_Trench(prntArr.pop(0))
            #     print("Current Depth: ", depthCount)
            #     depthCount -= 1
            #     print("\n\n")
            print_Trench(Node_Start.state)
            print("Current Depth: ", 0)
            print("\n\n")
            print("Max Queue Size: ", maxQueueSize)
            print("Total Nodes Expanded: ", nodeCount)
            print("Total Depth: ", depthCount)
            break

        # returns an array of all possible child state arrays
        #print("currNode.state = ", currNode.state)
        expandArr = expand_State(currNode.state)
        #print("expandArr = ", expandArr)

        # append each new child state to the queue
        while len(expandArr) > 0:
            tmpNode = Node()
            tmpNode.set_State(expandArr.pop())
            tmpNode.set_Parent(currNode)

            if heuristic == 1:
                # UCS
                currHeuristic = 0
                print("UCS: ", currHeuristic)
            elif heuristic == 2:
                # A* Tile
                currHeuristic = get_Heuristic_Tile(tmpNode.state)
                print("TILE: ", currHeuristic)

            elif heuristic == 3:
                currHeuristic = get_Heuristic(tmpNode.state)
                print("MANHATTAN: ", currHeuristic)

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
            while currState[j+1] == 0:
                if (j+1 == 4 and tmp[j+1] == 0) or (j+1 == 7 and tmp[j+1] == 0) or (j+1 == 10 and tmp[j+1] == 0):
                    break
                elif(j+1 == 4 and tmp[j+1] != 0) or (j+1 == 7 and tmp[j+1] != 0) or (j+1 == 10 and tmp[j+1] != 0):
                    if currState[j+2] == 0:
                        tmp[j+2], tmp[j] = currState[j], currState[j+2]
                        j += 2

                tmp[j+1], tmp[j] = currState[j], currState[j+1]
                j += 1
            returnArr.append(tmp)
            tmp = currState[:]

        # covers all positions with 2 possible moves (left or right)
        if i == 1 or i == 2:
            while currState[j-1] == 0 and (j-1 >= 0):
                tmp[j-1], tmp[j] = currState[j], currState[j-1]
                j -= 1
            returnArr.append(tmp)
            tmp = currState[:]

            while currState[i+1] == 0 and (j+1 <= 12):
                if (j+1 == 4 and tmp[j+1] == 0) or (j+1 == 7 and tmp[j+1] == 0) or (j+1 == 10 and tmp[j+1] == 0):
                    break
                elif(j+1 == 4 and tmp[j+1] != 0) or (j+1 == 7 and tmp[j+1] != 0) or (j+1 == 10 and tmp[j+1] != 0):
                    if currState[j+2] == 0:
                        tmp[j+2], tmp[j] = currState[j], currState[j+2]
                        j += 2
                tmp[i+1], tmp[i] = currState[i], currState[i+1]
                j += 1
            returnArr.append(tmp)
            tmp = currState[:]

        # Move left 2 or right 1
        if i == 5 or i == 8 or i == 11:
            if currState[i-2] == 0:
                tmp[i-2], tmp[i] = currState[i], currState[i-2]
                returnArr.append(tmp)
                tmp = currState[:]
            while currState[i+1] == 0 and (j+1 <= 12):
                if (j+1 == 4 and tmp[j+1] == 0) or (j+1 == 7 and tmp[j+1] == 0) or (j+1 == 10 and tmp[j+1] == 0):
                    break
                elif(j+1 == 4 and tmp[j+1] != 0) or (j+1 == 7 and tmp[j+1] != 0) or (j+1 == 10 and tmp[j+1] != 0):
                    if currState[j+2] == 0:
                        tmp[j+2], tmp[j] = currState[j], currState[j+2]
                        j += 2
                tmp[i+1], tmp[i] = currState[i], currState[i+1]
                j += 1
            returnArr.append(tmp)
            tmp = currState[:]

        # covers all positions with 3 possible moves (left, up (hole), right)
        if i == 3 or i == 6 or i == 9:
            if currState[i-1] == 0:
                tmp[i-1], tmp[i] = currState[i], currState[i-1]
                returnArr.append(tmp)
                tmp = currState[:]
            if currState[i+1] == 0:
                tmp[i+1], tmp[i] = currState[i], currState[i+1]
                returnArr.append(tmp)
                tmp = currState[:]
            if currState[i+2] == 0:
                tmp[i+2], tmp[i] = currState[i], currState[i+2]
                returnArr.append(tmp)
                tmp = currState[:]

        # covers all hole positions
        if i == 4 or i == 7 or i == 10:
            if currState[i-1] == 0:
                tmp[i-1], tmp[i] = currState[i], currState[i-1]
                returnArr.append(tmp)
                tmp = currState[:]

        if i == 12:
            if currState[j-1] == 0:
                tmp[i-1], tmp[i] = currState[i], currState[i-1]
                returnArr.append(tmp)
                tmp = currState[:]

    return returnArr


def print_Trench(trench_arr):
    x = " "
    arrTop = [x, x, x, 0, x, 0, x, 0, x, x]

    # set each indicy at 4,7,10 to the respective values in Trench_arr and then remove the indicies from the array.
    arrTop[3] = trench_arr[4]
    # trench_arr.pop(4)
    arrTop[5] = trench_arr[7]
    # trench_arr.pop(4)
    arrTop[7] = trench_arr[10]
    trench_arr.pop(4)
    trench_arr.pop(6)
    trench_arr.pop(8)

    for i in range(len(trench_arr)):
        print(arrTop[i], end=" ")
    print("\n")
    for i in range(len(trench_arr)):
        print(trench_arr[i], end=" ")
    print("\n")
    return


if __name__ == '__main__':
    ProjectStart()

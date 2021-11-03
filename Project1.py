import sys
import time


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

    searchType = input(
        "What Search would you like? Type '1' for Uniform Cost Search, '2' for A* Misplaced Tile Heurisitic, or '3' for A* Manhattan Distance Heuristic:\n")

    # searchType is equal to the heuristic value

    start = time.time()
    # passes in the list and heuristic value
    ans = General_Search(trenchOrder, searchType)
    end = time.time()
    print("Total Time: {}".format(end-start))  # prints total time of search
    return ans


def General_Search(puzzle, heuristic):
    print_Trench(puzzle)
    return puzzle


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

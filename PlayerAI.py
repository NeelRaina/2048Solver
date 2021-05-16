from BaseAI import BaseAI

import math

import time


class PlayerAI(BaseAI):
    # global time variable to keep track of time
    startTime = None

    moveLength = None
    # global Alpha and beta pruning variables

    alphaVal = -math.inf
    betaVal = math.inf

    cornerMatrix = [[2048, 1024, 516, 128],
                    [16, 16, 16, 16],
                    [4, 4, 4, 4],
                    [1, 1, 1, 1]]

    @staticmethod
    def checkTime():
        timePassed = time.clock() - PlayerAI.startTime
        if timePassed > (.2 / PlayerAI.moveLength - .05):
            return True
        else:
            return False

    def getMove(self, grid):

        return PlayerAI.decision(grid)

    @staticmethod
    def decision(grid):

        # variables for best move and utility
        nextMove = None
        nextUtil = -math.inf

        moveList = grid.getAvailableMoves()
        PlayerAI.moveLength = len(moveList)
        for move in moveList:
            PlayerAI.startTime = time.clock()
            testGrid = grid.clone()
            testGrid.move(move)

            # getting the child grids into a list
            testChildren = list()
            testMoveList = testGrid.getAvailableMoves()
            for testMove in testMoveList:
                childGrid = testGrid.clone()
                childGrid.move(testMove)
                testChildren.append(childGrid)

            # convert algorithm into python code

            # maxChild, maxUtil = None, -math.inf

            for state in testChildren:
                maxChild, maxUtil = PlayerAI.maximize(state)

                if maxUtil > nextUtil:
                    nextMove = move
                    nextUtil = maxUtil

        return nextMove

    # maximize algo to python code
    @staticmethod
    def maximize(grid):
        if not grid.canMove() or PlayerAI.checkTime():
            return None, PlayerAI.evalState(grid)

        maxChild, maxUtil = None, -math.inf

        # create childList
        testChildren = list()
        moveList = grid.getAvailableMoves()
        for move in moveList:
            childGrid = grid.clone()
            childGrid.move(move)
            testChildren.append(childGrid)
        # calling minimize
        for state in testChildren:
            minChild, util = PlayerAI.minimize(state)

            # alpha beta pruning
            if util > maxUtil:
                maxChild, maxUtil = state, util

            if maxUtil >= PlayerAI.betaVal:
                break

            if maxUtil > PlayerAI.alphaVal:
                PlayerAI.alphaVal = maxUtil

        return maxChild, maxUtil

    # minimize algo to python code
    @staticmethod
    def minimize(grid):

        if PlayerAI.checkTime() or not grid.canMove():
            return None, PlayerAI.evalState(grid)

        minChild, minUtil = None, math.inf

        tileChildren = list()
        tileList = grid.getAvailableCells()
        # minimize places tiles randomly
        for tile in tileList:
            tileGrid = grid.clone()
            tileGrid.setCellValue(tile, 2)
            tileChildren.append(tileGrid)

            tileGrid = grid.clone()
            tileGrid.setCellValue(tile, 4)
            tileChildren.append(tileGrid)

        for state in tileChildren:
            maxChild, util = PlayerAI.maximize(state)

            if util < minUtil:
                minChild, minUtil = state, util

            if minUtil <= PlayerAI.alphaVal:
                break

            if minUtil < PlayerAI.betaVal:
                PlayerAI.betaVal = minUtil

        return minChild, minUtil

    @staticmethod
    def evalState(grid):

        # The three heuristics I've decided on are smoothness and monotonicity and available number of cells
        availableCells = (len(grid.getAvailableCells()) - 15)/(len(grid.getAvailableCells()) + .01)

        availCellsWeight = 1.0

        maxValue = (grid.getMaxTile())
        maxWeight = 1.0

        cornerMap = PlayerAI.maxTileMap(grid)
        cornerMapWeight = 4.0


        # + (mono * monoWeight) + (smooth * smoothWeight)
        result = availableCells * availCellsWeight + \
                 maxValue * maxWeight + \
                 cornerMap * cornerMapWeight


        return result



    @staticmethod
    def maxTileMap(grid):
        value = 0
        for x in range(grid.size):
            for y in range(grid.size):
                value += grid.map[x][y] * PlayerAI.cornerMatrix[x][y]

        return value


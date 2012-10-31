from random import choice
from snakegame.common import *

def bfs(board, x, y, find):
    nodes=[[1, 0, x, y, ""]]
    #node format is [1=nothing 0=apple (for sorting reasons),
    #distance from start, x, y, dirs useed to get there, find apple, or nothing
    height=len(board)
    width = len(board[0])
    if find == "a":
        condition = "found < 8"
    elif find == "s":
        condition = "len(nodes) < 300"
    else:
        condition = "len(nodes) < 51"
    TARGET="*"
    ENTRY="."
    DIRS={"U":[-1,0], "D":[1,0], "L":[0,-1], "R":[0,1]}
    found=steps=0
    explored=[]
    checker=[]
    while eval(condition):
        steps+=1
        todo=[]
        for node in nodes:
            if node not in explored:
                x,y, prevdir=node[2],node[3], node[4]
                for dr, (dy, dx) in DIRS.items():
                    nx=(x+dx)%height
                    ny=(y+dy)%width
                    if board[ny][nx] == ENTRY:
                        a=[1, steps, nx, ny, (prevdir+dr)]
                        if a[2:4] not in checker:
                            todo.append(a)
                            checker.append(a[2:4])
                    elif board[ny][nx] == TARGET:
                        a=[0, steps, nx, ny, (prevdir+dr)]
                        if a[2:4] not in checker:
                            todo.append(a)
                            checker.append(a[2:4])
                            found+=1
                explored.append(node)
        if not todo:
            break
        for item in todo:
            nodes.append(item)
    if find == "a":
        if sorted(nodes)[0][0]==0:
            return sorted(nodes)
        else: return " " + str(nodes)
    elif find == "s":
        return nodes
    else:
        return len(nodes)-1

def best_no_app(choices):
        options={"U":0, "D":0, "L":0, "R":0}
        for choice in choices: #finding dr with most places
            if choice[-1]:
                chose=choice[-1][0]
                options[chose]+=1
        rec=0
        win = "U"
        for dr, num in options.items():
            if num > rec:
                rec=num
                win=dr
        return win

def win(tries, safety):
    record=200
    win=""
    for item in safety:
        stats, moves=item[0], item[1]
        if moves > tries:
            if stats[1] < record:
                record= stats[1]
                win=stats[4][0]
    return win

def best_with_app(board, choices, x, y, w, h):
        safety=[]
        for item in choices:
            if item[-1] and not item[0]:
                xy=directions[item[-1][0]]
                moves=bfs(board, (xy[0]+x)%w, (xy[1]+y)%h, "")
                safety.append([item, moves])
        bad=1
        for item in safety:
            dirs=directions[item[0][-1][0]]
            if bfs(board, x+dirs[0], y+dirs[1], "") > 49:
                bad=0
        if bad:
            return best_no_app(choices)
        else:
            dr=win(20, safety)
            if dr:
                return dr
        return "U"
            
def matt_old_bot(board, (x,y)):
    h=len(board)
    w=len(board[0])
    choices = bfs(board, x, y, "a") #finds apples. If no apples, finds moves
    if "[" != str(choices)[0]: #no apples reachable
        return best_no_app(eval(choices[1:])) #safety mode
    else: #there are apples
        return best_with_app(board, choices, x, y, w, h)
    
def safe_bot(board, (x,y)):
    enemies=0
    me=board[y][x]
    good = ".*"+me+me.lower()
    for line in board:
        for item in line:
            if item not in good:
                enemies=1
    if enemies:
        choices=bfs(board, x, y, "s")
        return best_no_app(choices)
    else:
        return matt_old_bot(board, (x,y))
# Test code to run the snake game.
# Leave the if statement as is, otherwise I won't be able to run your bot with
# the other bots.
if __name__ == '__main__':
	p = PygletSnakeEngine(25, 25, 50, wrap=True)
	p.add_bot(matt_bot)
	p.add_bot(safe_bot)
	p.run()

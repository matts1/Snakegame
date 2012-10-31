from snakegame.common import *
from random import choice

def conv((x, y)):
	return (W * y) + x

def find(n):
	global PAR
	if n == PAR[n]:
		return n
	else:
		PAR[n] = find(PAR[n])
		return PAR[n]

cfind = lambda x: find(conv(x))

def join(a, b):
	global PAR, RANK, SIZE
	pa = cfind(a)
	pb = cfind(b)
	if pa == pb:
		return
	if RANK[pa] < RANK[pb]:
		PAR[pa] = pb
		SIZE[pb] += SIZE[pa]
	elif RANK[pb] < RANK[pa]:
		PAR[pb] = pa
		SIZE[pa] += SIZE[pb]
	else:
		PAR[pb] = pa
		RANK[pa] += 1
		SIZE[pa] += SIZE[pb]
	
def axisdis(a, b, tot):
	lo, hi = sorted([a, b])
	return min(hi - lo, tot - hi + lo)

def dis((ax, ay), (bx, by)):
	return axisdis(ax, bx, W) + axisdis(ay, by, H)

def unionfind_bot(board, pos):
	(x, y) = pos
	me = board[y][x]
	global H, W, PAR, RANK, SIZE
	H = len(board)
	W = len(board[0])
	enemies = apple = False
	mylen = 0
	for y in xrange(H):
		for x in xrange(W):
			if board[y][x] not in "*.":
				if board[y][x].upper() == me:
					mylen += 1
				else:
					enemies = True

	RANK = [0] * (H * W)
	SIZE= [1] * (H * W)
	PAR = []
	for i in xrange(H * W):
		PAR.append(i)

	seen = []
	for y in xrange(H):
		seen.append([False] * W)
	seen[y][x] = True

	q = [pos]
	ptr = 0
	while ptr < len(q):
		x, y = q[ptr]
		ptr += 1
		for dir in directions.values():
			nx = (x + dir[0]) % W
			ny = (y + dir[1]) % H
			if board[ny][nx] in ".*" and not seen[ny][nx]:
				seen[ny][nx] = True
				q.append((nx, ny))
				if not apple and board[y][x] == "*":
					apple = (x, y)
				if pos != (x, y):
					join((nx, ny), (x, y))
			elif seen[ny][nx] and pos != (x, y):
				join((nx, ny), (x, y))

	x, y = pos
	hi = 0
	for dir in directions:
		nx = (x + directions[dir][0]) % W
		ny = (y + directions[dir][1]) % H
		n = cfind((nx, ny))
		hi = max(hi, SIZE[n])

	poss = []
	good = []
	for dir in "DRUL":
		nx = (x + directions[dir][0]) % W
		ny = (y + directions[dir][1]) % H
		if SIZE[cfind((nx, ny))] == hi:
			poss.append((dir, board[ny][nx]))
	
	for (dir, loc) in poss:
		if mylen < H and not enemies:
			#if we can't wrap around yet but there aren't enemies about
			if apple:
				nx = (x + directions[dir][0]) % W
				ny = (y + directions[dir][1]) % H
				if dis((nx, ny), apple) < dis((x, y), apple):
					return dir
		elif enemies:
			if loc == ".":
				good.append(dir)
		else:
			if hi == 1 and mylen == H * W - 1:
				print "matt_bot covered the board :D"
			return dir
	if good:
		return choice(good)
	elif enemies and mylen == 1:
		for dir in "DRUL":
			nx = (x + directions[dir][0]) % W
			ny = (y + directions[dir][1]) % H
			if SIZE[cfind((nx, ny))] >= 2:
				if board[ny][nx] == ".":
					return dir
		
	if hi == 0:
		print "Going down"
	return choice(poss)[0]


if __name__ == '__main__':
	from snakegame.engines.pyglet import PygletEngine
	import old_matt
	engine = PygletEngine(20, 20, 15)

	engine.add_bot(unionfind_bot)
	for i in range(25):
		engine.add_bot(old_matt.safe_bot)
	
	engine.run()

import string
import queue
import numpy as np
import sys


def applyMove(move, state) :
	turns = move % 3 + 1	#move对3求余+1  旋转90°的次数
	face = move // 3		#move除3取整    定义旋转哪一个面
	face_i = 0
	copyState = state.copy()
	while turns:		#顺时针旋转turns个90°
		turns -= 1
		lastState = copyState.copy()

		for i in [0,1,2,3] :	#在旋转过程中分别对4个角块的方向进行赋值
			target = affectedCubies[face][i]
			if (i & 3) == 3:
				killer_i = i-3
			if (i & 3) != 3:
				killer_i = i+1
			killer = affectedCubies[face][killer_i]		##将面按顺序的下一个角块的值取出来（用于移位）
			if face < 2:
				face_i = 0
			if face >= 2:
				face_i = 2 - (i & 1)
			orientationDelta = face_i		#顺时针旋转后方向改变量（0.1.2）
			copyState[target] = lastState[killer]		#用后一个替换前一个，完成顺时针旋转
			copyState[target + 8] = lastState[killer + 8] + orientationDelta	#记录旋转后方向的值
			if not turns :		#如果turns!=0即还要旋转，则不进入；若turns==0，则进入求余，防止方向值超过（0.1）或（0.1.2）
				copyState[target + 8] %= 3	#角块和3求余，不改变方向的值
	return copyState

def inverse(move) :
	move = 0 if move is None else move
	return move + 2 - 2 * (move % 3)



phase=1

applicableMoves = [ 0, 259263, 74943, 74898 ]	#分别为0，111111010010111111，10010010010111111，10010010010010010
affectedCubies = [
	[ 0,  1,  2,  3 ],	#U
	[ 4,  5,  6,  7 ],	#D
	[ 0,  3,  5,  4 ],	#F
	[ 2,  1,  7,  6 ],	#B
	[ 3,  2,  6,  5 ],	#L
	[ 1,  0,  4,  7 ],	#R
]
answer=[]

'''
对state状态进行旋转(顺时针90°180°270°)，返回旋转后的状态
move=0时，U面顺时针旋转90°move=1时，U面顺时针旋转180°move=2时，U面顺时针旋转270°
move=3时，D面顺时针旋转90°move=4时，D面顺时针旋转180°move=5时，D面顺时针旋转270°
move=6时，F面顺时针旋转90°move=7时，F面顺时针旋转180°move=8时，F面顺时针旋转270°
move=9时，B面顺时针旋转90°move=10时，B面顺时针旋转180°move=11时，B面顺时针旋转270°
move=12时，L面顺时针旋转90°move=13时，L面顺时针旋转180°move=14时，L面顺时针旋转270°
move=15时，R面顺时针旋转90°move=16时，R面顺时针旋转180°move=17时，R面顺时针旋转270°
'''

def nid(state) :	#取出输入状态的方向的值id
	if phase < 2 :	#第一步：角块方向
		result = state[8:16]	#取角块的方向值给result
		return result	#返回角块的方向（0.1.2）

	if phase < 3 :	#第二步：角块校验
		result=[0,0]
		for c in [0,1,2,3,4,5,6,7] :
			result[0] |= (state[c]& 5) << (3 * c)	#result[0]用24位存放8个角块的位置
		for i in range(0,8) :
			for j in range(i+1,8) :
				result[1] ^= state[i] > state[j]	#result[1]=0表示角块方向正确，result[2]=1表示角块方向错误
		return result

	return state

def main() :
	count = 0
	mark = 0
	argv = [ "LFU", "LUB", "DBR", "DFL", "FRU", "DLB","RBU", "RFD" ]	#输入魔方的状态，对照目标状态进行输入
	goal = [ "UFR", "URB", "UBL", "ULF", "DRF", "DFL", "DLB", "DBR" ]
	# 准备当前（开始）和目标状态
	currentState = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	goalState= [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	for i in [0,1,2,3,4,5,6,7] :	#将当前魔方状态输入到数表currentState里，由字母顺序转化到数字顺序，字母顺序包涵了位置和方向，数字顺序用一位表示位置，一位表示方向。
									# 规则为：0-7存按goal里编号角块的数字位置，8-15存角块的方向，角块如需旋转，则顺时针旋转90°记为1，顺时针旋转180°记为2
		goalState[i] = i		#初始化目标魔方各个楞块和角块的位置
		cubie = argv[i]			#遍历输入的argv中的8个块
		switch = 0
		for j in [0, 1, 2, 3, 4, 5, 6, 7]:
			if goal[j] == cubie:
				currentState[i] = j
				switch = 1
			if j == 7 and switch == 0:
				currentState[i] = 8
		while currentState[i]== 8:		#和目标魔方块的位置比较，块需要顺时针旋转90°
			cubie = cubie[1]+cubie[2] + cubie[0]
			currentState[i + 8] += 1		#记录到方向，回到正确位置需要顺时针旋转180°为2，顺时针旋转90°为1
			for j in [0, 1, 2, 3, 4, 5, 6, 7]:
				if goal[j] == cubie:
					currentState[i] = j
					switch = 1
				if j == 7 and switch == 0:
					currentState[i] = 8


	global phase	#开始西斯尔思韦特操作，循环四个过程
	while phase < 4 :
		currentId = nid(currentState)		#计算当前和目标状态的方向取值id，如果相等(表明方向正确，不需要调整)则跳过
		goalId = nid(goalState)
		if currentId == goalId:
			continue

		q = queue.Queue()		#初始化BFS（广度优先）队列（先进先出）
		q.put(currentState)
		q.put(goalState)
		# 初始化BFS算法的图表	map通过平衡二叉树对节点进行存储
		predecessor={}		#旋转前后的状态表存进predecessor，旋转后的表前面出现过则不存（即状态等价不存）
		direction={tuple(currentId):1,tuple(goalId):2}	#direction：存放不同状态的方向，该状态由输入魔方旋转得到，则关键字为1；有目标魔方旋转得到，关键字为2
		lastMove={}		#lastMove：将旋转后的方向值存入并记录当时的move值(即旋转的方式）
		# 开始BFS算法
		while 1 :		#从队列获取状态，计算它的ID并得到它的方向
			oldState = q.get()
			oldId = nid(oldState)
			if direction.get(tuple(oldId)) is None:
				direction[tuple(oldId)] = 0
				oldDir = 0
			else:
				oldDir = direction[tuple(oldId)]


			for move in range(0,18) :		#将所有适用的动作(每个面旋转90.180.270)应用到它并记录新的状态
				if (applicableMoves[phase] & (1 << move)) :	#在phase=2时，控制FBLR面只能旋转180°即降群到<U,D,F2,B2,L2,R2>；在phase=3时，控制UDFBLR面只能旋转180°即降群到<U2,D2,F2,B2,L2,R2>
					newState = applyMove(move, oldState)
					newId = nid(newState)
					if direction.get(tuple(newId)) is None:
						direction[tuple(newId)] = 0
						newDir = 0
					else :
						newDir = direction[tuple(newId)]
					lastnewId = newId.copy()
					count +=1
					# 判断是否能和关键字为2的状态联系起来，如果能，则找到解法，否，则继续搜索
					if newDir and (newDir != oldDir) :	#由目标魔方旋转后的状态的方向值与输入魔方某一状态的方向值相等时if成立
						if oldDir > 1:					#oldId表示之前的状态的方向，newId表示旋转后的状态的方向值，搜索解法
							newId, oldId = oldId,newId
							move = inverse(move)

						algorithm=[move]			#重现联系这两个状态的步骤move
						while oldId != currentId:	#在predecessor表里查找oldId==currentId，并记录需要的步骤到algorithm（算法）
							if lastMove.get(tuple(oldId)) is None:
								lastMove[tuple(oldId)] = 0
								algorithm.insert(0, 0)
							else :
								algorithm.insert(0, lastMove[tuple(oldId)])

							if predecessor.get(tuple(oldId)) is None:
								predecessor[tuple(oldId)] = [0]
								oldId = [0]
							else:
								oldId = predecessor[tuple(oldId)]

						while newId != goalId:		#还原到目标魔方状态需要转动的步骤
							if lastMove.get(tuple(newId)) is None:
								lastMove[tuple(newId)] = 0
								algorithm.append(inverse(0))
							else:
								algorithm.append(inverse(lastMove[tuple(newId)]))

							if predecessor.get(tuple(newId)) is None:
								predecessor[tuple(newId)] = [0]
								newId = [0]
							else:
								newId = predecessor[tuple(newId)]


						for i in range(0,np.size(algorithm)):
							print( "UDFBLR"[algorithm[i] // 3] , end = '')	#打印需要旋转的面和角度，1.2.3顺时针旋转90.180.270
							print(algorithm[i] % 3 + 1,end = '')
							answer.append(algorithm[i])
							currentState = applyMove(algorithm[i], currentState)	#旋转后的值赋给currentState（当前值）
						phase += 1
						mark = 1
						break

					if not newDir:
						q.put(newState)
						newDir = oldDir
						direction[tuple(lastnewId)] = oldDir
						lastMove[tuple(newId)] = move
						predecessor[tuple(newId)] = oldId
			if mark == 1:
				mark = 0
				break

main()



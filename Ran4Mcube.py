import string
import numpy as np
N=4
MOV=11
NEGX = -1
POSX = 1
NEGY = -2
POSY = 2
NEGZ = -3
POSZ = 3
ERR_NOTINITED = 1
ERR_MISPAINTED = 2
ERR_NONDESCRIPT = 3
ERR_PARITY_EDGE_FLIP = 4
ERR_PARITY_CORNER_ROTATION = 5
ERR_PARITY_CORNER_BACKWARD = 6
ERR_PARITY_CENTER_SWAP = 7
SHORTEN_NONE = 0
SHORTEN_STRIP_SOME = 1
SHORTEN_STRIP_ALL = 2
SHORTEN_STRIP_ROTATE_SOME = 3
SHORTEN_STRIP_ROTATE_ALL = 4
ITER_THRESHOLD = 10



class mcube(object):
    version = "20051216"
    numcubes = 0
    mov=[0,0,0,0,0,0,0,0,0,0,0,0]
    cube = np.zeros((6,6,6),dtype=int)
    inited = 0
    erval=0
    shorten=0
    fx=0;fy=0;fz=0
    solution=""
    def __init__(self):
        mcube.shorten = SHORTEN_STRIP_ROTATE_ALL
        mcube.erval = 0
        warnval = 0
        solution = ""
        mcube.resetcube(self)
        mcube.numcubes += 1

    def __del__(self):
        mcube.numcubes -= 1
#重定义==
    def __eq__(self, q):
         for i in range(1,N+1):
             for j in range(1,N+1):
                if q.cube[i][N+1][j] != cube[i][N+1][j] or q.cube[0][i][j] != cube[0][i][j] or q.cube[i][j][0] != cube[i][j][0] or q.cube[N+1][i][j] != cube[N+1][i][j] or q.cube[i][j][N+1] != cube[i][j][N+1] or q.cube[i][0][j] != cube[i][0][j] :
                    return False
         return True

#重定义！=
    def __ne__(self, q):
        return not __eq__(q)

    def DOMOVES(a, b):
        mcube.domoves(b)
        a += b

    def GETCORNER_C(a, b, c, x, y, z, f):
        f = mcube.findcorner_c(a, b, c)
        x = mcube.fx;
        y = mcube.fy;
        z = mcube.fz

    def GETCORNER_A(a, b, c, x, y, z, f):
        f = mcube.findcorner_a(a, b, c)
        x = mcube.fx;
        y = mcube.fy;
        z = mcube.fz
#指向魔方数组的指针
    def face(x,y,z):
        if x < 0 or x > N+1 or y < 0 or y > N+1 or z < 0 or z > N+1 :
            return None
        return id(mcube.cube[x][y][z])

#展示魔方表
    def renderscreen():
        print(
"\
          %i %i %i %i\n\
          %i %i %i %i\n\
          %i %i %i %i\n\
          %i %i %i %i\n\
 %i %i %i %i  %i %i %i %i  %i %i %i %i  %i %i %i %i\n\
 %i %i %i %i  %i %i %i %i  %i %i %i %i  %i %i %i %i\n\
 %i %i %i %i  %i %i %i %i  %i %i %i %i  %i %i %i %i\n\
 %i %i %i %i  %i %i %i %i  %i %i %i %i  %i %i %i %i\n\
          %i %i %i %i\n\
          %i %i %i %i\n\
          %i %i %i %i\n\
          %i %i %i %i\n\
",
mcube.cube[1][5][4], mcube.cube[2][5][4], mcube.cube[3][5][4], mcube.cube[4][5][4],
mcube.cube[1][5][3], mcube.cube[2][5][3], mcube.cube[3][5][3], mcube.cube[4][5][3],
mcube.cube[1][5][2], mcube.cube[2][5][2], mcube.cube[3][5][2], mcube.cube[4][5][2],
mcube.cube[1][5][1], mcube.cube[2][5][1], mcube.cube[3][5][1], mcube.cube[4][5][1],
mcube.cube[0][4][4], mcube.cube[0][4][3], mcube.cube[0][4][2], mcube.cube[0][4][1],
mcube.cube[1][4][0], mcube.cube[2][4][0], mcube.cube[3][4][0], mcube.cube[4][4][0],
mcube.cube[5][4][1], mcube.cube[5][4][2], mcube.cube[5][4][3], mcube.cube[5][4][4],
mcube.cube[4][4][5], mcube.cube[3][4][5], mcube.cube[2][4][5], mcube.cube[1][4][5],
mcube.cube[0][3][4], mcube.cube[0][3][3], mcube.cube[0][3][2], mcube.cube[0][3][1],
mcube.cube[1][3][0], mcube.cube[2][3][0], mcube.cube[3][3][0], mcube.cube[4][3][0],
mcube.cube[5][3][1], mcube.cube[5][3][2], mcube.cube[5][3][3], mcube.cube[5][3][4],
mcube.cube[4][3][5], mcube.cube[3][3][5], mcube.cube[2][3][5], mcube.cube[1][3][5],
mcube.cube[0][2][4], mcube.cube[0][2][3], mcube.cube[0][2][2], mcube.cube[0][2][1],
mcube.cube[1][2][0], mcube.cube[2][2][0], mcube.cube[3][2][0], mcube.cube[4][2][0],
mcube.cube[5][2][1], mcube.cube[5][2][2], mcube.cube[5][2][3], mcube.cube[5][2][4],
mcube.cube[4][2][5], mcube.cube[3][2][5], mcube.cube[2][2][5], mcube.cube[1][2][5],
mcube.cube[0][1][4], mcube.cube[0][1][3], mcube.cube[0][1][2], mcube.cube[0][1][1],
mcube.cube[1][1][0], mcube.cube[2][1][0], mcube.cube[3][1][0], mcube.cube[4][1][0],
mcube.cube[5][1][1], mcube.cube[5][1][2], mcube.cube[5][1][3], mcube.cube[5][1][4],
mcube.cube[4][1][5], mcube.cube[3][1][5], mcube.cube[2][1][5], mcube.cube[1][1][5],
mcube.cube[1][0][1], mcube.cube[2][0][1], mcube.cube[3][0][1], mcube.cube[4][0][1],
mcube.cube[1][0][2], mcube.cube[2][0][2], mcube.cube[3][0][2], mcube.cube[4][0][2],
mcube.cube[1][0][3], mcube.cube[2][0][3], mcube.cube[3][0][3], mcube.cube[4][0][3],
mcube.cube[1][0][4], mcube.cube[2][0][4], mcube.cube[3][0][4], mcube.cube[4][0][4]
  )
#返回魔方解法

    def issolved():
        c=[0,0,0,0,0,0,0]
        d=0
        c[1] = mcube.cube[1][N+1][1]
        c[2] = mcube.cube[0][1][1]
        c[3] = mcube.cube[1][1][0]
        c[4] = mcube.cube[N+1][1][1]
        c[5] = mcube.cube[1][1][N+1]
        c[6] = mcube.cube[1][0][1]
        for i in range(1,7):
            d = 0
            for j in range(1,7):
                if c[i] == j:
                    d += 1
            if d != 1 :
                return False
        for i in range(1,N+1):
            for j in range(1,N+1):
                if mcube.cube[i][N+1][j] != c[1] or mcube.cube[0][i][j] != c[2] or mcube.cube[i][j][0] != c[3] or mcube.cube[N+1][i][j] != c[4] or mcube.cube[i][j][N+1] != c[5] or mcube.cube[i][0][j] != c[6]:
                    return False
        return True

#重置魔方
    def resetcube(self):
        solution = "";
        for i in range(0,MOV+1):
            mcube.mov[i] = 0
        for i in range(0,N+2):
            for j in range(0,N+2):
                for k in range(0,N+2):
                    mcube.cube[i][j][k] = 0
        for i in range(1,N+1):
            for j in range(1,N+1):
                mcube.cube[i][N+1][j] = 1
                mcube.cube[0][i][j]   = 2
                mcube.cube[i][j][0]   = 3
                mcube.cube[N+1][i][j] = 4
                mcube.cube[i][j][N+1] = 5
                mcube.cube[i][0][j]   = 6
        mcube.erval = 0
        warnval = 0
        mcube.fx = 0
        mcube.fy = 0
        mcube.fz = 0
        mcube.inited = True

#向左旋转所给层
    def slice_l(s):
        if s < 1 or s > N:
            return None
        temp=np.zeros((N+2,N+2,N+2),dtype=int)
        for i in range(0,N+2):
            for j in range(0,N+2):
                for k in range(0,N+2):
                    temp[i][j][k] = mcube.cube[i][j][k]
        for i in range(1,N+1):
            if s == 1:
                for j in range(1,N+1):
                    mcube.cube[i][0][j] = temp[N+1-j][0][i]
            elif s == N:
                for j in range(1,N+1):
                    mcube.cube[i][N+1][j] = temp[N+1-j][N+1][i]
            mcube.cube[i][s][0]   = temp[N+1][s][i]
            mcube.cube[i][s][N+1] = temp[0][s][i]
            mcube.cube[0][s][i]   = temp[N+1-i][s][0]
            mcube.cube[N+1][s][i] = temp[N+1-i][s][N+1]

#向右旋转所给层
    def slice_r(s):
        if s < 1 or s > N:
            return  None
        temp=np.zeros((N+2,N+2,N+2),dtype=int)
        for i in range(0,N+2):
            for j in range(0,N+2):
                for k in range(0,N+2):
                    temp[i][j][k] = mcube.cube[i][j][k]
        for i in range(1,N+1):
            if s == 1 :
                for j in range(1,N+1):
                    mcube.cube[i][0][j] = temp[j][0][N+1-i]
            elif s == N :
                for j in range(1,N+1):
                    mcube.cube[i][N+1][j] = temp[j][N+1][N+1-i]
            mcube.cube[i][s][0]   = temp[0][s][N+1-i]
            mcube.cube[i][s][N+1] = temp[N+1][s][N+1-i]
            mcube.cube[0][s][i]   = temp[i][s][N+1]
            mcube.cube[N+1][s][i] = temp[i][s][0]

#向上旋转所给层
    def slice_u(s):
        if s < 1 or s > N:
            return  None
        temp=np.zeros((6,6,6),dtype=int)
        for i in range(0,N+2):
             for j in range(0,N+2):
                for k in range(0,N+2):
                    temp[i][j][k] = mcube.cube[i][j][k]
        for i in range(1,N+1):
            if s == 1:
                for j in range(1,N+1):
                    mcube.cube[0][i][j] = temp[0][j][N+1-i]
            if s == N:
                for j in range(1,N+1):
                    mcube.cube[N+1][i][j] = temp[N+1][j][N+1-i]
            mcube.cube[s][i][0]   = temp[s][0][N+1-i]
            mcube.cube[s][i][N+1] = temp[s][N+1][N+1-i]
            mcube.cube[s][0][i]   = temp[s][i][N+1]
            mcube.cube[s][N+1][i] = temp[s][i][0]

#向下旋转所给层
    def slice_d(s):
        if s < 1 or s > N :
            return None
        temp=np.zeros((N+2,N+2,N+2),dtype=int);
        for i in range(0, N + 2):
            for j in range(0, N + 2):
                for k in range(0, N + 2):
                    temp[i][j][k] = mcube.cube[i][j][k]
        for i in range(1,N+1):
            if s == 1:
                for j in range(1,N+1):
                    mcube.cube[0][i][j] = temp[0][N+1-j][i]
            if s == N:
                for j in range(1,N+1):
                    mcube.cube[N+1][i][j] = temp[N+1][N+1-j][i]
            mcube.cube[s][i][0]   = temp[s][N+1][i]
            mcube.cube[s][i][N+1] = temp[s][0][i]
            mcube.cube[s][0][i]   = temp[s][N+1-i][0]
            mcube.cube[s][N+1][i] = temp[s][N+1-i][N+1]

#顺时针旋转所给层
    def slice_c(s):
        if s < 1 or s > N:
            return None
        temp=np.zeros((N+2,N+2,N+2),dtype=int)
        for i in range(0, N + 2):
            for j in range(0, N + 2):
                for k in range(0, N + 2):
                    temp[i][j][k] = mcube.cube[i][j][k]
        for i in range(1,N+1):
            if s == 1:
                for j in range(1,N+1):
                    mcube.cube[i][j][0] = temp[N+1-j][i][0]
            if s == N:
                for j in range(1,N+1):
                    mcube.cube[i][j][N+1] = temp[N+1-j][i][N+1]
            mcube.cube[i][0][s]   = temp[N+1][i][s]
            mcube.cube[i][N+1][s] = temp[0][i][s]
            mcube.cube[0][i][s]   = temp[N+1-i][0][s]
            mcube.cube[N+1][i][s] = temp[N+1-i][N+1][s]

#逆时针旋转所给层
    def slice_a(s):
        if s < 1 or s > N:
            return None
        temp=np.zeros((N+2,N+2,N+2),dtype=int)
        for i in range(0, N + 2):
            for j in range(0, N + 2):
                for k in range(0, N + 2):
                    temp[i][j][k] = mcube.cube[i][j][k]
        for i in range(1,N+1):
            if s == 1:
                for j in range(1,N+1):
                    mcube.cube[i][j][0] = temp[j][N+1-i][0]
            if s == N:
                for j in range(1,N+1):
                    mcube.cube[i][j][N+1] = temp[j][N+1-i][N+1]
            mcube.cube[i][0][s]   = temp[0][N+1-i][s]
            mcube.cube[i][N+1][s] = temp[N+1][N+1-i][s]
            mcube.cube[0][i][s]   = temp[i][N+1][s]
            mcube.cube[N+1][i][s] = temp[i][0][s]

#定义魔方旋转函数
    #下面为旋转单层
    def UL():
        mcube.slice_l(N)
    def UR():
        mcube.slice_r(N)
    def DL():
        mcube.slice_l(1)
    def DR():
        mcube.slice_r(1)
    def LU():
        mcube.slice_u(1)
    def LD():
        mcube.slice_d(1)
    def RU():
        mcube.slice_u(N)
    def RD():
        mcube.slice_d(N)
    def FC():
        mcube.slice_c(1)
    def FA():
        mcube.slice_a(1)
    def BC():
        mcube.slice_c(N)
    def BA():
        mcube.slice_a(N)
    def uL():
        mcube.slice_l(N-1)
    def uR():
        mcube.slice_r(N-1)
    def dL():
        mcube.slice_l(2)
    def dR():
        mcube.slice_r(2)
    def lU():
        mcube.slice_u(2)
    def lD():
        mcube.slice_d(2)
    def rU():
        mcube.slice_u(N-1)
    def rD():
        mcube.slice_d(N-1)
    def fC():
        mcube.slice_c(2)
    def fA():
        mcube.slice_a(2)
    def bC():
        mcube.slice_c(N-1)
    def bA():
        mcube.slice_a(N-1)
    #下面为魔方整体旋转
    def CL():
        for i in range(1,N+1):
            mcube.slice_l(i)
    def CR():
        for i in range(1,N+1):
            mcube.slice_r(i) 
    def CU():
        for i in range(1,N+1):
            mcube.slice_u(i)
    def CD():
        for i in range(1,N+1):
            mcube.slice_d(i)
    def CC():
        for i in range(1,N+1):
            mcube.slice_c(i) 
    def CA():
        for i in range(1,N+1):
            mcube.slice_a(i)
        #下面为旋转单层两次
    def U2():
        mcube.UL()
        mcube.UL() 
    def D2():
        mcube.DR()
        mcube.DR() 
    def L2():
        mcube.LD()
        mcube.LD() 
    def R2():
        mcube.RU()
        mcube.RU() 
    def F2():
        mcube.FC()
        mcube.FC()  
    def B2():
        mcube.BA()
        mcube.BA()  
    def u2():
        mcube.uL()
        mcube.uL() 
    def d2():
        mcube.dR()
        mcube.dR()  
    def l2():
        mcube.lD()
        mcube.lD()  
    def r2():
        mcube.rU()
        mcube.rU()  
    def f2():
        mcube.fC()
        mcube.fC()  
    def b2():
        mcube.bA()
        mcube.bA() 
# 结束定义
# 打乱魔方
    def scramblecube():
        axis_direction, slice
  # 根据魔方大小对大量随机移动进行更好的计算
        nummoves = (N-2)*25+10
        nummoves += rand() % nummoves
        resetcube()
        for i in range(1, nummoves+1):
            axis_direction = rand() % 6 + 1 # 选轴和方向
            slice = rand() % N + 1           # 选层
            if axis_direction == 1:
                mcube.slice_l(slice)
            elif axis_direction == 2:
                mcube.slice_r(slice)
            elif axis_direction == 3:
                mcube.slice_u(slice)
            elif axis_direction == 4:
                mcube.slice_d(slice)
            elif axis_direction == 5:
                mcube.slice_c(slice)
            elif axis_direction == 6: 
                mcube.slice_a(slice)
# 做一系列移动步骤
    def domoves(s):
        a = ""
        for i in range(1, int(len(s) // 3)+1):
            a1 = s[i * 3 - 3]
            a2 = s[i * 3 - 2]
            a=a1+a2
            if (a == "UL") :mcube.UL()
            elif (a == "UR"):mcube.UR()
            elif (a == "DL"):mcube.DL()
            elif (a == "DR"):mcube.DR()
            elif (a == "LU"): mcube.LU()
            elif (a == "LD"): mcube.LD()
            elif (a == "RU"): mcube.RU()
            elif (a == "RD"): mcube.RD()
            elif (a == "FC"): mcube.FC()
            elif (a == "FA"): mcube.FA()
            elif (a == "BC"): mcube.BC()
            elif (a == "BA"): mcube.BA()
            elif (a == "uL"): mcube.uL()
            elif (a == "uR"): mcube.uR()
            elif (a == "dL"): mcube.dL()
            elif (a == "dR"): mcube.dR()
            elif (a == "lU"): mcube.lU()
            elif (a == "lD"): mcube.lD()
            elif (a == "rU"): mcube.RU()
            elif (a == "rD"): mcube.rD()
            elif (a == "fC"): mcube.fC()
            elif (a == "fA"): mcube.fA()
            elif (a == "bC"): mcube.bC()
            elif (a == "bA"): mcube.bA()
            elif (a == "CL"): mcube.CL()
            elif (a == "CR"): mcube.CR()
            elif (a == "CU"): mcube.CU()
            elif (a == "CD"): mcube.CD()
            elif (a == "CC"): mcube.CC()
            elif (a == "CA"): mcube.CA()
            elif (a == "U2"): mcube.U2()
            elif (a == "D2"): mcube.D2()
            elif (a == "L2"): mcube.L2()
            elif (a == "R2"): mcube.R2()
            elif (a == "F2"): mcube.F2()
            elif (a == "B2"): mcube.B2()
            elif (a == "u2"): mcube.u2()
            elif (a == "d2"): mcube.d2()
            elif (a == "l2"): mcube.l2()
            elif (a == "r2"): mcube.r2()
            elif (a == "f2"): mcube.f2()
            elif (a == "b2"): mcube.b2()

# 执行解决方案
    def dosolution(self):
        mcube.domoves(mcube.solution)
# 在顶面寻找给定的中心色块
    def findcenter_u(a):
        if mcube.cube[2][5][2] == a:
            mcube.fx = 2
            mcube.fy = 5
            mcube.fz = 2
            return POSY
        elif mcube.cube[2][5][3] == a:
            mcube.fx = 2
            mcube.fy = 5
            mcube.fz = 3
            return POSY
        elif mcube.cube[3][5][2] == a:
            mcube.fx = 3
            mcube.fy = 5
            mcube.fz = 2
            return POSY
        elif mcube.cube[3][5][3] == a:
            mcube.fx = 3
            mcube.fy = 5
            mcube.fz = 3
            return POSY
        return 0

# 在底面寻找给定的中心色块
    def findcenter_d(a):
        if mcube.cube[2][0][2] == a:
            mcube.fx = 2
            mcube.fy = 0
            mcube.fz = 2
            return NEGY
        elif mcube.cube[2][0][3] == a:
            mcube.fx = 2
            mcube.fy = 0
            mcube.fz = 3
            return NEGY
        elif mcube.cube[3][0][2] == a:
            mcube.fx = 3
            mcube.fy = 0
            mcube.fz = 2
            return NEGY
        elif mcube.cube[3][0][3] == a:
            mcube.fx = 3
            mcube.fy = 0
            mcube.fz = 3
            return NEGY
        return 0
# 在左面寻找给定的中心色块
    def findcenter_l(a):
        if mcube.cube[0][2][2] == a:
            mcube.fx = 0
            mcube.fy = 2
            mcube.fz = 2
            return NEGX
        elif mcube.cube[0][2][3] == a:
            mcube.fx = 0
            mcube.fy = 2
            mcube.fz = 3
            return NEGX
        elif mcube.cube[0][3][2] == a:
            mcube.fx = 0
            mcube.fy = 3
            mcube.fz = 2
            return NEGX
        elif mcube.cube[0][3][3] == a:
            mcube.fx = 0
            mcube.fy = 3
            mcube.fz = 3
            return NEGX
        return 0
#  在右面寻找给定的中心色块
    def findcenter_r(a):
        if mcube.cube[5][2][2] == a:
            mcube.fx = 5
            mcube.fy = 2
            mcube.fz = 2
            return POSX
        elif mcube.cube[5][2][3] == a:
            mcube.fx = 5
            mcube.fy = 2
            mcube.fz = 3
            return POSX
        elif mcube.cube[5][3][2] == a:
            mcube.fx = 5
            mcube.fy = 3
            mcube.fz = 2
            return POSX
        elif mcube.cube[5][3][3] == a:
            mcube.fx = 5
            mcube.fy = 3
            mcube.fz = 3
            return POSX
        return 0
#  在前面寻找给定的中心色块
    def findcenter_f(a):
        if mcube.cube[2][2][0] == a:
            mcube.fx = 2
            mcube.fy = 2
            mcube.fz = 0
            return NEGZ
        elif mcube.cube[2][3][0] == a:
            mcube.fx = 2
            mcube.fy = 3
            mcube.fz = 0
            return NEGZ
        elif mcube.cube[3][2][0] == a:
            mcube.fx = 3
            mcube.fy = 2
            mcube.fz = 0
            return NEGZ
        elif mcube.cube[3][3][0] == a:
            mcube.fx = 3
            mcube.fy = 3
            mcube.fz = 0
            return NEGZ
        return 0
#  在后面寻找给定的中心色块
    def findcenter_b(a):
        if mcube.cube[2][2][5] == a:
            mcube.fx = 2
            mcube.fy = 2
            mcube.fz = 5
            return POSZ
        elif mcube.cube[2][3][5] == a:
            mcube.fx = 2
            mcube.fy = 3
            mcube.fz = 5
            return POSZ
        elif mcube.cube[3][2][5] == a:
            mcube.fx = 3
            mcube.fy = 2
            mcube.fz = 5
            return POSZ
        elif mcube.cube[3][3][5] == a:
            mcube.fx = 3
            mcube.fy = 3
            mcube.fz = 5
            return POSZ
        return 0
# 寻找给定的中心色块不在顶面
    def findcenter_not_u(a):
        x = mcube.findcenter_l(a)
        if x: return x
        x = mcube.findcenter_f(a)
        if x: return x
        x = mcube.findcenter_r(a)
        if x :return x
        x = mcube.findcenter_b(a)
        if x :return x
        x = mcube.findcenter_d(a)
        if x :return x
        return 0
# 寻找给定的中心色块不在底面
    def findcenter_not_d(a):
        x = mcube.findcenter_b(a)
        if x: return x
        x = mcube.findcenter_r(a)
        if x: return x
        x = mcube.findcenter_f(a)
        if x: return x
        x = mcube.findcenter_l(a)
        if x: return x
        x = mcube.findcenter_u(a)
        if x: return x
        return 0
# 寻找给定的中心色块不在左面
    def findcenter_not_l(a):
        x = mcube.findcenter_u(a)
        if x: return x
        x = mcube.findcenter_f(a)
        if x: return x
        x = mcube.findcenter_d(a)
        if x: return x
        x = mcube.findcenter_b(a)
        if x: return x
        x = mcube.findcenter_r(a)
        if x: return x
        return 0

# 寻找给定的中心色块不在右面
    def findcenter_not_r(a):
        x = mcube.findcenter_b(a)
        if x: return x
        x = mcube.findcenter_d(a)
        if x: return x
        x = mcube.findcenter_f(a)
        if x: return x
        x = mcube.findcenter_u(a)
        if x: return x
        x = mcube.findcenter_l(a)
        if x: return x
        return 0
# 寻找给定的中心色块不在前面
    def findcenter_not_f(a):
        x = mcube.findcenter_l(a)
        if x: return x
        x = mcube.findcenter_u(a)
        if x: return x
        x = mcube.findcenter_r(a)
        if x: return x
        x = mcube.findcenter_d(a)
        if x: return x
        x = mcube.findcenter_b(a)
        if x: return x
        return 0
# 寻找给定的中心色块不在后面
    def findcenter_not_b(a):
        x = mcube.findcenter_d(a)
        if x: return x
        x = mcube.findcenter_r(a)
        if x: return x
        x = mcube.findcenter_u(a)
        if x: return x
        x = mcube.findcenter_l(a)
        if x: return x
        x = mcube.findcenter_f(a)
        if x: return x
        return 0
# 寻找给定中心
    def findcenter(a):
        x = mcube.findcenter_u(a)
        if x: return x
        x = mcube.findcenter_l(a)
        if x: return x
        x = mcube.findcenter_f(a)
        if x: return x
        x = mcube.findcenter_r(a)
        if x: return x
        x = mcube.findcenter_b(a)
        if x: return x
        x = mcube.findcenter_d(a)
        if x: return x
        return 0
#  在顶面寻找未给定的中心色块
    def find_not_center_u(a):
        if mcube.cube[2][5][2] != a:
            mcube.fx = 2
            mcube.fy = 5
            mcube.fz = 2
            return POSY
        elif mcube.cube[2][5][3] != a:
            mcube.fx = 2
            mcube.fy = 5
            mcube.fz = 3
            return POSY
        elif mcube.cube[3][5][2] != a:
            mcube.fx = 3
            mcube.fy = 5
            mcube.fz = 2
            return POSY
        elif mcube.cube[3][5][3] != a:
            mcube.fx = 3
            mcube.fy = 5
            mcube.fz = 3
            return POSY
        return 0

# 在底面寻找未给定的中心色块
    def find_not_center_d(a):
        if mcube.cube[2][0][2] != a:
            mcube.fx = 2
            mcube.fy = 0
            mcube.fz = 2
            return NEGY
        elif mcube.cube[2][0][3] != a:
            mcube.fx = 2
            mcube.fy = 0
            mcube.fz = 3
            return NEGY
        elif mcube.cube[3][0][2] != a:
            mcube.fx = 3
            mcube.fy = 0
            mcube.fz = 2
            return NEGY
        elif mcube.cube[3][0][3] != a:
            mcube.fx = 3
            mcube.fy = 0
            mcube.fz = 3
            return NEGY
        return 0
# 在左面寻找未给定的中心色块
    def find_not_center_l(a):
        if mcube.cube[0][2][2] != a:
            mcube.fx = 0
            mcube.fy = 2
            mcube.fz = 2
            return NEGX
        elif mcube.cube[0][2][3] != a:
            mcube.fx = 0
            mcube.fy = 2
            mcube.fz = 3
            return NEGX
        elif mcube.cube[0][3][2] != a:
            mcube.fx = 0
            mcube.fy = 3
            mcube.fz = 2
            return NEGX
        elif mcube.cube[0][3][3] != a:
            mcube.fx = 0
            mcube.fy = 3
            mcube.fz = 3
            return NEGX
        return 0
# 在右面寻找未给定的中心色块
    def find_not_center_r(a):
        if mcube.cube[5][2][2] != a:
            mcube.fx = 5
            mcube.fy = 2
            mcube.fz = 2
            return POSX
        elif mcube.cube[5][2][3] != a:
            mcube.fx = 5
            mcube.fy = 2
            mcube.fz = 3
            return POSX
        elif mcube.cube[5][3][2] != a:
            mcube.fx = 5
            mcube.fy = 3
            mcube.fz = 2
            return POSX
        elif mcube.cube[5][3][3] != a:
            mcube.fx = 5
            mcube.fy = 3
            mcube.fz = 3
            return POSX
        return 0
# 在前面寻找未给定的中心色块
    def find_not_center_f(a):
        if mcube.cube[2][2][0] != a:
            mcube.fx = 2
            mcube.fy = 2
            mcube.fz = 0
            return NEGZ
        elif mcube.cube[2][3][0] != a:
            mcube.fx = 2
            mcube.fy = 3
            mcube.fz = 0
            return NEGZ
        elif mcube.cube[3][2][0] != a:
            mcube.fx = 3
            mcube.fy = 2
            mcube.fz = 0
            return NEGZ
        elif mcube.cube[3][3][0] != a:
            mcube.fx = 3
            mcube.fy = 3
            mcube.fz = 0
            return NEGZ
        return 0
# 在后面寻找未给定的中心色块
    def find_not_center_b(a):
        if mcube.cube[2][2][5] != a:
            mcube.fx = 2
            mcube.fy = 2
            mcube.fz = 5
            return POSZ
        elif mcube.cube[2][3][5] != a:
            mcube.fx = 2
            mcube.fy = 3
            mcube.fz = 5
            return POSZ
        elif mcube.cube[3][2][5] != a:
            mcube.fx = 3
            mcube.fy = 2
            mcube.fz = 5
            return POSZ
        elif mcube.cube[3][3][5] != a:
            mcube.fx = 3
            mcube.fy = 3
            mcube.fz = 5
            return POSZ
        return 0

# 寻找给定的左边
    def findedge_l(a, b):

        if mcube.cube[2][5][4] == a  and mcube.cube[2][4][5] == b: # top back
            mcube.fx = 2
            mcube.fy = 5
            mcube.fz = 4
            return POSY

        elif mcube.cube[3][4][5] == a  and mcube.cube[3][5][4] == b:
            mcube.fx = 3
            mcube.fy = 4
            mcube.fz = 5
            return POSZ
        elif mcube.cube[3][5][1] == a  and mcube.cube[3][4][0] == b: # top front
            mcube.fx = 3
            mcube.fy = 5
            mcube.fz = 1
            return POSY
        elif mcube.cube[2][4][0] == a  and mcube.cube[2][5][1] == b:
            mcube.fx = 2
            mcube.fy = 4
            mcube.fz = 0
            return NEGZ
        elif mcube.cube[1][5][2] == a  and mcube.cube[0][4][2] == b: # top left
            mcube.fx = 1
            mcube.fy = 5
            mcube.fz = 2
            return POSY
        elif mcube.cube[0][4][3] == a  and mcube.cube[1][5][3] == b:
            mcube.fx = 0
            mcube.fy = 4
            mcube.fz = 3
            return NEGX
        elif mcube.cube[4][5][3] == a  and mcube.cube[5][4][3] == b: # top right
            mcube.fx = 4
            mcube.fy = 5
            mcube.fz = 3
            return POSY
        elif mcube.cube[5][4][2] == a  and mcube.cube[4][5][2] == b:
            mcube.fx = 5
            mcube.fy = 4
            mcube.fz = 2
            return POSX
        elif mcube.cube[2][0][1] == a  and mcube.cube[2][1][0] == b : # bottom front
            mcube.fx = 2
            mcube.fy = 0
            mcube.fz = 1
            return NEGY
        elif mcube.cube[3][1][0] == a  and mcube.cube[3][0][1] == b :
            mcube.fx = 3
            mcube.fy = 1
            mcube.fz = 0
            return NEGZ
        elif mcube.cube[3][0][4] == a  and mcube.cube[3][1][5] == b : # bottom back
            mcube.fx = 3
            mcube.fy = 0
            mcube.fz = 4
            return NEGY
        elif mcube.cube[2][1][5] == a  and mcube.cube[2][0][4] == b :
            mcube.fx = 2
            mcube.fy = 1
            mcube.fz = 5
            return POSZ
        elif mcube.cube[1][0][3] == a  and mcube.cube[0][1][3] == b : # bottom left
            mcube.fx = 1
            mcube.fy = 0
            mcube.fz = 3
            return NEGY
        elif mcube.cube[0][1][2] == a  and mcube.cube[1][0][2] == b :
            mcube.fx = 0
            mcube.fy = 1
            mcube.fz = 2
            return NEGX
        elif mcube.cube[4][0][2] == a  and mcube.cube[5][1][2] == b : # bottom right
            mcube.fx = 4
            mcube.fy = 0
            mcube.fz = 2
            return NEGY
        elif mcube.cube[5][1][3] == a  and mcube.cube[4][0][3] == b :
            mcube.fx = 5
            mcube.fy = 1
            mcube.fz = 3
            return POSX
        elif mcube.cube[1][2][0] == a  and mcube.cube[0][2][1] == b : # front left
            mcube.fx = 1
            mcube.fy = 2
            mcube.fz = 0
            return NEGZ
        elif mcube.cube[0][3][1] == a  and mcube.cube[1][3][0] == b :
            mcube.fx = 0
            mcube.fy = 3
            mcube.fz = 1
            return NEGX
        elif mcube.cube[4][3][0] == a  and mcube.cube[5][3][1] == b : # front right
            mcube.fx = 4
            mcube.fy = 3
            mcube.fz = 0
            return NEGZ
        elif mcube.cube[5][2][1] == a  and mcube.cube[4][2][0] == b :
            mcube.fx = 5
            mcube.fy = 2
            mcube.fz = 1
            return POSX
        elif mcube.cube[1][3][5] == a  and mcube.cube[0][3][4] == b : # back left
            mcube.fx = 1
            mcube.fy = 3
            mcube.fz = 5
            return POSZ
        elif mcube.cube[0][2][4] == a  and mcube.cube[1][2][5] == b :
            mcube.fx = 0
            mcube.fy = 2
            mcube.fz = 4
            return NEGX
        elif mcube.cube[4][2][5] == a  and mcube.cube[5][2][4] == b : # back right
            mcube.fx = 4
            mcube.fy = 2
            mcube.fz = 5
            return POSZ
        elif mcube.cube[5][3][4] == a  and mcube.cube[4][3][5] == b :
            mcube.fx = 5
            mcube.fy = 3
            mcube.fz = 4
            return POSX
        return 0

# 寻找给定的右边
    def findedge_r(a, b):

        if mcube.cube[3][5][4] == a and mcube.cube[3][4][5] == b:  # top back
            mcube.fx = 3
            mcube.fy = 5
            mcube.fz = 4
            return POSY
        elif mcube.cube[2][4][5] == a and mcube.cube[2][5][4] == b:
            mcube.fx = 2
            mcube.fy = 4
            mcube.fz = 5
            return POSZ
        elif mcube.cube[2][5][1] == a and mcube.cube[2][4][0] == b:  # top front
            mcube.fx = 2
            mcube.fy = 5
            mcube.fz = 1
            return POSY
        elif mcube.cube[3][4][0] == a and mcube.cube[3][5][1] == b:
            mcube.fx = 3
            mcube.fy = 4
            mcube.fz = 0
            return NEGZ
        elif mcube.cube[1][5][3] == a and mcube.cube[0][4][3] == b:  # top left
            mcube.fx = 1
            mcube.fy = 5
            mcube.fz = 3
            return POSY
        elif mcube.cube[0][4][2] == a and mcube.cube[1][5][2] == b:
            mcube.fx = 0
            mcube.fy = 4
            mcube.fz = 2
            return NEGX
        elif mcube.cube[4][5][2] == a and mcube.cube[5][4][2] == b:  # top right
            mcube.fx = 4
            mcube.fy = 5
            mcube.fz = 2
            return POSY
        elif mcube.cube[5][4][3] == a and mcube.cube[4][5][3] == b:
            mcube.fx = 5
            mcube.fy = 4
            mcube.fz = 3
            return POSX
        elif mcube.cube[3][0][1] == a and mcube.cube[3][1][0] == b:  # bottom front
            mcube.fx = 3
            mcube.fy = 0
            mcube.fz = 1
            return NEGY
        elif mcube.cube[2][1][0] == a and mcube.cube[2][0][1] == b:
            mcube.fx = 2
            mcube.fy = 1
            mcube.fz = 0
            return NEGZ
        elif mcube.cube[2][0][4] == a and mcube.cube[2][1][5] == b:  # bottom back
            mcube.fx = 2
            mcube.fy = 0
            mcube.fz = 4
            return NEGY
        elif mcube.cube[3][1][5] == a and mcube.cube[3][0][4] == b:
            mcube.fx = 3
            mcube.fy = 1
            mcube.fz = 5
            return POSZ
        elif mcube.cube[1][0][2] == a and mcube.cube[0][1][2] == b:  # bottom left
            mcube.fx = 1
            mcube.fy = 0
            mcube.fz = 2
            return NEGY
        elif mcube.cube[0][1][3] == a and mcube.cube[1][0][3] == b:
            mcube.fx = 0
            mcube.fy = 1
            mcube.fz = 3
            return NEGX
        elif mcube.cube[4][0][3] == a and mcube.cube[5][1][3] == b:  # bottom right
            mcube.fx = 4
            mcube.fy = 0
            mcube.fz = 3
            return NEGY
        elif mcube.cube[5][1][2] == a and mcube.cube[4][0][2] == b:
            mcube.fx = 5
            mcube.fy = 1
            mcube.fz = 2
            return POSX
        elif mcube.cube[1][3][0] == a and mcube.cube[0][3][1] == b:  # front left
            mcube.fx = 1
            mcube.fy = 3
            mcube.fz = 0
            return NEGZ
        elif mcube.cube[0][2][1] == a and mcube.cube[1][2][0] == b:
            mcube.fx = 0
            mcube.fy = 2
            mcube.fz = 1
            return NEGX
        elif mcube.cube[4][2][0] == a and mcube.cube[5][2][1] == b:  # front right
            mcube.fx = 4
            mcube.fy = 2
            mcube.fz = 0
            return NEGZ
        elif mcube.cube[5][3][1] == a and mcube.cube[4][3][0] == b:
            mcube.fx = 5
            mcube.fy = 3
            mcube.fz = 1
            return POSX
        elif mcube.cube[1][2][5] == a and mcube.cube[0][2][4] == b:  # back left
            mcube.fx = 1
            mcube.fy = 2
            mcube.fz = 5
            return POSZ
        elif mcube.cube[0][3][4] == a and mcube.cube[1][3][5] == b:
            mcube.fx = 0
            mcube.fy = 3
            mcube.fz = 4
            return NEGX
        elif mcube.cube[4][3][5] == a and mcube.cube[5][3][4] == b:  # back right
            mcube.fx = 4
            mcube.fy = 3
            mcube.fz = 5
            return POSZ
        elif mcube.cube[5][2][4] == a and mcube.cube[4][2][5] == b:
            mcube.fx = 5
            mcube.fy = 2
            mcube.fz = 4
            return POSX
        return 0
# 寻找给定边
    def findedge(a, b):
        x = mcube.findedge_l(a, b)
        if x: return x
        x = mcube.findedge_r(a, b)
        if x: return x
        return 0
# 顺时针寻找给定的角块
    def findcorner_c( a, b, c):

        if  mcube.cube[1][5][1] == a  and mcube.cube[1][4][0] == b  and mcube.cube[0][4][1] == c: # top left front
            mcube.fx = 1
            mcube.fy = 5
            mcube.fz = 1
            return POSY
        elif mcube.cube[1][4][0] == a  and mcube.cube[0][4][1] == b  and mcube.cube[1][5][1] == c:
            mcube.fx = 1
            mcube.fy = 4
            mcube.fz = 0
            return NEGZ
        elif mcube.cube[0][4][1] == a  and mcube.cube[1][5][1] == b  and mcube.cube[1][4][0] == c:
            mcube.fx = 0
            mcube.fy = 4
            mcube.fz = 1
            return NEGX
        elif mcube.cube[4][5][1] == a  and mcube.cube[5][4][1] == b  and mcube.cube[4][4][0] == c: # top right front
            mcube.fx = 4
            mcube.fy = 5
            mcube.fz = 1
            return POSY
        elif mcube.cube[5][4][1] == a  and mcube.cube[4][4][0] == b  and mcube.cube[4][5][1] == c:
            mcube.fx = 5
            mcube.fy = 4
            mcube.fz = 1
            return POSX
        elif mcube.cube[4][4][0] == a  and mcube.cube[4][5][1] == b  and mcube.cube[5][4][1] == c:
            mcube.fx = 4
            mcube.fy = 4
            mcube.fz = 0
            return NEGZ
        elif mcube.cube[1][5][4] == a  and mcube.cube[0][4][4] == b  and mcube.cube[1][4][5] == c: # top left back
            mcube.fx = 1
            mcube.fy = 5
            mcube.fz = 4
            return POSY
        elif mcube.cube[0][4][4] == a  and mcube.cube[1][4][5] == b  and mcube.cube[1][5][4] == c:
            mcube.fx = 0
            mcube.fy = 4
            mcube.fz = 4
            return NEGX
        elif mcube.cube[1][4][5] == a  and mcube.cube[1][5][4] == b  and mcube.cube[0][4][4] == c:
            mcube.fx = 1
            mcube.fy = 4
            mcube.fz = 5
            return POSZ
        elif mcube.cube[4][5][4] == a  and mcube.cube[4][4][5] == b  and mcube.cube[5][4][4] == c: # top right back
            mcube.fx = 4
            mcube.fy = 5
            mcube.fz = 4
            return POSY
        elif mcube.cube[4][4][5] == a  and mcube.cube[5][4][4] == b  and mcube.cube[4][5][4] == c:
            mcube.fx = 4
            mcube.fy = 4
            mcube.fz = 5
            return POSZ
        elif mcube.cube[5][4][4] == a  and mcube.cube[4][5][4] == b  and mcube.cube[4][4][5] == c:
            mcube.fx = 5
            mcube.fy = 4
            mcube.fz = 4
            return POSX
        elif mcube.cube[1][0][1] == a  and mcube.cube[0][1][1] == b  and mcube.cube[1][1][0] == c: # bottom left front
            mcube.fx = 1
            mcube.fy = 0
            mcube.fz = 1
            return NEGY
        elif mcube.cube[0][1][1] == a  and mcube.cube[1][1][0] == b  and mcube.cube[1][0][1] == c:
            mcube.fx = 0
            mcube.fy = 1
            mcube.fz = 1
            return NEGX
        elif mcube.cube[1][1][0] == a  and mcube.cube[1][0][1] == b  and mcube.cube[0][1][1] == c:
            mcube.fx = 1
            mcube.fy = 1
            mcube.fz = 0
            return NEGZ
        elif mcube.cube[4][0][1] == a  and mcube.cube[4][1][0] == b  and mcube.cube[5][1][1] == c: # bottom right front
            mcube.fx = 4
            mcube.fy = 0
            mcube.fz = 1
            return NEGY
        elif mcube.cube[4][1][0] == a  and mcube.cube[5][1][1] == b  and mcube.cube[4][0][1] == c:
            mcube.fx = 4
            mcube.fy = 1
            mcube.fz = 0
            return NEGZ
        elif mcube.cube[5][1][1] == a  and mcube.cube[4][0][1] == b  and mcube.cube[4][1][0] == c:
            mcube.fx = 5
            mcube.fy = 1
            mcube.fz = 1
            return POSX
        elif mcube.cube[1][0][4] == a  and mcube.cube[1][1][5] == b  and mcube.cube[0][1][4] == c: # bottom left back
            mcube.fx = 1
            mcube.fy = 0
            mcube.fz = 4
            return NEGY
        elif mcube.cube[1][1][5] == a  and mcube.cube[0][1][4] == b  and mcube.cube[1][0][4] == c:
            mcube.fx = 1
            mcube.fy = 1
            mcube.fz = 5
            return POSZ
        elif mcube.cube[0][1][4] == a  and mcube.cube[1][0][4] == b  and mcube.cube[1][1][5] == c:
            mcube.fx = 0
            mcube.fy = 1
            mcube.fz = 4
            return NEGX
        elif mcube.cube[4][0][4] == a  and mcube.cube[5][1][4] == b  and mcube.cube[4][1][5] == c: # bottom right back
            mcube.fx = 4
            mcube.fy = 0
            mcube.fz = 4
            return NEGY
        elif mcube.cube[5][1][4] == a  and mcube.cube[4][1][5] == b  and mcube.cube[4][0][4] == c:
            mcube.fx = 5
            mcube.fy = 1
            mcube.fz = 4
            return POSX
        elif mcube.cube[4][1][5] == a  and mcube.cube[4][0][4] == b  and mcube.cube[5][1][4] == c:
            mcube.fx = 4
            mcube.fy = 1
            mcube.fz = 5
            return POSZ
        return 0
# 逆时针寻找给定的角块
    def findcorner_a(a, b, c):

        if mcube.cube[1][5][1] == a and mcube.cube[0][4][1] == b and mcube.cube[1][4][0] == c: # top left front
            mcube.fx = 1
            mcube.fy = 5
            mcube.fz = 1
            return POSY
        elif mcube.cube[1][4][0] == a and mcube.cube[1][5][1] == b and mcube.cube[0][4][1] == c:
            mcube.fx = 1
            mcube.fy = 4
            mcube.fz = 0
            return NEGZ
        elif mcube.cube[0][4][1] == a and mcube.cube[1][4][0] == b and mcube.cube[1][5][1] == c:
            mcube.fx = 0
            mcube.fy = 4
            mcube.fz = 1
            return NEGX
        elif mcube.cube[4][5][1] == a and mcube.cube[4][4][0] == b and mcube.cube[5][4][1] == c: # top right front
            mcube.fx = 4
            mcube.fy = 5
            mcube.fz = 1
            return POSY
        elif mcube.cube[5][4][1] == a and mcube.cube[4][5][1] == b and mcube.cube[4][4][0] == c:
            mcube.fx = 5
            mcube.fy = 4
            mcube.fz = 1
            return POSX
        elif mcube.cube[4][4][0] == a and mcube.cube[5][4][1] == b and mcube.cube[4][5][1] == c:
            mcube.fx = 4
            mcube.fy = 4
            mcube.fz = 0
            return NEGZ
        elif mcube.cube[1][5][4] == a and mcube.cube[1][4][5] == b and mcube.cube[0][4][4] == c: # top left back
            mcube.fx = 1
            mcube.fy = 5
            mcube.fz = 4
            return POSY
        elif mcube.cube[0][4][4] == a and mcube.cube[1][5][4] == b and mcube.cube[1][4][5] == c:
            mcube.fx = 0
            mcube.fy = 4
            mcube.fz = 4
            return NEGX
        elif mcube.cube[1][4][5] == a and mcube.cube[0][4][4] == b and mcube.cube[1][5][4] == c:
            mcube.fx = 1
            mcube.fy = 4
            mcube.fz = 5
            return POSZ
        elif mcube.cube[4][5][4] == a and mcube.cube[5][4][4] == b and mcube.cube[4][4][5] == c: # top right back
            mcube.fx = 4
            mcube.fy = 5
            mcube.fz = 4
            return POSY
        elif mcube.cube[4][4][5] == a and mcube.cube[4][5][4] == b and mcube.cube[5][4][4] == c:
            mcube.fx = 4
            mcube.fy = 4
            mcube.fz = 5
            return POSZ
        elif mcube.cube[5][4][4] == a and mcube.cube[4][4][5] == b and mcube.cube[4][5][4] == c:
            mcube.fx = 5
            mcube.fy = 4
            mcube.fz = 4
            return POSX
        elif mcube.cube[1][0][1] == a and mcube.cube[1][1][0] == b and mcube.cube[0][1][1] == c: # bottom left front
            mcube.fx = 1
            mcube.fy = 0
            mcube.fz = 1
            return NEGY
        elif mcube.cube[0][1][1] == a and mcube.cube[1][0][1] == b and mcube.cube[1][1][0] == c:
            mcube.fx = 0
            mcube.fy = 1
            mcube.fz = 1
            return NEGX
        elif mcube.cube[1][1][0] == a and mcube.cube[0][1][1] == b and mcube.cube[1][0][1] == c:
            mcube.fx = 1
            mcube.fy = 1
            mcube.fz = 0
            return NEGZ
        elif mcube.cube[4][0][1] == a and mcube.cube[5][1][1] == b and mcube.cube[4][1][0] == c: # bottom right front
            mcube.fx = 4
            mcube.fy = 0
            mcube.fz = 1
            return NEGY
        elif mcube.cube[4][1][0] == a and mcube.cube[4][0][1] == b and mcube.cube[5][1][1] == c:
            mcube.fx = 4
            mcube.fy = 1
            mcube.fz = 0
            return NEGZ
        elif mcube.cube[5][1][1] == a and mcube.cube[4][1][0] == b and mcube.cube[4][0][1] == c:
            mcube.fx = 5
            mcube.fy = 1
            mcube.fz = 1
            return POSX
        elif mcube.cube[1][0][4] == a and mcube.cube[0][1][4] == b and mcube.cube[1][1][5] == c: # bottom left back
            mcube.fx = 1
            mcube.fy = 0
            mcube.fz = 4
            return NEGY
        elif mcube.cube[1][1][5] == a and mcube.cube[1][0][4] == b and mcube.cube[0][1][4] == c:
            mcube.fx = 1
            mcube.fy = 1
            mcube.fz = 5
            return POSZ
        elif mcube.cube[0][1][4] == a and mcube.cube[1][1][5] == b and mcube.cube[1][0][4] == c:
            mcube.fx = 0
            mcube.fy = 1
            mcube.fz = 4
            return NEGX
        elif mcube.cube[4][0][4] == a and mcube.cube[4][1][5] == b and mcube.cube[5][1][4] == c: # bottom right back
            mcube.fx = 4
            mcube.fy = 0
            mcube.fz = 4
            return NEGY
        elif mcube.cube[5][1][4] == a and mcube.cube[4][0][4] == b and mcube.cube[4][1][5] == c:
            mcube.fx = 5
            mcube.fy = 1
            mcube.fz = 4
            return POSX
        elif mcube.cube[4][1][5] == a and mcube.cube[5][1][4] == b and mcube.cube[4][0][4] == c:
            mcube.fx = 4
            mcube.fy = 1
            mcube.fz = 5
            return POSZ
        return 0
# 寻找给定角块
    def findcorner(a, b, c):
        x = mcube.findcorner_c(a, b, c)
        if x: return x
        x = mcube.findcorner_a(a, b, c)
        if x: return x
        return 0
# 转换输出方式
    def std_to_metr(s):
        a = s
        slice_metr='\0'
        dir_prime='\0'
        for i in range(1,int(len(s) // 3)+1):
            slice_std = s[i * 3 - 3]
            dir = s[i * 3 - 2]
            if slice_std == 'C':
                continue
            if dir == '2':
                if slice_std == 'U' or slice_std == 'u' or slice_std == 'd' or slice_std == 'D':
                    dir_prime = 'L'
                elif slice_std == 'L' or slice_std == 'l' or slice_std == 'r' or slice_std == 'R':
                    dir_prime = 'U'
                elif slice_std == 'F' or slice_std == 'f' or slice_std == 'b' or slice_std == 'B':
                    dir_prime = 'C'
            if slice_std == 'D' or slice_std == 'L' or slice_std == 'F':
                slice_metr = '1'
            elif slice_std == 'd' or slice_std == 'l' or slice_std == 'f':
                slice_metr = '2'
            elif slice_std == 'u' or slice_std == 'r' or slice_std == 'b':
                slice_metr = '3'
            elif slice_std == 'U' or slice_std == 'R' or slice_std == 'B':
                slice_metr = '4'
            a1=list(a)
            a1[i * 3 - 3]= slice_metr
            a=''.join(a1)
            if dir == '2':
                a[i * 3 - 2] = dir_prime
                a.insert(i * 3, "  .")
                a[i * 3] = slice_metr
                a[i * 3 + 1] = dir_prime
                i += 1
        return a

    def metr_to_std(s):
        a = s
        slice_std='\0'
        for i in range(1, int(len(s) // 3)+1):
            slice_metr = s[i * 3 - 3]
            dir = s[i * 3 - 2]
            if slice_metr == 'C':
                continue
            if dir=='L' or dir=='R':
                if slice_metr=='1':
                    slice_std = 'D'
                if slice_metr =='2':
                    slice_std = 'd'
                if slice_metr=='3':
                    slice_std = 'u'
                if slice_metr =='4':
                    slice_std = 'U'
            if dir == 'U' or dir == 'D':
                if slice_metr == '1':
                    slice_std = 'L'
                if slice_metr == '2':
                    slice_std = 'l'
                if slice_metr == '3':
                    slice_std = 'r'
                if slice_metr == '4':
                    slice_std = 'R'
            if dir == 'C' or dir == 'A':
                if slice_metr == '1':
                    slice_std = 'F'
                if slice_metr == '2':
                    slice_std = 'f'
                if slice_metr == '3':
                    slice_std = 'b'
                if slice_metr == '4':
                    slice_std = 'B'
            a1 = list(a)
            a1[i * 3 - 3] = slice_std
            a=''.join(a1)
        return a

    def std_to_rel(s):
        a = s
        dir_rel='\0'
        for i in range(1,int(len(s) // 3)+1):
            slice = s.at(i * 3 - 3)
            dir_std = s.at(i * 3 - 2)
            if slice == 'C':
                continue
            if dir_std =='L' or dir_std =='D' or dir_std =='C':
                dir_rel = '+'
            if dir_std == 'R' or dir_std == 'U' or dir_std == 'A':
                dir_rel = '-'
            if dir_std =='2':
                dir_rel = '2'
            a[i * 3 - 2] = dir_rel
        return a

    def rel_to_std(s):
        a = s
        dir_std='\0'
        for i in range(1,int(len(s) // 3)+1):
            slice = s.at(i * 3 - 3)
            dir_rel = s.at(i * 3 - 2)
            if slice == 'C':
                continue
            if slice == 'U' or slice == 'u' or slice == 'd' or slice == 'D':
                if dir_rel=='+':
                    dir_std = 'L'
                if dir_rel=='-':
                    dir_std = 'R'
            if slice == 'L' or slice == 'l' or slice == 'r' or slice == 'R':
                if dir_rel == '+':
                    dir_std = 'D'
                if dir_rel == '-':
                    dir_std = 'U'
            if slice == 'F' or slice == 'f' or slice == 'b' or slice == 'B':
                if dir_rel == '+':
                    dir_std = 'C'
                if dir_rel == '-':
                    dir_std = 'A'
            if dir_rel == '2':
                dir_std = '2'
            a[i * 3 - 2] = dir_std
        return a

    def metr_to_rel(s):
        return std_to_rel(mcube.metr_to_std(s)) 

    def rel_to_metr(s):
        return mcube.std_to_metr(rel_to_std(s))

# 允许转半圈
    def usehalfturns(s, b=0):
        a = s
        for i in range(1,int(len(a) // 3) - 1):
            slice = a.at(i * 3 - 3)
            dir = a.at(i * 3 - 2)
            slice_next = a.at(i * 3)
            dir_next = a.at(i * 3 + 1)
            if slice == 'C' or dir == '2':
                continue
            if slice == slice_next and dir == dir_next:
                a[i * 3 - 2] = '2'
                a1 = list(a)
                for j in range(0,3):
                    a1.pop(i * 3)
                a = ''.join(a1)

                if b:
                    mcube.shortenmov(i)
                i -=1
        return a
# 从解决方案字符串中去除多余的移动步骤
    def concise(s, b=0):
        strips = 0;redundancies=0
        a = mcube.std_to_metr(s)
        slice=''; dir='';
        sUD=0; sLR=0; sFB=0;
        dL=''; dR=''; dU=''; dD=''; dC=''; dA=''
  # step 1: 对整个魔方移动进行插值
        i=1
        while i <=int(len(a)// 3):
            slice = a[i * 3 - 3]
            if slice == 'C':
                dir = a[i * 3 - 2]
                sUD = 1
                sLR = 1
                sFB = 1
                dL = 'L'
                dR = 'R'
                dU = 'U'
                dD = 'D'
                dC = 'C'
                dA = 'A'
                if dir =='L':
                    sFB = -1; dU = 'A'; dD = 'C'; dC = 'U'; dA = 'D';
                elif dir == 'R':
                    sLR = -1; dU = 'C'; dD = 'A'; dC = 'D'; dA = 'U';
                elif dir == 'U':
                    sUD = -1; dL = 'C'; dR = 'A'; dC = 'R'; dA = 'L';
                elif dir == 'D':
                    sFB = -1; dL = 'A'; dR = 'C'; dC = 'L'; dA = 'R';
                elif dir == 'C':
                    sUD = -1; dL = 'D'; dR = 'U'; dU = 'L'; dD = 'R';
                elif dir == 'A':
                    sLR = -1; dL = 'U'; dR = 'D'; dU = 'R'; dD = 'L';
                a1=list(a)
                for j in range(0,3):
                    a1.pop(i * 3 - 3)
                a=''.join(a1)

                if b:
                    strips +=1
                    if strips > b:
                        mcube.shortenmov(i)
                for j in range(i, int(len(a) // 3) +1):
                    slice = a[j * 3 - 3]
                    dir = a[j * 3 - 2]
                    if dir=='L':
                        if sUD == -1 and slice != 'C':
                            slice = chr(N+1-(ord(slice)-ord('0'))+ord('0'))
                        dir = dL
                    elif dir=='R':
                        if sUD == -1 and slice != 'C':
                            slice = chr(N+1-(ord(slice)-ord('0'))+ord('0'))
                        dir = dR
                    elif dir== 'U':
                        if sLR == -1 and slice != 'C':
                            slice = chr(N+1-(ord(slice)-ord('0'))+ord('0'))
                        dir = dU
                    elif dir== 'D':
                        if sLR == -1 and slice != 'C':
                            slice = chr(N+1-(ord(slice)-ord('0'))+ord('0'))
                        dir = dD
                    elif dir== 'C':
                        if sFB == -1 and slice != 'C':
                            slice = chr(N+1-(ord(slice)-ord('0'))+ord('0'))
                        dir = dC
                    elif dir=='A':
                        if sFB == -1 and slice != 'C':
                            slice = chr(N+1-(ord(slice)-ord('0'))+ord('0'))
                        dir = dA
                    a1 = list(a)
                    a1[j * 3 - 3]= slice
                    a1[j * 3 - 2] = dir
                    a=''.join(a1)
                i -=1
            i += 1
        redundancies = 1
        while redundancies:

            slice=''; dir=''; slice_next=''; dir_next='';
            redundancies = 0
            dir_reverse='\0'
            i=1
            while i<=int(len(a)// 3) - 2:# step 2: 重新排序平行层
                slice = a[i * 3 - 3]
                dir = a[i * 3 - 2]
                slice_next = a[i * 3]
                dir_next = a[i * 3 + 1]
                if slice_next == slice:
                    i += 1
                    continue
                if dir == 'L':dir_reverse = 'R'
                if dir == 'R':dir_reverse = 'L'
                if dir == 'U': dir_reverse = 'D'
                if dir == 'D': dir_reverse = 'U'
                if dir == 'C': dir_reverse = 'A'
                if dir == 'A': dir_reverse = 'C'
                for j in range(i + 2, int(len(a) // 3)+1):
                    if not (dir_next == dir or dir_next == dir_reverse): break
                    slice_next = a[j * 3 - 3]
                    dir_next = a[j * 3 - 2]
                    if (slice_next == slice) and (dir_next == dir or dir_next == dir_reverse):
                        for k in range(j,i+1):
                            a[k * 3 - 3] = a[k * 3 - 6]
                            a[k * 3 - 2] = a[k * 3 - 5]
                        a1 = list(a)
                        a1[i * 3] = slice_next
                        a1[i * 3 + 1] = dir_next
                        a=''.join(a1)
                        i += 1
                i += 1

            slice = '';
            dir = '';
            slice_next = '';
            dir_next = '';
            dir_reverse='\0'  # step 3: 将3/4圈改为1/4圈
            i=1
            while i<=int(len(a)// 3) - 2:
                slice = a[i * 3 - 3]
                dir = a[i * 3 - 2]
                slice_next = a[i * 3]
                dir_next = a[i * 3 + 1]
                slice_after = a[i * 3 + 3]
                dir_after = a[i * 3 + 4]
                if(slice == slice_next) and (slice == slice_after) and(dir == dir_next) and (dir == dir_after):
                    if dir == 'L': dir_reverse = 'R'
                    if dir == 'R': dir_reverse = 'L'
                    if dir == 'U': dir_reverse = 'D'
                    if dir == 'D': dir_reverse = 'U'
                    if dir == 'C': dir_reverse = 'A'
                    if dir == 'A': dir_reverse = 'C'
                    a1=list(a)
                    a1[i * 3 - 2] = dir_reverse
                    for j in range(0,6):
                        a1.pop(i * 3)
                    a=''.join(a1)

                    if b:
                        strips +=1
                        if strips > b: mcube.shortenmov(i)
                        strips +=1
                        if strips > b: mcube.shortenmov(i)
                    i -= 2
                    if i < 0: i = 0
                    redundancies +=1
                i += 1

            slice = '';
            dir = '';
            slice_next = '';
            dir_next = '';
            dir_reverse='\0' # step 4: 删除相互矛盾的动作
            i=1
            while i <=int(len(a) // 3) - 1:
                slice = a[i * 3 - 3]
                dir = a[i * 3 - 2]
                slice_next = a[i * 3]
                dir_next = a[i * 3 + 1]
                if dir == 'L': dir_reverse = 'R'
                if dir == 'R': dir_reverse = 'L'
                if dir == 'U': dir_reverse = 'D'
                if dir == 'D': dir_reverse = 'U'
                if dir == 'C': dir_reverse = 'A'
                if dir == 'A': dir_reverse = 'C'
                if slice == slice_next and dir_next == dir_reverse:
                    a1=list(a)
                    for j in range(0,6):
                        a1.pop(i * 3 - 3)
                    a=''.join(a1)
                    if b: # change mov[] if necessary
                        strips += 1
                        if strips > b: mcube.shortenmov(i)
                        strips+=1
                        if strips > b: mcube.shortenmov(i)
                    i -= 2
                    if i < 0: i = 0
                    redundancies += 1
                i += 1

        return mcube.metr_to_std(a)
# 缩短 mov[]
    def shortenmov(m):
        tot = 0
        cur = 0
        for i in range(1, MOV+1):
            tot += mcube.mov[i]
            while tot >= m and cur < 1:
                mcube.mov[i] -= 1
                tot -= 1
                cur += 1
# 解魔方
    def solvecube(self):
        counter=0
        if not mcube.inited: # 确保魔方初始化
            mcube.erval = ERR_NOTINITED
            return mcube.erval
        mcube.erval = 0
        tcube = np.zeros((6,6,6),dtype=int)
        tmov = np.zeros(12,dtype=int)
        cen = np.zeros(7,dtype=int)
        parity = np.zeros(2,dtype=int)
        curmoves = 0
        U=0; D=0; L=0; R=0; F=0; B=0;
        tsolution = ""
        prefix = ""
        mcube.solution = "" # 清除 mov[] 和解决方案
        for i in range(0,MOV+1):
            mcube.mov[i] = 0
        for i in range(1,MOV+1):
            tmov[i] = 0
        tmov[0] = -1
        for i in range(0, N+2):#step1 备份原始魔方状态
            for j in range(0, N+2):
                for  k in range(0, N+2):
                    tcube[i][j][k] = mcube.cube[i][j][k]

        for i in range(0,7):#确保每种颜色都有正确的编号
            cen[i] = 0
        for i in range(0, N+2):
            for j in range(0, N+2):
                for k in range(0,N+2):
                    if mcube.cube[i][j][k] >= 1 and mcube.cube[i][j][k] <= 6:
                        cen[mcube.cube[i][j][k]] += 1
        for i in range(1,7):
            if cen[i] != N * N:
                mcube.erval = ERR_MISPAINTED
                return mcube.erval

        for i in range(1,7):# 设置插值表  U,D,L,R,F,B=1,2,3,4,5,6
            cen[i] = 0
        U = mcube.cube[1][N+1][1]
        L = mcube.cube[0][N][1]
        F = mcube.cube[1][N][0]
        for i in range(1,7):
            if i != U and i != L and i != F:
                if mcube.findcorner_c(F,U,i): R = i
                elif mcube.findcorner_c(U,L,i): B = i
                elif mcube.findcorner_c(L,F,i): D = i
                elif mcube.findcorner_a(F,U,i): R = i,
                elif mcube.findcorner_a(U,L,i): B = i 
                elif mcube.findcorner_a(L,F,i): D = i 

        if U == L or L == F or F == U or R == 0 or D == 0 or B == 0:# 确保每面都有不同的颜色
            mcube.erval = ERR_MISPAINTED
            return mcube.erval
        cen[U] = 1; cen[L] = 2; cen[F] = 3;
        cen[R] = 4; cen[B] = 5; cen[D] = 6;
        for i in range(1, N+1): # 应用插值
            for j in range(1, N+1):
                mcube.cube[i][N+1][j] = cen[mcube.cube[i][N+1][j]]
                mcube.cube[0][i][j]   = cen[mcube.cube[0][i][j]]
                mcube.cube[i][j][0]   = cen[mcube.cube[i][j][0]]
                mcube.cube[N+1][i][j] = cen[mcube.cube[N+1][i][j]]
                mcube.cube[i][j][N+1] = cen[mcube.cube[i][j][N+1]]
                mcube.cube[i][0][j]   = cen[mcube.cube[i][0][j]]
  # step 2 确保所有的小方块都存在

  # 发现“边缘翻转奇偶校验”问题
  # first check centers...
        for i in range(1,7):
            cen[i] = 0
        for i in range(2,N):
            for j in range(2, N):
                cen[mcube.cube[i][N+1][j]] += 1
                cen[mcube.cube[0][i][j]] += 1
                cen[mcube.cube[i][j][0]] += 1
                cen[mcube.cube[N+1][i][j]] += 1
                cen[mcube.cube[i][j][N+1]] += 1
                cen[mcube.cube[i][0][j]] += 1
        for i in range(1,7):
            if mcube.erval:break
            if cen[i] != (N-2) * (N-2):
                mcube.erval = ERR_MISPAINTED
        parity[0] = 0; # 检查角块
        for i in range(2,6):
            if mcube.erval: break
            if i<5: mark1=i+1
            if i>=5: mark1=i-3
            if not mcube.findcorner_c(1, mark1, i):
                if mcube.findcorner_a(1, mark1, i): parity[0]+=1
                else: mcube.erval = ERR_MISPAINTED
            if not mcube.findcorner_c(6, i, mark1):
                if mcube.findcorner_a(6, i, mark1): parity[0] +=1
                else: mcube.erval = ERR_MISPAINTED

        parity[1] = 0# 检查边块
        for i in range(2,6):
            if mcube.erval: break
            if not mcube.findedge_l(1, i):
                if mcube.findedge_r(1, i):
                    tx = mcube.fx; ty = mcube.fy; tz = mcube.fz;
                    mcube.cube[tx][ty][tz] = 0
                    if mcube.findedge_r(1, i): parity[1] += 1
                    else: mcube.erval = ERR_MISPAINTED
                    mcube.cube[tx][ty][tz] = 1
                else: mcube.erval = ERR_MISPAINTED
            if not mcube.findedge_r(1, i):
                if mcube.findedge_l(1, i):
                    tx = mcube.fz; ty = mcube.fy; tz = mcube.fz;
                    mcube.cube[tx][ty][tz] = 0
                    if mcube.findedge_l(1, i): parity[1] += 1
                    else: mcube.erval = ERR_MISPAINTED
                    mcube.cube[tx][ty][tz] = 1
                else: mcube.erval = ERR_MISPAINTED
            if not mcube.findedge_l(6, i):
                if mcube.findedge_r(6, i):
                    tx = mcube.fz; ty = mcube.fy; tz = mcube.fz
                    mcube.cube[tx][ty][tz] = 0
                    if mcube.findedge_r(6, i): parity[1] += 1
                    else: mcube.erval = ERR_MISPAINTED
                    mcube.cube[tx][ty][tz] = 6;
                else: mcube.erval = ERR_MISPAINTED
            if not mcube.findedge_r(6, i):
                if mcube.findedge_l(6, i):
                    tx = mcube.fz; ty = mcube.fy; tz = mcube.fz;
                    mcube.cube[tx][ty][tz] = 0
                    if mcube.findedge_l(6, i): parity[1]+=1
                    else: mcube.erval = ERR_MISPAINTED
                    mcube.cube[tx][ty][tz] = 6
                else: mcube.erval = ERR_MISPAINTED
            if i < 5 : mark2 = i+1
            if i >= 5: mark2 = i -3
            if not mcube.findedge_l(i, mark2):
                if mcube.findedge_r(i, mark2):
                    tx = mcube.fx; ty = mcube.fy; tz = mcube.fz;
                    mcube.cube[tx][ty][tz] = 0
                    if mcube.findedge_r(i,mark2): parity[1]+=1
                    else: mcube.erval = ERR_MISPAINTED
                    mcube.cube[tx][ty][tz] = i
                else: mcube.erval = ERR_MISPAINTED
            if not mcube.findedge_r(i,mark2):
                if mcube.findedge_l(i, mark2):
                    tx = mcube.fx; ty = mcube.fy; tz = mcube.fz;
                    mcube.cube[tx][ty][tz] = 0
                    if mcube.findedge_l(i, mark2): parity[1] += 1
                    else: mcube.erval = ERR_MISPAINTED
                    mcube.cube[tx][ty][tz] = i
                else: mcube.erval = ERR_MISPAINTED
        if parity[0] > 0 and not mcube.erval:
            mcube.erval = ERR_PARITY_CORNER_BACKWARD
        elif parity[1] > 0 and not mcube.erval:
            mcube.erval = ERR_PARITY_EDGE_FLIP
        for i in range(0,N+2):
            for j in range(0,N+2):
                for k in range(0,N+2):
                    mcube.cube[i][j][k] = tcube[i][j][k]
        if mcube.erval: return mcube.erval# 魔方看起来是可解的（除非存在奇偶校验错误）；尝试解决方案
        for h in range(1,7):# step 3 从每个可能的方向开始寻找最短的解决方案
            for g in range(1,5):
                for i in range(0,N+2):
                    for j in range(0,N+2):
                        for k in range(0,N+2):
                            tcube[i][j][k] = mcube.cube[i][j][k]
                for i in range(1,7): # step 4 设置插值表 U,D,L,R,F,B=1,2,3,4,5,6
                    cen[i] = 0
                U = mcube.cube[1][N+1][1]
                L = mcube.cube[0][N][1]
                F = mcube.cube[1][N][0]
                for i in range(1,7):
                    if i != U and i != L and i != F:
                        if mcube.findcorner_c(F,U,i): R = i
                        elif mcube.findcorner_c(L,F,i):D = i
                        elif mcube.findcorner_c(U,L,i): B = i
      # 设置矩阵
                cen[U] = 1; cen[L] = 2; cen[F] = 3;
                cen[R] = 4; cen[B] = 5; cen[D] = 6;
      # 应用插值
                for i in range(1,N+1):
                    for j in range(1,N+1):
                        mcube.cube[i][N+1][j] = cen[mcube.cube[i][N+1][j]]
                        mcube.cube[0][i][j]   = cen[mcube.cube[0][i][j]]
                        mcube.cube[i][j][0]   = cen[mcube.cube[i][j][0]]
                        mcube.cube[N+1][i][j] = cen[mcube.cube[N+1][i][j]]
                        mcube.cube[i][j][N+1] = cen[mcube.cube[i][j][N+1]]
                        mcube.cube[i][0][j]   = cen[mcube.cube[i][0][j]]
                if not mcube.erval:
                    counter+=1
                    cursolution = mcube.findsolution()        # step 5(ish) (FINALLLLLY): find a solution
                    if mcube.shorten >= SHORTEN_STRIP_ALL:
                        allmov = prefix + cursolution
                        prelen = int(len(prefix)) // 3
                        if prelen == 0: prelen = -1
                        cursolution = mcube.concise(allmov, prelen)
        # 查看当前解决方案是否比最佳解决方案更短
                    curmoves = int(len(cursolution))// 3
                    if curmoves < tmov[0] or tmov[0] < 0:
                        tsolution = cursolution
                        for i in range(1,MOV+1):
                            tmov[i] = mcube.mov[i]
                        tmov[0] = curmoves
                for i in range(0,N+2):
                    for j in range(0,N+2):
                        for k in range(0,N+2):
                            mcube.cube[i][j][k] = tcube[i][j][k]
      # 尝试下一个方向
                if mcube.shorten < SHORTEN_STRIP_ROTATE_ALL: break
                prefix += "CL."
                mcube.CL()
            if mcube.shorten < SHORTEN_STRIP_ROTATE_SOME: break
            if h % 2:
                prefix += "CU."
                mcube.CU()
            else:
                prefix += "CA."
                mcube.CA()
        if mcube.erval: return mcube.erval# step 6 设置成员并返回
        for i in range(0,MOV+1):
            mcube.mov[i] = tmov[i]
        mcube.solution = tsolution
        return 0
# 为准备好的魔方找到解决方案
    def findsolution():
        s = ""
        step = 0
  # step 1: 顶面中心
        step += 1
        a = ""
        iter = 0

        rot = 0
        while (not mcube.erval) and mcube.findcenter_not_u(1):
            if  mcube.cube[2][5][2] != 1:  pass
            elif mcube.cube[2][5][3] != 1:
                a += "CR."
                mcube.CR()
                rot=(rot+1)%4
            elif mcube.cube[3][5][2] != 1:
                a += "CL."
                mcube.CL()
                rot=(rot+3)%4
            elif mcube.cube[3][5][3] != 1:
                a += "CL.CL."
                mcube.CL()
                mcube.CL()
                rot=(rot+2)%4
            if mcube.findcenter_not_u(1)==0:pass
            elif mcube.findcenter_not_u(1)==NEGY:
                if  mcube.fx == 2 and mcube.fz == 2:pass
                elif mcube.fx == 2 and mcube.fz == 3:
                    a += "DR."
                    mcube.DR()
                elif mcube.fx == 3 and mcube.fz == 2:
                    a += "DL."
                    mcube.DL()
                elif mcube.fx == 3 and mcube.fz == 3:
                    a += "DL.DL."
                    mcube.DL()
                    mcube.DL()
                a += "lD.dR.LD.dR.lU.";
                mcube.lD(); mcube.dR(); mcube.LD(); mcube.dR(); mcube.lU();
            elif mcube.findcenter_not_u(1)==NEGX:
                if mcube.fy == 2 and mcube.fz == 2:pass
                elif mcube.fy == 2 and mcube.fz == 3:
                    a += "LU."
                    mcube.LU()
                elif mcube.fy == 3 and mcube.fz == 2:
                    a += "LD."
                    mcube.LD()
                elif mcube.fy == 3 and mcube.fz == 3:
                    a += "LD.LD."
                    mcube.LD()
                    mcube.LD()
                a += "rD.fC.rU.";
                mcube.rD(); mcube.fC(); mcube.rU();
            elif mcube.findcenter_not_u(1) ==NEGZ:
                if  mcube.fx == 2 and mcube.fy == 2:pass
                elif mcube.fx == 2 and mcube.fy == 3:
                    a+= "FA."
                    mcube.FA()
                elif mcube.fx == 3 and mcube.fy == 2:
                    a += "FC."
                    mcube.FC()
                elif mcube.fx == 3 and mcube.fy == 3:
                    a += "FA.FA."
                    mcube.FA(); mcube.FA();
                a += "bC.lU.bA.";
                mcube.bC(); mcube.lU(); mcube.bA();
            elif mcube.findcenter_not_u(1) ==POSX:
                if  mcube.fy == 2 and mcube.fz == 2:
                    a += "RU."; mcube.RU();
                elif mcube.fy == 2 and mcube.fz == 3:
                    a += "RD.RD."; mcube.RD(); mcube.RD();
                elif mcube.fy == 3 and mcube.fz == 2:pass
                elif mcube.fy == 3 and mcube.fz == 3:
                    a += "RD."; mcube.RD();
                a += "rU.fA.rD."
                mcube.rU(); mcube.fA(); mcube.rD();
            elif mcube.findcenter_not_u(1) ==POSZ:
                if mcube.fx == 2 and mcube.fy == 2:
                    a += "BC."; mcube.BC();
                elif mcube.fx == 2 and mcube.fy == 3:pass
                elif mcube.fx == 3 and mcube.fy == 2:
                    a += "BA.BA."; mcube.BA(); mcube.BA();
                elif mcube.fx == 3 and mcube.fy == 3:
                    a += "BA."; mcube.BA();
                a += "bC.lU.bA."
                mcube.bC(); mcube.lU(); mcube.bA();
            iter += 1
            if iter >= ITER_THRESHOLD: mcube.erval = ERR_NONDESCRIPT
        if rot==0:pass
        elif rot==1: a += "CL."; mcube.CL();
        elif rot==2: a += "CR.CR."; mcube.CR(); mcube.CR();
        elif rot==3: a += "CR."; mcube.CR();
    # 检查错误
        if mcube.erval:   return ""
        if mcube.shorten >= SHORTEN_STRIP_SOME:   a = mcube.concise(a)
        mcube.mov[step] = len(a) // 3
        s += a
  # step 2:底面中心

        step += 1
        a = ""
        iter = 0

        rot = 0
        while (not mcube.erval) and mcube.findcenter_not_d(6):
            if mcube.cube[2][0][2] != 6: pass
            elif mcube.cube[2][0][3] != 6:
                a += "CR."; mcube.CR(); rot=(rot+1)%4;
            elif mcube.cube[3][0][2] != 6:
                a += "CL."; mcube.CL(); rot=(rot+3)%4;
            elif mcube.cube[3][0][3] != 6:
                a += "CL.CL."; mcube.CL(); mcube.CL(); rot=(rot+2)%4;
            if mcube.findcenter_not_d(6) == 0:pass
            elif mcube.findcenter_not_d(6) == NEGX:
                if mcube.fy == 2 and mcube.fz == 2:
                    a += "LD."; mcube.LD();
                elif mcube.fy == 2 and mcube.fz == 3:pass
                elif mcube.fy == 3 and mcube.fz == 2:
                    a += "LU.LU."; mcube.LU(); mcube.LU();
                elif mcube.fy == 3 and mcube.fz == 3:
                    a += "LU."; mcube.LU();
                a += "fC.LU.fA.";
                mcube.fC(); mcube.LU(); mcube.fA();
            elif mcube.findcenter_not_d(6) ==  NEGZ:
                if mcube.fx == 2 and mcube.fy == 2:
                    a += "FA."; mcube.FA();
                elif mcube.fx == 2 and mcube.fy == 3:
                    a += "FC.FC."; mcube.FC(); mcube.FC();
                elif mcube.fx == 3 and mcube.fy == 2:pass
                elif mcube.fx == 3 and mcube.fy == 3:
                    a += "FC."; mcube.FC();
                a += "lU.FC.lD.";
                mcube.lU(); mcube.FC(); mcube.lD();
            elif mcube.findcenter_not_d(6) == POSX:
                if  mcube.fy == 2 and mcube.fz == 2:
                    a += "RU.RU."; mcube.RU(); mcube.RU();
                elif mcube.fy == 2 and mcube.fz == 3:
                    a += "RD."; mcube.RD();
                elif mcube.fy == 3 and mcube.fz == 2:
                    a += "RU."; mcube.RU();
                elif mcube.fy == 3 and mcube.fz == 3: pass
                a += "fA.RD.fC.";
                mcube.fA(); mcube.RD(); mcube.fC();
            elif mcube.findcenter_not_d(6) == POSZ:
                if  mcube.fx == 2 and mcube.fy == 2:
                    a += "BC.BC."; mcube.BC(); mcube.BC();
                elif mcube.fx == 2 and mcube.fy == 3:
                    a += "BC."; mcube.BC();
                elif mcube.fx == 3 and mcube.fy == 2:
                    a += "BA."; mcube.BA();
                elif mcube.fx == 3 and mcube.fy == 3: pass
                a += "lD.BA.lU.";
                mcube.lD(); mcube.BA(); mcube.lU();
            iter += 1
            if iter >= ITER_THRESHOLD: mcube.erval = ERR_NONDESCRIPT

        if rot == 0: pass
        elif rot == 1: a += "CL."; mcube.CL();
        elif rot == 2: a += "CR.CR."; mcube.CR(); mcube.CR();
        elif rot == 3: a += "CR."; mcube.CR();
    # 检查错误
        if mcube.erval: return ""
        if mcube.shorten >= SHORTEN_STRIP_SOME: a = mcube.concise(a)
        mcube.mov[step] = len(a) // 3
        s += a

  # step 3: 顶层角块
  
        step += 1
        a = ""
        iter = 0

        while (not mcube.erval) and not ((mcube.findcorner_c(1,3,2) == POSY and mcube.fx == 1 and mcube.fz == 1) and
        (mcube.findcorner_c(1,4,3) == POSY and mcube.fx == 4 and mcube.fz == 1) and
        (mcube.findcorner_c(1,5,4) == POSY and mcube.fx == 4 and mcube.fz == 4) and
        (mcube.findcorner_c(1,2,5) == POSY and mcube.fx == 1 and mcube.fz == 4) ) :
            for i in range(1,5):
                if i<4: mark2=i+2
                if i>=4: mark2=i-2
                if mcube.findcorner_c(1, mark2, (i+1))==POSY:
                    if mcube.fx == 1 and mcube.fz == 1: pass
                    elif mcube.fx == 1 and mcube.fz == 4:
                        a += "BA.DR.BC.FA.DL.FC."
                        mcube.BA(); mcube.DR(); mcube.BC(); mcube.FA(); mcube.DL(); mcube.FC();
                    elif mcube.fx == 4 and mcube.fz == 1 :
                        a += "RD.DL.RU.LD.DR.LU."
                        mcube.RD(); mcube.DL(); mcube.RU(); mcube.LD(); mcube.DR(); mcube.LU();
                    elif mcube.fx == 4 and mcube.fz == 4:
                        a += "BC.DL.BA.DL.LD.DR.LU."
                        mcube.BC(); mcube.DL(); mcube.BA(); mcube.DL(); mcube.LD(); mcube.DR(); mcube.LU();
                elif mcube.findcorner_c(1, mark2, (i+1))== NEGY:
                    if  mcube.fx == 1 and mcube.fz == 1:pass
                    elif mcube.fx == 1 and mcube.fz == 4:
                        a += "DR."
                        mcube.DR()
                    elif mcube.fx == 4 and mcube.fz == 1:
                        a += "DL."
                        mcube.DL()
                    elif mcube.fx == 4 and mcube.fz == 4:
                        a += "DL.DL."
                        mcube.DL(); mcube.DL();
                    a += "FA.DR.FC.DL.LD.DL.LU."
                    mcube.FA(); mcube.DR(); mcube.FC(); mcube.DL(); mcube.LD(); mcube.DL(); mcube.LU();
                elif mcube.findcorner_c(1, mark2, (i+1))== NEGX:
                    if  mcube.fy == 1 and mcube.fz == 1:
                        a += "LD.DR.LU."
                        mcube.LD(); mcube.DR(); mcube.LU();
                    elif mcube.fy == 1 and mcube.fz == 4:
                        a += "DR.FA.DL.FC."
                        mcube.DR(); mcube.FA(); mcube.DL(); mcube.FC();
                    elif mcube.fy == 4 and mcube.fz == 1:
                        a += "LD.DR.LU.DL.LD.DR.LU."
                        mcube.LD(); mcube.DR(); mcube.LU(); mcube.DL(); mcube.LD(); mcube.DR(); mcube.LU();
                    elif mcube.fy == 4 and mcube.fz == 4:
                        a += "LU.DL.LD.DL.LD.DL.LU."
                        mcube.LU(); mcube.DL(); mcube.LD(); mcube.DL(); mcube.LD(); mcube.DL(); mcube.LU();
                elif mcube.findcorner_c(1, mark2, (i+1))== NEGZ:
                    if   mcube.fx == 1 and mcube.fy == 1:
                        a += "FA.DL.FC."
                        mcube.FA(); mcube.DL(); mcube.FC();
                    elif mcube.fx == 1 and mcube.fy == 4:
                        a += "FA.DL.FC.DR.FA.DL.FC."
                        mcube.FA(); mcube.DL(); mcube.FC(); mcube.DR(); mcube.FA(); mcube.DL(); mcube.FC();
                    elif mcube.fx == 4 and mcube.fy == 1:
                        a += "DL.LD.DR.LU."
                        mcube.DL(); mcube.LD(); mcube.DR(); mcube.LU();
                    elif mcube.fx == 4 and mcube.fy == 4:
                        a += "FC.DR.FA.DR.FA.DR.FC."
                        mcube.FC(); mcube.DR(); mcube.FA(); mcube.DR(); mcube.FA(); mcube.DR(); mcube.FC();
                elif mcube.findcorner_c(1, mark2, (i+1))==POSX:
                    if   mcube.fy == 1 and mcube.fz == 1:
                        a += "LD.DL.LU.";
                        mcube.LD(); mcube.DL(); mcube.LU();
                    elif mcube.fy == 1 and mcube.fz == 4:
                        a += "DR.FA.DR.FC."
                        mcube.DR(); mcube.FA(); mcube.DR(); mcube.FC();
                    elif mcube.fy == 4 and mcube.fz == 1:
                        a += "RD.LD.DL.RU.LU."
                        mcube.RD(); mcube.LD(); mcube.DL(); mcube.RU(); mcube.LU();
                    elif mcube.fy == 4 and mcube.fz == 4:
                        a += "RU.DR.RD.FA.DR.FC."
                        mcube.RU(); mcube.DR(); mcube.RD(); mcube.FA(); mcube.DR(); mcube.FC();
                elif mcube.findcorner_c(1, mark2, (i+1))== POSZ:
                    if mcube.fx == 1 and mcube.fy == 1:
                        a += "FA.DR.FC.";
                        mcube.FA(); mcube.DR(); mcube.FC();
                    elif mcube.fx == 1 and mcube.fy == 4:
                        a += "BA.FA.DR.BC.FC."
                        mcube.BA(); mcube.FA(); mcube.DR(); mcube.BC(); mcube.FC();
                    elif mcube.fx == 4 and mcube.fy == 1:
                        a += "DL.LD.DL.LU."
                        mcube.DL(); mcube.LD(); mcube.DL(); mcube.LU();
                    elif mcube.fx == 4 and mcube.fy == 4:
                        a += "BC.DL.BA.LD.DL.LU."
                        mcube.BC(); mcube.DL(); mcube.BA(); mcube.LD(); mcube.DL(); mcube.LU();
                a += "CL."; mcube.CL();
            iter += 1
            if iter >= ITER_THRESHOLD: mcube.erval = ERR_NONDESCRIPT
    # 检查错误
        if mcube.erval: return ""
        if mcube.shorten >= SHORTEN_STRIP_SOME:   a = mcube.concise(a)
        mcube.mov[step] = len(a) // 3
        s += a
  # step 4:底面角块
        step += 1
        a = ""
        iter = 0
 
        good = 0
        corn = np.zeros(4,dtype=int)
        for i in range(0,4) :corn[i] = 0
        mcube.findcorner_c(6,2,3);
        if mcube.fx <= 1 and mcube.fz <= 1: corn[0]=1; good += 1
        mcube.findcorner_c(6,3,4);
        if mcube.fx >= 4 and mcube.fz <= 1:  corn[1]=1; good += 1
        mcube.findcorner_c(6,4,5);
        if mcube.fx >= 4 and mcube.fz >= 4:  corn[2]=1; good += 1
        mcube.findcorner_c(6,5,2);
        if mcube.fx <= 1 and mcube.fz >= 4:  corn[3]=1; good += 1
        for i in range(1,5):
            if good>=2: break
            a += "DR."; mcube.DR();
            good = 0;
            for j in range(0,4): corn[j] = 0
            mcube.findcorner_c(6,2,3)
            if mcube.fx <= 1 and mcube.fz <= 1:  corn[0]=1; good += 1
            mcube.findcorner_c(6,3,4)
            if mcube.fx >= 4 and mcube.fz <= 1:  corn[1]=1; good += 1
            mcube.findcorner_c(6,4,5)
            if mcube.fx >= 4 and mcube.fz >= 4:  corn[2]=1; good += 1
            mcube.findcorner_c(6,5,2)
            if mcube.fx <= 1 and mcube.fz >= 4:  corn[3]=1; good += 1
        while not mcube.erval and good < 4:
            for i in range(0,4):
                if i<3: mark3= i+1
                if i>=3: mark3 =i-3
                if corn[i] and corn[mark3]:
                    if i==0: a += "CR.CR."; mcube.CR(); mcube.CR();
                    elif i==1: a += "CR."; mcube.CR();
                    elif i==2: pass
                    elif i==3: a += "CL."; mcube.CL();
                    a += "RD.DL.RU.FC.DR.FA.RD.DR.RU.DR.DR."
                    mcube.RD(); mcube.DL(); mcube.RU(); mcube.FC(); mcube.DR(); mcube.FA(); mcube.RD(); mcube.DR(); mcube.RU(); mcube.DR(); mcube.DR();
                    if i ==0: a += "CL.CL."; mcube.CL(); mcube.CL();
                    elif i == 1: a += "CL."; mcube.CL();
                    elif i == 2: pass
                    elif i == 3: a += "CR."; mcube.CR();
                    break
                if i<2: mark4= i+2
                if i>=2: mark4 =i-2
                elif corn[i] and corn[mark4]:
                    if i==0: pass
                    elif i==1: a += "CL."; mcube.CL();
                    elif i==2: pass
                    elif i==3: a += "CR."; mcube.CR();
                    a += "RD.DL.RU.FC.DR.FA.RD.DR.RU.DR.CL.""RD.DL.RU.FC.DR.FA.RD.DR.RU.DR.DR.CR."
                    mcube.RD(); mcube.DL(); mcube.RU(); mcube.FC(); mcube.DR(); mcube.FA(); mcube.RD(); mcube.DR(); mcube.RU(); mcube.DR(); mcube.CL();
                    mcube.RD(); mcube.DL(); mcube.RU(); mcube.FC(); mcube.DR(); mcube.FA(); mcube.RD(); mcube.DR(); mcube.RU(); mcube.DR(); mcube.DR(); mcube.CR();
                    if i==0: pass
                    elif i==1: a += "CR."; mcube.CR();
                    elif i==2: pass
                    elif i==3: a += "CL."; mcube.CL();
                    break
            good = 0
            for i in range(0,4): corn[i] = 0
            mcube.findcorner_c(6,2,3)
            if mcube.fx <= 1 and mcube.fz <= 1:  corn[0]=1; good += 1
            mcube.findcorner_c(6,3,4)
            if mcube.fx >= 4 and mcube.fz <= 1:  corn[1]=1; good += 1
            mcube.findcorner_c(6,4,5)
            if mcube.fx >= 4 and mcube.fz >= 4:  corn[2]=1; good += 1
            mcube.findcorner_c(6,5,2)
            if mcube.fx <= 1 and mcube.fz >= 4:  corn[3]=1; good += 1
            for i in range(1,5):
                if good>=2:break
                a += "DR."; mcube.DR();
                good = 0
                for j in range(0,4): corn[j] = 0
                mcube.findcorner_c(6,2,3)
                if mcube.fx <= 1 and mcube.fz <= 1: corn[0]=1; good += 1
                mcube.findcorner_c(6,3,4)
                if mcube.fx >= 4 and mcube.fz <= 1: corn[1]=1; good += 1
                mcube.findcorner_c(6,4,5)
                if mcube.fx >= 4 and mcube.fz >= 4: corn[2]=1; good += 1
                mcube.findcorner_c(6,5,2)
                if mcube.fx <= 1 and mcube.fz >= 4: corn[3]=1; good += 1
            iter += 1
            if iter >= ITER_THRESHOLD: mcube.erval = ERR_NONDESCRIPT
    # 检查错误
        if mcube.erval: return ""
        if mcube.shorten >= SHORTEN_STRIP_SOME:   a = mcube.concise(a)
        mcube.mov[step] = len(a) // 3
        s += a
  # step 5: 底部角块定向
        step += 1
        a = ""
        iter = 0

        good = 0
        corn[0] = mcube.findcorner_c(6,2,3)
        corn[1] = mcube.findcorner_c(6,3,4)
        corn[2] = mcube.findcorner_c(6,4,5)
        corn[3] = mcube.findcorner_c(6,5,2)
        if corn[0] == NEGY: good+=1
        if corn[1] == NEGY: good+=1
        if corn[2] == NEGY: good+=1
        if corn[3] == NEGY: good+=1
        while not mcube.erval and good < 4:
            if  good == 3:
                mcube.erval = ERR_PARITY_CORNER_ROTATION
                break
            if good==0:
                f = 0
                for i in range(0,4):
                    if i > 0: mark5=i-1
                    if i <= 0: mark5 = i+3
                    if corn[i] == corn[mark5] or corn[i] == -(corn[mark5]):
                        f = 1
                        if i == 0: a += "CR.CR."; mcube.CR(); mcube.CR();
                        elif i==1: a += "CR."; mcube.CR();
                        elif i==2: pass
                        elif i==3: a += "CL."; mcube.CL();
                        if mcube.cube[5][1][1] == 6:
                            a += "RD.DL.DL.RU.DR.RD.DR.RU.""LD.DR.DR.LU.DL.LD.DL.LU."
                            mcube.RD(); mcube.DL(); mcube.DL(); mcube.RU(); mcube.DR(); mcube.RD(); mcube.DR(); mcube.RU();
                            mcube.LD(); mcube.DR(); mcube.DR(); mcube.LU(); mcube.DL(); mcube.LD(); mcube.DL(); mcube.LU();
                        else:
                            a += "LD.DR.LU.DR.LD.DL.DL.LU.""RD.DL.RU.DL.RD.DR.DR.RU."
                            mcube.LD(); mcube.DR(); mcube.LU(); mcube.DR(); mcube.LD(); mcube.DL(); mcube.DL(); mcube.LU();
                            mcube.RD(); mcube.DL(); mcube.RU(); mcube.DL(); mcube.RD(); mcube.DR(); mcube.DR(); mcube.RU();
                        if i==0:a += "CL.CL."; mcube.CL(); mcube.CL();
                        elif i==1:a += "CL."; mcube.CL();
                        elif i==2: pass
                        elif i==3: a += "CR."; mcube.CR();
                        break
                if not f:
                    mcube.erval = ERR_PARITY_CORNER_ROTATION
            elif good== 1:
                for  i in range(0,4):
                    if corn[i] == NEGY:
                        if i==0: pass
                        elif i==1: a += "CL."; mcube.CL();
                        elif i==2: a += "CR.CR."; mcube.CR(); mcube.CR();
                        elif i==3: a += "CR."; mcube.CR();
                        if mcube.cube[4][1][0] == 6:
                            a += "RD.DL.RU.DL.RD.DR.DR.RU.DR.DR."
                            mcube.RD(); mcube.DL(); mcube.RU(); mcube.DL(); mcube.RD(); mcube.DR(); mcube.DR(); mcube.RU(); mcube.DR(); mcube.DR();
                        else:
                            a += "DL.DL.RD.DL.DL.RU.DR.RD.DR.RU."
                            mcube.DL(); mcube.DL(); mcube.RD(); mcube.DL(); mcube.DL(); mcube.RU(); mcube.DR(); mcube.RD(); mcube.DR(); mcube.RU();
                        if i==0: pass
                        elif i==1: a += "CR."; mcube.CR();
                        elif i==2: a += "CL.CL."; mcube.CL(); mcube.CL();
                        elif i==3: a += "CL."; mcube.CL();
                        break
            elif good==2:
                for i in range(0,4):
                    if i>0: mark6 = i-1
                    if i<=0: mark6 = i+3
                    if corn[i] == NEGY and corn[mark6] == NEGY:
                        if i==0: pass
                        elif i==1: a += "CL."; mcube.CL();
                        elif i==2: a += "CR.CR."; mcube.CR(); mcube.CR();
                        elif i==3: a += "CR."; mcube.CR();
                        if mcube.cube[5][1][1] == 6:
                            a += "RD.DL.DL.RU.DR.RD.DR.RU.""LD.DR.DR.LU.DL.LD.DL.LU."
                            mcube.RD(); mcube.DL(); mcube.DL(); mcube.RU(); mcube.DR(); mcube.RD(); mcube.DR(); mcube.RU();
                            mcube.LD(); mcube.DR(); mcube.DR(); mcube.LU(); mcube.DL(); mcube.LD(); mcube.DL(); mcube.LU();
                        else:
                            a += "LD.DR.LU.DR.LD.DL.DL.LU.""RD.DL.RU.DL.RD.DR.DR.RU."
                            mcube.LD(); mcube.DR(); mcube.LU(); mcube.DR(); mcube.LD(); mcube.DL(); mcube.DL(); mcube.LU();
                            mcube.RD(); mcube.DL(); mcube.RU(); mcube.DL(); mcube.RD(); mcube.DR(); mcube.DR(); mcube.RU();
                        if i==0: pass
                        elif i==1: a += "CR."; mcube.CR();
                        elif i==2: a += "CL.CL."; mcube.CL(); mcube.CL();
                        elif i==3: a += "CL."; mcube.CL();
                        break
                    if i<2: mark7=i+2
                    if i>=2: mark7=i-2
                    elif corn[i] == NEGY and corn[mark7] == NEGY:
                        if i==0: pass
                        elif i==1: a += "CL."; mcube.CL();
                        elif i==2: pass
                        elif i==3: a += "CR."; mcube.CR();
                        if mcube.cube[4][1][0] == 6:
                            a += "CL.LD.DR.LU.DR.LD.DL.DL.LU.""RD.DL.RU.DL.RD.DR.DR.RU.""CR.LD.DR.LU.DR.LD.DL.DL.LU.""RD.DL.RU.DL.RD.DR.DR.RU."
                            mcube.CL(); mcube.LD(); mcube.DR(); mcube.LU(); mcube.DR(); mcube.LD(); mcube.DL(); mcube.DL(); mcube.LU();
                            mcube.RD(); mcube.DL(); mcube.RU(); mcube.DL(); mcube.RD(); mcube.DR(); mcube.DR(); mcube.RU();
                            mcube.CR(); mcube.LD(); mcube.DR(); mcube.LU(); mcube.DR(); mcube.LD(); mcube.DL(); mcube.DL(); mcube.LU();
                            mcube.RD(); mcube.DL(); mcube.RU(); mcube.DL(); mcube.RD(); mcube.DR(); mcube.DR(); mcube.RU();
                        else:
                            a += "RD.DL.DL.RU.DR.RD.DR.RU.""LD.DR.DR.LU.DL.LD.DL.LU.CL.""RD.DL.DL.RU.DR.RD.DR.RU.""LD.DR.DR.LU.DL.LD.DL.LU.CR."
                            mcube.RD(); mcube.DL(); mcube.DL(); mcube.RU(); mcube.DR(); mcube.RD(); mcube.DR(); mcube.RU();
                            mcube.LD(); mcube.DR(); mcube.DR(); mcube.LU(); mcube.DL(); mcube.LD(); mcube.DL(); mcube.LU(); mcube.CL();
                            mcube.RD(); mcube.DL(); mcube.DL(); mcube.RU(); mcube.DR(); mcube.RD(); mcube.DR(); mcube.RU();
                            mcube.LD(); mcube.DR(); mcube.DR(); mcube.LU(); mcube.DL(); mcube.LD(); mcube.DL(); mcube.LU(); mcube.CR();
                        if i==0: pass
                        elif i==1: a += "CR."; mcube.CR();
                        elif i==2: pass
                        elif i==3: a += "CL."; mcube.CL();
                        break
            good = 0
            corn[0] = mcube.findcorner_c(6,2,3)
            corn[1] = mcube.findcorner_c(6,3,4)
            corn[2] = mcube.findcorner_c(6,4,5)
            corn[3] = mcube.findcorner_c(6,5,2)
            if corn[0] == NEGY: good += 1
            if corn[1] == NEGY: good += 1
            if corn[2] == NEGY: good += 1
            if corn[3] == NEGY: good += 1
            iter += 1
            if iter >= ITER_THRESHOLD: mcube.erval = ERR_NONDESCRIPT
    # 检查错误
        if mcube.erval: return ""
        if mcube.shorten >= SHORTEN_STRIP_SOME: a = mcube.concise(a)
        mcube.mov[step] = len(a) // 3
        s += a
  # step 6: 3/4顶部边缘匹配
        step += 1
        a = ""
        iter = 0

        good = 0
        if mcube.cube[4][5][2] == 1 and mcube.cube[5][4][2] == 4 and mcube.cube[4][5][3] == 1 and mcube.cube[5][4][3] == 4 and mcube.cube[2][5][4] == 1 and mcube.cube[2][4][5] == 5 and mcube.cube[3][5][4] == 1 and mcube.cube[3][4][5] == 5 and mcube.cube[1][5][2] == 1 and mcube.cube[0][4][2] == 2 and mcube.cube[1][5][3] == 1 and mcube.cube[0][4][3] == 2 :
            good = 1
        while not mcube.erval and good < 1:
            a += "CL."; mcube.CL();
            for i in range (1,4):
                if i<3 : mark8=i+3
                if i>=3: mark8=i-1
                fnd = mcube.findedge_l(1,mark8)
                if fnd == POSY:
                    if  mcube.fx == 1:
                        a += "LD.dR.LU.dR.FC.dL.FA."
                        mcube.LD(); mcube.dR(); mcube.LU(); mcube.dR(); mcube.FC(); mcube.dL(); mcube.FA();
                    elif mcube.fz == 1: pass
                    elif mcube.fx == 4:
                        a += "RD.uL.RU.uL.FA.uR.FC."
                        mcube.RD(); mcube.uL(); mcube.RU(); mcube.uL(); mcube.FA(); mcube.uR(); mcube.FC();
                    elif mcube.fz == 4:
                        a += "BA.dL.dL.BC.dR.FC.dL.FA."
                        mcube.BA(); mcube.dL(); mcube.dL(); mcube.BC(); mcube.dR(); mcube.FC(); mcube.dL(); mcube.FA();
                elif fnd == NEGY:
                    if mcube.fx == 1:
                        a += "DR.DR.RU.uL.RD.uL.FA.uR.FC.DL.DL."
                        mcube.DR(); mcube.DR(); mcube.RU(); mcube.uL(); mcube.RD(); mcube.uL(); mcube.FA(); mcube.uR(); mcube.FC(); mcube.DL(); mcube.DL();
                    elif mcube.fz == 1:
                        a += "DR.RU.uL.RD.uL.FA.uR.FC.DL."
                        mcube.DR(); mcube.RU(); mcube.uL(); mcube.RD(); mcube.uL(); mcube.FA(); mcube.uR(); mcube.FC(); mcube.DL();
                    elif mcube.fx == 4:
                        a += "RU.uL.RD.uL.FA.uR.FC."
                        mcube.RU(); mcube.uL(); mcube.RD(); mcube.uL(); mcube.FA(); mcube.uR(); mcube.FC();
                    elif mcube.fz == 4:
                        a += "DL.RU.uL.RD.uL.FA.uR.FC.DR."
                        mcube.DL(); mcube.RU(); mcube.uL(); mcube.RD(); mcube.uL(); mcube.FA(); mcube.uR(); mcube.FC(); mcube.DR();
                elif fnd==NEGX:
                    if mcube.fz == 1:
                        a += "uL.FA.uR.FC."
                        mcube.uL(); mcube.FA(); mcube.uR(); mcube.FC();
                    elif mcube.fz == 4:
                        a += "dL.FC.dL.FA.";
                        mcube.dL(); mcube.FC(); mcube.dL(); mcube.FA();
                    elif mcube.fy == 4:
                        a += "LU.dL.LD.FC.dL.FA."
                        mcube.LU(); mcube.dL(); mcube.LD(); mcube.FC(); mcube.dL(); mcube.FA();
                    elif mcube.fy == 1:
                        a += "DR.DR.RD.uR.RU.FA.uR.FC.DL.DL."
                        mcube.DR(); mcube.DR(); mcube.RD(); mcube.uR(); mcube.RU(); mcube.FA(); mcube.uR(); mcube.FC(); mcube.DL(); mcube.DL();
                elif fnd==NEGZ:
                    if  mcube.fx == 1:
                        a += "dR.dR.FC.dL.FA."
                        mcube.dR(); mcube.dR(); mcube.FC(); mcube.dL(); mcube.FA();
                    elif mcube.fx == 4:
                        a += "uL.uL.FA.uR.FC."
                        mcube.uL(); mcube.uL(); mcube.FA(); mcube.uR(); mcube.FC();
                    elif mcube.fy == 4:
                        a += "FC.uR.FA.uR.FA.uR.FC."
                        mcube.FC(); mcube.uR(); mcube.FA(); mcube.uR(); mcube.FA(); mcube.uR(); mcube.FC();
                    elif mcube.fy == 1:
                        a += "FA.uR.FC.uR.FA.uR.FC.";
                        mcube.FA(); mcube.uR(); mcube.FC(); mcube.uR(); mcube.FA(); mcube.uR(); mcube.FC();
                elif fnd==POSX:
                    if   mcube.fz == 1:
                        a += "dR.FC.dL.FA."
                        mcube.dR(); mcube.FC(); mcube.dL(); mcube.FA();
                    elif mcube.fz == 4:
                        a += "uR.FA.uR.FC."
                        mcube.uR(); mcube.FA(); mcube.uR(); mcube.FC();
                    elif mcube.fy == 4:
                        a += "RU.uR.RD.FA.uR.FC."
                        mcube.RU(); mcube.uR(); mcube.RD(); mcube.FA(); mcube.uR(); mcube.FC();
                    elif mcube.fy == 1:
                        a += "RD.uR.RU.FA.uR.FC."
                        mcube.RD(); mcube.uR(); mcube.RU(); mcube.FA(); mcube.uR(); mcube.FC();
                elif fnd==POSZ:
                    if  mcube.fx == 1:
                        a += "FA.uR.FC."
                        mcube.FA(); mcube.uR(); mcube.FC();
                    elif mcube.fx == 4:
                        a += "FC.dL.FA."
                        mcube.FC(); mcube.dL(); mcube.FA();
                    elif mcube.fy == 4:
                        a += "BC.dL.BA.dR.FC.dL.FA."
                        mcube.BC(); mcube.dL(); mcube.BA(); mcube.dR(); mcube.FC(); mcube.dL(); mcube.FA();
                    elif mcube.fy == 1:
                        a += "DL.RD.uR.RU.FA.uR.FC.DR."
                        mcube.DL(); mcube.RD(); mcube.uR(); mcube.RU(); mcube.FA(); mcube.uR(); mcube.FC(); mcube.DR();
                if i<3: mark20=i+3
                if i>=3: mark20=i-1
                fnd = mcube.findedge_r(1,mark20)
                if fnd==POSY:
                    if  mcube.fx == 1:
                        a += "LD.uR.LU.uR.FC.uL.FA."
                        mcube.LD(); mcube.uR(); mcube.LU(); mcube.uR(); mcube.FC(); mcube.uL(); mcube.FA();
                    elif mcube.fz == 1: pass
                    elif mcube.fx == 4:
                        a += "RD.dL.RU.dL.FA.dR.FC.";
                        mcube.RD(); mcube.dL(); mcube.RU(); mcube.dL(); mcube.FA(); mcube.dR(); mcube.FC();
                    elif mcube.fz == 4:
                        a += "BC.dR.dR.BA.dL.FA.dR.FC."
                        mcube.BC(); mcube.dR(); mcube.dR(); mcube.BA(); mcube.dL(); mcube.FA(); mcube.dR(); mcube.FC();
                elif fnd==NEGY:
                    if  mcube.fx == 1:
                        a += "DR.DR.RU.dL.RD.dL.FA.dR.FC.DL.DL."
                        mcube.DR(); mcube.DR(); mcube.RU(); mcube.dL(); mcube.RD(); mcube.dL(); mcube.FA(); mcube.dR(); mcube.FC(); mcube.DL(); mcube.DL();
                    elif mcube.fz == 1:
                        a += "DR.RU.dL.RD.dL.FA.dR.FC.DL."
                        mcube.DR(); mcube.RU(); mcube.dL(); mcube.RD(); mcube.dL(); mcube.FA(); mcube.dR(); mcube.FC(); mcube.DL();
                    elif mcube.fx == 4:
                        a += "RU.dL.RD.dL.FA.dR.FC."
                        mcube.RU(); mcube.dL(); mcube.RD(); mcube.dL(); mcube.FA(); mcube.dR(); mcube.FC();
                    elif mcube.fz == 4:
                        a += "DL.RU.dL.RD.dL.FA.dR.FC.DR."
                        mcube.DL(); mcube.RU(); mcube.dL(); mcube.RD(); mcube.dL(); mcube.FA(); mcube.dR(); mcube.FC(); mcube.DR();
                elif fnd==NEGX:
                    if  mcube.fz == 1:
                        a += "dL.FA.dR.FC."
                        mcube.dL(); mcube.FA(); mcube.dR(); mcube.FC();
                    elif mcube.fz == 4:
                        a += "uL.FC.uL.FA."
                        mcube.uL(); mcube.FC(); mcube.uL(); mcube.FA();
                    elif mcube.fy == 4:
                        a += "LU.uL.LD.FC.uL.FA."
                        mcube.LU(); mcube.uL(); mcube.LD(); mcube.FC(); mcube.uL(); mcube.FA();
                    elif mcube.fy == 1:
                        a += "DR.DR.RD.dR.RU.FA.dR.FC.DL.DL.";
                        mcube.DR(); mcube.DR(); mcube.RD(); mcube.dR(); mcube.RU(); mcube.FA(); mcube.dR(); mcube.FC(); mcube.DL(); mcube.DL();
                elif fnd==NEGZ:
                    if  mcube.fx == 1:
                        a += "uR.uR.FC.uL.FA."
                        mcube.uR(); mcube.uR(); mcube.FC(); mcube.uL(); mcube.FA();
                    elif mcube.fx == 4:
                        a += "dL.dL.FA.dR.FC."
                        mcube.dL(); mcube.dL(); mcube.FA(); mcube.dR(); mcube.FC();
                    elif mcube.fy == 4:
                        a += "FA.uL.FC.uL.FC.uL.FA."
                        mcube.FA(); mcube.uL(); mcube.FC(); mcube.uL(); mcube.FC(); mcube.uL(); mcube.FA();
                    elif mcube.fy == 1:
                        a += "FC.uL.FA.uL.FC.uL.FA."
                        mcube.FC(); mcube.uL(); mcube.FA(); mcube.uL(); mcube.FC(); mcube.uL(); mcube.FA();
                elif fnd==POSX:
                    if  mcube.fz == 1:
                        a += "uR.FC.uL.FA."
                        mcube.uR(); mcube.FC(); mcube.uL(); mcube.FA();
                    elif mcube.fz == 4:
                        a += "dR.FA.dR.FC."
                        mcube.dR(); mcube.FA(); mcube.dR(); mcube.FC();
                    elif mcube.fy == 4:
                        a += "RU.dR.RD.FA.dR.FC."
                        mcube.RU(); mcube.dR(); mcube.RD(); mcube.FA(); mcube.dR(); mcube.FC();
                    elif mcube.fy == 1:
                        a += "RD.dR.RU.FA.dR.FC."
                        mcube.RD(); mcube.dR(); mcube.RU(); mcube.FA(); mcube.dR(); mcube.FC();
                elif fnd==POSZ:
                    if   mcube.fx == 1:
                        a += "FA.dR.FC."
                        mcube.FA(); mcube.dR(); mcube.FC();
                    elif mcube.fx == 4:
                        a += "FC.uL.FA."
                        mcube.FC(); mcube.uL(); mcube.FA();
                    elif mcube.fy == 4:
                        a += "BA.dR.BC.dL.FA.dR.FC."
                        mcube.BA(); mcube.dR(); mcube.BC(); mcube.dL(); mcube.FA(); mcube.dR(); mcube.FC();
                    elif mcube.fy == 1:
                        a += "DL.RD.dR.RU.FA.dR.FC.DR."
                        mcube.DL(); mcube.RD(); mcube.dR(); mcube.RU(); mcube.FA(); mcube.dR(); mcube.FC(); mcube.DR();
                a += "CL."; mcube.CL();
            if mcube.cube[4][5][2] == 1 and mcube.cube[5][4][2] == 4 and mcube.cube[4][5][3] == 1 and mcube.cube[5][4][3] == 4 and mcube.cube[2][5][4] == 1 and mcube.cube[2][4][5] == 5 and mcube.cube[3][5][4] == 1 and mcube.cube[3][4][5] == 5 and mcube.cube[1][5][2] == 1 and mcube.cube[0][4][2] == 2 and mcube.cube[1][5][3] == 1 and mcube.cube[0][4][3] == 2:
                good = 1
            iter += 1
            if iter >= ITER_THRESHOLD: mcube.erval = ERR_NONDESCRIPT
    #检查错误
        if mcube.erval: return ""
        if mcube.shorten >= SHORTEN_STRIP_SOME: a = mcube.concise(a)
        mcube.mov[step] = len(a) // 3
        s += a
  # step 7: 底部边缘
        step += 1
        a = ""
        iter = 0
        fnd=0

        good = 0
        if mcube.cube[1][0][2] == 6 and mcube.cube[0][1][2] == 2 and mcube.cube[1][0][3] == 6 and mcube.cube[0][1][3] == 2 and mcube.cube[2][0][1] == 6 and mcube.cube[2][1][0] == 3 and mcube.cube[3][0][1] == 6 and mcube.cube[2][1][0] == 3 and mcube.cube[4][0][2] == 6 and mcube.cube[5][1][2] == 4 and mcube.cube[4][0][3] == 6 and mcube.cube[5][1][3] == 4 and mcube.cube[2][0][4] == 6 and mcube.cube[2][1][5] == 5 and mcube.cube[3][0][4] == 6 and mcube.cube[3][1][5] == 5 :
            good = 1
        while (not mcube.erval) and good < 1:
            for i in range(1,5):
                if i<4: mark9=i+2
                if i>=4: mark9=i-2
                fnd = mcube.findedge_l(6,mark9);
                if fnd==POSY:
                    a += "FA.uL.FC.FC.uR.FA."
                    mcube.FA(); mcube.uL(); mcube.FC(); mcube.FC(); mcube.uR(); mcube.FA();
                elif fnd==NEGY:
                    if  mcube.fx == 1:
                        a += "DR.FA.dR.FC.DL.FA.dL.FC."
                        mcube.DR(); mcube.FA(); mcube.dR(); mcube.FC(); mcube.DL(); mcube.FA(); mcube.dL(); mcube.FC();
                    elif mcube.fz == 1: pass
                    elif mcube.fx == 4:
                        a += "DL.FA.dR.FC.DR.FA.dL.FC.";
                        mcube.DL(); mcube.FA(); mcube.dR(); mcube.FC(); mcube.DR(); mcube.FA(); mcube.dL(); mcube.FC();
                    elif mcube.fz == 4:
                        a += "DR.DR.FA.dR.FC.DL.DL.FA.dL.FC."
                        mcube.DR(); mcube.DR(); mcube.FA(); mcube.dR(); mcube.FC(); mcube.DL(); mcube.DL(); mcube.FA(); mcube.dL(); mcube.FC();
                elif fnd==NEGX:
                    if   mcube.fz == 1:
                        a += "uL.FC.uR.FA."
                        mcube.uL(); mcube.FC(); mcube.uR(); mcube.FA();
                    elif mcube.fz == 4:
                        a += "dL.FA.dL.FC."
                        mcube.dL(); mcube.FA(); mcube.dL(); mcube.FC();
                    elif mcube.fy == 1:
                        a += "DR.FC.dL.FA.DL.dL.FA.dL.FC."
                        mcube.DR(); mcube.FC(); mcube.dL(); mcube.FA(); mcube.DL(); mcube.dL(); mcube.FA(); mcube.dL(); mcube.FC();
                elif fnd==NEGZ:
                    if   mcube.fx == 1:
                        a += "dR.dR.FA.dL.FC."
                        mcube.dR(); mcube.dR(); mcube.FA(); mcube.dL(); mcube.FC();
                    elif mcube.fx == 4:
                        a += "uL.uL.FC.uR.FA."
                        mcube.uL(); mcube.uL(); mcube.FC(); mcube.uR(); mcube.FA();
                    elif mcube.fy == 4:
                        a += "FA.dL.FC.dL.FA.dL.FC."
                        mcube.FA(); mcube.dL(); mcube.FC(); mcube.dL(); mcube.FA(); mcube.dL(); mcube.FC();
                    elif mcube.fy == 1:
                        a += "FC.dL.FA.dL.FA.dL.FC."
                        mcube.FC(); mcube.dL(); mcube.FA(); mcube.dL(); mcube.FA(); mcube.dL(); mcube.FC();
                elif fnd==POSX:
                    if  mcube.fz == 1:
                        a += "dR.FA.dL.FC."
                        mcube.dR(); mcube.FA(); mcube.dL(); mcube.FC();
                    elif mcube.fz == 4:
                        a += "uR.FC.uR.FA."
                        mcube.uR(); mcube.FC(); mcube.uR(); mcube.FA();
                    elif mcube.fy == 1:
                        a += "DL.FC.dL.FA.DR.dL.FA.dL.FC."
                        mcube.DL(); mcube.FC(); mcube.dL(); mcube.FA(); mcube.DR(); mcube.dL(); mcube.FA(); mcube.dL(); mcube.FC();
                elif fnd==POSZ:
                    if  mcube.fx == 1:
                        a += "FC.uR.FA."
                        mcube.FC(); mcube.uR(); mcube.FA();
                    elif mcube.fx == 4:
                        a += "FA.dL.FC."
                        mcube.FA(); mcube.dL(); mcube.FC();
                    elif mcube.fy == 1:
                        a += "DL.DL.FC.dL.FA.DR.DR.dL.FA.dL.FC."
                        mcube.DL(); mcube.DL(); mcube.FC(); mcube.dL(); mcube.FA(); mcube.DR(); mcube.DR(); mcube.dL(); mcube.FA(); mcube.dL(); mcube.FC();
                if i<4: mark10=i+2
                if i>=4: mark10=i-2
                fnd = mcube.findedge_r(6,mark10)
                if fnd==POSY:
                    a += "FC.uR.FA.FA.uL.FC."
                    mcube.FC(); mcube.uR(); mcube.FA(); mcube.FA(); mcube.uL(); mcube.FC();
                    if mcube.cube[2][4][0] == 6 and mcube.cube[2][5][1] == mark10:pass
                elif fnd==NEGY:
                    if  mcube.fx == 1:
                        a += "DR.FC.dL.FA.DL.FC.dR.FA."
                        mcube.DR(); mcube.FC(); mcube.dL(); mcube.FA(); mcube.DL(); mcube.FC(); mcube.dR(); mcube.FA();
                    elif mcube.fz == 1: pass
                    elif mcube.fx == 4:
                        a += "DL.FC.dL.FA.DR.FC.dR.FA."
                        mcube.DL(); mcube.FC(); mcube.dL(); mcube.FA(); mcube.DR(); mcube.FC(); mcube.dR(); mcube.FA();
                    elif mcube.fz == 4:
                        a += "DR.DR.FC.dL.FA.DL.DL.FC.dR.FA."
                        mcube.DR(); mcube.DR(); mcube.FC(); mcube.dL(); mcube.FA(); mcube.DL(); mcube.DL(); mcube.FC(); mcube.dR(); mcube.FA();
                elif fnd==NEGX:
                    if   mcube.fz == 1:
                        a += "dL.FC.dR.FA."
                        mcube.dL(); mcube.FC(); mcube.dR(); mcube.FA();
                    elif mcube.fz == 4:
                        a += "uL.FA.uL.FC."
                        mcube.uL(); mcube.FA(); mcube.uL(); mcube.FC();
                    elif mcube.fy == 1:
                        a += "DR.FA.dR.FC.DL.dR.FC.dR.FA."
                        mcube.DR(); mcube.FA(); mcube.dR(); mcube.FC(); mcube.DL(); mcube.dR(); mcube.FC(); mcube.dR(); mcube.FA();
                elif fnd==NEGZ:
                    if  mcube.fx == 1:
                        a += "uR.uR.FA.uL.FC."
                        mcube.uR(); mcube.uR(); mcube.FA(); mcube.uL(); mcube.FC();
                    elif mcube.fx == 4:
                        a += "dL.dL.FC.dR.FA."
                        mcube.dL(); mcube.dL(); mcube.FC(); mcube.dR(); mcube.FA();
                    elif mcube.fy == 4:
                        a += "FC.dR.FA.dR.FC.dR.FA."
                        mcube.FC(); mcube.dR(); mcube.FA(); mcube.dR(); mcube.FC(); mcube.dR(); mcube.FA();
                    elif mcube.fy == 1:
                        a += "FA.dR.FC.dR.FC.dR.FA."
                        mcube.FA(); mcube.dR(); mcube.FC(); mcube.dR(); mcube.FC(); mcube.dR(); mcube.FA();
                elif fnd==POSX:
                    if mcube.fz == 1:
                        a += "uR.FA.uL.FC."
                        mcube.uR(); mcube.FA(); mcube.uL(); mcube.FC();
                    elif mcube.fz == 4:
                        a += "dR.FC.dR.FA.";
                        mcube.dR(); mcube.FC(); mcube.dR(); mcube.FA();
                    elif mcube.fy == 1:
                        a += "DL.FA.dR.FC.DR.dR.FC.dR.FA.";
                        mcube.DL(); mcube.FA(); mcube.dR(); mcube.FC(); mcube.DR(); mcube.dR(); mcube.FC(); mcube.dR(); mcube.FA();
                elif fnd==POSZ:
                    if  mcube.fx == 1:
                        a += "FC.dR.FA."
                        mcube.FC(); mcube.dR(); mcube.FA();
                    elif mcube.fx == 4:
                        a += "FA.uL.FC."
                        mcube.FA(); mcube.uL(); mcube.FC();
                    elif mcube.fy == 1:
                        a += "DL.DL.FA.dR.FC.DR.DR.dR.FC.dR.FA."
                        mcube.DL(); mcube.DL(); mcube.FA(); mcube.dR(); mcube.FC(); mcube.DR(); mcube.DR(); mcube.dR(); mcube.FC(); mcube.dR(); mcube.FA();
                a += "CL.UR."; mcube.CL(); mcube.UR();
            if mcube.cube[1][0][2] == 6 and mcube.cube[0][1][2] == 2 and mcube.cube[1][0][3] == 6 and mcube.cube[0][1][3] == 2 and mcube.cube[2][0][1] == 6 and mcube.cube[2][1][0] == 3 and mcube.cube[3][0][1] == 6 and mcube.cube[2][1][0] == 3 and mcube.cube[4][0][2] == 6 and mcube.cube[5][1][2] == 4 and mcube.cube[4][0][3] == 6 and mcube.cube[5][1][3] == 4 and mcube.cube[2][0][4] == 6 and mcube.cube[2][1][5] == 5 and mcube.cube[3][0][4] == 6 and mcube.cube[3][1][5] == 5 :
                good = 1
            iter += 1
            if iter >= ITER_THRESHOLD: mcube.erval = ERR_NONDESCRIPT
    # 检查错误
        if mcube.erval: return "";
        if mcube.shorten >= SHORTEN_STRIP_SOME: a = mcube.concise(a)
        mcube.mov[step] = len(a) // 3;
        s += a;
  # step 8: 顶部边缘配对
        step += 1
        a = ""
        iter = 0
        l_fnd=0; r_fnd=0; lx=0; ly=0; lz=0; rx=0; ry=0; rz=0
        good = 0
        if mcube.cube[2][5][1] == 1 and mcube.cube[2][4][0] == 3 and mcube.cube[3][5][1] == 1 and mcube.cube[3][4][0] == 3 : good = 1
        while (not mcube.erval) and good < 1:
            l_fnd = mcube.findedge_l(1,3)
            lx = mcube.fx; ly = mcube.fy; lz = mcube.fz;
            r_fnd = mcube.findedge_r(1,3)
            rx = mcube.fx; ry = mcube.fy; rz = mcube.fz;
            if ly == 2 and ry == 2:
                for i in range(1,5):
                    if ((lx <= 1 and lz <= 1 and rx >= 4) or(rx <= 1 and rz <= 1 and lx >= 4)):break
                    a += "dL."; mcube.dL();
                    l_fnd = mcube.findedge_l(1, 3);lx = mcube.fx;ly = mcube.fy;lz = mcube.fz
                    r_fnd = mcube.findedge_r(1, 3);rx = mcube.fx;ry = mcube.fy;rz = mcube.fz
                a += "RU.RU.uL.uL.RU.RU.";
                mcube.RU(); mcube.RU(); mcube.uL(); mcube.uL(); mcube.RU(); mcube.RU();
                l_fnd = mcube.findedge_l(1, 3);lx = mcube.fx;ly = mcube.fy;lz = mcube.fz
                r_fnd = mcube.findedge_r(1, 3);rx = mcube.fx;ry = mcube.fy;rz = mcube.fz
            elif ly == 3 and ry == 3:
                for i in range(1,5):
                    if ((lx <= 1 and lz <= 1 and rx >= 4) or (rx <= 1 and rz <= 1 and lx >= 4)):break
                    a += "uL."; mcube.uL();
                    l_fnd = mcube.findedge_l(1, 3);lx = mcube.fx;ly = mcube.fy;lz = mcube.fz
                    r_fnd = mcube.findedge_r(1, 3);rx = mcube.fx;ry = mcube.fy;rz = mcube.fz
                a += "RU.RU.dL.dL.RU.RU.";
                mcube.RU(); mcube.RU(); mcube.dL(); mcube.dL(); mcube.RU(); mcube.RU();
                l_fnd = mcube.findedge_l(1, 3);lx = mcube.fx;ly = mcube.fy;lz = mcube.fz
                r_fnd = mcube.findedge_r(1, 3);rx = mcube.fx;ry = mcube.fy;rz = mcube.fz
            elif ly >= 4 or ry >= 4:
                if ly == 2:
                    for i in range(1,5):
                        if not lz <= 1:break
                        a += "dL."; mcube.dL();
                        l_fnd = mcube.findedge_l(1, 3);lx = mcube.fx;ly = mcube.fy;lz = mcube.fz
                if ly == 3:
                    for i in range(1,5):
                        if not lz <= 1:break
                        a += "uL."; mcube.uL();
                        l_fnd = mcube.findedge_l(1, 3);lx = mcube.fx;ly = mcube.fy;lz = mcube.fz
                if ry == 2:
                    for i in range(1,5):
                        if not rz <= 1:break
                        a += "dL."; mcube.dL();
                        r_fnd = mcube.findedge_r(1, 3);rx = mcube.fx;ry = mcube.fy;rz = mcube.fz
                if ry == 3:
                    for i in range(1,5) :
                        if not rz <= 1:break
                        a += "uL."; mcube.uL();
                        r_fnd = mcube.findedge_r(1, 3);rx = mcube.fx;ry = mcube.fy;rz = mcube.fz
                a += "lU.rU.FA.lD.rD.FA.FA.lU.rU.FA.lD.rD.";
                mcube.lU(); mcube.rU(); mcube.FA(); mcube.lD(); mcube.rD(); mcube.FA(); mcube.FA(); mcube.lU(); mcube.rU(); mcube.FA(); mcube.lD(); mcube.rD();
                l_fnd = mcube.findedge_l(1, 3);lx = mcube.fx;ly = mcube.fy;lz = mcube.fz
                r_fnd = mcube.findedge_r(1, 3);rx = mcube.fx;ry = mcube.fy;rz = mcube.fz
            if ly == 2 and ry == 3:
                for i in range(1,5):
                    if (lx <= 1 and lz <= 1):break
                    a += "dL."; mcube.dL();
                    l_fnd = mcube.findedge_l(1, 3);lx = mcube.fx;ly = mcube.fy;lz = mcube.fz
                for i in range(1,5):
                    if (rx <= 1 and rz <= 1):break
                    a += "uL."; mcube.uL();
                    r_fnd = mcube.findedge_r(1, 3);rx = mcube.fx;ry = mcube.fy;rz = mcube.fz
            elif ly == 3 and ry == 2:
                for i in range(1,5) :
                    if  (lx <= 1 and lz <= 1):break
                    a += "uL."; mcube.uL();
                    l_fnd = mcube.findedge_l(1, 3);lx = mcube.fx;ly = mcube.fy;lz = mcube.fz
                for i in range(1,5) :
                    if rx <= 1 and rz <= 1:break
                    a += "dL."; mcube.dL();
                    r_fnd = mcube.findedge_r(1, 3);rx = mcube.fx;ry = mcube.fy;rz = mcube.fz
            if ((ly == 2 and ry == 3) or (ly == 3 and ry == 2)) and (lx <= 1 and lz <= 1 and lx == rx and lz == rz) :
                if r_fnd == NEGZ:
                    a += "lU.rU.FC.lD.rD.FC.FC.lU.rU.FC.lD.rD."
                    mcube.lU(); mcube.rU(); mcube.FC(); mcube.lD(); mcube.rD(); mcube.FC();
                    mcube.FC(); mcube.lU(); mcube.rU(); mcube.FC(); mcube.lD(); mcube.rD();
                elif r_fnd == NEGX:
                    a += "uR.dR.lU.rU.FA.lD.rD.FA.FA.lU.rU.FA.lD.rD."
                    mcube.uR(); mcube.dR(); mcube.lU(); mcube.rU(); mcube.FA(); mcube.lD(); mcube.rD();
                    mcube.FA(); mcube.FA(); mcube.lU(); mcube.rU(); mcube.FA(); mcube.lD(); mcube.rD();
            if mcube.cube[2][5][1] == 1 and mcube.cube[2][4][0] == 3 and mcube.cube[3][5][1] == 1 and mcube.cube[3][4][0] == 3 :
                good = 1
            iter += 1
            if iter >= ITER_THRESHOLD: mcube.erval = ERR_NONDESCRIPT
    # 检查错误
        if mcube.erval:return ""
        if mcube.shorten >= SHORTEN_STRIP_SOME: a = mcube.concise(a)
        mcube.mov[step] = len(a) // 3
        s += a
  # step 9: 第二排边缘
        step += 1
        a = ""
        iter = 0
    # fix
        good = 0
        if mcube.cube[0][3][1] == 2 and mcube.cube[1][3][0] == 3: good += 1
        if mcube.cube[4][3][0] == 3 and mcube.cube[5][3][1] == 4: good += 1
        if mcube.cube[5][3][4] == 4 and mcube.cube[4][3][5] == 5: good += 1
        if mcube.cube[1][3][5] == 5 and mcube.cube[0][3][4] == 2: good += 1
        while not mcube.erval and good < 4:
            r_fnd = mcube.findedge_r(4,3)
            if mcube.fy == 2:
                for i in range(1,5):
                    if mcube.fx >= 4:break
                    a += "dL."; mcube.dL();
                    r_fnd = mcube.findedge_r(4,3)
                a += "RU.RU.uL.uL.RD.RD."
                mcube.RU(); mcube.RU(); mcube.uL(); mcube.uL(); mcube.RD(); mcube.RD();
                r_fnd = mcube.findedge_r(4,3)
            if r_fnd == POSX: pass
            elif r_fnd == POSZ: a += "uL."; mcube.uL();
            elif r_fnd == NEGX: a += "uL.uL."; mcube.uL(); mcube.uL();
            elif r_fnd == NEGZ: a += "uR."; mcube.uR();
            r_fnd = mcube.findedge_r(3,2)
            if not (mcube.fx == 1 and mcube.fy == 3 and mcube.fz == 0):
                for i in range(1,5):
                    if mcube.fy != 3:break
                    a += "BA.BA.dL.dL.BA.BA."
                    mcube.BA(); mcube.BA(); mcube.dL(); mcube.dL(); mcube.BA(); mcube.BA();
                    r_fnd = mcube.findedge_r(3,2)
                for i in range(1,5) :
                    if mcube.fx >= 4 and mcube.fz <= 1:break
                    a += "dL."; mcube.dL();
                    r_fnd = mcube.findedge_r(3,2)
                a += "LU.LU.dL.dL.LU.LU.";
                mcube.LU(); mcube.LU(); mcube.dL(); mcube.dL(); mcube.LU(); mcube.LU();
            r_fnd = mcube.findedge_r(2,5);
            if not (mcube.fx == 0 and mcube.fy == 3 and mcube.fz == 4):
                for i in range(1,5):
                    if mcube.fy != 3:break
                    a += "BC.BC.dL.dL.BC.BC."
                    mcube.BC(); mcube.BC(); mcube.dL(); mcube.dL(); mcube.BC(); mcube.BC();
                    r_fnd = mcube.findedge_r(2,5)
                for i in range(1,5):
                    if mcube.fx <= 1 and mcube.fz <= 1:break
                    a += "dL."; mcube.dL();
                    r_fnd = mcube.findedge_r(2,5);
                a += "BC.BC.dL.dL.BC.BC.";
                mcube.BC(); mcube.BC(); mcube.dL(); mcube.dL(); mcube.BC(); mcube.BC();
            r_fnd = mcube.findedge_r(5,4);
            if not (mcube.fx == 4 and mcube.fy == 3 and mcube.fz == 5):
                for i in range(1,5):
                    if mcube.fx <= 1 and mcube.fz >= 4:break
                    a += "dL."; mcube.dL();
                    r_fnd = mcube.findedge_r(5,4);
                a += "uR.dR.BC.dL.BA.LD.LD.BC.dR.BA.LD.LD.uL.dL."
                mcube.uR(); mcube.dR(); mcube.BC(); mcube.dL(); mcube.BA(); mcube.LD(); mcube.LD();
                mcube.BC(); mcube.dR(); mcube.BA(); mcube.LD(); mcube.LD(); mcube.uL(); mcube.dL();
            good = 0
            if mcube.cube[0][3][1] == 2 and mcube.cube[1][3][0] == 3: good += 1
            if mcube.cube[4][3][0] == 3 and mcube.cube[5][3][1] == 4: good += 1
            if mcube.cube[5][3][4] == 4 and mcube.cube[4][3][5] == 5: good += 1
            if mcube.cube[1][3][5] == 5 and mcube.cube[0][3][4] == 2: good +=1
            iter += 1
            if iter >= ITER_THRESHOLD: mcube.erval = ERR_NONDESCRIPT
    # 检查错误
        if mcube.erval: return ""
        if mcube.shorten >= SHORTEN_STRIP_SOME: a = mcube.concise(a)
        mcube.mov[step] = len(a) // 3
        s += a
  # step 10: 第三排边缘
        step += 1
        a = ""
        iter = 0
 
        good = 0
        ok=np.zeros(4,dtype=int)
        while not mcube.erval and good < 4:
            if mcube.findedge_l(4,3) == POSX: pass
            elif mcube.findedge_l(4,3) == POSZ: a += "dL."; mcube.dL();
            elif mcube.findedge_l(4,3) == NEGX: a += "dL.dL."; mcube.dL(); mcube.dL();
            elif mcube.findedge_l(4,3) == NEGZ: a += "dR."; mcube.dR();
            good = 0
            for i in range(0,4): ok[i] = 0
            if mcube.cube[0][2][1] == 2 and mcube.cube[1][2][0] == 3:
                ok[0] = 1; good += 1
            if mcube.cube[4][2][0] == 3 and mcube.cube[5][2][1] == 4:
                ok[1] = 1; good += 1
            if mcube.cube[5][2][4] == 4 and mcube.cube[4][2][5] == 5:
                ok[2] = 1; good += 1
            if mcube.cube[1][2][5] == 5 and mcube.cube[0][2][4] == 2:
                ok[3] = 1; good += 1
            if good == 1:
                a += "FC.FC.RU.RU.FA.dL.FC.RU.RU.FA.dR.FA."
                mcube.FC(); mcube.FC(); mcube.RU(); mcube.RU(); mcube.FA(); mcube.dL();
                mcube.FC(); mcube.RU(); mcube.RU(); mcube.FA(); mcube.dR(); mcube.FA();
            elif good == 2:
                if ok[3] == 1:
                    a += "dR.dR.RU.RU.BA.BA.RD.dL.RU.BA.BA.RD.dR.RD.dR.""dR.LD.LD.FC.FC.LU.dL.LD.FC.FC.LU.dR.LU.dR.dR.""dR.dR.RU.RU.BA.BA.RD.dL.RU.BA.BA.RD.dR.RD.dR."
                    mcube.dR(); mcube.dR(); mcube.RU(); mcube.RU(); mcube.BA(); mcube.BA(); mcube.RD(); mcube.dL();
                    mcube.RU(); mcube.BA(); mcube.BA(); mcube.RD(); mcube.dR(); mcube.RD(); mcube.dR();
                    mcube.dR(); mcube.LD(); mcube.LD(); mcube.FC(); mcube.FC(); mcube.LU(); mcube.dL();
                    mcube.LD(); mcube.FC(); mcube.FC(); mcube.LU(); mcube.dR(); mcube.LU(); mcube.dR(); mcube.dR();
                    mcube.dR(); mcube.dR(); mcube.RU(); mcube.RU(); mcube.BA(); mcube.BA(); mcube.RD(); mcube.dL();
                    mcube.RU(); mcube.BA(); mcube.BA(); mcube.RD(); mcube.dR(); mcube.RD(); mcube.dR();
                elif ok[2] == 1:
                    a += "dR.dR.RU.RU.BA.BA.RD.dL.RU.BA.BA.RD.dR.RD.dR."
                    mcube.dR(); mcube.dR(); mcube.RU(); mcube.RU(); mcube.BA(); mcube.BA(); mcube.RD(); mcube.dL();
                    mcube.RU(); mcube.BA(); mcube.BA(); mcube.RD(); mcube.dR(); mcube.RD(); mcube.dR();
                elif ok[0] == 1:
                    a += "dR.LD.LD.FC.FC.LU.dL.LD.FC.FC.LU.dR.LU.dR.dR."
                    mcube.dR(); mcube.LD(); mcube.LD(); mcube.FC(); mcube.FC(); mcube.LU(); mcube.dL();
                    mcube.LD(); mcube.FC(); mcube.FC(); mcube.LU(); mcube.dR(); mcube.LU(); mcube.dR(); mcube.dR();
            good = 0
            if mcube.cube[0][2][1] == 2 and mcube.cube[1][2][0] == 3: good += 1
            if mcube.cube[4][2][0] == 3 and mcube.cube[5][2][1] == 4: good += 1
            if mcube.cube[5][2][4] == 4 and mcube.cube[4][2][5] == 5: good += 1
            if mcube.cube[1][2][5] == 5 and mcube.cube[0][2][4] == 2: good += 1
            iter += 1
            if iter >= ITER_THRESHOLD: mcube.erval = ERR_NONDESCRIPT
    # check for trouble
        if mcube.erval: return ""
        if mcube.shorten >= SHORTEN_STRIP_SOME: a = mcube.concise(a)
        mcube.mov[step] = len(a) // 3
        s += a
  # step 11:边块中心
        step += 1
        a = ""
        iter = 0
    # fix
        good = 0
        ok = np.zeros(4,dtype=int)
        col=0; a_fnd=0; b_fnd=0; ax=0; bx=0; ay=0; by=0; az=0; bz=0;
        ok[0] = not mcube.findcenter_not_l(2)
        ok[1] = not mcube.findcenter_not_f(3)
        ok[2] = not mcube.findcenter_not_r(4)
        ok[3] = not mcube.findcenter_not_b(5)
        good += ok[0]
        good += ok[1]
        good += ok[2]
        good += ok[3]
        while (not mcube.erval) and good < 4:
            for i in range(1,5):
                if i<4: mark11=i+2
                if i>=4: mark11=i-2
                col = mark11
                for j in range(1,5):
                    a_fnd = mcube.findcenter_not_f(col)
                    if not a_fnd:break
                    ax = mcube.fx; ay = mcube.fy; az = mcube.fz;
                    if a_fnd == POSZ:
                        if col>2: mark12 = col-1
                        if col<=2: mark12 = col +3
                        b_fnd = not mcube.find_not_center_l(mark12)
                        if b_fnd:
                            if col < 5: mark13 = col + 1
                            if col >= 5: mark13 = col - 3
                            b_fnd = mcube.find_not_center_r(mark13)
                            if b_fnd:
                                bx = mcube.fx; by = mcube.fy; bz = mcube.fz;
                            else:
                                bx = 5; by = 2; bz = 2;
                            if bz == 2 and by == 2: pass
                            elif bz == 2 and by == 3:  a += "RD."; mcube.RD();
                            elif bz == 3 and by == 2:  a += "RU."; mcube.RU();
                            elif bz == 3 and by == 3:  a += "RU.RU."; mcube.RU(); mcube.RU();
                            if ax == 2 and ay == 2: pass
                            elif ax == 2 and ay == 3:  a += "BA."; mcube.BA();
                            elif ax == 3 and ay == 2:  a += "BC."; mcube.BC();
                            elif ax == 3 and ay == 3:  a += "BA.BA."; mcube.BA(); mcube.BA();
                            a += "BC.BC.lU.fC.lD.BC.BC.lU.fA.lD."
                            mcube.BC(); mcube.BC(); mcube.lU(); mcube.fC(); mcube.lD(); mcube.BC(); mcube.BC(); mcube.lU(); mcube.fA(); mcube.lD();
                            if ax == 2 and ay == 2: pass
                            elif ax == 2 and ay == 3:  a += "BC."; mcube.BC();
                            elif ax == 3 and ay == 2:  a += "BA."; mcube.BA();
                            elif ax == 3 and ay == 3:  a += "BC.BC."; mcube.BC(); mcube.BC();
                            if bz == 2 and by == 2: pass
                            elif bz == 2 and by == 3:  a += "RU."; mcube.RU();
                            elif bz == 3 and by == 2:  a += "RD."; mcube.RD();
                            elif bz == 3 and by == 3:  a += "RD.RD."; mcube.RD(); mcube.RD();
                            a_fnd = mcube.findcenter_r(col)
                            ax = mcube.fx; ay = mcube.fy; az = mcube.fz;
                        else:
                            bx = mcube.fx; by = mcube.fy; bz = mcube.fz;
                            if bz == 2 and by == 3: pass
                            elif bz == 2 and by == 2:  a += "LU."; mcube.LU();
                            elif bz == 3 and by == 3: a += "LD."; mcube.LD();
                            elif bz == 2 and by == 2:  a += "LD.LD."; mcube.LD(); mcube.LD();
                            if ax == 3 and ay == 3: pass
                            elif ax == 3 and ay == 2:  a += "BA."; mcube.BA();
                            elif ax == 2 and ay == 3:  a += "BC."; mcube.BC();
                            elif ax == 2 and ay == 2:  a += "BA.BA."; mcube.BA(); mcube.BA();
                            a += "BC.BC.rD.fC.rU.BC.BC.rD.fA.rU."
                            mcube.BC(); mcube.BC(); mcube.rD(); mcube.fC(); mcube.rU(); mcube.BC(); mcube.BC(); mcube.rD(); mcube.fA(); mcube.rU();
                            if ax == 3 and ay == 3: pass
                            elif ax == 3 and ay == 2:  a += "BC."; mcube.BC();
                            elif ax == 2 and ay == 3:  a += "BA."; mcube.BA();
                            elif ax == 2 and ay == 2:  a += "BC.BC."; mcube.BC(); mcube.BC();
                            if bz == 2 and by == 3: pass
                            elif bz == 2 and by == 2:  a += "LD."; mcube.LD();
                            elif bz == 3 and by == 3:  a += "LU."; mcube.LU();
                            elif bz == 2 and by == 2:  a += "LU.LU."; mcube.LU(); mcube.LU();
                            a_fnd = mcube.findcenter_l(col);
                            ax = mcube.fx; ay = mcube.fy; az = mcube.fz;
                    if a_fnd == NEGX:
                        b_fnd = mcube.find_not_center_f(col)
                        bx = mcube.fx; by = mcube.fy; bz = mcube.fz;
                        if bx == 3 and by == 3: pass
                        elif bx == 3 and by == 2:  a += "FA."; mcube.FA();
                        elif bx == 2 and by == 3:  a += "FC."; mcube.FC();
                        elif bx == 2 and by == 2:  a += "FC.FC."; mcube.FC(); mcube.FC();
                        if az == 3 and ay == 3: pass
                        elif az == 3 and ay == 2:  a += "LD."; mcube.LD();
                        elif az == 2 and ay == 3:  a += "LU."; mcube.LU();
                        elif az == 2 and ay == 2:  a += "LD.LD."; mcube.LD(); mcube.LD();
                        a += "LU.LU.bC.rU.bA.LU.LU.bC.rD.bA.";
                        mcube.LU(); mcube.LU(); mcube.bC(); mcube.rU(); mcube.bA(); mcube.LU(); mcube.LU(); mcube.bC(); mcube.rD(); mcube.bA();
                        if az == 3 and ay == 3: pass
                        elif az == 3 and ay == 2: a += "LU."; mcube.LU();
                        elif az == 2 and ay == 3:  a += "LD."; mcube.LD();
                        elif az == 2 and ay == 2:  a += "LU.LU."; mcube.LU(); mcube.LU();
                        if bx == 3 and by == 3: pass
                        elif bx == 3 and by == 2:  a += "FC."; mcube.FC();
                        elif bx == 2 and by == 3:  a += "FA."; mcube.FA();
                        elif bx == 2 and by == 2:  a += "FA.FA."; mcube.FA(); mcube.FA();
                    elif a_fnd == POSX:
                        b_fnd = mcube.find_not_center_f(col)
                        bx = mcube.fx; by = mcube.fy; bz = mcube.fz;
                        if bx == 2 and by == 2: pass
                        elif bx == 2 and by == 3:  a += "FA."; mcube.FA();
                        elif bx == 3 and by == 2:  a += "FC."; mcube.FC();
                        elif bx == 3 and by == 3:  a += "FC.FC."; mcube.FC(); mcube.FC();
                        if az == 3 and ay == 2: pass
                        elif az == 3 and ay == 3:  a += "RU."; mcube.RU();
                        elif az == 2 and ay == 2:  a += "RD."; mcube.RD();
                        elif az == 2 and ay == 3:  a += "RU.RU."; mcube.RU(); mcube.RU();
                        a += "RD.RD.bC.lD.bA.RD.RD.bC.lU.bA.";
                        mcube.RD(); mcube.RD(); mcube.bC(); mcube.lD(); mcube.bA(); mcube.RD(); mcube.RD(); mcube.bC(); mcube.lU(); mcube.bA();
                        if az == 3 and ay == 2: pass
                        elif az == 3 and ay == 3:  a += "RD."; mcube.RD();
                        elif az == 2 and ay == 2:  a += "RU."; mcube.RU();
                        elif az == 2 and ay == 3:  a += "RD.RD."; mcube.RD(); mcube.RD();
                        if bx == 2 and by == 2: pass
                        elif bx == 2 and by == 3:  a += "FC."; mcube.FC();
                        elif bx == 3 and by == 2:  a += "FA."; mcube.FA();
                        elif bx == 3 and by == 3:  a += "FA.FA."; mcube.FA(); mcube.FA();
                a += "CL."; mcube.CL();
            good = 0;
            ok[0] = not mcube.findcenter_not_l(2)
            ok[1] = not mcube.findcenter_not_f(3)
            ok[2] = not mcube.findcenter_not_r(4)
            ok[3] = not mcube.findcenter_not_b(5)
            good += ok[0]
            good += ok[1]
            good += ok[2]
            good += ok[3]
            iter += 1
            if iter >= ITER_THRESHOLD: mcube.erval = ERR_NONDESCRIPT
    # 检查错误
        if mcube.erval: return ""
        if mcube.shorten >= SHORTEN_STRIP_SOME: a = mcube.concise(a)
        mcube.mov[step] = len(a) // 3
        s += a
        if not mcube.issolved():
            mcube.erval = ERR_NONDESCRIPT
            return ""
        return s




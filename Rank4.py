from Ran4Mcube import mcube
import sys
import string
N = 4
randm = False
verbal = True
inmode = 0
thecube = mcube()
coltochar =[0,0,0,0,0,0,0]
# 在屏幕上显示魔方
def myrenderscreen(c):
    for i in range(1, N+1):
      for j in range(1, N+1): print(" ",end="")
      print(" ",end="")
      for j in range(1,N+1):print(coltochar[c.cube[j][N+1][N+1-i]],end="")
      print("\n",end="")
    for i in range(1,N+1):
      for j in range(1,N+1):print(coltochar[c.cube[0][N+1-i][N+1-j]],end="")
      print(" ",end="")
      for j in range(1,N+1):print(coltochar[c.cube[j][N+1-i][0]],end="")
      print(" ",end="")
      for j in range(1,N+1):print(coltochar[c.cube[N+1][N+1-i][j]],end="")
      print(" ",end="")
      for j in range(1,N+1):print( coltochar[c.cube[N+1-j][N+1-i][N+1]],end="")
      print("\n",end="")
    for i in range(1,N+1):
      for j in range(1,N+1): print(" ",end="")
      print(" ",end="")
      for j in range(1, N + 1):print(coltochar[c.cube[j][0][i]],end="")
      print("\n",end="")

#返回与给定字符关联的数字
def chartocol(c):
    for i in range (1,7):
      if coltochar[i] == c:
        return i
    return 0

# 在屏幕上显示解决方案
def sendsolution():
    cmd = ""
    txt=""
    txt1=''
    lin = 0
    for i in range(1,N*N+1):
      cmd += "      "
    for i in range(1,N+1):
      for j in range(1,N+1):
        cmd1=list(cmd)
        cmd1[(i-1)*N+(j-1)] = coltochar[thecube.cube[j][N+1][N+1-i]]
        cmd1[(i-1)*N+(j-1)+N*N]   = coltochar[thecube.cube[0][N+1-i][N+1-j]]
        cmd1[((i-1)*N+(j-1))+N*N*2] = coltochar[thecube.cube[j][N+1-i][0]  ]
        cmd1[((i-1)*N+(j-1))+N*N*3] = coltochar[thecube.cube[N+1][N+1-i][j] ]
        cmd1[((i-1)*N+(j-1))+N*N*4] = coltochar[thecube.cube[N+1-j][N+1-i][N+1]]
        cmd1[((i-1)*N+(j-1))+N*N*5] = coltochar[thecube.cube[j][0][i]]
        cmd=''.join(cmd1)
    if inmode == 1:
      cmd.insert(N*N*5," D:")
      cmd.insert(N*N*4," B:")
      cmd.insert(N*N*3," R:")
      cmd.insert(N*N*2," F:")
      cmd.insert(N*N  ," L:")
      cmd.insert(0    , "U:")
    myrenderscreen(thecube)
    for i in range(1,thecube.mov[0]+1):
      if verbal:
        txt = ""
        if thecube.solution[i*3-3]=='U': txt += "U"; txt1 = 'U';
        if thecube.solution[i*3-3]=='u': txt += "IU"; txt1 = 'u';#I
        if thecube.solution[i*3-3]=='d': txt += "ID"; txt1 = 'd';#I
        if thecube.solution[i*3-3]=='D': txt += "D"; txt1 = 'D';
        if thecube.solution[i*3-3]=='L': txt += "L";  txt1 = 'L';
        if thecube.solution[i*3-3]=='l': txt += "IL"; txt1 = 'l';#I
        if thecube.solution[i*3-3]=='r': txt += "IR"; txt1 = 'r';#I
        if thecube.solution[i*3-3]=='R': txt += "R"; txt1 = 'R';
        if thecube.solution[i*3-3]=='F': txt += "F"; txt1 = 'F';
        if thecube.solution[i*3-3]=='f': txt += "IF"; txt1 = 'f';#I
        if thecube.solution[i*3-3]=='b': txt += "IB"; txt1 = 'b';#I
        if thecube.solution[i*3-3]=='B': txt += "B"; txt1 = 'B';
        if thecube.solution[i*3-2]=='L':
          if txt1=='U' or txt1=='u':txt += ""
          if txt1 == 'D' or txt1 == 'd':txt += "'"
        if thecube.solution[i*3-2]== 'R':
          if txt1 == 'U' or txt1 == 'u':txt += "'"
          if txt1 == 'D' or txt1 == 'd':txt += ""
        if thecube.solution[i*3-2]== 'U':
          if txt1 == 'L' or txt1 == 'l':txt += "'"
          if txt1 == 'R' or txt1 == 'r':txt += ""
        if thecube.solution[i*3-2]== 'D':
          if txt1 == 'L' or txt1 == 'l':txt += ""
          if txt1 == 'R' or txt1 == 'r':txt += "'"
        if thecube.solution[i*3-2]== 'C':
          if txt1 == 'F' or txt1 == 'f':txt += ""
          if txt1 == 'B' or txt1 == 'b':txt += "'"
        if thecube.solution[i*3-2]== 'A':
          if txt1 == 'F' or txt1 == 'f':txt += "'"
          if txt1 == 'B' or txt1 == 'b':txt += ""
        print(txt,end="")
        lin += 1
        if lin >= 24:
          lin = 0
      else:print(thecube.solution[i*3-3]+thecube.solution[i*3-2])
    thecube.dosolution()

# 使用命令行并打印魔方
def readcommandline(cmdln):
    cmd = cmdln
    numused = 0
    isused=0
    thecube.resetcube()
    for i in range(1,7):
      coltochar[i] = '\0'
    if cmd == "random":
      coltochar[1] = 'W'; coltochar[2] = 'R'; coltochar[3] = 'B';
      coltochar[4] = 'O'; coltochar[5] = 'G'; coltochar[6] = 'Y';
      thecube.scramblecube()
      randm = true
      inmode = 1
      return 0
    if len(cmd) < N * N * 6:
      return 1
    for i in range(0, N * N * 6):
      isused = 0
      for j in range(1,7):
        if coltochar[j] == cmd[i]:
          isused = 1
      if not isused:
        numused += 1
        if numused > 6:
          return 1
        coltochar[numused] = cmd[i]
    if numused < 6:
      return 1
    for i in range(1,N+1):
      for j in range(1,N+1):
        thecube.cube[j][N+1][N+1-i]     = chartocol(cmd[((i-1)*N+(j-1))])
        thecube.cube[0][N+1-i][N+1-j]   = chartocol(cmd[((i-1)*N+(j-1))+N*N])
        thecube.cube[j][N+1-i][0]       = chartocol(cmd[((i-1)*N+(j-1))+N*N*2])
        thecube.cube[N+1][N+1-i][j]     = chartocol(cmd[((i-1)*N+(j-1))+N*N*3])
        thecube.cube[N+1-j][N+1-i][N+1] = chartocol(cmd[((i-1)*N+(j-1))+N*N*4])
        thecube.cube[j][0][i]           = chartocol(cmd[((i-1)*N+(j-1))+N*N*5])
    return 0

# 程序入口
def main():
    cmdln = "OOOOWWWWWWWWWWWWWRRRGGGGGGGGGGGGBBBBWRRRWRRRWRRROOOYBBBBBBBBBBBBGGGGOOOYOOOYOOOYRYYYRYYYRYYYRYYY"
    inin = 0
    out = 0
    inin = readcommandline(cmdln)
    if inin == 0:
      out = thecube.solvecube()
      if out == 0:
        sendsolution()
    else:
      print("500 ERROR: solver failed for the following reason:")
      print("510 ERROR: non-protocol input entered.")
    return 0

main()
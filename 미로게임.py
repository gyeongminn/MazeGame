import turtle
import random
import time

#미로 배열을 좌표로 변환시킨다
def maze_to_pos(x, y) :
    x = int(-300 + 30 * x)
    y = int(300 - 30 * y)
    return x, y

#좌표를 미로 배열로 변환시킨다
def pos_to_maze(x, y) :
    x = int((x + 300) / 30)
    y = int((y - 300) / 30 * -1)
    return x, y

#미로를 생성한다
def make_maze() :
    maze = [[1] * maze_size for _ in range(maze_size)] #미로 배열 선언
    #홀수번째 칸은 길로 만든다
    for y in range(1, maze_size, 2) :
        for x in range(1, maze_size, 2) :
            maze[y][x] = 0
    #길을 랜덤하게 오른쪽 또는 아래쪽으로 뚫는다
    for y in range(1, maze_size, 2) :
        count = 1
        for x in range(1, maze_size, 2) :
            if x == maze_size - 2 and y == maze_size - 2 : #가장자리인 경우
                continue
            elif x == maze_size - 2 : #오른쪽에 벽이 있는 경우
                maze[y + 1][x] = 0
                continue
            elif y == maze_size - 2 : #아래에 벽이 있는 경우
                maze[y][x + 1] = 0
                continue
            if random.randint(0, 1) : 
                maze[y][x + 1] = 0 #오른쪽으로 뚫기
                count += 1
            else : 
                random_index = random.randint(0, count - 1) #연속된 가로줄 중에서 랜덤하게 내려간다
                maze[y + 1][x - random_index * 2] = 0 #아래쪽으로 뚫기
                count = 1
    maze[maze_size - 1][maze_size - 2] = 2 #종료지점 설정
    return maze

#미로를 그린다
def draw_maze() :
    t.up()
    t.speed(0)
    for j in range(maze_size) :
        for i in range(maze_size) :
            if maze[j][i] == 0 : #길이면 건너뜀
                continue
            x, y = maze_to_pos(i, j)
            t.goto(x, y)
            if maze[j][i] == 1 : #벽인 경우
                t.shape(wall)
                t.stamp()
            else :
                t.shape(carrot) #출구인 경우
                t.stamp()

#늑대를 이동시킨다
def move_wolf() :
    x, y = w.pos()
    x, y = pos_to_maze(x, y)
    while True :
        #상하좌우 랜덤하게 이동한다
        n = random.randint(1, 4)
        if n == 1 :
            if (maze[y][x - 1] == 0) : 
                w.goto(maze_to_pos(x - 1, y))
                break
        elif n == 2 :
            if (maze[y][x + 1] == 0) :
                w.goto(maze_to_pos(x + 1, y))
                break
        elif n == 3 :
            if (maze[y - 1][x] == 0) :
                w.goto(maze_to_pos(x, y - 1))
                break
        else :
            if (maze[y + 1][x] == 0) :
                w.goto(maze_to_pos(x, y + 1))
                break

#늑대랑 토끼랑 마주쳤는지 확인한다
def check_pos() :
    tx, ty = t.pos()
    tx, ty = pos_to_maze(tx, ty)
    wx, wy = w.pos()
    wx, wy = pos_to_maze(wx, wy)
    if abs(tx - wx) < 2 and abs(ty - wy) < 2 : #마주친 경우
        return 1
    else :
        return 0

#성공 화면 출력
def success() :
    t.clear() #화면초기화
    t.hideturtle()
    w.hideturtle()
    s.bgcolor('orange') #노란색 배경
    t.goto(0,-50)
    t.pensize(10)
    t.color('black')
    t.write("CLEAR!", False, "center", ("맑은 고딕",100)) #중앙에 글씨쓰기
    t.goto(0,-150)
    end_time = time.time() - start_time #완료시간을 소수 4번째 자리까지 저장
    t.write("Clear Time : %.3fs" %(end_time), False, "center", ("맑은 고딕",20))

#Up키 입력 함수
def up() : 
    x, y = t.pos() #좌표를 받아 현재 위치를 계산
    x, y = pos_to_maze(x, y)
    y -= 1 
    t.goto(maze_to_pos(x, y)) #한 칸 위로
    if (maze[y][x] == 1) : #벽에 닿으면 위치 초기화
        t.goto(maze_to_pos(1, 1))
    move_wolf()
    if check_pos() :
        t.goto(maze_to_pos(1, 1))
    
#Down키 입력 함수
def down() :
    x, y = t.pos()
    x, y = pos_to_maze(x, y)
    y += 1
    t.goto(maze_to_pos(x, y))
    if (maze[y][x] == 1) :
        t.goto(maze_to_pos(1, 1))
    elif (maze[y][x] == 2) : #도착한 경우
        success()
    move_wolf()
    if check_pos() :
        t.goto(maze_to_pos(1, 1))

#Left키 입력 함수
def left() :
    x, y = t.pos()
    x, y = pos_to_maze(x, y)
    x -= 1
    t.goto(maze_to_pos(x, y))
    if (maze[y][x] == 1) :
        t.goto(maze_to_pos(1, 1))
    move_wolf()
    if check_pos() :
        t.goto(maze_to_pos(1, 1))

#Right키 입력 함수
def right() :
    x, y = t.pos()
    x, y = pos_to_maze(x, y)
    x += 1
    t.goto(maze_to_pos(x, y))
    if (maze[y][x] == 1) :
        t.goto(maze_to_pos(1, 1))
    move_wolf()
    if check_pos() :
        t.goto(maze_to_pos(1, 1))

#도움말 출력
print("""
┌──────────────────────────────────────┐
│         토끼 미로 탈출 게임          │
│                                      │
│ 미로는 랜덤하게 생성됩니다.          │
│ 방향키로 토끼를 움직일 수 있습니다.  │
│                                      │
│ 미로 출구 주변에 늑대가 있습니다.    │
│ 벽에 닿거나, 늑대와 마주치게 되면    │
│ 시작 위치로 돌아갑니다.              │
│                                      │
│ 로딩이 끝나면 게임이 시작됩니다.     │
│ 토끼가 미로를 탈출하도록 도와주세요! │
└──────────────────────────────────────┘
""")

#shape 설정
t = turtle.Turtle()
w = turtle.Turtle()
s = turtle.Screen()
wall = "wall.gif"
wolf = "wolf.gif"
rabbit = "rabbit.gif"
carrot = "carrot.gif"
s.addshape(wall)
s.addshape(wolf)
s.addshape(rabbit)
s.addshape(carrot)

#게임 설정
maze_size = 21
maze = make_maze()
now_x = now_y = 1

#게임 시작
draw_maze()
t.shape(rabbit)
t.goto(maze_to_pos(1, 1))
w.up()
w.speed(0)
w.shape(wolf)
w.goto(maze_to_pos(19, 19))
start_time = time.time()

#키 입력받기
s.onkeypress(up,"Up")
s.onkeypress(down,"Down")
s.onkeypress(left,"Left")
s.onkeypress(right,"Right")
s.listen()
s.mainloop()
import cv2
import kociemba
import RPi.GPIO as GPIO
import time

# 设置 BCM 编号方式
GPIO.setmode(GPIO.BCM)

# 定义舵机信号引脚 实际引脚：12,16,18,22
u1 = 18  # 物理对应12
u2 = 23  # 物理对应16
d1 = 19  # 物理对应35
d2 = 25  # 物理对应22
# 减速电机
pwm = 5  # 物理对应29，电机输出pwm
in1 = 17  # 物理对应11，控制电机方向
in2 = 22  # 物理对应15，控制电机方向
# 超声波传感器
en = 6  # 物理对应31
data_in = 13  # 物理对应33
# 引脚初始化为低电平
GPIO.setup(en, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(data_in, GPIO.IN)
# 设置舵机信号引脚为输出模式
GPIO.setup(u1, GPIO.OUT)
GPIO.setup(u2, GPIO.OUT)
GPIO.setup(d1, GPIO.OUT)
GPIO.setup(d2, GPIO.OUT)
# 设置电机引脚为输出模式
GPIO.setup(pwm, GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)

# 创建 PWM 实例，频率设为 50Hz
pwm_motor = GPIO.PWM(pwm, 1000)
pwm_u1 = GPIO.PWM(u1, 50)
pwm_u2 = GPIO.PWM(u2, 50)
pwm_d1 = GPIO.PWM(d1, 50)
pwm_d2 = GPIO.PWM(d2, 50)
# 启动 PWM
pwm_motor.start(0)
pwm_u1.start(0)
pwm_u2.start(0)
pwm_d1.start(0)
pwm_d2.start(0)
# 初始化电机引脚为低电平
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)

# 说明：魔方以URFDLB的顺序排列
# 例如：RRBBUFBFB RLRRRFRDD URUBFBBRF LUDUDFLLF FLLLLDFBD DDUUBDLUU
# solution="U2 B R' F' D B R L' D' R' F' R2 U' B2 R2 U' D' F2 R2 U' B2"
# 这里的color[i]指代第i+1个方向的面，我们指定初始u=1,r=2,f=3,d=4,l=5,b=6


color = {'U': 1, 'R': 2, 'F': 3, 'D': 4, 'L': 5, 'B': 6}  # 用于记录当前各面的状态
color_const = {'U': 1, 'R': 2, 'F': 3, 'D': 4, 'L': 5, 'B': 6}  # 初始状态
angle_up = 0  # 假设上方舵机初始角度为0


def checkdist():
    '''
    超声波传感器函数
    该传感器的原理是：给传感器一个高电平启动信号，传感器发送一个超声波，在接收到超声波以前保持输出高电平，
    计算高电平持续时间即可算出高度
    :return: 当前高度
    '''
    # 发出触发信号
    GPIO.output(en, GPIO.HIGH)
    # 保持10us以上（我选择15us）
    time.sleep(0.000015)
    GPIO.output(en, GPIO.LOW)
    while not GPIO.input(data_in):
        pass
    # 发现高电平时开时计时
    t1 = time.time()
    while GPIO.input(data_in):
        pass
    # 高电平结束停止计时
    t2 = time.time()
    # 返回距离，单位为米
    # print('t2-t1: {0}'.format(t2-t1))
    return (t2 - t1) * 340 / 2


def motor(dir, distance):
    '''
    控制减速电机的函数，可以移动到指定的高度，在我们项目中，只有四个指定的高度：distance为[24.7， 20.4， 20.5， 7]
    :param dir: 方向，其实没必要指定方向，毕竟是移动到指定高度
    :param distance: 移动的高度
    :return: 无
    '''
    # 设置方向
    if dir == 'u':
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        distance = distance + 0.3
    elif dir == 'd':
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
        distance = distance - 0.3
    # 设置速度，设置占空比为100%
    pwm_motor.ChangeDutyCycle(100)
    while True:
        time.sleep(0.15)
        if distance == 25.0:  # 最高点，超声波传感器不灵敏，使用时间控制
            time.sleep(distance - checkdist() * 100 - 0.3)
            break
        else:  # 其余使用超声波传感器控制
            if distance - 0.3 <= checkdist() * 100 <= distance + 0.3:
                break
    if dir == 'u':
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
    elif dir == 'd':
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
    time.sleep(0.05)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    pwm_motor.ChangeDutyCycle(0)  # 设置占空比为0,停止pwm输出


# 舵机旋转的函数,angle:角度,engine_num：控制的舵机序号，该函数中已经预留了舵机反应时间 time.sleep(0.5)
def steering_engine(angle, engine_num, turn_time=2.5):
    '''
    :param angle: 舵机旋转的角度
    :param engine_num: 转动的舵机序号
    :param turn_time: 转动完成后，舵机停留时间
    :return: 无
    '''
    try:
        if engine_num == 1:  # 上爪旋转
            angle = (1 / 27) * angle + 2.5  # 将角度转换为占空比
            pwm_u1.ChangeDutyCycle(angle)
            time.sleep(turn_time + abs(angle - angle_up) / 90)
            return 1
        elif engine_num == 2:  # 上爪夹持
            angle = (1 / 18) * angle + 2.5
            pwm_u2.ChangeDutyCycle(angle)
            time.sleep(turn_time)
            return 1
        elif engine_num == 3:  # 下爪旋转
            angle = (1 / 18) * angle + 2.5
            pwm_d1.ChangeDutyCycle(angle)
            time.sleep(turn_time)
            return 1
        elif engine_num == 4:  # 下爪夹持
            angle = (1 / 18) * angle + 2.5
            pwm_d2.ChangeDutyCycle(angle)
            time.sleep(turn_time)
            return 1

    except KeyboardInterrupt:
        return -1


def color_identify(sz):
    '''
    调用摄像头识别魔方并返回颜色
    :param sz: 魔方阶数
    :return: 一个面的颜色，一个长sz^sz的字符串
    '''
    global sz_flag
    order_sz = [80, 70, 45]  # 魔方中心坐标之间的差的最大值（用于排序和计算重复）
    cpare_sz = [[20000, 40000, 200, 500, 90, 450], [2000, 30000, 210, 480, 100, 370],
                [4000, 12000, 150, 520, 60, 420]]  # 用于筛选矩形时的条件，分别是w * h_min, w * h_max，x_min, x_max, y_min, y_max
    center_point3 = [(270, 140), (370, 140), (465, 140), (270, 235), (370, 235), (465, 235), (270, 325), (370, 325),
                     (465, 325)]  # 如果坐标点数量不对，直接取值，这里只给出了三阶，其它阶数测量一下即可
    radius3 = 55  # 识别到的色块中心
    # 初始化摄像头

    camera = cv2.VideoCapture(0)
    while True:
        # 读取摄像头画面
        ret, frame = camera.read()
        # 显示画面
        cv2.imshow("Camera", frame)
        # 监听键盘输入
        key = cv2.waitKey(1)
        if key == ord('c'):  # 如果按下 'c'
            image = frame
            break

    # 关闭摄像头和窗口
    camera.release()
    cv2.destroyAllWindows()

    # 读取原始图像并转换为灰度图像
    # image = cv2.imread("C:\\Users\\mkm\\Desktop\\mofang3-3.jpg")
    imgContour = image.copy()
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur_image = cv2.GaussianBlur(gray_image, (3, 3), 1)  # 高斯模糊  (3, 3), 1 ：越大越模糊
    # 边缘检测
    edges = cv2.Canny(blur_image, 14, 19)  # 60，80：越小边缘检测效果越强
    # 加粗边缘
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # (3,3)影响膨胀效果
    dilated_edges = cv2.dilate(edges, kernel)
    # 将加粗后的边缘图像与原始图像叠7
    result = cv2.addWeighted(image, 0.7, cv2.cvtColor(dilated_edges, cv2.COLOR_GRAY2BGR), 0.65, 55)  # 0.7，叠加所占比例，50：亮度
    result_contour = result.copy()  # 复制副本

    result_gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)  # 获得灰度图像
    result_canny = cv2.Canny(result_gray, 17, 23)  # Canny算子边缘检测

    # 查找轮廓
    contours, _ = cv2.findContours(result_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    candidates = []
    # 遍历所有轮廓
    i = 0
    center = []
    unique_points = [(0, 0)]
    for contour in contours:
        # 进行多边形逼近
        area = cv2.contourArea(contour)  # 计算轮廓内区域的面积
        cv2.drawContours(result_contour, contour, -1, (255, 0, 0), 4)  # 绘制轮廓线
        epsilon = 0.01 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        x, y, w, h = cv2.boundingRect(contour)  # 获取坐标值和宽度、高度

        # 去掉边缘轮廓
        if cpare_sz[sz - 2][0] < w * h < cpare_sz[sz - 2][1] and cpare_sz[sz - 2][2] < x + w / 2 < cpare_sz[sz - 2][3] \
                and cpare_sz[sz - 2][4] < y + h / 2 < cpare_sz[sz - 2][5]:  # 这里的限制条件取决于摄像头识别到的图像
            M = cv2.moments(contour)  # 用于计算图像或形状的矩。
            if M["m00"]:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                cX = None
                cY = None

            # 去掉重复轮廓
            flag = 0
            for unique_point in unique_points:
                if abs(x + w / 2 - unique_point[0]) < order_sz[sz - 2] and abs(y + h / 2 - unique_point[1]) < order_sz[
                    sz - 2]:  # 去除重复点
                    flag = 1
                    break
            if flag == 0:
                unique_points.append((x + w / 2, y + h / 2))
                tmp = {'index': i, 'cx': cX, 'cy': cY, 'contour': contour}
                center.append(tmp)

                corner_num = len(approx)  # 轮廓角点的数量
                i = i + 1
                print(
                    "序号：{5}  面积：{0}  角点: {1}  area:{2} 坐标：({3},{4})".format(w * h, corner_num, area, x + w / 2,
                                                                                    y + h / 2, i))
                # 绘制多边形
                str = f"{w * h}"
                cv2.drawContours(result_contour, [approx], -1, (0, 255, 0), 2)
                cv2.putText(result_contour, str, (x + (w // 2), y + (h // 2)), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 0, 0),
                            1)  # 绘制文字

    center.sort(key=lambda k: (k.get('cy', 0)))
    row = []
    for i in range(sz):
        row.append(center[sz * i:sz * (i + 1)])
        row[i].sort(key=lambda k: (k.get('cx', 0)))

    center.clear()
    for i in range(sz):
        center = center + row[i]

    for component in center:
        candidates.append(component.get('contour'))

    '''cv2.drawContours(imgobj, candidates, -1, (0, 0, 255), 3)'''
    h = []
    s = []
    v = []
    name_color2 = []
    name_color = "None"
    hsv_value2 = [0, 0, 0]
    # 4、原图白色中心点
    L = len(candidates)  # contours轮廓数据是数组，因此用len()测数组长度，为了循环画点使用
    sz_flag = 0
    if L != sz * sz:
        sz_flag = 1  # 意味着识别到的色块不够，那就直接从固定位置取值（其实这种方法可能更好）
        L = sz * sz
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # 将图片转为hsv
    for i in range(L):
        (x, y) = center_point3[i]
        radius = radius3
        '''
        if sz_flag == 1:
            (x, y) = center_point3[i]
            radius = radius3
        else:
            cnt = candidates[i]  # cnt表示第i个白色快的轮廓信息
            (x, y), radius = cv2.minEnclosingCircle(cnt)  # 得到白色块外接圆的圆心坐标和半径
        '''
        # center[i] = (int(x), int(y))  # 画center圆心时。x,y必须是整数
        a = int(radius / 2)
        cv2.rectangle(image, (int(x) + a, int(y) + a), (int(x) - a, int(y) - a), (0, 0, 255), 2)
        for j in range(3):
            hsv_value = hsv[int(y) - j + 1, int(x) - j + 1]
            hsv_value2 = hsv_value + hsv_value2
        hsv_value3 = hsv_value2 / 3
        h.append(hsv_value3[0])  # 将hsv值的第一个元素添加到h列表中
        s.append(hsv_value3[1])  # 将hsv值的第二个元素添加到s列表中
        v.append(hsv_value3[2])  # 将hsv值的第三个元素添加到v列表中
        hsv_value2 = [0, 0, 0]

    for i in range(L):
        if 0 <= h[i] <= 180 and 0 <= s[i] <= 95 and 30 <= v[i] <= 228:
            name_color = "U"
        elif (h[i] <= 1 or 156 <= h[i] <= 180) and 43 <= s[i] <= 255 and 30 <= v[i] <= 255:
            name_color = "F"
        elif 0 <= h[i] <= 25 and 43 <= s[i] <= 255 and 30 <= v[i] <= 255:
            name_color = "B"
        elif 26 <= h[i] <= 44 and 43 <= s[i] <= 255 and 30 <= v[i] <= 255:
            name_color = "D"
        elif 45 <= h[i] <= 85 and 43 <= s[i] <= 255 and 30 <= v[i] <= 255:
            name_color = "L"
        elif 100 <= h[i] <= 134 and 43 <= s[i] <= 255 and 30 <= v[i] <= 255:
            name_color = "R"
        else:
            print("问题： h:{0}   s:{1}   v:{2}".format(int(h[i]), int(s[i]), int(v[i])))
        name_color2.append(name_color)
        imgobj2 = cv2.circle(image, center_point3[i], 3, (0, 0, 255), 5)  # 传入圆心信息，并画在原图上
        print("h:{0}   s:{1}   v:{2}  颜色：{3}".format(int(h[i]), int(s[i]), int(v[i]), name_color))

    # 显示结果图像
    cv2.imshow("image", image)
    cv2.imshow("result_contour", result_contour)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(name_color2)
    return name_color2



def color_change(situation):
    '''
    改变数组指向函数，color字典中使用字母代表方向，数字代表颜色，初始：color = {'U': 1, 'R': 2, 'F': 3, 'D': 4, 'L': 5, 'B': 6}
    例如'U'=2时代表绿色中心块在正上方
    :param situation: 执行的操作，根据该操作改变color字典
    :return: 无
    '''
    global color
    temp = color.copy()  # 保存原来的字典
    if situation == 'total_u90':  # u90,

        color['R'] = temp['B']
        color['F'] = temp['R']
        color['L'] = temp['F']
        color['B'] = temp['L']
    elif situation == 'total_u180':  # u180
        color['R'] = temp['L']
        color['F'] = temp['B']
        color['L'] = temp['R']
        color['B'] = temp['F']
    elif situation == 'total_u-90':  # u-90
        color['B'] = temp['R']
        color['R'] = temp['F']
        color['F'] = temp['L']
        color['L'] = temp['B']
    elif situation == 'total_d148.0':  # d90
        color['B'] = temp['U']
        color['U'] = temp['F']
        color['F'] = temp['D']
        color['D'] = temp['B']
    elif situation == 'total_d6.0':  # d-90
        color['U'] = temp['B']
        color['B'] = temp['D']
        color['D'] = temp['F']
        color['F'] = temp['U']
    print(color)



def turn(turn_posi, turn_angle, situ='total'):
    '''
    控制魔方旋转的函数
    除了测试函数外，只有该函数可以调用steering_engine()
    如果要写得更正式，只能通过调用该函数来旋转魔方
    :param turn_posi: turn_posi可以是u和d
    :param turn_angle: turn_angle可以为90，180，-90
    :param situ: 记录是旋转魔方的一个面还是整个旋转魔方，如果整个旋转魔方就要调用color_change()函数
    :return: 无
    '''
    global angle_up
    temp_angle = turn_angle
    if turn_posi == 'u':
        turn_angle = (turn_angle + angle_up + 360) % 360  # 错误的情况只可能是  0+-90, 180+180, 270+90, 270+180  这四种
        steering_engine(turn_angle, 1)  # 控制舵机旋转
        angle_up = turn_angle
    elif turn_posi == 'd':
        turn_angle = turn_angle * 71 / 90 * (-1)
        turn_angle = (turn_angle + 77 + 360) % 360  # 下方舵机每次旋转之后都会归位
        steering_engine(turn_angle, 3)  # 控制舵机旋转
        temp_angle = turn_angle
    # 接下来对数组进行赋值
    situ = situ + '_' + str(turn_posi) + str(temp_angle)
    print(situ)
    if 'total' in situ:
        color_change(situ)



def turn_to_up(clor_num):
    '''
    将指定面旋转到上方的函数，这个函数假定从上方夹持住一层的位置开始操作
    :param clor_num: 需要朝上的面当前所在的位置
    :return:
    '''
    # 1-1，不动
    if clor_num == 'U':
        pass

    # 2-1，夹子夹紧,u90,夹子松开,丝杆下,d-90,丝杆上
    elif clor_num == 'R':
        motor('u', 24.7)  # 丝杆上去，回到初始全部被包住位置
        u_turn(90)
        motor('d', 10.2)  # 从魔方整个被包住到下方夹子夹子的位置
        d_turn(-90)
        motor('u', 21.2)

    # 3-1,丝杆下，d-90,丝杆上
    elif clor_num == 'F':
        motor('d', 10.2)  # 从魔方整个被包住到下方夹子夹子的位置，步进电机转动2000
        d_turn(-90)
        motor('u', 21.2)  # 丝杆上去

    # 6-1,丝杆下,d90,d90,丝杆上
    elif clor_num == 'D':
        motor('d', 10.2)  # 从魔方整个被包住到下方夹子夹子的位置，步进电机转动2000
        d_turn(-90)
        d_turn(-90)
        motor('u', 21.2)  # 丝杆上去

    # 4-1,u-90,丝杆下,d-90,丝杆上
    elif clor_num == 'L':
        motor('u', 24.7)  # 丝杆上去，回到初始全部被包住位置
        u_turn(90)
        motor('d', 10.2)  # 从魔方整个被包住到下方夹子夹子的位置，步进电机转动2000
        d_turn(90)
        motor('u', 21.2)  # 丝杆上去

    # 5-1,丝杆下,d90,丝杆上
    elif clor_num == 'B':
        motor('d', 10.2)  # 从魔方整个被包住到下方夹子夹子的位置，步进电机转动2000
        d_turn(90)
        motor('u', 21.2)  # 丝杆上去



def d_turn(turn_angle):
    '''
    下方旋转动作
    d2夹子夹紧，丝杆下降，u1可以自由旋转，d1旋转turn_angle，丝杆上升，d2夹子松开，d1恢复水平
    :param turn_angle: 旋转角度
    :return: 无
    '''
    steering_engine(95, 4)  # d2夹子夹紧
    motor('d', 7)  # 丝杆下降，夹子可以自由旋转
    turn('d', turn_angle, 'total')  # d1旋转turn_angle: 90,-90，带着魔方一起旋转
    motor('u', 10.3)  # 丝杆上升
    steering_engine(57, 4)  # d2夹子松开
    turn('d', 0, 'd_empty')  # d1恢复水平,但是魔方没有旋转



def u_turn(turn_angle, situ='total'):
    '''
    上方旋转动作
    u2夹子夹紧，u1旋转turn_angle，u2夹子松开
    :param turn_angle: 旋转角度
    :param situ: 是否整个旋转魔方
    :return: 无
    '''
    steering_engine(60, 2)  # u2夹子夹紧
    turn('u', turn_angle, situ)  # turn_angle:90,-90
    steering_engine(110, 2)  # u2夹子松开



def get_init_color(sz):
    '''
    获取初始色块函数，只执行一次
    该代码使用了steering_engine()函数，从逻辑上来说不够好，封装性不好
    :param sz: 魔方阶数
    :return: 魔方六个面的色块，为一个长6*sz*sz的字符串
    '''
    tp = []
    cnt_temp = 0
    # 开始获取每个面的色块
    steering_engine(60, 4)  # d2夹子松开
    steering_engine(7, 3)  # d1 竖直
    tp.append(color_identify(sz))  # 得到f
    # time.sleep(3)

    steering_engine(95, 4)  # d2 catch
    motor('d', 7)
    steering_engine(150, 3)  # d1 turn
    motor('u', 10.2)
    steering_engine(55, 4)  # d2 lose
    tp.append(color_identify(sz))  # 得到b
    # time.sleep(3)
    steering_engine(75, 3)  # d1 恢复水平

    motor('u', 24.7)  # 丝杆上去,爪子抓住全部魔方
    u_turn(90)
    motor('d', 10.2)  # 丝杆下去
    steering_engine(0, 1)  # u1恢复原始状态
    for _ in range(4):
        steering_engine(60, 4)  # d2夹子松开
        steering_engine(7, 3)  # d1 竖直
        tp.append(color_identify(sz))  # 得到r,d,l,u
        # time.sleep(3)
        steering_engine(95, 4)
        motor('d', 7)
        steering_engine(75, 3)
        motor('u', 10.2)

    steering_engine(60, 4)  # d2夹子松开
    print(tp)
    # 因为魔方旋转之后左上角第一个色块改变了，所以需要手动调整成原来的色块
    state_f = ''
    state_r = ''
    state_b = ''
    state_l = ''
    for i in range(9):
        state_f = state_f + tp[0][i]
        state_b = state_b + tp[1][8 - i]
        state_r = state_r + tp[2][8 - i]
        state_l = state_l + tp[4][i]
    state_u = tp[3][6] + tp[3][3] + tp[3][0] \
              + tp[3][7] + tp[3][4] + tp[3][1] \
              + tp[3][8] + tp[3][5] + tp[3][2]
    state_d = tp[5][2] + tp[5][5] + tp[5][8] \
              + tp[5][1] + tp[5][4] + tp[5][7] \
              + tp[5][0] + tp[5][3] + tp[5][6]
    print(state_u)
    print(state_r)
    print(state_f)
    print(state_d)
    print(state_l)
    print(state_b)
    cube_state1 = state_u + state_r + state_f + state_d + state_l + state_b
    print(cube_state1)

    global angle_up
    angle_up = 0
    steering_engine(0, 1)
    motor('u', 21.2)  # 丝杆上去,爪子抓住魔方一层
    return cube_state1


def init():
    '''
    将舵机的角度初始化
    :return:
    '''
    steering_engine(110, 2)  # u2夹子，60夹紧，110松开
    steering_engine(10, 1)  # u1 0度刚好
    steering_engine(60, 4)  # d2夹子夹紧，65等于松开，95等于夹紧
    steering_engine(75, 3)  # d1 75等于90，取值从0到180


def get_angle():
    '''
    测试函数1，输入一个角度，使指定舵机旋转
    :return: 无
    '''
    while True:
        angle = int(input('请输入角度:'))
        engine_num = int(input('请输入舵机序号'))
        steering_engine(angle, engine_num)


def get_key(val):
    '''
    根据字典中的值获取字典的键
    :param val: 输入的值
    :return: 字典的键
    '''
    for key, value in color.items():
        if val == value:
            return key

    return "There is no such Key"


def test_func1():
    '''
    测试函数1，魔方下方旋转，随后上方旋转
    :return: 
    '''
    # motor('d', 10.2)
    # get_angle()
    print('---------------这里是开始的地方--------------')
    d_turn(90)
    time.sleep(2)
    motor('u', 21.2)
    u_turn(90, 'total')
    time.sleep(2)
    while True:
        pass



def test_func2():
    '''
    测试函数2，魔方获取初始颜色动作演示
    :return: 无
    '''
    print('---------------这里是开始的地方--------------')
    sz = 3
    cube_state = get_init_color(sz)
    if len(cube_state) != sz * sz * 6:
        print("错误")
    try:
        # 调用kociemba.solve()函数来还原魔方
        solu = kociemba.solve(cube_state)
        print("解决方案:", solu)
    except kociemba.Error as e:
        print("出现错误:", e)
    print("完成！")
    return solu
    # while True:
    #    pass


def test_func3(sz):
    '''
    测试函数3，调用摄像头获取颜色演示
    :param sz: 魔方阶数
    :return: 无
    '''
    print('---------------这里是开始的地方--------------')
    steering_engine(7, 3)  # d1 75等于90，取值从0到180
    while True:
        print(color_identify(sz))


def test_func4():
    '''
    测试函数4，四阶魔方动作演示
    :return: 
    '''
    # start from dowm
    for _ in range(2):
        d_turn(90)
        motor('u', 20.2)
        u_turn(90)
        motor('u', 24.7)
        u_turn(90)
        motor('d', 10)
        d_turn(90)
        motor('u', 21.2)
        u_turn(90)
        motor('d', 20.2)
        u_turn(-90)
        motor('u', 24.7)
        u_turn(180)
        motor('d', 10)


def test_func5():
    '''
    测试函数5，二阶魔方动作演示
    :return: 
    '''
    # start from dowm
    for _ in range(2):
        d_turn(90)
        motor('u', 22)
        u_turn(90)
        motor('u', 24.7)
        u_turn(90)
        motor('d', 10.3)
        d_turn(90)
        motor('u', 22)
        u_turn(90)
        motor('u', 24.7)
        u_turn(180)
        motor('d', 10.3)


# 从夹住一层开始
def restore(solu):
    '''
    还原函数，根据solu调用各个函数旋转魔方
    :param solu: 根据算法得到的操作步骤
    :return: 无
    '''
    global color
    color = {'U': 4, 'R': 3, 'F': 2, 'D': 1, 'L': 6, 'B': 5}
    print(color)

    solution_steps = solu.split(" ")
    for i in solution_steps:

        print('下一步操作： ' + i + '  当前u1的角度是: ' + str(angle_up) + '   各面颜色：' + str(color))
        turn_to_up(get_key(color_const[i[0]]))  # 使得指定面回到上面
        if len(i) == 2:  # '或者2
            if i[1] == "'":
                u_turn(-90, '1f')
            elif i[1] == '2':
                u_turn(180, '1f')
        else:
            u_turn(90, '1f')


print("--------------------主函数开始的地方----------------------")

init()
size = 3
solution = "F' R B2 U2 F2 D F D2 F' L U B2 U2 L2 D L2 F2 R2 B2 U2"

# test_func1()
# solution = test_func2()
# test_func3(size)
# test_func4()
# test_func5()

# restore(solution)

print("完成！")

# 停止 PWM
pwm_motor.stop()
pwm_u1.stop()
pwm_d1.stop()
pwm_u2.stop()
pwm_d2.stop()
# 清理GPIO引脚设置
GPIO.cleanup()
# 更改时间：10.28，18:15

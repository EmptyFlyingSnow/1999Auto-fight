import cv2 as cv
#import lib.api as api
from cards.aname import card_reflect
import os

class Turn:
    buff: int = 0
    debuff: int = 0
    count: int = 0
    heal: int = 0
    data:list = []
    card: list = []
    team: list = []

t = Turn()
#t.team = ['Apple','Sonetto','Matilda','Bkornblume']
#X，未锈铠，柏林以东还有兔毛手袋
t.team = ['Lilya','Centurion','Sotheby']
def find_team():
    pass

data = {
    'x': 0,
    'y': 0
}

imgname='screenshot.png'
#ip='127.0.0.1:5555'#此为蓝叠5adb地址
ip="127.0.0.1:16384"#此为mumu地址

def init(ip="127.0.0.1:5555",imgname='screenshot.png'):#确定模拟器分辨率
    try:
        get_screen_shot(ip)
    except:
        pass
        print("模拟器图像获取失败")
    img = cv.imread(imgname)
    height, width, dep = img.shape
    data['y'] = height
    data['x'] = width
init(ip)
#init()

flx=(437,622, 807, 992, 1177, 1362, 1547, 1732)
#手牌默认x坐标

def get_screen_shot(ip="127.0.0.1:5555",imgname='screenshot.png'):#获取模拟器截图
    bel=True
    try:
        a=os.system("adb connect {}".format(ip))
        if a:
            bel=False
            print('截图失败')
            
    except:
        print('截图失败')
    Path = os.getcwd().replace("\\", '/')
    PATH='/'.join(Path.split("/"))
    os.system("adb shell screencap /sdcard/screenshot.png")
    """adb shell screencap /sdcard/screenshot.png: 这个命令在安卓设备上执行屏幕截图，并将截图保存在/sdcard/screenshot.png路径下。这个命令通过adb shell调用执行，在设备的shell环境中运行。"""
    os.system(f"adb pull /sdcard/screenshot.png {PATH}\screenshot.png")
    """adb pull /sdcard/screenshot.png {Path}\screenshot.png: 这个命令用于将安卓设备上的文件（这里是截图）复制到本地路径。adb pull命令将设备上的文件复制到本地电脑，/sdcard/screenshot.png是设备上截图的路径，{Path}\screenshot.png是将截图复制到本地时的保存路径。"""
    ans = os.system("adb shell rm /sdcard/screenshot.png")
    """adb shell rm /sdcard/screenshot.png: 这个命令在安卓设备上删除之前保存的截图文件。它通过adb shell调用执行，在设备的shell环境中运行，将screenshot.png文件从设备的/sdcard/路径下删除。"""
    #return PATH
    return bel

def calculate(image1, image2):
    # 灰度直方图算法
    # 计算单通道的直方图的相似值
    hist1 = cv.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv.calcHist([image2], [0], None, [256], [0.0, 255.0])
    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + \
                (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    return degree


def similar(image1, image2, size=(160, 210)):#计算图片相似度
    if image1.size !=  0:
        cv.imwrite(f'image1.png',image1)
    else:
        print(image1.size)
    if image2.size !=  0:
        cv.imwrite(f'image2.png',image2)
    
    image1 = cv.resize(image1, size)
    image2 = cv.resize(image2, size)
    
    sub_image1 = cv.split(image1)
    sub_image2 = cv.split(image2)
    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += calculate(im1, im2)
    sub_data = sub_data / 3
    return sub_data

def search_star(upper_left,imgname='screenshot.png'):#获取卡牌星级
    
    img = cv.imread(imgname)#读入图片
    height=int(197*data['y']/1080)
    width=int(165*data['x']/1920)
    img3 = img[upper_left[1]-30:upper_left[1],upper_left[0]:upper_left[0] + width]
    
    height1, width1, dep1 = img3.shape
    s=0
    a=img3[int(height1/2)][52]
    b=img3[int(height1/2)][96]
    c=img3[int(height1/2)][120]
    if 65<=a[0]<=67 and 111<=a[1]<=112 and 243<=a[2]<=254:
        s=1
    if 65<=b[0]<=67 and 111<=b[1]<=112 and 243<=b[2]<=254:
        s=2
    if 65<=c[0]<=67 and 111<=c[1]<=112 and 243<=c[2]<=254:
        s=3
    return s


def find_card(imgname='screenshot.png'):#获取手牌截图
    
    lx=[]
    for i in flx:
        lx.append(int(i*data['x']/1920))
    y=int(822*data['y']/1080)
    img = cv.imread(imgname)#读入图片
    height=int(197*data['y']/1080)
    width=int(165*data['x']/1920)
    cards=[]
    for i in range(8):
        upper_left = (lx[i], y)
        imgi=img[upper_left[1]:upper_left[1]+height,upper_left[0]:upper_left[0]+width]
        #切分寻找卡牌截图
        a=(imgi,search_star(upper_left))
        cards.append(a)#加入卡牌截图和星级
    return cards
        
def search_cards(character: list,imgname='screenshot.png'):#寻找卡牌
    i=0
    while i<=10:
        try:
            i+=1
            get_screen_shot(ip)
            break
        except:
            pass
            print("截图获取失败")
    img = cv.imread(imgname)#读入屏幕截图
    characters = []
    for chars in character:#循环遍历传入的字符串，据调用为t.team
        characters.append(f'{chars}1')
        characters.append(f'{chars}2')#角色卡牌命名规则为：角色名称+123
        characters.append(f'{chars}3')#应该为一个角色的三个技能
    characters.append('None')
    cardshow=[]
    for i in characters:#读入所有登场角色的卡牌
        #print(i)
        a=cv.imread(f'carda/{i}.png')
        if type(a) != 'NoneType':
            cardshow.append((cv.imread(f'carda/{i}.png'),i))
        else:
            print('类型错误1')
    cards=find_card()
    cardlist=[]
    for i in range(8):
        best=0
        card=[]
        for j in cardshow[:-1]:
            a=similar(cards[i][0],j[0])
            if a > best and a>0.5:
                best=a
                card=(j[1],cards[i][1])#卡牌名称和星级
            #大招的星级识别
        if best != 0:
            cardlist.append(card)#加入手牌列表
    #print('手牌：',cardlist)
    return cardlist

#print(search_cards(t.team))







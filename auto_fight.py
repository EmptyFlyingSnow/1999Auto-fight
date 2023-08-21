from findcard import *
from message import *
import time
import random
cardlist=[]
lis=[('Sotheby1', 1), ('Lilya2', 1), ('Lilya1', 1), ('Centurion2', 1), ('Sotheby2', 1), ('Centurion1', 1), ('Sotheby1', 1)]
lis=[('Sotheby1', 1), ('Lilya1', 1), ('Sotheby1', 1), ('Centurion2', 1), ('Sotheby2', 1), ('Centurion1', 1), ('Lilya1', 1)]
lis=[('Sotheby1', 1), ('Lilya1', 1), ('Sotheby1', 1), ('Centurion2', 1), ('Sotheby2', 1), ('Lilya1', 1), ('Centurion1', 1)]
temp=lis.pop(1)

#自动战斗
test=[['a',1],['a',2],['a',1],['a',1],['b',2]]
#测试用序列

def 伤害计算(card):
    if card[0][-1]=='3':
        return 大招伤害计算(card)
    else:
        summa=大招伤害计算(card)/5
        a=card_reflect[card[0]][card[1]]
        summ=a[0]*a[1]
        summ+=summa
        return summ

def 大招伤害计算(cardname):
    name=cardname[0][:-1]+'3'
    card=card_reflect[name][1]
    summ=card[0]*card[1]
    return summ

def 升星伤害(cardname):
    card1=cardname
    card2=(cardname[0],cardname[1]+1)
    a=伤害计算(card1)
    b=伤害计算(card2)
    summ=b-a
    return summ

def is_double(lists,summ,time):#判断合卡升星操作
    #这个函数在我的测试中经受住了考验，但我总是感觉逻辑上应该是有bug的，
    #在某些特殊序列的合卡操作下，我认为这个函数可能无法完全完成合卡判断
    #此失误可能会对出牌选择产生影响，但总体而言应该不会彻底妨碍战斗的顺利经行
    for i in range(len(lists)-1):
        if i>=(len(lists)-1):
            continue
        if lists[i][0]==lists[i+1][0] and lists[i][1]==lists[i+1][1] and lists[i][1]<3:
            
            lists.pop(i)
            
            summ+=(大招伤害计算(lists[i])/5+升星伤害(lists[i]))
            lists[i]=(lists[i][0],lists[i][1]+1)
            time+=1
            lists,summ,time=is_double(lists,summ,time)
    return lists,summ,time

summ=0
wait=0

def copy(lists):
    lis=[]
    for i in lists:
        lis.append(i)
    return lis

def gettimes(times=3):#剩余行动点
    return times
"""
def movecard(lis,temp,sec):
    best=0
    number=0
    #print(len(lis))
    for i in range(len(lis)):
        summ=0
        wait=0
        #a=[temp]
        
        lists=lis[:i]+[temp]+lis[i:]
        #print(lis,temp)
        #print(lists)
        lists,summ,wait=is_double(lists,summ,wait)
        if summ>best:
            best=summ
            number=i
            if sec >= i:
                number+=1
    #print('mov:',lists,best,number)
    return lists,best,int(number+1),wait"""
def movecard(lis,temp,sec):
    best=0
    number=0
    #print(len(lis))
    bestlist=[]
    for i in range(len(lis)):
        summ=0
        wait=0
        #a=[temp]
        
        lists=lis[:i]+[temp]+lis[i:]
        lists,summ,wait=is_double(lists,summ,wait)
        if summ>best:
            best=summ
            number=i
            bestlist=copy(lists)
            if sec >= i:
                number+=1
    #print('mov:',lists,best,number)
    return bestlist,best,int(number+1),wait
    
            
        

def search_card(card_list,times):
    besta=0
    lista=card_list
    suma=0
    #time=0
    numbera=len(lista)
    use={'a':0,'b':0,'c':0}
    timea=0
    numbera=len(lista)
    for i in range(len(lista)):

        if times <1:
            break
        wait=0
        lista=copy(card_list)
        temp=lista.pop(i)
        listma=copy(lista)
        #print("listma:",listma)
        suma=伤害计算(temp)
        lista,suma,wait=is_double(lista,suma,wait)

        if suma>besta:#记录最高期望伤害的操作
            besta=suma
            #use['a']=use.get("a",0)+1
            timea=wait+1
            listaa=copy(lista)#保存最优解的手牌序列
            use['a']=(i,numbera,timea,'use',(),listaa)
            
            
            tempa=copy(temp)
            print('使用',temp,)
            print("手牌组:",card_list)
            print('使用结束：',listaa)
            print('伤害：',suma)
            print()
        summa=0
        #listma=[]
        numberma=0
        
        listma,summa,numberma,waitma=movecard(listma,temp,i)
        
        if summa>besta:
            besta=summa
            timea=waitma+1
            listaa=copy(listma)
            use['a']=(i,numbera,timea,'mov',(i+1,numberma),listaa)
            '''
            print(use)
            print('移动',temp)
            print("手牌组",card_list)
            print('移动结束：',listma)
            print('伤害：',summa)
            print()'''
        bestb=0
        numberb=len(listaa)
        for j in range(len(listaa)):
            
            if times<2:
                break
            wait=0
            listb=copy(listaa)
            temp=listb.pop(j)
            listmb=copy(listb)
            sumb=伤害计算(temp)
            listb,sumb,wait=is_double(listb,sumb,wait)

            if sumb>bestb:
                bestb=int(sumb)
                timeb=wait+1
                listbb=copy(listb)
                use['b']=(j,numberb,timeb,'use',(),listaa)

                
                tempb=copy(temp)
                

            bestc=0
            
            summb=0
            numbermb=0
            listmb,summb,numbermb,waitmb=movecard(listmb,temp,j)
            if summb>bestb:
                bestb=int(summb)
                timeb=waitmb+1
                listbb=copy(listmb)
                
                use['b']=(j,numberb,timeb,'mov',(j+1,numbermb),listaa)
                
            
            numberc=len(listbb)
            for k in range(len(listbb)):
                numberc=len(listbb)
                wait=0
                if times<3:
                    break
                listc=copy(listbb)
                listmc=copy(listc)
                temp=listc.pop(k)
                listmc=copy(listc)
                sumc=伤害计算(temp)
                listc,sumc,wait=is_double(listc,sumc,wait)
                if sumc>bestc:
                    bestc=int(sumc)
                    timec=wait+1
                    listcc=copy(listc)
                    use['c']=(k,numberc,timec,'use',(),listcc)
                    
                    tempc=copy(temp)
                summc=0
                numbermc=0
                listmc,summc,numbermc,waitmc=movecard(listmc,temp,k)
                if summc>bestc:
                    bestc=summc
                    timec=waitmc+1
                    listcc=copy(listmc)
                    use['c']=(k,numberc,timec,'mov',(k+1,numbermc),listcc)
                

    return use

def touch(x, y):
    print(f'click {x} {y}')
    print(os.system(f'adb shell input tap {x} {y}'))


def touch(point):
    print(f'click {point[0]} {point[1]}')
    print(os.system(f'adb shell input tap {point[0]} {point[1]}'))


def swipe(p1, p2):
    print(f'swipe from  {p1[0]} {p1[1]} to {p2[0]} {p2[1]}')
    print(
        os.system(f'adb shell input touchscreen swipe {p1[0]} {p1[1]} {p2[0]} {p2[1]} 100'))



def getcardxy(n):
    x=int(flx[n]*data['x']/1920+165/2)
    y=int(822*data['y']/1080+197/2)
    return (x,y)

def use(lis):
    ls=[]
    print('dic:',lis)
    for k,v in lis.items():
        
        n=(8-v[1])+v[0]
        xy=getcardxy(n)
        ls.append((v[3],xy,v[2],v[4],v[5]))

    for i in ls:
        print(i[0])
        if i[0]=='use':
            print("touch({})".format(i[1]))
            touch(i[1])
        if i[0]=='mov':
            p1=getcardxy(i[3][0])
            p2=getcardxy(i[3][1])
            print('swipe({},{})'.format(p1,p2))
            
            swipe(p1, p2)
        print("time.sleep{}".format(i[2]))
        time.sleep(i[2])


def AAA():#测试函数，用于行动一步
    ccc=search_card(search_cards(t.team),gettimes())
    use(ccc)

def onestep(team):#用于行动一步
    a=search_card(search_cards(team),gettimes())
    use(a)

def activea():#测试函数，用于测试战斗逻辑
    while 1:
        try:
            
            ccc=search_card(search_cards(t.team),gettimes())
            use(ccc)
        except:
            print("error")
            #continue
        time.sleep(15)

def cut(pa1,pa2,imgname="screenshot.png",name='image',br='r'):
    #开发用函数，输入截取图片名称，任意两对角点，
    #可以自动完成切分和图片储存
    img = cv.imread(imgname)
    p1=[pa1[0],pa1[1]]
    p2=[pa2[0],pa2[1]]
    if p1[0]>p2[0]:
        p1[0],p2[0]=p2[0],p1[0]
    if p1[1]>p2[1]:
        p1[1],p2[1]=p2[1],p1[1]
    img2 = img[p1[1]:p2[1],
               p1[0]:p2[0]]
    if br=='w':
        cv.imshow('a',img2)
        cv.imwrite('{}.png'.format(name),img2)
    if br=='r':
        pass
    return img2

personnamelis=['Eternity', 'MedicinePocket', 'NewBabel', 'Anan', 'Sotheby', 'Druvis', 'Voyager', 'Knight', 'Lilya', 'Regulus', 'Centurion', 'Sonetto', 'Charlie', 'BalloonParty', 'Matilda','X']

def getteam(br=False):
    if br:
        get_screen_shot()
    lis=[[[836,112],[1061,382]],
     [[1083,201],[1312,471]],
     [[1333,157],[1562,427]],
     [[1582,112],[1809,382]]]#角色头像坐标
    """carda/{i}.png"""
    perlis=[]
    for i in range(len(lis)):
        #print('切分人物截图')
        a=lis[i]
        perlis.append(cut(a[0],a[1]))
    personlis=[]
    for i in personnamelis:
        #print("读取人物素材")
        try:
            personlis.append((cv.imread(f'carda/{i}.png'),i))
        except:
            print("Person ReadError:{}".format(i))
    personallis=[]
    for i in perlis:
        #print(i)
        best=0
        person=''
        for j in personlis:
            #print(j)
            #a=0
            try:
                a=similar(i,j[0])
            except:
                a=0
            if a>best and a>0.5:
                best=a
                person=j[1]
        personallis.append(person)
        #print(best)
    return personallis

def find(id: str, take=False):
    #使用相似算法寻找图中位置
    #（但不好用基本上用不了）
    if take:
        get_screen_shot()
    img = cv.imread("screenshot.png")
    #print(f'{id}.png')
    #img_terminal = cv.imread(f'{id}.png')#读入模板图片
    img_terminal = cv.imread(id)
    #print(img_terminal.shape)

    #print(img_terminal.shape)
    height, width, dep = img_terminal.shape#读取模板图片大小分辨率

    result = cv.matchTemplate(img, img_terminal, cv.TM_SQDIFF_NORMED)#搜索模板图片对应位置

    upper_left = cv.minMaxLoc(result)[2]#左上角坐标为对应矩阵位置
    #img = cv.imread("screenshot.png")#再读入图片（没看懂为什么要再读一遍）
    img2 = img[upper_left[1]:upper_left[1]+height,
               upper_left[0]:upper_left[0] + width]#在原图中切出相似区域
    lower_right = (upper_left[0]+width, upper_left[1]+height)#右下角坐标

    avg = (int((upper_left[0]+lower_right[0])/2),
           int((upper_left[1]+lower_right[1])/2),#返回图像中点坐标和模板图片以及
           similar(img_terminal, img2),
           (width,height))#计算相似度最高区域的图片的相似值
    
    # cv.imwrite(f'{id}2.png', img2)
    #可以返回图像中点坐标，相似度，模板尺寸
    return avg

def is_restart():
    """>>> cut([1248,945],[1315,1019],br='w')
        >>> 复现按钮
        >>> cut([1375,945],[1820,1019],br='w')
        >>> 开始按钮"""
    """检测是否可以复现，暂且掠过
        mrstart=cut([1248,945],[1315,1019])
        a=similar(mrstart,cv.imread('carda/rstart2.png'))
        if a>0.75:
            touch((1282,982))"""
    pass

def action(times=1):
    #该函数针对进入关卡后，可以看到和选择队伍人员的界面开发
    #逻辑顺序1：尝试复现，检测复现选项，失败则点击按钮开始战斗
    #逻辑顺序2：进入战斗后，检测行动点位置，行动点出现则认为行动已完成，可以开始出牌
    #逻辑顺序3：若未发现行动点，则尝试检测结束标志，若发现，则行动完成，行动次数+1
    
    team=getteam()
    for i in range(times):
        #为多次行动做准备
        is_restart()
        a=cut([1375,945],[1820,1019])
        aa=similar(mrstart,cv.imread('carda/action1.png'))
        bb=similar(mrstart,cv.imread('carda/action2.png'))
        if aa > 0.5 or bb>0.5:
            touch((1598,952))#点击开始作战按钮，进入战斗
            fight(team)
        """复现模块代码
        #rstart=find('carda/rstart.png')
        print(rstart)
        #if rstart[2][0]>0.45:
        if 1:
            #r=find('carda/rstart.png')
            touch((rstart[0],rstart[1]))#尝试点击复现按钮
            cx=find('carda/cx.png')
            if cx[2][0]>0.45:
                touch(cx[0],cx[1])
                best=0#进入复现部分
            else:#无法复现，开始行动
                a=find('carda/action1.png')
                b=find('carda/action2.png')
                if a[2][0]>0.45:
                    touch((a[0],a[1]))
                    print(a)
                elif b[2][0]>0.45:
                    touch((b[0],b[1]))
                    print(b)
                else:
                    print('未找到行动按钮')"""
    return 0

def fight(team):
    while True:
        touch((980,295))
        a=get_screen_shot(ip)
        if a==False:
            continue
        ls=[]
        imgm=cv.imread('carda/disappear.png')
        for i in range(3):
            a=cut([802+(101+29)*i,224],[802+101+(101+29)*i,365],imgname="screenshot1.png",br='w',name=i)
            b=similar(a.imgm)
            ls.append(b)
        if b[0]>0.5 and b[1]>0.5 and b[2]>0.5:
            #认为行动完成，可以开始出牌
            onestep(team)
        
        #准备添加战斗获胜结算界面
        #如果发现，break
        time.sleep(1)


    

"""
            for i in range(4):
                x=find('carda/x{}.png'.format(i))
                if x[2][0]>best and x[2][0]>0.5:
                    best=x[2][0]#发现复现倍率选项
        a=find('carda/action1.png')
        b=find('carda/action2.png')
        if a[2][0]>0.45:
            print(a)
        elif b[2][0]>0.45:
            print(b)
    return a"""
    
#active()
#AAA()

name_to_english= {
    '温妮弗雷德' : 'Eternity',
    '兔毛手袋' : 'MedicinePocket',
    '新巴别塔' : 'NewBabel',
    '泥鯭的士' : 'Anan',
    '新巴别塔' : 'NewBabel',
    '苏芙比' : 'Sotheby',
    '槲寄生' : 'Druvis',
    '远旅' : 'Voyager',
    '未锈铠' : 'Knight',
    '红弩箭' : 'Lilya',
    '星锑' : 'Regulus',
    '百夫长' : 'Centurion',
    '十四行诗' : 'Sonetto',
    '夏利' : 'Charlie',
    '气球派对' : 'BalloonParty',
    '玛蒂尔达' : 'Matilda',

}

'''
800,366
903,223
103,143'''
            

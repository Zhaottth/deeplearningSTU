from html import escape
from math import exp, sqrt, pi

G='#25664f'; O='#b8653c'; L='#c4d3c0'; M='#687b6a'
def text(x,y,t,size=15,color=G,anchor='middle'):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" fill="{color}">{escape(t)}</text>'
def line(x1,y1,x2,y2,color=L,dash=''):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.5"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def box(x,y,w,h,t,fill='#e5eee1'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}"/>'+text(x+w/2,y+h/2+5,t)
def frame(title,body,caption,h=230):
    return '<figure class="concept-figure"><svg viewBox="0 0 720 '+str(h)+'" role="img" aria-label="'+escape(title)+'"><title>'+escape(title)+'</title>'+body+'</svg><figcaption>'+escape(caption)+'</figcaption></figure>'

def visual(i):
    if i in (5,6):
        b='<rect x="30" y="25" width="660" height="197" rx="4" fill="#faf8f1" stroke="#c4d3c0"/>'+text(56,49,'Ω',18)
        if i==5:
            b+='<ellipse cx="225" cy="120" rx="100" ry="72" fill="#dce8da" stroke="#25664f"/><ellipse cx="500" cy="120" rx="84" ry="72" fill="#f1dcb8" stroke="#b8653c"/>'
            b+=text(225,70,'A',18)+text(500,70,'B',18)+text(195,126,'1',22)+text(252,146,'2',22)+text(500,132,'5',22,O)
            for x,t in [(80,'3'),(355,'4'),(640,'6')]:b+=text(x,194,t,18,M)
            b+=text(360,253,'互斥：没有重叠；并集共 2+1=3 个结果',18)
            return frame('互斥事件可以直接相加',b,'大框是全部结果 Ω={1,2,3,4,5,6}。左圈 A={1,2}，右圈 B={5}，不重叠。两个圈里共有 3 个结果，公平骰子下 P(A∪B)=3/6。圈的面积只用于示意，不代表概率。',280)
        b+='<ellipse cx="275" cy="120" rx="148" ry="80" fill="#dce8da" fill-opacity=".85" stroke="#25664f"/><ellipse cx="440" cy="120" rx="148" ry="80" fill="#f1dcb8" fill-opacity=".6" stroke="#b8653c"/>'
        b+=text(210,68,'A',18)+text(502,68,'B',18,O)+text(210,130,'2',23)+text(357,100,'4',23)+text(357,155,'6',23)+text(509,130,'5',23,O)+text(78,190,'1',18,M)+text(642,190,'3',18,M)
        b+=text(360,253,'并集数 2、4、5、6；交集只数重叠处的 4、6',18)
        return frame('并集收两圈，交集只收重叠',b,'A={2,4,6}，B={4,5,6}。相加 3+3 时，重叠的 4、6 各数了两遍，所以并集结果数为 3+3−2=4。图中圈的面积不代表概率，概率按六个等可能点数来数。',280)
    if i==2:
        b=text(360,30,'一枚公平骰子：完整名单 6 个，偶数名单 3 个',17)
        for j in range(1,7):
            x=100+(j-1)*104;fill=G if j%2==0 else '#e5eee1'
            b+=f'<circle cx="{x}" cy="100" r="28" fill="{fill}"/>'+text(x,106,str(j),22,'white' if j%2==0 else G)
        b+=text(360,170,'P(偶数) = 符合要求的 3 个 / 全部 6 个 = 1/2',19)
        return frame('先数分母，再数分子',b,'每个圆是一个可能点数，深绿色表示偶数 2、4、6。六个基本结果等可能，所以能用个数相除。这是一张结果名单，没有坐标轴。',200)
    if i==9:
        b=text(160,30,'原世界：六种等可能结果',17)+text(545,30,'已知偶数：只留下 2、4、6',17)
        for j in range(6):
            x=70+(j%3)*80;y=80+(j//3)*65
            fill=G if j+1>3 else '#e5eee1'
            b+=f'<circle cx="{x}" cy="{y}" r="25" fill="{fill}"/>'+text(x,y+5,str(j+1),17,'white' if j+1>3 else G)
        b+=text(345,120,'→',32)
        for j,v in enumerate((2,4,6)):
            x=455+j*85;b+=f'<circle cx="{x}" cy="110" r="28" fill="{G if v>3 else L}"/>'+text(x,116,str(v),20,'white' if v>3 else G)
        b+=text(150,205,'P(大于 3) = 3/6',16)+text(540,205,'P(大于 3 | 偶数) = 2/3',16)
        return frame('条件概率改变参照范围',b,'绿色表示大于 3。已知“偶数”后，分母从六种结果缩小为三种；满足所求的只剩 4 和 6。')
    if i in (19,20):
        b=text(360,26,'5 个位置选 2 个成功位置，共 10 种安排',17)
        k=0
        for a in range(5):
            for c in range(a+1,5):
                x=35+(k%5)*140;y=74+(k//5)*85
                for j in range(5):
                    b+=f'<circle cx="{x+j*21}" cy="{y}" r="8" fill="{G if j in (a,c) else L}"/>'
                b+=text(x+42,y+31,f'{a+1}、{c+1}',12,M);k+=1
        b+=text(360,218,'每一种的概率相同：p²(1−p)³；总概率再乘 10',14)
        return frame('二项系数计数图',b,'深绿是成功，浅绿是失败。组合数计算位置安排数，不是把同一个顺序重复算十次。')
    if i in (22,23,24):
        b=line(75,185,650,185)+line(75,185,75,35)+text(650,211,'x',15)+text(60,35,'f(x)',15)
        b+='<path d="M75 185L575 45" fill="none" stroke="'+G+'" stroke-width="3"/>'
        b+='<path d="M75 185L325 115L325 185Z" fill="#b8d4be"/>'
        b+=line(325,185,325,115,O,'4 4')+text(75,211,'0',13)+text(325,211,'0.5',13)+text(575,211,'1',13)
        b+=text(435,70,'f(x)=2x',18)+text(210,166,'面积 = 0.25',15)+text(570,29,'密度高度≠概率',14,M)
        return frame('密度曲线下的面积',b,'f(x)=2x，0≤x≤1。绿色三角形面积为 0.5×0.5×1=0.25，所以 P(X≤0.5)=0.25；f(0.5)=1 是高度。')
    if i in (26,37):
        X=lambda z:360+80*z;Y=lambda y:190-350*y
        pts=[(X(-3.6+k*.018),Y(exp(-.5*(-3.6+k*.018)**2)/sqrt(2*pi))) for k in range(401)]
        b=line(45,190,675,190)
        sub=[(x,y) for x,y in pts if 280<=x<=440]
        b+='<path d="M280 190 '+''.join(f'L{x:.2f} {y:.2f}' for x,y in sub)+'L440 190Z" fill="#bdd7c0"/>'
        b+='<path d="'+''.join(('M' if k==0 else 'L')+f'{x:.2f} {y:.2f}' for k,(x,y) in enumerate(pts))+'" fill="none" stroke="'+G+'" stroke-width="3"/>'
        for z,t in [(-2,'μ−2σ'),(-1,'μ−σ'),(0,'μ'),(1,'μ+σ'),(2,'μ+2σ')]:
            b+=line(X(z),190,X(z),Y(exp(-z*z/2)/sqrt(2*pi)),L,'4 4')+text(X(z),215,t,13)
        b+=text(360,29,'均值左右一个标准差：约 68.27% 的概率',17)
        return frame('正态分布的位置与尺度',b,'只有正态分布才具有这里的 68.27% 比例。标准化改变位置和尺度，并不把任意分布变成正态。')
    if i==30:
        b=text(360,30,'四张等可能卡片：0、0、0、4',19)
        for j,v in enumerate((0,0,0,4)):
            b+=box(105+j*135,65,100,65,str(v))
        b+=text(360,174,'(0+0+0+4)/4 = 0×3/4 + 4×1/4 = 1',22)
        return frame('普通平均变成概率加权平均',b,'每张卡片概率为 1/4。把三个 0 合并后，数值 0 的权重为 3/4；数值 4 的权重为 1/4。这不是抽到数值 1，而是加权后的平均为 1。',205)
    if i in (34,35):
        b=line(90,110,630,110)
        for x,t in [(180,'X=0'),(360,'μ=1'),(540,'X=2')]:
            b+=f'<circle cx="{x}" cy="110" r="8" fill="{G if x!=360 else O}"/>'+text(x,148,t,18)
        b+=text(270,85,'偏差 −1',16)+text(450,85,'偏差 +1',16)
        b+=box(120,175,220,48,'平方后：1')+box(380,175,220,48,'平方后：1')
        b+=text(360,30,'各以 1/2 取 0、2：方差 = (1+1)/2 = 1',17)
        return frame('方差先平方再平均',b,'偏差直接平均会抵消为零；平方后衡量离中心的距离。均值 1 不需要是变量实际能取得的值。',250)
    if i in (66,68,101):
        b=text(360,28,'前向计算给出损失；反向传播传递局部导数',17)
        labels=['输入 x','得分 z','概率 p','损失 J'] if i!=68 else ['输入 x','预测 ŷ','误差 r','损失 J']
        if i==101:labels=['输入固定','得分 z (3,)','概率 q (3,)','损失 J（数）']
        for j,t in enumerate(labels):
            x=15+j*180;b+=box(x,73,145,55,t)
            if j<3:b+=text(x+160,108,'→',22)
        b+=text(360,172,'← 梯度沿计算链返回参数',19,O)
        if i==68:b+=text(360,214,'J = (ŷ−y)²/2； ∂J/∂ŷ = ŷ−y',17)
        elif i==101:b+=text(360,214,'softmax + 交叉熵：得分梯度 g = q−y',17)
        else:b+=text(360,214,'sigmoid + 二元交叉熵： ∂ℓ/∂z = p−y',17)
        return frame('从概率损失到反向传播',b,'每一条箭头都有一个局部导数。沿链相乘得到参数梯度；概率模型解释损失，链式法则解释梯度。',245)
    if i in (77,83,84):
        b=line(360,38,360,200,M,'4 4')+text(360,24,'固定真值 μ',16)
        intervals=[(240,430,300),(310,505,410),(125,320,225),(270,465,365),(205,400,290)]
        for j,(a,c,mean) in enumerate(intervals):
            y=60+j*32;ok=a<=360<=c;col=G if ok else O;b+=line(a,y,c,y,col)+f'<circle cx="{mean}" cy="{y}" r="4" fill="{col}"/>'
        return frame('置信区间的随机性在区间',b,'这是覆盖含义的示意图，不是模拟结果。真值固定不动；换一批样本，样本均值与区间一起变化，有的会漏掉真值。')
    return ''

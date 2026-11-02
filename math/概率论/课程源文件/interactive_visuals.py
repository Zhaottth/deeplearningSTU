"""只把有助于当前概念的互动图嵌入相应课程。"""
from html import escape

KINDS={46:'joint',47:'joint',48:'triangle',55:'gaussian',68:'loss'}

def interactive(i):
    kind=KINDS.get(i)
    if not kind:return ''
    ids=f'visual-{i}'
    if kind=='joint':
        title='把四格概率表，立起来看。'
        intro='沿用本节的 100 人例子。X 表示是否点击，Y 表示是否购买；0 表示否，1 表示是。每根柱子对应一对结果，柱高就是这对结果的概率。'
        controls='<label>圈出哪一组<select data-visual-event><option value="all">全部结果</option><option value="both" selected>点击且购买：X=1，Y=1</option><option value="click">点击：X=1</option><option value="either">至少一个为 1</option><option value="same">两个结果相同：X=Y</option></select></label>'
        reading='<li><b>两条底边：</b>X 是点击，Y 是购买。底面上的位置 (1,1) 表示点击且购买。</li><li><b>竖直方向：</b>柱高是概率。柱宽只用于排版；离散概率直接读柱高。</li><li><b>橙色柱：</b>符合你所选事件的结果。把这些柱高相加，就是事件概率。</li>'
        question='先选“点击”，猜一猜要加哪两根柱子，再核对数表。'
        fallback='''<div class="visual-data-table"><table><caption>同一组数据 · 数表核对（每格为概率）</caption><thead><tr><th scope="col">Y \\ X</th><th scope="col">X=0 未点击</th><th scope="col">X=1 点击</th></tr></thead><tbody><tr><th scope="row">Y=0 未购买</th><td data-joint-cell="0,0">0.60</td><td data-joint-cell="1,0">0.10</td></tr><tr><th scope="row">Y=1 购买</th><td data-joint-cell="0,1">0.10</td><td data-joint-cell="1,1">0.20</td></tr></tbody></table></div>'''
        note='四根柱高相加为 1。改变视角和圈选事件，都不会改变原来的四个概率。'
    elif kind=='triangle':
        title='高度是 2，概率为什么仍不超过 1？'
        intro='本节的连续模型：只在三角区域 0<x<y<1 上，密度 f(x,y)=2；其余位置为 0。先看底面的三角形，再看它上方的体积。'
        controls='<label>事件边界 t：只看 X&lt;t <output data-visual-param-value>0.50</output><input data-visual-param type="range" min="0" max="1" step="0.05" value="0.5"></label>'
        reading='<li><b>底面：</b>横向 X、纵向 Y。只有 X&lt;Y 的半个正方形有密度，底面积为 1/2。</li><li><b>竖直方向：</b>高度恒为密度 2。完整体积=底面积 1/2 × 高 2=1，所以总概率为 1。</li><li><b>橙色部分：</b>在 X&lt;t 区域上方的体积。改变 t，改变的是所问区域，密度模型保持不变。</li>'
        question='把 t 设成 0.5：底面选中的面积是多少？为什么乘以高度 2 后，概率是 0.75？'
        fallback='<noscript><p>总底面积为 1/2，乘密度 2 得总概率 1。t=0.5 时，未选中的是边长 0.5 的三角形，面积 0.125；选中面积 0.5−0.125=0.375，乘 2 得 0.75。</p></noscript>'
        note='连续密度的高度不是概率。这里用平坦的三角台，先让“底面面积 × 高度 = 概率体积”可以直接手算。'
    elif kind=='gaussian':
        title='转一转，看看两个量怎样一起变化。'
        intro='固定均值为 (0,0)，X 的标准差为 2，Y 的标准差为 1。只改变相关系数 ρ（读作“柔”），观察等密度轮廓的方向。'
        controls='<label>相关系数 ρ <output data-visual-param-value>0.00</output><input data-visual-param type="range" min="-0.85" max="0.85" step="0.05" value="0"></label>'
        reading='<li><b>两条底边：</b>分别是 X 与 Y 的数值，底面上的一个位置对应一对观测值。</li><li><b>竖直方向：</b>高度是联合密度 f(x,y)。颜色越深、曲面越高，附近小区域的概率密度越大。</li><li><b>平面图：</b>线条连接相同密度的点。ρ&gt;0 时轮廓沿同向偏离倾斜，ρ&lt;0 时沿反向偏离倾斜。每条线的围内概率并非标注的密度值。</li>'
        question='先保持 ρ=0，再改成 0.7：两个方向各自的标准差没变，轮廓的方向发生了什么？'
        fallback='<noscript><p>ρ=0 时，Σ=[[4,0],[0,1]]，等密度轮廓沿 X 方向更宽；ρ=0.7 时，Σ=[[4,1.4],[1.4,1]]，轮廓沿同向偏离倾斜。</p></noscript>'
        note='图只展示 X、Y 各在 −6 到 6 的窗口。完整曲面下的体积为 1；某个点的高度和某条等密度线都不是单点概率。'
    else:
        title='看一次更新，怎样沿着损失走低。'
        intro='沿用本节的一条数据：输入 x=2，真实值 y=5。底面两轴放参数 w、b，竖直方向放损失 J=(2w+b−5)²/2。橙色点从 w=1、b=0 出发。'
        controls='<label>学习率 η <output data-visual-param-value>0.10</output><input data-visual-param type="range" min="0.02" max="0.45" step="0.01" value="0.1"></label><button class="button" data-visual-step>更新一步 →</button><button data-visual-restart>重新开始</button>'
        reading='<li><b>底面：</b>每个位置是一组参数 (w,b)，不是一条输入数据。移动点，就是换一组参数。</li><li><b>竖直方向：</b>高度是这一组参数的损失。橙线记录更新路径；点越低，当前数据上的误差越小。</li><li><b>谷底：</b>单条数据只要求 2w+b=5，因此整条谷底线都达到零损失，最优参数并不唯一。</li>'
        question='先用 η=0.1 更新一步，核对 4.5→1.125。再重新开始，把 η 调到 0.45，预测损失会怎样变化。'
        fallback='<noscript><p>初始 w=1、b=0、J=4.5。η=0.1 时，新参数 w=1.6、b=0.3，新损失 J=1.125。η=0.45 时，新参数 w=3.7、b=1.35，新损失为 7.03125，步长过大使损失上升。</p></noscript>'
        note='同一份固定数据，只改变参数。曲面本身不随更新改变；为容纳路径，显示窗口可能扩大。学习率过大时，损失可能上升。'
    return f'''<section class="math-visual" data-visual-kind="{kind}" id="{ids}" aria-labelledby="{ids}-title"><div class="section-heading"><span>读图 / 先预测，再动手</span><h2 id="{ids}-title">{title}</h2></div><p class="visual-intro">{intro}</p><div class="visual-model-controls">{controls}</div><div class="visual-viewbar"><div role="group" aria-label="选择读图方式"><button data-visual-view="3d" aria-pressed="true">3D · 拖动旋转</button><button data-visual-view="2d" aria-pressed="false">平面图</button></div><button data-visual-reset>还原视角 ↺</button></div><canvas class="visual-canvas" role="img" aria-label="{escape(title)}" aria-describedby="{ids}-caption">{escape(intro)}</canvas><div class="visual-camera"><label>左右转动<input data-visual-yaw type="range" min="-180" max="180" step="1" value="-35"></label><label>观察仰角<input data-visual-elevation type="range" min="15" max="75" step="1" value="32"></label><span>鼠标或手指左右拖动图形，也能旋转。</span></div><p class="visual-readout" data-visual-readout role="status" aria-live="polite"></p>{fallback}<div class="visual-reading" id="{ids}-caption"><strong>这张图这样读</strong><ol>{reading}</ol><p class="visual-note">{note}</p></div><p class="visual-question">{question}</p></section>'''

"""从课程目录与教学内容生成全部离线页面，无需外部源文件。"""
from pathlib import Path
import json
import sys
sys.dont_write_bytecode=True
from content import LESSONS
from notebook import TITLES as titles, lesson, shell, index, glossary, name, esc
ROOT=Path(__file__).resolve().parent.parent

def review():
    formulas=[('事件规则','P(Aᶜ)=1−P(A)；P(A∪B)=P(A)+P(B)−P(A∩B)','补集不要求独立；并集需扣重复。'),('条件与贝叶斯','P(A|B)=P(A∩B)/P(B)；P(A|B)=P(B|A)P(A)/P(B)','分母为正；区分条件方向。'),('期望与方差','E[aX+b]=aE[X]+b；Var(X)=E[X²]−E[X]²','矩需存在；Var(aX+b)=a²Var(X)。'),('变量之和','Var(X+Y)=Var(X)+Var(Y)+2Cov(X,Y)','独立或零协方差时才可直接加方差。'),('独立样本均值','E[X̄]=μ；SE(X̄)=σ/√n','标准误公式要求独立同方差等条件。'),('二项分布','P(X=k)=C(n,k)pᵏ(1−p)ⁿ⁻ᵏ','固定 n，独立，同 p。'),('MLE 与 MAP','MLE: max ln L；MAP: max(ln L+ln prior)','连续观测用密度；先验影响参数估计。'),('二元交叉熵','−[y ln p+(1−y)ln(1−p)]；∂ℓ/∂z=p−y','最后一个梯度要求 p=sigmoid(z)。'),('均值区间','x̄ ± t_(1−α/2,n−1) s/√n','独立正态样本 σ 未知时精确。'),('Welch 标准误','SE=√(s₁²/n₁+s₂²/n₂)','两组独立；配对时先求差值。'),('比例区间','Wilson 区间通常比简单 Wald 更稳健','小样本及边界不要得到零宽区间就放心。'),('信息论','H(p,q)=H(p)+D_KL(p||q)','p 固定时，交叉熵与该方向 KL 同步变化。')]
    cards=''.join(f'<section class="formula-card"><h3>{esc(t)}</h3><div class="formula">{esc(f)}</div><p>{esc(c)}</p></section>' for t,f,c in formulas)
    tasks=[('两枚独立公平骰子，已知和为偶数，求和为 8 的概率。','和为偶数共有 18 个有序对；和为 8 共 5 个，所以 5/18。先条件化再计数。'),('正面率 p 未知，20 次有 14 次正面。求 MLE，再用 Beta(2,2) 先验更新。','MLE=0.7；后验 Beta(16,8)，后验均值 2/3，内部 MAP=15/22≈0.6818。'),('已知 σ=8，独立样本 n=64，x̄=100，95% 均值区间是什么？','SE=1，区间 [98.04,101.96]。需要正态精确条件或合适大样本近似。'),('同 12 个任务对比两个模型，为什么不直接做独立两样本检验？','同任务结果可能相关，应分析每任务差值。若差值条件满足，用配对 t 检验，df=11。'),('p=0.2，y=1，z 是 sigmoid 输入，x=3 且 z=wx+b。单样本梯度？','dℓ/dz=p−y=−0.8；dℓ/dw=−2.4；dℓ/db=−0.8。梯度下降推动真实类概率上升。'),('实验 p=0.08，是否证明两个方法相同？','不能。可能精度不足；需看差异区间。要主张等效，应预定等效界限并使用相应方法。')]
    quiz=''.join(f'<details class="review-question"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in tasks)
    return shell('总复习','<div class="utility-page"><div class="eyebrow">REVIEW ／ 把知识连成线</div><h1>先解释，再算一遍。</h1><p class="goal">公式旁边永远写上条件。练习能独立完成，再考虑标记“掌握”。</p><div class="formula-grid">'+cards+'</div><h2>六道综合检查题</h2>'+quiz+'<section class="teaching example"><h2>一个小项目：把硬币学到底</h2><ol><li>在实验室选择真实 p，生成多次观测，记录频率。</li><li>手算 MLE，再画出似然与负对数损失。</li><li>用 Beta 先验更新，比较 MLE、后验均值和 MAP。</li><li>重复抽样，观察区间覆盖与样本量的关系。</li><li>解释为什么当前样本不能确定参数，为什么后面的试验不需要补偿前面的偏差。</li></ol><p>完成标准：每一步能说出假设、公式由来和结果的解释。</p></section></div>')

def lab_page():
    return shell('互动实验室','''<div class="utility-page labs"><div class="eyebrow">PROBABILITY LAB ／ 先预测，再动手</div><h1>让公式，动起来。</h1><p class="goal">改变一个参数，先想象图会怎样，再核对计算。所有实验在本机运行。</p><nav class="lab-tabs"><a href="#events">骰子与事件</a><a href="#bayes">贝叶斯</a><a href="#distribution">分布</a><a href="#sampling">抽样</a><a href="#likelihood">似然</a><a href="#coverage">区间覆盖</a></nav>
<section class="lab-panel" id="events"><header><span>01</span><h2>36 个格子，看清并集与条件</h2></header><p>每格是两枚独立公平骰子的一个有序对，概率都是 1/36。选取 A、B 后，看重叠和条件样本空间。</p><div class="controls"><label>事件 A<select id="event-a"><option value="sum7">点数和 = 7</option><option value="sumge7" selected>点数和 ≥ 7</option><option value="firsteven">第一枚为偶数</option><option value="same">两枚相同</option></select></label><label>已知事件 B<select id="event-b"><option value="firsteven" selected>第一枚为偶数</option><option value="sumeven">点数和为偶数</option><option value="sumge7">点数和 ≥ 7</option><option value="second6">第二枚为 6</option></select></label></div><div class="dice-layout"><div><div class="dice-caption">行：第一枚 ／ 列：第二枚</div><div id="dice-grid" class="dice-grid"></div><div class="legend"><span><i class="a-color"></i>仅 A</span><span><i class="b-color"></i>仅 B</span><span><i class="both-color"></i>A∩B</span></div></div><div id="event-output" class="results" aria-live="polite"></div></div><p class="lab-question">想一想：P(A|B) 的分母，为什么是 B 的格子数？</p></section>
<section class="lab-panel" id="bayes"><header><span>02</span><h2>阳性之后，概率是多少？</h2></header><p>下表把模型换算为 10000 人中的期望人数。改变先验患病率，观察阳性人群的构成。</p><div class="controls"><label>先验患病率 <output id="prior-value"></output><input id="prior" type="range" min="1" max="500" value="10"></label><label>灵敏度 <output id="sensitivity-value"></output><input id="sensitivity" type="range" min="10" max="100" value="90"></label><label>假阳性率 <output id="falsepositive-value"></output><input id="falsepositive" type="range" min="1" max="300" value="50"></label></div><div id="bayes-output" aria-live="polite"></div><div id="bayes-bar" class="bayes-bar"></div><p class="small muted">绿色：真阳性；橙色：假阳性。横条显示阳性池内部的占比。人数为期望值，可能含小数。</p><p class="lab-question">先把患病率调低：为什么同样的检测也会给出完全不同的后验？</p></section>
<section class="lab-panel" id="distribution"><header><span>03</span><h2>形状、概率与累计</h2></header><div class="controls"><label>分布<select id="dist-type"><option value="binomial">二项分布 Bin(n,p)</option><option value="normal">正态分布 N(μ,σ²)</option><option value="uniform">均匀分布 U(0,b)</option></select></label><label><span id="dist-param1-label">试验次数 n</span> <output id="dist-param1-value"></output><input id="dist-param1" type="range" min="1" max="40" value="10"></label><label><span id="dist-param2-label">成功率 p</span> <output id="dist-param2-value"></output><input id="dist-param2" type="range" min="1" max="99" value="50"></label><label>累计阈值 x <output id="dist-threshold-value"></output><input id="dist-threshold" type="range" min="0" max="40" value="5" step="1"></label></div><div id="dist-chart" class="chart"></div><div id="dist-output" class="results" aria-live="polite"></div><p class="small muted">绿色：x 左侧概率质量或密度面积。橙线：CDF，读取右侧 0–1 刻度。连续密度曲线只显示有限窗口，总概率由完整分布计算。</p></section>
<section class="lab-panel" id="sampling"><header><span>04</span><h2>平均值，怎样变得稳定？</h2></header><div class="controls"><label>观察模式<select id="sample-mode"><option value="lln">大数定律：一条硬币累计频率</option><option value="clt">中心极限定理：很多批均值</option></select></label><label>每批观测数 n <output id="sample-n-value"></output><input id="sample-n" type="range" min="1" max="100" value="20"></label><label>CLT 原分布<select id="sample-source"><option value="uniform">U(0,1)</option><option value="exponential">指数分布，均值 1</option><option value="bernoulli">Bern(0.2)</option></select></label><button class="button secondary" id="resample">换一批随机数据 ↻</button></div><div id="sample-chart" class="chart"></div><div id="sample-output" class="results" aria-live="polite"></div><p class="small muted">LLN 固定公平硬币共 1000 次，滑块 n 仅用于 CLT。CLT 重复 2000 批，画每批均值；每次换数据更新随机种子。改变 n 会用同一随机序列比较。</p></section>
<section class="lab-panel" id="likelihood"><header><span>05</span><h2>最大似然，怎样变成交叉熵？</h2></header><p>固定数据：20 次观测，14 次成功。只改变模型参数 p。曲线是平均负对数似然；越低，模型给这份数据的似然越高。</p><div class="controls"><label>模型成功率 p <output id="like-p-value"></output><input id="like-p" type="range" min="1" max="99" value="50"></label><button class="button secondary" id="like-mle">跳到 MLE：p=0.7</button></div><div id="like-chart" class="chart"></div><div id="like-output" class="results" aria-live="polite"></div><div class="formula">J(p)=−[0.7 ln p + 0.3 ln(1−p)]<br>dJ/dp=(p−0.7)/[p(1−p)]<br>若 p=sigmoid(z)，dJ/dz=p−0.7</div><p class="lab-question">在 p=0.5 时，梯度是什么符号？梯度下降会把 p 推向哪一边？</p></section>
<section class="lab-panel" id="coverage"><header><span>06</span><h2>95% 置信度，是反复抽样的覆盖</h2></header><p>真均值 μ=0、已知 σ=1，每次独立抽样得到一个均值，画出一个 z 区间。重复 100 次，看哪些区间漏掉固定真值。</p><div class="controls"><label>每次样本量 n <output id="coverage-n-value"></output><input id="coverage-n" type="range" min="4" max="400" value="25"></label><label>置信度<select id="coverage-confidence"><option value="90">90%</option><option value="95" selected>95%</option><option value="99">99%</option></select></label><button class="button secondary" id="coverage-resample">重做 100 次抽样 ↻</button></div><div id="coverage-chart" class="chart coverage-chart"></div><div id="coverage-output" class="results" aria-live="polite"></div><p class="small muted">绿色覆盖 μ，橙色漏掉 μ。使用正态样本均值的精确抽样分布直接生成均值。改变 n 复用标准化偏差，因此覆盖数保持不变而区间缩窄；点“重做”才重新抽样。</p><p class="lab-question">为什么 95% 不保证这 100 个区间恰好有 95 个覆盖？</p></section></div>''',mode='lab-page') .replace('</body>','<script src="资源/labs.js" defer></script></body>')


def main():
    (ROOT/'课程').mkdir(exist_ok=True)
    (ROOT/'资源').mkdir(exist_ok=True)
    doc=index()
    (ROOT/'开始学习.html').write_text(doc,encoding='utf-8')
    for i in titles:
        (ROOT/'课程'/name(i)).write_text(shell(titles[i],lesson(i,True),base='../',mode='standalone',lesson_id=i),encoding='utf-8')
    for filename,render in (('术语与符号.html',glossary),('总复习.html',review),('实验室.html',lab_page)):
        (ROOT/filename).write_text(render(),encoding='utf-8')
    (ROOT/'课程源文件/课程目录.json').write_text(json.dumps([{'id':i,'title':titles[i],'file':'课程/'+name(i),'original':i<99} for i in titles],ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'先看这里.txt').write_text(README,encoding='utf-8')
    print(f'Generated {len(titles)} guided lessons and 4 entry/reference pages.')

README="""概率手记 · 从高中数学出发

双击“开始学习.html”即可学习。无需网络、安装或账号。
“开始学习.html”是唯一的学习入口，固定使用它可以延续同一入口的笔记。

顶部只显示当前这一节需要的知识，切换课程会自动更换；完整内容可到“符号词典”查。
点击符号可看高中知识的小例子，也能按需补导数、积分、向量矩阵与梯度。
首页骰子实验可切换并集、交集、条件概率；实色表示符合要求，边框表示分母范围。

课程共 102 节：原目录 0–98，加 3 节信息论与深度学习补充。
每节先进入一个有选项的生活场景，选完会看到针对这条判断的解释；然后读小例子、变量关系与符号、逐步推导、数值例子与检查题。每章都在当前页面补足所需基础，不需要配套视频或外部课程。
“再往前一步”只多显示一个推导步骤；也可以展开全部。检查题先写草稿再看解析。
草稿不保存；“轮到你解释了”中的理解笔记和掌握标记会保存在当前浏览器。
上一版的进度记录格式保持兼容，原有的导出 JSON 可以合并导入。
不同浏览器或文件目录不一定共享记录，建议定期导出备份。

首页按 / 搜索课程全文；阅读时可用左右方向键翻课。
点击章节标题可收起目录。搜索时会自动展开匹配章节。
Python 代码块可复制运行；包含频率、分类训练、回归训练和三候选词得分更新。
实验室保留 6 个互动实验，独立讲义可以离线阅读与打印。
第 05、06 节有集合图；第 46、47、48、55、68 节有本地互动 3D 图，可拖动旋转、切换平面图。
目录里带“3D 可动”标记的课程含有互动图，搜索 3D 可筛选出来；进入后点击“直接看本节互动图”即可到达。
3D 图分别解释联合概率柱高、连续概率体积、多元正态密度与回归损失更新；图旁附坐标、颜色和读图说明。
打印时自动展开本页推导和解析，结束后恢复阅读状态。

课程可按自己的节奏学习；每章故事、基础小抄、推导、互动与检查题都在当前页面。
资源/ 为本地样式与交互，课程源文件/ 为生成内容；重新生成后可运行 verify.py 检查。
"""
if __name__=='__main__':main()

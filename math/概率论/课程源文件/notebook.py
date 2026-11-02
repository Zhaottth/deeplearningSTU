"""静态概率手册的页面、阅读台阶与共享知识速查。"""
from pathlib import Path
import html, json, re
from content import LESSONS
from pedagogy import TOOLS, GUIDES, CODE
from diagrams import visual
from interactive_visuals import interactive, KINDS
from episodes import EPISODES, scene as episode_scene

ROOT=Path(__file__).resolve().parent.parent
TITLES={r['id']:r['title'] for r in json.loads((ROOT/'课程源文件/课程目录.json').read_text(encoding='utf-8'))}
GROUPS=[(0,29,'01','概率基础与分布','先找分母，再谈机会。'),(30,56,'02','期望、波动与关系','平均以外，数据还在说什么？'),(57,76,'03','从样本学习参数','让数据来调整模型。'),(77,98,'04','统计推断与实验','给结论留出误差的空间。'),(99,101,'＋','走向深度学习','把概率接到一次真实计算。')]
def esc(s): return html.escape(str(s),quote=True)
def group(i):return next(g for g in GROUPS if g[0]<=i<=g[1])
def name(i):return f'{i:02d}_{re.sub(r"[\\/:*?\"<>|]", "", TITLES[i])}.html'
def paragraphs(s):return ''.join('<p>'+esc(p)+'</p>' for p in s.split('\n') if p)

TOOL_CHIPS={
 'sets':('sets','{…}','集合 · 按条件分类'),
 'fractions':('fractions','a/b','分数 · 分母先定范围'),
 'powers':('powers','aⁿ','指数 · 重复相乘'),
 'functions':('functions','f(x)','函数 · 输入与输出'),
 'average':('average','∑','求和与加权平均'),
 'squares':('squares','√','平方、根号与单位'),
 'logs':('logs','ln','对数 · 指数的逆运算'),
 'derivative':('derivative','f′','导数 · 变化率'),
 'integral':('integral','∫','积分 · 累加面积'),
 'vectors':('vectors','[…]','向量与矩阵'),
 'chain':('chain','∇','梯度 · 参数更新'),
}
OVERVIEW_CHIPS=[('sets','∪','并集 · 至少一个'),('sets','∩','交集 · 同时满足'),('fractions','P(A|B)','条件概率 · 已知 B'),TOOL_CHIPS['fractions']]

def knowledge_items(i):
    d=LESSONS[i];guide=GUIDES[i]
    text=' '.join([guide['question'],guide['example'],d['intuition'],*d['steps'],d['example'],d['warning'],d['question'],d['answer']])
    chips=[]
    for symbol,label in [('∪','并集 · 至少一个'),('∩','交集 · 同时满足'),('Aᶜ','补集 · A 不发生')]:
        if symbol in text:chips.append(('sets',symbol,label))
    if re.search(r'P\([^)]*\|',text):chips.append(('fractions','P(A|B)','条件概率 · 已知 B'))
    # 运算符只在这一节实际出现时列出，前置基础取该节自己的清单。
    chips.extend(TOOL_CHIPS[key] for key in guide['tools'])
    return chips

def toolbox(lesson_id=None, overview=False, base=''):
    chips=knowledge_items(lesson_id) if lesson_id is not None else OVERVIEW_CHIPS if overview else []
    buttons=''.join(f'<button class="tool-chip" data-tool="{k}"><span class="math">{s}</span><span>{label}</span></button>' for k,s,label in chips)
    panels=''.join(f'<section class="tool-panel" id="tool-{key}" data-tool-panel="{key}" hidden><div class="eyebrow">{esc(v[1])}</div><h2>{esc(v[0])}</h2><p>{esc(v[2])}</p><div class="worked-mini">{esc(v[3])}</div></section>' for key,v in TOOLS.items())
    tabs=''.join(f'<button data-tool="{key}">{esc(v[0])}</button>' for key,v in TOOLS.items())
    label='本节用到' if lesson_id is not None else '本页用到'
    return f'''<section class="knowledge-shelf" aria-label="当前内容所需知识" data-overview-knowledge="{esc(json.dumps(OVERVIEW_CHIPS,ensure_ascii=False))}"{'' if chips else ' hidden'}><div class="shelf-label"><strong>{label}</strong><small>不认识就点一下</small></div><div class="shelf-chips" aria-live="polite">{buttons}</div><a class="all-tools" href="{base}术语与符号.html">去符号词典 ↗</a></section><dialog id="toolbox-dialog" aria-label="知识工具箱"><div class="dialog-top"><strong>随手查 · 知识工具箱</strong><button data-close-tool aria-label="关闭知识工具箱">关闭 ×</button></div><p class="dialog-note">高中知识先用起来；导数、积分和矩阵在需要时补。</p><div class="tool-layout"><nav aria-label="工具分类">{tabs}</nav><div>{panels}</div></div></dialog>'''

def shell(title,body,base='',mode='',sidebar='',lesson_id=None):
    if 'data-visual-kind=' in body:
        body+=f'<script src="{base}资源/visual-math.js" defer></script><script src="{base}资源/math-visuals.js" defer></script>'
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="从高中数学开始的概率学习手册：先手算一个小例子，再拆开符号，一步步理解推导、统计与模型训练。离线可用。"><title>{esc(title)} · 概率手记</title><link rel="stylesheet" href="{base}资源/course.css"><link rel="stylesheet" href="{base}资源/notebook.css?v=2"><link rel="stylesheet" href="{base}资源/math-visuals.css"></head>
<body class="{mode}"><a class="skip" href="#main">跳到正文</a><header class="topbar"><a class="brand" href="{base}开始学习.html"><span class="brand-mark">1<span>6</span></span><span>概率手记<small>从高中数学出发</small></span></a><span class="edition">一本可以动手的学习手册</span><nav aria-label="主导航"><a href="{base}开始学习.html">学习路线</a><a href="{base}实验室.html">动手实验</a><a href="{base}术语与符号.html">符号词典</a><a href="{base}总复习.html">复习</a></nav><button class="print-button" data-print>打印 ↗</button></header>{sidebar}<main id="main">{toolbox(lesson_id,mode=='course-app',base)}{body}</main><footer class="footer"><strong>概率手记</strong><span>先数清楚，再写公式。一次弄懂一个问题。</span><small>每节都在本页补足基础、推导、互动和练习；不需要配套视频或外部课程。离线使用，笔记留在当前浏览器。</small></footer><script src="{base}资源/notebook.js?v=2" defer></script></body></html>'''

def roles(i):
    if i<17:return [('先固定','试验规则、样本空间 Ω、已知条件。'),('在改变','试验结果；有新信息时，参照范围也可能改变。'),('要算出','事件的概率或更新后的比例；不是结果的编号。')]
    if i<57:return [('先固定','随机变量的定义、给定分布或这批数据。'),('在改变','可能的取值 x；作图时也可改变分布参数。'),('要算出','概率、均值、波动或关系；注意单位与条件。')]
    if i<65:return [('已知数据','抽到的观测值 x₁,…,xₙ，n 是样本个数。'),('未知对象','总体参数，例如均值 μ、成功率 p。'),('计算结果','样本均值、比例或方差；换一批样本通常会变。')]
    if i<77 or i>=99:return [('先固定','当前训练或观测数据；真实标签 y 不是待调参数。'),('在改变','模型参数 θ（例如 w、b、p）；预测随参数改变。'),('计算结果','似然、后验、损失或梯度；它们的作用各不相同。')]
    return [('已知数据','当前样本的均值、比例、波动与样本数。'),('先定规则','置信度或显著性水平、假设、方向与抽样条件。'),('计算结果','区间、统计量或 p 值；未知真值不因计算而改变。')]

def vocabulary(i):
    if i<=16:return [('Ω','全部可能结果的名单，叫样本空间。'),('A、B','事件：符合某个条件的结果集合。'),('P(A)','A 发生的概率，范围在 0 到 1。'),('∪ / ∩','至少一个成立 / 两个同时成立。'),('P(A|B)','已知 B，问 A；竖线右边先限定范围。')]
    if i<=29:return [('X / x','X 是从结果到数值的规则；x 是某个取值。'),('p / n / k','单次成功概率 / 试验次数 / 成功次数；看各节具体定义。'),('p(x) / f(x)','离散概率 / 连续密度。密度要乘宽度并累计。'),('F(x)','P(X≤x)：不超过 x 的累计概率。'),('∼','读“服从”；说明分布类型，不是等号。')]
    if i<=56:return [('E[X] / μ','概率加权平均 / 总体均值。'),('Var(X) / σ² / σ','方差 / 常用方差符号 / 标准差。'),('∑ / ∫','离散逐项相加 / 连续区域累计。'),('Cov(X,Y) / ρ','协方差 / 去掉单位后的线性相关系数。'),('Σ（矩阵）','协方差数表；与求和号 ∑ 按上下文区分。')]
    if i<=64:return [('n / xᵢ','观测个数 / 第 i 个观测值。'),('μ / σ² / p','固定但未知的总体均值 / 方差 / 成功率。'),('x̄ / p̂ / s²','这批数据算出的均值 / 成功比例 / 样本方差。'),('X̄ / x̄','抽样前会随机变化的均值 / 本次算出的均值。'),('SE','标准误，描述估计量反复抽样的波动。')]
    if i<=76 or i>=99:return [('θ / w / b','待估或待更新的参数 / 常用权重 / 截距。'),('x / y / ŷ','输入 / 真实结果或标签 / 模型预测。'),('L / J','似然常记 L；本手册的训练损失常记 J，勿混淆。'),('ln / exp','自然对数 / 以 e 为底的指数。'),('∂ / ∇ / η','只改一个参数的导数 / 各偏导组成的梯度 / 学习率。'),('p / q','信息论中常指真实分布 / 模型分布；两者都不是标签。')]
    return [('μ / p','未知总体均值 / 未知总体成功率。'),('x̄ / s / n','样本均值 / 样本标准差 / 样本数。'),('SE / SD','估计量的波动 / 观测值本身的波动。'),('H₀ / H₁','原假设 / 备择假设；数字 0、1 是编号。'),('α / β','第一类错误概率 / 指定备择下第二类错误概率。'),('p 值','H₀ 下至少同样极端的尾部概率；不同于参数 p。')]

def lesson(i,standalone=False):
    d=LESSONS[i]; guide=GUIDES[i];g=group(i);base='../' if standalone else ''
    visual_jump=f'<button class="visual-jump" data-scroll-visual="visual-{i}">直接看本节互动图 ↓</button>' if i in KINDS else ''
    vocab=''.join(f'<div><dt class="math">{esc(a)}</dt><dd>{esc(b)}</dd></div>' for a,b in vocabulary(i))
    rolehtml=''.join(f'<div><strong>{a}</strong><p>{b}</p></div>' for a,b in roles(i))
    # 每步只显示一块；无 JS 时全部可读。
    steps=''.join(f'<li data-step="{k}"><span class="step-number">{k+1:02d}</span><div>{paragraphs(s)}</div></li>' for k,s in enumerate(d['steps']))
    walkthrough=f'''<section class="teaching walkthrough"><div class="section-heading"><span>03 / 连起来想</span><h2>每一步，都有来由。</h2></div><ol class="steps">{steps}</ol><div class="step-controls" hidden><span class="step-status" aria-live="polite"></span><button data-next-step>再往前一步 →</button><button class="quiet-button" data-all-steps>展开全部</button></div></section>'''
    code=''
    if i in CODE:
        title,source,trace=CODE[i]
        code=f'<section class="teaching code-section"><div class="section-heading"><span>验证 / 把手算交给程序</span><h2>{esc(title)}</h2></div><p>下面是可直接运行的完整 Python 例子，只使用 Python 自带功能。</p><div class="code-bar"><span>Python 3</span><button data-copy-code>复制代码</button></div><pre><code>{esc(source)}</code></pre><p>{esc(trace)}</p></section>'
    prev=f'<a href="{base}开始学习.html#lesson-{i-1:02d}">← {esc(TITLES[i-1])}</a>' if i else '<a href="'+base+'开始学习.html">← 学习路线</a>'
    nxt=f'<a href="{base}开始学习.html#lesson-{i+1:02d}">{esc(TITLES[i+1])} →</a>' if i<101 else f'<a href="{base}总复习.html">去总复习 →</a>'
    # 入口里的前后翻课保持同一文件与存储上下文。
    if not standalone:prev=prev.replace('开始学习.html#','#');nxt=nxt.replace('开始学习.html#','#')
    reflection=f'<section class="reflection"><label for="note-{i}">轮到你解释了。</label><p>用自己的话写：这节在解决什么问题？哪一步还没想通？</p><textarea id="note-{i}" data-note="{i}" rows="3" placeholder="比如：已知偶数后，分母只数 2、4、6……"></textarea><div><button class="button mark" data-complete="{i}">我能解释这一节了 ✓</button><span class="save-state" role="status"></span></div></section>' if not standalone else f'<p class="notice">在<a href="../开始学习.html#lesson-{i:02d}">学习入口打开本节</a>，可以保存理解笔记与掌握进度。</p>'
    lab=f'<a class="lab-link" href="{base}实验室.html#{d["lab"]}">拿去实验室试一下 <span>改变一个量，核对你刚才的预测 ↗</span></a>' if d['lab'] else ''
    return f'''<article class="lesson" id="lesson-{i:02d}" data-id="{i}" data-knowledge="{esc(json.dumps(knowledge_items(i),ensure_ascii=False))}"{'' if standalone else ' hidden'}>
<header class="lesson-header"><div class="eyebrow">{g[2]} / {g[3]} <span>第 {i:02d} 节{' · 补充' if i>=99 else ''}</span></div><h1>{esc(TITLES[i])}</h1><p class="goal">这一节只抓住一件事：{esc(d['goal'])}</p></header>
{episode_scene(i)}{visual_jump}
<section class="teaching first-question"><div class="section-heading"><span>01 / 把现场翻译成数学</span><h2>先用一组小数字，摆好问题。</h2></div><p>{esc(guide['example'])}</p><p class="intuition">{esc(d['intuition'])}</p></section>
<section class="teaching notation"><div class="section-heading"><span>02 / 把字母读懂</span><h2>先认人，再看公式。</h2></div><div class="variable-roles">{rolehtml}</div><details><summary>这一节会遇到的符号 · 点开对照</summary><dl>{vocab}</dl><p class="small muted">字母的含义取决于本节定义；同一个字母在不同场景可能有不同用法。</p></details></section>
{walkthrough}{visual(i)}
<section class="teaching example"><div class="section-heading"><span>04 / 再算一次</span><h2>把数字带回去。</h2></div>{paragraphs(d['example'])}</section>{interactive(i)}{lab}{code}
<section class="teaching warning"><h2>这里停一下。</h2>{paragraphs(d['warning'])}</section>
<section class="teaching exercise"><div class="section-heading"><span>05 / 换你来</span><h2>先答一小题。</h2></div><p>{esc(d['question'])}</p><label for="answer-{i}" class="small">写下答案或理由，先别急着看解析。</label><textarea id="answer-{i}" class="scratch-answer" rows="2" placeholder="这是一张草稿纸，不计分，也不保存。"></textarea><details class="answer-details"><summary>我想过了，核对思路</summary>{paragraphs(d['answer'])}</details><p class="small muted">还卡着？先分清是基础、符号、计算，还是不知道哪个量在变；回到上面对应那一步。</p></section>
<details class="bridge"><summary>理解以后，再接到机器学习</summary>{paragraphs(d['bridge'])}</details>{reflection}<nav class="lesson-pagination" aria-label="前后课程">{prev}{nxt}</nav></article>'''

def index():
    sidebar='<aside class="sidebar"><div class="sidebar-title">你的学习路线</div><nav aria-label="课程章节">'+''.join(f'<a href="#module-{g[2]}" data-module="{g[2]}"><span>{g[2]}</span>{g[3]}</a>' for g in GROUPS)+'<a href="实验室.html"><span>↗</span>动手实验室</a></nav><div class="sidebar-note"><span class="hand-mark">记住</span><p>分母变了，<br>你问的问题<br>就变了。</p></div><div class="sidebar-bottom"><span id="progress-label">已掌握 0 / 99</span><div class="progress-track"><div id="progress-fill"></div></div><small>可以慢，别跳过不懂的那步。</small></div></aside>'
    dice=''.join(f'<button class="demo-die" data-die="{i}" aria-pressed="false" aria-label="点数 {i}，点击显示是否属于事件"><span class="pip-layout pips-{i}">'+''.join('<i></i>' for _ in range(i))+f'</span><span class="die-number">{i}</span></button>' for i in range(1,7))
    hero=f'''<section class="hero"><div class="hero-copy"><div class="eyebrow"><span class="issue">起点 001</span> 只用一枚公平骰子</div><h1>先别背公式。<br>来，<span class="underline">数一数。</span></h1><p>“偶数”有 3 个，“大于 3”也有 3 个。<br>合在一起，为什么不是 6 个？</p><div class="hero-actions"><a class="button" href="#lesson-02" id="continue-learning">从这里开始 →</a><a class="text-link" href="#catalog">看学习路线 ↓</a></div><p class="hero-footnote">不用找视频：每节都把要用的高中知识、完整推导和练习放在这一页。</p></div><div class="dice-note"><div class="note-top"><span>在这里，先玩明白</span><span class="note-index">EX. 01</span></div><div class="event-defs"><span><b>A</b> 偶数 {{2,4,6}}</span><span><b>B</b> 大于 3 {{4,5,6}}</span></div><div class="demo-modes" role="group" aria-label="选择事件运算"><button data-mode="union" class="active" aria-pressed="true">A∪B <small>至少一个</small></button><button data-mode="intersection" aria-pressed="false">A∩B <small>同时满足</small></button><button data-mode="conditional" aria-pressed="false">P(A|B) <small>已知 B</small></button></div><div class="demo-dice">{dice}</div><p class="dice-key"><span></span>实色：符合要求 <i></i>边框：当前分母范围</p><div class="demo-result" aria-live="polite"><div class="demo-equation math" id="demo-equation">P(A∪B) = 4 / 6 = 2 / 3</div><p id="demo-explanation">4 和 6 重复了。3+3−2=4 个，分母仍是全部 6 个。</p></div><p id="die-inspect" class="die-inspect" aria-live="polite">点任意一枚骰子，看看它属于哪份名单。</p></div></section>'''
    home=f'<div id="overview">{hero}{episode_scene(6,home=True)}<div class="learning-strip"><span><b>01</b> 先用故事做判断</span><span><b>02</b> 再把符号拆开</span><span><b>03</b> 一步一步推出去</span><span><b>04</b> 换你解释一次</span></div><section class="welcome"><div><span class="hand-mark">一个人也能学</span><h2>不必先找老师或视频。<br>每页都从你会的地方开始。</h2><p>先看一个小场景，自己选答案，页面马上解释为什么。再补上这一节真正用到的高中知识，手算、看图、逐步推导，最后亲自试一题。导数、积分、向量和矩阵也会在第一次用到时讲清楚。</p></div><div class="study-controls"><strong id="home-progress">已掌握 0 / 99 节</strong><span id="bonus-progress" class="small muted">补充课 0 / 3</span><div class="backup"><button id="export-progress">导出进度与笔记 ↗</button><label class="import-label">导入<input type="file" id="import-progress" accept="application/json,.json"></label></div><span class="small muted" id="storage-status" role="status">记录保存在当前浏览器，建议定期导出。</span></div></section><section class="catalog" id="catalog"><div class="catalog-tools"><div><div class="eyebrow">102 个小问题 / 不用按课时赶进度</div><h2>挑一个你想解开的谜。</h2></div><label class="search"><span>找一节课</span><input type="search" id="course-search" placeholder="试试：条件概率、方差、损失" aria-label="搜索全部课程"><kbd>/</kbd></label></div><p class="small muted" id="search-status" aria-live="polite">每节都是一份独立小讲义，卡住时可点页面最上方的本节知识点。</p>'
    for lo,hi,num,title,desc in GROUPS:
        home+=f'<details class="module" id="module-{num}"'+(' open' if lo==0 else '')+f'><summary class="module-header"><span class="module-number">{num}</span><span><h3>{title}</h3><p>{desc}</p></span><span class="module-count">{hi-lo+1} 节 <b>＋</b></span></summary><div class="lesson-grid">'
        for i in range(lo,hi+1):
            d=LESSONS[i];guide=GUIDES[i];case=EPISODES[i];corpus=' '.join([TITLES[i],*map(str,d.values()),guide['question'],guide['example'],case['title'],case['scene'],'3D 三维 互动图' if i in KINDS else ''])
            tag='<small class="lesson-visual-tag">3D 可动</small>' if i in KINDS else ''
            home+=f'<a class="lesson-card" href="#lesson-{i:02d}" data-card="{i}" data-search="{esc(corpus)}"><span class="lesson-number">{i:02d}</span><div><h4>{esc(TITLES[i])}{tag}</h4><p><span class="case-teaser">{esc(case["title"])}</span></p></div><span class="card-check" aria-hidden="true">↗</span></a>'
        home+='</div></details>'
    home+='</section><noscript><p class="notice">当前浏览器未启用 JavaScript。下面的独立讲义仍可阅读，全部推导步骤会直接显示。</p><ul>'+''.join(f'<li><a href="课程/{esc(name(i))}">{i:02d} {esc(TITLES[i])}</a></li>' for i in TITLES)+'</ul></noscript></div>'
    home+='<div id="reader" hidden><div class="reader-toolbar"><a href="#catalog">← 返回学习路线</a><span id="reader-position"></span><a id="standalone-link" href="#">独立讲义 ↗</a></div>'+''.join(lesson(i) for i in TITLES)+'</div>'
    return shell('开始学习',home,mode='course-app',sidebar=sidebar)

def glossary():
    toolsections=''.join(f'<section class="foundation" id="foundation-{key}"><div class="eyebrow">{esc(v[1])}</div><h2>{esc(v[0])}</h2><p>{esc(v[2])}</p><div class="worked-mini">{esc(v[3])}</div></section>' for key,v in TOOLS.items())
    vocab={a:b for i in (0,17,30,58,68,89) for a,b in vocabulary(i)}
    rows=''.join(f'<tr><th scope="row" class="math">{esc(a)}</th><td>{esc(b)}</td></tr>' for a,b in vocab.items())
    return shell('术语与符号',f'<div class="utility-page"><div class="eyebrow">随手查 / 不必一次背完</div><h1>每个符号，<br>都有一句人话。</h1><p class="goal">先查符号的含义，再回到原来的例子里。∪ 是并集，∩ 是交集；字母 U 是另一回事。</p><nav class="foundation-links">'+''.join(f'<a href="#foundation-{k}">{esc(v[0])}</a>' for k,v in TOOLS.items())+f'</nav>{toolsections}<h2>公式中常见的字母</h2><div class="table-scroll"><table><thead><tr><th>符号</th><th>在这门课里怎么读</th></tr></thead><tbody>{rows}</tbody></table></div></div>')

/* 本地 Canvas 画出可旋转模型；所有概率与更新均来自 visual-math.js。 */
(()=>{'use strict';
const M=globalThis.ProbabilityVisualMath;if(!M)return;
const $=(s,r)=>r.querySelector(s),all=(s,r)=>[...r.querySelectorAll(s)];
const clamp=(x,a,b)=>Math.min(b,Math.max(a,x)),fmt=(x,d=3)=>Number(x.toFixed(d)).toString();
const teal='#246f65',orange='#bf4932',ink='#343b32',muted='#70796a',paper='#faf8f1';
function isSelected(c,event){return event==='all'||event==='both'&&c.x===1&&c.y===1||event==='click'&&c.x===1||event==='either'&&c.x+c.y>=1||event==='same'&&c.x===c.y}

all('.math-visual',document).forEach(root=>{
  const kind=root.dataset.visualKind,canvas=$('canvas',root),ctx=canvas.getContext('2d');if(!ctx)return;
  const state={view:'3d',yaw:-35,elevation:32,rho:0,t:0.5,rate:0.1,event:'both',history:[{w:1,b:0}],last:null};
  const out=$('[data-visual-readout]',root),parameter=$('[data-visual-param]',root);let scheduled=false,drag=null;
  root.classList.add('is-interactive');
  function updateText(){
    if(parameter)$('[data-visual-param-value]',root).textContent=Number(parameter.value).toFixed(2);
    if(kind==='joint'){
      const selected=M.joint.filter(c=>isSelected(c,state.event)),sum=selected.reduce((a,c)=>a+c.p,0);
      out.textContent=selected.map(c=>`p(${c.x},${c.y})`).join(' + ')+' = '+selected.map(c=>fmt(c.p)).join(' + ')+(selected.length>1?` = ${fmt(sum)}`:'')+'；四格总和为 1。';
      all('[data-joint-cell]',root).forEach(cell=>{const [x,y]=cell.dataset.jointCell.split(',').map(Number),selected=isSelected({x,y},state.event);cell.classList.toggle('visual-selected',selected);cell.setAttribute('aria-label',`X=${x}，Y=${y}，概率 ${cell.textContent}${selected?'，属于所选事件':''}`)});
    }else if(kind==='triangle'){
      const area=state.t-state.t*state.t/2;
      out.textContent=`t=${fmt(state.t,2)}：选中底面积 ${fmt(area,4)} × 高度 2 = 概率 ${fmt(M.triangleProbability(state.t),4)}。`;
    }else if(kind==='gaussian'){
      out.textContent=`ρ=${state.rho.toFixed(2)}；Σ=[[4,${fmt(2*state.rho,2)}],[${fmt(2*state.rho,2)},1]]；中心密度 f(0,0)≈${fmt(M.gaussian(0,0,state.rho),4)}。X、Y 的标准差仍为 2、1。`;
    }else{
      const p=state.history.at(-1),j=M.loss(p.w,p.b),n=state.history.length-1;
      out.textContent=`第 ${n} 步：w=${fmt(p.w,4)}，b=${fmt(p.b,4)}，预测 ŷ=${fmt(2*p.w+p.b,4)}，损失 J=${fmt(j,6)}。`+(state.last===null?'':`本次损失 ${fmt(state.last,6)} → ${fmt(j,6)}，${j<state.last?'下降':j>state.last?'上升':'保持不变'}。`);
      const button=$('[data-visual-step]',root);button.disabled=n>=20;button.textContent=n>=20?'已更新 20 步，请重新开始':'更新一步 →';
    }
    all('[data-visual-view]',root).forEach(b=>b.setAttribute('aria-pressed',String(state.view===b.dataset.visualView)));
    $('.visual-camera',root).hidden=state.view==='2d';canvas.hidden=kind==='joint'&&state.view==='2d';
  }
  function ranges(){
    if(kind==='joint')return {x:[-0.5,1.5],y:[-0.5,1.5],z:[0,0.7],xname:'X 点击',yname:'Y 购买',zname:'概率'};
    if(kind==='triangle')return {x:[0,1],y:[0,1],z:[0,2.4],xname:'X',yname:'Y',zname:'密度'};
    if(kind==='gaussian')return {x:[-6,6],y:[-6,6],z:[0,0.16],xname:'X',yname:'Y',zname:'密度'};
    const xs=state.history.map(p=>p.w),ys=state.history.map(p=>p.b),x=[Math.min(0,...xs)-0.3,Math.max(3,...xs)+0.3],y=[Math.min(-1,...ys)-0.3,Math.max(2,...ys)+0.3];
    const max=Math.max(...x.flatMap(w=>y.map(b=>M.loss(w,b))));return{x,y,z:[0,max*1.05],xname:'w',yname:'b',zname:'损失 J'};
  }
  function schedule(){if(scheduled)return;scheduled=true;requestAnimationFrame(()=>{scheduled=false;draw()})}
  function draw(){
    if(canvas.hidden)return;
    const box=canvas.getBoundingClientRect();if(box.width<1||box.height<1)return;
    const W=box.width,H=box.height,dpr=Math.min(devicePixelRatio||1,2);
    if(canvas.width!==Math.round(W*dpr)||canvas.height!==Math.round(H*dpr)){canvas.width=Math.round(W*dpr);canvas.height=Math.round(H*dpr)}
    ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,W,H);ctx.fillStyle=paper;ctx.fillRect(0,0,W,H);
    const r=ranges(),rad=Math.PI/180,angle=state.yaw*rad,elevation=state.elevation*rad,scale=Math.min(W*.30,H*.47),cx=W*.51,cy=H*.67;
    const norm=(v,b)=>(v-b[0])/(b[1]-b[0]);
    function project(p){const x=norm(p[0],r.x)*2-1,y=norm(p[1],r.y)*2-1,z=norm(p[2],r.z),rx=x*Math.cos(angle)-y*Math.sin(angle),ry=x*Math.sin(angle)+y*Math.cos(angle);return[cx+rx*scale,cy+ry*scale*Math.sin(elevation)-z*scale*1.35*Math.cos(elevation),ry*Math.cos(elevation)+z*1.35*Math.sin(elevation)]}
    function text(label,x,y,color=ink,size=12,align='center'){ctx.font=`${size}px "Microsoft YaHei",sans-serif`;ctx.fillStyle=color;ctx.textAlign=align;ctx.textBaseline='middle';const half=ctx.measureText(label).width/2;x=clamp(x,align==='center'?half+6:6,align==='center'?W-half-6:W-6);ctx.fillText(label,x,clamp(y,12,H-12))}
    function polygon(points,fill,stroke='#ffffff70'){ctx.beginPath();points.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.closePath();ctx.fillStyle=fill;ctx.fill();if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=.55;ctx.stroke()}}
    function poly3(points,fill,stroke){polygon(points.map(project),fill,stroke)}
    function line3(points,color,width=1){ctx.beginPath();points.map(project).forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.strokeStyle=color;ctx.lineWidth=width;ctx.stroke()}
    const shade=value=>`hsl(164 31% ${94-58*Math.sqrt(clamp(value,0,1))}%)`;
    const functionValue=(x,y)=>kind==='gaussian'?M.gaussian(x,y,state.rho):M.loss(x,y);
    function planeSetup(){const marginX=W<450?46:62,marginY=44,size=Math.min(W-2*marginX,H-2*marginY),left=(W-size)/2,top=marginY;return{size,left,top,point:(x,y)=>[left+norm(x,r.x)*size,top+size-norm(y,r.y)*size]}}
    if(state.view==='2d'&&kind!=='joint'){
      const p=planeSetup(),N=kind==='triangle'?20:48;
      for(let i=0;i<N;i++)for(let j=0;j<N;j++){
        const x0=r.x[0]+i/N*(r.x[1]-r.x[0]),x1=r.x[0]+(i+1)/N*(r.x[1]-r.x[0]),y0=r.y[0]+j/N*(r.y[1]-r.y[0]),y1=r.y[0]+(j+1)/N*(r.y[1]-r.y[0]);
        if(kind==='triangle'){
          if(i>j)continue;const points=i===j?[[x0,y0],[x1,y1],[x0,y1]]:[[x0,y0],[x1,y0],[x1,y1],[x0,y1]];
          polygon(points.map(v=>p.point(...v)),(x0+x1)/2<state.t?'#c26748':'#aac8b4',null);
        }else{const z=functionValue((x0+x1)/2,(y0+y1)/2);ctx.fillStyle=shade(z/r.z[1]);const q=p.point(x0,y1);ctx.fillRect(q[0],q[1],p.size/N+.6,p.size/N+.6)}
      }
      if(kind==='gaussian')for(const radius of [1,2,3]){ctx.beginPath();for(let k=0;k<=120;k++){const t=k/120*2*Math.PI,x=2*radius*Math.cos(t),y=radius*(state.rho*Math.cos(t)+Math.sqrt(1-state.rho**2)*Math.sin(t)),q=p.point(x,y);k?ctx.lineTo(...q):ctx.moveTo(...q)}ctx.strokeStyle='#246f6590';ctx.lineWidth=1.2;ctx.stroke()}
      if(kind==='triangle'){const a=p.point(state.t,0),b=p.point(state.t,1);ctx.setLineDash([5,4]);ctx.beginPath();ctx.moveTo(...a);ctx.lineTo(...b);ctx.strokeStyle=orange;ctx.lineWidth=2;ctx.stroke();ctx.setLineDash([]);text('X<t',p.left+9,p.top+15,orange,11,'left')}
      if(kind==='loss'){
        ctx.beginPath();for(let k=0;k<=100;k++){const w=r.x[0]+(r.x[1]-r.x[0])*k/100,b=5-2*w;if(b<r.y[0]||b>r.y[1])continue;const q=p.point(w,b);if(k===0)ctx.moveTo(...q);else ctx.lineTo(...q)}ctx.strokeStyle=teal;ctx.lineWidth=2;ctx.stroke();
        ctx.beginPath();state.history.forEach((v,i)=>{const q=p.point(v.w,v.b);i?ctx.lineTo(...q):ctx.moveTo(...q)});ctx.strokeStyle=orange;ctx.lineWidth=2;ctx.stroke();const v=state.history.at(-1),q=p.point(v.w,v.b);ctx.beginPath();ctx.arc(...q,5,0,Math.PI*2);ctx.fillStyle=orange;ctx.fill();ctx.strokeStyle=paper;ctx.lineWidth=2;ctx.stroke();
      }
      ctx.strokeStyle='#9baf9c';ctx.strokeRect(p.left,p.top,p.size,p.size);
      for(let k=0;k<=4;k++){const x=r.x[0]+k/4*(r.x[1]-r.x[0]),y=r.y[0]+k/4*(r.y[1]-r.y[0]);text(fmt(x,2),p.left+k/4*p.size,p.top+p.size+16,muted,10);text(fmt(y,2),p.left-13,p.top+p.size-k/4*p.size,muted,10)}
      text(r.xname,p.left+p.size+26,p.top+p.size,ink,12);text(r.yname,p.left,p.top-17,ink,12);
      text(kind==='gaussian'?'同色与曲线上的点密度相近':kind==='triangle'?'橙色底面面积 × 2 = 概率':'颜色越深，损失越高；橙点是当前参数',W/2,17,muted,11);
      return;
    }
    // 底面网格与三条坐标轴。曲面的高度采用线性刻度。
    const x0=r.x[0],x1=r.x[1],y0=r.y[0],y1=r.y[1];
    poly3([[x0,y0,0],[x1,y0,0],[x1,y1,0],[x0,y1,0]],'#e9edde',null);
    for(let k=0;k<=4;k++){const x=x0+k/4*(x1-x0),y=y0+k/4*(y1-y0);line3([[x,y0,0],[x,y1,0]],'#bfcbb690');line3([[x0,y,0],[x1,y,0]],'#bfcbb690')}
    const faces=[];
    function face(points,color,stroke){faces.push({points,color,stroke,depth:points.reduce((a,p)=>a+project(p)[2],0)/points.length})}
    if(kind==='joint'){
      for(const c of M.joint){const a=c.x-.28,b=c.x+.28,d=c.y-.28,e=c.y+.28,z=c.p,chosen=isSelected(c,state.event),top=chosen?'#c26748':'#4b8b78',side=chosen?'#ad583b':'#397761';
        face([[a,d,0],[b,d,0],[b,d,z],[a,d,z]],side);face([[b,d,0],[b,e,0],[b,e,z],[b,d,z]],side);face([[b,e,0],[a,e,0],[a,e,z],[b,e,z]],side);face([[a,e,0],[a,d,0],[a,d,z],[a,e,z]],side);face([[a,d,z],[b,d,z],[b,e,z],[a,e,z]],top);
      }
    }else if(kind==='triangle'){
      const N=20;
      for(let i=0;i<N;i++)for(let j=i;j<N;j++){const a=i/N,b=(i+1)/N,d=j/N,e=(j+1)/N,points=i===j?[[a,d,2],[b,e,2],[a,e,2]]:[[a,d,2],[b,d,2],[b,e,2],[a,e,2]];face(points,(a+b)/2<state.t?'#c26748':'#78a68a')}
      for(const [a,b] of [[[0,0],[0,1]],[[0,1],[1,1]],[[1,1],[0,0]]])for(let k=0;k<N;k++){
        const c=a.map((v,j)=>v+(b[j]-v)*k/N),d=a.map((v,j)=>v+(b[j]-v)*(k+1)/N),chosen=(c[0]+d[0])/2<state.t;
        face([[...c,0],[...d,0],[...d,2],[...c,2]],chosen?'#c26748c0':'#94b29ab0',chosen?'#ad583b60':'#70967960');
      }
    }else{
      const N=34;
      for(let i=0;i<N;i++)for(let j=0;j<N;j++){const a=x0+i/N*(x1-x0),b=x0+(i+1)/N*(x1-x0),d=y0+j/N*(y1-y0),e=y0+(j+1)/N*(y1-y0),points=[[a,d,functionValue(a,d)],[b,d,functionValue(b,d)],[b,e,functionValue(b,e)],[a,e,functionValue(a,e)]];face(points,shade(functionValue((a+b)/2,(d+e)/2)/r.z[1]))}
    }
    faces.sort((a,b)=>a.depth-b.depth).forEach(f=>poly3(f.points,f.color,f.stroke));
    line3([[x0,y0,0],[x1,y0,0]],'#70876c',1.3);line3([[x0,y0,0],[x0,y1,0]],'#70876c',1.3);line3([[x0,y0,0],[x0,y0,r.z[1]]],'#70876c',1.3);
    for(let k=0;k<=2;k++){const z=r.z[1]*k/2,p=project([x0,y0,z]);text(fmt(z,3),p[0]-18,p[1],muted,10)}
    const xp=project([x1,y0,0]),yp=project([x0,y1,0]),zp=project([x0,y0,r.z[1]]);text(r.xname,xp[0]+23,xp[1]+29,ink,12);text(r.yname,yp[0]-29,yp[1]+29,ink,12);text(r.zname,zp[0],zp[1]-18,ink,12);
    const ticks=kind==='joint'?[0,1]:[x0,(x0+x1)/2,x1];
    for(const x of ticks){const p=project([x,y0,0]);text(fmt(x,1),p[0],p[1]+12,muted,10)}
    for(const y of kind==='joint'?[0,1]:[(y0+y1)/2,y1]){const p=project([x0,y,0]);text(fmt(y,1),p[0]-9,p[1]+6,muted,10)}
    if(kind==='joint')for(const c of M.joint){const p=project([c.x,c.y,c.p]);text(c.p.toFixed(2),p[0],p[1]-11,ink,12)}
    if(kind==='loss'){
      line3(state.history.map(p=>[p.w,p.b,M.loss(p.w,p.b)+r.z[1]*.008]),orange,2.5);
      const v=state.history.at(-1),q=project([v.w,v.b,M.loss(v.w,v.b)+r.z[1]*.01]);ctx.beginPath();ctx.arc(q[0],q[1],6,0,Math.PI*2);ctx.fillStyle=orange;ctx.fill();ctx.strokeStyle=paper;ctx.lineWidth=2;ctx.stroke();text('当前参数',q[0]+30,q[1]-15,orange,11);
    }
    text(kind==='joint'?'柱高 = 这一对结果的概率':kind==='loss'?'曲面固定，橙点沿更新路径移动':'密度高度不是概率；曲面下的体积才是概率',W/2,20,muted,11);
  }
  all('[data-visual-view]',root).forEach(b=>b.addEventListener('click',()=>{state.view=b.dataset.visualView;updateText();schedule()}));
  $('[data-visual-reset]',root).addEventListener('click',()=>{state.yaw=-35;state.elevation=32;$('[data-visual-yaw]',root).value=-35;$('[data-visual-elevation]',root).value=32;schedule()});
  for(const key of ['yaw','elevation'])$(`[data-visual-${key}]`,root).addEventListener('input',e=>{state[key]=Number(e.target.value);schedule()});
  if(parameter)parameter.addEventListener('input',()=>{const n=Number(parameter.value);if(kind==='gaussian')state.rho=n;else if(kind==='triangle')state.t=n;else state.rate=n;updateText();schedule()});
  $('[data-visual-event]',root)?.addEventListener('change',e=>{state.event=e.target.value;updateText();schedule()});
  $('[data-visual-step]',root)?.addEventListener('click',()=>{if(state.history.length>20)return;const p=state.history.at(-1);state.last=M.loss(p.w,p.b);state.history.push(M.step(p.w,p.b,state.rate));updateText();schedule()});
  $('[data-visual-restart]',root)?.addEventListener('click',()=>{state.history=[{w:1,b:0}];state.last=null;updateText();schedule()});
  canvas.addEventListener('pointerdown',e=>{if(state.view!=='3d')return;drag={x:e.clientX,yaw:state.yaw};canvas.setPointerCapture(e.pointerId)});
  canvas.addEventListener('pointermove',e=>{if(!drag)return;state.yaw=((drag.yaw+(e.clientX-drag.x)*.65+540)%360)-180;$('[data-visual-yaw]',root).value=state.yaw;schedule()});
  for(const event of ['pointerup','pointercancel','lostpointercapture'])canvas.addEventListener(event,()=>drag=null);
  new ResizeObserver(schedule).observe(canvas);updateText();schedule();
});
all('[data-scroll-visual]',document).forEach(button=>button.addEventListener('click',()=>{
  const target=document.getElementById(button.dataset.scrollVisual);
  target?.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth',block:'start'});
}));
})();

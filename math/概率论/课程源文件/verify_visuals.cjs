// 核对图里的概率、密度归一化与训练更新；不依赖绘图实现。
const assert=require('node:assert/strict');
const M=require('../资源/visual-math.js');
const close=(a,b,tol=1e-10)=>assert.ok(Math.abs(a-b)<tol,`${a} != ${b}`);
close(M.joint.reduce((s,c)=>s+c.p,0),1);
close(M.joint.filter(c=>c.x===1).reduce((s,c)=>s+c.p,0),0.3);
close(M.joint.filter(c=>c.x===1&&c.y===1).reduce((s,c)=>s+c.p,0),0.2);
close(M.triangleProbability(0),0);close(M.triangleProbability(0.5),0.75);close(M.triangleProbability(1),1);
for(const rho of [-0.7,0,0.7]){
  let mass=0,xx=0,yy=0,xy=0;const N=240,dx=16/N,dy=12/N;
  for(let i=0;i<N;i++)for(let j=0;j<N;j++){
    const x=-8+(i+.5)*dx,y=-6+(j+.5)*dy,p=M.gaussian(x,y,rho)*dx*dy;
    assert.ok(p>=0);mass+=p;xx+=x*x*p;yy+=y*y*p;xy+=x*y*p;
  }
  close(mass,1,0.0001);close(xx,4,0.01);close(yy,1,0.002);close(xy,2*rho,0.003);
}
close(M.gaussian(0,0,0),1/(4*Math.PI));
const small=M.step(1,0,.1);close(small.w,1.6);close(small.b,.3);close(M.loss(small.w,small.b),1.125);
const large=M.step(1,0,.45);close(M.loss(large.w,large.b),7.03125);assert.ok(M.loss(large.w,large.b)>M.loss(1,0));
for(const w of [-1,0,1,2.5])close(M.loss(w,5-2*w),0);
console.log('PASS: joint probabilities, triangular probability volume, Gaussian mass/covariance, small-step descent, large-step increase, and non-unique zero-loss valley.');

/* 图形与手算共用的数学模型；不依赖网络或第三方库。 */
(()=>{'use strict';
const joint=[{x:0,y:0,p:0.6},{x:0,y:1,p:0.1},{x:1,y:0,p:0.1},{x:1,y:1,p:0.2}];
function gaussian(x,y,rho){
  const u=x/2,v=y,q=1-rho*rho;
  return Math.exp(-(u*u-2*rho*u*v+v*v)/(2*q))/(4*Math.PI*Math.sqrt(q));
}
function loss(w,b){return (2*w+b-5)**2/2}
function step(w,b,rate){const error=2*w+b-5;return {w:w-rate*error*2,b:b-rate*error}}
function triangleProbability(t){return 2*t-t*t}
const api={joint,gaussian,loss,step,triangleProbability};
if(typeof module!=='undefined'&&module.exports)module.exports=api;
else globalThis.ProbabilityVisualMath=api;
})();

/* 爵士101 節奏遊戲：九種節奏，每關「聽、跟拍、猜」。全部用 WebAudio 現場合成，不載入音檔 */
(function(){
var RHY=window.RHY||[], BY={}; RHY.forEach(function(r){BY[r.id]=r});
var AC=window.AudioContext||window.webkitAudioContext, ctx=null, master=null, wet=null, bus=null;
function F(m){return 440*Math.pow(2,(m-69)/12)}
function init(){
  ctx=new AC(); master=ctx.createGain(); master.gain.value=.9;
  var lp=ctx.createBiquadFilter(); lp.type='lowpass'; lp.frequency.value=9000;
  var cp=ctx.createDynamicsCompressor(); cp.threshold.value=-14; cp.ratio.value=4;
  master.connect(lp); lp.connect(cp); cp.connect(ctx.destination);
  var cv=ctx.createConvolver(), len=ctx.sampleRate*1.6, ir=ctx.createBuffer(2,len,ctx.sampleRate);
  for(var c=0;c<2;c++){var d=ir.getChannelData(c);for(var i=0;i<len;i++)d[i]=(Math.random()*2-1)*Math.pow(1-i/len,3)}
  cv.buffer=ir; wet=ctx.createGain(); wet.gain.value=.13; wet.connect(cv); cv.connect(cp);
}
function out(n){n.connect(bus); n.connect(wet)}
var NB=null;function noiseBuf(){if(NB)return NB;var b=ctx.createBuffer(1,ctx.sampleRate*2,ctx.sampleRate),d=b.getChannelData(0);for(var i=0;i<d.length;i++)d[i]=Math.random()*2-1;return NB=b}
function noise(t,type,freq,q,v,dec,att){var s=ctx.createBufferSource();s.buffer=noiseBuf();var f=ctx.createBiquadFilter();f.type=type;f.frequency.value=freq;f.Q.value=q||1;var g=ctx.createGain();
  if(att){g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(v,t+att);g.gain.exponentialRampToValueAtTime(.0001,t+att+dec)}
  else{g.gain.setValueAtTime(v,t);g.gain.exponentialRampToValueAtTime(.0001,t+dec)}
  s.connect(f);f.connect(g);out(g);s.start(t);s.stop(t+(att||0)+dec+.05)}
function tone(t,type,fr,v,dec,fr2){var o=ctx.createOscillator(),g=ctx.createGain();o.type=type;o.frequency.setValueAtTime(fr,t);if(fr2)o.frequency.exponentialRampToValueAtTime(fr2,t+dec*.6);
  g.gain.setValueAtTime(v,t);g.gain.exponentialRampToValueAtTime(.0001,t+dec);o.connect(g);out(g);o.start(t);o.stop(t+dec+.03)}
var INS={
 piano:function(t,m,d,v){[1,2.003,3.01].forEach(function(h,k){var o=ctx.createOscillator(),g=ctx.createGain();o.type='sine';o.frequency.value=F(m)*h;
   var a=v*[1,.28,.08][k];g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(a,t+.008);g.gain.exponentialRampToValueAtTime(a*.3,t+.4);g.gain.exponentialRampToValueAtTime(.0001,t+d+.3);
   o.connect(g);out(g);o.start(t);o.stop(t+d+.35)})},
 epiano:function(t,m,d,v){var o=ctx.createOscillator(),o2=ctx.createOscillator(),g=ctx.createGain(),g2=ctx.createGain();o.type='sine';o2.type='sine';o.frequency.value=F(m);o2.frequency.value=F(m)*4.01;
   g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(v,t+.006);g.gain.exponentialRampToValueAtTime(v*.35,t+.5);g.gain.exponentialRampToValueAtTime(.0001,t+d+.25);
   g2.gain.setValueAtTime(v*.25,t);g2.gain.exponentialRampToValueAtTime(.0001,t+.12);o.connect(g);o2.connect(g2);out(g);out(g2);o.start(t);o2.start(t);o.stop(t+d+.3);o2.stop(t+.15)},
 gtr:function(t,m,d,v){var o=ctx.createOscillator(),f=ctx.createBiquadFilter(),g=ctx.createGain();o.type='triangle';o.frequency.value=F(m);f.type='lowpass';f.frequency.setValueAtTime(2600,t);f.frequency.exponentialRampToValueAtTime(700,t+.3);
   g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(v,t+.004);g.gain.exponentialRampToValueAtTime(.0001,t+Math.max(.25,d));o.connect(f);f.connect(g);out(g);o.start(t);o.stop(t+Math.max(.25,d)+.05)},
 bass:function(t,m,d,v){var o=ctx.createOscillator(),f=ctx.createBiquadFilter(),g=ctx.createGain();o.type='triangle';o.frequency.value=F(m);f.type='lowpass';f.frequency.setValueAtTime(1400,t);f.frequency.exponentialRampToValueAtTime(380,t+.25);
   g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(v,t+.01);g.gain.exponentialRampToValueAtTime(v*.45,t+.18);g.gain.exponentialRampToValueAtTime(.0001,t+d);o.connect(f);f.connect(g);out(g);o.start(t);o.stop(t+d+.05)},
 arco:function(t,m,d,v){var o=ctx.createOscillator(),f=ctx.createBiquadFilter(),g=ctx.createGain();o.type='sawtooth';o.frequency.value=F(m);f.type='lowpass';f.frequency.value=600;
   g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(v,t+d*.4);g.gain.exponentialRampToValueAtTime(.0001,t+d);o.connect(f);f.connect(g);out(g);o.start(t);o.stop(t+d+.05)},
 ride:function(t,m,d,v){noise(t,'highpass',7000,.7,v*.5,.45);tone(t,'square',5200,v*.03,.3)},
 hat:function(t,m,d,v){noise(t,'highpass',8000,.7,v*.35,.05)},
 ohat:function(t,m,d,v){noise(t,'highpass',7500,.7,v*.3,.22)},
 brush:function(t,m,d,v){noise(t,'bandpass',4500,.6,v*.4,.18)},
 snare:function(t,m,d,v){noise(t,'bandpass',1900,.8,v*.7,.16);tone(t,'sine',220,v*.4,.1,140)},
 rim:function(t,m,d,v){noise(t,'bandpass',3200,3,v*.6,.035);tone(t,'square',1650,v*.12,.04)},
 tom:function(t,m,d,v){tone(t,'sine',F(m),v,.3,F(m)*.6)},
 kick:function(t,m,d,v){tone(t,'sine',110,v,.25,42)},
 clave:function(t,m,d,v){tone(t,'sine',2500,v*.5,.06);tone(t,'triangle',2500*1.5,v*.12,.03)},
 bell:function(t,m,d,v){[540,812].forEach(function(fr){var o=ctx.createOscillator(),f=ctx.createBiquadFilter(),g=ctx.createGain();o.type='square';o.frequency.value=fr;f.type='bandpass';f.frequency.value=900;f.Q.value=2;
   g.gain.setValueAtTime(v*.25,t);g.gain.exponentialRampToValueAtTime(.0001,t+.22);o.connect(f);f.connect(g);out(g);o.start(t);o.stop(t+.25)})},
 conga:function(t,m,d,v){tone(t,'sine',F(m),v*.8,.22,F(m)*.92);noise(t,'bandpass',900,1,v*.15,.03)},
 slap:function(t,m,d,v){noise(t,'bandpass',1400,1.5,v*.6,.05);tone(t,'sine',F(m),v*.3,.06)},
 shaker:function(t,m,d,v){noise(t,'highpass',6000,.7,v*.22,.045,.012)},
 swell:function(t,m,d,v){noise(t,'highpass',5000,.5,v*.45,d*.45,d*.55)}
};
function E(a,i,b,n,d,v){a.push([i,b,n,d,v])}
function chord(a,i,b,ns,d,v){ns.forEach(function(n,k){E(a,i,b+k*.004,n,d,v)})}
/* ---- 九種節奏 ---- */
var P={
 swing:{bpm:150,meter:4,bars:2,sw:.67,grid:[0,.5],tgt:[1,3,5,7],make:function(){var a=[],k,b;
   for(b=0;b<8;b+=4){[0,1,1.5,2,3,3.5].forEach(function(x){E(a,'ride',b+x,0,0,x%1?.5:.85)});E(a,'hat',b+1,0,0,.9);E(a,'hat',b+3,0,0,.9)}
   [41,45,48,50,46,50,53,52].forEach(function(n,k){E(a,'bass',k,n,.9,.55)});
   chord(a,'piano',0,[57,63,67],.7,.12);chord(a,'piano',1.5,[57,63,67],.4,.1);chord(a,'piano',4,[56,62,65],.7,.12);chord(a,'piano',5.5,[56,62,65],.4,.1);
   return a}},
 twobeat:{bpm:184,meter:4,bars:2,sw:.6,grid:[0,.5],tgt:[0,2,4,6],make:function(){var a=[],b;
   [[36,43],[43,38]].forEach(function(p,bar){E(a,'bass',bar*4,p[0],1.4,.75);E(a,'bass',bar*4+2,p[1],1.4,.7)});
   [[52,55,57,60],[52,55,57,60],[53,55,59,62],[53,55,59,62]].forEach(function(c,k){chord(a,'piano',1+k*2,c,.35,.13)});
   for(b=1;b<8;b+=2)E(a,'brush',b,0,0,.7);for(b=0;b<8;b+=2)E(a,'brush',b,0,0,.3);
   [[0,72],[.5,74],[1,76],[2,79],[3,76],[4,74],[5.5,71],[6,72]].forEach(function(x){E(a,'piano',x[0],x[1],.4,.11)});
   return a}},
 shuffle:{bpm:92,meter:4,bars:2,sw:.5,grid:[0,1/3,2/3],tgt:[2/3,5/3,8/3,11/3,14/3,17/3,20/3,23/3],make:function(){var a=[],b;
   var line=[36,40,43,45,46,45,43,40];
   for(b=0;b<8;b++){E(a,'hat',b,0,0,.8);E(a,'hat',b+2/3,0,0,.55);E(a,'bass',b,line[b],.55,.6);E(a,'bass',b+2/3,line[b],.28,.45)}
   [1,3,5,7].forEach(function(x){E(a,'snare',x,0,0,.75)});[0,2,4,6].forEach(function(x){E(a,'kick',x,0,0,.8)});
   [1+2/3,3+2/3,5+2/3].forEach(function(x){chord(a,'piano',x,[58,64,67],.3,.12)});
   return a}},
 bossa:{bpm:132,meter:4,bars:2,sw:.5,grid:[0,.5],tgt:[0,1.5,3,5,6.5],make:function(){var a=[],b;
   [0,1.5,3,5,6.5].forEach(function(x){E(a,'rim',x,0,0,.9)});
   for(b=0;b<8;b+=.5)E(a,'shaker',b,0,0,b%1?.45:.7);
   [[0,41],[1.5,48],[2,48],[3.5,41],[4,43],[5.5,50],[6,50],[7.5,43]].forEach(function(x){E(a,'bass',x[0],x[1],x[0]%1?.4:1.3,.55)});
   var c1=[57,60,64,65],c2=[55,59,62,65];[0,1.5,2.5,3.5].forEach(function(x){chord(a,'gtr',x,c1,.4,.09)});[4.5,5.5,6.5,7].forEach(function(x){chord(a,'gtr',x,c2,.4,.09)});
   E(a,'kick',0,0,0,.4);E(a,'kick',4,0,0,.4);
   return a}},
 clave:{bpm:108,meter:4,bars:2,sw:.5,grid:[0,.5],tgt:[0,1.5,3,5,6],make:function(){var a=[],b;
   [0,1.5,3,5,6].forEach(function(x){E(a,'clave',x,0,0,1)});
   for(b=0;b<8;b++)E(a,'bell',b,0,0,b%2?.55:.8);
   for(b=0;b<8;b+=4){E(a,'slap',b+1,62,0,.6);E(a,'conga',b+3,60,0,.75);E(a,'conga',b+3.5,60,0,.75);E(a,'conga',b+2.5,64,0,.4)}
   [[1.5,41],[3,48],[5.5,43],[7,48]].forEach(function(x){E(a,'bass',x[0],x[1],1.4,.6)});
   var m=[65,69,72,69,65,69,72,74];m.forEach(function(n,k){E(a,'piano',k+.5,n,.35,.11);E(a,'piano',k+.5,n-12,.35,.08)});
   return a}},
 waltz:{bpm:168,meter:3,bars:2,sw:.67,grid:[0,.5],tgt:[0,3],make:function(){var a=[],b;
   for(b=0;b<6;b+=3){[0,1,1.5,2].forEach(function(x){E(a,'ride',b+x,0,0,x==0?.95:.55)});E(a,'hat',b+1,0,0,.6);E(a,'hat',b+2,0,0,.6)}
   E(a,'kick',0,0,0,.35);E(a,'kick',3,0,0,.35);
   [[0,39],[2,46],[3,36],[5,43]].forEach(function(x){E(a,'bass',x[0],x[1],x[0]%3?.9:1.8,.6)});
   chord(a,'piano',1,[55,58,62,65],.5,.11);chord(a,'piano',2,[55,58,62,65],.4,.09);chord(a,'piano',4,[51,55,58,63],.5,.11);chord(a,'piano',5,[51,55,58,63],.4,.09);
   [[0,75],[1,74],[1.5,72],[2,70],[3,72],[4,67]].forEach(function(x){E(a,'piano',x[0],x[1],.6,.13)});
   return a}},
 five:{bpm:172,meter:5,bars:2,sw:.67,grid:[0,.5],tgt:[0,3,5,8],make:function(){var a=[],b;
   for(b=0;b<10;b+=5){[0,1,1.5,2,3,4,4.5].forEach(function(x){E(a,'ride',b+x,0,0,x%1?.5:(x==0||x==3?.9:.65))});E(a,'snare',b+3,0,0,.35);E(a,'kick',b,0,0,.5)}
   for(b=0;b<10;b+=5){chord(a,'piano',b,[54,58,61,63],.9,.13);chord(a,'piano',b+1.5,[54,58,61,63],1,.11);chord(a,'piano',b+3,[53,56,61,63],.9,.13);chord(a,'piano',b+4,[53,56,61,63],.6,.1);
     E(a,'bass',b,39,1.4,.65);E(a,'bass',b+1.5,46,1.2,.45);E(a,'bass',b+3,34,.9,.65);E(a,'bass',b+4,41,.9,.5)}
   return a}},
 funk:{bpm:100,meter:4,bars:2,sw:.5,grid:[0,.25,.5,.75],tgt:[0,.75,2.5,4,4.75,6.5],make:function(){var a=[],b;
   for(b=0;b<8;b+=.25)E(a,'hat',b,0,0,b%.5?.4:.8);E(a,'ohat',7.5,0,0,.8);
   [1,3,5,7].forEach(function(x){E(a,'snare',x,0,0,1)});[1.75,3.25,5.75].forEach(function(x){E(a,'snare',x,0,0,.18)});
   [0,.75,2.5,4,4.75,6.5].forEach(function(x){E(a,'kick',x,0,0,1)});
   [[0,41,.5],[.75,41,.2],[1.5,53,.2],[2.5,44,.4],[3.5,46,.4],[4,41,.5],[4.75,41,.2],[5.5,53,.2],[6.5,48,.4],[7.25,51,.3]].forEach(function(x){E(a,'bass',x[0],x[1],x[2]*1.6,.7)});
   [1.5,3.5,5.5,7.5].forEach(function(x){chord(a,'epiano',x,[56,60,63,67],.3,.12)});
   return a}},
 free:{bpm:60,meter:0,bars:1,sw:.5,free:true,len:8,grid:[],tgt:[],make:function(){var a=[],t=0,k;
   E(a,'swell',Math.random()*1.5,0,2.5+Math.random()*2,.8);E(a,'swell',4+Math.random()*2,0,2+Math.random()*1.5,.6);
   t=Math.random()*.6;while(t<7.6){var r=Math.random();
     if(r<.35){var n=3+Math.floor(Math.random()*6),g=.18-Math.random()*.08;for(k=0;k<n;k++){E(a,Math.random()<.5?'tom':'snare',t,[45,41,38,48][k%4],0,.3+Math.random()*.5);t+=g*(1-k/(n*1.6))}}
     else if(r<.55){chord(a,'piano',t,[48,49,55,58,61,66].map(function(x){return x+Math.floor(Math.random()*12)}),.8,.1+Math.random()*.06)}
     else if(r<.7){E(a,'arco',t,28+Math.floor(Math.random()*14),1.2+Math.random()*1.4,.35)}
     else if(r<.85){E(a,'ride',t,0,0,.3+Math.random()*.6)}
     else E(a,'kick',t,0,0,.5);
     t+=.2+Math.random()*.9*(Math.random()<.3?2:1)}
   return a}}
};
/* ---- 時間 ---- */
function bt(p,b){if(p.free)return b;var w=Math.floor(b+1e-6),f=b-w;if(p.sw!=.5&&Math.abs(f-.5)<1e-6)f=p.sw;return w+f}
function loopBeats(p){return p.free?p.len:p.meter*p.bars}
function loopSec(p){return loopBeats(p)*60/p.bpm}
var cur=null,timer=null;
function sched(p,t0){var spb=60/p.bpm;p.make().forEach(function(e){INS[e[0]](t0+bt(p,e[1])*spb,e[2],Math.max(.05,e[3]*spb),e[4])});
  return p.tgt.map(function(b){return t0+bt(p,b)*spb})}
function tick(){if(!cur)return;var now=ctx.currentTime;
  while(cur.next<now+.4){var p=P[cur.id],ts=sched(p,cur.next);cur.loops.push(cur.next);if(cur.loops.length>6)cur.loops.shift();
    ts.forEach(function(t){cur.tgts.push({t:t,hit:null,loop:cur.n})});cur.n++;cur.next+=loopSec(p);
    if(cur.maxLoops&&cur.n>=cur.maxLoops){cur.next=1e9}}
  if(cur.onTick)cur.onTick(now)}
function play(id,opt){stop();if(!ctx)init();ctx.resume();bus=ctx.createGain();bus.gain.value=1;bus.connect(master);opt=opt||{};
  cur={id:id,next:ctx.currentTime+.12,loops:[],tgts:[],n:0,maxLoops:opt.maxLoops||0,onTick:opt.onTick,onEnd:opt.onEnd};
  tick();timer=setInterval(tick,40);
  return cur}
function stop(){if(!cur)return;clearInterval(timer);var b=bus,c=cur;cur=null;b.gain.setTargetAtTime(0,ctx.currentTime,.05);setTimeout(function(){b.disconnect()},500);if(c.onEnd)c.onEnd()}
function curEndTime(){if(!cur)return 0;var p=P[cur.id];return cur.loops.length?cur.loops[cur.loops.length-1]+loopSec(p):0}

/* ---- 節奏圈 ---- */
var cv=document.getElementById('wheel'),g2=cv.getContext('2d'),flashes=[],wheelId='swing',raf=null,breath=0;
var C={bg:'#172033',ring:'#2e3a52',dot:'#5d6880',beat:'#e9e5dc',tgt:'#d9a64e',good:'#f2efe9',off:'#c8695c',txt:'#8e93a0'};
function size(){var w=Math.min(cv.parentNode.clientWidth,window.innerWidth<600?300:420),r=window.devicePixelRatio||1;cv.style.width=w+'px';cv.style.height=w+'px';cv.width=w*r;cv.height=w*r;g2.setTransform(r,0,0,r,0,0);return w}
var W=size();window.addEventListener('resize',function(){W=size()});
function ang(p,beat){return -Math.PI/2+2*Math.PI*bt(p,beat)/loopBeats(p)}
function draw(){var p=P[wheelId],R=W*.38,cx=W/2,cy=W/2,now=ctx?ctx.currentTime:0;g2.clearRect(0,0,W,W);
  if(!p){g2.beginPath();g2.arc(cx,cy,R,0,Math.PI*2);g2.strokeStyle=C.ring;g2.lineWidth=3;g2.stroke();g2.fillStyle=C.txt;g2.font='300 '+Math.round(W*.16)+'px Inter,sans-serif';g2.textAlign='center';g2.textBaseline='middle';g2.fillText('?',cx,cy);raf=requestAnimationFrame(draw);return}
  var playing=cur&&cur.id===wheelId&&cur.loops.length;
  if(p.free){breath+=.02;g2.beginPath();for(var i=0;i<=120;i++){var a=i/120*Math.PI*2,rr=R*(1+(playing?.05:.02)*Math.sin(a*5+breath*3)*Math.sin(breath+i*.07));g2.lineTo(cx+Math.cos(a)*rr,cy+Math.sin(a)*rr)}
    g2.strokeStyle=C.ring;g2.lineWidth=3;g2.stroke();g2.fillStyle=C.txt;g2.font='500 15px '+getComputedStyle(document.body).fontFamily;g2.textAlign='center';g2.fillText('沒有固定的拍子',cx,cy+5)}
  else{g2.beginPath();g2.arc(cx,cy,R,0,Math.PI*2);g2.strokeStyle=C.ring;g2.lineWidth=3;g2.stroke();
    var lb=loopBeats(p),tg={};p.tgt.forEach(function(b){tg[b.toFixed(3)]=1});
    for(var b=0;b<lb;b++){p.grid.forEach(function(s){var bb=b+s,a=ang(p,bb),isB=s===0,isT=tg[bb.toFixed(3)],x=cx+Math.cos(a)*R,y=cy+Math.sin(a)*R;
      g2.beginPath();g2.arc(x,y,isT?(W*.03):(isB?W*.014:W*.008),0,Math.PI*2);g2.fillStyle=isT?C.tgt:(isB?C.beat:C.dot);g2.fill();
      if(isB){var bi=b%p.meter+1,xr=cx+Math.cos(a)*(R-W*.075),yr=cy+Math.sin(a)*(R-W*.075);g2.fillStyle=bi==1?C.beat:C.txt;g2.font=(bi==1?'700 ':'500 ')+Math.round(W*.038)+'px Inter,sans-serif';g2.textAlign='center';g2.textBaseline='middle';g2.fillText(bi,xr,yr)}})}
    if(p.bars>1)for(var k=0;k<p.bars;k++){var a0=ang(p,k*p.meter);g2.beginPath();g2.moveTo(cx+Math.cos(a0)*(R+W*.04),cy+Math.sin(a0)*(R+W*.04));g2.lineTo(cx+Math.cos(a0)*(R+W*.07),cy+Math.sin(a0)*(R+W*.07));g2.strokeStyle=C.txt;g2.lineWidth=2;g2.stroke()}
    if(playing){var L=null;for(var i=cur.loops.length-1;i>=0;i--)if(cur.loops[i]<=now){L=cur.loops[i];break}
      if(L!==null){var fr=(now-L)/loopSec(p),a=-Math.PI/2+fr*2*Math.PI;g2.beginPath();g2.moveTo(cx,cy);g2.lineTo(cx+Math.cos(a)*(R+W*.05),cy+Math.sin(a)*(R+W*.05));g2.strokeStyle='rgba(242,239,233,.85)';g2.lineWidth=2;g2.stroke();
        g2.beginPath();g2.arc(cx,cy,W*.012,0,Math.PI*2);g2.fillStyle=C.beat;g2.fill()}}}
  flashes=flashes.filter(function(f){return now-f.t<.6});flashes.forEach(function(f){var k=1-(now-f.t)/.6;g2.beginPath();g2.arc(cx+Math.cos(f.a)*R,cy+Math.sin(f.a)*R,W*.03+W*.05*(1-k),0,Math.PI*2);
    g2.strokeStyle=f.q==='off'||f.q==='extra'?C.off:(f.q==='perfect'?C.tgt:C.good);g2.globalAlpha=k;g2.lineWidth=3;g2.stroke();g2.globalAlpha=1});
  raf=requestAnimationFrame(draw)}
draw();

/* ---- 存檔 ---- */
var KEY='j101-rhythm-v1',SAVE={};try{SAVE=JSON.parse(localStorage.getItem(KEY)||'{}')||{}}catch(e){SAVE={}}
function save(){try{localStorage.setItem(KEY,JSON.stringify(SAVE))}catch(e){}}
var OFF=0;try{OFF=+(localStorage.getItem(KEY+'-off')||0)}catch(e){}
var offIn=document.getElementById('lat'),offOut=document.getElementById('latv');
if(offIn){offIn.value=OFF;offOut.textContent=OFF+' ms';offIn.addEventListener('input',function(){OFF=+offIn.value;offOut.textContent=OFF+' ms';try{localStorage.setItem(KEY+'-off',OFF)}catch(e){}})}
function lat(){return (ctx.outputLatency||0)+(ctx.baseLatency||0)+OFF/1000}

/* ---- 關卡介面 ---- */
var $=function(s,r){return (r||document).querySelector(s)},$$=function(s,r){return [].slice.call((r||document).querySelectorAll(s))};
var stage=$('#stage'),lv=null,step='listen',state={};
function stars(n){var s='';for(var i=0;i<3;i++)s+='<i class="'+(i<n?'on':'')+'" aria-hidden="true">★</i>';return '<span class="stars" aria-label="'+n+' 顆星">'+s+'</span>'}
function refreshMap(){$$('.lvl').forEach(function(a){var s=SAVE[a.dataset.id]||0;a.querySelector('.st').innerHTML=stars(s);a.classList.toggle('done',s>0);a.classList.toggle('cur',lv&&lv.id===a.dataset.id)});
  var tot=RHY.reduce(function(n,r){return n+(SAVE[r.id]||0)},0),done=RHY.filter(function(r){return SAVE[r.id]}).length;$('#tot').textContent=done+' / 9 關，'+tot+' 顆星'}
function open(id,noScroll){stop();lv=BY[id];wheelId=id;step='listen';state={};
  $('#lvnum').textContent='第 '+lv.n+' 關';$('#lvname').textContent=lv.name;$('#lven').textContent=lv.en;$('#lvone').textContent=lv.one;
  $('#lvfact').textContent=lv.fact;$('#lvsongs').innerHTML=lv.songs.map(function(s){return '<a href="https://music.apple.com/search?term='+encodeURIComponent(s[0]+' '+s[1])+'" target="_blank" rel="noopener">'+s[0]+'〈'+s[1]+'〉</a>'}).join('');
  $('#lvep').innerHTML=lv.ep?'<a href="short/ep'+lv.ep+'.html">相關的一分鐘故事：'+lv.eptitle+'</a>':'';
  stage.hidden=false;refreshMap();show('listen');if(!noScroll)stage.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'});
  if(!noScroll){try{history.replaceState(null,'','#'+id)}catch(e){}}}
function show(s){stop();step=s;$$('.steps button').forEach(function(b){var on=b.dataset.s===s;b.classList.toggle('on',on);b.setAttribute('aria-current',on?'step':'false')});
  $$('.pane').forEach(function(p){p.hidden=p.dataset.s!==s});$('#tapzone').hidden=s!=='tap';wheelId=lv.id;
  if(s==='listen'){$('#lslisten').textContent=lv.listen;setBtn($('#lplay'),false)}
  if(s==='tap'){$('#tapinfo').textContent=lv.tap;$('#tapfb').textContent='按「開始」，先聽一輪，金色的點亮起時再拍。';$('#tapres').hidden=true;$('#tstart').hidden=false;$('#tapcount').textContent=''}
  if(s==='guess')newGuess()}
function setBtn(b,on){b.classList.toggle('playing',on);b.querySelector('span').textContent=on?'停止':b.dataset.l;b.setAttribute('aria-pressed',on)}
$$('.steps button').forEach(function(b){b.addEventListener('click',function(){show(b.dataset.s)})});
$$('.lvl').forEach(function(a){a.addEventListener('click',function(ev){ev.preventDefault();open(a.dataset.id)})});
$('#lplay').addEventListener('click',function(){var b=this;if(cur){stop();setBtn(b,false);return}play(lv.id,{onEnd:function(){setBtn(b,false)}});setBtn(b,true)});
$('#tonext').addEventListener('click',function(){show('tap')});

/* 跟拍 */
var NEED=12,tap=null;
function startTap(){if(window.innerWidth<820)$('.rs-wheel').scrollIntoView({block:'start',behavior:'auto'});tap={P:0,G:0,O:0,M:0,X:0,n:0,taps:[]};$('#tstart').hidden=true;$('#tapres').hidden=true;
  if(lv.id==='free'){$('#tapfb').textContent='開始拍，拍十下。';play('free');$('#tapcount').textContent='0 / 10';return}
  $('#tapfb').textContent='先聽一輪……';
  play(lv.id,{onTick:function(now){var tt=now-lat();
    cur.tgts.forEach(function(g){if(g.loop===0){if(!g.cue&&g.t<=now+.02){g.cue=1}return}
      if(!g.done&&tt>g.t+.2){g.done=1;if(!g.hit){tap.M++;tap.n++;fb('miss')}else tap.n++}});
    if(cur.n>=1&&cur.loops.length&&now>=cur.loops[0]+loopSec(P[lv.id])-.05&&!tap.go){tap.go=1;$('#tapfb').textContent='開始拍！'}
    $('#tapcount').textContent=Math.min(tap.n,NEED)+' / '+NEED;
    if(tap.n>=NEED)endTap()}})}
function fb(q,ms){var t={perfect:'準！',good:'可以',miss:'沒拍到',extra:'多拍了一下'}[q]||(ms<0?'早了 ':'晚了 ')+Math.abs(Math.round(ms))+' ms';var el=$('#tapfb');el.textContent=t;el.className='tapfb q-'+q}
function doTap(){if(step!=='tap'||!tap||!cur)return;var now=ctx.currentTime,tt=now-lat();
  if(lv.id==='free'){tap.taps.push(tt);flashes.push({t:now,a:-Math.PI/2+Math.random()*Math.PI*2,q:'good'});var n=tap.taps.length;$('#tapcount').textContent=n+' / 10';
    if(n>=2){var d=Math.round((tap.taps[n-1]-tap.taps[n-2])*1000);$('#tapfb').textContent='這一下間隔 '+d+' ms';$('#tapfb').className='tapfb'}
    if(n>=10)endTap();return}
  if(!tap.go)return;var best=null,bd=1;cur.tgts.forEach(function(g){if(g.loop===0||g.hit||g.done)return;var d=Math.abs(tt-g.t);if(d<bd){bd=d;best=g}});
  var p=P[lv.id],L=cur.loops.length?cur.loops[cur.loops.length-1]:now;
  if(!best||bd>.25){tap.X++;fb('extra');flashes.push({t:now,a:-Math.PI/2+2*Math.PI*(((tt-cur.loops[0])/loopSec(p))%1),q:'extra'});return}
  var err=tt-best.t,q=Math.abs(err)<.06?'perfect':(Math.abs(err)<.12?'good':'off');best.hit=q;tap[q==='perfect'?'P':q==='good'?'G':'O']++;
  var bi=p.tgt[cur.tgts.indexOf(best)%p.tgt.length];flashes.push({t:now,a:ang(p,bi),q:q});if(q==='off')fb('off',err*1000);else fb(q)}
function endTap(){var t=tap;stop();var pct,msg;
  if(lv.id==='free'){var iv=[];for(var i=1;i<t.taps.length;i++)iv.push(t.taps[i]-t.taps[i-1]);var m=iv.reduce(function(a,b){return a+b},0)/iv.length,sd=Math.sqrt(iv.reduce(function(a,b){return a+(b-m)*(b-m)},0)/iv.length),cvv=Math.round(sd/m*100);
    pct=100;msg=cvv<12?'你的十下很穩，間隔只差大約 '+cvv+'%。可是音樂沒有給你拍子，這份穩定是你自己帶進來的。自由爵士的樂手也是這樣：各自帶著自己的脈動，一邊聽彼此。':'你的十下間隔忽長忽短，差了大約 '+cvv+'%。在前面八關，你的手會被拍子拉住；在這裡，沒有東西拉你。這就是自由爵士：樂手彼此聽，而不是一起數拍子。'}
  else{pct=Math.max(0,Math.round((2*t.P+t.G-t.X)/(2*NEED)*100));msg='準 '+t.P+'　可以 '+t.G+'　偏掉 '+t.O+'　沒拍到 '+t.M+(t.X?'　多拍 '+t.X:'')}
  state.tap=Math.max(state.tap||0,pct);var r=$('#tapres');r.hidden=false;
  $('#tappct').textContent=lv.id==='free'?'過關':pct+' 分';$('#tapmsg').textContent=msg;
  $('#tapverdict').textContent=lv.id==='free'?'':pct>=80?'很穩，這個節奏你已經抓到了。':pct>=55?'過關。再拍一次可以更穩。':'還差一點：先閉上眼睛只聽，跟著點頭，再試一次。';
  $('#tapnext').hidden=pct<55;$('#tstart').hidden=false;$('#tstart').querySelector('span').textContent='再拍一次';tap=null}
$('#tstart').addEventListener('click',startTap);
$('#tapbtn').addEventListener('pointerdown',function(e){e.preventDefault();doTap();this.classList.add('hit');var b=this;setTimeout(function(){b.classList.remove('hit')},90)});
document.addEventListener('keydown',function(e){if(step==='tap'&&(e.code==='Space'||e.key===' ')&&!e.repeat&&document.activeElement.tagName!=='INPUT'){e.preventDefault();doTap();var b=$('#tapbtn');b.classList.add('hit');setTimeout(function(){b.classList.remove('hit')},90)}});
$('#tapnext').addEventListener('click',function(){show('guess')});

/* 猜：A/B 哪一段是這關的節奏 */
function newGuess(){state.g={round:0,ok:0};nextRound()}
function nextRound(){var g=state.g;stop();g.round++;var others=RHY.filter(function(r){return r.id!==lv.id});var d=others[Math.floor(Math.random()*others.length)].id;
  g.ans=Math.random()<.5?'A':'B';g.A=g.ans==='A'?lv.id:d;g.B=g.ans==='B'?lv.id:d;g.answered=false;
  $('#gq').textContent='第 '+g.round+' / 3 題：A 和 B，哪一段是「'+lv.name+'」？';$('#gfb').textContent='兩段都可以先聽，再選。';$('#gfb').className='gfb';
  $$('.gans').forEach(function(b){b.disabled=false;b.classList.remove('right','wrong')});$('#gnext').hidden=true;$('#gres').hidden=true;$$('.gplay').forEach(function(b){setBtn(b,false)})}
$$('.gplay').forEach(function(b){b.addEventListener('click',function(){var w=b.dataset.w,g=state.g;var on=b.classList.contains('playing');stop();$$('.gplay').forEach(function(x){setBtn(x,false)});if(on)return;
  wheelId=g.answered?g[w]:'__hide';play(g[w],{onEnd:function(){setBtn(b,false)}});setBtn(b,true)})});
$$('.gans').forEach(function(b){b.addEventListener('click',function(){var g=state.g;if(g.answered)return;g.answered=true;var w=b.dataset.w,ok=w===g.ans;if(ok)g.ok++;
  b.classList.add(ok?'right':'wrong');$$('.gans').forEach(function(x){x.disabled=true});var other=BY[g.ans==='A'?g.B:g.A];
  $('#gfb').textContent=(ok?'答對。':'不是喔，是 '+g.ans+'。')+'另一段是「'+other.name+'」。';$('#gfb').className='gfb '+(ok?'q-perfect':'q-miss');
  if(g.round<3)$('#gnext').hidden=false;else endGuess()})});
$('#gnext').addEventListener('click',nextRound);
function endGuess(){var g=state.g,tp=state.tap||0,pass=g.ok>=2&&tp>=55,s=pass?1+(tp>=80?1:0)+(g.ok===3?1:0):0;
  if(s>(SAVE[lv.id]||0)){SAVE[lv.id]=s;save()}refreshMap();var r=$('#gres');r.hidden=false;
  var nx=RHY[lv.n]||null;
  $('#gresT').innerHTML=pass?'第 '+lv.n+' 關過關 '+stars(s):(tp<55?'猜對 '+g.ok+' / 3。跟拍還沒過關，回去再拍一次。':'猜對 '+g.ok+' / 3，要對兩題才過關。');
  $('#gresN').hidden=!nx;if(nx){$('#gresN').textContent='下一關：'+nx.name;$('#gresN').onclick=function(){open(nx.id)}}
  $('#gretry').onclick=function(){show(tp<55?'tap':'guess')}}

/* 總複習：九選一 */
var X=null,xo=$('#xopts');xo.innerHTML=RHY.map(function(r){return '<button data-id="'+r.id+'">'+r.name+'</button>'}).join('');
function xRound(){X.i++;var pool=RHY.map(function(r){return r.id}).filter(function(id){return id!==X.last});X.id=pool[Math.floor(Math.random()*pool.length)];X.last=X.id;X.done=false;
  $('#xq').textContent='第 '+X.i+' / 10 題：這是哪一種？';$('#xfb').textContent='';$$('#xopts button').forEach(function(b){b.disabled=false;b.classList.remove('right','wrong')});$('#xnext').hidden=true;
  wheelId='__hide';playX()}
function playX(){var b=$('#xplay');stop();play(X.id,{onEnd:function(){setBtn(b,false)}});setBtn(b,true)}
$('#xstart').addEventListener('click',function(){X={i:0,ok:0,last:null};$('#xbox').hidden=false;$('#xstart').hidden=true;$('#xend').hidden=true;xRound()});
$('#xplay').addEventListener('click',function(){if(cur){stop();return}playX()});
$$('#xopts button').forEach(function(b){b.addEventListener('click',function(){if(X.done)return;X.done=true;var ok=b.dataset.id===X.id;if(ok)X.ok++;b.classList.add(ok?'right':'wrong');
  $$('#xopts button').forEach(function(x){x.disabled=true;if(x.dataset.id===X.id)x.classList.add('right')});$('#xfb').textContent=ok?'答對。':'這段是「'+BY[X.id].name+'」。';
  if(X.i<10)$('#xnext').hidden=false;else{stop();$('#xend').hidden=false;$('#xstart').hidden=false;$('#xstart').querySelector('span').textContent='再考一次';
    $('#xendT').textContent='十題答對 '+X.ok+' 題。'+(X.ok>=9?'你的耳朵已經分得出爵士的九種走路方式。':X.ok>=6?'大部分都分得出來，錯的那幾種回去各聽一輪。':'先回到關卡，把每一關的「聽」多放幾輪。');
    try{if(X.ok>(SAVE.exam||0)){SAVE.exam=X.ok;save()}}catch(e){}}})});
$('#xnext').addEventListener('click',xRound);

if(/debug/.test(location.search))window.__rg={cur:function(){return cur},ctx:function(){return ctx},lat:function(){return lat()}};
refreshMap();var h=(location.hash||'').slice(1);open(BY[h]?h:'swing',true)
})();

/* 爵士101 和聲遊戲（由 build.py 產生：聲音引擎取自 rhythm.js） */
(function(){
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
/* ---- 和聲遊戲：九關，先聽、再考；畫面是五度圈。聲音引擎與節奏遊戲共用（build.py 把 rhythm.js 的合成段落接在前面） ---- */
var LV=window.HAR||[],BY={};LV.forEach(function(r){BY[r.id]=r});
var NM=['C','D♭','D','E♭','E','F','G♭','G','A♭','A','B♭','B'];
var QI={maj:[0,4,7],min:[0,3,7],maj7:[0,4,7,11],'7':[0,4,7,10],m7:[0,3,7,10]};
var QS={maj:'',min:'m',maj7:'maj7','7':'7',m7:'m7'};
function nm(pc,q){return NM[((pc%12)+12)%12]+(QS[q]||'')}
function vc(r,q){return QI[q].map(function(i){var n=48+((r+i)%12+12)%12;while(n<52)n+=12;while(n>71)n-=12;return n}).sort(function(a,b){return a-b})}
function bassN(r){return 36+((r%12)+12)%12-(((r%12)+12)%12>7?12:0)}
function rnd(a){return a[Math.floor(Math.random()*a.length)]}
/* 一串和弦 → 事件：[根音pc, 性質, 拍數] */
function prog(list,o){o=o||{};var a=[],mk=[],b=0;list.forEach(function(c){var r=c[0],q=c[1],L=c[2],v=vc(r,q),bn=bassN(r);
    if(o.comp&&L>=2){chord(a,'piano',b,v,1.2,.13);if(L>=4)chord(a,'piano',b+2.5,v,1,.1)}else chord(a,'piano',b,v,L*.92,.14);
    E(a,'bass',b,bn,Math.min(L,2)*.95,.6);if(L>=4)E(a,'bass',b+2,c[3]!=null?bassN(c[3]):bn+7,1.9,.5);
    mk.push([b,nm(r,q),((r%12)+12)%12]);b+=L});
  if(o.ride)for(var x=0;x<b;x++){E(a,'ride',x,0,0,.45);if(x%2)E(a,'ride',x+.5,0,0,.28);if(x%2)E(a,'hat',x,0,0,.4)}
  return {ev:a,mk:mk,beats:b,bpm:o.bpm||120,sw:.67}}
function triad(r,q){var a=[],v=vc(r,q);v.forEach(function(n,k){E(a,'piano',k*.5,n,.5,.15)});chord(a,'piano',1.75,v,2.2,.15);E(a,'bass',1.75,bassN(r),2.2,.45);
  return {ev:a,mk:[[0,nm(r,q),((r%12)+12)%12]],beats:4.5,bpm:96,sw:.5}}
function mode(r,iv,label){var a=[],seq=iv.concat(iv.slice(0,-1).reverse());E(a,'bass',0,bassN(r)-12+12,seq.length*.5+1,.45);E(a,'arco',0,bassN(r)+7,seq.length*.5+1,.2);
  seq.forEach(function(i,k){E(a,'piano',k*.5,60+((r%12)+12)%12+i-(r%12>7?12:0),.48,.17)});return {ev:a,mk:[[0,NM[((r%12)+12)%12]+' '+label,((r%12)+12)%12]],beats:seq.length*.5+1,bpm:116,sw:.5}}
var KEYS=[0,2,3,5,7,8,10];
function T(list,k){return list.map(function(c){return [c[0]+k,c[1],c[2],c[3]!=null?c[3]+k:null]})}
var BLUES=function(k,quick,bars){var I=[0,'7',4],IV=[5,'7',4];var L=[I,quick?IV:I,I,I,IV,IV,I,[9,'7',4],[2,'m7',4],[7,'7',4],I,[7,'7',4]].slice(0,bars||12);return prog(T(L,k),{ride:1,bpm:168,comp:1})};
var G={
 majmin:{demos:function(){return [['C 大三和弦',triad(0,'maj')],['C 小三和弦',triad(0,'min')]]},
  q:function(){var q=rnd(['maj','min']),r=rnd(KEYS);return {clip:triad(r,q),opts:['大三和弦（亮）','小三和弦（暗）'],ans:q=='maj'?0:1,why:'這是 '+nm(r,q)+(q=='maj'?'：中間那個音高半音，聽起來亮。':'：中間那個音低半音，聽起來暗。')}}},
 sevenths:{demos:function(){return [['Cmaj7 大七',triad(0,'maj7')],['C7 屬七',triad(0,'7')],['Cm7 小七',triad(0,'m7')]]},
  q:function(){var q=rnd(['maj7','7','m7']),r=rnd(KEYS);return {clip:triad(r,q),opts:['大七：穩','屬七：想走','小七：柔'],ans:['maj7','7','m7'].indexOf(q),why:'這是 '+nm(r,q)+'。'}}},
 iivi:{demos:function(){return [['二五一：回家',prog([[2,'m7',4],[7,'7',4],[0,'maj7',8]],{ride:1,comp:1})],['停在五級：還沒回家',prog([[2,'m7',4],[7,'7',4],[2,'m7',4],[7,'7',4]],{ride:1,comp:1})],['假回家：去了六級',prog([[2,'m7',4],[7,'7',4],[9,'m7',8]],{ride:1,comp:1})]]},
  q:function(){var k=rnd(KEYS),e=rnd(['home','home','vi','stay']),L=[[2,'m7',4],[7,'7',4]];
   L.push(e=='home'?[0,'maj7',8]:e=='vi'?[9,'m7',8]:[2,'m7',8]);
   return {clip:prog(T(L,k),{ride:1,comp:1}),opts:['回家了','還沒回家'],ans:e=='home'?0:1,why:e=='home'?'最後到了 '+nm(k,'maj7')+'，就是這個調的家。':(e=='vi'?'最後去了 '+nm(k+9,'m7')+'，像要回家卻開錯門。':'又回到 '+nm(k+2,'m7')+'，故事還沒講完。')}}},
 blues:{demos:function(){return [['爵士藍調（第 2 小節先換）',BLUES(5,true)],['基本藍調（第 5 小節才換）',BLUES(5,false)]]},
  q:function(){var k=rnd([5,10,0,7]),qk=Math.random()<.5;return {clip:BLUES(k,qk,6),opts:['第 2 小節就換了','第 5 小節才換'],ans:qk?0:1,why:'這是 '+NM[k]+' 藍調，'+(qk?'第 2 小節先跳到 '+nm(k+5,'7')+' 再回來。':'前四小節都停在 '+nm(k,'7')+'。')}}},
 secdom:{demos:function(){return [['原本：C → Am7 → Dm7 → G7 → C',prog([[0,'maj7',4],[9,'m7',4],[2,'m7',4],[7,'7',4],[0,'maj7',8]],{ride:1,comp:1})],['借來的屬七：C → A7 → Dm7 → G7 → C',prog([[0,'maj7',4],[9,'7',4],[2,'m7',4],[7,'7',4],[0,'maj7',8]],{ride:1,comp:1})]]},
  q:function(){var k=rnd(KEYS),s=Math.random()<.5;return {clip:prog(T([[0,'maj7',4],[9,s?'7':'m7',4],[2,'m7',4],[7,'7',4],[0,'maj7',8]],k),{ride:1,comp:1}),opts:['第二個是原本的小七','第二個是借來的屬七'],ans:s?1:0,why:'第二個和弦是 '+nm(k+9,s?'7':'m7')+(s?'：它把下一個 '+nm(k+2,'m7')+' 當成暫時的家，推了一把。':'：照調內原本的樣子走。')}}},
 modulate:{demos:function(){var P=[[0,'maj7',4],[9,'m7',4],[2,'m7',4],[7,'7',4]];return [['不轉調',prog(P.concat(P,[[0,'maj7',6]]),{ride:1,comp:1,bpm:132})],['第二遍升半音',prog(P.concat(T(P,1),[[1,'maj7',6]]),{ride:1,comp:1,bpm:132})],['第二遍升全音',prog(P.concat(T(P,2),[[2,'maj7',6]]),{ride:1,comp:1,bpm:132})]]},
  q:function(){var k=rnd(KEYS),u=rnd([0,1,2]),P=[[0,'maj7',4],[9,'m7',4],[2,'m7',4],[7,'7',4]];return {clip:prog(T(P,k).concat(T(P,k+u),[[k+u,'maj7',6]]),{ride:1,comp:1,bpm:132}),opts:['沒有轉調','升了半音','升了全音'],ans:u,
   why:u?'第二遍從 '+nm(k+u,'maj7')+' 開始，整個調'+(u==1?'升半音':'升全音')+'。':'兩遍都在 '+NM[(k+12)%12]+' 大調。'}}},
 modes:{demos:function(){return [['D Ionian（大調）',mode(2,[0,2,4,5,7,9,11,12],'Ionian')],['D Dorian',mode(2,[0,2,3,5,7,9,10,12],'Dorian')],['D Aeolian（小調）',mode(2,[0,2,3,5,7,8,10,12],'Aeolian')]]},
  q:function(){var r=rnd([0,2,4,7,9]),m=rnd([0,1,2]),IV=[[0,2,4,5,7,9,11,12],[0,2,3,5,7,9,10,12],[0,2,3,5,7,8,10,12]][m],nmL=['Ionian','Dorian','Aeolian'][m];
   return {clip:mode(r,IV,nmL),opts:['Ionian（大調）','Dorian','Aeolian（小調）'],ans:m,why:'這是 '+NM[r]+' '+nmL+'：'+['第三音高，一路明亮。','第三音低，但第六音高，暗中帶一點光。','第三、第六音都低，最暗。'][m]}}},
 tritone:{demos:function(){return [['原本：Dm7 → G7 → C',prog([[2,'m7',4,9],[7,'7',4,2],[0,'maj7',8]],{ride:1,comp:1})],['替代：Dm7 → D♭7 → C',prog([[2,'m7',4,9],[1,'7',4,8],[0,'maj7',8]],{ride:1,comp:1})]]},
  q:function(){var k=rnd(KEYS),s=Math.random()<.5;return {clip:prog(T([[2,'m7',4,9],[s?1:7,'7',4,s?8:2],[0,'maj7',8]],k),{ride:1,comp:1}),opts:['原本的五級屬七','三全音替代'],ans:s?1:0,why:'中間是 '+nm(k+(s?1:7),'7')+(s?'：低音 '+NM[(k+2)%12]+' → '+NM[(k+1)%12]+' → '+NM[k%12]+'，一路半音往下滑。':'：低音跳四度回家，最典型的走法。')}}},
 giant:{demos:function(){return [['三個調輪流跳（B、G、E♭）',prog([[11,'maj7',2],[2,'7',2],[7,'maj7',2],[10,'7',2],[3,'maj7',4],[9,'m7',2],[2,'7',2],[7,'maj7',2],[10,'7',2],[3,'maj7',2],[6,'7',2],[11,'maj7',4]],{ride:1,bpm:150})],['一直在同一個調',prog([[4,'m7',2],[9,'7',2],[2,'m7',2],[7,'7',2],[0,'maj7',4],[9,'m7',2],[2,'m7',2],[7,'7',2],[0,'maj7',4]],{ride:1,bpm:150})]]},
  q:function(){var k=rnd([0,2,5,7]),g=Math.random()<.5,L=g?[[11,'maj7',2],[2,'7',2],[7,'maj7',2],[10,'7',2],[3,'maj7',4],[9,'m7',2],[2,'7',2],[7,'maj7',4]]:[[4,'m7',2],[9,'7',2],[2,'m7',2],[7,'7',2],[0,'maj7',4],[9,'m7',2],[2,'m7',2],[0,'maj7',4]];
   return {clip:prog(T(L,k),{ride:1,bpm:150}),opts:['一直在同一個調','三個調輪流跳'],ans:g?1:0,why:g?'三個家相隔大三度，在五度圈上畫出一個三角形。':'全部繞著同一個家轉。'}}}
};
/* ---- 播放 ---- */
var cur=null,endT=null;
function play(clip,o){stop();if(!ctx)init();ctx.resume();bus=ctx.createGain();bus.gain.value=1;bus.connect(master);o=o||{};
  var t0=ctx.currentTime+.1,spb=60/clip.bpm,p={sw:clip.sw};
  clip.ev.forEach(function(e){var b=e[1],w=Math.floor(b+1e-6),f=b-w;if(p.sw!=.5&&Math.abs(f-.5)<1e-6)f=p.sw;INS[e[0]](t0+(w+f)*spb,e[2],Math.max(.05,e[3]*spb),e[4])});
  cur={clip:clip,t0:t0,spb:spb,reveal:o.reveal!==false,onEnd:o.onEnd,trail:[]};var c=cur;
  endT=setTimeout(function(){if(cur===c)stop()},(clip.beats*spb+.6)*1000)}
function stop(){if(!cur)return;clearTimeout(endT);var b=bus,c=cur;cur=null;b.gain.setTargetAtTime(0,ctx.currentTime,.05);setTimeout(function(){b.disconnect()},500);if(c.onEnd)c.onEnd()}
/* ---- 五度圈 ---- */
var cv=document.getElementById('wheel'),g2=cv.getContext('2d'),W=0,last=null;
var ORD=[0,7,2,9,4,11,6,1,8,3,10,5],LAB=['C','G','D','A','E','B','F♯','D♭','A♭','E♭','B♭','F'];
var C={ring:'#2e3a52',txt:'#a3a8b4',on:'#e0ae55',cream:'#f2efe9'};
function size(){var w=Math.min(cv.parentNode.clientWidth,window.innerWidth<600?300:420),r=window.devicePixelRatio||1;cv.style.width=w+'px';cv.style.height=w+'px';cv.width=w*r;cv.height=w*r;g2.setTransform(r,0,0,r,0,0);W=w}
size();window.addEventListener('resize',size);
function pos(pc,R){var i=ORD.indexOf(pc),a=-Math.PI/2+i*Math.PI/6;return [W/2+Math.cos(a)*R,W/2+Math.sin(a)*R]}
function draw(){var R=W*.38,cx=W/2,now=ctx?ctx.currentTime:0;g2.clearRect(0,0,W,W);
  g2.beginPath();g2.arc(cx,cx,R,0,Math.PI*2);g2.strokeStyle=C.ring;g2.lineWidth=2;g2.stroke();
  var on=null,lab='',hist=[];
  if(cur&&cur.reveal){cur.clip.mk.forEach(function(m){if(cur.t0+m[0]*cur.spb<=now)hist.push(m)});if(hist.length){on=hist[hist.length-1][2];lab=hist[hist.length-1][1]}}
  var tr=[];hist.forEach(function(m){if(!tr.length||tr[tr.length-1]!==m[2])tr.push(m[2])});tr=tr.slice(-5);
  for(var j=1;j<tr.length;j++){var p0=pos(tr[j-1],R),p1=pos(tr[j],R);g2.beginPath();g2.moveTo(p0[0],p0[1]);g2.lineTo(p1[0],p1[1]);g2.strokeStyle='rgba(224,174,85,'+(.25+.6*j/tr.length)+')';g2.lineWidth=3;g2.stroke()}
  ORD.forEach(function(pc,i){var p=pos(pc,R),isOn=pc===on;g2.beginPath();g2.arc(p[0],p[1],isOn?W*.06:W*.042,0,Math.PI*2);g2.fillStyle=isOn?C.on:'#1f2a40';g2.fill();
    g2.fillStyle=isOn?'#1d1408':C.txt;g2.font=(isOn?'700 ':'500 ')+Math.round(W*.042)+'px Inter,sans-serif';g2.textAlign='center';g2.textBaseline='middle';g2.fillText(LAB[i],p[0],p[1]+1)});
  g2.fillStyle=lab?C.cream:C.txt;g2.font=(lab?'600 ':'300 ')+Math.round(W*(lab&&lab.length>6?.075:.1))+'px Inter,sans-serif';g2.fillText(cur&&!cur.reveal?'?':(lab||'五度圈'),cx,cx);
  requestAnimationFrame(draw)}
draw();
/* ---- 存檔與介面 ---- */
var KEY='j101-harmony-v1',SAVE={};try{SAVE=JSON.parse(localStorage.getItem(KEY)||'{}')||{}}catch(e){SAVE={}}
function save(){try{localStorage.setItem(KEY,JSON.stringify(SAVE))}catch(e){}}
var $=function(s){return document.querySelector(s)},$$=function(s){return [].slice.call(document.querySelectorAll(s))};
var lv=null,Q=null,stage=$('#stage');
function stars(n){var s='';for(var i=0;i<3;i++)s+='<i class="'+(i<n?'on':'')+'" aria-hidden="true">★</i>';return '<span class="stars" aria-label="'+n+' 顆星">'+s+'</span>'}
function refreshMap(){$$('.lvl').forEach(function(a){var s=SAVE[a.dataset.id]||0;a.querySelector('.st').innerHTML=stars(s);a.classList.toggle('done',s>0);a.classList.toggle('cur',lv&&lv.id===a.dataset.id)});
  var tot=LV.reduce(function(n,r){return n+(SAVE[r.id]||0)},0),done=LV.filter(function(r){return SAVE[r.id]}).length;$('#tot').textContent=done+' / 9 關，'+tot+' 顆星'}
var PLAY='<svg viewBox="0 0 14 14" aria-hidden="true"><path d="M3 1.5v11l9-5.5z" fill="currentColor"/></svg>';
function setBtn(b,on){b.classList.toggle('playing',on);b.querySelector('span').textContent=on?'停止':b.dataset.l;b.setAttribute('aria-pressed',on)}
function open(id,noScroll){stop();lv=BY[id];$('#lvnum').textContent='第 '+lv.n+' 關';$('#lvname').textContent=lv.name;$('#lven').textContent=lv.en;$('#lvone').textContent=lv.one;
  $('#lvfact').textContent=lv.fact;$('#lvsongs').innerHTML=lv.songs.length?lv.songs.map(function(s){return '<a href="https://music.apple.com/search?term='+encodeURIComponent(s[0]+' '+s[1])+'" target="_blank" rel="noopener">'+s[0]+'〈'+s[1]+'〉</a>'}).join(''):'<span>聽任何一張爵士鋼琴三重奏，注意低音回家前的那一步。</span>';
  $('#lvep').innerHTML=lv.ep?'<a href="short/ep'+lv.ep+'.html">相關的一分鐘故事：'+lv.eptitle+'</a>':'';
  $('#lslisten').textContent=lv.listen;var box=$('#demos');box.innerHTML='';
  G[id].demos().forEach(function(d,i){var b=document.createElement('button');b.className='dplay';b.dataset.l=d[0];b.setAttribute('aria-pressed','false');b.innerHTML=PLAY+'<span>'+d[0]+'</span>';
    b.addEventListener('click',function(){var was=b.classList.contains('playing');$$('#demos .dplay').forEach(function(x){setBtn(x,false)});stop();if(was)return;var c=G[id].demos()[i][1];play(c,{onEnd:function(){setBtn(b,false)}});setBtn(b,true)});box.appendChild(b)});
  show('listen');refreshMap();if(!noScroll){stage.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'});try{history.replaceState(null,'','#'+id)}catch(e){}}}
function show(s){stop();$$('.steps button').forEach(function(b){var on=b.dataset.s===s;b.classList.toggle('on',on);b.setAttribute('aria-current',on?'step':'false')});$$('.pane').forEach(function(p){p.hidden=p.dataset.s!==s});
  $$('#demos .dplay').forEach(function(x){setBtn(x,false)});if(s==='quiz'){Q={i:0,ok:0};nextQ()}}
$$('.steps button').forEach(function(b){b.addEventListener('click',function(){show(b.dataset.s)})});
$$('.lvl').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();open(a.dataset.id)})});
$('#tonext').addEventListener('click',function(){show('quiz')});
var NQ=5;
function nextQ(){Q.i++;Q.cur=G[lv.id].q();Q.done=false;$('#hq').textContent='第 '+Q.i+' / '+NQ+' 題：'+lv.ask;$('#hfb').textContent='';$('#hfb').className='gfb';$('#hnext').hidden=true;$('#hres').hidden=true;
  var o=$('#hopts');o.innerHTML='';Q.cur.opts.forEach(function(t,k){var b=document.createElement('button');b.className='gans';b.textContent=t;b.addEventListener('click',function(){answer(k,b)});o.appendChild(b)});playQ()}
function playQ(){var b=$('#hplay');stop();play(Q.cur.clip,{reveal:Q.done,onEnd:function(){setBtn(b,false)}});setBtn(b,true)}
$('#hplay').addEventListener('click',function(){if(cur){stop();return}playQ()});
function answer(k,b){if(Q.done)return;Q.done=true;var ok=k===Q.cur.ans;if(ok)Q.ok++;$$('#hopts .gans').forEach(function(x,j){x.disabled=true;if(j===Q.cur.ans)x.classList.add('right')});if(!ok)b.classList.add('wrong');
  $('#hfb').textContent=(ok?'答對。':'不是喔。')+Q.cur.why+'　再按一次「再聽一次」，五度圈會亮給你看。';$('#hfb').className='gfb '+(ok?'q-perfect':'q-miss');
  if(Q.i<NQ)$('#hnext').hidden=false;else endQ()}
$('#hnext').addEventListener('click',nextQ);
function endQ(){var s=Q.ok>=5?3:Q.ok>=4?2:Q.ok>=3?1:0;if(s>(SAVE[lv.id]||0)){SAVE[lv.id]=s;save()}refreshMap();$('#hres').hidden=false;var nx=LV[lv.n]||null;
  $('#hresT').innerHTML=s?'第 '+lv.n+' 關過關 '+stars(s):'答對 '+Q.ok+' / '+NQ+'，要對三題才過關。回「聽」再比較幾次。';
  $('#hresN').hidden=!nx;if(nx){$('#hresN').textContent='下一關：'+nx.name;$('#hresN').onclick=function(){open(nx.id)}}$('#hretry').onclick=function(){show('quiz')}}
refreshMap();var h=(location.hash||'').slice(1);open(BY[h]?h:'majmin',true);

})();

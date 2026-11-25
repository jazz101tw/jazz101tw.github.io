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

function mel(ns,o){o=o||{};var a=[],b=0,mk=[];ns.forEach(function(x){var n=x[0],d=x[1]||1;if(n!=null)E(a,'piano',b,n,d*.9,.17);b+=d});
  if(o.drone!=null){E(a,'bass',0,o.drone,b,.3)}return {ev:a,mk:mk,beats:b+.5,bpm:o.bpm||100,sw:.5,vis:'keys',home:o.home}}
var MAJ=[0,2,4,5,7,9,11,12];
function scale(r,o){return mel(MAJ.map(function(i){return [60+r+i,.5]}),o)}
var KEYS=[0,2,3,5,7,8,10];
function T(list,k){return list.map(function(c){return [c[0]+k,c[1],c[2],c[3]!=null?c[3]+k:null]})}
var BLUES=function(k,quick,bars){var I=[0,'7',4],IV=[5,'7',4];var L=[I,quick?IV:I,I,I,IV,IV,I,[9,'7',4],[2,'m7',4],[7,'7',4],I,[7,'7',4]].slice(0,bars||12);return prog(T(L,k),{ride:1,bpm:168,comp:1})};
var G={
 keys12:{demos:function(){return [['十二個音一路往上',mel([60,61,62,63,64,65,66,67,68,69,70,71,72].map(function(n){return [n,.5]}))],['只彈白鍵：Do Re Mi',mel(MAJ.map(function(i){return [60+i,.5]}))]]},
  q:function(){var a=60+Math.floor(Math.random()*12),b=a;while(b===a)b=60+Math.floor(Math.random()*12);var c=mel([[a,1],[null,.25],[b,1]],{});return {clip:c,opts:['第一個比較高','第二個比較高'],ans:a>b?0:1,why:'第一個是 '+NM[a%12]+'，第二個是 '+NM[b%12]+'。'}}},
 home:{demos:function(){return [['回到家：停在 Do',mel([[64,.5],[65,.5],[67,1],[65,.5],[64,.5],[62,1],[60,2]],{home:60})],['沒到家：停在 Re',mel([[64,.5],[65,.5],[67,1],[65,.5],[64,.5],[60,1],[62,2]],{home:60})],['沒到家：停在 Ti',mel([[64,.5],[65,.5],[67,1],[65,.5],[64,.5],[62,1],[59,2]],{home:60})]]},
  q:function(){var r=rnd([0,2,5,7]),end=rnd([0,0,2,-1,7]),line=[[4,.5],[5,.5],[7,1],[5,.5],[4,.5],[2,1]];var c=mel(line.map(function(x){return [60+r+x[0],x[1]]}).concat([[60+r+end,2]]),{home:60+r});
   return {clip:c,opts:['結束了，回到家','還沒結束'],ans:end===0?0:1,why:end===0?'最後停在這個調的 Do，就是家。':'最後停在 '+({2:'Re','-1':'Ti',7:'Sol'})[end]+'，耳朵還在等下一個音。'}}},
 stack:{demos:function(){return [['Do、Mi、Sol 一個一個疊上去',{ev:[['piano',0,60,3,.15],['piano',1,64,2,.15],['piano',2,67,1,.15],['piano',3.2,60,2,.15],['piano',3.2,64,2,.15],['piano',3.2,67,2,.15]],mk:[[3.2,'C',0]],beats:5.5,bpm:90,sw:.5,vis:'keys'}],['Re、Fa、La：另一個和弦',{ev:[['piano',0,62,3,.15],['piano',1,65,2,.15],['piano',2,69,1,.15],['piano',3.2,62,2,.15],['piano',3.2,65,2,.15],['piano',3.2,69,2,.15]],mk:[[3.2,'Dm',2]],beats:5.5,bpm:90,sw:.5,vis:'keys'}]]},
  q:function(){var k=rnd([1,2,3]),r=60+rnd([0,2,4,5,7,9]),iv=[0,4,7].slice(0,k),a=[];iv.forEach(function(i){E(a,'piano',0,r+i,2,.15)});
   return {clip:{ev:a,mk:[],beats:3,bpm:90,sw:.5,vis:'keys'},opts:['一個音','兩個音','三個音（和弦）'],ans:k-1,why:'同時按下了 '+k+' 個音。'+(k===3?'三個音隔一個疊起來，就是一個和弦。':'')}}},
 circle:{demos:function(){var cyc=[0,7,2,9,4,11,6,1,8,3,10,5,0].map(function(r){return [r,'maj',1]});return [['C 大調音階',scale(0)],['G 大調音階：只多一個升 Fa',scale(7)],['沿著五度圈走一圈',(function(){var c=prog(cyc,{bpm:110});c.vis='circle';return c})()]]},
  q:function(){var r=rnd([0,7,5]),near=Math.random()<.5,r2=near?(r+rnd([7,5]))%12:(r+6)%12;var A=scale(r),B=scale(r2),off=A.beats;B.ev.forEach(function(e){A.ev.push([e[0],e[1]+off,e[2],e[3],e[4]])});A.beats+=B.beats;
   return {clip:A,opts:['隔壁的調（只差一個音）','很遠的調'],ans:near?0:1,why:'第一段是 '+NM[r]+' 大調，第二段是 '+NM[r2]+' 大調'+(near?'，在五度圈上是隔壁，只差一個音。':'，在五度圈的正對面，差了六個音。')}}},
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
function drawKeys(now){var lo=55,hi=79,wk=[],x=0,kw=W/15,top=W*.3,h=W*.4;g2.clearRect(0,0,W,W);
  var on={},home=cur&&cur.clip.home;if(cur&&cur.reveal!==false)cur.clip.ev.forEach(function(e){if(e[0]!=='piano')return;var t=cur.t0+e[1]*cur.spb;if(now>=t&&now<t+Math.max(.25,e[3]*cur.spb))on[e[2]]=1});
  var WH=[0,2,4,5,7,9,11],pos={};for(var n=lo;n<=hi;n++)if(WH.indexOf(n%12)>=0){pos[n]=x;x+=kw}
  var off=(W-x)/2;Object.keys(pos).forEach(function(n){n=+n;var xx=off+pos[n];g2.fillStyle=on[n]?'#e0ae55':(n===home?'#3a4660':'#f2efe9');g2.fillRect(xx+1,top,kw-2,h);
    if(n%12===0){g2.fillStyle=on[n]?'#1d1408':'#6e6e73';g2.font='500 '+Math.round(W*.03)+'px Inter,sans-serif';g2.textAlign='center';g2.fillText(n===60?'C4':'C',xx+kw/2,top+h-W*.03)}});
  for(n=lo;n<=hi;n++)if(WH.indexOf(n%12)<0&&pos[n-1]!=null){var xx2=off+pos[n-1]+kw*.68;g2.fillStyle=on[n]?'#e0ae55':'#111722';g2.fillRect(xx2,top,kw*.64,h*.6)}
  var lab='';if(cur&&cur.reveal!==false&&cur.clip.mk.length){cur.clip.mk.forEach(function(m){if(cur.t0+m[0]*cur.spb<=now)lab=m[1]})}
  g2.fillStyle=cur&&cur.reveal===false?'#a3a8b4':'#f2efe9';g2.font='600 '+Math.round(W*.09)+'px Inter,sans-serif';g2.textAlign='center';g2.textBaseline='middle';g2.fillText(cur&&cur.reveal===false?'?':(lab||(home?'家＝'+NM[home%12]:'')),W/2,W*.17);
  requestAnimationFrame(draw)}
function draw(){var now=ctx?ctx.currentTime:0;if((cur&&cur.clip.vis==='keys')||(!cur&&lv&&lv.vis==='keys'))return drawKeys(now);var R=W*.38,cx=W/2;g2.clearRect(0,0,W,W);
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
  var tot=LV.reduce(function(n,r){return n+(SAVE[r.id]||0)},0),done=LV.filter(function(r){return SAVE[r.id]}).length;$('#tot').textContent=done+' / '+LV.length+' 關，'+tot+' 顆星'}
var PLAY='<svg viewBox="0 0 14 14" aria-hidden="true"><path d="M3 1.5v11l9-5.5z" fill="currentColor"/></svg>';
function setBtn(b,on){b.classList.toggle('playing',on);b.querySelector('span').textContent=on?'停止':b.dataset.l;b.setAttribute('aria-pressed',on)}
function open(id,noScroll){stop();lv=BY[id];$('#lvnum').textContent='第 '+lv.n+' 關';$('#lvname').textContent=lv.name;$('#lven').textContent=lv.en;$('#lvone').textContent=lv.one;
  $('#lvfact').textContent=lv.fact;$('#lvsongs').parentNode.hidden=!lv.songs.length;$('#lvsongs').innerHTML=lv.songs.length?lv.songs.map(function(s){return '<a href="https://music.apple.com/search?term='+encodeURIComponent(s[0]+' '+s[1])+'" target="_blank" rel="noopener">'+s[0]+'〈'+s[1]+'〉</a>'}).join(''):'';
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
refreshMap();var h=(location.hash||'').slice(1);open(BY[h]?h:'keys12',true);

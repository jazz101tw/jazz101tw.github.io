/* 爵士101 換伴奏（由 build.py 產生：聲音引擎取自 rhythm.js） */
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
/* ---- 換伴奏：同一段旋律，五種伴奏，播放中可以隨時切換（下一小節生效）。聲音引擎取自 rhythm.js ---- */
var SONGS=window.SONGS||[],STY=window.STY||[],SB={},YB={};SONGS.forEach(function(s){SB[s.id]=s});STY.forEach(function(s){YB[s.id]=s});
var NM=['C','D♭','D','E♭','E','F','G♭','G','A♭','A','B♭','B'];
var QI={maj:[0,4,7],min:[0,3,7],maj7:[0,4,7,11],'6':[0,4,7,9],'7':[0,4,7,10],m7:[0,3,7,10],m7b5:[0,3,6,10]};
var QS={maj:'',min:'m',maj7:'maj7','6':'6','7':'7',m7:'m7',m7b5:'m7♭5'};
var RO={I:0,ii:2,iii:4,IV:5,V:7,vi:9,II7:2,I7:0,iv:5,VI7:9,III7:4};
/* 羅馬數字 → [根音, 性質]，依風格 */
function chordOf(ro,sty){var r=RO[ro];
  if(sty==='pop'){return [r,{I:'maj',ii:'min',iii:'min',IV:'maj',V:'maj',vi:'min',II7:'7',I7:'maj',iv:'min',VI7:'7',III7:'7'}[ro]]}
  if(sty==='minor'){return {I:[0,'min'],ii:[2,'m7b5'],iii:[3,'maj'],IV:[5,'min'],V:[7,'7'],vi:[8,'maj'],II7:[2,'m7b5'],I7:[0,'min'],iv:[5,'min'],VI7:[8,'maj'],III7:[7,'7']}[ro]}
  if(sty==='blues'){return [r,'7']}
  return [r,{I:'6',ii:'m7',iii:'m7',IV:'maj7',V:'7',vi:'m7',II7:'7',I7:'7',iv:'m7',VI7:'7',III7:'7'}[ro]]}
function cname(c){return NM[(c[0]+12)%12]+QS[c[1]]}
/* 爵士、巴薩：五級前面插二級；停很久的一級，最後兩拍變成屬七推向下一個 */
function reharm(ch){var out=[];ch.forEach(function(c,i){var nx=ch[i+1];
  if(c[0]==='V'&&c[1]>=2){out.push(['ii',c[1]/2]);out.push(['V',c[1]/2])}
  else if(c[0]==='I'&&c[1]>=4&&nx&&nx[0]==='IV'){out.push(['I',c[1]-2]);out.push(['I7',2])}
  else out.push(c)});return out}
function vc(c){return QI[c[1]].map(function(i){var n=48+((c[0]+i)%12+12)%12;while(n<53)n+=12;while(n>70)n-=12;return n}).sort(function(a,b){return a-b})}
function bassN(r){r=(r%12+12)%12;return 36+r-(r>7?12:0)}
/* 一首歌 × 一種風格 → 事件 [樂器, 拍, 音, 長度, 力度]，加上和弦標記 */
function arrange(song,sty){var a=[],mk=[],M=song.meter,b=song.pick||0;
  var mel=[],t=0;song.mel.forEach(function(x){if(x[0]!=null){var p=60+x[0];
      if(sty==='minor'){var d=((x[0]%12)+12)%12;if(d===4||d===9)p-=1}
      mel.push([t,p,x[1]])}t+=x[1]});
  var total=Math.max(t,song.ch.reduce(function(s,c){return s+c[1]},0)+(song.pick?0:0));
  mel.forEach(function(m){E(a,sty==='minor'||sty==='bossa'?'epiano':'piano',m[0],m[1]+12*(sty==='bossa'?0:0),m[2]*.92,sty==='bossa'?.2:.2);a[a.length-1].mel=1});
  var ch=(sty==='jazz'||sty==='bossa')?reharm(song.ch):song.ch;var cb=song.chStart||0;
  ch.forEach(function(c,i){var cc=chordOf(c[0],sty),L=c[1],v=vc(cc),bn=bassN(cc[0]),nx=ch[i+1]?chordOf(ch[i+1][0],sty):cc;mk.push([cb,cname(cc),v]);
    var k;
    if(sty==='pop'){for(k=0;k<L;k++){chord(a,'piano',cb+k,v,.9,k%2?.07:.09)}E(a,'bass',cb,bn,Math.min(L,2)*.95,.6);if(L>=3&&M===4)E(a,'bass',cb+2,bn+7,1.9,.5)}
    if(sty==='minor'){for(k=0;k<L*2;k++){E(a,'piano',cb+k/2,v[k%v.length]-(k%v.length===0?0:0),.9,.08)}E(a,'arco',cb,bn,L*.95,.35)}
    if(sty==='jazz'){for(k=0;k<L;k++){var wb=k===0?bn:(k===L-1?bassN(nx[0])+(Math.random()<.5?1:-1):bn+[0,QI[cc[1]][1],7,QI[cc[1]][2]][k%4]);E(a,'bass',cb+k,wb,.95,.6)}
      chord(a,'piano',cb+(L>=2?1.5:0),v,.6,.09);if(L>=4)chord(a,'piano',cb+3,v,.4,.07)}
    if(sty==='bossa'){E(a,'bass',cb,bn,1.4,.55);if(L>=2)E(a,'bass',cb+1.5,bn+7,.5,.45);if(L>=4){E(a,'bass',cb+2,bn+7,1.4,.5);E(a,'bass',cb+3.5,bn,.5,.4)}
      [0,1.5,2.5,3.5].forEach(function(x){if(x<L)chord(a,'gtr',cb+x,v,.4,.08)})}
    if(sty==='blues'){var line=[0,4,7,9,10,9,7,4];for(k=0;k<L;k++){E(a,'bass',cb+k,bn+line[(k*2)%8],.55,.55);E(a,'bass',cb+k+2/3,bn+line[(k*2+1)%8],.3,.42)}
      for(k=0;k<L;k++)if(k%2)chord(a,'piano',cb+k+2/3,v,.3,.09)}
    cb+=L});
  var end=Math.max(total,cb),x;
  for(x=0;x<end;x++){var bi=((x-(song.pick||0))%M+M)%M;
    if(sty==='pop'){if(M===4){if(bi%2===0)E(a,'kick',x,0,0,.45);else E(a,'snare',x,0,0,.3)}else if(bi===0)E(a,'kick',x,0,0,.45);else E(a,'hat',x,0,0,.35)}
    if(sty==='jazz'){if(M===3){[0,1,1.5,2].forEach(function(y){if(bi===Math.floor(y))E(a,'ride',x+y-Math.floor(y),0,0,y===0?.7:.45)});if(bi)E(a,'hat',x,0,0,.4)}
      else{E(a,'ride',x,0,0,.55);if(bi%2){E(a,'ride',x+.5,0,0,.35);E(a,'hat',x,0,0,.5)}}}
    if(sty==='bossa'){E(a,'shaker',x,0,0,.5);E(a,'shaker',x+.5,0,0,.3);var bp=((x-(song.pick||0))%(M*2)+M*2)%(M*2);[0,1.5,3,5,6.5].forEach(function(y){if(Math.floor(y)===bp)E(a,'rim',x+y-Math.floor(y),0,0,.6)})}
    if(sty==='blues'){E(a,'hat',x,0,0,.6);E(a,'hat',x+2/3,0,0,.4);if(bi%2)E(a,'snare',x,0,0,.6);else E(a,'kick',x,0,0,.6)}}
  return {ev:a,mk:mk,beats:end,sw:sty==='jazz'?.67:.5}}
/* ---- 播放：逐拍排程，換風格在下一小節生效 ---- */
var cur=null,timer=null;
function bt(b,sw){var w=Math.floor(b+1e-6),f=b-w;if(sw!==.5&&Math.abs(f-.5)<1e-6)f=sw;return w+f}
function play(songId,sty,o){stop();if(!ctx)init();ctx.resume();bus=ctx.createGain();bus.gain.value=1;bus.connect(master);o=o||{};
  var s=SB[songId];cur={song:s,sty:sty,next:sty,arr:{},t0:ctx.currentTime+.15,spb:60/s.bpm,pos:0,bar:0,once:!!o.once,onEnd:o.onEnd,reveal:o.reveal!==false,shown:[]};
  cur.arr[sty]=arrange(s,sty);tick();timer=setInterval(tick,40);return cur}
function A(st){if(!cur.arr[st])cur.arr[st]=arrange(cur.song,st);return cur.arr[st]}
function tick(){if(!cur)return;var now=ctx.currentTime,M=cur.song.meter,pk=cur.song.pick||0;
  while(cur.t0+cur.pos*cur.spb<now+.35){var p=cur.pos,ar=A(cur.sty);
    if(p>=ar.beats){if(cur.once){var c=cur;setTimeout(function(){if(cur===c)stop()},(ar.beats*cur.spb-(now-cur.t0))*1000+700);cur.pos=1e9;break}
      cur.t0+=ar.beats*cur.spb+cur.spb*(M===3?0:0);cur.pos=0;cur.arr={};ar=A(cur.sty);p=0}
    if(((p-pk)%M+M)%M===0&&cur.next!==cur.sty){cur.sty=cur.next;ar=A(cur.sty)}
    var sw=ar.sw;ar.ev.forEach(function(e){if(e[1]>=p&&e[1]<p+1){INS[e[0]](cur.t0+bt(e[1],sw)*cur.spb,e[2],Math.max(.05,e[3]*cur.spb),e[4]);if(e.mel)cur.shown.push([cur.t0+bt(e[1],sw)*cur.spb,e[2],e[3]*cur.spb,1])}});
    ar.mk.forEach(function(m){if(m[0]>=p&&m[0]<p+1)cur.shown.push([cur.t0+m[0]*cur.spb,m,0,0,cur.sty])});
    cur.pos+=1}
  if(cur.shown.length>200)cur.shown=cur.shown.slice(-120)}
function stop(){if(!cur)return;clearInterval(timer);var b=bus,c=cur;cur=null;b.gain.setTargetAtTime(0,ctx.currentTime,.05);setTimeout(function(){b.disconnect()},500);if(c.onEnd)c.onEnd()}
/* ---- 鍵盤畫面 ---- */
var cv=document.getElementById('wheel'),g2=cv.getContext('2d'),W=0,H=0;
function size(){var w=Math.min(cv.parentNode.clientWidth,560),r=window.devicePixelRatio||1;W=w;H=Math.round(w*.62);cv.style.width=w+'px';cv.style.height=H+'px';cv.width=w*r;cv.height=H*r;g2.setTransform(r,0,0,r,0,0)}
size();window.addEventListener('resize',size);
var WH=[0,2,4,5,7,9,11];
function draw(){var now=ctx?ctx.currentTime:0;g2.clearRect(0,0,W,H);var lo=53,hi=79,pos={},x=0,n,kw;
  for(n=lo;n<=hi;n++)if(WH.indexOf(n%12)>=0){pos[n]=x;x++}kw=W/x;var top=H*.34,h=H*.6;
  var chordNotes=[],melNote=null,lab='',sty=null;
  if(cur&&cur.reveal){cur.shown.forEach(function(s){if(s[0]<=now){if(s[3])melNote=(now<s[0]+Math.max(.15,s[2]))?s[1]:melNote;else{lab=cname2(s[1]);chordNotes=s[1][2];sty=s[4]}}})}
  var cs={};(chordNotes||[]).forEach(function(q){cs[q]=1});
  Object.keys(pos).forEach(function(k){k=+k;var xx=pos[k]*kw;g2.fillStyle=k===melNote?'#7fb3d5':(cs[k]?'#e0ae55':'#f2efe9');g2.fillRect(xx+1,top,kw-2,h);
    if(k%12===0){g2.fillStyle='#6e6e73';g2.font='500 '+Math.round(kw*.45)+'px Inter,sans-serif';g2.textAlign='center';g2.fillText('C',xx+kw/2,top+h-kw*.4)}});
  for(n=lo;n<=hi;n++)if(WH.indexOf(n%12)<0&&pos[n-1]!=null){var x2=(pos[n-1]+.68)*kw;g2.fillStyle=n===melNote?'#7fb3d5':(cs[n]?'#e0ae55':'#111722');g2.fillRect(x2,top,kw*.64,h*.6)}
  g2.textAlign='center';g2.textBaseline='middle';
  if(cur&&!cur.reveal){g2.fillStyle='#a3a8b4';g2.font='300 '+Math.round(H*.2)+'px Inter,sans-serif';g2.fillText('?',W/2,H*.16)}
  else{g2.fillStyle='#f2efe9';g2.font='600 '+Math.round(H*.16)+'px Inter,sans-serif';g2.fillText(lab||' ',W/2,H*.16)}
  requestAnimationFrame(draw)}
function cname2(m){return m[1]}
draw();
/* ---- 介面 ---- */
var $=function(s){return document.querySelector(s)},$$=function(s){return [].slice.call(document.querySelectorAll(s))};
var song=SONGS[0].id,sty='pop';
function setSong(id){song=id;$$('.songs button').forEach(function(b){b.classList.toggle('on',b.dataset.id===id);b.setAttribute('aria-pressed',b.dataset.id===id)});$('#sname').textContent=SB[id].name;$('#snote').textContent=SB[id].note;if(cur){var s=cur.sty;stop();play(id,s,{onEnd:onEnd});setPlay(true)}}
function setSty(id){sty=id;$$('.stys button').forEach(function(b){b.classList.toggle('on',b.dataset.id===id);b.setAttribute('aria-pressed',b.dataset.id===id)});$('#styname').textContent=YB[id].name;$('#stydesc').textContent=YB[id].desc;if(cur)cur.next=id}
function setPlay(on){var b=$('#pp');b.classList.toggle('playing',on);b.querySelector('span').textContent=on?'停止':'播放';b.setAttribute('aria-pressed',on)}
function onEnd(){setPlay(false)}
$$('.songs button').forEach(function(b){b.addEventListener('click',function(){setSong(b.dataset.id)})});
$$('.stys button').forEach(function(b){b.addEventListener('click',function(){setSty(b.dataset.id);if(!cur){play(song,sty,{onEnd:onEnd});setPlay(true)}})});
$('#pp').addEventListener('click',function(){if(cur){stop();return}play(song,sty,{onEnd:onEnd});setPlay(true)});
/* 小考：聽伴奏猜風格 */
var X=null;$('#xopts').innerHTML=STY.map(function(s){return '<button data-id="'+s.id+'">'+s.name+'</button>'}).join('');
function xRound(){X.i++;X.song=SONGS[Math.floor(Math.random()*SONGS.length)].id;var pool=STY.map(function(s){return s.id}).filter(function(i){return i!==X.last});X.sty=pool[Math.floor(Math.random()*pool.length)];X.last=X.sty;X.done=false;
  $('#xq').textContent='第 '+X.i+' / 10 題：〈'+SB[X.song].name+'〉這次是哪一種伴奏？';$('#xfb').textContent='';$$('#xopts button').forEach(function(b){b.disabled=false;b.classList.remove('right','wrong')});$('#xnext').hidden=true;playX()}
function playX(){var b=$('#xplay');stop();play(X.song,X.sty,{once:true,reveal:false,onEnd:function(){b.classList.remove('playing');b.querySelector('span').textContent='再聽一次'}});b.classList.add('playing');b.querySelector('span').textContent='停止'}
$('#xstart').addEventListener('click',function(){X={i:0,ok:0,last:null};$('#xbox').hidden=false;$('#xstart').hidden=true;$('#xend').hidden=true;xRound();document.getElementById('xbox').scrollIntoView({block:'nearest'})});
$('#xplay').addEventListener('click',function(){if(cur){stop();return}playX()});
$$('#xopts button').forEach(function(b){b.addEventListener('click',function(){if(X.done)return;X.done=true;var ok=b.dataset.id===X.sty;if(ok)X.ok++;
  $$('#xopts button').forEach(function(x){x.disabled=true;if(x.dataset.id===X.sty)x.classList.add('right')});if(!ok)b.classList.add('wrong');
  $('#xfb').textContent=(ok?'答對。':'這次是「'+YB[X.sty].name+'」。')+YB[X.sty].hint;
  if(X.i<10)$('#xnext').hidden=false;else{stop();$('#xend').hidden=false;$('#xstart').hidden=false;$('#xstart').querySelector('span').textContent='再考一次';
   $('#xendT').textContent='十題答對 '+X.ok+' 題。'+(X.ok>=9?'你的耳朵已經分得出伴奏的顏色了，可以去玩和聲遊戲的基礎關。':X.ok>=6?'大部分都對了。錯的那幾種，回上面同一首歌切換著多聽幾次。':'回上面挑一首熟的歌，五種伴奏輪流切，聽它們差在哪。')}})});
$('#xnext').addEventListener('click',xRound);
setSong(song);setSty(sty);

})();

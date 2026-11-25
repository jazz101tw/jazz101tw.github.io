"""爵士101 網站產生器 v4（故事加長＋入門路線＋聽懂爵士＋樂手＋小辭典＋時間軸＋選品）
用法：python3 build.py [Substack網址]
輸出位置預設 jimframe-site/jazz/；設 JAZZ_OUT=/路徑 可改輸出到獨立 repo"""
import os, sys, json, html, shutil, random
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
OUT = os.environ.get('JAZZ_OUT') or os.path.join(ROOT, 'jazz')
sys.path.insert(0, HERE)
from stories import S
from extras import PEOPLE, WORDS, TIMELINE, START, BRANCH, SHOP, ERAS, HALLS, TL_MORE

IMGSRC = os.path.join(HERE, 'img')
META = json.load(open(os.path.join(IMGSRC, 'meta.json'), encoding='utf-8')) if os.path.exists(os.path.join(IMGSRC, 'meta.json')) else {}
PHOTO = {'village-vanguard-1961': 'village', 'koln-concert': 'koln', 'sonny-rollins-bridge': 'rollins',
         'van-gelder-living-room': 'vangelder', 'giant-steps': 'coltrane', 'real-book': None}
PHOTO2 = {'sonny-rollins-bridge': 'bridge', 'village-vanguard-1961': 'evans'}
PPH = {'bill-evans': 'evans', 'john-coltrane': 'coltrane', 'keith-jarrett': 'koln', 'sonny-rollins': 'rollins'}   # 文中第二張照片
for s in S:
    n = sum(len(x) for _, ps in s['sections'] for x in ps) + sum(len(a) + len(b) for a, b in s['listen'])
    s['chars'] = n
    s['read'] = f"{max(2, round(n / 400))} 分鐘"
    k = PHOTO.get(s['slug']); s['ph'] = META.get(k) if k else None
    k2 = PHOTO2.get(s['slug']); s['ph2'] = META.get(k2) if k2 else None
BYSLUG = {s['slug']: s for s in S}
PBY = {p[0]: p for p in PEOPLE}
WBY = {w[0]: w for w in WORDS}

SUB = sys.argv[1] if len(sys.argv) > 1 else ''
IG = 'https://www.instagram.com/jazz101tw/'
SUB_HREF = SUB or IG
SUB_TXT = '免費訂閱' if SUB else '先追蹤 IG，電子報開放時通知你'
COMING = json.load(open(os.path.join(HERE, 'coming.json'), encoding='utf-8'))
e = html.escape

# 示範說明：id → (標題, 說明, 聽什麼, [選項])
DEMOS = {
 'swing': ('搖擺：同一段旋律，直的和搖的', '兩個八分音符平均分，聽起來像進行曲；第一個拉長、第二個縮短，就開始搖了。', '切換兩種，注意你的頭什麼時候開始想跟著點。', ['直的', '搖擺']),
 'walking': ('走路低音：貝斯一步一步走', '貝斯可以只彈每小節的兩個音，也可以一拍一個音往下一個和弦走。', '聽「走路」的時候，整首歌是不是突然往前推了？', ['兩拍', '走路']),
 'blues': ('十二小節藍調：爵士的母語', '十二個小節為一輪，三組和弦反覆循環。幾乎所有爵士樂手都會彈。', '跟著亮起來的格子數，第 5 小節和第 9 小節和弦會換，聽得出來嗎？', ['慢', '快']),
 'bluescale': ('藍調音階：那幾個「歪」的音', '一般的大調音階很明亮；藍調音階多了降三、降五、降七，一下子就有了憂傷。', '比較兩種，哪一種讓你想到深夜的酒吧？', ['大調音階', '藍調音階']),
 'iivi': ('二五一：一句話的起、承、合', '從 Dm7 到 G7 再到 Cmaj7，耳朵會覺得「回到家了」。', '切到「不回家」，G7 之後又回到 Dm7，你會一直等那個家。', ['回到家', '不回家']),
 'giant': ('Giant Steps：三個調不停跳', 'Coltrane 在 B、G、降 E 三個調之間快速跳動，每個和弦只停一兩拍。', '先用慢速聽和弦怎麼換，再切到接近原速，想像要在上面即興。', ['慢速', '接近原速']),
 'comping': ('伴奏：鋼琴什麼時候插話', '鋼琴在獨奏後面伴奏，可以每拍都彈，也可以挑空隙回一句。', '聽「挑空隙」的版本，鋼琴是不是比較像在跟旋律聊天？', ['每拍都彈', '挑空隙']),
 'trading': ('交換四小節：你一句、我一句', '薩克斯風吹四小節，鼓手接著即興四小節，輪流對話。', '每次聽旋律都會不一樣，因為它是現場隨機即興的。', []),
 'motif': ('主題式即興：同一句話換五種說法', 'Sonny Rollins 常拿一小段旋律反覆變化。這裡把同一句話用五種方式說一次。', '跟著格子看：移高、晚半拍、只留前半、尾巴加長。', []),
 'vamp': ('反覆段：一直轉的左手', '左手不斷重複同樣的節奏，右手在上面慢慢長出旋律，就像《The Köln Concert》那樣。', '右手每一輪都是隨機的，左手永遠一樣。聽久了會有一點催眠。', []),
}
DEMO_ORDER = ['swing', 'walking', 'blues', 'bluescale', 'iivi', 'comping', 'trading', 'motif', 'giant', 'vamp']

def demo_card(i, small=False):
    t, d, h, opts = DEMOS[i]
    o = ''.join(f'<button data-o="{k}" class="{"on" if k == 0 else ""}" aria-pressed="{"true" if k == 0 else "false"}">{e(x)}</button>' for k, x in enumerate(opts))
    return (f'<div class="demo{" sm" if small else ""}" data-demo="{i}" id="d-{i}"><div class="dtop"><h3>{e(t)}</h3><p>{e(d)}</p></div>'
            f'<div class="dctl"><button class="dplay" aria-pressed="false"><svg viewBox="0 0 14 14" aria-hidden="true"><path d="M3 1.5v11l9-5.5z" fill="currentColor"/></svg><span>播放</span></button>'
            f'{"<div class=opts>" + o + "</div>" if opts else ""}</div><div class="cells" aria-hidden="true"></div><p class="hint">{e(h)}</p></div>')

CSS = r"""
:root{
  --paper:#ffffff; --ink:#1d1d1f; --graphite:#6e6e73; --hair:#e3e1dc;
  --brass:#a97a2b; --midnight:#172033; --lamp:#f5ebdd; --wash:#faf8f4;
  --font:"Inter",-apple-system,BlinkMacSystemFont,"PingFang TC","Noto Sans TC",sans-serif;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --paper:#121417; --ink:#f2f1ee; --graphite:#a1a1a6; --hair:#2a2d33; --brass:#d2a24e; --midnight:#0c111c; --lamp:#3a2f22; --wash:#181b20;}}
:root[data-theme="dark"]{--paper:#121417; --ink:#f2f1ee; --graphite:#a1a1a6; --hair:#2a2d33; --brass:#d2a24e; --midnight:#0c111c; --lamp:#3a2f22; --wash:#181b20;}
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-text-size-adjust:100%}
body{background:var(--paper);color:var(--ink);font-family:var(--font);font-size:17px;line-height:1.75;-webkit-font-smoothing:antialiased;overflow-x:hidden}
a{color:inherit}
:focus-visible{outline:2px solid var(--brass);outline-offset:3px;border-radius:6px}
img{display:block;max-width:100%}

/* nav */
.nav{position:sticky;top:0;z-index:20;background:color-mix(in srgb,var(--paper) 78%,transparent);backdrop-filter:saturate(180%) blur(20px);-webkit-backdrop-filter:saturate(180%) blur(20px);border-bottom:1px solid var(--hair)}
.nav .in{max-width:1000px;margin:0 auto;padding:0 22px;height:52px;display:flex;align-items:center;justify-content:space-between}
.brand{font-weight:600;font-size:17px;text-decoration:none;letter-spacing:-.01em}
.nav nav a{font-size:13px;color:var(--graphite);text-decoration:none;margin-left:22px}
.nav nav a:hover{color:var(--ink)}

/* hero */
.hero{text-align:center;padding:84px 22px 40px;position:relative;overflow:hidden}
.hero h1 .nw{display:inline-block;white-space:nowrap}
.hero h1{font-size:clamp(30px,7.4vw,72px);line-height:1.12;font-weight:700;letter-spacing:-.02em}
.hero p{font-size:clamp(18px,2.6vw,22px);color:var(--graphite);margin:18px auto 0;max-width:30em;line-height:1.6}
.ctas{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:30px}
.btn{display:inline-block;background:var(--ink);color:var(--paper);text-decoration:none;font-size:16px;padding:12px 24px;border-radius:999px;font-weight:500}
.btn.alt{background:transparent;color:var(--brass);padding:12px 6px}
.btn.alt:hover{text-decoration:underline}

/* the record */
.stage{position:relative;margin:34px auto 0;width:min(600px,90vw);aspect-ratio:1.18/1;border-radius:28px;
  background:linear-gradient(135deg,rgba(255,255,255,.10),transparent 40%),repeating-linear-gradient(91deg,rgba(0,0,0,.05) 0 2px,transparent 2px 11px,rgba(255,255,255,.035) 11px 13px,transparent 13px 23px),linear-gradient(100deg,#5e3f25,#4a301b 45%,#5a3b22);
  box-shadow:0 50px 90px -40px rgba(60,35,10,.65),inset 0 1px 0 rgba(255,255,255,.18)}
.glow{position:absolute;left:50%;top:58%;width:min(900px,140vw);height:min(900px,140vw);transform:translate(-50%,-50%);background:radial-gradient(closest-side,var(--lamp),transparent 70%);z-index:-1;pointer-events:none}
.platter{position:absolute;top:7%;bottom:7%;left:5%;aspect-ratio:1/1;border-radius:50%;background:#151515;box-shadow:0 40px 80px -30px rgba(20,16,10,.55),0 0 0 10px #232323;z-index:1}
.disc{position:absolute;inset:0;border-radius:50%;
  background:
   radial-gradient(circle at 50% 50%,transparent 0 31%,rgba(255,255,255,.04) 31.3% 31.6%,transparent 32%),
   repeating-radial-gradient(circle at 50% 50%,#101010 0 1.6px,#1b1b1b 1.6px 3.2px),
   #121212}
.disc:after{content:"";position:absolute;inset:0;border-radius:50%;background:conic-gradient(from 210deg,transparent 0 12%,rgba(255,255,255,.10) 16%,transparent 22% 62%,rgba(255,255,255,.07) 66%,transparent 72%)}
.label{position:absolute;inset:34%;border-radius:50%;background:radial-gradient(circle at 50% 50%,#121212 0 4%,var(--brass) 4.5% 100%);display:grid;place-items:center;text-align:center;color:#20170a}
.label b{font-size:clamp(11px,2vw,15px);font-weight:700;letter-spacing:.02em;display:block;margin-bottom:26%}
.label span{font-size:clamp(9px,1.5vw,11px);display:block}
.spin .disc{animation:spin 1.8s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.arm{position:absolute;right:6%;top:8%;width:9%;height:62%;z-index:2;transform-origin:50% 8%;transform:rotate(-18deg);transition:transform 1.1s cubic-bezier(.3,.7,.2,1)}
.arm:before{content:"";position:absolute;left:50%;top:0;width:34px;height:34px;margin-left:-17px;border-radius:50%;background:#d9d6cf;box-shadow:inset 0 0 0 6px #bdb9b0}
.arm i{position:absolute;left:50%;top:6%;width:5px;height:90%;margin-left:-2.5px;background:linear-gradient(#e7e4dd,#bdb9b0);border-radius:3px}
.arm i:after{content:"";position:absolute;bottom:-14px;left:-7px;width:19px;height:26px;background:#2b2b2b;border-radius:4px}
.spin .arm{transform:rotate(6deg)}
.play{position:relative;z-index:3;display:inline-flex;align-items:center;gap:10px;margin-top:26px;background:none;border:1px solid var(--hair);color:var(--ink);font:inherit;font-size:15px;padding:10px 20px;border-radius:999px;cursor:pointer}
.play:hover{border-color:var(--brass)}
.play svg{width:14px;height:14px}
.playnote{font-size:13px;color:var(--graphite);margin-top:10px}
@media (prefers-reduced-motion:reduce){.spin .disc{animation:none}.arm{transition:none}}

/* featured band */
.band{background:var(--midnight);color:#f2efe9;margin-top:90px}
.band .in{max-width:1000px;margin:0 auto;padding:80px 22px;display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center}
@media (max-width:760px){.band .in{grid-template-columns:1fr;gap:28px;padding:56px 22px}}
.band figure img{border-radius:18px;aspect-ratio:4/5;object-fit:cover;width:100%;filter:sepia(.18) saturate(.9)}
.band figcaption,.credit{font-size:11px;color:#8e93a0;margin-top:8px;line-height:1.5}
.band small{color:var(--brass);font-size:14px}
.band h2{font-size:clamp(28px,4.4vw,44px);line-height:1.2;font-weight:700;letter-spacing:-.015em;margin:10px 0 16px}
.band p{color:#b9bdc7;font-size:17px}
.band .btn{background:#f2efe9;color:#172033;margin-top:26px}
.yearbig{font-size:clamp(64px,10vw,112px);font-weight:200;letter-spacing:-.04em;line-height:1;color:var(--brass)}

/* list */
.wrap{max-width:1000px;margin:0 auto;padding:0 22px}
.sec{padding:96px 0 20px}
.sec h2{font-size:clamp(30px,4.6vw,48px);font-weight:700;letter-spacing:-.02em;line-height:1.15}
.sec .lede{color:var(--graphite);font-size:19px;margin-top:10px;max-width:34em}
.list{margin-top:36px;border-top:1px solid var(--hair)}
.row{display:grid;grid-template-columns:120px 1fr 120px;gap:24px;align-items:center;padding:26px 0;border-bottom:1px solid var(--hair);text-decoration:none}
.row .y{font-size:40px;font-weight:200;letter-spacing:-.03em;color:var(--graphite);transition:color .2s}
.row h3{font-size:21px;font-weight:600;line-height:1.4;letter-spacing:-.01em}
.row p{color:var(--graphite);font-size:15px;line-height:1.65;margin-top:4px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.row .t{width:120px;aspect-ratio:1/1;border-radius:12px;object-fit:cover;filter:sepia(.15)}
.row .t.empty{background:radial-gradient(circle,#111 0 3%,var(--c,#a97a2b) 3.5% 30%,#161616 31% 100%);border-radius:50%;box-shadow:inset 0 0 0 1px #000}
.row:hover .y{color:var(--brass)}
.row:hover h3{text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:4px}
@media (max-width:640px){.row{grid-template-columns:1fr 84px;gap:14px}.row .y{grid-column:1/-1;font-size:28px;margin-bottom:-12px}.row .t{width:84px}}
.soon{columns:2;column-gap:40px;margin-top:30px;list-style:none}
@media (max-width:640px){.soon{columns:1}}
.soon li{break-inside:avoid;color:var(--graphite);font-size:15px;padding:9px 0;border-bottom:1px solid var(--hair)}

/* newsletter */
.letter{text-align:center;padding:110px 22px;background:var(--wash);margin-top:90px}
.letter h2{font-size:clamp(30px,5vw,52px);font-weight:700;letter-spacing:-.02em;line-height:1.15}
.letter p{color:var(--graphite);font-size:19px;max-width:28em;margin:16px auto 28px}

footer{max-width:1000px;margin:0 auto;padding:30px 22px 60px;font-size:12px;color:var(--graphite);border-top:1px solid var(--hair);line-height:1.8}

/* article */
.ahead{max-width:720px;margin:0 auto;padding:72px 22px 30px;text-align:center}
.ahead .yearbig{color:var(--brass)}
.ahead h1{font-size:clamp(30px,5.6vw,50px);font-weight:700;line-height:1.2;letter-spacing:-.02em;margin-top:18px}
.ahead .dek{color:var(--graphite);font-size:20px;line-height:1.65;margin-top:18px}
.ahead .rt{font-size:14px;color:var(--graphite);margin-top:18px}
.hero-img{max-width:1000px;margin:20px auto 0;padding:0 22px}
.hero-img img{width:100%;max-height:560px;object-fit:cover;border-radius:22px;filter:sepia(.15) saturate(.92)}
.hero-img .credit{color:var(--graphite);text-align:right}
.body{max-width:660px;margin:0 auto;padding:30px 22px 0;font-size:18px;line-height:1.95}
.body h2{font-size:26px;font-weight:700;letter-spacing:-.01em;margin:56px 0 14px;line-height:1.35}
.body p{margin-bottom:22px}
.tracks{max-width:660px;margin:60px auto 0;padding:0 22px}
.tracks h2,.more h2{font-size:26px;font-weight:700;margin-bottom:6px}
.tracks .sub{color:var(--graphite);font-size:15px;margin-bottom:18px}
.tr{display:grid;grid-template-columns:34px 1fr;gap:14px;padding:18px 0;border-top:1px solid var(--hair)}
.tr .n{font-size:15px;color:var(--brass);font-weight:600;padding-top:2px}
.tr b{font-weight:600;font-size:18px}
.tr p{color:var(--graphite);font-size:15px;line-height:1.7;margin-top:2px}
.tr a{font-size:13px;color:var(--brass);text-decoration:none;margin-right:14px}
.tr a:hover{text-decoration:underline}
.more{max-width:660px;margin:56px auto 0;padding:0 22px}
.more ul{list-style:none}
.more li{padding:12px 0;border-top:1px solid var(--hair);font-size:16px}
.src{max-width:660px;margin:40px auto 0;padding:0 22px;font-size:13px;color:var(--graphite)}
.pn{max-width:660px;margin:50px auto 0;padding:0 22px;display:grid;grid-template-columns:1fr 1fr;gap:16px}
.pn a{text-decoration:none;font-size:16px;font-weight:600;line-height:1.45}
.pn a small{display:block;font-weight:400;font-size:13px;color:var(--graphite);margin-bottom:4px}
.pn a:last-child{text-align:right}
@media (max-width:520px){.pn{grid-template-columns:1fr}.pn a:last-child{text-align:left}}
"""

PLAYER = r"""
(function(){
  var btn=document.getElementById('play'); if(!btn) return;
  var stage=document.getElementById('stage'), ctx=null, playing=false, timer=null, master=null;
  // ii–V–I in C（Dm9 → G13 → Cmaj9 → A7b9），搖擺八分音符的低音
  var prog=[[50,53,57,60,64],[43,53,57,59,64],[48,52,55,59,62],[45,49,55,58,61]];
  var bass=[[38,41,45,43],[31,35,38,40],[36,40,43,45],[33,37,40,43]];
  function f(m){return 440*Math.pow(2,(m-69)/12)}
  function note(m,t,d,v,type){
    var o=ctx.createOscillator(),g=ctx.createGain(),o2=ctx.createOscillator(),g2=ctx.createGain();
    o.type=type||'sine';o.frequency.value=f(m);o2.type='sine';o2.frequency.value=f(m)*2.002;
    g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(v,t+.012);g.gain.exponentialRampToValueAtTime(v*.35,t+.35);g.gain.exponentialRampToValueAtTime(.0001,t+d);
    g2.gain.setValueAtTime(v*.25,t);g2.gain.exponentialRampToValueAtTime(.0001,t+.5);
    o.connect(g);o2.connect(g2);g.connect(master);g2.connect(master);o.start(t);o2.start(t);o.stop(t+d+.05);o2.stop(t+.6);
  }
  function brush(t){var n=ctx.createBufferSource(),b=ctx.createBuffer(1,ctx.sampleRate*.12,ctx.sampleRate),d=b.getChannelData(0);
    for(var i=0;i<d.length;i++)d[i]=(Math.random()*2-1)*(1-i/d.length);
    var hp=ctx.createBiquadFilter();hp.type='highpass';hp.frequency.value=5000;var g=ctx.createGain();g.gain.value=.05;
    n.buffer=b;n.connect(hp);hp.connect(g);g.connect(master);n.start(t);}
  function bar(t,i){var beat=60/112,sw=beat*2/3;
    prog[i].forEach(function(m,k){note(m,t+k*.012,beat*3.6,.06)});
    prog[i].forEach(function(m){note(m,t+beat*2+sw,beat*1.2,.035)});
    bass[i].forEach(function(m,k){note(m,t+k*beat,beat*.95,.16,'triangle')});
    for(var k=0;k<4;k++){brush(t+k*beat);brush(t+k*beat+sw*.5+beat*.5)}}
  function loop(){var t=ctx.currentTime+.05,len=60/112*4;for(var i=0;i<4;i++)bar(t+i*len,i);timer=setTimeout(loop,len*4*1000-60)}
  btn.addEventListener('click',function(){
    if(!ctx){ctx=new (window.AudioContext||window.webkitAudioContext)();master=ctx.createGain();master.gain.value=.9;
      var lp=ctx.createBiquadFilter();lp.type='lowpass';lp.frequency.value=3800;master.disconnect();master.connect(lp);lp.connect(ctx.destination);}
    playing=!playing;
    if(playing){ctx.resume();master.gain.setTargetAtTime(.9,ctx.currentTime,.05);loop();stage.classList.add('spin');btn.setAttribute('aria-pressed','true');btn.querySelector('span').textContent='停下來';btn.querySelector('path').setAttribute('d','M3 1.5h3v11H3zM8 1.5h3v11H8z');}
    else{clearTimeout(timer);master.gain.setTargetAtTime(0,ctx.currentTime,.15);stage.classList.remove('spin');btn.setAttribute('aria-pressed','false');btn.querySelector('span').textContent='放一段二五一';btn.querySelector('path').setAttribute('d','M3 1.5v11l9-5.5z');
      setTimeout(function(){if(!playing){ctx.close();ctx=null}},600);}
  });
})();
"""

CSS2 = r"""
/* nav v4 */
.nav .in{gap:18px}
.nav nav{display:flex;overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch;min-width:0}
.nav nav::-webkit-scrollbar{display:none}
.nav nav a{white-space:nowrap;margin-left:0;margin-right:20px;padding:4px 0}
.nav nav a.cur{color:var(--ink)}
@media (max-width:640px){.nav .in{height:auto;flex-direction:column;align-items:stretch;padding:10px 22px 0;gap:4px}.nav nav{padding-bottom:8px}}
/* doors */
.doors{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--hair);border:1px solid var(--hair);border-radius:20px;overflow:hidden;margin-top:40px}
.doors a{background:var(--paper);padding:26px 22px 24px;text-decoration:none;display:block}
.doors a:hover{background:var(--wash)}
.doors b{display:block;font-size:19px;font-weight:600;margin-bottom:4px}
.doors span{display:block;color:var(--graphite);font-size:14px;line-height:1.6}
.doors i{font-style:normal;color:var(--brass);font-size:13px;display:block;margin-top:12px}
@media (max-width:760px){.doors{grid-template-columns:1fr 1fr}}
@media (max-width:420px){.doors{grid-template-columns:1fr}}
.more-link{display:inline-block;margin-top:26px;color:var(--brass);text-decoration:none;font-size:16px}
.more-link:hover{text-decoration:underline}
/* demo */
.demo{background:var(--wash);border-radius:22px;padding:28px 26px 24px;margin-top:20px}
.band .demo{background:rgba(255,255,255,.05);color:#f2efe9}
.dtop h3{font-size:20px;font-weight:600;line-height:1.4}
.dtop p{color:var(--graphite);font-size:15px;margin-top:4px;line-height:1.7}
.band .dtop p,.band .hint{color:#b9bdc7}
.dctl{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-top:18px}
.dplay{display:inline-flex;align-items:center;gap:9px;background:var(--ink);color:var(--paper);border:0;font:inherit;font-size:15px;padding:10px 20px;border-radius:999px;cursor:pointer}
.band .dplay{background:#f2efe9;color:#172033}
.dplay svg{width:13px;height:13px}
.dplay.playing{background:var(--brass);color:#1d1408}
.opts{display:inline-flex;background:var(--paper);border:1px solid var(--hair);border-radius:999px;padding:3px}
.band .opts{background:transparent;border-color:#2e3a52}
.opts button{background:none;border:0;font:inherit;font-size:14px;color:var(--graphite);padding:7px 14px;border-radius:999px;cursor:pointer}
.opts button.on{background:var(--ink);color:var(--paper)}
.band .opts button.on{background:#f2efe9;color:#172033}
.cells{display:grid;grid-template-columns:repeat(auto-fill,minmax(64px,1fr));gap:6px;margin-top:18px}
.cells.notes{grid-template-columns:repeat(auto-fill,minmax(42px,1fr))}
.cell{font-size:13px;text-align:center;padding:10px 4px;border-radius:10px;border:1px solid var(--hair);color:var(--graphite);transition:background .08s,color .08s;font-variant-numeric:tabular-nums;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.band .cell{border-color:#2e3a52;color:#8e93a0}
.cell.on{background:var(--brass);border-color:var(--brass);color:#1d1408}
.hint{font-size:14px;color:var(--graphite);margin-top:14px}
.demos{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:36px}
.demos .demo{margin-top:0}
@media (max-width:760px){.demos{grid-template-columns:1fr}}
/* article v4 */
.facts{max-width:660px;margin:34px auto 0;padding:0 22px}
.facts dl{display:grid;grid-template-columns:auto 1fr;border-top:1px solid var(--hair)}
.facts dt,.facts dd{padding:11px 0;border-bottom:1px solid var(--hair);font-size:15px}
.facts dt{color:var(--graphite);padding-right:22px;white-space:nowrap}
.pull{font-size:clamp(22px,3.4vw,28px);line-height:1.55;font-weight:600;letter-spacing:-.01em;color:var(--brass);margin:44px 0;padding-left:20px;border-left:3px solid var(--brass)}
.body figure{margin:36px -22px}
.body figure img{border-radius:18px;width:100%;filter:sepia(.12)}
.body figure figcaption{font-size:12px;color:var(--graphite);padding:8px 22px 0}
.chips{max-width:660px;margin:50px auto 0;padding:0 22px}
.chips h3{font-size:15px;font-weight:600;color:var(--graphite);margin:18px 0 10px}
.chips a{display:inline-block;font-size:14px;text-decoration:none;border:1px solid var(--hair);border-radius:999px;padding:6px 14px;margin:0 8px 8px 0}
.chips a:hover{border-color:var(--brass);color:var(--brass)}
.ademo{max-width:700px;margin:60px auto 0;padding:0 22px}
.ademo>h2{font-size:26px;font-weight:700;margin-bottom:2px}
/* page head */
.phead{max-width:760px;margin:0 auto;padding:80px 22px 10px;text-align:center}
.phead h1{font-size:clamp(34px,6vw,60px);font-weight:700;letter-spacing:-.02em;line-height:1.15}
.phead p{color:var(--graphite);font-size:19px;margin-top:14px;line-height:1.7}
/* path */
.path{list-style:none;margin-top:40px;counter-reset:p}
.step{display:grid;grid-template-columns:84px 1fr;gap:22px;padding:30px 0;border-top:1px solid var(--hair);counter-increment:p}
.step .disc2{width:84px;height:84px;border-radius:50%;background:radial-gradient(circle,#0f0f0f 0 4%,var(--c) 4.5% 29%,#141414 30% 100%);box-shadow:inset 0 0 0 1px #000;position:relative}
.step .disc2:after{content:counter(p);position:absolute;right:-6px;top:-6px;width:28px;height:28px;border-radius:50%;background:var(--paper);border:1px solid var(--hair);display:grid;place-items:center;font-size:13px;font-weight:600}
.step h3{font-size:22px;font-weight:600;line-height:1.35}
.step h3 small{display:block;font-size:14px;color:var(--graphite);font-weight:400;margin-top:2px}
.step p{margin-top:8px;font-size:16px;line-height:1.75}
.step .lf{color:var(--graphite);font-size:15px}
.step .lf b{color:var(--ink);font-weight:600}
.step a.st{font-size:14px;color:var(--brass);text-decoration:none;display:inline-block;margin-top:8px}
@media (max-width:520px){.step{grid-template-columns:56px 1fr;gap:16px}.step .disc2{width:56px;height:56px}}
.branch{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--hair);border:1px solid var(--hair);border-radius:18px;overflow:hidden;margin-top:30px}
.branch div{background:var(--paper);padding:22px}
.branch b{display:block;font-size:17px;margin-bottom:4px}
.branch span{color:var(--graphite);font-size:15px}
@media (max-width:640px){.branch{grid-template-columns:1fr}}
.pathmini{display:flex;gap:18px;margin-top:34px;overflow-x:auto;padding-bottom:8px;scrollbar-width:thin}
.pathmini a{flex:0 0 150px;text-decoration:none}
.pathmini .disc2{width:150px;height:150px;border-radius:50%;background:radial-gradient(circle,#0f0f0f 0 3%,var(--c) 3.5% 30%,#141414 31% 100%),#141414;box-shadow:0 20px 40px -24px rgba(0,0,0,.6)}
.pathmini b{display:block;font-size:15px;margin-top:12px;line-height:1.4}
.pathmini span{display:block;font-size:13px;color:var(--graphite)}
/* people */
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1px;background:var(--hair);border:1px solid var(--hair);border-radius:20px;overflow:hidden;margin-top:40px}
.person{background:var(--paper);padding:26px 24px;scroll-margin-top:120px}
.pic{margin:-26px -24px 18px;aspect-ratio:4/3;position:relative;overflow:hidden;background:#111}
.pic img{width:100%;height:100%;object-fit:cover;object-position:50% 22%;filter:grayscale(.15) contrast(1.02)}
.pic figcaption{position:absolute;left:0;right:0;bottom:0;font-size:10px;line-height:1.4;color:rgba(255,255,255,.75);padding:16px 10px 6px;background:linear-gradient(transparent,rgba(0,0,0,.55))}
.pic.ill{background:radial-gradient(circle at 50% 40%,color-mix(in srgb,var(--c) 70%,#fff) 0,var(--c) 70%);color:#fbf5ea;display:grid;place-items:center}
.pic.ill svg{width:62%;height:auto;opacity:.92}
.pic .tag{position:absolute;left:10px;bottom:8px;font-size:11px;color:#fbf5ea;background:rgba(0,0,0,.28);padding:3px 9px;border-radius:999px}
.pmini .pic{margin:-18px -18px 12px;aspect-ratio:1/1}
.pmini .pic figcaption{display:none}
.pmini .pic .tag{font-size:10px}
.person:target{background:var(--lamp)}
.person img.mono2{object-fit:cover;filter:grayscale(.2)}
.person .mono2{width:46px;height:46px;border-radius:50%;background:var(--c);color:#fff;display:grid;place-items:center;font-size:16px;font-weight:600;letter-spacing:.02em}
.person h3{font-size:20px;font-weight:600;margin-top:14px;line-height:1.35}
.person .meta{font-size:13px;color:var(--graphite)}
.person .one{font-weight:500;margin-top:10px;font-size:16px}
.person p.bio{color:var(--graphite);font-size:15px;line-height:1.75;margin-top:8px}
.person .first{font-size:14px;margin-top:12px}
.person .first a{color:var(--brass);text-decoration:none}
.person .rel{font-size:13px;margin-top:8px}
.person .rel a{color:var(--graphite)}
.pmini{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--hair);border:1px solid var(--hair);border-radius:18px;overflow:hidden;margin-top:34px}
.pmini a{background:var(--paper);padding:18px;text-decoration:none}
.pmini a:hover{background:var(--wash)}
.pmini b{display:block;font-size:16px}
.pmini span{font-size:13px;color:var(--graphite)}
@media (max-width:760px){.pmini{grid-template-columns:1fr 1fr}}
/* words */
.search{display:block;width:100%;max-width:420px;margin:30px auto 0;font:inherit;font-size:16px;padding:12px 18px;border-radius:999px;border:1px solid var(--hair);background:var(--paper);color:var(--ink)}
.wlist{margin-top:30px;border-top:1px solid var(--hair)}
.word{display:grid;grid-template-columns:200px 1fr;gap:24px;padding:22px 0;border-bottom:1px solid var(--hair);scroll-margin-top:120px}
.word:target{background:var(--lamp)}
.word h3{font-size:20px;font-weight:600;line-height:1.35}
.word h3 small{display:block;font-size:13px;color:var(--graphite);font-weight:400}
.word p{font-size:16px;line-height:1.8}
.word .ex{color:var(--graphite);font-size:14px;margin-top:6px}
.word .ex a{color:var(--brass);text-decoration:none}
@media (max-width:640px){.word{grid-template-columns:1fr;gap:6px}}
.today{background:var(--wash);border-radius:22px;padding:34px 30px;margin-top:34px;display:grid;grid-template-columns:1fr auto;gap:20px;align-items:end}
.today h3{font-size:clamp(28px,4vw,38px);font-weight:700;letter-spacing:-.01em}
.today h3 small{font-size:15px;color:var(--graphite);font-weight:400;margin-left:10px}
.today p{font-size:17px;margin-top:8px;max-width:36em}
.today button{background:none;border:1px solid var(--hair);color:var(--ink);font:inherit;font-size:14px;padding:8px 16px;border-radius:999px;cursor:pointer}
@media (max-width:640px){.today{grid-template-columns:1fr}}
/* timeline */
.tl{position:relative;margin-top:44px;padding-left:34px}
.tl:before{content:"";position:absolute;left:8px;top:6px;bottom:6px;width:2px;background:var(--hair)}
.ev{position:relative;padding:0 0 34px}
.ev:before{content:"";position:absolute;left:-31px;top:10px;width:12px;height:12px;border-radius:50%;background:var(--paper);border:2px solid var(--graphite)}
.ev.has:before{background:var(--brass);border-color:var(--brass)}
.ev .yr{font-size:34px;font-weight:200;letter-spacing:-.03em;line-height:1.1;color:var(--graphite)}
.ev.has .yr{color:var(--brass)}
.ev h3{font-size:20px;font-weight:600;margin-top:4px}
.ev p{color:var(--graphite);font-size:16px;line-height:1.75;margin-top:4px;max-width:36em}
.ev a{font-size:14px;color:var(--brass);text-decoration:none;display:inline-block;margin-top:6px}
.ev.wp{display:grid;grid-template-columns:1fr 260px;gap:28px;align-items:start}
.evpic{margin:6px 0 0;border-radius:14px;overflow:hidden;background:#111;aspect-ratio:4/3;position:relative}
.evpic img{width:100%;height:100%;object-fit:cover;object-position:50% 30%;filter:sepia(.18) contrast(1.02)}
.evpic figcaption{position:absolute;left:0;right:0;bottom:0;font-size:10px;line-height:1.4;color:rgba(255,255,255,.78);padding:14px 9px 5px;background:linear-gradient(transparent,rgba(0,0,0,.55))}
@media (max-width:640px){.ev.wp{grid-template-columns:1fr;gap:12px}.ev.wp .evpic{order:-1;margin-top:0}}
.hallnav{position:sticky;top:52px;z-index:5;display:flex;gap:6px;overflow-x:auto;scrollbar-width:none;background:color-mix(in srgb,var(--paper) 88%,transparent);backdrop-filter:saturate(1.6) blur(14px);-webkit-backdrop-filter:saturate(1.6) blur(14px);padding:10px max(22px,calc(50% - 440px)) 12px;border-bottom:1px solid var(--hair);margin-top:30px}
.hallnav::-webkit-scrollbar{display:none}
.hallnav a{flex:0 0 auto;text-decoration:none;padding:7px 14px;border-radius:999px;font-size:14px;color:var(--graphite);border:1px solid transparent;white-space:nowrap}
.hallnav a b{font-weight:600;margin-right:6px}
.hallnav a.on{background:var(--ink);color:var(--paper)}
.hallnav i{position:absolute;left:0;right:0;bottom:-1px;height:2px;background:var(--brass);transform:scaleX(0);transform-origin:left;transition:transform .1s linear}
@media (max-width:640px){.hallnav{top:78px}.hallnav a span{display:none}}
.exhibition{max-width:900px}
.hall{padding-top:70px;scroll-margin-top:130px}
.hallhead{padding:36px 34px;border-radius:24px;background:linear-gradient(135deg,var(--lamp),var(--wash));margin-bottom:40px}
.hallhead .no{font-size:14px;color:var(--brass);font-weight:600}
.hallhead h2{font-size:clamp(30px,5vw,46px);font-weight:700;letter-spacing:-.02em;margin-top:6px;line-height:1.2}
.hallhead p{font-size:17px;line-height:1.85;margin-top:12px;max-width:38em;color:var(--ink)}
.hall .tl{margin-top:0}
.ev{position:relative;border-radius:18px;transition:background .2s}
.ev:hover{background:var(--wash)}
.evbtn{position:absolute;inset:-8px -14px;z-index:2;background:transparent;border:0;cursor:pointer;border-radius:18px}
.evbtn:focus-visible{outline:2px solid var(--brass);outline-offset:2px}
.ev .open{display:inline-block;margin-top:10px;font-size:14px;color:var(--brass)}
.ev .open:after{content:" ＋"}
.ev.pre{opacity:0;transform:translateY(18px);transition:opacity .6s ease,transform .6s ease,background .2s}
.ev.pre.in{opacity:1;transform:none}
.evpic.none{display:grid;place-items:center;background:linear-gradient(135deg,#2a2018,#4a3622)}
.evpic.none span{font-size:44px;font-weight:200;color:#e9d9bd;letter-spacing:-.03em}
#exhibit{border:0;padding:0;margin:auto;inset:0;width:min(920px,calc(100% - 24px));max-height:calc(100dvh - 40px);border-radius:24px;background:var(--paper);color:var(--ink);box-shadow:0 40px 120px -30px rgba(0,0,0,.6);overflow:hidden;display:none;flex-direction:column}
#exhibit[open]{display:flex;animation:pop .28s ease}
#exhibit::backdrop{background:rgba(12,10,8,.62);backdrop-filter:blur(4px)}
@keyframes pop{from{opacity:0;transform:translateY(16px) scale(.98)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){#exhibit[open]{animation:none}}
.xbar{display:flex;justify-content:space-between;align-items:center;padding:12px 16px 12px 22px;border-bottom:1px solid var(--hair);font-size:13px;color:var(--graphite)}
.xclose{background:var(--wash);border:0;width:34px;height:34px;border-radius:50%;font-size:15px;cursor:pointer;color:var(--ink)}
.xbody{overflow-y:auto;display:grid;grid-template-columns:1fr 1fr;min-height:0}
.xi{background:#111;position:relative;min-height:320px}
.xi img{width:100%;height:100%;object-fit:cover;position:absolute;inset:0;filter:sepia(.12)}
.xi small{position:absolute;left:0;right:0;bottom:0;font-size:11px;color:rgba(255,255,255,.8);padding:24px 14px 10px;background:linear-gradient(transparent,rgba(0,0,0,.6))}
.xi .ph{position:absolute;inset:0;display:grid;place-items:center;font-size:64px;font-weight:200;color:#e9d9bd;background:linear-gradient(135deg,#2a2018,#4a3622)}
.xtx{padding:30px 30px 26px}
.xy{font-size:44px;font-weight:200;letter-spacing:-.03em;color:var(--brass);line-height:1}
.xt{font-size:26px;font-weight:700;margin-top:8px;line-height:1.3}
.xd{font-size:16px;line-height:1.8;margin-top:12px;font-weight:500}
.xm{font-size:16px;line-height:1.9;margin-top:12px;color:var(--graphite)}
.xs{margin-top:20px;background:var(--wash);border-radius:16px;padding:16px 18px}
.xs b{display:block;font-size:16px}
.xs span{display:block;font-size:14px;color:var(--graphite);margin-top:4px}
.xs .lk a{color:var(--brass);text-decoration:none;margin-right:16px;font-size:14px}
.xp h4{font-size:14px;color:var(--graphite);font-weight:500;margin:20px 0 10px}
.xp a{display:inline-flex;align-items:center;gap:8px;text-decoration:none;font-size:14px;border:1px solid var(--hair);border-radius:999px;padding:4px 14px 4px 4px;margin:0 8px 8px 0}
.xp a img{width:28px;height:28px;border-radius:50%;object-fit:cover}
.xp a.story{display:block;border:0;padding:0;margin-top:14px;color:var(--brass);font-size:15px}
.xnav{display:flex;justify-content:space-between;padding:12px 16px;border-top:1px solid var(--hair)}
.xnav button{background:none;border:1px solid var(--hair);color:var(--ink);font:inherit;font-size:14px;padding:9px 18px;border-radius:999px;cursor:pointer}
.xnav button:hover{border-color:var(--brass);color:var(--brass)}
@media (max-width:720px){.xbody{grid-template-columns:1fr;display:block}.xi{min-height:0;height:auto}.xi img{position:static;display:block;height:auto;max-height:46vh;object-fit:cover}.xi small{position:static;background:#111;padding:6px 12px}.xi .ph{position:static;height:180px}.xtx{padding:22px 20px}.xy{font-size:36px}.xt{font-size:22px}}
.tlmini img{display:block;width:134px;height:90px;object-fit:cover;border-radius:10px;margin-bottom:10px;filter:sepia(.18)}
.tlmini{display:flex;gap:0;margin-top:34px;overflow-x:auto;border-top:2px solid var(--hair);scrollbar-width:thin}
.tlmini a{flex:0 0 150px;padding:16px 16px 10px 0;text-decoration:none;position:relative}
.tlmini a:before{content:"";position:absolute;top:-7px;left:0;width:12px;height:12px;border-radius:50%;background:var(--paper);border:2px solid var(--graphite)}
.tlmini a.has:before{background:var(--brass);border-color:var(--brass)}
.tlmini b{display:block;font-size:22px;font-weight:300;letter-spacing:-.02em}
.tlmini span{font-size:13px;color:var(--graphite);line-height:1.5;display:block}
/* shop */
.shop{margin-top:20px}
.shop h2{font-size:clamp(26px,3.6vw,34px);font-weight:700;margin-top:60px}
.shop .sd{color:var(--graphite);font-size:17px;margin-top:6px;max-width:36em}
.items{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px;margin-top:22px}
.item{border:1px solid var(--hair);border-radius:18px;padding:22px;display:flex;flex-direction:column}
.item b{font-size:17px;font-weight:600;line-height:1.45}
.item p{color:var(--graphite);font-size:15px;line-height:1.7;margin-top:6px;flex:1}
.item .lk{margin-top:14px;font-size:13px}
.item .lk a{color:var(--brass);text-decoration:none;margin-right:14px}
.note2{background:var(--wash);border-radius:18px;padding:22px 24px;margin-top:50px;color:var(--graphite);font-size:15px;line-height:1.8}
"""

HEAD = """<!doctype html><html lang="zh-Hant-TW"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">{ogimg}
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500;600;700&family=Noto+Sans+TC:wght@300;400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p}style.css"></head><body>"""

NAV = [('index.html#stories', '故事', 'stories'), ('shorts.html', '一分鐘故事', 'shorts'), ('start.html', '入門路線', 'start'), ('listen.html', '聽懂爵士', 'listen'), ('rhythm.html', '節奏遊戲', 'rhythm'), ('harmony.html', '和聲遊戲', 'harmony'), ('people.html', '樂手', 'people'),
       ('words.html', '小辭典', 'words'), ('timeline.html', '線上展', 'timeline'), ('shop.html', '選品', 'shop'), ('index.html#letter', '電子報', 'letter')]
def nav(p, cur=''):
    links = ''.join(f'<a href="{p}{h}"{" class=cur aria-current=page" if k == cur else ""}>{t}</a>' for h, t, k in NAV)
    return f'<div class="nav"><div class="in"><a class="brand" href="{p}index.html">爵士101</a><nav aria-label="網站導覽">{links}</nav></div></div>'

def foot(p='', js=''):
    return (f'<footer>爵士101 由 Jim 在台北整理。每篇故事都附出處，查不到的不寫；照片來自 Wikimedia Commons，作者與授權標在照片下方。聲音示範全部由瀏覽器現場合成。<br>'
            f'一分鐘版在 Instagram <a href="{IG}" target="_blank" rel="noopener">@jazz101tw</a>。</footer>{js}</body></html>')

def letter():
    return f'<section class="letter" id="letter"><h2>每兩週，一張唱片。</h2><p>電子報〈慢慢聽〉每期只講一張爵士唱片：那天在哪裡錄、台上是誰、你該聽哪一段。不用懂樂理，戴上耳機照著聽。</p><a class="btn" href="{SUB_HREF}" target="_blank" rel="noopener">{SUB_TXT}</a></section>'

def clean_artist(a):
    import re
    a = re.sub(r'^[^:]*\.jpg:\s*', '', a)
    if 'nknown author' in a or a.startswith('Anonymous'):
        return '作者不詳'
    a = a.replace('Photographer uncredited a', '攝影者未具名').strip()
    return a
def credit(ph):
    return f'照片：{e(clean_artist(ph["artist"]))}，{e(ph["license"])}，Wikimedia Commons' if ph else ''

COL = ['#a97a2b', '#8c2f2b', '#2f5d6b', '#c9b48a', '#4b3a6b', '#6d7a3a', '#b4532a', '#3e6b52', '#7a2f4f', '#5a6e8c']
def img(ph, pre, cls='', alt='', i=0):
    return f'<img class="{cls}" src="{pre}img/{ph["file"]}" alt="{e(alt)}" loading="lazy">' if ph else f'<div class="{cls} empty" style="--c:{COL[i % len(COL)]}" aria-hidden="true"></div>'

def q(s): return s.replace(' ', '+')
def links(song):
    return f'<div><a href="https://music.apple.com/search?term={e(q(song))}" target="_blank" rel="noopener">在 Apple Music 找</a><a href="https://open.spotify.com/search/{e(q(song))}" target="_blank" rel="noopener">在 Spotify 找</a></div>'
def W(p, name, page):
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(page)

os.makedirs(os.path.join(OUT, 'story'), exist_ok=True)
os.makedirs(os.path.join(OUT, 'img'), exist_ok=True)
for k, m in META.items():
    if m and os.path.exists(os.path.join(IMGSRC, m['file'])):
        shutil.copy(os.path.join(IMGSRC, m['file']), os.path.join(OUT, 'img', m['file']))
CSSR = r'''
/* 節奏遊戲 */
.rgame{padding-bottom:20px}
.lvmap{display:grid;grid-template-columns:repeat(9,minmax(0,1fr));gap:8px;margin-top:8px}
@media (max-width:900px){.lvmap{grid-template-columns:repeat(3,minmax(0,1fr))}}
.lvl{display:block;text-decoration:none;border:1px solid var(--hair);border-radius:16px;padding:14px 12px 12px;background:var(--paper);min-width:0}
.lvl:hover{border-color:var(--brass)}
.lvl em,.rhmini em{font-style:normal;font-size:30px;font-weight:200;color:var(--graphite);line-height:1;display:block;letter-spacing:-.02em}
.lvl b{display:block;font-size:15px;font-weight:600;margin-top:8px;line-height:1.35}
.lvl>span{display:block;font-size:12px;color:var(--graphite);line-height:1.4;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.lvl.cur{border-color:var(--brass);box-shadow:inset 0 0 0 1px var(--brass)}
.lvl.done em{color:var(--brass)}
.stars i{font-style:normal;color:var(--hair);font-size:13px;letter-spacing:1px}.stars i.on{color:var(--brass)}
.tot{font-size:14px;color:var(--graphite);margin-top:12px}
.rstage{background:var(--midnight);color:#f2efe9;border-radius:28px;margin-top:24px;padding:34px 34px 30px;scroll-margin-top:70px}
@media (max-width:520px){.rstage{padding:24px 18px 22px;border-radius:22px}}
.rs-head small{color:#e0ae55;font-size:14px;display:block}
.rs-head h2{font-size:clamp(30px,5vw,46px);font-weight:700;letter-spacing:-.02em;line-height:1.15;display:inline}
.rs-head .en{color:#8e93a0;font-size:16px;margin-left:12px;white-space:nowrap}
.rs-head p{color:#b9bdc7;margin-top:8px;font-size:17px}
.steps{display:inline-flex;margin-top:22px;border:1px solid #2e3a52;border-radius:999px;padding:3px;max-width:100%}
.steps button{background:none;border:0;color:#a3a8b4;font:inherit;font-size:15px;padding:8px 18px;border-radius:999px;cursor:pointer;white-space:nowrap}
.steps button.on{background:#f2efe9;color:#172033}
.rs-body{display:grid;grid-template-columns:minmax(0,420px) minmax(0,1fr);gap:40px;margin-top:26px;align-items:start}
@media (max-width:820px){.rs-body{grid-template-columns:minmax(0,1fr);gap:18px}}
.rs-wheel{display:flex;flex-direction:column;align-items:center;min-width:0}
#wheel{display:block}
.tapbtn{margin-top:14px;width:100%;height:96px;border-radius:24px;border:0;background:#e0ae55;color:#1d1408;font:inherit;font-size:28px;font-weight:700;cursor:pointer;touch-action:manipulation;user-select:none;-webkit-user-select:none;-webkit-tap-highlight-color:transparent;transition:transform .06s}
.tapbtn.hit{transform:scale(.97);background:#f4cd84}
.tapzone{width:100%;max-width:420px;text-align:center}.tapzone[hidden]{display:none}.tapline{display:flex;justify-content:space-between;align-items:baseline;gap:10px;margin-top:10px}.tapline .tapfb{margin-top:0;text-align:left}.rs-wheel{scroll-margin-top:110px}
.rs-side{min-width:0}
.rs-side p{color:#c9ccd4}
.rstage .dplay{background:#f2efe9;color:#172033}
.rstage .dplay.playing{background:#e0ae55;color:#1d1408}
.btn2{background:none;border:1px solid #3a4660;color:#f2efe9;font:inherit;font-size:15px;padding:9px 18px;border-radius:999px;cursor:pointer}
.btn2:hover{border-color:#e0ae55}
.btn2[hidden],.dplay[hidden]{display:none}
.tapcount{font-variant-numeric:tabular-nums;color:#a3a8b4;font-size:15px}
.tapfb{font-size:22px;font-weight:600;margin-top:16px;min-height:1.5em;color:#f2efe9!important}
.rstage .q-perfect{color:#ecbd62!important}.rstage .q-miss,.rstage .q-off,.rstage .q-extra{color:#ec9a8c!important}
.kbd{font-size:13px;color:#8e93a0!important;margin-top:2px}
.res{margin-top:18px;padding:18px 20px;border-radius:18px;background:rgba(255,255,255,.06)}
.res b{font-size:24px;font-weight:700;display:block;line-height:1.4}
.res .meta{font-size:14px;color:#a3a8b4}
.res .btn2,.res .dplay{margin-top:12px}
.gab{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:14px}
.gab>div{display:flex;flex-direction:column;gap:8px;background:rgba(255,255,255,.04);padding:14px;border-radius:16px;align-items:stretch}
.gab .dplay{justify-content:center}
.gans{background:none;border:1px solid #3a4660;color:#f2efe9;font:inherit;font-size:16px;padding:10px;border-radius:12px;cursor:pointer}
.gans:disabled{cursor:default}
.gans.right,.xopts button.right{background:#e0ae55;border-color:#e0ae55;color:#1d1408}
.gans.wrong{border-color:#ec9a8c;color:#ec9a8c}
.gfb{margin-top:14px;font-size:17px;min-height:1.6em}
.rs-more{margin-top:26px;border-top:1px solid #2e3a52;padding-top:6px;font-size:15px}
.rs-more p{margin-top:12px;color:#b9bdc7;line-height:1.7}
.rs-more b{display:block;color:#f2efe9;font-size:14px;font-weight:600}
.rs-more a{color:#ecbd62;text-decoration:none;margin-right:16px;display:inline-block}
.rs-more a:hover{text-decoration:underline}
.exam .dplay{margin-top:22px}
.xopts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-top:16px;max-width:620px}
@media (max-width:520px){.xopts{grid-template-columns:repeat(2,minmax(0,1fr))}}
.xopts button{background:var(--paper);border:1px solid var(--hair);color:var(--ink);font:inherit;font-size:15px;padding:12px 8px;border-radius:12px;cursor:pointer}
.xopts button.wrong{border-color:#c8695c;color:#c8695c}
.exam #xq{font-size:19px;font-weight:600;margin:24px 0 0}
.exam #xfb{margin-top:12px;font-size:17px;min-height:1.6em}
.exam .btn2{color:var(--ink);border-color:var(--hair);margin-top:4px}
.exam #xend b{display:block;font-size:20px;margin-top:20px;line-height:1.5}
.latset{margin:56px 0 0;font-size:14px;color:var(--graphite)}
.latset summary{cursor:pointer}
.latset p{margin-top:8px;max-width:34em}
.latset input{vertical-align:middle;width:min(220px,60vw)}
.rhmini{display:grid;grid-template-columns:repeat(9,minmax(0,1fr));gap:8px;margin-top:30px}
@media (max-width:760px){.rhmini{grid-template-columns:repeat(3,minmax(0,1fr))}}
.rhmini a{border:1px solid var(--hair);border-radius:14px;padding:12px;text-decoration:none;min-width:0}
.rhmini a:hover{border-color:var(--brass)}
.tier{font-size:20px;font-weight:700;margin:30px 0 10px;letter-spacing:-.01em}.tier span{display:block;font-size:14px;font-weight:400;color:var(--graphite);margin-top:2px}.lvmap.t4{grid-template-columns:repeat(4,minmax(0,1fr))}.lvmap.t3{grid-template-columns:repeat(3,minmax(0,1fr))}.lvmap.t6{grid-template-columns:repeat(6,minmax(0,1fr))}@media (max-width:900px){.lvmap.t4{grid-template-columns:repeat(2,minmax(0,1fr))}.lvmap.t6{grid-template-columns:repeat(3,minmax(0,1fr))}}.hstory{max-width:40em;margin:70px 0 0}.hstory h2{font-size:clamp(26px,4vw,36px);font-weight:700;letter-spacing:-.02em;line-height:1.25}.hstory p{margin-top:14px;color:var(--ink)}
.hdemos{display:flex;flex-direction:column;align-items:flex-start;gap:10px;margin-top:16px}.hdemos .dplay{text-align:left}.hq{font-size:19px;font-weight:600;color:#f2efe9!important}.hopts{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px;margin-top:16px}
.rhmini b{display:block;font-size:14px;font-weight:600;margin-top:6px;line-height:1.35}
'''
open(os.path.join(OUT, 'style.css'), 'w', encoding='utf-8').write(CSS + CSS2 + CSSR)
open(os.path.join(OUT, 'player.js'), 'w', encoding='utf-8').write(PLAYER)
shutil.copy(os.path.join(HERE, 'audio.js'), os.path.join(OUT, 'audio.js'))
shutil.copy(os.path.join(HERE, 'rhythm.js'), os.path.join(OUT, 'rhythm.js'))
_rj_src = open(os.path.join(HERE, 'rhythm.js'), encoding='utf-8').read()
_core = _rj_src[_rj_src.index('var AC='):_rj_src.index('/* ---- 九種節奏 ---- */')]
open(os.path.join(OUT, 'harmony.js'), 'w', encoding='utf-8').write('/* 爵士101 和聲遊戲（由 build.py 產生：聲音引擎取自 rhythm.js） */\n(function(){\n' + _core + open(os.path.join(HERE, 'harmony_body.js'), encoding='utf-8').read() + '\n})();\n')
AUD = lambda p: f'<script src="{p}audio.js"></script>'
PW = os.environ.get('JAZZ_PAYWALL') == '1'   # 會員制試做版
FREE_DEMOS = {'swing', 'blues', 'iivi'}
def LOCK(p, what, short=False):
    if short:
        return f'<a class="lockmini" href="{p}members.html">🔒 {e(what)}：深夜場會員限定</a>'
    return (f'<div class="lock"><div class="lk-ic" aria-hidden="true">🔒</div><b>{e(what)}是〈深夜場〉會員內容</b>'
            f'<p>加入會員看完整版：全部故事全文、展品完整說明與先聽一首、十個聲音示範、每週導聆課、台北爵士週報。</p>'
            f'<a class="btn" href="{p}members.html">看會員方案</a></div>')
if PW:
    NAV.insert(0, ('members.html', '深夜場', 'members'))
    _nav0 = nav
    def nav(p, cur=''):
        return _nav0(p, cur) + f'<div class="pwbar">會員制試做版・還沒公開，只是給你看效果・<a href="https://jazz101tw.github.io/">正式網站</a></div>'
open(os.path.join(OUT, 'style.css'), 'a', encoding='utf-8').write(r"""
.lock{max-width:620px;margin:34px auto;padding:30px 28px;border-radius:22px;text-align:center;background:linear-gradient(160deg,#172033,#2a2018);color:#f5ebdd;position:relative}
.lock:before{content:"";position:absolute;left:0;right:0;top:-90px;height:90px;background:linear-gradient(transparent,var(--paper));pointer-events:none}
.lock .lk-ic{font-size:26px}
.lock b{display:block;font-size:20px;margin-top:6px}
.lock p{color:#cfc6b6;font-size:15px;line-height:1.8;margin:10px 0 18px}
.lock .btn{background:#d6aa60;color:#1d1408}
.lockmini{display:inline-block;margin-top:10px;font-size:14px;color:var(--brass);text-decoration:none;border:1px dashed var(--brass);border-radius:999px;padding:5px 14px}
.demo.locked{opacity:.92}
.demo.locked .cells,.demo.locked .dctl{display:none}
.step.locked{opacity:.55}
.pwbar{background:#d6aa60;color:#1d1408;text-align:center;font-size:13px;padding:6px 12px}
.pwbar a{color:#1d1408}
.plans{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:16px;margin-top:30px}
.plan{border:1px solid var(--hair);border-radius:20px;padding:24px}
.plan.hot{border-color:var(--brass);box-shadow:0 0 0 2px var(--brass) inset}
.plan b{font-size:18px}
.plan .pr{font-size:30px;font-weight:700;margin:8px 0}
.plan p{color:var(--graphite);font-size:14px;line-height:1.7}
.bens{margin-top:30px;border-top:1px solid var(--hair)}
.ben{display:grid;grid-template-columns:44px 1fr;gap:14px;padding:16px 0;border-bottom:1px solid var(--hair)}
.ben i{font-style:normal;font-size:22px}
.ben b{font-size:17px}
.ben p{color:var(--graphite);font-size:15px;line-height:1.7;margin-top:2px}
""") if PW else None

# ---------- 故事頁 ----------
for i, s in enumerate(S):
    body = ''
    for n, (h, ps) in enumerate(s['sections']):
        if PW and n >= 2:
            body += LOCK('../', '這篇故事的後半段'); break
        body += f'<h2>{e(h)}</h2>' + ''.join(f'<p>{e(x)}</p>' for x in ps)
        if n == 1 and s.get('pull'):
            body += f'<blockquote class="pull">{e(s["pull"])}</blockquote>'
        if n == 3 and s['ph2']:
            body += f'<figure><img src="../img/{s["ph2"]["file"]}" alt="" loading="lazy"><figcaption>{credit(s["ph2"])}</figcaption></figure>'
    tr = ''
    for n, (a, b) in enumerate(s['listen'], 1):
        song = a if not a.startswith(('再', '注意', 'Part', '聽他', '比一比', '同一首')) else ''
        if PW and n > 1:
            tr += f'<div class="tr"><div class="n">{n}</div><div><b>{e(a)}</b>{LOCK("../", "完整聽法", True)}</div></div>'; continue
        tr += f'<div class="tr"><div class="n">{n}</div><div><b>{e(a)}</b><p>{e(b)}</p>{links(song) if song else ""}</div></div>'
    more = ''.join(f'<li>{e(m)}</li>' for m in s['more']) if not PW else f'<li>{LOCK("../", "延伸聽", True)}</li>'
    prev = S[i - 1] if i > 0 else None
    nxt = S[i + 1] if i < len(S) - 1 else None
    pn = '<div class="pn">' + (f'<a href="{prev["slug"]}.html"><small>上一篇</small>{e(prev["title"])}</a>' if prev else '<span></span>') + (f'<a href="{nxt["slug"]}.html"><small>下一篇</small>{e(nxt["title"])}</a>' if nxt else '<span></span>') + '</div>'
    ph = s['ph']
    hero = f'<div class="hero-img"><img src="../img/{ph["file"]}" alt="{e(s["title"])}"><p class="credit">{credit(ph)}</p></div>' if ph else ''
    facts = '<section class="facts" aria-label="基本資料"><dl>' + ''.join(f'<dt>{e(a)}</dt><dd>{e(b)}</dd>' for a, b in s.get('facts', [])) + '</dl></section>'
    chips = '<section class="chips">'
    if s.get('people'):
        chips += '<h3>這篇裡的人</h3>' + ''.join(f'<a href="../people.html#{p}">{e(PBY[p][1])}</a>' for p in s['people'] if p in PBY)
    if s.get('words'):
        chips += '<h3>這篇用到的名詞</h3>' + ''.join(f'<a href="../words.html#{w}">{e(WBY[w][1])}</a>' for w in s['words'] if w in WBY)
    chips += '</section>'
    dm = f'<section class="ademo"><h2>先用耳朵聽懂</h2>{demo_card(s["demo"])}</section>' if s.get('demo') and (not PW or s['demo'] in FREE_DEMOS) else ''
    page = HEAD.format(title=e(s['title']) + '｜爵士101', desc=e(s['dek']), p='../', ogimg=(f'<meta property="og:image" content="../img/{ph["file"]}">' if ph else '')) + nav('../', 'stories') + \
        f'<header class="ahead"><div class="yearbig">{e(s["year"])}</div><h1>{e(s["title"])}</h1><p class="dek">{e(s["dek"])}</p><p class="rt">約 {s["chars"]:,} 字・閱讀約 {e(s["read"])}</p></header>{hero}{facts}' + \
        f'<article class="body">{body}</article>{dm}' + \
        f'<section class="tracks"><h2>這樣聽</h2><p class="sub">戴上耳機，照這個順序。</p>{tr}</section>' + \
        f'<section class="more"><h2>聽完再去聽</h2><ul>{more}</ul></section>{chips}' + \
        f'<p class="src">出處：{"、".join(e(x) for x in s["src"])}</p>{pn}{letter()}' + foot('../', AUD('../') if s.get('demo') else '')
    W('../', os.path.join('story', s['slug'] + '.html'), page)

def phead(t, d):
    return f'<header class="phead"><h1>{e(t)}</h1><p>{e(d)}</p></header>'

# ---------- 入門路線 ----------
steps = ''
for n, (alb, art, yr, why, song, lf, st) in enumerate(START):
    stl = f'<a class="st" href="story/{st}.html">相關故事：{e(BYSLUG[st]["title"])}</a>' if st else ''
    if PW and n >= 3:
        steps += f'<li class="step locked"><div class="disc2" style="--c:{COL[n % len(COL)]}" aria-hidden="true"></div><div><h3>《{e(alb)}》<small>{e(art)}・{e(yr)}</small></h3>{LOCK("", "這張的聽法", True)}</div></li>'; continue
    steps += (f'<li class="step"><div class="disc2" style="--c:{COL[n % len(COL)]}" aria-hidden="true"></div><div><h3>《{e(alb)}》<small>{e(art)}・{e(yr)}</small></h3>'
              f'<p>{e(why)}</p><p class="lf"><b>先聽〈{e(song)}〉</b>：{e(lf)}</p><div class="tr" style="border:0;padding:6px 0 0;display:block">{links(art + " " + song)}</div>{stl}</div></li>')
br = ''.join(f'<div><b>{e(a)}</b><span>{e(b) if not PW else LOCK("", "推薦", True)}</span></div>' for a, b in BRANCH)
W('', 'start.html', HEAD.format(title='入門路線｜爵士101', desc='第一次聽爵士，照這十張的順序聽。', p='', ogimg='') + nav('', 'start') +
  phead('第一次聽爵士，照這十張的順序。', '從最好入口的開始，一張比一張多一點東西。每張只要先聽一首，知道該注意什麼就好。') +
  f'<div class="wrap"><ol class="path">{steps}</ol><section class="sec" style="padding-top:60px"><h2>聽完十張之後</h2><p class="lede">看你最喜歡哪一種，往那個方向繼續。</p><div class="branch">{br}</div></section></div>' + letter() + foot())

# ---------- 聽懂爵士 ----------
cards = ''.join(demo_card(i) if (not PW or i in FREE_DEMOS) else demo_card(i).replace('class="demo"', 'class="demo locked"', 1).replace('data-demo="' + i + '"', 'data-demo="x-' + i + '"').replace('<p class="hint">', LOCK('', '這個示範', True) + '<p class="hint" hidden>') for i in DEMO_ORDER)
W('', 'listen.html', HEAD.format(title='聽懂爵士｜爵士101', desc='十個可以按的聲音示範：搖擺、走路低音、藍調、二五一、Giant Steps。', p='', ogimg='') + nav('', 'listen') +
  phead('不用懂樂理，用耳朵聽懂爵士。', '十個可以按的聲音示範。每一個都在你的瀏覽器裡現場彈出來，可以切換比較。建議戴耳機。') +
  f'<div class="wrap"><div class="demos">{cards}</div></div>' + letter() + foot('', AUD('')))

# ---------- 樂手 ----------
STORY_OF = {}
for s in S:
    for p in s.get('people', []):
        STORY_OF.setdefault(p, []).append(s)

ICON = {
 'trumpet': '<path d="M30 78h88M30 70v16M118 64l52-22v72l-52-22z"/><path d="M58 78V58m14 20V58m14 20V58"/><circle cx="58" cy="54" r="4"/><circle cx="72" cy="54" r="4"/><circle cx="86" cy="54" r="4"/><path d="M40 78c0 18 70 18 70 0"/>',
 'sax': '<path d="M96 20v70c0 22-14 34-30 34s-26-10-26-24c0-8 6-12 12-12"/><path d="M110 20v72c0 30-20 44-44 44"/><path d="M96 20h14l10-8"/><path d="M52 100c-6 4-10 10-10 18"/><circle cx="103" cy="44" r="4"/><circle cx="103" cy="60" r="4"/><circle cx="103" cy="76" r="4"/><circle cx="103" cy="92" r="4"/>',
 'piano': '<rect x="24" y="44" width="152" height="64" rx="4"/><path d="M43 44v64M62 44v64M81 44v64M100 44v64M119 44v64M138 44v64M157 44v64"/><path d="M38 44h10v38H38zM57 44h10v38H57zM95 44h10v38H95zM114 44h10v38h-10zM133 44h10v38h-10z" fill="currentColor"/>',
 'mic': '<rect x="78" y="18" width="44" height="62" rx="22"/><path d="M84 36h32M84 48h32M84 60h32"/><path d="M66 60c0 30 68 30 68 0"/><path d="M100 90v34M76 128h48"/>',
 'drums': '<ellipse cx="100" cy="104" rx="42" ry="32"/><ellipse cx="100" cy="104" rx="14" ry="11"/><ellipse cx="52" cy="70" rx="24" ry="8"/><path d="M28 70v18c0 5 11 8 24 8s24-3 24-8V70"/><path d="M128 40l44-8M150 36v80M44 26l40 22M88 52l10-18"/>',
 'bass': '<path d="M100 14v40"/><path d="M92 14h16"/><path d="M84 58c-20 0-24 18-14 30-14 8-18 20-14 34 6 16 30 20 44 20s38-4 44-20c4-14 0-26-14-34 10-12 6-30-14-30-6 0-10 4-16 4s-10-4-16-4z"/><path d="M96 54v80M104 54v80"/><path d="M84 92c4 4 4 10 0 14M116 92c-4 4-4 10 0 14"/>',
}
def icon_for(ins):
    for k, v in [('小號', 'trumpet'), ('人聲', 'mic'), ('薩克斯風', 'sax'), ('鋼琴', 'piano'), ('鼓', 'drums'), ('貝斯', 'bass')]:
        if ins.startswith(k) or (k in ins and k != '人聲'):
            return v
    return 'piano'
def portrait(sl, en, ins, n, pre=''):
    k = PPH.get(sl, sl); ph = META.get(k)
    if ph:
        return f'<figure class="pic"><img src="{pre}img/{ph["file"]}" alt="{e(en)}" loading="lazy"><figcaption>{credit(ph)}</figcaption></figure>'
    return (f'<figure class="pic ill" style="--c:{COL[n % len(COL)]}"><svg viewBox="0 0 200 150" role="img" aria-label="{e(en)}的樂器示意圖" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">{ICON[icon_for(ins)]}</svg>'
            f'<span class="tag">示意圖・{e(ins.split("、")[0])}</span></figure>')

def initials(n): return ''.join(w[0] for w in n.split()[:2])
pg = ''
for n, (sl, en, zh, yrs, ins, one, bio, (song, where)) in enumerate(PEOPLE):
    rel = ''.join(f'<div class="rel">相關故事：<a href="story/{s["slug"]}.html">{e(s["title"])}</a></div>' for s in STORY_OF.get(sl, [])[:2])
    pg += (f'<article class="person" id="{sl}">{portrait(sl, en, ins, n)}<h3>{e(en)}</h3><div class="meta">{e(zh)}・{e(yrs)}・{e(ins)}</div>'
           f'<p class="one">{e(one)}</p>' + (LOCK('', '完整介紹與先聽', True) + '</article>' if PW else f'<p class="bio">{e(bio)}</p><p class="first">先聽：<a href="https://music.apple.com/search?term={e(q(en + " " + song))}" target="_blank" rel="noopener">〈{e(song)}〉</a>　<span class="meta">{e(where)}</span></p>{rel}</article>'))
W('', 'people.html', HEAD.format(title='樂手｜爵士101', desc='十五位改變爵士的人，各用一段話認識，附上先聽哪一首。', p='', ogimg='') + nav('', 'people') +
  phead('十五個改變爵士的人。', '依出生年份排列。每個人先記住一句話，再聽一首。') + f'<div class="wrap"><div class="pgrid">{pg}</div></div>' + letter() + foot())

# ---------- 小辭典 ----------
wl = ''
for (wid, zh, en, ex, eg, dm) in WORDS:
    dl = f'　<a href="listen.html#d-{dm}">去聽示範</a>' if dm else ''
    wl += f'<div class="word" id="{wid}" data-k="{e((zh + en + ex).lower())}"><h3>{e(zh)}<small>{e(en)}</small></h3><div><p>{e(ex)}</p><p class="ex">例子：{e(eg)}{dl}</p></div></div>'
W('', 'words.html', HEAD.format(title='小辭典｜爵士101', desc='聽爵士會遇到的名詞，用白話講清楚。', p='', ogimg='') + nav('', 'words') +
  phead('聽爵士會遇到的名詞。', f'{len(WORDS)} 個詞，用白話講一次，附一個可以去聽的例子。有些可以直接聽示範。') +
  '<div class="wrap"><input class="search" type="search" id="q" placeholder="搜尋，例如：搖擺、bebop" aria-label="搜尋名詞">' + f'<div class="wlist">{wl}</div></div>' +
  '<script>document.getElementById("q").addEventListener("input",function(){var v=this.value.trim().toLowerCase();document.querySelectorAll(".word").forEach(function(w){w.style.display=!v||w.dataset.k.indexOf(v)>-1?"":"none"})})</script>' + letter() + foot())

# ---------- 時間軸 ----------
TLPH = {'1890s': ['bolden'], '1917': ['odjb'], '1925': ['hotfive', 'louis-armstrong'], '1927': ['cottonclub', 'duke-ellington'],
        '1935': ['goodman'], '1938': ['carnegie', 'goodman'], '1939': ['hawkins'], '1940s': ['mintons', 'gillespie', 'charlie-parker'],
        '1949': ['mulligan', 'miles-davis'], '1953': ['vangelder'], '1954': ['newport'], '1956': ['rollins'], '1959': ['brubeck', 'coltrane'],
        '1961': ['village'], '1962': ['getz', 'gilberto'], '1965': ['coltrane'], '1970': ['miles-davis'], '1970s': ['berklee', 'berkleepc', 'leadsheet', 'sheetmusic'],
        '1975': ['koln'], '1987': ['capitol'], '2004': ['leadsheet', 'sheetmusic', 'fakebook', 'berkleepc']}
def tlph(y):
    for k in TLPH.get(y, []):
        if META.get(k): return META[k]
    return None
TLPH.update({'2008': ['herbie-hancock'], '2011': ['esperanza'], '2015': ['kamasi']})
EXH = []
for n, (y, ti, d, st) in enumerate(TIMELINE):
    era, more, (song, sn), ppl = TL_MORE[y]
    ph = tlph(y)
    if PW: more, song, sn = '', '', ''
    EXH.append({'id': 'y' + y, 'y': y, 't': ti, 'd': d, 'm': more, 'era': era, 'song': song, 'sn': sn, 'lk': PW,
                'img': ('img/' + ph['file']) if ph else '', 'cr': credit(ph) if ph else '',
                'st': ({'href': f'story/{st}.html', 't': BYSLUG[st]['title']} if st else None),
                'pp': [{'id': x, 'n': PBY[x][1], 'img': ('img/' + META[PPH.get(x, x)]['file']) if META.get(PPH.get(x, x)) else ''} for x in ppl if x in PBY]})
halls = ''
hnav = ''
for hi, (eid, ename) in enumerate(ERAS):
    hn, yrs, intro = HALLS[eid]
    no, nm = hn.split('　')
    hnav += f'<a href="#hall-{eid}" data-h="{eid}"><b>{e(no)}</b><span>{e(nm)}</span></a>'
    evs = ''
    for x in [x for x in EXH if x['era'] == eid]:
        fig = f'<figure class="evpic"><img src="{x["img"]}" alt="" loading="lazy"><figcaption>{e(x["cr"])}</figcaption></figure>' if x['img'] else f'<figure class="evpic none"><span>{e(x["y"])}</span></figure>'
        evs += (f'<article class="ev{" has" if x["st"] else ""} wp" id="{x["id"]}"><button class="evbtn" data-id="{x["id"]}" aria-label="打開展品：{e(x["t"])}"></button>'
                f'<div class="evt"><div class="yr">{e(x["y"])}</div><h3>{e(x["t"])}</h3><p>{e(x["d"])}</p><span class="open">看展品說明＋先聽一首</span></div>{fig}</article>')
    halls += (f'<section class="hall" id="hall-{eid}" data-h="{eid}"><header class="hallhead"><span class="no">{e(no)}・{e(yrs)}</span><h2>{e(nm)}</h2><p>{e(intro)}</p></header>'
              f'<div class="tl">{evs}</div></section>')
exjs = json.dumps(EXH, ensure_ascii=False)
EXHJS = r"""<script>(function(){var X=__X__,dlg=document.getElementById('exhibit'),cur=-1;
function q(s){return encodeURIComponent(s)}
function show(i){cur=(i+X.length)%X.length;var x=X[cur];
 dlg.querySelector('.xi').innerHTML=x.img?'<img src="'+x.img+'" alt=""><small>'+x.cr+'</small>':'<div class="ph">'+x.y+'</div>';
 dlg.querySelector('.xy').textContent=x.y;dlg.querySelector('.xt').textContent=x.t;dlg.querySelector('.xd').textContent=x.d;dlg.querySelector('.xm').textContent=x.m;
 dlg.querySelector('.xs').innerHTML='<b>先聽一首：〈'+x.song+'〉</b><span>'+x.sn+'</span><span class="lk"><a target="_blank" rel="noopener" href="https://music.apple.com/search?term='+q(x.song)+'">Apple Music</a><a target="_blank" rel="noopener" href="https://open.spotify.com/search/'+q(x.song)+'">Spotify</a></span>';
 if(x.lk){dlg.querySelector('.xs').innerHTML='<a class="btn" href="members.html">🔒 展品完整說明與先聽一首：深夜場會員限定</a>'}
 dlg.querySelector('.xp').innerHTML=(x.pp.length?'<h4>這件展品裡的人</h4>'+x.pp.map(function(p){return '<a href="people.html#'+p.id+'">'+(p.img?'<img src="'+p.img+'" alt="">':'')+p.n+'</a>'}).join(''):'')+(x.st?'<a class="story" href="'+x.st.href+'">讀完整故事：'+x.st.t+'</a>':'');
 dlg.querySelector('.xc').textContent='展品 '+(cur+1)+' / '+X.length;
 if(!dlg.open)dlg.showModal();dlg.querySelector('.xbody').scrollTop=0;history.replaceState(null,'','#'+x.id)}
document.querySelectorAll('.evbtn').forEach(function(b){b.addEventListener('click',function(){show(X.findIndex(function(x){return x.id===b.dataset.id}))})});
dlg.querySelector('.xprev').onclick=function(){show(cur-1)};dlg.querySelector('.xnext').onclick=function(){show(cur+1)};
dlg.querySelector('.xclose').onclick=function(){dlg.close()};
dlg.addEventListener('click',function(ev){if(ev.target===dlg)dlg.close()});
dlg.addEventListener('close',function(){history.replaceState(null,'',location.pathname);var el=document.getElementById(X[cur].id);if(el)el.scrollIntoView({block:'center'})});
document.addEventListener('keydown',function(ev){if(!dlg.open)return;if(ev.key==='ArrowRight')show(cur+1);if(ev.key==='ArrowLeft')show(cur-1)});
var h=location.hash.slice(1),hi=X.findIndex(function(x){return x.id===h});if(hi>-1)setTimeout(function(){show(hi)},200);
var nav=document.querySelectorAll('.hallnav a'),bar=document.querySelector('.hallnav i');
var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){nav.forEach(function(a){a.classList.toggle('on',a.dataset.h===en.target.dataset.h);if(a.dataset.h===en.target.dataset.h&&a.scrollIntoView)a.parentNode.scrollTo({left:a.offsetLeft-20,behavior:'smooth'})})}})},{rootMargin:'-45% 0px -50% 0px'});
document.querySelectorAll('.hall').forEach(function(s){io.observe(s)});
addEventListener('scroll',function(){var m=document.getElementById('exhibition'),r=m.getBoundingClientRect(),p=Math.min(1,Math.max(0,(innerHeight*.5-r.top)/r.height));bar.style.transform='scaleX('+p+')'},{passive:true});
if(!matchMedia('(prefers-reduced-motion: reduce)').matches){var ro=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');ro.unobserve(en.target)}})},{rootMargin:'0px 0px -12% 0px'});document.querySelectorAll('.ev').forEach(function(el){el.classList.add('pre');ro.observe(el)})}
})()</script>""".replace('__X__', exjs)
DLG = ('<dialog id="exhibit" aria-label="展品說明"><div class="xbar"><span class="xc"></span><button class="xclose" aria-label="關閉">✕</button></div><div class="xbody"><div class="xi"></div>'
       '<div class="xtx"><div class="xy"></div><h2 class="xt"></h2><p class="xd"></p><p class="xm"></p><div class="xs"></div><div class="xp"></div></div></div>'
       '<div class="xnav"><button class="xprev">← 上一件</button><button class="xnext">下一件 →</button></div></dialog>')
W('', 'timeline.html', HEAD.format(title='爵士一百年線上展｜爵士101', desc='像逛一個展：從紐奧良的街頭到今天，六個展廳、二十多件展品，每件都能點開看說明、先聽一首。', p='', ogimg='') + nav('', 'timeline') +
  phead('爵士一百年，一個線上展。', '從紐奧良的街頭，走到今天。六個展廳，按順序逛；每一件展品都可以點開，看說明、先聽一首。') +
  f'<nav class="hallnav" aria-label="展廳">{hnav}<i aria-hidden="true"></i></nav><div class="wrap exhibition" id="exhibition">{halls}</div>{DLG}' + letter() + foot('', EXHJS))

# ---------- 選品 ----------
sh = ''
for (cat, desc, items) in SHOP:
    its = ''.join(f'<div class="item"><b>{e(n)}</b><p>{e(d)}</p><div class="lk"><a href="https://www.google.com/search?q={e(q(k))}" target="_blank" rel="noopener">搜尋這個</a></div></div>' for n, d, k in items)
    sh += f'<h2>{e(cat)}</h2><p class="sd">{e(desc)}</p><div class="items">{its}</div>'
W('', 'shop.html', HEAD.format(title='選品｜爵士101', desc='開始聽爵士需要的唱片、書和器材。', p='', ogimg='') + nav('', 'shop') +
  phead('開始聽爵士，需要的東西不多。', '幾張唱片、一兩本書、一副能聽見貝斯的耳機。這裡是我們挑的起點。') +
  f'<div class="wrap"><div class="shop">{sh}</div><p class="note2">爵士101 自己的周邊（帆布袋、明信片、唱片標籤貼紙）正在設計中，做好會先通知電子報讀者。</p></div>' + letter() + foot())

# ---------- 深夜場（只在試做版） ----------
if PW:
    BEN = [('📖','網站完整版','線上展每件展品的完整說明與先聽一首、6 篇長篇故事全文、15 位樂手完整介紹、入門路線 10 張全部。'),
           ('🎧','每週導聆課','一張唱片照時間碼帶著聽：「2:14 貝斯開始跟鋼琴對話」，附 Jim 的一段話。'),
           ('🗓','台北爵士週報','每週五：本週 3–5 場演出精選、對新手友善的酒吧、低消資訊。'),
           ('🎹','全部聲音示範','10 個可以按的示範全開，每月新增 1 個。'),
           ('🗣','展廳語音導覽','每個展廳 1 分鐘耳機導覽，像真的在美術館。'),
           ('🎷','伴奏音軌','藍調、二五一、標準曲和弦進行，可調速度，拿樂器跟著練即興。'),
           ('📀','每期歌單','跟著導聆課一起聽的 Spotify／Apple Music 歌單。'),
           ('📕','唱片小冊 PDF','每月一張唱片做成可列印的小冊。'),
           ('🖼','展品桌布','手機與電腦桌布，每年一張年度海報。'),
           ('⏩','新展品搶先看','新故事、新展廳先給會員看一週。'),
           ('🗳','選題投票','決定下個月的導聆課和新展品。'),
           ('✉️','讀者問答','每月挑會員的問題回答一封。'),
           ('💬','會員社群','分享這週聽了什麼。'),
           ('🎟','聽音樂會','每月線上一起聽；每季一場黑膠聽音會，會員優先、折扣。'),
           ('🏷','合作店家優惠','唱片行、爵士酒吧、樂器行的會員折扣。')]
    bens = ''.join(f'<div class="ben"><i aria-hidden="true">{a}</i><div><b>{e(b)}</b><p>{e(c)}</p></div></div>' for a, b, c in BEN)
    plans = ('<div class="plans">'
             '<div class="plan"><b>慢慢聽</b><div class="pr">免費</div><p>雙週電子報、網站預覽、小辭典、三個聲音示範。</p></div>'
             '<div class="plan hot"><b>深夜場・月繳</b><div class="pr">NT$150<small>／月</small></div><p>上面 15 項權益全部。</p></div>'
             '<div class="plan"><b>深夜場・年繳</b><div class="pr">NT$1,500<small>／年</small></div><p>等於送兩個月。前 100 位創始會員 NT$1,200，續訂不漲價。</p></div>'
             '<div class="plan"><b>贊助者</b><div class="pr">NT$3,600<small>／年</small></div><p>每年一場實體聽音會免費、名字列在線上展贊助牆。</p></div></div>')
    W('', 'members.html', HEAD.format(title='深夜場｜爵士101 會員', desc='爵士101 會員方案：完整線上展、每週導聆課、台北爵士週報。', p='', ogimg='') + nav('', 'members') +
      phead('深夜場：陪你把爵士聽進去。', '免費的部分告訴你發生了什麼；會員有人帶著聽、知道這週台北去哪聽、到現場一起聽。') +
      f'<div class="wrap" style="max-width:900px">{plans}<section class="sec"><h2>會員可以拿到的 15 件事</h2><div class="bens">{bens}</div></section>'
      f'<p class="note2">會員方案準備中，開放時會先通知電子報讀者和 IG 追蹤者。</p></div>' + letter() + foot())

# ---------- 節奏遊戲 ----------
from rhythm_data import RHY
_SHT = {x['ep']: x['title'] for x in json.load(open(os.path.join(HERE, 'shorts.json'), encoding='utf-8'))}
_rj = [dict(r, n=i + 1, eptitle=_SHT.get(r['ep'], '')) for i, r in enumerate(RHY)]
PLAYSVG = '<svg viewBox="0 0 14 14" aria-hidden="true"><path d="M3 1.5v11l9-5.5z" fill="currentColor"/></svg>'
def pbtn(i, label, cls='dplay', extra=''):
    return f'<button class="{cls}" id="{i}" data-l="{label}" aria-pressed="false"{extra}>{PLAYSVG}<span>{label}</span></button>'
lvmap = ''.join(f'<a class="lvl" data-id="{r["id"]}" href="#{r["id"]}"><em>{r["n"]}</em><b>{e(r["name"])}</b><span>{e(r["en"])}</span><span class="st"></span></a>' for r in _rj)
gab = ''.join(f'<div><button class="dplay gplay" data-w="{w}" data-l="聽 {w}" aria-pressed="false">{PLAYSVG}<span>聽 {w}</span></button><button class="gans" data-w="{w}">是 {w}</button></div>' for w in 'AB')
RPAGE = (HEAD.format(title='節奏遊戲｜爵士101', desc='爵士樂的九種節奏，九關：先聽、再跟著拍、最後用耳朵猜。搖擺、shuffle、巴薩諾瓦、clave、5/4、放克、自由爵士。', p='', ogimg='') + nav('', 'rhythm') +
  phead('九種節奏，九關。', '爵士不只有搖擺。九關，每關三步：先聽、再跟著拍、最後用耳朵猜。音樂都在你的瀏覽器裡現場演奏，建議戴耳機或開喇叭。') +
  f'<div class="wrap rgame"><div class="lvmap">{lvmap}</div><p class="tot" id="tot"></p>'
  '<section class="rstage" id="stage" aria-label="關卡"><div class="rs-head"><small id="lvnum"></small><h2 id="lvname"></h2><span class="en" id="lven"></span><p id="lvone"></p></div>'
  '<div class="steps"><button data-s="listen">1 聽</button><button data-s="tap">2 跟拍</button><button data-s="guess">3 猜</button></div>'
  '<div class="rs-body"><div class="rs-wheel"><canvas id="wheel" role="img" aria-label="節奏圈：一圈是一段循環，金色的點是要拍的地方"></canvas><div class="tapzone" id="tapzone" hidden><button class="tapbtn" id="tapbtn">拍</button><div class="tapline"><p id="tapfb" class="tapfb" aria-live="polite"></p><span id="tapcount" class="tapcount"></span></div><p class="kbd">用電腦可以按空白鍵。</p></div></div><div class="rs-side">'
  f'<div class="pane" data-s="listen"><p id="lslisten"></p><div class="dctl">{pbtn("lplay", "播放")}<button class="btn2" id="tonext">下一步：跟著拍</button></div></div>'
  f'<div class="pane" data-s="tap" hidden><p id="tapinfo"></p><div class="dctl">{pbtn("tstart", "開始")}</div>'
  '<div id="tapres" class="res" hidden><b id="tappct"></b><p id="tapverdict"></p><p id="tapmsg" class="meta"></p><button class="btn2" id="tapnext">下一步：猜</button></div></div>'
  f'<div class="pane" data-s="guess" hidden><p id="gq"></p><div class="gab">{gab}</div><p id="gfb" class="gfb" aria-live="polite"></p><button class="btn2" id="gnext" hidden>下一題</button>'
  '<div id="gres" class="res" hidden><b id="gresT"></b><div class="dctl"><button class="dplay" id="gresN"></button><button class="btn2" id="gretry">再玩一次</button></div></div></div>'
  '<div class="rs-more"><p><b>冷知識</b><span id="lvfact"></span></p><p><b>去聽這兩首</b><span id="lvsongs"></span></p><p id="lvep"></p></div>'
  '</div></div></section>'
  f'<section class="sec exam"><h2>總複習：九選一</h2><p class="lede">隨機放一段，你猜是哪一種。一共十題，九關還沒玩完也可以先考。</p>{pbtn("xstart", "開始考")}'
  f'<div id="xbox" hidden><p id="xq"></p>{pbtn("xplay", "再聽一次")}<div id="xopts" class="xopts"></div><p id="xfb" aria-live="polite"></p><button class="btn2" id="xnext" hidden>下一題</button></div><div id="xend" hidden><b id="xendT"></b></div></section>'
  '<details class="latset"><summary>拍子總是對不上？</summary><p>藍牙耳機會讓聲音晚一點才到。系統已經自動扣掉一部分；如果你一直被判「晚了」，把這裡往右調，一直被判「早了」就往左。</p>'
  '<label>補償 <input type="range" id="lat" min="-100" max="250" step="10" value="0"> <output id="latv">0 ms</output></label></details></div>'
  + letter() + f'<script>window.RHY={json.dumps(_rj, ensure_ascii=False)};</script><script src="rhythm.js"></script>' + foot())
W('', 'rhythm.html', RPAGE)
RHMINI = ''.join(f'<a href="rhythm.html#{r["id"]}"><em>{r["n"]}</em><b>{e(r["name"])}</b></a>' for r in _rj)

# ---------- 和聲遊戲 ----------
from harmony_data import HAR
_hj = [dict(r, n=i + 1, eptitle=_SHT.get(r['ep'], '')) for i, r in enumerate(HAR)]
_hcard = lambda r: f'<a class="lvl" data-id="{r["id"]}" href="#{r["id"]}"><em>{r["n"]}</em><b>{e(r["name"])}</b><span>{e(r["en"])}</span><span class="st"></span></a>'
_tdesc = {'入門': '沒學過樂理從這裡開始：音、家、和弦、五度圈。', '基礎': '爵士最常聽到的三件事。', '進階': '樂手們真正在玩的東西。'}
hmap = ''.join(f'<h3 class="tier">{t}<span>{_tdesc[t]}</span></h3><div class="lvmap t{len([x for x in _hj if x["tier"] == t])}">' + ''.join(_hcard(r) for r in _hj if r['tier'] == t) + '</div>' for t in ['入門', '基礎', '進階'])
HSTORY = ('<section class="hstory"><h2>爵士樂發明了所有的和弦嗎？</h2>'
  '<p>常聽到這句話，但不是真的。屬七和弦在巴哈的年代就到處都是；九和弦這類更濃的和弦，德布西、拉威爾在 1900 年前後也已經大量寫進曲子裡。</p>'
  '<p>爵士做的事情是另一件：把這些「濃」的和弦變成每天都在用的家常菜，並且和流行樂手一起，把和弦整理成一套樂手之間的速記，例如 Cmaj7、G7、Dm7。拿到一張只寫旋律和這些代號的譜，樂手就能當場彈出一整首歌。</p>'
  '<p>Bill Evans 這類受過古典訓練的鋼琴手，常說自己從德布西、拉威爾學到和聲的顏色，再帶進俱樂部，所以爵士聽起來常常像古典印象派，只是多了搖擺。</p></section>')
HPAGE = (HEAD.format(title='和聲遊戲｜爵士101', desc='沒學過樂理也能玩：十二個音、調性、和弦、五度圈，一路聽到二五一、藍調、轉調和 Giant Steps。', p='', ogimg='') + nav('', 'harmony') +
  phead('用耳朵學和弦。', '從十二個音、調性、和弦、五度圈開始，一路聽到 Giant Steps。不用看譜，每關先聽、再考，畫面會亮給你看聲音走到哪裡。建議戴耳機。') +
  f'<div class="wrap rgame">{hmap}<p class="tot" id="tot"></p>'
  '<section class="rstage" id="stage" aria-label="關卡"><div class="rs-head"><small id="lvnum"></small><h2 id="lvname"></h2><span class="en" id="lven"></span><p id="lvone"></p></div>'
  '<div class="steps"><button data-s="listen">1 聽</button><button data-s="quiz">2 考</button></div>'
  '<div class="rs-body"><div class="rs-wheel"><canvas id="wheel" role="img" aria-label="五度圈：亮起的是現在的和弦根音，線是剛剛走過的路"></canvas></div><div class="rs-side">'
  '<div class="pane" data-s="listen"><p id="lslisten"></p><div class="hdemos" id="demos"></div><div class="dctl"><button class="btn2" id="tonext">下一步：考考耳朵</button></div></div>'
  f'<div class="pane" data-s="quiz" hidden><p id="hq" class="hq"></p><div class="dctl">{pbtn("hplay", "再聽一次")}</div><div class="hopts" id="hopts"></div><p id="hfb" class="gfb" aria-live="polite"></p><button class="btn2" id="hnext" hidden>下一題</button>'
  '<div id="hres" class="res" hidden><b id="hresT"></b><div class="dctl"><button class="dplay" id="hresN"></button><button class="btn2" id="hretry">再考一次</button></div></div></div>'
  '<div class="rs-more"><p><b>冷知識</b><span id="lvfact"></span></p><p><b>去聽</b><span id="lvsongs"></span></p><p id="lvep"></p></div>'
  '</div></div></section>' + HSTORY + '<p class="tot" style="margin-top:40px">也玩玩看<a href="rhythm.html" style="color:var(--brass)">節奏遊戲</a>：九種爵士節奏，跟著拍。</p></div>'
  + letter() + f'<script>window.HAR={json.dumps(_hj, ensure_ascii=False)};</script><script src="harmony.js"></script>' + foot())
W('', 'harmony.html', HPAGE)
HMINI = ''.join(f'<a href="harmony.html#{r["id"]}"><em>{r["n"]}</em><b>{e(r["name"])}</b></a>' for r in _hj[:9])

# ---------- 首頁 ----------
f0 = S[0]
rows = ''.join(f'<a class="row" href="story/{s["slug"]}.html"><div class="y">{e(s["year"])}</div><div><h3>{e(s["title"])}</h3><p>{e(s["dek"])}</p></div>{img(s["ph"], "", "t", s["title"], S.index(s))}</a>' for s in sorted(S, key=lambda x: x['year']))
soon = ''.join(f'<li>{e(t)}</li>' for t in COMING)
fph = f0['ph']
fig = f'<figure><img src="img/{fph["file"]}" alt="{e(f0["title"])}"><figcaption>{credit(fph)}</figcaption></figure>' if fph else '<div class="yearbig">' + e(f0['year']) + '</div>'
doors = ('<div class="doors">'
         f'<a href="#stories"><b>讀故事</b><span>{len(S)} 篇長篇，每篇兩三千字，附「這樣聽」。</span><i>從這裡開始</i></a>'
         '<a href="start.html"><b>照路線聽</b><span>第一次聽爵士，十張唱片照順序聽。</span><i>入門路線</i></a>'
         '<a href="listen.html"><b>用耳朵學</b><span>十個可以按的聲音示範，搖擺、藍調、二五一。</span><i>聽懂爵士</i></a>'
         f'<a href="words.html"><b>查名詞</b><span>{len(WORDS)} 個名詞，用白話講清楚。</span><i>小辭典</i></a></div>')
pmini = ''.join(f'<a href="start.html"><div class="disc2" style="--c:{COL[n % len(COL)]}" aria-hidden="true"></div><b>{n+1}．《{e(a)}》</b><span>{e(b)}・{e(y)}</span></a>' for n, (a, b, y, *_r) in enumerate(START[:6]))
tlm = ''.join(f'<a href="timeline.html#y{y}" class="{"has" if st else ""}">{(f"<img src='img/{tlph(y)['file']}' alt='' loading='lazy'>" if tlph(y) else "")}<b>{e(y)}</b><span>{e(t)}</span></a>' for (y, t, d, st) in TIMELINE)

# ---------- 一分鐘故事（IG 40 集的網站版）----------
from shorts_deep import DEEP, FREE as SHORT_FREE
SH = json.load(open(os.path.join(HERE, 'shorts.json'), encoding='utf-8'))
os.makedirs(os.path.join(OUT, 'short'), exist_ok=True)
os.makedirs(os.path.join(OUT, 'img', 'short'), exist_ok=True)
for x in SH:
    for ph in x['photos']:
        shutil.copy(os.path.join(IMGSRC, ph['file']), os.path.join(OUT, 'img', ph['file']))
def shcredit(ph):
    return f'照片：{e(ph["artist"])}，{e(ph["license"])}，{e(ph["src"])}'
open(os.path.join(OUT, 'style.css'), 'a', encoding='utf-8').write(r"""
.shgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:22px;margin-top:34px}
.shc{text-decoration:none;color:var(--ink);display:block}
.shc .im{aspect-ratio:4/3;border-radius:16px;overflow:hidden;background:var(--wash);position:relative}
.shc img{width:100%;height:100%;object-fit:cover;filter:saturate(.92);transition:transform .5s}
.shc:hover img{transform:scale(1.04)}
.shc .no{position:absolute;left:10px;top:10px;background:rgba(18,18,20,.72);color:#f3e7d3;font-size:12px;padding:3px 9px;border-radius:999px;letter-spacing:.04em}
.shc .tag{position:absolute;right:10px;top:10px;background:#d6aa60;color:#1d1408;font-size:12px;padding:3px 9px;border-radius:999px}
.shc b{display:block;font-size:17px;margin-top:12px;line-height:1.4}
.shc p{color:var(--graphite);font-size:14px;line-height:1.7;margin-top:4px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.shead{max-width:720px;margin:0 auto;padding:56px 22px 10px}
.shead small{color:var(--brass);font-size:13px;letter-spacing:.06em}
.shead h1{font-size:clamp(30px,6vw,46px);line-height:1.2;margin-top:8px}
.shead .dek{font-size:19px;line-height:1.7;color:var(--graphite);margin-top:14px}
.shero{max-width:860px;margin:26px auto 0;padding:0 22px}
.shero img{width:100%;border-radius:20px;max-height:560px;object-fit:cover}
.shero .credit{font-size:12px;color:var(--graphite);margin-top:8px}
.sbody{max-width:680px;margin:0 auto;padding:10px 22px}
.sbody h2{font-size:22px;margin:44px 0 14px}
.sbody p{font-size:18px;line-height:2;margin-bottom:16px}
.sbody figure{margin:28px 0}.sbody figure img{width:100%;border-radius:16px}.sbody figcaption{font-size:12px;color:var(--graphite);margin-top:6px}
.full{border-top:1px solid var(--hair);margin-top:40px}
.full .badge{display:inline-block;font-size:12px;color:var(--brass);border:1px solid var(--brass);border-radius:999px;padding:2px 10px;margin-top:34px}
.lis{background:var(--wash);border-radius:18px;padding:20px 22px;margin:10px 0 24px}
.lis b{font-size:18px}.lis p{font-size:16px;margin:6px 0 10px;line-height:1.8}
.lis a{color:var(--brass);text-decoration:none;margin-right:16px;font-size:14px}
.sbody details{border:1px solid var(--hair);border-radius:14px;padding:14px 18px;margin:14px 0}
.sbody summary{cursor:pointer;font-weight:600}
.sbody .en p{font-size:15px;line-height:1.8;color:var(--graphite);margin:8px 0}
.sbody .notes{font-size:14px;line-height:1.9;color:var(--graphite)}
.sbody .notes a{color:var(--brass);word-break:break-all}
""")
def short_page(i, x):
    ep = x['ep']; free = ep in SHORT_FREE
    deep, (song, point) = DEEP[ep]
    z = x['zh']; n = len(z); a = max(1, n // 3); b = max(a + 1, 2 * n // 3)
    paras = [''.join(z[:a]), ''.join(z[a:b]), ''.join(z[b:])]
    ph = x['photos']
    body = f'<h2>故事</h2>' + ''.join(f'<p>{e(t)}</p>' for t in paras[:2])
    if len(ph) > 1:
        body += f'<figure><img src="../img/{ph[1]["file"]}" alt="" loading="lazy"><figcaption>{shcredit(ph[1])}</figcaption></figure>'
    body += f'<p>{e(paras[2])}</p>'
    full = '<section class="full"><span class="badge">完整版</span>'
    if PW and not free:
        full += LOCK('../', '這篇的完整版') + '</section>'
    else:
        full += '<h2>故事後面</h2>' + ''.join(f'<p>{e(t)}</p>' for t in deep)
        if len(ph) > 2:
            full += f'<figure><img src="../img/{ph[2]["file"]}" alt="" loading="lazy"><figcaption>{shcredit(ph[2])}</figcaption></figure>'
        full += f'<h2>這樣聽</h2><div class="lis"><b>{e(song)}</b><p>{e(point)}</p>{links(song)}</div>'
        full += '<details class="en"><summary>逐句英文</summary>' + ''.join(f'<p>{e(t)}</p>' for t in x['en']) + '</details>'
        full += '<details><summary>查證筆記與出處</summary><div class="notes"><p>' + e(x['note']) + '</p><p>' + '<br>'.join(f'<a href="{e(u)}" target="_blank" rel="noopener">{e(u)}</a>' for u in x['srcs']) + '</p></div></details></section>'
    prev = SH[i - 1] if i > 0 else None; nxt = SH[i + 1] if i < len(SH) - 1 else None
    pn = '<div class="pn">' + (f'<a href="ep{prev["ep"]}.html"><small>上一則</small>{e(prev["title"])}</a>' if prev else '<span></span>') + (f'<a href="ep{nxt["ep"]}.html"><small>下一則</small>{e(nxt["title"])}</a>' if nxt else '<span></span>') + '</div>'
    hero = f'<div class="shero"><img src="../img/{ph[0]["file"]}" alt="{e(x["title"])}"><p class="credit">{shcredit(ph[0])}</p></div>' if ph else ''
    page = HEAD.format(title=e(x['title']) + '｜爵士101 一分鐘故事', desc=e(x['hook']), p='../', ogimg=(f'<meta property="og:image" content="../img/{ph[0]["file"]}">' if ph else '')) + nav('../', 'shorts') + \
        f'<header class="shead"><small>一分鐘故事 No.{ep}</small><h1>{e(x["title"])}</h1><p class="dek">{e(x["hook"])}</p></header>{hero}' + \
        f'<article class="sbody">{body}{full}<p class="src">一分鐘影片版在 Instagram <a href="{IG}" target="_blank" rel="noopener">@jazz101tw</a>。</p></article>{pn}{letter()}' + foot('../')
    W('../', os.path.join('short', f'ep{ep}.html'), page)
for i, x in enumerate(SH): short_page(i, x)
def shcard(x, pre=''):
    ph = x['photos'][0] if x['photos'] else None
    tag = ('<span class="tag">免費全文</span>' if x['ep'] in SHORT_FREE else '<span class="tag">🔒 完整版</span>') if PW else ''
    im = f'<img src="{pre}img/{ph["file"]}" alt="" loading="lazy">' if ph else ''
    return f'<a class="shc" href="{pre}short/ep{x["ep"]}.html"><div class="im">{im}<span class="no">No.{x["ep"]}</span>{tag}</div><b>{e(x["title"])}</b><p>{e(x["hook"])}</p></a>'
W('', 'shorts.html', HEAD.format(title='一分鐘故事｜爵士101', desc='IG 上的一分鐘爵士故事，網站版：故事全文、真實照片、延伸背景、這樣聽、出處。', p='', ogimg='') + nav('', 'shorts') +
  '<div class="wrap">' + phead('一分鐘故事', 'IG 上一分鐘講完的爵士故事，這裡放全文和照片。每一則還有「完整版」：故事後面的背景、該聽哪一首、逐句英文和出處。') +
  f'<div class="shgrid">{"".join(shcard(x) for x in SH)}</div></div>' + letter() + foot())
SHMINI = ''.join(shcard(x) for x in SH[:6])
peo = ''.join(f'<a href="people.html#{p[0]}">{portrait(p[0], p[1], p[4], n)}<b>{e(p[1])}</b><span>{e(p[4])}・{e(p[3])}</span></a>' for n, p in enumerate(PEOPLE[:8]))
wjs = json.dumps([[w[0], w[1], w[2], w[3]] for w in WORDS], ensure_ascii=False)
shopmini = ''.join(f'<div class="item"><b>{e(n)}</b><p>{e(d)}</p></div>' for n, d, k in [SHOP[0][2][3], SHOP[1][2][0], SHOP[2][2][0]])
index = HEAD.format(title='爵士101｜一分鐘講不完的爵士故事', desc='爵士史上的人、晚上和唱片，一篇講完整，附上該怎麼聽。還有入門路線、聲音示範、樂手和名詞小辭典。', p='', ogimg='') + nav('') + \
    '<section class="hero"><h1><span class="nw">一分鐘講不完的爵士，</span><span class="nw">在這裡慢慢聽。</span></h1><p>那些錄音室、俱樂部和唱片背後的故事，一篇講完，再告訴你該聽哪一段。</p>' + \
    '<div class="ctas"><a class="btn" href="#stories">開始讀故事</a><a class="btn alt" href="start.html">第一次聽？從這裡</a></div>' + \
    '<div class="glow" aria-hidden="true"></div><div class="stage" id="stage"><div class="platter"><div class="disc"></div><div class="label"><div><b>JAZZ 101</b><span>Side A　ii–V–I</span></div></div></div><div class="arm"><i></i></div></div>' + \
    '<button class="play" id="play" aria-pressed="false"><svg viewBox="0 0 14 14" aria-hidden="true"><path d="M3 1.5v11l9-5.5z" fill="currentColor"/></svg><span>放一段二五一</span></button>' + \
    '<p class="playnote">爵士樂最常聽到的和弦進行，用瀏覽器現場彈給你聽。</p></section>' + \
    f'<div class="wrap">{doors}</div>' + \
    f'<section class="band"><div class="in">{fig}<div><small>這次先讀這篇</small><h2>{e(f0["title"])}</h2><p>{e(f0["dek"])}</p><a class="btn" href="story/{f0["slug"]}.html">讀這篇故事</a></div></div></section>' + \
    f'<div class="wrap"><section class="sec" id="stories"><h2>所有故事</h2><p class="lede">依年份排列的人、晚上和唱片。每一篇都附上「這樣聽」。</p><div class="list">{rows}</div></section>' + \
    f'<section class="sec"><h2>一分鐘故事</h2><p class="lede">IG 上一分鐘講完的故事，這裡有全文、照片和延伸背景。</p><div class="shgrid">{SHMINI}</div><a class="more-link" href="shorts.html">看全部 {len(SH)} 則</a></section>' + \
    f'<section class="sec"><h2>第一次聽，照這個順序。</h2><p class="lede">十張唱片，一張比一張多一點東西。每張先聽一首就好。</p><div class="pathmini">{pmini}</div><a class="more-link" href="start.html">看完整的入門路線</a></section></div>' + \
    f'<section class="band"><div class="in" style="display:block"><small>聽懂爵士</small><h2>先按下去，再讀解釋。</h2><p>同一段旋律，直的和搖擺的差在哪裡？十二小節藍調長什麼樣子？用瀏覽器現場彈給你聽。</p>' + \
    f'<div class="demos">{demo_card("swing")}{demo_card("blues")}</div><a class="btn" href="listen.html">聽全部十個示範</a></div></section>' + \
    f'<div class="wrap"><section class="sec"><h2>爵士有九種走路的方式。</h2><p class="lede">搖擺、shuffle、巴薩諾瓦、5/4……九關節奏遊戲，每關先聽、再跟著拍、最後用耳朵猜。</p><div class="rhmini">{RHMINI}</div><a class="more-link" href="rhythm.html">開始玩節奏遊戲</a></section><section class="sec"><h2>和弦也可以用耳朵學。</h2><p class="lede">沒學過樂理也能玩：從十二個音、調性和五度圈開始，一路聽到 Giant Steps。</p><div class="rhmini">{HMINI}</div><a class="more-link" href="harmony.html">開始玩和聲遊戲</a></section></div>' + \
    f'<div class="wrap"><section class="sec"><h2>逛一個爵士一百年的展。</h2><p class="lede">六個展廳、二十多件展品，從紐奧良的街頭走到今天。點任何一件，就能看說明、先聽一首。</p><div class="tlmini">{tlm}</div><a class="more-link" href="timeline.html">走進線上展</a></section>' + \
    f'<section class="sec"><h2>先認識這些人。</h2><p class="lede">每個人一句話、一首歌。</p><div class="pmini">{peo}</div><a class="more-link" href="people.html">看全部 {len(PEOPLE)} 位樂手</a></section>' + \
    '<section class="sec"><h2>今天學一個詞。</h2><div class="today" id="today"><div><h3 id="tw"></h3><p id="tx"></p></div><div><button id="tn">換一個</button></div></div><a class="more-link" href="words.html">打開小辭典</a></section>' + \
    f'<section class="sec"><h2>開始聽，需要的東西不多。</h2><p class="lede">幾張唱片、一本書、一副能聽見貝斯的耳機。</p><div class="items">{shopmini}</div><a class="more-link" href="shop.html">看全部選品</a></section>' + \
    f'<section class="sec"><h2>正在寫的故事</h2><p class="lede">IG 上已經講過一分鐘版本，長篇陸續放上來。</p><ul class="soon">{soon}</ul></section></div>' + \
    letter() + '<script src="player.js"></script>' + AUD('') + \
    '<script>(function(){var W=' + wjs + ',i=Math.floor(Math.random()*W.length);function s(){var w=W[i%W.length];document.getElementById("tw").innerHTML=w[1]+"<small>"+w[2]+"</small>";document.getElementById("tx").textContent=w[3];document.getElementById("today").onclick=null}s();document.getElementById("tn").onclick=function(){i++;s()}})()</script>' + foot()
W('', 'index.html', index)
total = sum(s['chars'] for s in S)
print('ok', len(S), 'stories,', total, '字;', len(PEOPLE), 'people;', len(WORDS), 'words;', len(TIMELINE), 'events;', 'out=', OUT)

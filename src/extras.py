# 爵士101 其他內容：樂手、名詞、時間軸、入門路線、選品
# 事實以 Wikipedia 與唱片資訊為準；查不到的不寫。

# 樂手：slug, 名字, 中文稱呼, 生卒, 樂器, 一句話, 介紹, 先聽(曲, 唱片)
PEOPLE = [
("louis-armstrong", "Louis Armstrong", "路易斯・阿姆斯壯", "1901–1971", "小號、人聲", "把爵士從合奏變成獨奏的人。",
 "在紐奧良長大，少年時期在感化院學會吹短號。1920 年代他的 Hot Five 和 Hot Seven 錄音，讓「一個人站出來即興獨奏」成了爵士的核心。他也是最早用沒有歌詞的聲音即興唱歌（scat）的名人之一。晚年的〈What a Wonderful World〉讓不聽爵士的人也認識他。",
 ("West End Blues", "1928 年 Hot Five 錄音")),
("duke-ellington", "Duke Ellington", "艾靈頓公爵", "1899–1974", "鋼琴、作曲、大樂團", "把大樂團當成一件樂器來寫的作曲家。",
 "1927 年起在哈林區的 Cotton Club 駐場，靠電台轉播紅遍全美。他寫曲子時想的不是「小號」「長號」，而是樂團裡的某一個人，替每位樂手的聲音量身打造。一生寫了上千首作品，從三分鐘的舞曲到長篇組曲。",
 ("Take the ‘A’ Train", "1941 年，Billy Strayhorn 作曲")),
("charlie-parker", "Charlie Parker", "查理・帕克", "1920–1955", "中音薩克斯風", "bebop 的發明者之一，綽號 Bird。",
 "來自堪薩斯市，1940 年代初在紐約哈林區的 Minton's 和 Monroe's 等俱樂部，跟小號手 Dizzy Gillespie 一起把爵士推向更快、更複雜的和聲。他的句子又快又流暢，幾十年後的樂手還在一個音一個音地學。生活很亂，34 歲就過世。",
 ("Ko-Ko", "1945 年錄音")),
("billie-holiday", "Billie Holiday", "比莉・哈樂黛", "1915–1959", "人聲", "聲音不大，但每個字都像真的發生過。",
 "沒有受過正式訓練，音域也不寬，但她唱歌的時間感像管樂手，常常故意晚一點進拍。1939 年唱的〈Strange Fruit〉是一首控訴美國南方私刑的歌，被認為是美國最早的民權歌曲之一。晚年的聲音沙啞了，很多人反而覺得更動人。",
 ("Strange Fruit", "1939 年錄音")),
("ella-fitzgerald", "Ella Fitzgerald", "艾拉・費茲傑羅", "1917–1996", "人聲", "爵士第一夫人，也是 scat 的天后。",
 "十幾歲在哈林區阿波羅劇院的業餘之夜得獎，之後一路唱了六十年。她的音準和節奏近乎完美，1950 年代錄的一系列「歌本」唱片，把美國作曲家的名曲一首首唱成標準版本。1960 年在柏林忘了〈Mack the Knife〉的歌詞，乾脆當場即興編新的，那張現場專輯還得了葛萊美獎。",
 ("Mack the Knife", "《Ella in Berlin》，1960")),
("thelonious-monk", "Thelonious Monk", "瑟隆尼斯・孟克", "1917–1982", "鋼琴、作曲", "聽起來像彈錯，其實每個音都是故意的。",
 "bebop 誕生時就在場，但他的鋼琴跟誰都不像：不和諧的音、突然的停頓、歪歪的節奏。他寫的曲子〈'Round Midnight〉〈Straight, No Chaser〉成了必彈標準曲。他在台上會突然站起來跳舞，也以各式各樣的帽子出名。",
 ("'Round Midnight", "1947 年 Blue Note 錄音")),
("miles-davis", "Miles Davis", "邁爾士・戴維斯", "1926–1991", "小號", "每隔幾年，就帶爵士換一次方向。",
 "十八歲到紐約找 Charlie Parker，從 bebop 起步。之後他帶出了 cool jazz（《Birth of the Cool》）、hard bop、調式爵士（《Kind of Blue》）、電子融合（《Bitches Brew》）。他吹得很少、很省，常說重點是那些沒吹的音。他的樂團也是一所學校：Coltrane、Bill Evans、Herbie Hancock、Wayne Shorter 都從這裡出發。",
 ("So What", "《Kind of Blue》，1959")),
("art-blakey", "Art Blakey", "亞特・布萊基", "1919–1990", "鼓", "帶了三十多年樂團的鼓手，也是年輕樂手的校長。",
 "他的樂團 The Jazz Messengers 是 hard bop 的代表，鼓聲又大又推，每一段都把樂手往前趕。三十多年裡，他不斷找年輕樂手加入，Lee Morgan、Wayne Shorter、Freddie Hubbard、Wynton Marsalis 都在他的樂團成名。",
 ("Moanin'", "《Moanin'》，1958")),
("sonny-rollins", "Sonny Rollins", "桑尼・羅林斯", "1930–", "次中音薩克斯風", "在最紅的時候停下來，上橋練琴兩年。",
 "在哈林區長大，跟 Monk、Bud Powell 是鄰居。1956 年的《Saxophone Colossus》讓他被叫作「薩克斯風巨人」。他的即興會拿一小段旋律反覆變化，被稱為主題式即興。父母來自維京群島，卡利普索的節奏一直在他的音樂裡。",
 ("St. Thomas", "《Saxophone Colossus》，1956")),
("john-coltrane", "John Coltrane", "約翰・柯川", "1926–1967", "次中音、高音薩克斯風", "練琴練到出名，最後把音樂當成禱告。",
 "在 Miles Davis 和 Monk 的樂團裡磨練，1959 年用《Giant Steps》把和弦推到極限，1960 年代組了經典四重奏，往更自由、更靈性的方向走。《A Love Supreme》是他寫給神的一封信。過世時才 40 歲。",
 ("My Favorite Things", "1961 年發行")),
("charles-mingus", "Charles Mingus", "查爾斯・明格斯", "1922–1979", "貝斯、作曲", "脾氣很大的貝斯手，寫出最有情緒的爵士。",
 "他的音樂裡有教會的福音、有藍調、有艾靈頓的大樂團，也有很多憤怒和幽默。他會在台上罵觀眾、停下樂團重來，也寫曲子諷刺種族歧視的政客。《Mingus Ah Um》是最適合入門的一張。",
 ("Better Git It in Your Soul", "《Mingus Ah Um》，1959")),
("bill-evans", "Bill Evans", "比爾・艾文斯", "1929–1980", "鋼琴", "安靜的鋼琴手，改變了三重奏的樣子。",
 "念古典鋼琴出身，1959 年參與《Kind of Blue》並寫了內頁說明。同年組的三重奏讓鋼琴、貝斯、鼓三個人平等對話。他的和弦常常省略根音、堆在中音區，溫暖又有一點霧，影響了之後幾乎所有爵士鋼琴手。",
 ("Waltz for Debby", "《Waltz for Debby》，1961 年錄音")),
("wayne-shorter", "Wayne Shorter", "韋恩・蕭特", "1933–2023", "次中音、高音薩克斯風、作曲", "寫曲子像寫謎語的人。",
 "先後待過 Art Blakey 和 Miles Davis 的樂團，替兩個樂團寫了大量的曲子，〈Footprints〉〈Speak No Evil〉都是。之後和鍵盤手 Joe Zawinul 組了融合樂團 Weather Report。他的旋律常常不按牌理走，但聽幾次就忘不掉。",
 ("Footprints", "《Adam's Apple》，1966")),
("herbie-hancock", "Herbie Hancock", "賀比・漢考克", "1940–", "鋼琴、鍵盤", "從原聲鋼琴一路玩到電子和嘻哈。",
 "小時候是古典神童，二十出頭寫出〈Watermelon Man〉，接著加入 Miles Davis 的第二個經典五重奏。1970 年代用合成器做出放克味的《Head Hunters》，1983 年的〈Rockit〉還上了 MTV。2008 年以向 Joni Mitchell 致敬的專輯拿下葛萊美年度專輯。",
 ("Maiden Voyage", "《Maiden Voyage》，1965")),
("keith-jarrett", "Keith Jarrett", "奇斯・傑瑞", "1945–", "鋼琴", "一個人、一台琴，完全即興整晚。",
 "三歲學琴，待過 Art Blakey、Charles Lloyd 和 Miles Davis 的樂團。1970 年代起跟 ECM 唱片合作，以完全即興的獨奏會聞名，《The Köln Concert》是史上最暢銷的獨奏鋼琴專輯之一。另一面是跟貝斯手 Gary Peacock、鼓手 Jack DeJohnette 合作三十年的三重奏。2018 年中風後停止演出。",
 ("The Köln Concert, Part IIc", "1975 年現場")),
]

# 名詞：id, 名詞, 英文, 白話解釋, 例子, 示範 id
WORDS = [
("swing", "搖擺", "Swing", "爵士最核心的節奏感。兩個八分音符不平均：第一個長一點、第二個短一點，像走路時一跛一跛地往前，聽起來會讓人想點頭。", "Count Basie〈Jumpin' at the Woodside〉", "swing"),
("improvisation", "即興", "Improvisation", "演奏當下才決定要彈什麼。不是亂彈，而是在曲子的和弦和節奏框架裡，用自己學過的語彙即時說話。", "Keith Jarrett《The Köln Concert》", None),
("blues", "藍調", "Blues", "一種十二小節為一輪、反覆循環的曲式，也是一種帶著憂傷的聲音。幾乎所有爵士樂手都會彈藍調，它是爵士的母語之一。", "Miles Davis〈Freddie Freeloader〉", "blues"),
("blue-notes", "藍調音", "Blue notes", "介於大調和小調之間、聽起來有點「歪」的音，例如降三、降七音。爵士和藍調的憂傷感很多來自這幾個音。", "Charles Mingus〈Goodbye Pork Pie Hat〉", "bluescale"),
("ii-v-i", "二五一", "ii–V–I", "爵士最常見的和弦進行：從二級和弦、到五級和弦、再回到一級和弦。像一句話的「起、承、合」，聽到第三個和弦，耳朵會覺得回到家了。", "〈Autumn Leaves〉", "iivi"),
("walking-bass", "走路低音", "Walking bass", "貝斯一拍彈一個音，一步一步走向下一個和弦。它同時負責穩住拍子和告訴大家和弦在哪裡，是搖擺樂的地基。", "Paul Chambers 在《Kind of Blue》裡的貝斯", "walking"),
("comping", "伴奏", "Comping", "鋼琴或吉他在別人獨奏時，不規則地插入短促的和弦，像聊天時說「嗯」「對」的回應。不是每拍都彈，而是挑空隙回話。", "Red Garland 在 Miles Davis 五重奏裡的鋼琴", "comping"),
("head", "主題", "Head", "曲子一開始和最後一次出現的旋律。爵士演出通常是：主題 → 每個人輪流即興 → 回到主題結束。", "〈So What〉開頭的貝斯與號角對答", None),
("chorus", "一輪", "Chorus", "把曲子的和弦從頭走到尾一次，叫一輪。獨奏的人常常會說「我吹三輪」，意思是在整首和弦上即興三次。", "藍調一輪是 12 小節", None),
("trading", "交換四小節", "Trading fours", "獨奏結束前，樂手和鼓手輪流各即興四個小節，你一句、我一句，像在對話或比賽。", "Art Blakey 的現場錄音", "trading"),
("scat", "擬聲吟唱", "Scat", "歌手不用歌詞，用「嘟比嘟哇」這類無意義的音節即興，把嗓子當成一支樂器。", "Ella Fitzgerald〈How High the Moon〉", None),
("standard", "標準曲", "Standard", "大家都會彈、都認得的曲子，多半來自百老匯、電影和老流行歌。爵士樂手上台不用排練，喊一首標準曲就能一起玩。", "〈All the Things You Are〉", None),
("lead-sheet", "主旋律譜", "Lead sheet", "只寫旋律和和弦記號的簡單樂譜。剩下的伴奏、低音和節奏，由樂手自己決定。《Real Book》就是一整本主旋律譜。", "《Real Book》任何一頁", None),
("chord-symbol", "和弦記號", "Chord symbol", "寫在旋律上方的字母和數字，例如 Dm7、G7、Cmaj7，告訴樂手這一段要用什麼和弦。", "Cmaj7 = C、E、G、B 四個音", None),
("bebop", "咆勃", "Bebop", "1940 年代在紐約發展出來的爵士：速度快、和聲複雜、旋律跳躍，是給人聽、不是給人跳舞的爵士。", "Charlie Parker〈Ko-Ko〉", None),
("hard-bop", "硬咆勃", "Hard bop", "1950 年代從 bebop 延伸出來的風格，加入更多藍調和福音的味道，節奏更重、更有力。Blue Note 唱片的主力。", "Art Blakey〈Moanin'〉", None),
("cool", "酷派", "Cool jazz", "1950 年前後出現的爵士，聲音比 bebop 柔和、放鬆，編曲講究。很多在美國西岸發展。", "Miles Davis《Birth of the Cool》", None),
("modal", "調式爵士", "Modal jazz", "不靠快速換和弦，而是在一個調式（一組音階）上停留很久，讓樂手有更多空間慢慢發展旋律。", "Miles Davis〈So What〉", None),
("free-jazz", "自由爵士", "Free jazz", "1950 年代末出現，放掉固定的和弦、節拍甚至曲式，讓樂手更自由地即興。剛聽會覺得很吵，但它要的是一種能量。", "Ornette Coleman《The Shape of Jazz to Come》", None),
("fusion", "融合爵士", "Fusion", "1960 年代末起，把爵士和搖滾、放克、電子樂器混在一起的風格。電吉他、電鋼琴和合成器上場。", "Miles Davis《Bitches Brew》", None),
("bossa-nova", "巴薩諾瓦", "Bossa nova", "1950 年代末在巴西里約出現，把森巴的節奏放慢、放輕，加上爵士的和聲。輕聲細語地唱，像在耳邊講話。", "〈The Girl from Ipanema〉", None),
("trio", "三重奏", "Piano trio", "鋼琴、貝斯、鼓三個人的編制。爵士最常見、也最適合入門的組合之一。", "Bill Evans Trio", None),
("interplay", "互動", "Interplay", "樂手一邊彈一邊聽彼此，隨時回應對方的句子。不是輪流講話，而是同時在對話。", "《Sunday at the Village Vanguard》", None),
("brushes", "鼓刷", "Brushes", "用一束細鋼絲做成的鼓棒，在小鼓上畫圈、刷動，發出沙沙聲。慢歌和三重奏很常用。", "Paul Motian 在 Bill Evans Trio 裡的鼓", None),
("vamp", "反覆段", "Vamp", "一小段不斷重複的和弦或節奏，可以一直轉下去，讓獨奏的人在上面發揮。", "《The Köln Concert》Part I 的左手", "vamp"),
("solo", "獨奏", "Solo", "樂團裡輪到某一個人站出來即興的段落。其他人退到後面伴奏。", "任何一張爵士唱片", None),
("thematic", "主題式即興", "Thematic improvisation", "拿曲子裡的一小段旋律，反覆變化、拆開、重組來即興，而不是只在和弦上跑音階。", "Sonny Rollins〈Blue 7〉", "motif"),
("coltrane-changes", "Coltrane 和弦進行", "Coltrane changes", "Coltrane 在〈Giant Steps〉裡用的和弦走法：在三個相隔大三度的調之間快速跳動。", "〈Giant Steps〉、〈Countdown〉", "giant"),
("sheets-of-sound", "聲音的毯子", "Sheets of sound", "樂評 Ira Gitler 在 1958 年形容 Coltrane 的詞：一大片又快又密的音，一層一層鋪上來。", "Coltrane〈Giant Steps〉的獨奏", None),
("tenor-sax", "次中音薩克斯風", "Tenor saxophone", "爵士最具代表性的樂器之一，聲音比中音薩克斯風低、比較厚。Coleman Hawkins、Sonny Rollins、John Coltrane 都吹它。", "Coleman Hawkins〈Body and Soul〉", None),
("tempo", "速度", "Tempo", "曲子的快慢，用每分鐘幾拍（BPM）表示。慢歌大約 60，〈Giant Steps〉大約 290。", "比較〈My Foolish Heart〉和〈Giant Steps〉", None),
("live-album", "現場專輯", "Live album", "在俱樂部或音樂廳演出時錄下來的唱片。爵士特別重視現場，因為即興每一晚都不一樣。", "《Sunday at the Village Vanguard》", None),
("jam-session", "即興聚會", "Jam session", "樂手們聚在一起，不排練、不預先安排，喊一首曲子就上台一起即興。很多新風格就是在 jam session 裡長出來的。", "1940 年代的 Minton's Playhouse", None),
("session", "錄音場次", "Recording session", "一次進錄音室的錄音時段。1950 年代很多爵士唱片，一天之內就錄完了。", "《Kind of Blue》只用了兩個場次", None),
("blue-note", "Blue Note 唱片", "Blue Note Records", "1939 年在紐約成立的爵士唱片公司，以講究的錄音、會付錢讓樂手排練，和大膽的封面設計聞名。", "Lee Morgan《The Sidewinder》", None),
("rvg", "RVG 刻字", "RVG", "錄音師 Rudy Van Gelder 刻在黑膠唱片上的縮寫，看到它就知道是他錄的或他做的母帶。", "1950、60 年代的 Blue Note 原版黑膠", None),
]

# 時間軸：年份, 標題, 說明, 連到哪篇故事 slug
TIMELINE = [
("1890s", "紐奧良的街頭", "藍調、拉格泰姆、銅管樂隊和教會音樂在紐奧良交會。短號手 Buddy Bolden 被很多人稱為第一位爵士樂手，但他沒有留下任何錄音。", None),
("1917", "第一張爵士唱片", "Original Dixieland Jass Band 錄下〈Livery Stable Blues〉，被視為第一張爵士唱片。錄音的是一群白人樂手。", None),
("1925", "Louis Armstrong 的 Hot Five", "Armstrong 開始錄 Hot Five 和 Hot Seven 系列，把獨奏推到爵士的中心。", None),
("1927", "Duke Ellington 進駐 Cotton Club", "Ellington 樂團在哈林區的 Cotton Club 駐場，靠電台轉播紅遍全美。", None),
("1935", "搖擺時代開始", "Benny Goodman 樂團在洛杉磯 Palomar 舞廳的演出引起轟動，大樂團搖擺樂成為美國的流行音樂。同一年，Village Vanguard 開張。", "village-vanguard-1961"),
("1938", "爵士進了卡內基音樂廳", "Benny Goodman 在卡內基音樂廳舉行爵士音樂會，古典音樂的殿堂第一次迎來一整晚的搖擺樂。", None),
("1939", "Blue Note 成立", "Alfred Lion 和 Francis Wolff 在紐約創辦 Blue Note 唱片。同年 Coleman Hawkins 錄下〈Body and Soul〉。", "van-gelder-living-room"),
("1940s", "bebop 誕生", "Charlie Parker、Dizzy Gillespie、Thelonious Monk 在哈林區的俱樂部裡，把爵士變得更快、更複雜。", None),
("1949", "酷派爵士", "Miles Davis 九重奏開始錄後來集結成《Birth of the Cool》的作品，帶出更柔和的聲音。", None),
("1953", "客廳裡的錄音室", "Blue Note 開始把錄音交給在 Hackensack 客廳錄音的 Rudy Van Gelder。", "van-gelder-living-room"),
("1954", "第一屆新港爵士音樂節", "美國羅德島新港舉辦第一屆爵士音樂節，後來成為世界最重要的爵士音樂節之一。", None),
("1956", "Saxophone Colossus", "Sonny Rollins 錄下《Saxophone Colossus》；同年 Duke Ellington 在新港音樂節的演出讓樂團重新翻紅。", "sonny-rollins-bridge"),
("1959", "爵士最豐收的一年", "《Kind of Blue》《Giant Steps》《Time Out》《Mingus Ah Um》《The Shape of Jazz to Come》都在這一年錄音或發行。Sonny Rollins 退下舞台，走上大橋。", "giant-steps"),
("1961", "Village Vanguard 的星期天", "Bill Evans 三重奏的五輪現場錄音。十一天後，貝斯手 Scott LaFaro 過世。", "village-vanguard-1961"),
("1962", "巴薩諾瓦來了", "Stan Getz 和 Charlie Byrd 的《Jazz Samba》把巴西的巴薩諾瓦帶進美國；1964 年的《Getz/Gilberto》讓〈The Girl from Ipanema〉紅遍全世界。", None),
("1965", "A Love Supreme", "John Coltrane 的《A Love Supreme》發行，一張唱片就是一段禱告。", None),
("1970", "Bitches Brew", "Miles Davis 的《Bitches Brew》把電吉他、電鋼琴和搖滾節奏帶進爵士，融合爵士時代開始。", None),
("1970s", "Real Book 出現", "一本手抄、沒有授權的曲譜在樂手之間影印流傳，成了全世界爵士樂手的共同語言。", "real-book"),
("1975", "科隆的那一晚", "Keith Jarrett 在一台壞掉的鋼琴上即興，《The Köln Concert》後來賣了數百萬張。", "koln-concert"),
("1987", "國家珍寶", "美國國會通過決議，稱爵士為「珍貴的美國國家寶藏」。", None),
("2004", "Real Book 合法了", "Hal Leonard 出版取得授權的《Real Book》，作曲家終於拿得到版稅。", "real-book"),
]

# 入門路線：唱片, 樂手, 年份, 為什麼, 先聽哪首, 聽什麼, 相關故事
START = [
("Kind of Blue", "Miles Davis", "1959", "史上最暢銷的爵士唱片之一，速度慢、空間多，第一次聽也不會迷路。", "So What", "開頭貝斯和號角一問一答，之後每個人輪流獨奏。數數看有幾個人。", "giant-steps"),
("Waltz for Debby", "Bill Evans Trio", "1961", "安靜、溫暖的鋼琴三重奏，適合晚上戴耳機聽。", "My Foolish Heart", "注意和弦之間的空白，還有鼓刷的沙沙聲。", "village-vanguard-1961"),
("Getz/Gilberto", "Stan Getz & João Gilberto", "1964", "爵士和巴西音樂相遇，輕得像微風。不喜歡吵鬧的人從這張開始。", "The Girl from Ipanema", "聽薩克斯風怎麼在歌聲之後輕輕接上，像是在回答。", None),
("Time Out", "Dave Brubeck Quartet", "1959", "整張唱片都在玩奇怪的拍子，但旋律好記到不像實驗。", "Take Five", "跟著數「一二三、四五」，這首是五拍一小節。", None),
("Ella and Louis", "Ella Fitzgerald & Louis Armstrong", "1956", "兩個最受歡迎的爵士歌手對唱，一個甜、一個沙啞。", "Cheek to Cheek", "聽兩個人輪流唱，以及 Armstrong 唱完後吹的那段小號。", None),
("Saxophone Colossus", "Sonny Rollins", "1956", "旋律感最強的薩克斯風手，最開朗的一張。", "St. Thomas", "加勒比海的節奏，鼓手開場的那段獨奏很好認。", "sonny-rollins-bridge"),
("Moanin'", "Art Blakey & The Jazz Messengers", "1958", "hard bop 的代表，有教會、有藍調，鼓聲很推。", "Moanin'", "鋼琴問一句，號角答一句，這叫呼喚與回應。", "van-gelder-living-room"),
("Mingus Ah Um", "Charles Mingus", "1959", "情緒最多的一張，有吵鬧、有溫柔、有幽默。", "Better Git It in Your Soul", "聽樂手在背景裡喊叫拍手，像教會的禮拜。", None),
("Giant Steps", "John Coltrane", "1960", "等你習慣了爵士，再來挑戰最快的這張。", "Giant Steps", "先聽主題旋律，再聽鋼琴獨奏那一段。", "giant-steps"),
("A Love Supreme", "John Coltrane", "1965", "整張唱片是一段禱告，適合找一個不被打擾的晚上聽完。", "Acknowledgement", "開頭的鑼聲，以及後半段反覆唱出的「A Love Supreme」。", None),
]
BRANCH = [
("喜歡安靜的", "Bill Evans、Chet Baker《Chet Baker Sings》、Keith Jarrett《The Köln Concert》"),
("喜歡熱鬧的", "Art Blakey、Duke Ellington《Ellington at Newport》、Count Basie"),
("喜歡人聲的", "Ella Fitzgerald、Billie Holiday、Sarah Vaughan、Nina Simone"),
("喜歡電子和放克的", "Herbie Hancock《Head Hunters》、Miles Davis《Bitches Brew》、Weather Report"),
]

# 周邊選品：分類, 說明, [(名稱, 一句話, 搜尋關鍵字)]
SHOP = [
("第一批黑膠", "想開始收黑膠，可以從這幾個大廠重新發行的系列找起。都是用原始母帶重新製作，價格和品質比較穩定。", [
 ("Blue Note Tone Poet 系列", "Blue Note 官方的高品質復刻，厚紙封套，聲音細緻。", "Blue Note Tone Poet"),
 ("Blue Note Classic Vinyl 系列", "價格比較親民的官方復刻，入門收藏剛好。", "Blue Note Classic Vinyl Series"),
 ("Craft Recordings OJC 系列", "Prestige、Riverside 等老廠牌的官方復刻，《Waltz for Debby》也在裡面。", "Craft Recordings Original Jazz Classics"),
 ("《Kind of Blue》黑膠", "如果只買一張，就是這張。", "Kind of Blue vinyl"),
]),
("讀物", "想知道得更多，這幾本書可以讀。", [
 ("村上春樹《爵士群像》", "小說家寫他最愛的爵士樂手，一人一篇，配上和田誠的插畫。", "村上春樹 爵士群像"),
 ("Ashley Kahn《Kind of Blue: The Making of the Miles Davis Masterpiece》", "一整本書講一張唱片怎麼錄出來。", "Ashley Kahn Kind of Blue"),
 ("Ted Gioia《How to Listen to Jazz》", "爵士史學家寫給初學者的聽法指南。", "Ted Gioia How to Listen to Jazz"),
 ("Ted Gioia《The Jazz Standards》", "兩百多首標準曲的故事和推薦版本，可以當辭典翻。", "Ted Gioia The Jazz Standards"),
 ("Barry Kernfeld《The Story of Fake Books》", "Real Book 那篇故事的延伸讀物。", "The Story of Fake Books Kernfeld"),
]),
("聽的器材", "不需要很貴。重點是能讓你聽得到貝斯和鼓刷。", [
 ("一副封閉式耳罩耳機", "低音比耳塞清楚，通勤也能用。爵士的貝斯是一半的樂趣。", "封閉式耳罩耳機 推薦"),
 ("一台入門唱盤", "選有內建唱頭放大器的款式，接喇叭就能聽，不用另外買擴大機。", "入門黑膠唱盤 內建唱放"),
 ("唱片刷與內套", "黑膠最怕灰塵，一支碳纖維刷、一包防靜電內套就夠了。", "黑膠 碳纖維刷 防靜電內套"),
]),
]

# 時間軸展開內容：年份 → (年代分組, 展開說明, (先聽曲, 說明), [相關樂手 slug])
ERAS = [('origin', '起源'), ('swing', '搖擺時代'), ('bebop', 'Bebop 與酷派'), ('golden', '黃金年代'), ('after', '融合之後')]
TL_MORE = {
"1890s": ("origin", "十九世紀末的紐奧良是一座港口城市，非洲、加勒比海、法國和西班牙的文化混在一起。黑人在剛果廣場的鼓聲與舞蹈、教會的福音、街頭的銅管樂隊、鋼琴上的拉格泰姆，慢慢揉成一種新的音樂。Buddy Bolden 的樂團以音量大、帶著藍調味道出名，但他 1907 年就因精神疾病住進療養院，一個音都沒有被錄下來。這張照片，幾乎是他留下的唯一影像。", ("Buddy Bolden's Blues", "Jelly Roll Morton 1939 年的錄音，憑記憶唱出 Bolden 當年的歌"), ["louis-armstrong"]),
"1917": ("origin", "1917 年 2 月，一支從紐奧良來的白人樂團在紐約的 Victor 錄音室錄下兩首曲子，唱片一推出就大賣，「jazz」這個字從此在全美流行起來。樂團名字原本拼成 Jass，後來才改成 Jazz。諷刺的是，第一張爵士唱片不是由創造這種音樂的黑人樂手錄的；很多黑人樂手要再等幾年，才有機會走進錄音室。", ("Livery Stable Blues", "第一張爵士唱片，可以聽到樂器模仿馬叫和雞叫"), []),
"1925": ("origin", "1925 年到 1928 年，Louis Armstrong 在芝加哥用自己的樂團錄了一系列唱片。在這之前，爵士多半是大家一起即興合奏；Armstrong 站出來，一個人吹一大段，吹得又亮又有自信，從此「獨奏」成了爵士的中心。他在〈Heebie Jeebies〉裡用沒有意義的音節即興唱，讓 scat 唱法流行起來。", ("West End Blues", "1928 年。開頭那段小號獨奏，常被說是爵士史上最有名的十幾秒"), ["louis-armstrong"]),
"1927": ("origin", "Cotton Club 在哈林區，但只讓白人客人進場，台上表演的卻全是黑人樂手和舞者。Duke Ellington 的樂團在這裡駐場了好幾年，為舞台秀寫了大量帶著異國情調的曲子。俱樂部的演出透過電台轉播到全美，讓 Ellington 成了家喻戶曉的名字，也讓他有穩定的收入養一整個樂團，慢慢寫出更有野心的作品。", ("Mood Indigo", "1930 年。三把管樂器的特殊配置，聽起來像一種新的顏色"), ["duke-ellington"]),
"1935": ("swing", "1935 年 8 月，Benny Goodman 的樂團在美國巡迴，一路反應冷淡，到了洛杉磯的 Palomar 舞廳，台下的年輕人卻瘋了。透過電台，西岸的聽眾早就聽過他的搖擺樂。從這一晚起，大樂團搖擺樂成了美國最流行的音樂。Goodman 也是最早在台上讓黑人和白人樂手同台的樂團領袖之一，例如鋼琴手 Teddy Wilson 和顫音琴手 Lionel Hampton。", ("Sing, Sing, Sing", "1937 年。鼓手 Gene Krupa 的鼓聲幾乎從頭打到尾"), []),
"1938": ("swing", "1938 年 1 月 16 日，Benny Goodman 帶著樂團走進紐約的卡內基音樂廳。這裡原本是古典音樂的殿堂，爵士樂手能站上這個舞台，在當時是一件大事。那天的演出被錄了下來，但錄音盤一度被遺忘，直到 1950 年才發行成唱片，成了最暢銷的現場爵士專輯之一。", ("Sing, Sing, Sing（1938 卡內基現場）", "十幾分鐘的版本，台下的興奮聽得出來"), []),
"1939": ("swing", "這一年有兩件事。1 月，Alfred Lion 在紐約錄下 Blue Note 的第一場錄音，兩位布基伍基鋼琴手。10 月，次中音薩克斯風手 Coleman Hawkins 錄了〈Body and Soul〉，整首幾乎不吹原本的旋律，直接在和弦上即興，結果意外成了暢銷曲。很多人說，這首曲子證明了大眾也聽得懂純粹的即興。", ("Body and Soul", "Coleman Hawkins，1939。注意他多快就離開了原本的旋律"), ["sonny-rollins", "john-coltrane"]),
"1940s": ("bebop", "1940 年代初，哈林區的 Minton's Playhouse 每到深夜就有即興聚會。駐店鋼琴手是 Thelonious Monk，鼓手是 Kenny Clarke，Charlie Parker 和 Dizzy Gillespie 常常來。他們故意把曲子彈得更快、和弦換得更複雜，讓只會跟著舞曲節奏走的人跟不上。這種新音樂後來被叫作 bebop。不巧的是，1942 到 1944 年美國樂手工會罷錄，bebop 誕生的那幾年幾乎沒有留下錄音。", ("Ko-Ko", "Charlie Parker，1945。速度快到令人喘不過氣"), ["charlie-parker", "thelonious-monk"]),
"1949": ("bebop", "bebop 又快又熱，有一群樂手想走另一條路。1949 到 1950 年，Miles Davis 帶著一個九人樂團錄音，編制裡有法國號和低音號，聲音柔和、層次細，編曲由 Gil Evans、Gerry Mulligan、John Lewis 等人負責。這些錄音後來在 1957 年集結成《Birth of the Cool》，被當成酷派爵士的起點。", ("Boplicity", "《Birth of the Cool》。聽法國號和低音號怎麼讓整個樂團變柔"), ["miles-davis"]),
"1953": ("bebop", "Blue Note 唱片開始把錄音交給 Rudy Van Gelder。他白天當驗光師，晚上在紐澤西父母家的客廳錄音。接下來十幾年，大量的 hard bop 經典都在這間客廳和他後來蓋的錄音室裡錄成，他的名字縮寫 RVG 也刻在無數張黑膠上。", ("Moanin'", "Art Blakey，1958 年 Hackensack 錄音"), ["art-blakey", "thelonious-monk"]),
"1954": ("bebop", "1954 年 7 月，在羅德島新港的富人避暑地，第一屆新港爵士音樂節開幕，由鋼琴手兼製作人 George Wein 籌辦。爵士第一次有了自己的大型戶外音樂節。1956 年，Duke Ellington 樂團在這裡演出〈Diminuendo and Crescendo in Blue〉，薩克斯風手 Paul Gonsalves 一口氣吹了二十七輪獨奏，全場起立，讓已經過氣的 Ellington 重新翻紅。", ("Diminuendo and Crescendo in Blue（1956 新港現場）", "中段那段長長的薩克斯風獨奏，聽台下怎麼越來越瘋"), ["duke-ellington"]),
"1956": ("golden", "1956 年 6 月，Sonny Rollins 在 Van Gelder 的客廳錄下《Saxophone Colossus》，五首曲子，一天錄完。這張唱片讓他被叫作「薩克斯風巨人」。1950 年代中期是 hard bop 的高峰，Blue Note 和 Prestige 幾乎每個月都在發經典。", ("St. Thomas", "《Saxophone Colossus》第一首，加勒比海節奏"), ["sonny-rollins"]),
"1959": ("golden", "1959 年常被說是爵士史上最豐收的一年。Miles Davis 的《Kind of Blue》、John Coltrane 的《Giant Steps》、Dave Brubeck 的《Time Out》、Charles Mingus 的《Mingus Ah Um》、Ornette Coleman 的《The Shape of Jazz to Come》，都在這一年錄音或發行。五張唱片，五個完全不同的方向：調式、快速換和弦、奇數拍子、情緒與福音、自由爵士。", ("Take Five", "Dave Brubeck Quartet，《Time Out》。五拍一小節，卻好聽到成了暢銷單曲"), ["miles-davis", "john-coltrane", "charles-mingus"]),
"1961": ("golden", "Bill Evans 三重奏在 Village Vanguard 從下午彈到晚上，錄下兩張經典現場專輯。十一天後，貝斯手 Scott LaFaro 車禍過世，那個星期天成了這個組合最後的聲音。", ("Gloria's Step", "《Sunday at the Village Vanguard》第一首，聽貝斯怎麼站到前面來"), ["bill-evans"]),
"1962": ("golden", "1962 年 2 月，薩克斯風手 Stan Getz 和吉他手 Charlie Byrd 在華盛頓錄下《Jazz Samba》，把巴西的巴薩諾瓦帶進美國，單曲〈Desafinado〉大賣。1963 年，Getz 和巴西歌手 João Gilberto、作曲家 Antônio Carlos Jobim 合作《Getz/Gilberto》，Gilberto 的太太 Astrud 臨時唱了英文版〈The Girl from Ipanema〉，紅遍全世界。這張唱片後來拿下葛萊美年度專輯。", ("The Girl from Ipanema", "《Getz/Gilberto》。先是葡萄牙文，再換 Astrud 輕輕唱英文"), []),
"1965": ("golden", "1964 年 12 月 9 日，John Coltrane 的經典四重奏（McCoy Tyner 鋼琴、Jimmy Garrison 貝斯、Elvin Jones 鼓）在 Van Gelder 的錄音室，只用一個晚上錄完四段組曲。Coltrane 在內頁寫了一首獻給神的詩。《A Love Supreme》隔年初發行，成了他最暢銷、也最多人覺得神聖的一張唱片。", ("Acknowledgement", "第一段。後半段四個人反覆唱出「A Love Supreme」"), ["john-coltrane"]),
"1970": ("after", "1969 年 8 月，Miles Davis 找來一大群樂手，連續三天在錄音室裡即興：兩個鼓手、兩把貝斯、好幾台電鋼琴，還有吉他手 John McLaughlin。製作人 Teo Macero 再把一大堆錄音帶剪接拼貼成曲子。1970 年發行的《Bitches Brew》聽起來像搖滾、像放克，也像一場夢，很多傳統爵士迷聽不下去，卻賣得比 Miles 之前的唱片都好。", ("Miles Runs the Voodoo Down", "《Bitches Brew》。電吉他、電鋼琴和兩組鼓一起推"), ["miles-davis", "wayne-shorter", "herbie-hancock"]),
"1970s": ("after", "波士頓一帶的音樂學生手抄了一本曲譜，收錄當時樂手真正在彈的幾百首曲子，沒有出版社、沒有作者，一路影印流傳到全世界。它就是《Real Book》。網站上有完整的故事。", ("Autumn Leaves", "幾乎每個爵士學生學的第一首曲子"), []),
"1975": ("after", "1975 年 1 月 24 日深夜，Keith Jarrett 在科隆歌劇院，用一台音不準、高音刺耳的小鋼琴，完全即興彈了一整場。這場差點取消的演出，後來成了史上最暢銷的獨奏鋼琴專輯之一。網站上有完整的故事。", ("The Köln Concert, Part I", "先聽開頭那幾個像鈴聲的音"), ["keith-jarrett"]),
"1987": ("after", "1987 年，美國國會通過一份決議，稱爵士是「一種珍貴而罕見的美國國家寶藏」，鼓勵政府和民間保存、研究、教育爵士樂。這是爵士從街頭、俱樂部、地下室一路走到國家殿堂的一個象徵。", ("Take the 'A' Train", "Duke Ellington 樂團的招牌曲"), ["duke-ellington"]),
"2004": ("after", "音樂出版社 Hal Leonard 花了很多功夫，一首一首跟作曲家談授權，推出合法版的《Real Book》，保留原本的手寫風格和頁碼，讓作曲家終於拿得到版稅。地下流傳了三十年的書，在這一年走到了檯面上。", ("All the Things You Are", "《Real Book》裡最受樂手喜愛的標準曲之一"), []),
}

ERAS.append(('now', '今天'))
# 展廳導覽：id → (展廳名稱, 年代, 導覽文字)
HALLS = {
 'origin': ('第一廳　港口的聲音', '1890s–1920s', '爵士從哪裡來？從紐奧良的街頭、教會和舞廳開始。非洲的節奏、歐洲的和聲、藍調的憂傷，在一座港口城市裡相遇，再坐著火車和唱片，一路往北走到芝加哥和紐約。'),
 'swing': ('第二廳　全美國都在跳舞', '1930s', '經濟大蕭條的年代，大家需要一點快樂。十幾個人的大樂團、能跳舞的搖擺節奏、電台轉播，讓爵士變成全美國的流行音樂。'),
 'bebop': ('第三廳　深夜的實驗室', '1940s–1950s 初', '戰爭結束前後，一群年輕樂手在深夜的俱樂部裡，把爵士彈得更快、更複雜，不再是為了讓人跳舞，而是為了讓人坐下來聽。另一群人則往反方向走，讓爵士變得更柔、更酷。'),
 'golden': ('第四廳　黃金年代', '1950s–1960s', '錄音技術成熟、黑膠唱片普及，爵士迎來最多經典誕生的十幾年。hard bop、調式爵士、巴薩諾瓦、自由爵士，好幾條路同時往前走。'),
 'after': ('第五廳　插上電之後', '1970s–1990s', '搖滾和放克佔領了排行榜，爵士樂手拿起電吉他和合成器。同時，爵士走進學校和音樂廳，被寫成教科書，也被稱為國家寶藏。'),
 'now': ('第六廳　今天的爵士', '2000s–', '爵士沒有變成博物館裡的東西。新一代的樂手把嘻哈、靈魂樂、電子音樂帶進來，在串流平台上找到新的聽眾。'),
}
TIMELINE += [
("2008", "爵士拿下年度專輯", "Herbie Hancock 向 Joni Mitchell 致敬的《River: The Joni Letters》拿下葛萊美年度專輯，是《Getz/Gilberto》之後四十多年來第一張得獎的爵士專輯。", None),
("2011", "貝斯手打敗了小賈斯汀", "爵士貝斯手兼歌手 Esperanza Spalding 拿下葛萊美最佳新人，是這個獎項第一次頒給爵士樂手。", None),
("2015", "三小時的史詩", "薩克斯風手 Kamasi Washington 發行長達近三小時的三張唱片《The Epic》，在年輕聽眾之間爆紅，讓很多人第一次走進爵士。", None),
]
TL_MORE.update({
"2008": ("now", "Herbie Hancock 從 1960 年代就在 Miles Davis 的樂團裡，一路玩過電子、放克、嘻哈。這張向創作歌手 Joni Mitchell 致敬的專輯，找來 Norah Jones、Tina Turner 等歌手合作，安靜又細膩，在 2008 年的葛萊美打敗了一群流行巨星。", ("River", "專輯同名曲，Corinne Bailey Rae 演唱"), ["herbie-hancock", "wayne-shorter"]),
"2011": ("now", "Esperanza Spalding 一邊彈低音大提琴一邊唱歌，曲風混合爵士、巴西音樂和靈魂樂。2011 年她拿下葛萊美最佳新人，同一個獎項的入圍者還有當紅的 Justin Bieber，消息一出，很多人第一次聽到她的名字。", ("Little Fly", "《Chamber Music Society》，2010"), []),
"2015": ("now", "Kamasi Washington 來自洛杉磯，跟饒舌歌手 Kendrick Lamar 合作過。《The Epic》有合唱團、弦樂團和兩組鼓，聲音巨大又帶著靈性，讓人想起 Coltrane。它證明了在串流時代，一張將近三小時的爵士唱片也能找到年輕的聽眾。", ("Change of the Guard", "《The Epic》第一首"), ["john-coltrane"]),
})

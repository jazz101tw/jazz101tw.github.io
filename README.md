# 爵士101 網站（jazz101tw.github.io）

> 📘 中文說明書（2026-11-28 整理）｜狀態：🟢 使用中
> 全部 29 個 repo 的總表與封存建議：[repo 地圖](https://github.com/jay0916746661/jimframe-site/blob/main/docs/repo地圖與封存建議.md)

## 這是什麼
爵士101 的獨立網站：長篇爵士故事、樂手、小辭典、時間軸、入門路線、聆聽頁。網站網址 https://jazz101tw.github.io（網域 jazz101.tw）。11/26 已縮編，節奏／和聲／換伴奏遊戲從導覽拿掉（檔案還在）。

## 怎麼用／怎麼改
**不要手改根目錄的 HTML**，它們是程式產生的。改內容：編 `src/stories.py`（長篇故事）或 `src/extras.py`（樂手、辭典、時間軸、入門、選品），再跑 `JAZZ_OUT=. python3 src/build.py`，commit 推上 main，1–2 分鐘後網站更新。照片來源與授權在 `src/img/meta.json`。

## 要注意
`.github/workflows/photofetch.yml`（手動）：替 Reels 抓 Wikimedia 照片，不需要 Claude。網站沒更新：Actions 頁看 pages 部署是否紅燈。Wikimedia 回 429 是限流，隔一陣子再跑。

### 怎麼修（不用 Claude 也做得到）
1. 小改字：在 GitHub 網頁打開檔案 → 右上角鉛筆 ✏️ → 改完按 Commit changes。
2. 大改：用 Antigravity（Gemini）開這個 repo，第一句貼：「先讀 README.md，照裡面的說明改，改完給我分支名＋PR 連結，不要直接改 main。」
3. 改壞了：GitHub 網頁 → Commits → 找到改壞前那一版 → 點 `<>` 看舊檔，複製回來。**不要刪 repo、不要 force push。**

## 封存建議（只是建議，沒有動任何東西）
不建議。

---

## 原本的 README（保留原文）

# 爵士101｜慢慢聽

一分鐘講不完的爵士故事。網站：https://jay0916746661.github.io/jazz101/

- 網站檔案在根目錄（index.html、story/、img/…），由 `src/build.py` 產生。
- 改內容：編 `src/stories.py`（長篇故事）或 `src/extras.py`（樂手、小辭典、時間軸、入門路線、選品），然後
  `JAZZ_OUT=. python3 src/build.py`
- 照片來自 Wikimedia Commons，作者與授權見 `src/img/meta.json`，網頁上也逐張標示。

# AInote Log — Streamlit Cloud

## 部署
1. 將此資料夾推送至 GitHub 儲存庫。
2. 在 Streamlit Community Cloud 選擇 `app.py` 作為入口。
3. Python 依賴見 `requirements.txt`。

## 功能
左上角 AInote Log，右上角文件操作，左側 Explorer；支援 Markdown 預覽、MathJax 公式、貼上後重渲染、文件開啟/儲存/另存/匯出、資料夾樹、右鍵操作、拖曳排序、節點優先序。

## 重要限制
- 這是新建獨立版本，未整合既有 AInote 專案程式碼。
- 資料夾直接讀寫依賴 Chromium 瀏覽器的 File System Access API 和使用者授權。部分 Android 瀏覽器不支援，會改用資料夾匯入與 JSON 備份。
- 工作區狀態保存在瀏覽器 localStorage，並非雲端永久儲存；請定期下載備份。
- Explorer 的「保存」在獲得資料夾授權時寫入檔案；未授權時下載 JSON 備份。資料夾同步目前不會刪除磁碟上已移除的檔案，也不會自動清除重新命名前的舊檔。
- Markdown 與 MathJax 引擎由 CDN 載入，需要網路連線；CDN 不可用時以純文字安全預覽。
- 本版提供拖放排序；觸控長按拖動在不同 Android 瀏覽器上可能受限。
- Streamlit iframe 在部分瀏覽器下可能限制資料夾授權功能。


## v1.1 單一編輯即預覽
中央改成 contenteditable 單一所見即所得區域。輸入直接顯示格式，貼上富文字即顯示；離開編輯區或按工具重新渲染時重新處理 LaTeX。Markdown 匯出使用 Turndown。注意：複雜 LaTeX 的編輯/匯出保真尚有限制，建議備份原檔。

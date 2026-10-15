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


## v1.2 Explorer UI 修正
- Explorer 操作按鈕可換行且不截斷標籤，側欄可拖曳調整寬度。
- FOLD 右鍵選單新增「關閉 FOLD」：根 FOLD 解除目前工作區載入；子 FOLD 收合。兩者均不刪除實體文件。
- 右鍵選單位置依視窗大小調整，避免選單超出畫面。
- 本版專注 Explorer UI；LaTeX、SVG、表格的渲染問題尚未修復或驗收。


## v1.3 選取區域公式渲染

- 左鍵選取公式原始文字，右鍵選「渲染數學式」；不再對整份文件執行 MathJax typeset。
- 工具列也可對目前選取範圍執行同一操作。
- 編輯器右鍵操作採可擴充 editorActions 陣列。
- 初次使用（尚無瀏覽器工作區）建立「歡迎.md」教學文件；已存在的工作區不會覆蓋。
- 貼上或失焦不會自動重建文件。
- 限制：跨多個複雜 HTML 區塊的選取不適用，請只選取公式文字；Mermaid 的圖形渲染仍取決於現有前端功能。

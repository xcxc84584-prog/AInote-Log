# AS-CODE-P v1.1｜ASCII 可視化代碼架構協議

**英文名稱：ASCII Code Architecture Protocol**

**協議縮寫：AS-CODE-P**

**版本：1.1**

**文件類型：架構規範文件（Architecture Specification）**

---

# Chapter 1｜協議總則

## 1.1 協議目的

AS-CODE-P 是一套使用純文字 ASCII 字元描述軟體系統架構、功能模組、邏輯節點及資料流向的架構描述協議。

本協議的主要目的：

1. 使用純文字表示軟體架構。
2. 讓人類與 AI Agent 都能理解系統架構。
3. 建立統一的模組命名與封裝規則。
4. 明確描述模組之間的資料流動。
5. 降低模組之間的耦合程度。
6. 支援大型軟體專案的模組化設計。
7. 支援軟體架構文件的自動產生與驗證。
8. 支援後續程式碼分析與架構一致性檢查。
9. 支援跨程式語言的架構描述。
10. 保持架構文件的可讀性、可移植性及可維護性。

AS-CODE-P 是架構描述協議，不是可直接執行的程式語言。

## 1.2 設計原則

AS-CODE-P 採用以下核心原則：

| 原則 | 英文 | 說明 |
|---|---|---|
| 模組化 | Modularity | 將系統拆分為獨立功能模組 |
| 封裝性 | Encapsulation | 隱藏內部實作細節 |
| 單一職責 | Single Responsibility | 每個元件負責明確功能 |
| 低耦合 | Low Coupling | 減少元件之間的依賴 |
| 高內聚 | High Cohesion | 將相關功能集中管理 |
| 介面導向 | Interface-Oriented Design | 透過公開介面交換資料 |
| 資料完整性 | Data Integrity | 確保資料傳輸正確 |
| 可追蹤性 | Traceability | 能追蹤資料來源及目的地 |
| 可驗證性 | Verifiability | 架構可由規則進行檢查 |
| 可讀性 | Readability | 使用純文字理解架構 |

## 1.3 架構層級

AS-CODE-P 採用以下階層：

```text
PROJECT
   |
   v
ENCAPSULATION
   |
   v
AREA
   |
   v
NODE
```

BUS 負責連接不同元件，不屬於額外的封裝層級。

各層級關係：

```text
PROJECT
   |
   +--- ENCAPSULATION.(A)
   |           |
   |           +--- AREA.(A1)
   |           |        |
   |           |        +--- NODE.(A)
   |           |        +--- NODE.(B)
   |           |
   |           +--- AREA.(A2)
   |
   +--- ENCAPSULATION.(B)
               |
               +--- AREA.(B1)
                        |
                        +--- NODE.(C)
```

---

# Chapter 2｜核心元件

AS-CODE-P 定義六種核心元件：

1. NODE
2. BUS
3. AREA
4. ENCAPSULATION
5. EXTERNAL
6. FOLD

---

# Chapter 3｜NODE 規則

## 3.1 NODE 定義

NODE 是 AS-CODE-P 中最小的邏輯處理單元。

NODE 必須遵守：

- 單一輸入。
- 單一輸出。
- 固定的功能職責。
- 黑箱封裝。
- 明確的輸入與輸出資料格式。

NODE 的內部程式碼邏輯不得被其他元件直接修改或干擾。

外部元件只能透過 NODE 的公開輸入與輸出介面進行互動。

## 3.2 NODE 命名規則

標準格式：

```text
NODE.(Name)
```

範例：

```text
NODE.(Input)
NODE.(Validate)
NODE.(Process)
NODE.(Output)
NODE.(MathConvert)
NODE.(ErrorHandler)
```

NODE 名稱必須符合：

1. 名稱不可為空。
2. 同一 AREA 內不可重複。
3. 名稱應描述功能。
4. 建議使用英文 PascalCase。
5. 不得使用 BUS 控制字元作為名稱的一部分。

## 3.3 NODE 單一輸入規則

每個 NODE 只能有一個邏輯輸入介面。

允許輸入結構化資料：

```json
{
  "content": "x^2",
  "format": "latex",
  "options": {
    "displayMode": true
  }
}
```

即使輸入包含多個欄位，仍視為一個邏輯輸入。

禁止將多個獨立介面直接接入同一 NODE。

錯誤範例：

```text
NODE.(A) ----+
             +---- NODE.(Process)
NODE.(B) ----+
```

如果兩個來源沒有經過明確的資料聚合處理，則此架構不符合單一輸入規則。

正確設計：

```text
NODE.(A) ----+
             +---- NODE.(Merge) ---- NODE.(Process)
NODE.(B) ----+
```

此處 BUS 必須先將兩路資料聚合為單一結構化輸入，再交給 NODE.(Merge)。

NODE.(Merge) 本身仍只有一個輸入介面。

## 3.4 NODE 單一輸出規則

每個 NODE 只能有一個邏輯輸出介面。

允許輸出包含：

- 處理結果。
- 執行狀態。
- 錯誤訊息。
- 附加資料。

標準輸出範例：

```json
{
  "status": "success",
  "data": {},
  "error": null
}
```

錯誤輸出範例：

```json
{
  "status": "error",
  "data": null,
  "error": {
    "code": "N001",
    "message": "Invalid input"
  }
}
```

## 3.5 NODE 黑箱規則

NODE 內部實作不得由外部元件直接存取。

禁止：

1. 外部元件直接修改 NODE 的內部變數。
2. 外部元件直接呼叫 NODE 的私人函數。
3. 外部元件繞過 NODE 的輸入介面。
4. 外部元件依賴 NODE 未公開的內部狀態。

允許：

1. 透過公開輸入傳遞資料。
2. 透過公開輸出取得結果。
3. 在維持介面契約的情況下替換內部實作。

## 3.6 NODE 單一職責規則

一個 NODE 原則上只負責一項明確的邏輯工作。

範例：

```text
NODE.(Input)
    |
    v
NODE.(Validate)
    |
    v
NODE.(Convert)
    |
    v
NODE.(Output)
```

不建議將輸入驗證、資料轉換、資料儲存及 UI 渲染全部放入同一 NODE。

## 3.7 NODE 錯誤處理

NODE 發生錯誤時，應透過唯一的輸出介面回傳錯誤狀態。

不得產生未宣告的額外輸出通道。

錯誤輸出必須包含：

1. 錯誤識別碼。
2. 錯誤原因。
3. 錯誤來源。
4. 可選的附加資訊。

---

# Chapter 4｜BUS 規則

## 4.1 BUS 定義

BUS 是負責在元件之間傳輸資料的有向通道。

BUS 可用於：

1. 傳輸資料。
2. 傳輸執行結果。
3. 傳輸錯誤狀態。
4. 分配資料。
5. 聚合資料。
6. 建立元件之間的資料依賴關係。

BUS 本身不應包含業務處理邏輯。

## 4.2 BUS 基本符號

正式 BUS 使用以下符號：

| 符號 | 名稱 | 功能 |
|---|---|---|
| `-` | Horizontal | 水平連線 |
| `|` | Vertical | 垂直連線 |
| `>` | Right Direction | 向右傳輸 |
| `<` | Left Direction | 向左傳輸 |
| `+` | Junction | 轉折或交會點 |

可讀性擴充符號：

| 符號 | 功能 |
|---|---|
| `v` | 向下傳輸 |
| `^` | 向上傳輸 |

其中 `v` 與 `^` 屬於可讀性擴充符號。

正式解析器若支援這兩種符號，必須明確宣告所採用的語法版本。

## 4.3 BUS 傳輸方向

主要資料流預設由左至右。

標準範例：

```text
NODE.(Input) ---> NODE.(Process) ---> NODE.(Output)
```

反向傳輸必須明確標示：

```text
NODE.(A) <--- NODE.(B)
```

不得僅根據元件的排列位置推測反向傳輸。

## 4.4 BUS 連續性

BUS 必須在行列位置上實際對齊，才能視為連續。

例如：

```text
NODE.(A) ---> NODE.(B)
```

為連續 BUS。

若垂直通道未處於同一字元欄位，不得視為連接。

所有架構圖必須使用等寬字型。

禁止使用 Tab 進行對齊。

必須使用空格。

## 4.5 BUS 分支規則

一條 BUS 可以將同一份資料分配至多個元件。

```text
                 +---> NODE.(A)
                 |
NODE.(Input) ----+
                 |
                 +---> NODE.(B)
```

分支資料預設採用相同的邏輯資料內容。

若分支需要不同資料，必須由 NODE 或 AREA 明確處理資料轉換。

## 4.6 BUS 聚合規則

BUS 可以聚合多個來源。

```text
NODE.(A) ----+
             +----> NODE.(Merge)
NODE.(B) ----+
```

聚合時必須定義：

1. 資料來源。
2. 資料欄位。
3. 聚合方式。
4. 資料衝突處理。
5. 資料缺失處理。

BUS 聚合不得隱含未宣告的業務邏輯。

## 4.7 BUS 交叉規則

兩條 BUS 在圖面上交叉，不代表一定相連。

只有明確標示交會點 `+`，且方向及端點符合連線規則時，才視為相連。

若交叉處沒有交會點，視為兩條獨立通道。

## 4.8 BUS 數量限制

每一行最多允許三段彼此不連續的 BUS。

此限制用於維持 ASCII 架構圖的可讀性。

若超過三段，應：

1. 增加行數。
2. 拆分圖面。
3. 使用子 AREA。
4. 使用獨立的架構文件。

## 4.9 BUS 資料安全

BUS 應維護資料的：

- Integrity：完整性。
- Availability：可用性。

涉及機密資料時，還必須考慮：

- Confidentiality：機密性。

相關安全機制包括：

1. 資料驗證。
2. 存取控制。
3. 傳輸完整性檢查。
4. 錯誤偵測。
5. 超時控制。
6. 重試機制。
7. 必要時的加密保護。

BUS 的圖形描述不代表上述機制已經實作。

## 4.10 BUS 資料契約

重要 BUS 應定義：

```text
BUS_ID:
SOURCE:
DESTINATION:
DATA_TYPE:
DIRECTION:
VALIDATION:
ERROR_POLICY:
```

範例：

```text
BUS_ID: BUS_MathResult
SOURCE: AREA.(MathParser)
DESTINATION: AREA.(TXTSummarize)
DATA_TYPE: JSON
DIRECTION: LEFT_TO_RIGHT
VALIDATION: REQUIRED
ERROR_POLICY: PROPAGATE
```

---

# Chapter 5｜AREA 規則

## 5.1 AREA 定義

AREA 是實現一項完整功能的模組。

AREA 可以包含：

1. NODE。
2. BUS。
3. 輸入介面。
4. 輸出介面。
5. 錯誤處理機制。

AREA 必須具有明確的功能邊界。

## 5.2 AREA 命名

標準格式：

```text
AREA.(Name)
```

範例：

```text
AREA.(MathParser)
AREA.(SVGParser)
AREA.(MarkdownParser)
AREA.(GraphParser)
AREA.(DocumentStorage)
```

## 5.3 AREA 獨立文件

每個 AREA 必須使用獨立 TXT 文件。

命名格式：

```text
AREA_Name.txt
```

範例：

```text
AREA_MathParser.txt
AREA_SVGParser.txt
AREA_MarkdownParser.txt
AREA_GraphParser.txt
```

一個 AREA 文件只能描述一個主要 AREA。

## 5.4 AREA 文件格式

```text
/*
AREA:MathParser

NODE.(Input) ---> NODE.(Validate) ---> NODE.(Process) ---> NODE.(Output)
*/

// Input：接收資料。
// Validate：驗證資料格式。
// Process：執行數學公式解析。
// Output：輸出解析結果。
```

## 5.5 AREA 封裝規則

AREA 的內部 NODE 不得被其他 AREA 直接存取。

錯誤：

```text
AREA.(A).NODE.(Process)
```

其他 AREA 不得直接呼叫此內部 NODE。

正確：

```text
AREA.(A) ---> AREA.(B)
```

AREA 之間必須透過公開介面及 BUS 通信。

## 5.6 AREA 功能完整性

每個 AREA 必須能明確回答：

1. 接收什麼資料？
2. 執行什麼功能？
3. 輸出什麼結果？
4. 發生錯誤時如何處理？
5. 依賴哪些其他模組？

## 5.7 AREA 單一職責

AREA 應負責一個完整且明確的功能。

例如：

```text
AREA.(MathParser)
```

負責數學公式解析。

不應同時負責使用者帳號管理、資料庫備份及 UI 主題切換。

## 5.8 AREA 相互依賴

AREA 可以依賴其他 AREA 的公開輸出。

依賴關係必須記錄於：

```text
AREA_Summarize.txt
```

禁止未經宣告的循環依賴。

---

# Chapter 6｜ENCAPSULATION 規則

## 6.1 ENCAPSULATION 定義

ENCAPSULATION 是由一個或多個 AREA 組成的獨立封裝系統。

ENCAPSULATION 具有：

1. 公開 INPUT BUS。
2. 公開 OUTPUT BUS。
3. 內部 AREA。
4. 內部 BUS。
5. 明確的功能邊界。

## 6.2 ENCAPSULATION 黑箱規則

ENCAPSULATION 對外只允許公開：

```text
INPUT BUS
OUTPUT BUS
```

其他 ENCAPSULATION 不得直接存取其內部 AREA 或 NODE。

## 6.3 ENCAPSULATION 命名

標準格式：

```text
ENCAPSULATION.(Name)
```

範例：

```text
ENCAPSULATION.(TextEditor)
ENCAPSULATION.(DocumentStorage)
ENCAPSULATION.(UserAuthentication)
ENCAPSULATION.(CloudSynchronization)
```

## 6.4 ENCAPSULATION 獨立 FOLD

每個 ENCAPSULATION 必須建立獨立資料夾。

格式：

```text
ENCAPSULATION_Name/
```

範例：

```text
ENCAPSULATION_TextEditor/
ENCAPSULATION_DocumentStorage/
ENCAPSULATION_UserAuthentication/
```

## 6.5 ENCAPSULATION 文件

每個 ENCAPSULATION 至少包含：

```text
ENCAPSULATION.txt
AREA_Summarize.txt
INTERFACE.txt
```

以及該封裝所有 AREA 的獨立文件。

## 6.6 ENCAPSULATION 介面規則

公開介面必須定義：

```text
INPUT:
OUTPUT:
DATA_TYPE:
ERROR_POLICY:
VERSION:
```

範例：

```text
INPUT:
  document: string

OUTPUT:
  rendered_document: object

DATA_TYPE:
  JSON

ERROR_POLICY:
  PROPAGATE

VERSION:
  1.0
```

## 6.7 ENCAPSULATION 隔離

禁止：

1. 直接修改其他封裝的內部狀態。
2. 直接呼叫其他封裝的私人 NODE。
3. 直接存取其他封裝的內部 AREA。
4. 繞過公開 BUS 進行資料傳輸。

允許：

1. 呼叫公開 INPUT BUS。
2. 接收公開 OUTPUT BUS。
3. 使用公開定義的資料契約。
4. 透過公開介面建立依賴。

## 6.8 ENCAPSULATION 版本相容性

內部實作可以修改，但應維持公開介面的相容性。

如果修改：

- INPUT 格式。
- OUTPUT 格式。
- 錯誤格式。
- 介面語義。

則必須進行相容性評估。

不相容的介面修改應提升主要版本號。

---

# Chapter 7｜EXTERNAL 規則

## 7.1 EXTERNAL 定義

EXTERNAL 表示架構封裝外部的資料來源或接收端。

可能包括：

1. 使用者。
2. 瀏覽器。
3. 外部 API。
4. 資料庫服務。
5. 作業系統。
6. 其他 ENCAPSULATION。

## 7.2 EXTERNAL 命名

標準格式：

```text
EXTERNAL.(Name)
```

範例：

```text
EXTERNAL.(USER_INPUT)
EXTERNAL.(OUTPUT)
EXTERNAL.(DATABASE)
EXTERNAL.(API)
```

## 7.3 EXTERNAL 存取規則

EXTERNAL 不得直接存取 ENCAPSULATION 的內部 NODE。

必須透過公開 BUS 進行資料交換。

---

# Chapter 8｜FOLD 文件結構

## 8.1 FOLD 定義

FOLD 是 AS-CODE-P 的文件組織容器。

FOLD 對應實際檔案系統中的資料夾。

## 8.2 專案根目錄

所有 AS-CODE-P 文件必須放在：

```text
ASCII Code Architecture Protocol/
```

## 8.3 標準目錄

```text
ASCII Code Architecture Protocol/
|
+-- README.md
|
+-- AS-CODE-P_Rules.md
|
+-- ENCAPSULATION_Summarize.txt
|
+-- ENCAPSULATION_TextEditor/
|   |
|   +-- ENCAPSULATION.txt
|   |
|   +-- AREA_Summarize.txt
|   |
|   +-- INTERFACE.txt
|   |
|   +-- AREA_InputDispatcher.txt
|   |
|   +-- AREA_MathParser.txt
|   |
|   +-- AREA_MarkdownParser.txt
|   |
|   +-- AREA_SVGParser.txt
|   |
|   +-- AREA_GraphParser.txt
|   |
|   +-- AREA_TXTSummarize.txt
|
+-- ENCAPSULATION_DocumentStorage/
    |
    +-- ENCAPSULATION.txt
    |
    +-- AREA_Summarize.txt
    |
    +-- INTERFACE.txt
    |
    +-- AREA_SaveDocument.txt
    |
    +-- AREA_LoadDocument.txt
```

## 8.4 文件職責

| 文件 | 職責 |
|---|---|
| README.md | 專案說明 |
| AS-CODE-P_Rules.md | 協議規則 |
| ENCAPSULATION_Summarize.txt | 封裝系統總覽 |
| ENCAPSULATION.txt | 單一封裝架構 |
| AREA_Summarize.txt | AREA 關係總覽 |
| AREA_Name.txt | 單一 AREA 內部架構 |
| INTERFACE.txt | 公開介面契約 |

## 8.5 文件隔離

不同 ENCAPSULATION 的 AREA 文件不得混合放置。

每個 AREA 文件必須位於其所屬 ENCAPSULATION 的 FOLD 中。

---

# Chapter 9｜Summarize 規則

## 9.1 ENCAPSULATION_Summarize

專案根目錄必須包含：

```text
ENCAPSULATION_Summarize.txt
```

用於描述所有 ENCAPSULATION 之間的關係。

範例：

```text
/*
ENCAPSULATION:Summarize

ENCAPSULATION.(TextEditor)
              |
              v
ENCAPSULATION.(DocumentStorage)
              |
              v
ENCAPSULATION.(CloudSynchronization)
*/
```

此文件只負責描述架構，不代表實際執行模組。

## 9.2 AREA_Summarize

每個 ENCAPSULATION 必須包含：

```text
AREA_Summarize.txt
```

此文件用於描述該封裝內部 AREA 的依賴及資料流。

範例：

```text
/*
AREA:Summarize

AREA.(InputDispatcher)
         |
         +---> AREA.(MathParser) -----+
         |                            |
         +---> AREA.(MarkdownParser) -+
         |                            |
         +---> AREA.(SVGParser) ------+---> AREA.(TXTSummarize)
         |                            |
         +---> AREA.(GraphParser) ----+
*/
```

## 9.3 Summarize 一致性

Summarize 中的元件名稱必須與實際文件一致。

不得引用不存在的 AREA 或 ENCAPSULATION。

不得省略已存在且參與資料流的必要元件。

Summarize 必須隨架構變更同步更新。

---

# Chapter 10｜ASCII 架構圖規範

## 10.1 架構宣告

所有主要架構圖使用：

```text
/*
TYPE:Name

ARCHITECTURE
*/
```

TYPE 可以是：

```text
AREA
ENCAPSULATION
```

Summarize 文件使用對應的 Summarize 名稱。

## 10.2 元件表示

```text
NODE.(Name)
AREA.(Name)
ENCAPSULATION.(Name)
EXTERNAL.(Name)
```

## 10.3 註解規則

註解使用：

```text
// 說明
```

範例：

```text
/*
AREA:MathParser

NODE.(Input) ---> NODE.(Process) ---> NODE.(Output)
*/

// Input：接收輸入資料。
// Process：解析數學公式。
// Output：回傳解析結果。
```

## 10.4 排版規則

1. 使用等寬字型。
2. 使用空格對齊。
3. 不使用 Tab。
4. 保持 BUS 的行列連續性。
5. 不得以視覺接近代替實際連線。
6. 每行最多三段不連續 BUS。
7. 優先採用左至右的資料流。
8. 複雜架構應拆分為多個 AREA。
9. 圖形應保持在純文字環境中可閱讀。
10. 不得依賴顏色表達必要語義。

## 10.5 正式語法與閱讀語法

AS-CODE-P 區分：

### Strict Mode

正式解析模式。

使用：

```text
-
|
<
>
+
```

並透過明確的連線方向及座標規則解析架構。

### Readable Mode

人類閱讀模式。

額外允許：

```text
v
^
```

用於表示垂直方向。

Readable Mode 的圖形若需要由程式自動解析，必須先通過相容性檢查。

兩種模式不得在未宣告的情況下混用。

## 10.6 方向與歧義處理

Strict Mode 中：

1. `>` 表示向右。
2. `<` 表示向左。
3. `-` 只表示水平通道，不單獨決定方向。
4. `|` 只表示垂直通道，不單獨決定方向。
5. `+` 表示連接或轉折，不單獨決定方向。

若僅依圖形無法判斷垂直方向，必須在介面契約中補充方向資訊。

不得由解析器任意猜測。

---

# Chapter 11｜資料介面規則

## 11.1 Interface Contract

所有公開介面必須具有資料契約。

資料契約至少定義：

```text
INTERFACE_NAME:
SOURCE:
DESTINATION:
INPUT_TYPE:
OUTPUT_TYPE:
ERROR_POLICY:
VERSION:
```

## 11.2 資料格式

允許使用：

- JSON
- String
- Number
- Boolean
- Binary
- Array
- Object
- 自訂結構化資料

自訂資料格式必須有明確說明。

## 11.3 資料驗證

接收資料的元件應檢查：

1. 資料類型。
2. 必要欄位。
3. 資料範圍。
4. 格式正確性。
5. 存取權限。

## 11.4 資料所有權

跨 AREA 或 ENCAPSULATION 傳遞資料時，應明確定義：

1. 資料是否可修改。
2. 資料是否可複製。
3. 資料是否為參照。
4. 資料的生命週期。
5. 資料的責任歸屬。

不得假設所有 BUS 都傳遞可自由修改的資料。

---

# Chapter 12｜錯誤處理規則

## 12.1 錯誤傳播

錯誤必須沿公開 OUTPUT BUS 傳遞。

不得使用未宣告的隱藏輸出通道。

## 12.2 錯誤資料格式

建議格式：

```json
{
  "status": "error",
  "error": {
    "id": "A001",
    "reason": "Invalid input",
    "source": "AREA.MathParser",
    "details": {}
  }
}
```

## 12.3 錯誤來源

錯誤必須能定位至：

1. ENCAPSULATION。
2. AREA。
3. NODE。

## 12.4 錯誤處理策略

可使用：

```text
PROPAGATE
RETRY
FALLBACK
ABORT
IGNORE
```

說明：

| 策略 | 功能 |
|---|---|
| PROPAGATE | 向上傳遞錯誤 |
| RETRY | 重新執行 |
| FALLBACK | 使用替代處理 |
| ABORT | 中止流程 |
| IGNORE | 忽略非關鍵錯誤 |

IGNORE 不得用於必須處理的安全性或資料完整性錯誤。

---

# Chapter 13｜依賴管理規則

## 13.1 依賴宣告

所有跨 AREA 或 ENCAPSULATION 的依賴必須可由架構文件識別。

## 13.2 禁止隱藏依賴

不得依賴未宣告的：

- 全域變數。
- 私有函數。
- 內部資料結構。
- 隱藏資料通道。

## 13.3 循環依賴

原則上應避免循環依賴。

如確實需要雙向通信，必須明確定義：

1. 通信方向。
2. 觸發條件。
3. 結束條件。
4. 超時處理。
5. 避免無限循環的機制。

## 13.4 依賴隔離

不同 ENCAPSULATION 之間不得直接引用內部 NODE 或 AREA。

所有依賴都必須透過公開介面建立。

---

# Chapter 14｜版本管理

## 14.1 協議版本

採用：

```text
MAJOR.MINOR.PATCH
```

例如：

```text
1.1.0
```

## 14.2 版本變更

MAJOR：

不相容的規則或介面變更。

MINOR：

向下相容的新規則或功能。

PATCH：

錯誤修正及文字說明調整。

## 14.3 文件版本

建議在 README.md 中記錄：

```text
PROJECT_VERSION:
AS_CODE_P_VERSION:
LAST_UPDATED:
```

## 14.4 介面相容性

若公開介面發生不相容變更，必須更新相應版本。

若只是內部 NODE 實作改變，而公開介面不變，原則上不需要提升介面的主要版本。

---

# Chapter 15｜架構驗證

## 15.1 必要驗證

AS-CODE-P 文件應檢查：

1. 所有 ENCAPSULATION 是否具有獨立 FOLD。
2. 所有 AREA 是否具有獨立 TXT。
3. 是否存在 AREA_Summarize。
4. 是否存在 ENCAPSULATION_Summarize。
5. NODE 是否只有一個輸入介面。
6. NODE 是否只有一個輸出介面。
7. BUS 是否正確連接。
8. BUS 是否符合方向規則。
9. BUS 是否符合行列對齊規則。
10. 是否存在未宣告的跨封裝存取。
11. 是否存在未宣告的循環依賴。
12. 是否存在重複元件名稱。
13. Summarize 是否與實際架構一致。
14. 公開介面是否具有資料契約。
15. 錯誤處理策略是否明確。

## 15.2 驗證結果

驗證結果分為：

```text
PASS
WARNING
ERROR
```

PASS：

符合協議。

WARNING：

存在可能影響可維護性或可讀性的問題，但未必違反強制規則。

ERROR：

違反協議強制規則。

## 15.3 驗證錯誤格式

```text
ERROR_ID:
RULE_ID:
FILE:
LOCATION:
REASON:
SUGGESTION:
```

範例：

```text
ERROR_ID: ACP-E001
RULE_ID: N01
FILE: AREA_MathParser.txt
LOCATION: NODE.Process
REASON: Multiple independent input interfaces
SUGGESTION: Aggregate inputs before NODE.Process
```

---

# Chapter 16｜完整規則編號

## 16.1 NODE Rules

| ID | 規則 |
|---|---|
| N01 | NODE 必須具有單一輸入介面 |
| N02 | NODE 必須具有單一輸出介面 |
| N03 | NODE 必須具有明確功能 |
| N04 | NODE 必須遵守黑箱封裝 |
| N05 | NODE 名稱在同一 AREA 中必須唯一 |
| N06 | NODE 輸入輸出必須具有明確格式 |
| N07 | NODE 錯誤必須透過公開輸出回傳 |
| N08 | NODE 不得被外部直接修改內部狀態 |

## 16.2 BUS Rules

| ID | 規則 |
|---|---|
| B01 | BUS 必須具有明確來源 |
| B02 | BUS 必須具有明確目的地 |
| B03 | BUS 預設左至右傳輸 |
| B04 | BUS 必須遵守行列對齊 |
| B05 | BUS 連續性不得依賴視覺推測 |
| B06 | BUS 可分支 |
| B07 | BUS 可聚合結構化資料 |
| B08 | BUS 不得隱含業務處理邏輯 |
| B09 | BUS 應維護資料完整性 |
| B10 | BUS 應考慮資料可用性 |
| B11 | BUS 每行最多三段不連續通道 |
| B12 | BUS 交叉不自動代表連接 |
| B13 | BUS 方向不明時必須補充宣告 |

## 16.3 AREA Rules

| ID | 規則 |
|---|---|
| A01 | AREA 必須實現完整功能 |
| A02 | AREA 必須具有獨立 TXT 文件 |
| A03 | AREA 必須具有明確輸入輸出 |
| A04 | AREA 必須遵守封裝 |
| A05 | AREA 內部 NODE 不得被外部直接存取 |
| A06 | AREA 應遵守單一職責 |
| A07 | AREA 依賴必須記錄 |
| A08 | AREA 錯誤處理必須明確 |
| A09 | AREA 文件必須具有架構宣告 |

## 16.4 ENCAPSULATION Rules

| ID | 規則 |
|---|---|
| E01 | ENCAPSULATION 必須具有獨立 FOLD |
| E02 | ENCAPSULATION 只能公開 INPUT BUS 與 OUTPUT BUS |
| E03 | ENCAPSULATION 內部 AREA 不得被外部直接存取 |
| E04 | ENCAPSULATION 必須具有 ENCAPSULATION.txt |
| E05 | ENCAPSULATION 必須具有 AREA_Summarize.txt |
| E06 | ENCAPSULATION 必須具有 INTERFACE.txt |
| E07 | ENCAPSULATION 之間必須透過公開介面通信 |
| E08 | ENCAPSULATION 必須維持介面契約 |
| E09 | ENCAPSULATION 應避免循環依賴 |
| E10 | ENCAPSULATION 內部實作應可獨立維護 |

## 16.5 FILE Rules

| ID | 規則 |
|---|---|
| F01 | 所有文件放在統一專案根目錄 |
| F02 | 每個 ENCAPSULATION 使用獨立 FOLD |
| F03 | 每個 AREA 使用獨立 TXT |
| F04 | 根目錄必須具有 ENCAPSULATION_Summarize |
| F05 | 每個 ENCAPSULATION 必須具有 AREA_Summarize |
| F06 | 文件名稱必須與元件名稱一致 |
| F07 | 不同封裝文件不得混合 |
| F08 | 架構變更必須同步更新 Summarize |

## 16.6 SYNTAX Rules

| ID | 規則 |
|---|---|
| S01 | 架構使用 `/* ... */` 宣告 |
| S02 | NODE 使用 `NODE.(Name)` |
| S03 | AREA 使用 `AREA.(Name)` |
| S04 | ENCAPSULATION 使用 `ENCAPSULATION.(Name)` |
| S05 | EXTERNAL 使用 `EXTERNAL.(Name)` |
| S06 | 註解使用 `//` |
| S07 | 必須使用等寬字元 |
| S08 | 不得使用 Tab 對齊 |
| S09 | BUS 必須行列對齊 |
| S10 | 不得存在未宣告的隱含連線 |
| S11 | 正式語法與閱讀語法必須區分 |
| S12 | 元件名稱必須符合命名規範 |

## 16.7 INTERFACE Rules

| ID | 規則 |
|---|---|
| I01 | 公開介面必須具有資料契約 |
| I02 | 資料格式必須明確 |
| I03 | 必須定義錯誤處理方式 |
| I04 | 重要資料流應可追蹤 |
| I05 | 不相容介面變更必須更新版本 |
| I06 | 不得繞過公開介面 |
| I07 | 應定義資料所有權 |
| I08 | 應定義必要的資料驗證 |

---

# Chapter 17｜完整應用範例

## 17.1 ENCAPSULATION_TextEditor

文件：

```text
ENCAPSULATION_TextEditor/ENCAPSULATION.txt
```

內容：

```text
/*
ENCAPSULATION:TextEditor

EXTERNAL.(USER_INPUT)
         |
         v
AREA.(InputDispatcher)
         |
         +---> AREA.(MathParser) -----+
         |                            |
         +---> AREA.(MarkdownParser) -+
         |                            |
         +---> AREA.(SVGParser) ------+---> AREA.(TXTSummarize)
         |                            |
         +---> AREA.(GraphParser) ----+
                                            |
                                            v
                                    EXTERNAL.(OUTPUT)
*/

// InputDispatcher：接收並分配使用者輸入。
// MathParser：解析 LaTeX 公式。
// MarkdownParser：解析 Markdown。
// SVGParser：解析 SVG。
// GraphParser：解析圖表。
// TXTSummarize：整合解析結果。
```

此圖採用 Readable Mode。

## 17.2 AREA_MathParser

文件：

```text
ENCAPSULATION_TextEditor/AREA_MathParser.txt
```

內容：

```text
/*
AREA:MathParser

NODE.(Input) ---> NODE.(Validate) ---> NODE.(Process) ---> NODE.(Output)
*/

// Input：接收數學公式。
// Validate：檢查 LaTeX 格式。
// Process：轉換為 KaTeX 或 MathML。
// Output：輸出處理結果與錯誤狀態。
```

## 17.3 AREA_Summarize

文件：

```text
ENCAPSULATION_TextEditor/AREA_Summarize.txt
```

內容：

```text
/*
AREA:Summarize

AREA.(InputDispatcher)
         |
         +---> AREA.(MathParser) -----+
         |                            |
         +---> AREA.(MarkdownParser) -+
         |                            |
         +---> AREA.(SVGParser) ------+---> AREA.(TXTSummarize)
         |                            |
         +---> AREA.(GraphParser) ----+
*/

// 描述 TextEditor 內部 AREA 的資料流。
// 本文件不代表可執行的 AREA。
```

## 17.4 INTERFACE

文件：

```text
ENCAPSULATION_TextEditor/INTERFACE.txt
```

內容：

```text
INTERFACE_NAME: TextEditor

VERSION: 1.0

INPUT:
  content: string
  format: string

OUTPUT:
  status: string
  rendered_content: object
  error: object|null

DATA_TYPE:
  JSON

ERROR_POLICY:
  PROPAGATE
```

---

# Chapter 18｜架構設計限制

## 18.1 AS-CODE-P 不等於程式碼

AS-CODE-P 描述：

- 元件。
- 模組。
- 封裝。
- 資料流。
- 依賴。
- 公開介面。

AS-CODE-P 不直接描述完整的程式語言語義。

## 18.2 ASCII 圖不保證實際安全性

即使架構符合 AS-CODE-P，仍必須透過實際程式碼檢查確認：

1. 存取控制。
2. 輸入驗證。
3. 資料完整性。
4. 權限隔離。
5. 錯誤處理。
6. 資料保護。

## 18.3 黑箱不等於完全無依賴

黑箱代表內部實作不可由外部直接操作。

不代表模組之間完全沒有依賴。

允許透過公開介面建立受控依賴。

## 18.4 單一輸入輸出是邏輯限制

NODE 的單一輸入與輸出指的是公開邏輯介面。

單一輸入可以包含多個欄位。

單一輸出可以包含結果、狀態及錯誤資訊。

## 18.5 複雜架構應拆分

若單一 ASCII 圖過於複雜，應優先拆分 AREA 或 ENCAPSULATION。

不得為了在單一圖面表示全部架構而破壞可讀性及連線規則。

---

# Chapter 19｜協議強制性與擴充

## 19.1 強制規則

以下規則為核心強制要求：

1. NODE 單一輸入與輸出。
2. NODE 黑箱封裝。
3. AREA 獨立文件。
4. ENCAPSULATION 獨立 FOLD。
5. ENCAPSULATION 對外僅公開 INPUT / OUTPUT BUS。
6. BUS 必須有明確方向及連線。
7. BUS 必須符合行列對齊。
8. 每行最多三段不連續 BUS。
9. 每個 ENCAPSULATION 必須有 AREA_Summarize。
10. 專案必須有 ENCAPSULATION_Summarize。
11. 不得跨越封裝邊界直接存取內部元件。
12. 架構文件必須與實際宣告的元件一致。

## 19.2 建議規則

以下規則屬於建議：

1. 使用 PascalCase 命名。
2. 使用結構化 JSON 介面。
3. 為重要 BUS 建立資料契約。
4. 使用統一錯誤格式。
5. 使用語義化版本管理。
6. 避免循環依賴。
7. 將複雜 AREA 拆分。
8. 建立自動驗證器。
9. 建立架構變更紀錄。
10. 建立資料流追蹤機制。

## 19.3 擴充規則

未來版本可擴充：

- 非同步 BUS。
- 事件驅動架構。
- 狀態機描述。
- 資料庫結構描述。
- 權限模型。
- 安全信任邊界。
- 自動程式碼對應。
- AI Agent 架構驗證。
- 自動生成架構圖。
- 自動依賴分析。

擴充功能不得在未提升適當版本的情況下破壞既有核心語義。

---

# Chapter 20｜協議總結

AS-CODE-P 的核心結構為：

```text
PROJECT
   |
   v
ENCAPSULATION
   |
   v
AREA
   |
   v
NODE
```

其中：

**NODE**

最小邏輯處理單元，單一輸入、單一輸出，內部邏輯採用黑箱封裝。

**BUS**

資料傳輸通道，負責元件之間的資料分配、傳遞與聚合，必須遵守連線、方向及資料契約規則。

**AREA**

實現完整功能的模組，由 NODE 與 BUS 組成，每個 AREA 使用獨立 TXT 文件。

**ENCAPSULATION**

由多個 AREA 組成的獨立封裝系統，對外只公開 INPUT BUS 與 OUTPUT BUS，每個 ENCAPSULATION 使用獨立 FOLD。

**EXTERNAL**

系統封裝外部的資料來源或接收端，只能透過公開介面與 ENCAPSULATION 通信。

**FOLD**

文件組織容器，負責隔離各 ENCAPSULATION 及其內部 AREA 文件。

所有相關文件統一存放於：

```text
ASCII Code Architecture Protocol/
```

最終目標是建立一套：

**Human-Readable、AI-Readable、Machine-Verifiable、Modular、Encapsulated**

的純文字軟體架構描述協議。

---

**AS-CODE-P v1.1 — End of Specification**
---
title: PnP PowerShell 知识图谱与实战参考
created: 2026-06-04
updated: 2026-06-04
type: research
tags:
status: stable
version: 2.x
oversized_ok: true
  - M365
  - PowerShell
  - PnP
  - 迁移
---

# PnP PowerShell 知识图谱与实战参考

> 面向 M365 跨租户迁移(含 21Vianet→Global)的工程师手册。版本基准:PnP.PowerShell **2.x**(.NET / PowerShell 7+)。
> 关键时效:**2024/9/9 起多租户 PnP Management Shell 应用已被微软删除,所有连接必须自注册 Entra App 并显式传 `-ClientId`**〔信源 1,2〕。沿用旧脚本(不带 ClientId)会直接报 `AADSTS700016`。

---

## 第 0 章 速查:30 秒拿到能用的连接

```powershell
# 1) 装模块(PowerShell 7+,Windows/macOS/Linux 均可)
Install-Module PnP.PowerShell -Scope CurrentUser

# 2) 一次性给本租户注册一个 Entra App(交互式),记下输出的 ClientId
Register-PnPEntraIDApp -ApplicationName "PnP-Mig-Tool" -Tenant contoso.onmicrosoft.com -Interactive

# 3) 用 ClientId 连接(Global)
Connect-PnPOnline -Url https://contoso.sharepoint.com/sites/A -ClientId <client-id> -Interactive

# 3') 连 21Vianet(China)——端点不同,必须加 -AzureEnvironment China
Connect-PnPOnline -Url https://contoso.sharepoint.cn/sites/A -ClientId <client-id> -AzureEnvironment China -Interactive
```

> 记住三件事:**自己的 ClientId**、**对的 URL 后缀(.com vs .cn)**、**China 必须 `-AzureEnvironment China`**。

---

## 第 1 章 知识图谱(全景)

```
                         ┌─────────────────────────────┐
                         │      PnP PowerShell 2.x      │
                         │   (.NET, PowerShell 7+)      │
                         └──────────────┬──────────────┘
                                        │
            ┌───────────────────────────┼───────────────────────────┐
            │                           │                           │
      [认证 Auth]                 [操作对象 Scope]              [运行形态 Runtime]
            │                           │                           │
  ┌─────────┼─────────┐       ┌─────────┼─────────┐       ┌─────────┼─────────┐
  │         │         │       │         │         │       │         │         │
交互式   App-Only   Device   租户级   站点级   列表/项级   本地交互  无人值守  CI/CD
-Interactive 证书   -Device  Tenant   Site     List/Item  脚本     计划任务  Pipeline
  │      Thumbprint  Login   Admin    Web       Folder/File         证书登录  证书+Secret
  │      /Base64           Get-PnP    Get-PnP   Get-PnP
必须      App-Only        TenantSite  Web       ListItem
ClientId  无人值守                    Get-PnP   Add/Set/
                                      List      Remove
                                                Get-PnPFile

            ┌───────────────────────────┴───────────────────────────┐
            │                  [环境 Environment]                     │
            │   Global(.com / -AzureEnvironment Production 默认)      │
            │   China 21Vianet(.cn / -AzureEnvironment China)        │
            │   USGov / USGovHigh / USGovDoD / Germany                │
            └─────────────────────────────────────────────────────────┘
```

### 1.1 三条主轴

| 轴 | 选项 | 何时用 |
|---|---|---|
| **认证** | 交互式 / App-Only 证书 / Device Login | 人工跑用交互;批处理/夜跑用 App-Only 证书;无浏览器环境用 Device |
| **操作对象** | 租户 → 站点 → 列表 → 项/文件 | 一个连接锁定一个站点上下文;切站点要重连或多连接 |
| **运行形态** | 交互脚本 / 计划任务 / CI/CD | 迁移盘点用交互;批量搬运用 App-Only 无人值守 |

### 1.2 四类核心 cmdlet(按对象层级)

| 层级 | 代表 cmdlet | 用途 |
|---|---|---|
| **连接** | `Connect-PnPOnline` `Disconnect-PnPOnline` `Get-PnPConnection` | 建立/切换上下文 |
| **租户** | `Get-PnPTenantSite` `New-PnPSite` `Set-PnPTenantSite` `Get-PnPTenant` | 站点清单、建站、租户配置(需 admin URL) |
| **站点结构** | `Get-PnPSiteTemplate` `Invoke-PnPSiteTemplate` `Get-PnPWeb` `Get-PnPList` `Get-PnPField` `Get-PnPContentType` | 导出/重放站点模板、列表、字段、内容类型 |
| **内容/项** | `Get-PnPListItem` `Add-PnPListItem` `Set-PnPListItem` `Get-PnPFile` `Add-PnPFile` `Copy-PnPFile` `Move-PnPFile` | 数据读写、文件搬运 |
| **权限** | `Get-PnPGroup` `Get-PnPGroupMember` `Set-PnPListItemPermission` `Grant-PnPAzureADAppSitePermission` | 组、独立权限、App 站点授权 |
| **元数据** | `Get-PnPTerm` `Get-PnPTermSet` `Export-PnPTermGroupToXml` `Import-PnPTermGroupFromXml` | 托管元数据/术语库迁移 |

---

## 第 2 章 认证详解(2024 新规后)

### 2.1 为什么旧脚本突然失效

2024/9/9 微软删除了多租户应用 `PnP Management Shell`(AppId `31359c7f-bd7e-475c-86db-fdb8c937548e`)。此前 `Connect-PnPOnline -Interactive` 无需 ClientId,靠这个共享应用。现在直接报:

```
AADSTS700016: Application with identifier '31359c7f-...' was not found in the directory
```

→ **每个租户必须自注册一个 Entra App,连接时显式 `-ClientId`**〔信源 1〕。

### 2.2 注册自己的 App(两法)

**法 A:PnP cmdlet 自动注册(推荐,最快)**
```powershell
# 交互登录用
Register-PnPEntraIDApp -ApplicationName "PnP-Mig-Tool" `
  -Tenant contoso.onmicrosoft.com -Interactive
# 输出含 ClientId、证书(pfx/cer)、thumbprint、base64 key —— 全部记录归档

# App-Only 无人值守用(自动生成并上传证书)
Register-PnPEntraIDApp -ApplicationName "PnP-Mig-AppOnly" `
  -Tenant contoso.onmicrosoft.com -OutPath C:\certs -DeviceLogin
```
可选权限范围参数:`-GraphApplicationPermissions` `-GraphDelegatePermissions` `-SharePointApplicationPermissions` `-SharePointDelegatePermissions`。

**法 B:Entra 管理中心手动注册**(无 PowerShell 注册权限时)
1. entra.microsoft.com → 应用注册 → 新注册,记下 **Application (client) ID**
2. 身份验证 → 添加平台 → **移动和桌面应用** → 重定向 URI 填 `http://localhost`
3. API 权限 → 加 **SharePoint 委派权限**(`AllSites.FullControl` 或按需)+ Graph
4. **授予管理员同意**(需 Global Admin,灰显说明你权限不够)

### 2.3 四种连接方式

```powershell
# ① 交互式(人工跑,支持 MFA)—— 迁移盘点首选
Connect-PnPOnline -Url https://contoso.sharepoint.com/sites/A `
  -ClientId <id> -Interactive

# ② App-Only 证书(thumbprint,Windows 证书库)—— 无人值守首选
Connect-PnPOnline -Url https://contoso.sharepoint.com/sites/A `
  -ClientId <id> -Tenant contoso.onmicrosoft.com -Thumbprint <thumb>

# ③ App-Only 证书(base64/路径)—— 跨平台/CI
Connect-PnPOnline -Url https://contoso.sharepoint.com/sites/A `
  -ClientId <id> -Tenant contoso.onmicrosoft.com `
  -CertificatePath C:\certs\app.pfx -CertificatePassword (Read-Host -AsSecureString)

# ④ Device Login(无浏览器的服务器)
Connect-PnPOnline -Url https://contoso.sharepoint.com/sites/A `
  -ClientId <id> -Tenant contoso.onmicrosoft.com -DeviceLogin
```

> **迁移项目建议**:盘点阶段用①交互式(快、能 MFA);批量搬运用②/③App-Only 证书(无人值守、夜跑不掉线)。`-UseWebLogin`/`-Credentials`(纯账密)在启用 MFA/CA 的租户上基本不可用,**别用**。

---

## 第 3 章 China(21Vianet)专项 —— 迁移项目重点

### 3.1 端点差异(连错就落到空 Global 租户)

| 项 | Global | China(21Vianet) |
|---|---|---|
| SharePoint URL | `*.sharepoint.com` | `*.sharepoint.cn` |
| OneDrive URL | `*-my.sharepoint.com` | `*-my.sharepoint.cn` |
| Admin URL | `*-admin.sharepoint.com` | `*-admin.sharepoint.cn` |
| 连接参数 | 默认(Production) | **必须 `-AzureEnvironment China`** |
| 登录端点 | login.microsoftonline.com | login.partner.microsoftonline.cn |
| Graph 端点 | graph.microsoft.com | microsoftgraph.chinacloudapi.cn |

```powershell
# 连 21V 租户管理(站点清单)
Connect-PnPOnline -Url https://contoso-admin.sharepoint.cn `
  -ClientId <china-app-id> -AzureEnvironment China -Interactive

# 连 21V 单站点
Connect-PnPOnline -Url https://contoso.sharepoint.cn/sites/A `
  -ClientId <china-app-id> -AzureEnvironment China -Interactive
```

### 3.2 China 三个真实坑〔信源 2,实测社区案例〕

1. **ClientId 必须是 China 租户里注册的 App** —— Global 注册的 App 在 21V 用不了,要在 21V 端单独 `Register-PnPEntraIDApp`(连接时同样带 `-AzureEnvironment China`)。
2. **403 FORBIDDEN 高发**:21V 上用 `-UseWebLogin` 连上后跑 `Get-PnPListItem` 常报 403(GitHub issue #3118 实例)。根因是**委派权限不足/登录方式弱**——改用 `-Interactive` + 正确的 `AllSites.FullControl` 委派权限。
3. **Site.Selected 授权变化**:`-Interactive` 近期收紧,给 App 授站点权限用 `Grant-PnPAzureADAppSitePermission`,需先在 Entra 授 `Sites.Selected`。

### 3.3 跨云迁移的 PnP 角色定位

PnP **不能**直接 21V↔Global 云内搬运(无云内信任通道)。它在迁移里干三件事:
- **采集盘点**(连 21V 读结构/权限/容量,导 CSV)
- **结构重放**(把 21V 导出的站点模板/列表/字段/内容类型 `Invoke` 到 Global)
- **权限重挂**(按身份映射表在 Global 重建组和独立权限)

文件内容本体走 BitTitan 或 PnP `Get-PnPFile`→`Add-PnPFile` 两段式(经本地/中转),详见主方案 §3.6。

---

## 第 4 章 使用方法(按迁移场景分)

### 4.1 站点结构导出 → 重放(Provisioning Engine)

```powershell
# 源(21V)导出整站模板:列表/字段/内容类型/页面/导航/品牌
Connect-PnPOnline -Url https://src.sharepoint.cn/sites/A `
  -ClientId <id> -AzureEnvironment China -Interactive
Get-PnPSiteTemplate -Out A.pnp -IncludeAllPages -PersistBrandingFiles `
  -Handlers Lists,Fields,ContentTypes,Pages,Navigation,SiteSecurity

# 目标(Global)重放
Connect-PnPOnline -Url https://dst.sharepoint.com/sites/A -ClientId <id> -Interactive
Invoke-PnPSiteTemplate -Path A.pnp
```
> 模板是 XML+文件包,可手改(改 URL/去掉不兼容 WebPart)再重放。**复杂自定义(SPFx/旧工作流)不会自动迁**,需单独处理。

### 4.2 列表数据批量读写

```powershell
# 分页读(大列表必须 -PageSize,否则超时)
$items = Get-PnPListItem -List "Documents" -PageSize 2000

# 批量写(用 Add-PnPListItem 循环;>5000 项考虑 Batch)
$batch = New-PnPBatch
foreach ($row in Import-Csv data.csv) {
  Add-PnPListItem -List "Tasks" -Values @{Title=$row.Title; Status=$row.Status} -Batch $batch
}
Invoke-PnPBatch -Batch $batch   # 批量提交,远快于逐条
```

### 4.3 文件搬运(两段式跨云)

```powershell
# 从 21V 下载
Connect-PnPOnline -Url https://src.sharepoint.cn/sites/A -ClientId <id> -AzureEnvironment China -Interactive
Get-PnPFile -Url "/sites/A/Shared Documents/Report.docx" -Path C:\stage -AsFile -Force

# 上传到 Global(保留文件夹结构)
Connect-PnPOnline -Url https://dst.sharepoint.com/sites/A -ClientId <id> -Interactive
Add-PnPFile -Path C:\stage\Report.docx -Folder "Shared Documents"
```
> 大批量别用这个逐文件搬——慢。批量用 BitTitan 或 `rclone`(主方案 §3.6)。PnP 文件操作适合**小批量/补漏/特殊文件**。

### 4.4 权限盘点与重挂

```powershell
# 盘点:找出独立权限项(broken inheritance)—— 决定权限工期
$lists = Get-PnPList | ? {$_.Hidden -eq $false}
foreach ($l in $lists) {
  $items = Get-PnPListItem -List $l -PageSize 500
  $u = $items | ? { Get-PnPProperty -ClientObject $_ -Property HasUniqueRoleAssignments }
  "[$($l.Title)] 独立权限项 $($u.Count) / 总 $($items.Count)"
}

# 重挂:按映射表给目标项重设权限
Set-PnPListItemPermission -List "Documents" -Identity 12 `
  -User "user@contoso.com" -AddRole "Contribute"
```

### 4.5 托管元数据(术语库)迁移

```powershell
# 源导出
Export-PnPTermGroupToXml -Identity "公司分类" -Out terms.xml
# 目标导入
Import-PnPTermGroupFromXml -Path terms.xml
```

---

## 第 5 章 实战案例

### 案例 1:迁移前全租户盘点(21V)
**目标**:一次性导出所有站点容量/项数/owner,筛超限项。
```powershell
Connect-PnPOnline -Url https://contoso-admin.sharepoint.cn `
  -ClientId <id> -AzureEnvironment China -Interactive
Get-PnPTenantSite -IncludeOneDriveSites |
  Select Url,Template,StorageUsageCurrent,Owner |
  Export-Csv sites.csv -NoTypeInformation -Encoding UTF8
# 筛 >5TB(迁移工具上限)
Import-Csv sites.csv | ? {[int]$_.StorageUsageCurrent -gt 5242880} |
  Export-Csv over_5tb.csv -NoTypeInformation -Encoding UTF8
```
**产出**:`sites.csv` 作报价依据,`over_5tb.csv` 作清洗清单。

### 案例 2:深路径预清洗(迁移硬约束 400 字符)
```powershell
Connect-PnPOnline -Url https://src.sharepoint.cn/sites/A -ClientId <id> -AzureEnvironment China -Interactive
Get-PnPListItem -List "Documents" -PageSize 500 -Fields FileRef |
  ? { $_.FieldValues.FileRef.Length -gt 380 } |
  Select @{N='Path';E={$_.FieldValues.FileRef}}, @{N='Len';E={$_.FieldValues.FileRef.Length}} |
  Export-Csv deep_paths.csv -NoTypeInformation -Encoding UTF8
```
**用途**:迁移前必须把 >400 字符路径改短,否则该文件迁移失败。

### 案例 3:无人值守批量结构重放(夜跑)
```powershell
# 用 App-Only 证书,无需人盯
Connect-PnPOnline -Url https://dst.sharepoint.com/sites/A `
  -ClientId <id> -Tenant contoso.onmicrosoft.com -Thumbprint <thumb>
Get-ChildItem .\templates\*.pnp | ForEach-Object {
  $url = "https://dst.sharepoint.com/sites/" + $_.BaseName
  Connect-PnPOnline -Url $url -ClientId <id> -Tenant contoso.onmicrosoft.com -Thumbprint <thumb>
  Invoke-PnPSiteTemplate -Path $_.FullName
  Write-Host "Done: $($_.BaseName)"
}
```

### 案例 4:身份映射驱动的权限重建
```powershell
$map = Import-Csv identity_map.csv  # 源 UPN → 目标 UPN
Connect-PnPOnline -Url https://dst.sharepoint.com/sites/A -ClientId <id> -Interactive
foreach ($m in $map) {
  # 把源端某用户的角色,在目标端授给映射后的新 UPN
  Set-PnPListItemPermission -List "Documents" -Identity $m.ItemId `
    -User $m.TargetUPN -AddRole "Contribute"
}
```

---

## 第 6 章 避坑清单

| 坑 | 现象 | 解法 |
|---|---|---|
| 旧脚本无 ClientId | `AADSTS700016` | 自注册 App,显式 `-ClientId`〔1〕 |
| China 连错环境 | 登录失败/落到空租户 | 加 `-AzureEnvironment China` + `.cn` URL |
| China 用 Global App | 应用找不到 | 在 21V 端单独注册 App |
| 21V 跑命令 403 | `Get-PnPListItem` 403 FORBIDDEN | 用 `-Interactive`(非 UseWebLogin)+ 足够委派权限〔2〕 |
| 大列表超时 | 卡死/超时 | 必加 `-PageSize`(≤5000),用 `New-PnPBatch` 批量 |
| 逐文件搬运慢 | 大批量耗时离谱 | 内容本体走 BitTitan/rclone,PnP 只补漏 |
| 证书过期 | 无人值守突然掉线 | 证书有效期登记,到期前轮换 |
| 节流(429) | 大批量被限速 | 重试+退避,夜间/周末跑批 |
| 模板重放报错 | SPFx/旧工作流不兼容 | 手改模板 XML,剔除不兼容 Handler 单独处理 |

---

## 第 7 章 跨云迁移完整命令(21V → Global,CSV 本地 + 正文 Azure 暂存)

> 配套主迁移方案 §3.6。核心分流:**CSV/映射/日志放本地磁盘,文件正文走 Global 区域 Azure Blob 暂存**。下面是端到端可跑的命令骨架。

### 7.1 数据分流原则(命令视角)

| 数据 | 存放 | 对应命令产物 |
|---|---|---|
| 结构(站点/列表/字段/内容类型) | 本地 `.pnp` 模板包 | `Get-PnPSiteTemplate` → `Invoke-PnPSiteTemplate` |
| 术语库 | 本地 XML | `Export-PnPTermGroupToXml` |
| 清单/映射/checkpoint | 本地 CSV | `Export-Csv` / `Import-Csv` |
| 文件正文 | Global 区域 Azure Blob 暂存 | `Get-PnPFile -AsMemoryStream` → Az.Storage → `Add-PnPFile` |

### 7.2 前置:本地目录 + Azure 暂存

```powershell
# 本地工作目录(放所有 CSV/模板/日志,建议在 Git 仓内)
$Work = "D:\mig"
New-Item -ItemType Directory -Force -Path $Work,"$Work\templates","$Work\logs" | Out-Null

# Global 区域开一个临时 Blob 容器作暂存(就近目标,弹性容量)
Connect-AzAccount   # Global Azure
$ctx = (New-AzStorageContext -StorageAccountName "migstage" -UseConnectedAccount)
New-AzStorageContainer -Name "spo-stage" -Context $ctx -Permission Off
# 生命周期:7 天自动清(在存储账户 Lifecycle Management 配,或下方迁完手动清)
```

### 7.3 第一步:盘点(21V → 本地 CSV)

```powershell
Connect-PnPOnline -Url https://contoso-admin.sharepoint.cn `
  -ClientId <cn-app-id> -AzureEnvironment China -Interactive

# 站点清单 → 本地 CSV
Get-PnPTenantSite -IncludeOneDriveSites |
  Select Url,Template,StorageUsageCurrent,Owner |
  Export-Csv "$Work\sites.csv" -NoTypeInformation -Encoding UTF8

# 身份映射表模板 → 本地 CSV(人工/规则填目标 UPN)
# (用户从 Graph 导,见主方案 §8.2 ①)
```

### 7.4 第二步:结构 + 术语库(本地中转包,不落 CSV)

```powershell
# 源(21V)导出结构
Connect-PnPOnline -Url https://contoso.sharepoint.cn/sites/A `
  -ClientId <cn-app-id> -AzureEnvironment China -Interactive
Get-PnPSiteTemplate -Out "$Work\templates\A.pnp" -IncludeAllPages -PersistBrandingFiles `
  -Handlers Lists,Fields,ContentTypes,Pages,Navigation,SiteSecurity
Export-PnPTermGroupToXml -Identity "公司分类" -Out "$Work\terms.xml"

# 目标(Global)重放
Connect-PnPOnline -Url https://contoso.sharepoint.com/sites/A -ClientId <global-id> -Interactive
Invoke-PnPSiteTemplate -Path "$Work\templates\A.pnp"
Import-PnPTermGroupFromXml -Path "$Work\terms.xml"
```

### 7.5 第三步:文件正文(21V → Azure 暂存 → Global,带 checkpoint)

```powershell
$log = "$Work\logs\progress.csv"
$done = @{}
if (Test-Path $log) { Import-Csv $log | % { $done[$_.FileRef] = $_.Status } }  # 断点续传

# 大文件阈值:超过此值不走内存流,改临时磁盘文件,避免 OOM
$BigFileBytes = 250MB
$tmp = "$Work\filetmp"; New-Item -ItemType Directory -Force -Path $tmp | Out-Null

# 连源(21V)与目标(Global)——两条连接都要显式持有
$src = Connect-PnPOnline -Url https://contoso.sharepoint.cn/sites/A `
  -ClientId <cn-app-id> -AzureEnvironment China -Interactive -ReturnConnection
$dst = Connect-PnPOnline -Url https://contoso.sharepoint.com/sites/A `
  -ClientId <global-app-id> -Interactive -ReturnConnection

$items = Get-PnPListItem -List "Documents" -PageSize 2000 -Connection $src

foreach ($it in $items) {
  $ref  = $it.FieldValues.FileRef
  if ($done[$ref] -eq "OK") { continue }   # 已迁跳过
  $size = [int64]$it.FieldValues.File_x0020_Size   # 字节
  $blobName = $ref.TrimStart('/')
  $leaf   = Split-Path $ref -Leaf
  $folder = Split-Path $ref -Parent
  try {
    if ($size -ge $BigFileBytes) {
      # ── 大文件:全程走磁盘临时文件,内存占用恒定 ──
      $local = Join-Path $tmp ([guid]::NewGuid().ToString('N'))
      Get-PnPFile -Url $ref -Path $tmp -FileName (Split-Path $local -Leaf) -AsFile -Force -Connection $src
      Set-AzStorageBlobContent -Container "spo-stage" -Blob $blobName `
        -BlobType Block -Context $ctx -Force -File $local | Out-Null
      $dl = Get-AzStorageBlob -Container "spo-stage" -Blob $blobName -Context $ctx
      $dl.ICloudBlob.DownloadToFile($local, [System.IO.FileMode]::Create)
      # Add-PnPFile -Path 对大文件自动分块上传(SPO REST chunked upload)
      Add-PnPFile -Path $local -Folder $folder `
        -Values @{ Title = $it["Title"]; Modified = $it["Modified"] } -Connection $dst | Out-Null
      Remove-Item $local -Force -ErrorAction SilentlyContinue
    } else {
      # ── 小文件:内存流直传,省磁盘 IO ──
      $stream = Get-PnPFile -Url $ref -AsMemoryStream -Connection $src
      Set-AzStorageBlobContent -Container "spo-stage" -Blob $blobName `
        -BlobType Block -Context $ctx -Force -Stream $stream | Out-Null
      $dl = Get-AzStorageBlob -Container "spo-stage" -Blob $blobName -Context $ctx
      $ms = New-Object System.IO.MemoryStream
      $dl.ICloudBlob.DownloadToStream($ms); $ms.Position = 0
      Add-PnPFile -Stream $ms -FileName $leaf -Folder $folder `
        -Values @{ Title = $it["Title"]; Modified = $it["Modified"] } -Connection $dst | Out-Null
      $ms.Dispose()
    }
    "$ref,OK" | Out-File $log -Append -Encoding UTF8
  } catch {
    "$ref,FAIL:$($_.Exception.Message)" | Out-File $log -Append -Encoding UTF8
  }
}
```

> **两条连接必须分别持有**(`$src` 连 21V、`$dst` 连 Global),跨云迁移没有云内信任,不能复用同一上下文。
> **大文件**(默认 ≥250MB)全程走磁盘临时文件:`Get-PnPFile -AsFile` 落盘、`Add-PnPFile -Path` 触发 SPO 分块上传,内存占用恒定;小文件保留内存流以省磁盘 IO。阈值按中转机内存调整。

### 7.6 第四步:权限重挂(按本地 CSV 映射)

```powershell
$map = Import-Csv "$Work\identity_map.csv"   # 源 UPN → 目标 UPN
$lookup = @{}; $map | % { $lookup[$_.UserPrincipalName] = $_.TargetUPN }

# 重挂独立权限(示例:把源端授权翻译到目标新 UPN)
Set-PnPListItemPermission -List "Documents" -Identity 12 `
  -User $lookup["user@contoso.cn"] -AddRole "Contribute" -Connection $dst
```

### 7.7 收尾:清暂存 + 核对

```powershell
# 迁完删 Azure 暂存(或靠 7 天生命周期自动清)
Remove-AzStorageContainer -Name "spo-stage" -Context $ctx -Force

# 失败项复核
Import-Csv $log | ? { $_.Status -like "FAIL*" } | Format-Table
```

> 安全提醒:Azure 暂存用 SAS 临时授权或 `-UseConnectedAccount`(RBAC),别硬编码 account key;暂存容器权限设 `Off`(私有);迁完即清,留访问日志备审计。正文出境须客户已完成数据出境合规评估(见主方案 §3.6)。

---

## 附录:信源

1. Register an Entra ID Application to Use with PnP PowerShell — O365Reports(2024/9/11,确认 2024/9/9 多租户应用删除、必须自注册+ClientId、注册两法)
   `https://o365reports.com/register-an-entra-id-application-to-use-with-pnp-powershell`
2. Connect-PnPOnline 官方 cmdlet 参考(全部参数集:Interactive/证书/Device/ClientSecret、AzureEnvironment、China 端点参数)
   `https://pnp.github.io/powershell/cmdlets/Connect-PnPOnline.html`
3. PnP/powershell issue #3118 — Azure China 连接后 Get-PnPListItem 403 实例
   `https://github.com/pnp/powershell/issues/3118`
4. Changes in PnP Management Shell registration — GitHub pnp/blog #1909(2024/9/9 生效公告)
   `https://github.com/pnp/blog/issues/1909`

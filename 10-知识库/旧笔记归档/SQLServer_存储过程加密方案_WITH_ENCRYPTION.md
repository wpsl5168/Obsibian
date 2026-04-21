---
title: "SQLServer_存储过程加密方案_WITH_ENCRYPTION"
created: 2026-04-07
updated: 2026-04-20
type: concept
tags: [security]
status: draft
date: 2026-04-08
category: SQL-Server
---

# SQL Server 存储过程加密方案 (WITH ENCRYPTION)

> 系列文档：[[SQLServer_Dacpac包加密与自动化部署|Dacpac加密部署]] · [[SQLServer_高级加密方案_CLR_混淆|CLR高级混淆]]

## 场景与原理
为了防止拥有高级权限（如 `sa`）的人员轻易窥探和窃取核心业务存储过程源码，SQL Server 提供了原生的 `WITH ENCRYPTION` 选项。
- **作用**：通过对系统表中存储的源码进行内部混淆（异或算法），使 `sp_helptext` 或 SSMS 的“修改”功能失效，直接阻断明文查看。
- **特点**：不需要外部证书，零成本。属“防君子不防小人”级别，针对高级 DBA 仍有逆向解密风险，但在常规生产环境（防运维/初级开发人员拷贝代码）下行之有效。
- **⚠️ 核心警告**：**加密不可逆！** 数据库不再保留明文，执行加密前**必须**自行在本地或 Git 库中备份源码。

## 单个存储过程加密示例
在参数列表之后、`AS` 关键字之前添加 `WITH ENCRYPTION`：

```sql
-- 修改已有的存储过程
ALTER PROCEDURE dbo.sp_YourCoreBusinessLogic
    @Param1 INT,
    @Param2 VARCHAR(50)
WITH ENCRYPTION
AS
BEGIN
    -- 核心商业逻辑...
END
GO
```

## 全库批量自动化加密方案 (PowerShell + Invoke-Sqlcmd)
> 生产环境首选方案：自动化备份源码 + 正则安全替换 + 批量刷入

使用 T-SQL 游标处理字符串存在极大误伤（截断）风险。采用 PowerShell 脚本是更稳妥、专业的做法。以下脚本具备**自动备份原始明文**的保命机制。

### 自动化执行脚本 (`Encrypt-AllSPs.ps1`)

```powershell
# 1. 数据库连接信息配置
$ServerInstance = "localhost\MSSQLSERVER" # 替换为实际服务器地址
$DatabaseName   = "YourDatabaseName"      # 替换为实际业务库名
$BackupPath     = "C:\SQLBackup\StoredProcedures_$(Get-Date -Format 'yyyyMMdd_HHmmss')"

# 确保备份目录存在（必须执行，防止源码丢失）
if (!(Test-Path -Path $BackupPath)) { New-Item -ItemType Directory -Path $BackupPath | Out-Null }

# 2. 查询所有未加密的用户存储过程
$Query = @"
SELECT 
    '[' + s.name + '].[' + o.name + ']' AS ProcName,
    m.definition AS ProcDefinition
FROM sys.sql_modules m
JOIN sys.objects o ON m.object_id = o.object_id
JOIN sys.schemas s ON o.schema_id = s.schema_id
WHERE o.type = 'P' 
  AND o.is_ms_shipped = 0 
  AND m.is_encrypted = 0;
"@

# 获取结果集
$Procedures = Invoke-Sqlcmd -ServerInstance $ServerInstance -Database $DatabaseName -Query $Query -ErrorAction Stop

Write-Host "共找到 $($Procedures.Count) 个未加密的存储过程。开始处理..." -ForegroundColor Cyan

foreach ($Proc in $Procedures) {
    $ProcName = $Proc.ProcName
    $Def      = $Proc.ProcDefinition

    Write-Host "处理存储过程: $ProcName"

    # 3. 备份明文源码到本地文件
    $SafeFileName = $ProcName -replace '[\[\]]', ''
    $BackupFile = Join-Path -Path $BackupPath -ChildPath "$SafeFileName.sql"
    $Def | Out-File -FilePath $BackupFile -Encoding UTF8

    # 4. 正则替换逻辑
    # 匹配 CREATE 到第一个 AS 之间的定义，并强制插入 WITH ENCRYPTION
    $RegexPattern = '(?is)(^\s*CREATE\s+PROC(?:EDURE)?.*?)(?=\bAS\b)'
    
    if ($Def -match $RegexPattern) {
        # 将头部的 CREATE 替换为 ALTER
        $NewDef = $Def -replace '(?is)^\s*CREATE\s+', 'ALTER '
        $NewDef = $NewDef -replace $RegexPattern, "`$1 WITH ENCRYPTION `r`n"

        try {
            # 5. 刷回数据库执行加密
            Invoke-Sqlcmd -ServerInstance $ServerInstance -Database $DatabaseName -Query $NewDef -ErrorAction Stop
            Write-Host "  -> $ProcName 加密成功！" -ForegroundColor Green
        }
        catch {
            Write-Host "  -> $ProcName 加密失败: $($_.Exception.Message)" -ForegroundColor Red
        }
    } else {
        Write-Host "  -> 未匹配到标准的 CREATE PROCEDURE 头部，跳过加密。" -ForegroundColor Yellow
    }
}

Write-Host "全部执行完毕！原始源码已安全备份至: $BackupPath" -ForegroundColor Cyan
```

## 进阶加固：执行前自动剥离所有注释
原生 `WITH ENCRYPTION` 会将包含中文业务备注在内的整段源码进行加密。一旦加密被恶意破解，注释将一览无遗。最佳防线是**在加密前使用正则将注释彻底剔除**。

你可以在上述 PowerShell 脚本的第 4 步替换逻辑之前，插入以下“洗稿”代码：

```powershell
# ========================================================
# 进阶脱敏：在替换 $RegexPattern 之前执行，剥离所有注释信息
# ========================================================

# 1. 剔除多行注释 /* ... */
# (?s) 开启单行模式，使得 . 可以匹配换行符；非贪婪匹配 .*?
$Def = $Def -replace '(?s)/\*.*?\*/', ''

# 2. 剔除单行注释 -- 及该行后续所有内容
# 注意：若业务 SQL 字符串中恰好有 '--'（如 SELECT '1--2'），可能会被极小概率误伤。执行前需在测试库跑通。
$Def = $Def -replace '--.*', ''

# ========================================================
```
执行此进阶步骤后，刷入数据库并被加密混淆的代码将不再包含任何一个中文字符的业务备注。
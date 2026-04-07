# SQL Server 存储过程加密方案 (WITH ENCRYPTION)

## 场景与原理
为了防止拥有高级权限（如 `sa`）的人员轻易窥探和窃取核心业务存储过程源码，SQL Server 提供了原生的 `WITH ENCRYPTION` 选项。
- **作用**：通过对系统表中存储的源码进行内部混淆（异或算法），使 `sp_helptext` 或 SSMS 的“修改”功能失效，直接阻断明文查看。
- **性能零损耗**：加密仅作用于对象的保存与读取阶段，执行时跑的是已编译的二进制执行计划，**完全不影响查询性能**。
- **终极安全加固**：原生加密连注释也会一并加密。如果被破解，注释将一览无遗。最佳实践是**在加密前执行脱敏脚本剔除所有注释（如单行 `--` 与多行 `/*...*/`）**。
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

    # 4. 深度脱敏与正则替换逻辑
    # ==========================
    # 4.1 剥离所有注释信息（终极反解密策略）
    # 去除多行注释 /* ... */
    $NewDef = $Def -replace '(?s)/\*.*?\*/', ''
    # 去除单行注释 -- 及后续内容（注意：若业务字符串中恰好有 '--' 极小概率会被误伤，请人工评估）
    $NewDef = $NewDef -replace '--.*', ''
    
    # 4.2 匹配 CREATE 到第一个 AS 之间的定义，并强制插入 WITH ENCRYPTION
    $RegexPattern = '(?is)(^\s*CREATE\s+PROC(?:EDURE)?.*?)(?=\bAS\b)'
    
    if ($NewDef -match $RegexPattern) {
        # 将头部的 CREATE 替换为 ALTER
        $NewDef = $NewDef -replace '(?is)^\s*CREATE\s+', 'ALTER '
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
---
title: "SQLServer_Dacpac包加密与自动化部署"
created: 2026-04-08
updated: 2026-04-20
type: concept
tags: [security]
status: draft
date: 2026-04-08
category: SQL-Server
---

# SQLServer_Dacpac包加密与自动化部署 (PowerShell+AES256)

> 系列文档：[[SQLServer_存储过程加密方案_WITH_ENCRYPTION|WITH ENCRYPTION基础方案]] · [[SQLServer_高级加密方案_CLR_混淆|CLR高级混淆]]

**日期**: 2026-04-08
**关联**: 基于 2026-04-07 讨论的 SQL Server 存储过程加密方案 (防代码泄露) 的进一步延伸 (防介质泄漏)。

## 背景与痛点

微软原生的 `.dacpac` 包本质上是一个 ZIP 压缩包，解压后可以通过 `model.xml` 等文件直接查看完全明文的数据库架构定义（包括表结构、视图、存储过程的 T-SQL 源码等）。
在需要对外部分发或在不信任环境部署时，必须防止 `.dacpac` 介质被窃取导致核心业务逻辑泄漏。

## 解决方案

整套方案使用 PowerShell 原生实现，基于 .NET AES-256 算法，并结合 SQL Server 自带的 `SqlPackage.exe`。
**特点**:
1. 纯代码实现，无第三方依赖（不需要安装 7z/WinRAR 等加密压缩软件）。
2. 在部署阶段实现“阅后即焚”，尽可能缩短明文包在磁盘上的停留时间。

## 1. 打包端脚本：导出并加密 (`Export-And-Encrypt.ps1`)

该脚本从源数据库提取 `.dacpac`，使用 AES-256 加密生成 `.dacpac.enc` 文件，并在加密完成后立即删除明文文件。

```powershell
# 1. 配置参数
$SqlPackagePath = "C:\Program Files\Microsoft SQL Server\160\DAC\bin\SqlPackage.exe"
$SourceConnectionString = "Server=.;Database=YourDB;Integrated Security=True;TrustServerCertificate=True;"
$PlainDacpacPath = "C:\temp\YourDB.dacpac"
$EncryptedFilePath = "C:\temp\YourDB.dacpac.enc"
$Password = "YourStrongPassword123!"

# 2. 导出 Dacpac
Write-Host "开始提取 Dacpac..." -ForegroundColor Cyan
& $SqlPackagePath /Action:Extract /SourceConnectionString:$SourceConnectionString /TargetFile:$PlainDacpacPath
if ($LASTEXITCODE -ne 0) { throw "Dacpac 提取失败！" }

# 3. AES-256 加密函数
function Protect-File {
    param([string]$Path, [string]$Destination, [string]$Password)
    $salt = New-Object Byte[] 16
    [Security.Cryptography.RNGCryptoServiceProvider]::Create().GetBytes($salt)
    $pbkdf2 = New-Object Security.Cryptography.Rfc2898DeriveBytes($password, $salt, 100000)
    $aes = [Security.Cryptography.Aes]::Create()
    $aes.Key = $pbkdf2.GetBytes(32)
    $aes.IV = $pbkdf2.GetBytes(16)
    
    $fsOut = New-Object IO.FileStream($Destination, [IO.FileMode]::Create)
    $fsOut.Write($salt, 0, $salt.Length)
    $cs = New-Object Security.Cryptography.CryptoStream($fsOut, $aes.CreateEncryptor(), [Security.Cryptography.CryptoStreamMode]::Write)
    $fsIn = New-Object IO.FileStream($Path, [IO.FileMode]::Open)
    $fsIn.CopyTo($cs)
    $cs.Close(); $fsOut.Close(); $fsIn.Close()
}

# 4. 执行加密并清理明文
Write-Host "开始加密文件..." -ForegroundColor Cyan
Protect-File -Path $PlainDacpacPath -Destination $EncryptedFilePath -Password $Password
Remove-Item -Path $PlainDacpacPath -Force
Write-Host "打包并加密完成！输出文件: $EncryptedFilePath" -ForegroundColor Green
```

## 2. 部署端脚本：解密并发布 (`Decrypt-And-Publish.ps1`)

将加密后的 `.dacpac.enc` 分发到目标服务器，运行此脚本进行解密、执行部署（发布到目标数据库），并在部署完成后立刻强制删除明文的 `.dacpac`。

```powershell
# 1. 配置参数
$SqlPackagePath = "C:\Program Files\Microsoft SQL Server\160\DAC\bin\SqlPackage.exe"
$TargetConnectionString = "Server=.;Database=TargetDB;Integrated Security=True;TrustServerCertificate=True;"
$EncryptedFilePath = "C:\temp\YourDB.dacpac.enc"
$TempDacpacPath = "C:\temp\YourDB_temp.dacpac"
$Password = "YourStrongPassword123!"

# 2. AES-256 解密函数
function Unprotect-File {
    param([string]$Path, [string]$Destination, [string]$Password)
    $fsIn = New-Object IO.FileStream($Path, [IO.FileMode]::Open)
    $salt = New-Object Byte[] 16
    $fsIn.Read($salt, 0, $salt.Length) | Out-Null
    $pbkdf2 = New-Object Security.Cryptography.Rfc2898DeriveBytes($password, $salt, 100000)
    $aes = [Security.Cryptography.Aes]::Create()
    $aes.Key = $pbkdf2.GetBytes(32)
    $aes.IV = $pbkdf2.GetBytes(16)
    
    $cs = New-Object Security.Cryptography.CryptoStream($fsIn, $aes.CreateDecryptor(), [Security.Cryptography.CryptoStreamMode]::Read)
    $fsOut = New-Object IO.FileStream($Destination, [IO.FileMode]::Create)
    $cs.CopyTo($fsOut)
    $fsOut.Close(); $cs.Close(); $fsIn.Close()
}

try {
    # 3. 执行解密
    Write-Host "正在解密文件..." -ForegroundColor Cyan
    Unprotect-File -Path $EncryptedFilePath -Destination $TempDacpacPath -Password $Password
    
    # 4. 发布部署
    Write-Host "开始部署数据库..." -ForegroundColor Cyan
    & $SqlPackagePath /Action:Publish /SourceFile:$TempDacpacPath /TargetConnectionString:$TargetConnectionString
    if ($LASTEXITCODE -ne 0) { throw "部署过程发生错误！" }
    
    Write-Host "数据库部署成功！" -ForegroundColor Green
}
finally {
    # 5. 阅后即焚（强制清理明文）
    if (Test-Path $TempDacpacPath) {
        Remove-Item -Path $TempDacpacPath -Force
        Write-Host "临时明文 dacpac 已安全销毁。" -ForegroundColor Yellow
    }
}
```

## 注意事项

- **工具路径**: 脚本中的 `$SqlPackagePath` 需要根据目标服务器实际安装的 SQL Server 目录或 SSMS/Visual Studio 携带的 `DAC\bin` 路径进行微调。
- **安全性**: 密码在脚本中建议通过参数化传入，或者部署工具动态获取，避免直接硬编码在文件中。
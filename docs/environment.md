# 本机环境与运行方式

[回仓库首页](../README.md) · [按时间学课](study-calendar.md)

以下为已有环境记录；本次目录整理没有重新安装或重新核验全部依赖。

## 项目位置

```text
D:\python\File of python\Harness开发
```

本项目使用由 `D:\python\python.exe` 创建的独立虚拟环境 `.venv`。
Python 版本为 3.14.6；Git 和 Node.js 沿用电脑中已有的安装。

## 每次开始学习

在 PowerShell 中进入项目目录：

```powershell
Set-Location -LiteralPath 'D:\python\File of python\Harness开发'
& .\.venv\Scripts\python.exe --version
```

命令中的 `.\` 表示当前目录，`&` 表示执行指定程序。
使用这个完整的解释器路径，可以避开电脑上多个 Python 入口造成的混淆，
也不需要修改 PowerShell 执行策略或手动激活虚拟环境。

## 环境检查命令

```powershell
# 检查依赖之间是否存在版本冲突
& .\.venv\Scripts\python.exe -m pip check

# 确认测试工具能启动
& .\.venv\Scripts\python.exe -m pytest --version

# 查看当前项目的版本管理状态
git status --short
```

当前采用本目录已有的第一课实现，用 Python 条件检查校验工具参数。
后续参考实验已经使用 Pydantic 做参数和检查点格式校验；pytest 用于运行测试。
setuptools 是项目配置中声明的 Python 打包后端。

## 依赖与版本记录

- `pyproject.toml`：记录计划使用的依赖范围及未来的项目结构。
- `requirements-harness.txt`：保留本目录已有的学习依赖清单。
- `requirements-environment.lock.txt`：记录本次实际安装的依赖版本，安装成功后生成。
- `pytest.ini`：保留本目录已有的测试配置，将临时文件放在项目内。
- `.gitignore`：排除虚拟环境、缓存、密钥文件和后续运行记录。

当前 `.venv` 已恢复版本记录中的第一课核心依赖。`requirements-harness.txt` 还列有后续课程的
模型 SDK 等额外依赖；这份原有清单保留不变，额外依赖尚未恢复到新虚拟环境中。

如需在同类 Windows / Python 3.14 环境中恢复依赖，可在已创建的虚拟环境中执行：

```powershell
& .\.venv\Scripts\python.exe -m pip install -r .\requirements-environment.lock.txt
```

该命令会联网下载依赖；版本记录不保证其他操作系统或 Python 版本完全兼容。


第一课演示与测试命令请从 [项目首页](../README.md) 或 [第一课讲义](../lessons/01_tool_call/README.md) 打开。

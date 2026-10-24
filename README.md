# Harness

Harness Engineering 学习项目。

当前阶段：第一课，用模拟模型跑通一次工具调用。参考实验和对应测试已建立。

## 教材与学习进度

第一课是为本学习项目单独编写的 Python 教学实验，演示模型请求、工具分发、参数校验和结果回传。
claw-code 与开源 Codex 作为贯穿 12 周的主教材；Hermes 记忆机制另设五课专题。
当前先学第一课的数据流，再逐步完成真实源码精读，进度按实际讲解和练习验收。

- [教材来源与使用方式](docs/learning-sources.md)
- [完整 12 周课程：72 次动手课与 12 次复盘](lessons/12_week_course/README.md)
- [claw-code 与 Codex 源码主教材](lessons/source_mastery/README.md)
- [Hermes 记忆机制五课](lessons/hermes_memory/README.md)
- [12 周路线](docs/roadmap.md)
- [第一课讲义](lessons/01_tool_call/README.md)
- [第一课学习记录与问答](lessons/01_tool_call/learning-log.md)
- [接下来六次学习的总入口](lessons/six_day_pack/README.md)
- [第 7—9 天：权限、超时与恢复](lessons/days07_09/README.md)

当前已由学习者实际运行演示和测试，结果为 **13 passed**；第一课仍在讲解测试如何检查执行过程。

在本项目目录运行实验与测试：

```powershell
& .\.venv\Scripts\python.exe -X utf8 -m mini_harness.lesson01 --workspace .\lessons\01_tool_call\workspace
& .\.venv\Scripts\python.exe -X utf8 -m pytest -q
```

本课不联网，不调用模型 API，不产生模型费用。

## 已准备的六天入门课程

按每次约 2 小时安排，不绑定日期。前 3 次是工具反馈、注册与校验、有限循环；
后 3 次是 JSONL 记录、上下文裁剪、固定案例报告。
每次都有讲义、参考实验、留给学习者填写的小函数、单独的检查器、提示和聊天复盘模板。

从 [六天课程总入口](lessons/six_day_pack/README.md) 开始；
实际学习进度记在 [study-log.md](lessons/six_day_pack/study-log.md)，目前全部留为待学习。
材料准备完成不代表学习者已经完成。

默认 `pytest -q` 运行参考实现检查，加入第 7—9 天与记忆缩影后当前为 119 项；练习要显式运行相应的
`exercises/check_dayXX.py`，未填写时会提示 `NotImplementedError`。
运行核验见 [verification.md](lessons/six_day_pack/verification.md)。

## 已准备的第 7—9 天

继续按每次约 2 小时安排：第 7 天区分注册与许可，第 8 天处理固定工具进程超时，
第 9 天用 SQLite 保存只读模拟任务，再启动另一个进程恢复。
每一天都有讲义、参考实验、待填写练习、检查器、分级提示和聊天入口。

从 [第 7—9 天总入口](lessons/days07_09/README.md) 打开；
实际学习进度留在该目录的 [学习日志](lessons/days07_09/study-log.md)，仍为待学习。
新增 43 项参考检查；详细范围与限制见 [本批核验](lessons/days07_09/verification.md)。

## 完整课程与材料

12 周讲义、30 个自编修复任务、独立评分材料生成器、实验与架构模板、面试练习已备好。
30 题材料校准不等于真实模型修复成绩；未来完整 Agent 的 run/resume/eval、Docker 执行器等仍为课程实现任务。
当前不产生模型调用费用。核验范围见 [course-verification.md](course-verification.md)。

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

## 当前边界

- 项目使用 Git 管理。GitHub 同步包含学习代码、测试、讲义、路线与学习记录；虚拟环境、缓存和密钥文件由忽略规则排除。
- 第一课代码位于 `mini_harness/lesson01.py`，测试位于 `test_lesson01.py`；沿用本目录已有的文件，保留其实现。
- 六天参考实验位于 `mini_harness/lesson01_cases.py` 与 `lesson02.py` 到 `lesson06.py`；只处理离线教学数据。
- 第 7—9 天参考实验位于 `mini_harness/lesson07.py` 到 `lesson09.py`；第 8 天的固定 worker 不执行模型生成代码，第 9 天仅恢复只读模拟任务。
- `pyproject.toml` 中的 `mini-harness` 命令入口尚未实现；本课直接运行 Python 文件，不安装这个入口。
- 第一课测试验证教学实验的行为；真实模型效果尚未验证。
- Docker、模型 API 和密钥留到对应课程中配置；本阶段没有发起模型调用。

从第一课讲义开始，运行后把终端输出和自己的理解带回聊天，再逐步进入下一项实验。

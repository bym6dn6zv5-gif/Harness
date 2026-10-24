# 实验操作约定

## 固定目录与已可运行的命令

代码目录是 `D:\python\File of python\Harness开发`；终端先执行：

```powershell
Set-Location -LiteralPath 'D:\python\File of python\Harness开发'
& .\.venv\Scripts\python.exe -X utf8 -c "import sys; print(sys.executable); print(sys.version)"
git --version
git status --short
```

`.venv` 是项目环境，Node.js 不是这些 Python 实验的必需依赖。
缺少命令时先带报错来聊天，不用反复安装，也不把全局 Python 当成本项目环境。

下面是现成的参考实验，均不调用模型 API：

```powershell
& .\.venv\Scripts\python.exe -X utf8 -m mini_harness.lesson03 --scenario normal
& .\.venv\Scripts\python.exe -X utf8 -m mini_harness.lesson07 --scenario denied
& .\.venv\Scripts\python.exe -X utf8 -m mini_harness.lesson08 --scenario timeout
& .\.venv\Scripts\python.exe -X utf8 -m mini_harness.lesson09 start
& .\.venv\Scripts\python.exe -X utf8 -m pytest -q
```

第 9 天从输出中复制恢复命令。学习者填写练习后还要显式检查，例如：

```powershell
& .\.venv\Scripts\python.exe -X utf8 -m pytest .\exercises\check_day07.py -q
```

默认检查不收集尚未填写的 `check_dayXX.py`，因此参考测试通过不代表练习完成。

## 完整项目的文件分工

以下是后续动手时逐步创建的目标结构，不是本次已经实现的第二套完整 Agent：

```text
mini_harness/
  cli.py                 第 3 周起逐步完成
  project/
    messages.py          内部消息与结果类型
    client.py            mock 与单一服务商适配
    loop.py              继续、执行、回传、停止
    tools.py             读、搜、补丁、测试的受限入口
    environment.py       容器生命周期与超时
    state.py             SQLite 检查点
    context.py           构造发送视图
    events.py            结构化轨迹与用量
    evaluation.py        独立评分与批量记录
tests_project/           自己新增的行为检查
docs/                    实际项目的说明与报告
.harness/                每次运行的工作区和记录，Git 忽略
```

先完成当前课需要的文件，不要一次建立全部空壳。现有 lesson 模块和 starter 保留为教材。
每次新增重要边界写一项行为检查，用具体测试文件运行；避免只做“每行代码对应一个断言”的测试。

目标命令入口在实现之后再运行：

```text
mini-harness run --workspace <任务副本> --task <问题> --mode mock --max-steps 8
mini-harness resume --state <检查点数据库>
mini-harness eval --split dev --config <冻结配置>
```

`pyproject.toml` 已声明未来入口，但 `mini_harness.cli:main` 当前尚未实现。
上面三个命令是验收接口草案，尖括号必须替换，当前不能照抄当作已安装工具。

## 每天的提交物

在自己的学习记录里保留：本次目标、修改文件、运行命令、预期与实际、首个失败、下一步。
截图不是必需；文本错误的最后几行通常更便于分析。不要粘贴密钥、完整请求头或个人文件内容。

Git 操作按“看 status → 看 diff → 只暂存本次文件 → 看暂存 diff → 提交”推进。
提交消息描述具体变化，如“reject invalid search limits before reading files”。
运行数据留本机，报告保留必要的匿名结果及可复现配置。

## 测试与执行环境

Harness 自身的可信代码和 mock 检查可在项目环境运行。
Agent 修改后的任务源码以及最终评分放入第 4 周准备的容器，不在宿主直接执行。
第 8 天的 worker 是本教材固定进程实验，不是任意代码执行隔离。

如果 pytest 临时目录权限报错，先记录完整路径。
需要改 basetemp 时选择项目内全新且不存在的目录，避免指定存有学习资料的文件夹；
pytest 可能清理它使用的临时目录。不要用递归删除“修复”不认识的权限问题。

## 真实模型调用前的最后准备

由你实际选择一个能访问、支持所需接口的服务，核对官方文档和当日价格，配置宿主密钥与硬限额。
先 mock，再一次小调用，再观察 usage 与账单。全课程首次费用上限暂为人民币 100 元。
本地账本不能可靠约束时继续 mock，不以请求完成后才计算的估计冒充硬上限。
教材生成、离线测试与材料校准都没有产生模型费用。

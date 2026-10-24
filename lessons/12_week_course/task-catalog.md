# 30 个固定任务：准备、校准和独立评分

材料为本课程自编的单文件微型修复题，入口统一为 `solve(...)`。
它们帮助检查运行循环、工具执行和评分流程，任务规模较小，不代表真实仓库修复能力或招聘分数线。
T01—T20 固定为开发集，T21—T30 固定为保留集。

## 已可运行的材料命令

```powershell
Set-Location -LiteralPath 'D:\python\File of python\Harness开发'
& .\.venv\Scripts\python.exe -X utf8 -m mini_harness.course_tasks list
& .\.venv\Scripts\python.exe -X utf8 -m mini_harness.course_tasks verify
& .\.venv\Scripts\python.exe -X utf8 -m mini_harness.course_tasks prepare --id T01
```

list 默认只显示 20 个开发任务。verify 只执行本课程自编且可信的起始源码和参考源码，
确认每题起始版本至少失败一个评分案例、参考版本通过全部案例；它不会加载你准备或修改过的工作区。
输出 `authored_fixture_calibration`、`real_model_evaluation: false`，不能称为 Agent 30 题通过率。

prepare 在 `.harness/course-tasks/T01-<唯一编号>` 新建：

```text
workspace/
  task.py             Agent 可以修改的起始源码
  README.md           精确需求和允许修改范围
  test_public.py      只覆盖一个案例的公开测试
grading/
  test_grading.py     全部固定评分案例，位于工作区之外
metadata.json         材料及评分指纹、绝对目录
```

每次准备都是新目录，不覆盖上次结果。仅把 workspace 交给 Agent，
不要把主项目中的材料模块、参考答案或 grading 加到工具检索范围。
所有题要求输入容器保持不变；浮点结果允许极小舍入误差，布尔值不能用 0/1 顶替。

## 开发集

| ID | 修复主题 |
| --- | --- |
| T01 | 空白日期输入 |
| T02 | 空列表平均数 |
| T03 | 数值限幅与非法区间 |
| T04 | 按首次出现顺序去重 |
| T05 | 保留最后不足一块的数据 |
| T06 | 逗号字段与空白 |
| T07 | 严格布尔字符串解析 |
| T08 | 只分割首个等号 |
| T09 | 字符串频次统计 |
| T10 | 连续空白分词的 slug |
| T11 | 端口边界 |
| T12 | 重叠子串计数 |
| T13 | 展开一层列表 |
| T14 | 右侧配置覆盖 |
| T15 | 最短字符串及并列规则 |
| T16 | 括号顺序与嵌套 |
| T17 | 中位数与输入不变 |
| T18 | 移动平均的完整窗口 |
| T19 | 除零哨兵 |
| T20 | 重复键取最后值 |

## 保留集

| ID | 修复主题 |
| --- | --- |
| T21 | 嵌套键缺失 |
| T22 | 日期闭区间 |
| T23 | JSON 列表约束 |
| T24 | 文件扩展名边界 |
| T25 | 无向配对去重 |
| T26 | 排行榜同分次序 |
| T27 | 退避序号 |
| T28 | 最近秩百分位 |
| T29 | 换行归一化 |
| T30 | 闭区间相交 |

完整材料和参考源码在 `mini_harness/course_task_data.py`，为方便教学而可见。
保留集是实验使用约定，不能声称从未公开或对所有读者未知。
冻结实现后再显式添加 `--allow-holdout` 准备保留任务；这只是防止误用的开关，不是权限安全机制。
如果已经看过保留题解或据此改进策略，在报告中说明泄漏，并另建未参与开发的任务集。

## 如何接入第 8 周评分器

Agent 只运行公开测试。Agent 停止后，由宿主启动独立评分容器：
只读挂载 workspace 和 grading，把 `HARNESS_TASK_WORKSPACE` 设为容器内任务目录，
固定运行 grading 中的 pytest；不传模型密钥。
测试输出、容器状态与超时由第 4 周执行器收集。
评分前后校验 metadata 中的 grading_sha256，防止评分规则随 Agent 修改。

这是宿主评分器的**目标行为**，课程准备器没有实现 Docker 调度或 Agent 批量运行。
不要在宿主直接运行 Agent 修改后的 task.py；verify 也不是这种运行器。
公开测试通过不足以判定任务成功，外部测试必须单独执行。

## 材料版本与扩展

准备器记录整个 TASKS 的 material_sha256；正式实验冻结该指纹和课程仓库提交。
修改需求、起始代码或评分案例都要升级实验版本，不能混算旧结果。
这批题目只覆盖小函数边界，后续增加多文件依赖、较长定位链和测试环境问题，另行报告难度与分组。

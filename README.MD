<p align="center"><img src="assets/cockpit-logo.png" width="280" alt="cockpit 驾驶舱" /></p>

<p align="center"><strong>cockpit 驾驶舱 · AI 开发与内容工作流</strong></p>
<h1 align="center">把案例做成系统，把过程变成作品。</h1>
<p align="center">从需求整理、AI 开发到图文、视频与代码交付，让每一步都有记录。</p>
<p align="center">喜文FDE案例系列 · Python · MIT</p>
<p align="center"><a href="https://resume.fangnan.club/cockpit/">了解 cockpit</a> · <a href="https://resume.fangnan.club/">认识作者</a> · <a href="LICENSE">MIT 许可证</a></p>

## 认识作者，一起把想法做出来

**我是方楠，智能体工程师 / 全栈工程师。**

专注 AI 编程、智能体开发与业务系统落地，具备 Python、前后端开发、数据工程与技术交付经验。这个项目记录我如何把具体需求拆成开发任务，再把系统实现、操作演示和项目资料组织成可以持续维护的工作流。

**有相似需求？欢迎交流业务场景、AI 开发实践与项目合作。**

| 联系方式 | 入口 |
| :--- | :--- |
| 个人主页 | [方楠 · 个人简历](https://resume.fangnan.club/) |
| 电话 / 微信 | 16607557430 |
| 抖音 | 喜文官方企业号 · 抖音号：75604309245 |
| cockpit 介绍 | [cockpit 驾驶舱](https://resume.fangnan.club/cockpit/) |

<p align="center"><img src="assets/douyin-qr.png" width="320" alt="喜文官方企业号抖音码，抖音号75604309245" /></p>
<p align="center"><strong>关注喜文官方企业号，看需求如何一步步变成系统。</strong><br />真实开发过程 · 系统操作演示 · 项目复盘</p>

---

## 项目版本

当前版本：**v0.1**。项目版本以 VERSION 为准，变更见 CHANGELOG.md；不等同于数据库模式或中台记录版本。

## 检测认证进度看板解决什么问题？

面向检测认证，围绕“委托收样、检测、报告与发证状态追踪”提供可操作的演示系统。当前交付状态：**已完成中台功能验收；用于业务演示，未完成生产部署验收**。

## 系统架构

```text
浏览器页面 ⇄ 同源 JSON API ⇄ Python 业务后端 ⇄ SQLite 数据库
后端校验、事务写入、版本冲突保护与操作审计；前端展示与 CSV 导出
```

cockpit 用于 AI 开发过程，不是此系统运行的必需服务。本系统没有因为使用 AI 开发而自动接入运行时大模型。

## 本地运行

```bash
python3 backend.py --port 8000
```

打开 http://127.0.0.1:8000/ 。Python 3.10+，后端只用标准库。首次启动从 seed.json 初始化 data/business.sqlite3；后续启动保留数据。必须启动后端，不能直接打开 HTML 替代联调。独立运行只监听 loopback，不提供独立账号系统；中台访问受登录、权限和 CSRF 保护。

验证命令：`python3 smoke-test.py`，使用临时数据库验证写入、版本冲突、非法数据拒绝、重开持久化和审计。完整业务浏览器联调及在线服务重启测试已通过，结果见 backend-acceptance.json 与 backend-online-acceptance.json。

数据库为多浏览器共享数据，刷新读取他人更新；过期版本保存返回409，必须刷新重试。确认重置影响所有访问本项目的浏览器，并保留变更前审计快照。旧浏览器本地存档不自动导入。尚未进行生产容量压测，未接真实硬件或外部通知。

## 代码目录

```text
index.html     前端页面与异步 API 交互
backend.py     业务后端、SQLite 事务与审计
backend-config.json 项目标识
seed.json      脱敏初始化数据
smoke-test.py   可运行后端数据库测试
VERSION        项目发布版本
CHANGELOG.md   版本变更记录
assets/        README 品牌素材
data/          运行数据库（自动创建，不提交）
README.MD      项目说明
LICENSE        MIT 许可证
```

## 操作与业务规则

## 操作验收

1. 点击“新增委托单”，使用 WT- 加 4～12 位数字的虚构编号，样品使用 YP- 加 4～12 位数字，保存后进入收样。
2. 用编号搜索，点击“详情 / 流转”，推进至检测，选择检测结论，再推进至报告、发证，最后完成发证。
3. 每次操作后检查时间线、四个环节停留天数和顶部指标。检测不通过进入报告后禁止发证。
4. 组合使用编号、环节、结论和超时筛选，导出 CSV 只包含当前筛选结果。
5. 修改检测类别或虚构样品编号，刷新验证保存；重置必须经过确认，取消不会清除数据。

## 口径与边界

- 天数按连续 24 小时折算到 1 位小数；超时用未四舍五入的实际时长判断。时限分别为 2、5、3、2 天。台账每分钟刷新时效；详情打开或推进时重新计算。
- 指标随筛选变化，通过率分母仅包含已判定单；无已判定数据时显示横线。历史环节使用离开时间固定时长。
- 不通过委托保留在报告环节；本演示不含复检、撤销流转和退回功能。报告/发证仅为状态演示，不生成真实报告与证书。



## 验证范围

发布前在独立导出目录验证启动与入口访问；实际结果随发布回执记录。业务验收状态与代码发布状态分开管理。原有测试记录属于历史开发验证，不代表生产环境验收。

## 交流与贡献

使用问题请在本仓库 Issues 提供环境、复现步骤与脱敏截图。欢迎提交改进建议或 Pull Request；业务交流见顶部公开联系方式。如果对你有帮助，欢迎 Star 收藏。

## 项目地址

- GitHub: https://github.com/fn199544123/cockpit-fde-13-certification
- 码云: https://gitee.com/xiwenfde/cockpit-fde-13-certification

## 许可证

本项目原创代码采用 [MIT](LICENSE)，允许在遵守许可声明的前提下使用、修改与商用。第三方组件适用各自许可证；cockpit 品牌素材用于项目归属展示，不代表商标授权或官方背书。

演示数据均为虚构编号与通用业务信息，不代表真实客户经营数据。

---

<p align="center"><strong>cockpit 驾驶舱 · 喜文FDE案例系列</strong></p>

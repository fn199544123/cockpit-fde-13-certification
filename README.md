<p align="center">
  <img src="assets/cockpit-logo.png" width="280" alt="cockpit 驾驶舱" />
</p>

<p align="center"><strong>cockpit 驾驶舱 · AI 开发实作</strong></p>
<h1 align="center">把业务需求，做成看得见、用得上的系统。</h1>
<p align="center">从需求拆解到系统实现，记录 AI 开发的真实过程。</p>
<h2 align="center">检测认证进度看板</h2>
<p align="center">喜文FDE案例系列</p>
<p align="center">检测认证 · 委托收样、检测、报告与发证状态追踪 · 业务演示系统</p>
<p align="center"><a href="https://resume.fangnan.club/cockpit/">了解 cockpit</a> · <a href="https://resume.fangnan.club/">认识作者</a></p>


## 认识作者，一起把想法做出来

**我是方楠，智能体工程师 / 全栈工程师。**

专注 AI 编程、智能体开发与业务系统落地，具备 Python、前后端开发、数据工程与技术交付经验。从需求梳理、架构设计到系统实现，关注技术怎样解决具体业务问题。

这里分享我使用 cockpit 驾驶舱开展 AI 开发的项目：需求怎样拆、系统怎样做、业务流程怎样验证。希望这些可查看、可复现的实现，为你的下一个项目提供参考。

**有相似需求？欢迎交流业务场景、AI 开发实践与项目合作。**

| 了解我 / 联系我 | 入口 |
| :--- | :--- |
| 个人主页 | [方楠 · 个人简历](https://resume.fangnan.club/) |
| 电话 / 微信 | 16607557430 |
| 合作邮箱 | [16607557430@163.com](mailto:16607557430@163.com) |
| 抖音 | 智效上门AI解决方案 · 抖音号：74759905847 |
| cockpit 介绍 | [了解 cockpit 驾驶舱](https://resume.fangnan.club/cockpit/) |

<p align="center">
  <img src="assets/douyin-qr-placeholder.svg" width="200" alt="抖音二维码待提供；此处为不可扫码的版式占位" />
</p>
<p align="center"><strong>关注我的抖音，看需求如何一步步变成系统。</strong><br />真实开发过程 · 系统操作演示 · 项目复盘</p>

作者介绍与联系方式整理自[个人简历网站](https://resume.fangnan.club/)。抖音二维码原图待补。

<p align="center"><strong>喜欢这类项目，欢迎 Star 收藏，也欢迎通过 Issues 一起完善。</strong></p>

---

## 检测认证进度看板解决什么问题？

面向检测认证，围绕“委托收样、检测、报告与发证状态追踪”提供可操作的演示系统。当前交付状态：**已完成中台功能验收**。

## 系统架构

```text
浏览器页面 → JavaScript 校验与业务计算 → localStorage
浏览器页面 ← 列表 / 指标 / CSV ← 当前浏览器中的演示记录
```

cockpit 用于 AI 开发过程，不是此系统运行的必需服务。本系统没有因为使用 AI 开发而自动接入运行时大模型。

## 本地运行

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

打开 http://127.0.0.1:8000/index.html 。无需构建或后端依赖，也可直接打开 index.html；建议固定 HTTP 地址，避免浏览器存储来源变化。

## 代码目录

```text
index.html     页面、样式与业务逻辑
smoke-test.py  独立浏览器功能测试
assets/       README 品牌素材
README.md      项目说明
LICENSE        MIT 许可证
```

## 操作与业务规则


入口为当前目录 `index.html`，单文件内嵌 CSS/JS，无外部依赖，可直接用浏览器打开。演示身份统一为 douyin。

## 本地运行

在宿主机当前项目目录执行：

```bash
python3 -m http.server 18113 --bind 127.0.0.1
```


## 操作验收

1. 点击“新增委托单”，使用 WT- 加 4～12 位数字的虚构编号，样品使用 YP- 加 4～12 位数字，保存后进入收样。
2. 用编号搜索，点击“详情 / 流转”，推进至检测，选择检测结论，再推进至报告、发证，最后完成发证。
3. 每次操作后检查时间线、四个环节停留天数和顶部指标。检测不通过进入报告后禁止发证。
4. 组合使用编号、环节、结论和超时筛选，导出 CSV 只包含当前筛选结果。
5. 修改检测类别或虚构样品编号，刷新验证保存；重置必须经过确认，取消不会清除数据。

## 可重复测试

在宿主机安装有 Python Playwright 及其 Chromium 的环境中执行：

```bash
python3 smoke-test.py
```

脚本在宿主机本地随机端口运行临时服务器，使用独立浏览器上下文，不影响演示者数据；结束后关闭测试服务器。生成 `smoke-test-results.json`、`evidence-desktop.png`、`evidence-mobile.png`。实际执行结果见 development-result.json。

## 口径与边界

- 演示数据·仅当前浏览器保存。localStorage 键为 `development-13-orders-v1`。不同域名/端口/浏览器分别保存；清理浏览器数据会丢失记录。
- 天数按连续 24 小时折算到 1 位小数；超时用未四舍五入的实际时长判断。时限分别为 2、5、3、2 天。台账每分钟刷新时效；详情打开或推进时重新计算。
- 指标随筛选变化，通过率分母仅包含已判定单；无已判定数据时显示横线。历史环节使用离开时间固定时长。
- 不通过委托保留在报告环节；本演示不含复检、撤销流转和退回功能。报告/发证仅为状态演示，不生成真实报告与证书。
- 无后台、真实账号认证、多用户协同、外部通知或硬件接入；无对外发布。

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

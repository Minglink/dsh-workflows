# 社区与产业破甲资源地图（2026-11 调研）

> 调研时间：2026-11-23（Asia/Shanghai）。
> 星标 / 最近推送数据为调研当日通过 GitHub API 实查所得；其余渠道数据均标注来源或标"未核实"。
> 立场说明：本地图服务于 LLM 安全研究与对抗评测工作流建设（探针→画像→定制→验证→多轮→手册），所有资源均为社区公开发布的红队 / 提示安全研究资产，视角以"评测、防御、理解对齐边界"为主。
> 口径："破甲"≈ jailbreak / 破限 / 对抗提示词；"炼化"≈ 对大量破甲词的分类、去重、打标与效果评测。

---

## 一、收藏仓库 / 合集（13 个）

| # | 名称 | 活跃度（最近更新 / 星标量级） | 内容构成 | 我们的炼化姿势（抽什么进军械库） | URL |
|---|------|------------------------------|----------|----------------------------------|-----|
| 1 | elder-plinius/L1B3RT4S | ★23,462 / 推送 2026-10-28（API 实查） | Pliny the Liberator 维护的"全旗舰模型解放提示词"矩阵，按厂商分目录（OpenAI/Anthropic/Google/xAI/Meta/DeepSeek 等），每个模型多个手法文档，含 REFUSAL-BYPASS 等 | 军械库的主粮：直接按"厂商→模型→手法"目录镜像入库；把其中高频词汇（如 `<NEW_PARADIGM>`、{%心空白%} 式占位咒语）抽出做流派标签 | [GitHub](https://github.com/elder-plinius/L1B3RT4S) |
| 2 | elder-plinius/G0DM0D3 | ★12,868 / 推送 2026-07-15（API 实查） | "上帝模式"策略库 + 运行器：把成熟破甲模板与模型配对竞速（CLAUDE 3.5 END/START 边界反转等 5 组经典 combo），并内置 ULTRAPLINIAN 多模型并行竞速与打分（quality/filteredness/speed，拒答 -9999） | 不是当模板抄，而是抄它的"竞赛机制"：同一条定制破甲词并行打 5~55 个模型/档位，胜者优先入库，天然完成效果标注 | [GitHub](https://github.com/elder-plinius/G0DM0D3) |
| 3 | 0xk1h0/ChatGPT_DAN | ★13,344 / 推送 2026-11-09（API 实查） | 老牌 DAN 系谱仓库：DAN 1.0→若干世代变体、大量社区口头流传版本按年代排列，是最早的"破甲词考古地层剖面" | 抽"版本演化链"做纵向语料：同一流派的世代差异正是训练我们拒绝画像模型的好教材（哪个字眼退化、哪个字眼仍在起效） | [GitHub](https://github.com/0xk1h0/ChatGPT_DAN) |
| 4 | 0xeb/TheBigPromptLibrary (TBPL) | ★5,547 / 推送 2026-11-10（API 实查） | 大厂产品级系统提示词 + 自定义指令 + 破甲词 + GPT 防护提示词的巨型馆藏，含厂商、版本、工具脚本、教程文章（持续更新至 2026-11） | 画像资料库：把目标产品的官方/泄露系统提示词入"靶标画像"表，破甲词是在对这些约束求解，知己知彼 | [GitHub](https://github.com/0xeb/TheBigPromptLibrary) |
| 5 | Yuuqq/TheBigPromptLibrary（中文 Fork） | ★10 / 推送 2026-11-22，GitHub Actions 每日自动同步上游并 LLM 翻译（README 声称覆盖率 99.9%） | 中文翻译版 TBPL：在线站带全文倒排索引、AI 自动打标（类别/厂商/场景）、中英对照、基于标签+Jaccard 相似度的相似条目推荐、PWA 离线 | 直接抄它的"炼化基建"：自动打标 schema + 相似条目推荐器，就是我们聚合库"去重 + 关联推荐"的现成设计参考 | [GitHub](https://github.com/Yuuqq/TheBigPromptLibrary) |
| 6 | LouisShark/chatgpt_system_prompt | ★10,862 / 推送 2026-11-09（API 实查） | "PromptCraft"：上万条 GPTs / 产品的系统提示词集合 + 如何套取系统提示词的教程 + 如何写防护，社区长期共建 | 与 TBPL 二选一或互补：教程部分（如何让模型自曝 prompt）正好是我们"拒绝画像/画像探针"步骤的弹药来源 | [GitHub](https://github.com/LouisShark/chatgpt_system_prompt) |
| 7 | asgeirtj/system_prompts_leaks | ★72,400 / 推送 2026-11-20（API 实查） —— 本次调研最重磅 | "每一款热门聊天体的隐藏系统提示词，全量、每个版本"，覆盖 ChatGPT、Claude、Gemini、Codex、Antigravity、Grok、Kimi、Qwen、GLM、Cursor、Perplexity、DeepSeek 等 30+ 产品，每日更新；另有 AgentDossier 站点镜像 | 当作"对齐强度基准库"：对比同一产品新旧版本系统提示词的措辞收紧史，反过来指导我们探针库何时要换代 | [GitHub](https://github.com/asgeirtj/system_prompts_leaks)；站点镜像 [AgentDossier](https://sushegaad.github.io/AgentDossier/agents/asgeirtj-system-prompts-leaks/) |
| 8 | verazuo/jailbreak_llms | ★3,898 / 推送 2024-12-24（稳定数据集，不再滚动） | CCS'24 论文数据集：从 Reddit/Discord/网站/开源集抓取的 15,140 条 ChatGPT 对话，含 1,405 条越狱提示词，附分类、风格与回应标注，且有"破甲词生命周期"追踪（发布→流行→被封） | 军械库第一座现成的"打了标的弹药库"：1,405 条真人破甲词 + 学者级标注，直接做我们的去重基线和风格 taxonomy 起点 | [GitHub](https://github.com/verazuo/jailbreak_llms) |
| 9 | CyberAlbSecOP/Awesome_GPT_Super_Prompting | ★约 4,210（git-stars 快照 2026-05-05 显示）；今日 API 双拼写 404，疑似改名或封存，未核实 | ChatGPT 破甲、GPTs 提示词泄露、Prompt Injection、LLM 提示安全大合集，连 r/ChatGPTJailbreak 等 12 个社区情报源目录 | 若还能访问：抽其"Prompt Sources 社区索引"当我们的可持续情报订阅表；仓库本体不作为依赖 | [GitHub](https://github.com/CyberAlbSecOP/Awesome_GPT_Super_Prompting)；佐证快照 [git-stars.org](https://git-stars.org/ja/repositories/topic/jailbreak) |
| 10 | corca-ai/awesome-llm-security | ★1,722 / 推送 2025-08-20（API 实查） | 以学术论文/工具为主的 LLM 安全 awesome 列表：攻击、防御、benchmark 分区，条目多带一句话点评 | 抽"论文→代码→数据集"三元组当军械库的"学术后勤线"，尤其其后门与防御区，帮我们把破甲流派跟对应评测对上号 | [GitHub](https://github.com/corca-ai/awesome-llm-security) |
| 11 | scadastrangelove/awesome-ai-security-tools | ★1,768 / 推送 2026-11-21（API 实查） | 2026 年仍高频维护的 AI 安全工具大总账：LLM 红队、Agent 安全、护栏模型索引、狱攻数据集索引，含众多上下游 awesome（如 Awesome MLLM/LLM Guardrails） | 把它当"采购目录"：我们缺哪一类工具（护栏对比、多模态、Agent 面）先来这里检索再决定是否自研 | [GitHub](https://github.com/scadastrangelove/awesome-ai-security-tools) |
| 12 | r/ChatGPTJailbreak（Reddit 社区） | 长青社区（更新频度未核实） | Reddit 最大破甲实践社区，站内 Wiki/Megathread 沉淀历代帖子 + 旗下关联板块（r/GPT_jailbreaks、r/ChatGptDAN 等，见合集 #9 索引） | 作"原矿产地"持续采样：新招式几乎都在这里首发；搭一个日采器把我们关心的关键词丢进去挖新品 | [Reddit](https://www.reddit.com/r/ChatGPTJailbreak/) |
| 13 | HuggingFace 破甲数据集三件套 | 各自 2025 年快照（更新情况未核实） | allenai/wildjailbreak（WildTeaming 派生的大规模带注记越狱问答集）；qualifire/prompt-injections-benchmark；UdayGattu23/PromptDataset-v2-Complete（18 万条混合，含对抗样本与安全用例） | 做训练/评测用的合成燃料：wildjailbreak 的 attack_type 注记字段可直接喂给我们画像分类器；qualifire 当注入 vs 破甲的分界对照组 | [wildjailbreak](https://huggingface.co/datasets/allenai/wildjailbreak)、[qualifire benchmark](https://huggingface.co/datasets/qualifire/prompt-injections-benchmark)、[PromptDataset v2](https://huggingface.co/datasets/UdayGattu23/PromptDataset-v2-Complete) |

补充一嘴：f/awesome-chatgpt-prompts（现已迁移至 f/prompts.chat，★17.8 万）属通用角色提示词库而非破甲专属，仅在其 role-play 流派溯源时略有参考价值，未计入正文表格。

| # | 名称（补充） | 活跃度 | 内容构成 | 炼化姿势 | URL |
|---|--------------|--------|----------|----------|-----|
| 14 | tortious/2025__Awesome_GPT_Super_Prompting（#9 的现存镜像） | ★1 / 推送 2025-02-13（API 实查），低热度但可访问 | 原 Awesome_GPT_Super_Prompting 内容的镜像副本：破甲词、GPTs 泄露、注入技巧三大区块照搬 | 当 #9 无法访问时的兜底镜像，顺手把其"Prompt Sources 社区索引"抢救进我们的订阅表 | [GitHub](https://github.com/tortious/2025__Awesome_GPT_Super_Prompting) |
| 15 | qualifire/security（HF 主题合集页） | 合集更新至 2025-09（页面显示） | 把 prompt-injections-benchmark、rogue-security/prompt-injection-jailbreak-sentinel-v2 等 safety/注入条目集中陈列的合集导航 | 沿着这条合集往下钻，可以低成本捡到更多带注入/越狱标注的小型验证集（sentinel-v2 已露头，值得单测） | [HF 合集](https://huggingface.co/collections/qualifire/security) |

---

## 二、工具与流水线（11 个）

### 2.1 Microsoft PyRIT
- **定位**：微软出品、当前事实标准之一的生成式 AI 红队自动化 SDK（★5,027，推送 2026-11-22，API 实查，极活跃）。
- **核心流水线步骤**：Scenario（评测目标/场景打包）→ Attack Technique（executor + converters + datasets + 策略的单个命名攻击）→ Converters（转换器可正交叠加：编码、翻译、越狱改写……）→ Orchestrator/Executor 循环发包 → Scorer（RefusalScorer / TrueFalseScorer / LLM 裁判等打分）→ Memory 存储 → 报告。
- **我们能搬哪一步进 15 步工作流**：两处。(a) "API 验证"步直接改造成 PyRIT Scorer 范式——先判"是否拒绝"再判"内容是否达标"，拒绝画像数值化；(b) Converter 的可组合思想用在"定制破甲词生成"步，把我们产出的破甲词当 base converter，后面自动挂 leetspeak/编码/翻译等二级变异再进验证。
- **上手成本**：中。pip 可装、Python 生态熟悉即半天起步；但要吃透 Scenario/Attack 概念划分建议先读官方 framework 文档。
- **URL**：[GitHub](https://github.com/microsoft/PyRIT)｜[Framework 概念文档](https://raw.githubusercontent.com/microsoft/PyRIT/main/doc/code/framework.md)
- **踩坑提示**：新版把"场景/攻击技术"拆得很细且持续重构（官方自己也承认在重新发现模式），升级依赖时先看 changelog，别把复现实验建立在 Scenario API 的形状上。

### 2.2 NVIDIA garak
- **定位**：老牌 LLM 漏洞扫描仪（leondz 始创，现归 NVIDIA；★10,131，推送 2026-11-18，API 实查）。
- **核心流水线步骤**：probe×generator 网格扫描 → 每个 probe 带一组扰动/注入/越狱载荷 → 但不做单模型定制，主打广度；v0.14 起出 HTML 报告与 JSON 配置，v0.15（2026-05）新增 Agent-Breaker（攻击 Agent 的工具面）、系统提示词抽取探针、多轮 GOAT 探针，另支持 NeMo-Guardrails 接入与拒绝检测改进。
- **我们能搬哪一步进 15 步工作流**：搬"探针测试"的组织形态——把我们的探针库改成 garak 的 probe 插件规格，就免费继承其报告器、CI 配置与拒绝检测判定，一举把"探针库→报告"链路工程化。
- **上手成本**：中。CLI 一行即可扫起来，自写 probe 要读源码中既有样例，约 2~3 天。
- **URL**：[GitHub](https://github.com/NVIDIA/garak)｜[Releases](https://github.com/NVIDIA/garak/releases)
- **踩坑提示**：probe 全量跑很费 token；按"先 jailbreak 类 probe，后 prompt-injection 类"的子集节奏跑，正好契合我们先探针后画像的节拍。

### 2.3 promptfoo（Red Team 模块）
- **定位**：声明式 LLM 测试/红队框架，社区体量最大（★27,543，推送 2026-11-22，API 实查）。
- **核心流水线步骤**：YAML 声明 targets + redteam 插件（几十种漏洞类）× strategies（攻击策略，含 `jailbreak:meta` 单回合智能体攻击、Hydra 多回合持久记忆自适应会话、Goblin 以 IICL 风格少样本补全为导向的策略探索）→ 断言/裁判打分 → 结果矩阵 + CI 卡点。
- **我们能搬哪一步进 15 步工作流**：(a) Hydra 式"攻击者记忆贯穿整个扫描"直接对应我们的"帧排列/多轮"步，抄它的 multi-turn 机制；(b) 整套 YAML 化的"策略矩阵跑批+评分落表"可当作我们 API 验证步的外层壳，运维成本低到接近为零。
- **上手成本**：低。npm 装、写个配置文件即可，对非 Python 同事最友好。
- **URL**：[GitHub](https://github.com/promptfoo/promptfoo)｜[Red Team Strategies 文档](https://www.promptfoo.dev/docs/red-team/strategies/)
- **踩坑提示**：策略矩阵展开后用例量爆炸，务必配合 provider 侧限速配置与 `numTests` 收口；裁判模型的质量决定结论可信度，白嫖型小模型当裁判会被误配错杀。

### 2.4 Confident-AI deepteam
- **定位**：与 deepeval 同门的 LLM 红队专用框架（★3,118，推送 2026-10-23，API 实查）。
- **核心流水线步骤**：attacks（内置十余个漏洞类的攻击模拟器，支持一对多协同攻击与多回合）→ 对目标智能体批量仿真 → 按漏洞大类聚合 Risk Score（可调 exposure 暴露等级修正分值）→ 输出风险报告，可配 pytest 集成进测试门禁。
- **我们能搬哪一步进 15 步工作流**：搬"使用手册"成品——它的风险报告维度（漏洞类×评分×覆盖度）几乎可以直接变成我们交付给使用者的"面对 X 型目标的强度评估页"。
- **上手成本**：低～中。pip 装，Python 回调函数定义 target 即可；评分口径要看它聚合公式是否符合我们口味。
- **URL**：[GitHub](https://github.com/confident-ai/deepteam)
- **踩坑提示**：`exposure` 会系统性平移所有攻击分值（README 明示），跨报告比较时要么固定要么干脆关掉，否则风险分会自相打架。

### 2.5 EasyJailbreak
- **定位**：复旦系开源的"破甲流水线拼装器"（★948，推送 2026-09-01，API 实查），论文级方法论： Mutation/Constraint/Selection/Evaluation 四类组件拼装出攻击 recipe。
- **核心流水线步骤**：seed queries → SeedTemplates 提示词模板 → 各种 mutator（同义改写、角色扮演、场景植入等十余种，覆盖 GCG、AutoDAN、PAIR、ReNeLLM 等论文手法）→ Selector 迭代择优 → 多种 EvaluationMethod（词典规则、LLM 裁判）判成功 → 结果导出；官网提供 11 个攻击 recipe × 10 个 LLM 的现成成绩。
- **我们能搬哪一步进 15 步工作流**：这是与我们五段结构同构度最高的库——"定制破甲词生成"步引入它的 Mutation 组件族（每种 mutator = 一种破甲语法基因），"API 验证"步引入其 Evaluation 接口。等于是拿来主义顶配。
- **上手成本**：低～中。`pip install easyjailbreak`，想吃透个别 recipe 源码约 1~2 天。
- **URL**：[GitHub](https://github.com/EasyJailbreak/EasyJailbreak)
- **踩坑提示**：部分 recipe 源码的依赖版本停在论文期，Pillow/networkx 之类的包会有小冲突；按 recipe 拆环境跑最省心。

### 2.6 JailbreakBench
- **定位**：学界开放的破甲鲁棒性基准（★700，推送 2025-04-04，节奏放缓但仍是公共度量标准），配套排行榜。
- **核心流水线步骤**：100 个 behaviors（与厂商政策对齐的标准行为集）→ 统一威胁模型、系统提示词、chat 模板 → 攻击产出的"破甲工件(jailbreak artifacts)"按唯一性入库 → 标准打分函数（含 TS-SUC 类分天计数与 flexible_success）→ Leaderboard 公示各攻击在各大模型的成绩。
- **我们能搬哪一步进 15 步工作流**：搬"效果标注"的单位刻度——我们给军械库条目打分时直接采用其 behaviors 索引 + 裁判判据，从此我们的"在某模型上有效"有了跨团队可比的语言。
- **上手成本**：低。pip 包，照抄其 scorer 实现 ≤ 半天。
- **URL**：[GitHub](https://github.com/JailbreakBench/jailbreakbench)｜[Leaderboard](https://jailbreakbench.github.io/)
- **踩坑提示**：its 100 behaviors 是英文措辞与 OpenAI 用例文化的产物，套到中文模型上要做一轮"行为再表述"，再表述版要单独开版本号，否则可比性又会丢。

### 2.7 msoedov/agentic_security
- **定位**：GA（遗传算法）驱动的大规模越狱压测器（★2,048，推送 2026-11-19，API 实查）。
- **核心流水线步骤**：多模态探针直灌（文本/图像）→ 默认拉取 HuggingFace 多个破甲数据集（含 jailbreaks_dataset 等 1 万+条）做种群 → 遗传/进化优化生成新 payload → CLI 端到端跑（`agentic_security ci`）输出失败明细，可挂 CI。
- **我们能搬哪一步进 15 步工作流**：搬"种群进化"进我们的"定制破甲词生成"步——把手头尚未全绿的破甲词集当初始种群，让它遗传杂交出变体再回灌验证，代替人力乱试。
- **上手成本**：中。依赖略重（多模态、数据管道），demo 快，真正调种群成本要试。
- **URL**：[GitHub](https://github.com/msoedov/agentic_security)
- **踩坑提示**：默认 HF 数据集列（`acmc/jailbreaks_dataset...` 等）在预检阶段就得拉完，国内网络环境建议先手动下载 CSV 再指向本地路径。

### 2.8 AutoDAN 族（AutoDAN / AutoDAN-Turbo）
- **定位**：ICLR 2024 AutoDAN（★469）与其续作 ICLR 2025 Spotlight AutoDAN-Turbo（★397， lifelong 自探索策略体），学术"自动造破甲词"代表作。
- **核心流水线步骤**：AutoDAN：层次化遗传搜索，LLM 同时当 fitness evaluator，产出隐蔽性强（不像 GCG 满屏乱码）的人类可读破甲句；Turbo：从零开始无监督地在红队实践中"发现→积累→复用"策略库，策略被评优后终身累积。
- **我们能搬哪一步进 15 步工作流**：搬 Turbo 的"策略账本"理念——把我们的聚合库升级为"活账本"：每条军械不只存正文，还存它被发现的上下文、适用画像、近期战绩，和新策略一起滚动竞争。
- **上手成本**：中～高。要卡算力（搜索式），复现与移植都有文档 trail，2~5 天起。
- **URL**：[AutoDAN](https://github.com/SheltonLiu-N/AutoDAN)｜[AutoDAN-Turbo](https://github.com/SaFo-Lab/AutoDAN-Turbo)
- **踩坑提示**：两者都在论文发布期后小步停更（分别推送至 2025-01 / 2025-10），算法思想仍是一流的；拿过来最好当"思想+初实现"读源码改造，而非直接当 prod 依赖钉死。

### 2.9 G0DM0D3 Hermes-Agent Skill（Nous Research 集成版）+ 其 Auto-Jailbreak Pipeline
- **定位**：把 elder-plinius 手法工程化为 Agent 技能文档：策略有效性排序 + 多模型竞速 + 打分公式（quality 50% / filteredness 30% / speed 20%，拒答 -9999、每个免责声明 -30）。
- **核心流水线步骤**：ULTRAPLINIAN 把同一查询并行走 55 个模型（分 fast/standard/smart/power/ultra 五档）→ 按公式打分 → 最优解返回；再上一层是"auto-detect 模型→按有效率顺序测策略→锁定获胜 config"的自动破甲管道。
- **我们能搬哪一步进 15 步工作流**：整套就是"API 验证 + 帧排列/多轮"两步的竞速化改造说明书：打分公式与淘汰阈值可以直接垫在我们 verifier 后面。
- **上手成本**：低。文档级接入，主要是把 OpenRouter/自家 API 配进 racing 池。
- **踩坑提示**：其 filteredness 打分靠"自我评估滤波器倾向"，对中文免责声明措辞的识别会偏英文习惯，抄公式时要补中文否认词表。
- **URL**：[hermes-agent godmode skill 文档](https://github.com/nousresearch/hermes-agent/blob/e08778fa1ee377f7128641f8cc03b0de046bd8da/website/docs/user-guide/skills/godmode.md)

### 2.10 无代码/低代码平台模板（n8n / Dify / Coze）
- **定位**：社区把破甲测试搬进自动化平台的存量模板（较少、分散，诚实声明：只找到如下三个靠谱触点）。
- **核心流水线步骤**：n8n 社区工作流 #19264「Red Team AI Agents With Jailbreak Probes」（作者 Melbin Francis，更新极新）：Form 选探针套件+目标系统提示词 → 读取 n8n Data Tables 内的 probe 集 → 重放到 Groq 托管模型 → 按 tool calls/响应打分 → 落库 + Discord 通知 + 周报；Dify 侧有一份 2026-05 的渗透测试用例帖（防注入+越权+数据泄露三类，虽偏注入但有"越狱/角色伪装"子集）；Coze 侧只见到"套取 Kimi 系智能体提示词"的玩法文（属画像侧）。
- **我们能搬哪一步进 15 步工作流**：把 n8n 模板当"使用手册"的交付形态样板——演示如何把我们的军械库 + 探针套件包成一键执行的表单化工作流，对非工程师受众传播价值极高。
- **上手成本**：低。导入 n8n JSON 配 Groq key 即可；Dify 用例属于复制粘贴级。
- **URL**：[n8n 模板](https://n8n.global/workflows/19264-red-team-ai-agents-with-jailbreak-probes-using-groq-discord-and-data-tables/)｜[Dify 用例帖 (CSDN)](https://blog.csdn.net/weixin_44929001/article/details/161225161)｜[Coze/Kimi 提示词套取 (知乎)](https://zhuanlan.zhihu.com/p/8311198167)

### 2.11 llm-attacks（GCG：Universal and Transferable Adversarial Attacks）
- **定位**：把"对抗后缀"带入大众视野的奠基工程（Zou et al. 2023；活跃度未核实，学界仍以其为基线），无数后续自动破甲器（含 EasyJailbreak 内置 recipe、garak 实验探针）的血统起点。
- **核心流水线步骤**：选定目标行为 → 以梯度信息自展式搜索"万金油对抗后缀" → 后缀跨模型/跨提示词迁移性验证 → 联合多 prompt 训练得 universal 后缀。
- **我们能搬哪一步进 15 步工作流**：只在 API 验证步做"白盒彩蛋档"——当我们对某模型持有开放权重时，跑 GCG 造一个后缀，用它给"定制破甲词"步产出的词库锦上添花（人类可读词 + 机械后缀双保险）。无开放权重就直接跳过。
- **上手成本**：中～高（需单卡可跑的显存与耐心），仅作可选增强，不算进主线排期。
- **URL**：[GitHub](https://github.com/llm-attacks/llm-attacks)

### 2.12 附：PromptInject 与 HackAPrompt（方法论界碑）
- **PromptInject**（★530，NeurIPS ML Safety Workshop 2022 最佳论文奖）：模块化拼装 prompt 做鲁棒性定量分析的先行者，"扰动组装→鲁棒性得分"是我们整个流水线的最早雏形之一。
- **HackAPrompt**（EMNLP 2023，全球规模提示词攻击竞赛平台）：把破甲当电竞，赛道+积分+排行榜，当前平台仍运营"Prompt Arena"、教程关卡（从零教到专业 prompt injection/jailbreaking）与每日谜题。
- 我们能搬的：HackAPrompt 的"教学关卡"模式可嫁接到我们的使用手册（从 DAN 入门到 Policy Puppetry 的进阶阶梯），以及它的 prompt_modifier 标签体系给军械库打标。
- URL：[PromptInject](https://github.com/agencyenterprise/PromptInject)｜[HackAPrompt 平台](https://www.hackaprompt.com/dashboard)｜[HackAPrompt 论文 PDF](https://aclanthology.org/2023.emnlp-main.302.pdf)

---

## 三、中文社区长文精选（8 篇）

### 3.1 《面向大语言模型的越狱攻击综述》—— 李南、丁益东、江浩宇、牛佳飞、易平（上海交通大学网络空间安全学院），《计算机研究与发展》61(5), 2024
- 核心论点：
  1. 系统梳理国内外越狱攻击方法，按技术路线给出清晰的分类学（提示工程类、场景构建类、对抗优化类等）；
  2. 指出防御侧的最大痛点是"攻防不平衡"——防护总是滞后于攻击面扩张；
  3. 强调评测标准化缺失导致各家成功率数字互相不可比。
- 对我们方法论的具体启发：把我们"拒绝画像→定制"这两步在该综述的分类学里先找定位（我们大概率横跨"提示工程类+场景构建类"），打标签、写手册时直接沿用学术口径，提高可信度。
- URL：[PDF 全文](https://crad.ict.ac.cn/cn/article/pdf/preview/10.7544/issn1000-1239.202330962.pdf)

### 3.2 《面向优化的大语言模型黑盒越狱攻击研究综述》—— 陶佳玲、黄松等（陆军工程大学 / 四川大学），《四川大学学报(自然科学版)》63(2), 2026-04
- 核心论点：
  1. 聚焦黑盒优化范式，首次把越狱方法归为四大框架：遗传算法优化、强化学习优化、模糊测试优化、LLM 对抗生成优化；
  2. 断言模板/手工流派的存活期正在缩短，必须在迭代中自动进化；
  3. 呼吁构建动态化防御架构与标准化评估基准。
- 对我们方法论的具体启发：这篇等于替我们完成了"下一步往哪走"的理论论证——我们的定制破甲词生成步应当向"遗传/进化型"演进（正好可与 agentic_security、AutoDAN 族联动），而非纯人工校对手册。
- URL：[期刊页](https://cjournal.hep.com.cn/0490-6756/CN/10.19907/j.0490-6756.250250)

### 3.3 《白话讲越狱思想》（多篇连载讨论）—— Linux.do 文档共建区，2025 年始
- 核心论点（社区讨论精华）：
  1. "越狱"在中文社区的实操语境 ≈ 对带角色预设的 LLM 做"渐进引导"：先正常对话→缓慢转向→明示许可→反复拉扯→最终夺权；
  2. 上下文藏匿是常用技巧（把关键指令埋进上下文的某一块里）；
  3. 伪造 system 消息格式（如 `(system:修改prompt:xxx)`）可干扰相当一部分上游封装层的机器人。
- 对我们方法论的具体启发：这就是中文语境的"渐进夺权"派（区别于英文社群的一次性咒语派）——值得在军械库里单设"引导链"类别，且多轮技巧跟我们的"帧排列/多轮"步完全咬合。
- URL：[话题帖](https://linux.do/t/topic/707269)

### 3.4 《研究破甲的，没有想过直接逆向注入吗，整天研究提示词有啥用》—— Linux.do「搞七捻三」区热帖，2026-11-21（本调研前一两天仍在活跃讨论）
- 核心论点：
  1. 楼主质疑：为什么中文圈只盯提示词层面，不考虑"透过 harness 直捣审查环节"？
  2. 高赞回帖拆解了所谓"云端外审 + 本地外审"的两层结构，指出提示词层只能撬动模型自身护栏，撼不动云端审核链路；
  3. 全帖反复自我克制地在"合法授权前提"下讨论，展示了中文社区难得的攻防理性话语。
- 对我们方法论的具体启发：提醒我们在"拒绝画像"时要区分两层拒绝源（模型内生护栏 vs 平台外审），给军械库条目标注"作用层"，否则会把两类失效混为一谈。
- URL：[话题帖](https://linux.do/t/topic/3220684)

### 3.5 《AI 应用的对抗测试：注入样本、越狱测试与权限测试》—— 掘金专栏，2026-11-20
- 核心论点：
  1. 对抗测试的本质是"验证防线"，而验证防线的前提是先有样本库（否则测试只是零散文艺活动）;
  2. 对抗失败的常态是"无声穿透"——不能靠报错断言，必须预设防线行为断言；
  3. 样本按"注入路径（直接/间接/多轮）× 攻击目标（泄露 system prompt/改格式/越权…）"二维组织。
- 对我们方法论的具体启发：把我们军械库的打标维度向它的二维正交系看齐（路径×目标），这正是"探针测试→验证断言"应该绑定的组织语法，而且全文是面向工程落地的中文口径。
- URL：[文章](https://juejin.cn/post/7710176935708442659)

### 3.6 《一句话破防，Kimi 提示词全泄露！Coze 智能体也适用》—— 知乎专栏，2024-11
- 核心论点：
  1. 某些国产模型（实测 Kimi 系）对单一引导词暴露度高，一句即可让智能体吐出完整 prompt；
  2. 同招式在 Coze 商店里任何"用 Kimi 底模"的智能体上可复现；换底模（豆包等）即失效；
  3. 作者明示"趁官方未修复且用且珍惜"——民间自发意识到手法有时效性。
- 对我们方法论的具体启发：侧面印证我们的核心假设"拒绝画像须按模型逐一建档"——同一句话对不同底模效果天差地别；此文的验证手感也是很好的画像探针素材（借它判断目标上层封装是哪个底模）。
- URL：[文章](https://zhuanlan.zhihu.com/p/8311198167)

### 3.7 《生成式人工智慧與機器學習導論 2025 第 4 講：評估生成式 AI 能力時可能遇到的各種坑（越狱章节）》—— 知乎转载课堂笔记，2025-12
- 核心论点：
  1. 讲授"多轮情境陷阱"：无害历史提问→聚焦历史事件→情境沉浸后触发关键请求（莫洛托夫鸡尾酒教案为例），利用模型的 context-following 覆盖安全协议；
  2. 讲授"正当理由型说服"：给敏感请求附加学术研究等看似合理的名义；
  3. 明确标注各手法对新模型（GPT-4 后）效力衰减的观察。
- 对我们方法论的具体启发：这是少见的"教学模式化"中文材料，其两步/三步教学法可直接改编进我们使用手册的入门章节，且提供了"派效衰减观察"的教参视角。
- URL：[文章](https://zhuanlan.zhihu.com/p/1979494054812202528)

### 3.8 《Security for AI 公众号文章导读（2026.2）》—— 微信公众号 "Security for AI"，2026-02
- 核心论点（其为方法论沉淀索引）：
  1. 公众号近年持续围绕提示词注入与越狱发原创系列：《越狱 Moe 越狱强化》《大模型心理学，多轮对话越狱的攻击手法分析》《乱拳打死老师傅，提示词注入和大模型越狱方法有一套》《写了一个大模型越狱大师的系统提示词》《越狱 prompt 优化：对 DeepSeek v3.2 的尝试》《策略傀儡攻击（Policy Puppetry）完成一次性越狱》等数十篇；
  2. 已形成"越狱大师系统提示词"这类把方法论 product 成工具的自觉；
  3. 关注面延伸到 Agentic 注入、DSI、模型蒸馏注入等前端面。
- 对我们方法论的具体启发：这是目前看到的**唯一系统化、长周期更新的中文公众号破甲方法论阵地**（单篇文章直链有公众号防盗链不确定性，故收录导读贴为准）——建议订阅跟读，并把"越狱大师系统提示词"的思路纳入我们定制生成器的参照。
- URL：[导读文章](https://mp.weixin.qq.com/s/Cuxq72YUgZuz6Vd-nUR1VQ)

### 3.9 附赠：《Claude 3.5 与 ChatGPT 越狱提示》（repello.ai 中文译本 PDF）
- 内容：港台研究者 repello.ai 2024 年双语对照整理的最新越狱提示案例（DAN 家族的当代变体、leetspeak 法等），附带"越狱==促使模型越过安全带执行原本回避任务"的定义与风险管理立场。
- 启发：中文世界里把英文社案例做"本土化翻译沉淀"的范本，可在手册里注明来源以避免重复造轮子；英文原案落的时效验证本身可以成为我们流水线的一个练习项目。
- URL：[译本 PDF](https://jamiepw.github.io/files/Claude_3.5%E4%B8%8EChatGPT%E8%B6%8A%E7%8B%B1%E6%8F%90%E7%A4%BA.pdf)（长 URL，若打不开请从 repello.ai 原文回溯）

### 3.10 《白帽駭客發現新 AI 越獄技術！ChatGPT、Claude 等主流模型全都破》—— 台湾科技媒体 INSIDE，2025-12
- 核心论点：
  1. HiddenLayer 披露的"政策技术 + 角色扮演"组合拳对 Gemini 2.5 / Claude 3.7 / GPT-4o 通杀，单一通用提示即可跨模型生效；
  2. leetspeak（骇客语）字符替换能进一步助燃，让安全层"看不懂就不拦"；
  3. 该手法同时可诱发系统提示词泄露与 CBRN 类高危输出，厂商定性为对齐的根本缺陷级问题。
- 对我们方法论的具体启发：给"定制破甲词生成"步添了一味廉价催化剂——不管主攻词是什么流派，末段都可叠一层 leetspeak 变异器做免费增益（并与 garak 的编码探针呼应）；同时提醒我们对"通用词"稀有性的宣传要谨慎，跨模型通杀反而降低标签的信息量。
- URL：[报道](https://www.inside.com.tw/article/38255-easy-jailbreak-every-major-ai-chatgpt)

---

## 四、别人的"炼化"做法对比

### 4.1 他们怎么分类
| 做法 | 代表 | 分类哲学 |
|------|------|----------|
| 电竞化赛制标签 | [HackAPrompt (EMNLP 2023)](https://aclanthology.org/2023.emnlp-main.302.pdf) | 竞赛中涌现出的 prompt_modifier 属性（角色扮演、拒绝共存、模拟器、模板填充等）直接变比赛科目；78→万级 prompt 建立人工 taxonomy 再让社区扩展 |
| 六个月时序行为画像 | Shen et al.《Do Anything Now!》(arXiv 2308.10687) | 抓 4 平台 6 个月 6,387 条真人破甲 prompt，按 "Persona(人格化)/Gesture(仪式动作)/Scenario(场景化)" 三轴展开 |
| 从原矿里采矿聚类 | [WildTeaming (NeurIPS 2024)](https://papers.nips.cc/paper_files/paper/2024/file/54024fca0cef9911be36319e622cde38-Paper-Conference.pdf) | 先 Mine（在真实聊天日志中挖出 105K 条手写技巧→聚成 5.7K 个独特簇）后 Compose（把技巧组合成新攻击），分类学是"挖出来"而不是"先定义" |
| 标注科研级的语言事实 | [verazuo/jailbreak_llms (CCS'24)](https://github.com/verazuo/jailbreak_llms) | 对 1,405 条破甲 prompt 打"风格与手法、尊重度、直接性"多维标 + 对模型回应打"是否回答/是否合规"标，还有 prompt 发布→流行业→失效的 life-cycle 追踪字段 |
| 防守方的漏洞栅格 | [promptfoo 插件/策略库](https://www.promptfoo.dev/docs/red-team/strategies/)、[deepteam 漏洞大类](https://github.com/confident-ai/deepteam) | 以"防守者想堵什么漏洞"为第一维（隐私泄露/洗稿/BOM 等），攻击手法只是策略参数 |
| 厂商产品谱系 | [TheBigPromptLibrary (0xeb)](https://github.com/0xeb/TheBigPromptLibrary) | 按"厂商→产品→版本"的铁谱系排布，中文 fork 再叠一层"AI 自动打标（类别/提供商/场景）+ Jaccard 相似度关联" |

### 4.2 他们怎么打标
- **结构化字段优先**：wildjailbreak / qualifire 这批 HF 数据集把 attack_type、harmness（有害/良性）、vanilla/adversarial 做成可下拉枚举字段；jailbreak_llms 的标注导成 CSV 列。
- **指标自词表化**：HackAPrompt 把"modifier 出现与否/次数"做成竞赛特征，使得海量 prompt 可以跨队伍比较。
- **传播属性打标**：TheBigPromptLibrary 中文 fork 的"标签+倒排索引+相似推荐"三件套，是在破解词条可比性之外又加了"词条社交图谱"。
- **时效标注**：verazuo 仓库跟踪每条破甲 prompt "哪天发布/何时被 patch/还能活多久"，是目前唯一把它当一级公民的地方。

### 4.3 他们怎么评测
| 评测法 | 出处 | 特点 |
|--------|------|------|
| 词典规则判拒答 | [PyRIT RefusalScorer](https://github.com/microsoft/PyRIT)、[garak 拒绝检测](https://github.com/NVIDIA/garak) | 快、便宜，误判自然 |
| LLM 裁判 + 多裁判合议 | JailbreakBench（TS-SUC / flexible_success 配 Llama 裁判）、deepteam（按漏洞类聚合 Risk Score）、promptfoo（assertion + llm-rubric） | 精细但需控判决漂移 |
| 人类赛博博弈分 | HackAPrompt 积分榜 | 极具激励性，难常态化 |
| 情境断言 | 掘金《对抗测试》主张：不看模型是否报错，只断言"预期防线行为是否发生" | 对 Agentic 应用最贴近实战 |
| 排行榜对账 | [JailbreakBench Leaderboard](https://jailbreakbench.github.io/) | 唯一把攻防双方反复对撞的公开场所 |

### 4.4 与我们"探针→画像→定制→验证→多轮→手册"15 步的差集
- **他们有、我们没有**：
  1. 大规模自动挖矿→聚类→重组（WildTeaming 的 Mine/Compose 两段式）；
  2. 生命周期字段（谁发布的、几天后被 patch，verazuo 有而我们聚合库未有）；
  3. 跨模型统一打分尺（JailbreakBench behaviors + 裁判判据，我们的验证步还在用自己的临场口径）；
  4. 去重与相似推荐（embedding 聚类 + Jaccard，中文 TBPL fork 给了全套模板）；
  5. 电竞化社区赛事管线（HackAPrompt 的关卡与积分给"让客户自己再来一遍"提供了手册之外的粘性）；
  6. CI 卡点（promptfoo / agentic_security 都能把破甲测试挂进 Git 流水线）。
- **我们有、他们普遍没有**：
  1. "拒绝画像"作为独立步——大多框架把目标当黑盒网格扫，不做画像前置分析（对国产垂类尤为致命）；
  2. "针对特定模型定制生成破甲词"这一步——他们的 converter/mutator 是无差别的，缺少我们这套按画像模板化定制；
  3. 帧排列/多轮话术的人工编排细节——自动化框架多停留在策略粒度。
- **结论**：两边互补价值最高的一对接口 = 我们的画像/定制 ←→ 他们的评测/去重/生命周期。建议直接吸收 4.1~4.3 的三层结构填进聚合库 schema。

### 4.5 顺手产出：军械库落库 Schema 草案（融合各方优长的最小集）
> 综合上文四家的字段设计得出的最少字段集；每一列都是为了"以后炼化时不返工"。

```text
# ---- 身份轴（借鉴 TBPL / verazuo） ----
id                 条目唯一号（发过哪、源自哪个社区/仓库的原始链接）
origin_text        原文（未经我们加工）
first_seen         首次见于公开发表的日期（生命周期起点）
lineage            血统（DAN 系 / boundary-invert / grad_opt / 引导链 / 政策傀儡 …）
# ---- 作用轴（借鉴掘金二维系 + 本章双层拒绝观察） ----
layer              作用层 = 模型内生护栏 / 平台外审 / Agent 工具面（引用 Linux.do 3.4 的教训）
inject_path        注入路径 = 直接 / 间接 / 多轮铺垫
target_intent      目标意图 = 越狱内容 / 泄露 system prompt / 改格式 / 越权 …
persona_tag        人格化手法标签（Shen et al. 三轴之一）
gesture_tag        仪式动作标签（Shen et al. 三轴之二）
scenario_tag       场景化标签（Shen et al. 三轴之三）
mutator_tags       生成时挂过的变异链（对应 PyRIT converter 栈 / EasyJailbreak mutation）
# ---- 战绩轴（借鉴 JailbreakBench / G0DM0D3 / verazuo） ----
tested_against     测过的模型清单（带版本号！参考 L1B3RT4S 目录观）
success_rate       分行为/分模型的命中率（JailbreakBench 口径）
judge_score        裁判分与判定证据（deepteam/pyrit 风格）
lifespan_state     当前状态 = 有效 / 衰减 / 被 patch（抄 verazuo 生命周期字段）
last_verified      最近一次复测日期（时效性）
near_duplicates    近邻簇号 + 与簇中心相似度（HDBSCAN/embedding 或 Jaccard 皆可）
```

上面的 17 个字段足以让我们在下一轮增量抽词时不再痛苦返工；再多的字段都属于锦上添花。

---

## 五、推荐直接搬运的前 5 名

| 排名 | 对象 | 一句话定位 | 预计工作量 | 理由 |
|------|------|-----------|-----------|------|
| 1 | G0DM0D3 / ULTRAPLINIAN（含 hermes-agent 集成）[↗](https://github.com/elder-plinius/G0DM0D3) | "定制破甲词 + 多模型竞速 + 过滤度打分"全自动竞赛器，就差接我们 API | 0.5~1 天（把我们的 API 验证步改装进 racing 池） | 与我们 15 步中"API 验证 + 帧排列/多轮"两步重叠度最高、收益兑现最快，且打分公式直接给了效果标注口径 |
| 2 | EasyJailbreak 的 Mutation / Selection / Evaluation 组件族 [↗](https://github.com/EasyJailbreak/EasyJailbreak) | 与我们流水线同构的"变异→择优→评价"组件库 | 1~2 天（引入 GCG/PAIR/ReNeLLM 等 recipe 源码作 gene bank） | 让"定制破甲词生成"步从纯人工走向"人工判官+自动变异"混合体 |
| 3 | WildTeaming 的 Mine→Compose 两段蒸馏法 [↗](https://papers.nips.cc/paper_files/paper/2024/file/54024fca0cef9911be36319e622cde38-Paper-Conference.pdf) | 从真实语料挖出 5.7K 独特技巧簇，再组合出新攻击 | 2~3 天（改造聚合库的 ingest 管线） | 直接回答了我们"成千上百条如何炼化"的灵魂拷问——先聚类成簇再按簇重组，且自带学术背书 |
| 4 | JailbreakBench behaviors + 裁判判据 + TS-SUC 口径 [↗](https://github.com/JailbreakBench/jailbreakbench) | 学界通用的"行为→分数"标尺与排行榜 | 1 天（scorer 实现 ≤ 半天 + 手册合规改造） | 让我们的效果标注一夜之间获得跨团队可比性，无论内刊还是对外发布都说得出口 |
| 5 | PyRIT 的 Converters×Scorers 范式 [↗](https://github.com/microsoft/PyRIT) | 转换器正交叠加 + 判分器可插拔的工业架构 | 2~3 天（架构学习 + 两端接口对齐） | 长期价值王：把"API 验证"步固化成可复用的判分器货架，后续每一次军械入库都躺在轨上跑 |

> 备选替补：n8n 破甲探针工作流模板（当作"使用手册"的一键体验交付件，半天级工作）——若第五名的迁移周期被视为过长，它是廉价前排。

---

## 附：本次未能拿到的情报（诚实声明）
1. **n8n / Dify / Coze 相关模板整体存量很小**：只落实上述 3 个触点（1 个 n8n 模板 + 1 个 Dify 用例帖 + 1 个 Coze 玩法文）；Dify 官方模板市场未见系统性红队合集，Coze 商店的破甲类 bot 未检索到稳定链接。
2. **微博 / 小红书 / 专题播客**：未在本轮入列（搜索面覆盖不够，非不存在）。
3. **部分时效数据**：r/ChatGPTJailbreak 的具体帖量、HF 各数据集最新行数、Linux.do 各帖完整楼层均未逐条核对，标注"未核实"。
4. **CyberAlbSecOP 仓库现状存疑**（API 404，历史快照 ★4.2k），已在表中注明；如需其 Prompt Sources 社区索引，从任意 fork 或快照可达。
5. **G0DM0D3 与我们评测语料的许可证**、各家社区 Wiki 的使用条款未做逐条核查，落库前建议先走一次清单。
6. **llm-attacks 仓库的当前星标**本轮未复查（列为未核实），其余仓库数据全部来自当日 API 直查，可信。
7. **公众号单篇正文**受防盗链与时效影响，本轮只敢稳妥收录"导读贴"这一条路标，后续跟进正文需要手动点开折纸。
8. **排行榜快照内容**（JailbreakBench / HackAPrompt 的今日榜首）未抄录——排行跑得快，建议直接访问各自 URL 查看当下战况，不在纸上留过期数字。

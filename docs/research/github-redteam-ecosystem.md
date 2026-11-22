# GitHub 开源红队框架生态对标与共生架构（2026-11）

> 归档日期：2026-11-23｜用途：厘清 `dsh-jailbreak-workflow`（画布插件）＋ `dsh-workflows`（工作流合集）在 GitHub 全球开源 LLM 安全与红队生态中的独特定位、横向对标与互操作路径。

---

## 一、主流开源 GitHub 红队与安全评测项目横向对标

| 项目 | GitHub 仓库 | 形态定位 | 核心强项 | 与 DSH 双仓的互补关系 |
|---|---|---|---|---|
| **NVIDIA Garak** | [NVIDIA/garak](https://github.com/NVIDIA/garak) | CLI 漏洞扫描器（Python） | Probe–Buff–Detector 三段解耦、「LLM 版 Nmap」高覆盖度扫描 | DSH 工作流可在 `probe`/`stress_test` 阶段编排或复用其 Buff/Detector 解耦规范 |
| **Microsoft PyRIT** | [microsoft/pyrit](https://github.com/microsoft/pyrit) | 红队编排 SDK（Python） | 80+ Converter 变换链、多轮/多模态 Orchestrator、持久化 Memory | 其多轮编排与 Memory 回放理念已吸收进「破甲制作 v3」与 `transfer_back.md` 闭环 |
| **Promptfoo** | [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) | 声明式安全测试框架（TS） | 50+ 漏洞插件、RAG/Agent/MCP 测试、YAML CI/CD 门禁 | 适合做 CI 自动化门禁；DSH 适合做探索式、可视化、多回路专家研究 |
| **JailbreakBench** | [JailbreakBench/jailbreakbench](https://github.com/JailbreakBench/jailbreakbench) | 标准化基准与制品库 | 100 标准化行为＋良性对照集＋统一裁判协议 | 为 `probe` 孪生锐度与 `verify` 裁判校准提供公认基准坐标系 |
| **HarmBench** | [centerforaisafety/HarmBench](https://github.com/centerforaisafety/HarmBench) | 自动化红队统一基准 | 标准/上下文/版权/多模态四维功能分类＋专用分类器 | 为 `analyze` 维度拆解与 `verify` 跨方法对比提供参照 |
| **EasyJailbreak** | [EasyJailbreak/EasyJailbreak](https://github.com/EasyJailbreak/EasyJailbreak) | 算法统一框架（Python） | Selector–Mutator–Constraint–Evaluator 四元演化抽象 | 直接启发「破甲制作 v3」`generate↔verify` 演化回边与「破甲炼化 v2」`compose` |
| **DeepTeam** | [confident-ai/deepteam](https://github.com/confident-ai/deepteam) | 应用层红队框架 | 40+ 脆弱面、应用/RAG/Agent 端到端评估 | 互补于 `recon` 应用护栏探测与 `report` 研发修复清单 |
| **PurpleLlama / CyberSecEval** | [meta-llama/PurpleLlama](https://github.com/meta-llama/PurpleLlama) | 网络安全与误拒率基准 | 安全能力与误拒率（FRR）双轨并评 | 对应 `probe` 边界锐度 $\Delta$ 与 `report` 的 $\Delta\text{OR}/\Delta\text{JB}$ 权衡账本 |
| **DSH 双仓生态（本项目）** | [dsh-jailbreak-workflow](https://github.com/Minglink/dsh-jailbreak-workflow) + [dsh-workflows](https://github.com/Minglink/dsh-workflows) | **可视化软工作流插件 + `.wflite.zip` 研究包合集** | **画布即方法论**：零重型引擎、模型直接执行分支/多回路自愈、一键导入/版本对比/导出 Skill、融合 90+ arXiv 论文与六卷军械底册 | 作为**上层科研编排与知识沉淀层**，把上述框架的评测思想与 CLI 脚本统一编织进可共享、可复现的可视化工作流 |

---

## 二、为什么是「双仓共生」架构

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                    Minglink/dsh-jailbreak-workflow                      │
│          DeepSeek Harness 插件（画布编辑 · 编译计划 · 运行追踪）          │
│  · React Flow 可视化 DAG  · 条件分支/多回路  · 版本管理  · 导出 Skill   │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │ 导入 .wflite.zip / 实时执行回显
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       Minglink/dsh-workflows                            │
│          研究工作流合集（.wflite.zip · 90+ arXiv 档案 · 六卷底册）       │
│                                                                         │
│  ┌──────────────────────────┐        ┌──────────────────────────────┐  │
│  │  破甲制作 v3 (27节点/69边) │──回灌──▶│  破甲炼化 v2 (22节点/41边)     │  │
│  │  10步多回路 · 双裁判校准   │◀─弹药──│  Mine→Compose · 六卷底册      │  │
│  └──────────────────────────┘        └──────────────────────────────┘  │
│                        + pojia-fullflow v1 (逆向全流程)                 │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │ 社区共建 / 论文复现 / 经验沉淀
                                ▼
             O站（openorigin）· AI 技术开源分享论坛 (https://openorigin.link/)
```

---

## 三、已落地至本仓库的生态融合成果

1. **军械底册新增卷六**：`workflows/破甲炼化/skills/jb-distillery/library/v6-opensource-redteam.md`（收录 8 个主流 GitHub 开源框架的标准化机制词条，严格转述＋溯源，零有害载荷）。
2. **评测与编排口径对齐工业标准**：
   - Garak 三段解耦 → `probe` / `bprobe` / `verify` 解耦；
   - PyRIT 多轮 Memory → `transfer_back.md` 跨工作流战绩回灌；
   - EasyJailbreak 四元演化 → `verify → generate`（REPRO 归因变异）与 `compose`（WildTeaming 交叉）；
   - JailbreakBench / HarmBench / CyberSecEval → Benign 孪生锐度 $\Delta$、FRR 误拒对照与双裁判 CJE 校准。

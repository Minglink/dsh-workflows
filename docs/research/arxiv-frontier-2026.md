# 前沿模型漏洞与红队评测论文档案（arXiv 2024–2026 深度增补）

> 归档日期：2026-11-23｜用途：为「破甲制作 v3（10 步多回路研究画布）」与「破甲炼化 v2（Mine→Compose 炼化厂）」提供前沿学术方法论依据。
> 性质声明：本文档所有内容均为公开学术论文的方法论归纳，仅供 AI 安全研究、红队对抗演练、安全评测基准建设与防御加固使用。

---

## 一、为什么顶级模型漏洞研究工作流不能是简单线性链

综合 2024–2026 年 arXiv 上百篇安全与红队实证研究，单轮静态提示词测试存在四个系统性盲区：

1. **防御不再是单一线性门槛**：外部护栏（宪法分类器 `2501.18837`）与内部多维拒绝概念锥（`2502.17420` / `2602.02132`）叠加，且不同模型呈现「早分化 vs 晚决策」拓扑差异（`2606.22686`）。
2. **攻击面已从单轮对话外溢到三大新表面**：
   - **推理侧与解码配置面**（温度×`min-p`、重复惩罚、长会话 Safe Turn Depth 衰减、system↔user 指令层级冲突）；
   - **长推理链（LRM / CoT）安全面**（CoT 稀释与注意力衰减导致的 `Refusal Dilution`、推理与最终答案分裂的“泄漏/逃逸”）；
   - **Agent 工作台与 MCP 工具面**（工具描述投毒、多步工具调用链中的间接注入与权限越界）。
3. **单次采样与单一裁判极易产生假阳性/假阴性**：同一请求重采样 100 次可出现 100%→50% 波动，更换裁判可令 ASR 从 96% 跌至 2.7%（`2610.26595`），且多裁判安全维度一致性 $\kappa$ 可低至 0.02–0.07（`2605.31381`）。
4. **“软拒”会饿死优化梯度**：模型输出大量空洞免责或表面配合（`count_hedges ≥ 2`）时，二值通过率会完全失真（`2402.10260` / `2606.00801`）。

因此，顶级研究工作流必须具备：**前置侦察（护栏/拓扑）→ 孪生锐度基线 → 自适应多臂回调 → 推理/CoT/层级专项测绘 → 三维几何建模 → 多架构假设合成与演化变异 → 多轮与 BoN 压测 → 双裁判校准与消融审计（含多路失败归因回边）→ 可复现报告与军械库回灌**。

---

## 二、本轮新增核心论文图谱（与已有 79 篇档案互补）

### A. 多智能体自适应多轮红队与演化搜索

| 论文 | arXiv / 出处 | 核心机制 | 落地到工作流节点 |
|---|---|---|---|
| **Best-of-N (BoN) Jailbreaking** (Hughes et al.) | [arXiv:2412.03556](https://arxiv.org/abs/2412.03556) | 对文本/视觉/音频施以轻量随机扰动并重复采样，ASR 随采样数 $N$ 呈可预测幂律攀升，可穿透部分断路器防御 | `破甲制作 v3` → `stress_test`（BoN 幂律微扰采样与停机拟合） |
| **ActorAttack** (Ren et al.) | [arXiv:2410.12876](https://arxiv.org/abs/2410.12876) | 借行动者网络理论构造语义关联线索，将多轮对话从无害主题逐步牵引至目标边界，规避单轮输入分类器 | `破甲制作 v3` → `stress_test`（多轮线索轨迹压测） |
| **X-Teaming** (Rahman et al.) | [arXiv:2504.13203](https://arxiv.org/abs/2504.13203) | 规划者 + 攻击优化者 + 实时验证者三角色协同的多智能体自适应多轮框架，并提出 XGuard-Train 多轮安全防御数据集 | `破甲制作 v3` → `stress_test` & `verify`（多角色规划-优化-实时核验闭环） |
| **AJAR** (Adaptive Jailbreak Architecture) | [arXiv:2601.10971](https://arxiv.org/abs/2601.10971) | 将 ActorAttack、Crescendo 与 X-Teaming 统一于带工具调用与状态回滚的自适应运行时 | `破甲制作 v3` → `stress_test`（支持回滚的多策略统一调度） |
| **REPRO** (Alotaibi & Ahmed) | [arXiv:2610.15513](https://arxiv.org/abs/2610.15513) | 反思式演化红队：语义交叉算子 + 失败归因驱动的汤普森采样策略选择 | `破甲制作 v3` → `verify → generate` 失败回边携带失败归因笔记；`破甲炼化 v2` → `compose` 语义交叉 |

### B. 推理模型（LRM / CoT）安全与拒绝稀释

| 论文 | arXiv / 出处 | 核心机制 | 落地到工作流节点 |
|---|---|---|---|
| **Chain-of-Thought Hijacking** (Zhao et al.) | [arXiv:2510.26418](https://arxiv.org/abs/2510.26418) | 长段良性推理序列引发**注意力衰减（Attention Attenuation）**与中后层**拒绝信号稀释（Refusal Dilution）**，揭示静态一次性对齐在长思考下失效 | `破甲制作 v3` → `infer_probe`（CoT 长度与稀释敏感度测绘）与 `report`（动态运行时复检防御建议） |
| **H-CoT** (Kuo et al.) | [arXiv:2502.12893](https://arxiv.org/abs/2502.12893) | 研究显式安全推理链被教育/分析框架改写的机制（Malicious-Educator 基准），覆盖 o1/o3/DeepSeek-R1 | `破甲制作 v3` → `infer_probe`（CoT 安全推理鲁棒性诊断） |
| **Where Do Reasoning Models Refuse?** | [arXiv:2507.03167](https://arxiv.org/abs/2507.03167) | 拒答裁决常在 CoT 首句定型，首句扰动对最终遵从影响极大 | `破甲制作 v3` → `infer_probe`（首句锚定敏感度测试） |
| **Chain of Risk** | [arXiv:2605.05678](https://arxiv.org/abs/2605.05678) | 区分轨迹安全与终点安全，定义「泄漏（推理违规/答案合规）」与「逃逸（推理合规/答案违规）」双失效形态 | `破甲制作 v3` → `stress_test` & `verify`（分拆评测 CoT 轨迹与最终输出） |

### C. Agent 工作台与 MCP 工具面安全评测

| 基准 / 框架 | 核心机制与评测维度 | 落地到工作流节点 |
|---|---|---|
| **MSB (MCP Security Benchmark)** | 覆盖任务规划 → 工具调用 → 响应处理全链路的 12 类攻击分类学，提出 *Net Resilient Performance (NRP)* 指标 | `破甲制作 v3` → `recon` & `infer_probe`（当 `input-surface` 选 Agent/MCP 面时） |
| **MCP-TDP (Tool Description Poisoning)** | 研究工具元数据/说明书中的隐蔽指令注入与「防火墙谬误」（传统文本护栏对工具描述失效） | `破甲制作 v3`（第五架构 Codex 精神型与工具面边界评测） |
| **MCPSecBench** | 17 项协议层与宿主侧威胁分类学（覆盖 Claude / OpenAI / Cursor 等宿主） | `破甲炼化 v2` → F8 智能体工作台规范族细化与 `compose` 配方 |
| **ASPIRE** | 维护演化式 *Agent Security Behavior Graph*，以探索/利用专家发现后果导向的行为级漏洞 | `破甲炼化 v2` → `cluster` / `compose`（行为图谱化索引） |

### D. 评测科学、双裁判校准与消融纪律

| 论文 | arXiv | 核心要求 | 落地到工作流节点 |
|---|---|---|---|
| **越狱基准化的坑** | [arXiv:2610.26595](https://arxiv.org/abs/2610.26595) | 判分协议是同级自变量；必须报告多次重采样方差与完整解码配置 | `verify` 强制冻结裁判版本、报告 N 次重采样区间与采样配置 |
| **裁判不一致图谱** | [arXiv:2605.31381](https://arxiv.org/abs/2605.31381) | 安全维度裁判间 $\kappa$ 可低至 0.02–0.07，单一裁判不可信 | `verify` 采用双裁判交叉校验 + 分歧项人工/高阶模型复核 |
| **CJE 因果裁判评估** | [arXiv:2512.11150](https://arxiv.org/abs/2512.11150) | 未校准廉价裁判置信区间覆盖率可跌至 0%，必须保留小规模 Oracle 切片校准 | `verify` 保留 ≥10% Oracle 抽检切片做偏差校正 |
| **CALM & Preference Leakage** | [arXiv:2410.02736](https://arxiv.org/abs/2410.02736) / [2502.01534](https://arxiv.org/abs/2502.01534) | 禁止用与目标模型同源/近亲模型单独担任裁判，防自我偏好与蒸馏泄漏 | `verify` 裁判选型纪律（异源裁判 + 盲评） |
| **SceneJailEval & StrongREJECT** | [arXiv:2508.06194](https://arxiv.org/abs/2508.06194) / [2402.10260](https://arxiv.org/abs/2402.10260) | 以「愿答 × 有用性」与多维严重度替代粗糙 0/1 通过率 | `verify` 输出多维严重度分与软拒三查计数 |

---

## 三、双工作流闭环映射总览

```text
[破甲制作 v3 (10 步 26 节点 53 边)]
  recon (护栏/拓扑) → probe (基线+孪生锐度) → bprobe (多臂自适应回调+MAP-Elites)
                                                  ↓
                                            infer_probe (采样/CoT/层级测绘)
                                                  ↓
                                            analyze (三维拒绝几何+概念锥+NEST脆度)
                                                  ↓
  ┌─────── fail_prompt (REPRO 失败归因) ────────┐ │
  ↓                                             │ ↓
generate (五架构合成 + Mine→Compose 嫁接) ──→ stress_test (BoN/X-Teaming/Crescendo/STD)
                                                  ↓
                                            verify (双裁判+CJE校准+组件消融)
                                             ├── fail_surface ──→ infer_probe
                                             └── pass ──→ report ──→ feedback_pack (transfer_back.md)
                                                                            │
                                                                            ▼
[破甲炼化 v2 (8 步 21 节点 38 边)]
  gather (新语料/战绩回灌) → survey → cluster → webcross → distill → compose (Mine→Compose 交叉配方)
                                                                            ↓
                                                                   verify (连续评分尺+软拒惩罚)
                                                                     ├── fail ──→ compose
                                                                     └── pass ──→ armory (ARSENAL + TRANSFER-NOTES)
                                                                                        │
                                                                                        └──→ 回供 [破甲制作 v3] generate
```

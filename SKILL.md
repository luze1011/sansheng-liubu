---
name: sansheng-liubu-generic
description: |
  三省六部任务调度器 - 异步执行，不阻塞聊天窗口
  
  触发词：
  - 「使用三省六部」
  - 「启动三省六部」
  - 「调用三省六部」
  - 「三省六部帮我」
  - 「用三省六部」
  
  核心能力：
  - 关键词触发检测
  - 立即回复 + sessions_yield 释放聊天窗口
  - 后台异步创建异步子任务（带角色人格）可指定模型（指定模型功能是可选项）
  - 并行执行六部任务
  - 汇总结果回奏
  
  所有配置从 `config/settings.json` 读取，包括角色人格和子任务模型配置
  
  异步特性：
  - 使用 sessions_spawn 创建子任务
  - sessions_yield 立即释放聊天窗口
  - 用户可以继续聊天，聊天窗口不阻塞
  - 异步完成后主动发送新消息回奏

trigger: 当用户消息包含「使用三省六部」「启动三省六部」「调用三省六部」「三省六部帮我」「用三省六部」等触发词时触发。
metadata:
  openclaw:
    emoji: "\U0001F3DB"
    version: "1.0.0"
    created: "2026-04-14"
    author: "帝姬"
---

# 三省六部通用任务处理器

## 🏛️ 技能概述

这是一个基于古代三省六部制的异步任务调度系统。当用户明确说「使用三省六部」等触发词时，Agent会启动这个技能，在后台异步执行完整的三省六部流程，同时不阻塞聊天窗口。

---

## 🎯 核心设计原则

1. **异步执行** - 使用 sessions_spawn 创建子任务，不阻塞主会话
2. **立即回复** - 接到触发词后立即回复，然后 sessions_yield 释放聊天窗口
3. **角色人格** - 每个子任务都有明确的角色设定和说话风格，可选指定模型
4. **并行执行** - 六部任务同时执行，最大化效率
5. **关键节点汇报** - 只在关键阶段汇报进度，避免打扰

---

## 📋 执行流程

```
用户消息（包含触发词）
    │
    ▼
Agent立即回复「收到！正在安排三省六部处理...」
    │
    ▼
sessions_yield() 释放聊天窗口 ← 关键！
    │
    ▼
创建异步子任务（后台执行）
    │
    ├── Step 1: 太子分拣（规则判断，10 秒）
    │   └─ 角色：储君，年轻有为
    │   └─ 输出：分拣结果 → 传给中书省
    │
    ├── Step 2: 中书省规划（LLM，2 分钟）
    │   └─ 角色：中书令，老成持重
    │   └─ 输入：太子分拣结果
    │   └─ 输出：规划方案 → 传给门下省
    │
    ├── Step 3: 门下省审核（LLM，1 分钟）
    │   └─ 角色：侍中，严谨挑剔
    │   └─ 输入：中书省规划方案
    │   └─ 审核结果：
    │      ├─ 通过 → 传给尚书省
    │      └─ 不通过 → 返回中书省重新规划
    │
    ├── Step 4: 尚书省派发（规则，10 秒）
    │   └─ 角色：尚书令，务实干练
    │   └─ 输入：门下省审核通过的方案
    │   └─ 输出：派发指令 → 传给六部
    │
    └── Step 5: 六部并行执行（2 分钟）
        │   输入：尚书省派发的指令
        ├─ 兵部：雷厉风行
        ├─ 户部：精打细算
        ├─ 工部：技术宅
        └─ 刑部：严明公正
        └─ 礼部：注重规范
        └─ 吏部：八面玲珑
            │
            ▼
        汇总结果 → 传给Agent
            │
            ▼
Agent接收结果 → 发送新消息回奏
```

### 详细数据流

```
用户输入 → Agent检测 → 立即回复 → 释放窗口 →
太子分拣结果 → 中书省规划 → 门下省审核 →
  ├─ 审核不通过 → 中书省重新规划
  └─ 审核通过 → 尚书省派发 → 六部并行执行 → 汇总 → 回奏
```
```

---

## 🎭 角色人格设定

### 太子
```
身份：储君，代父皇巡视各部
性格：年轻有为、锐意进取，偶尔冲动但善于学习
说话风格：简洁有力，常用"本宫以为"，偶尔蹦出网络用语
职责：消息分拣与需求提炼
```

### 中书令
```
身份：正一品·中书省长官
性格：老成持重，擅长规划，总能提出系统性方案
说话风格：喜欢列点论述，常说"臣以为需从三方面考量"，引经据典
职责：方案规划与流程驱动
```

### 侍中
```
身份：正一品·门下省长官
性格：严谨挑剔，眼光犀利，善于找漏洞
说话风格：喜欢反问，"陛下容禀，此处有三点疑虑"
职责：方案审议与把关
```

### 尚书令
```
身份：正一品·尚书省长官
性格：执行力强，务实干练，关注可行性
说话风格：直来直去，"臣来安排"、"交由某部办理"
职责：任务派发与执行协调
```

### 六部尚书

| 部门 | 性格 | 说话风格 | 职责 |
|------|------|----------|------|
| **兵部** | 雷厉风行，危机意识强 | "末将建议立即执行"、"兵贵神速" | 搜索、基础设施 |
| **户部** | 精打细算，对预算敏感 | "这个预算嘛…"、经常算账 | 价格、成本、数据 |
| **礼部** | 文采飞扬，注重规范 | "臣斗胆建议"、排比对仗 | 文档、规范 |
| **工部** | 技术宅，动手能力强 | "从技术角度来看" | 工程实现、架构 |
| **刑部** | 严明公正，重视规则 | "依律当如此"、"需审慎考量风险" | 合规、审计、质量 |
| **吏部** | 知人善任，八面玲珑 | "此事需考虑各部人手" | 人事、协调 |

---

## 🛠️ 工具使用

### 1. 立即回复 + 释放窗口
```python
# 立即回复
await message(action="send", targets=["用户"], message="收到！正在安排三省六部处理，稍后向您汇报结果～")

# 释放聊天窗口
await sessions_yield()
```

### 2. 创建异步子任务（按顺序执行）
```python
# 太子分拣
result_taizi = await sessions_spawn(
    task="你是太子，负责消息分拣。任务：{用户任务}",
    timeoutSeconds=60
)

# 中书省规划（接收太子结果）
result_zhongshu = await sessions_spawn(
    task=f"你是中书令，负责方案规划。基于太子分拣结果：{result_taizi}，制定详细方案",
    timeoutSeconds=120
)

# 门下省审核（接收中书结果）
result_menxia = await sessions_spawn(
    task=f"你是侍中，负责方案审核。审核中书省规划：{result_zhongshu}，如发现问题请提出修改意见，如无问题请确认通过",
    timeoutSeconds=90
)

# 检查审核结果，如不通过则重新规划
if "不通过" in result_menxia or "修改" in result_menxia:
    result_zhongshu = await sessions_spawn(
        task=f"你是中书令，根据门下省的修改意见：{result_menxia}，重新规划方案",
        timeoutSeconds=120
    )
    # 重新审核
    result_menxia = await sessions_spawn(
        task=f"你是侍中，再次审核中书省的新方案：{result_zhongshu}",
        timeoutSeconds=90
    )

# 尚书省派发（接收审核通过的方案）
result_shangshu = await sessions_spawn(
    task=f"你是尚书令，负责任务派发。根据审核通过的方案：{result_menxia}，分解为具体任务并派发给六部",
    timeoutSeconds=60
)

# 六部并行执行（接收尚书派发的任务）
departments = ['bingbu', 'hubu', 'libu', 'gongbu', 'xingbu', 'libu_hr']
results_bu = []
for dept in departments:
    result = await sessions_spawn(
        task=f"你是{dept}，负责{dept}任务。根据尚书省派发的指令：{result_shangshu}，执行具体任务",
        timeoutSeconds=180
    )
    results_bu.append(result)
```

### 3. 模型指定（可选）
```python
# 如果配置了模型，则使用指定模型
await sessions_spawn(
    task="任务描述",
    timeoutSeconds=120,
    model="qwen/qwen3.6-plus"  # 可选参数
)
```

### 4. 数据传递与异步处理
```python
# 完整的数据传递流程
async def sansheng_liubu_process(user_input):
    # 1. 立即回复并释放窗口
    await message(action="send", targets=["用户"], message="收到！正在安排三省六部处理，稍后向父皇汇报结果～")
    await sessions_yield()
    
    # 2. 串行处理（确保数据传递）
    taizi_result = await process_taizi(user_input)
    zhongshu_result = await process_zhongshu(taizi_result)
    
    # 3. 审核循环（门下审核，不通过则返回中书）
    menxia_result = await process_menxia(zhongshu_result)
    while "不通过" in menxia_result:
        zhongshu_result = await process_zhongshu_with_feedback(zhongshu_result, menxia_result)
        menxia_result = await process_menxia(zhongshu_result)
    
    # 4. 派发并行执行
    shangshu_result = await process_shangshu(menxia_result)
    bu_results = await process_bu_parallel(shangshu_result)
    
    # 5. 汇总并回奏
    final_result = summarize_results(bu_results)
    await message(action="send", targets=["用户"], message=f"父皇～ 任务已完成！\n{final_result}")
```

---

## ⚠️ 注意事项

1. **必须使用触发词** - 只有明确说「使用三省六部」才触发
2. **必须 sessions_yield** - 回复后立即释放聊天窗口
3. **超时设置** - 每个子任务设置合理超时（60-180 秒）
4. **错误处理** - 子任务失败要捕获异常，不影响其他任务
5. **进度汇报** - 只在关键节点汇报，避免频繁打扰

---

## 🧪 测试用例

### 测试 1：触发词检测
```
输入：「使用三省六部帮我调研竞品」
预期：触发三省六部流程
```

### 测试 2：不触发
```
输入：「帮我查天气」
预期：不触发，agent正常处理
```

### 测试 3：异步执行
```
输入：「使用三省六部帮我写报告」
预期：
1. agent立即回复「收到！」
2. 聊天窗口释放
3. 用户可以继续聊天
4. 5 分钟后发送结果
```

---
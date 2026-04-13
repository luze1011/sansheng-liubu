# 三省六部任务调度器

Sansheng Liubu (Three Departments and Six Ministries) Task Dispatcher

一个基于古代三省六部制度的通用任务调度框架，适用于任何 Agent 系统。

## 📖 简介

这是一个多智能体协作分析框架，灵感来自古代中国的三省六部制度。保留了传统的部门架构，但将其现代化为通用的任务调度系统。

### 核心特性

- ✅ **异步执行** - 使用 sessions_spawn，不阻塞聊天窗口
- ✅ **多角色协作** - 中书省、门下省、尚书省、六部
- ✅ **并行处理** - 六部同时执行，效率提升
- ✅ **配置驱动** - 所有参数从配置文件读取
- ✅ **通用设计** - 适配任何 Agent 系统

## 🏛️ 架构

```
用户指令
    │
    ▼
立即回复 + sessions_yield 释放窗口
    │
    ▼
异步子任务
    │
    ├── 中书省 → 方案规划
    ├── 门下省 → 审核把关
    ├── 尚书省 → 任务派发
    │
    └── 六部（并行）
        ├── 兵部：搜索/基础设施
        ├── 户部：成本/数据
        ├── 礼部：文档/规范
        ├── 工部：技术/架构
        └── 刑部：合规/审计
            │
            ▼
        结果汇总 → 发送给用户
```

## 📦 安装

```bash
# 克隆仓库
git clone https://github.com/your-repo/sansheng-liubu.git

# 进入目录
cd sansheng-liubu
```

## 🚀 使用方法

### 命令行

```bash
# 基本用法
python scripts/main.py --task "分析竞品"

# 交互模式
python scripts/main.py --interactive

# 列出所有部门
python scripts/main.py --list-departments

# 串行执行
python scripts/main.py --task "任务" --sequential

# 自定义配置
python scripts/main.py --task "任务" --config my_config.json
```

### 作为 OpenClaw 技能使用

将目录复制到 OpenClaw skills 目录：

```bash
cp -r sansheng-liubu ~/.openclaw/skills/
```

触发方式：
```
使用三省六部分析这个
启动三省六部来处理任务
调用三省六部
```

## ⚙️ 配置说明

所有配置从 `config/settings.json` 读取。

### 主要配置项

| 配置项 | 说明 |
|--------|------|
| `trigger_words` | 触发词列表 |
| `roles.*.title` | 部门名称 |
| `roles.*.duty` | 职责描述 |
| `roles.*.timeout` | 超时时间 |
| `roles.*.enabled` | 是否启用 |
| `roles.*.order` | 执行顺序 |

### 自定义角色

```json
{
  "roles": {
    "my_dept": {
      "title": "我的部门",
      "alias": "部长",
      "identity": "部门负责人",
      "personality": "专业稳重",
      "style": "从专业角度分析",
      "duty": "自定义职责",
      "timeout": 120,
      "enabled": true,
      "order": 1
    }
  }
}
```

## 📁 目录结构

```
sansheng-liubu/
├── SKILL.md              # 技能描述
├── README.md             # 本文件
├── config/
│   └── settings.json    # 配置文件
└── scripts/
    └── main.py           # 主程序
```

## 🤝 贡献

欢迎提交 Pull Request！

1. Fork 本仓库
2. 创建特性分支
3. 提交更改
4. 打开 Pull Request

## 📝 许可证

MIT License

---

**版本**: 2.0.0  
**作者**: Azer阿泽  
**创建日期**: 2026-04-13
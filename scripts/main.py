#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

"""
三省六部任务调度器 - 通用版
Sansheng Liubu (Three Departments and Six Ministries) Task Dispatcher

这是一个基于古代三省六部制度的通用任务调度框架。
支持异步执行，不阻塞聊天窗口。

用法：
    python main.py --task "任务描述"
    python main.py --interactive
    python main.py --config custom.json
    python main.py --list-departments
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

# 获取配置目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'config')
DEFAULT_CONFIG = os.path.join(CONFIG_DIR, 'settings.json')


def load_config(config_path: str = None) -> Dict:
    """从配置文件加载配置"""
    if config_path is None:
        config_path = DEFAULT_CONFIG
    
    if not os.path.exists(config_path):
        print(f"⚠️ 配置文件不存在: {config_path}，使用默认配置")
        return get_default_config()
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_default_config() -> Dict:
    """获取默认配置（内嵌）"""
    return {
        "trigger_words": {
            "zh": ["使用三省六部", "启动三省六部", "调用三省六部"],
            "en": ["use sansheng liubu"]
        },
        "roles": {
            "zhongshu": {
                "title": "中书省", "alias": "中书令",
                "identity": "正一品·中书省长官",
                "personality": "老成持重，擅长规划",
                "style": "需从三方面考量",
                "duty": "方案规划", "timeout": 120, "enabled": True, "order": 1
            },
            "mensxia": {
                "title": "门下省", "alias": "侍中",
                "identity": "正一品·门下省长官",
                "personality": "严谨挑剔",
                "style": "此处有三点疑虑",
                "duty": "方案审核", "timeout": 90, "enabled": True, "order": 2
            },
            "shangshu": {
                "title": "尚书省", "alias": "尚书令",
                "identity": "正一品·尚书省长官",
                "personality": "执行力强",
                "style": "交由某部办理",
                "duty": "任务派发", "timeout": 60, "enabled": True, "order": 3
            }
        },
        "messages": {
            "triggered": "收到！正在启动三省六部处理...",
            "completed": "任务已完成！"
        }
    }


def is_triggered(message: str, config: Dict) -> bool:
    """检测是否触发了三省六部（从配置读取）"""
    trigger_words = config.get('trigger_words', {})
    all_words = trigger_words.get('zh', []) + trigger_words.get('en', [])
    message_lower = message.lower()
    return any(word.lower() in message_lower for word in all_words)


def build_role_prompt(role_key: str, task: str, context: str, config: Dict) -> str:
    """构建角色 Prompt（从配置读取）"""
    roles = config.get('roles', {})
    role_info = roles.get(role_key, {})
    
    prompt = f"""你是{role_info.get('title', role_key)}（{role_info.get('alias', '')}），负责{role_info.get('duty', '任务')}。

【角色设定】
- 身份：{role_info.get('identity', '官员')}
- 性格：{role_info.get('personality', '专业')}
- 说话风格：{role_info.get('style', '陈述')}

【当前任务】
{task}

"""
    
    if context:
        prompt += f"""【上下文】
{context}

"""
    
    prompt += """请基于你的角色定位，执行你的职责。
请用清晰的结构化方式呈现你的工作结果。

开始执行：
"""
    return prompt


def get_enabled_roles(config: Dict) -> List[tuple]:
    """获取启用的角色列表（按顺序）"""
    roles = config.get('roles', {})
    enabled = []
    
    for key, value in roles.items():
        if value.get('enabled', True) if isinstance(value, dict) else True:
            enabled.append((key, value.get('order', 99)))
    
    # 按顺序排序
    enabled.sort(key=lambda x: x[1])
    return [x[0] for x in enabled]


def get_execution_groups(config: Dict) -> List[str]:
    """获取执行组（六部）"""
    roles = config.get('roles', {})
    execution_roles = []
    
    # 三省之后的角色是六部
    for key, value in roles.items():
        order = value.get('order', 99) if isinstance(value, dict) else 99
        if order >= 4 and value.get('enabled', True) if isinstance(value, dict) else True:
            execution_roles.append(key)
    
    return execution_roles


def save_result(result: Dict, config: Dict) -> str:
    """保存结果到文件（从配置读取）"""
    output_dir = config.get('output', {}).get('directory', 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/sansheng_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    return filename


def format_result(results: Dict, config: Dict) -> str:
    """格式化结果（从配置读取）"""
    messages = config.get('messages', {})
    roles = config.get('roles', {})
    output = []
    
    output.append("=" * 50)
    output.append(messages.get('completed', '任务完成'))
    output.append("=" * 50)
    output.append("")
    
    if 'task' in results:
        output.append(f"📋 任务：{results['task']}")
        output.append("")
    
    if 'status' in results:
        status_emoji = "✅" if results['status'] == 'success' else "❌"
        output.append(f"{status_emoji} 状态：{results['status']}")
        output.append("")
    
    if 'role_results' in results:
        output.append("📝 执行摘要：")
        output.append("-" * 30)
        
        for role, result in results['role_results'].items():
            role_title = roles.get(role, {}).get('title', role)
            output.append(f"\n### {role_title}")
            
            if isinstance(result, dict):
                if 'summary' in result:
                    output.append(result['summary'])
                elif 'content' in result:
                    output.append(result['content'])
                else:
                    output.append(str(result)[:200])
            else:
                output.append(str(result)[:200])
        
        output.append("")
    
    if 'summary' in results:
        output.append("📌 汇总：")
        output.append("-" * 30)
        output.append(results['summary'])
        output.append("")
    
    output.append("=" * 50)
    
    return "\n".join(output)


class SanshengLiubuDispatcher:
    """三省六部调度器 - 从配置文件加载"""
    
    def __init__(self, config_path: str = None):
        self.config = load_config(config_path)
        self.results = {}
    
    def dispatch(self, task: str, use_parallel: bool = None) -> Dict:
        """执行三省六部调度"""
        if use_parallel is None:
            use_parallel = self.config.get('execution', {}).get('parallel_execution', True)
        
        self.results = {
            'task': task,
            'status': 'running',
            'timestamp': datetime.now().isoformat(),
            'role_results': {}
        }
        
        roles = self.config.get('roles', {})
        
        # 获取所有启用的角色，按顺序排列
        sorted_roles = sorted(
            [(k, v) for k, v in roles.items() if v.get('enabled', True)],
            key=lambda x: x[1].get('order', 99)
        )
        
        step = 1
        
        for role_key, role_info in sorted_roles:
            order = role_info.get('order', 99)
            
            # 根据角色类型确定执行方式
            if order == 0:
                # 太子：消息分拣
                print(f"👑 Step {step}: {role_info.get('title')}分拣需求...")
                context = ""
            elif order >= 1 and order <= 3:
                # 三省：串行执行
                print(f"📋 Step {step}: {role_info.get('title')}执行...")
                context = "待处理的任务"
            else:
                # 六部：并行执行
                if order == 4:  # 第一个执行组
                    if use_parallel:
                        execution_groups = [k for k, v in sorted_roles if v.get('order', 99) >= 4]
                        print(f"⚡ Step {step}: 六部并行执行 ({len(execution_groups)}个部门)...")
                context = ""
            
            # 构建 prompt
            prompt = build_role_prompt(role_key, task, context, self.config)
            self.results['role_results'][role_key] = {
                'prompt': prompt,
                'status': 'ready',
                'title': role_info.get('title')
            }
            
            # 更新步骤号（非并行执行的角色）
            if order < 4:
                step += 1
        
        self.results['status'] = 'success'
        self.results['summary'] = "三省六部执行完成，各部门已准备就绪。使用 OpenClaw 的 sessions_spawn 可以实际执行这些任务。"
        
        return self.results


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='三省六部任务调度器 - 通用版'
    )
    parser.add_argument('--task', '-t', type=str, help='任务描述')
    parser.add_argument('--interactive', '-i', action='store_true', help='交互模式')
    parser.add_argument('--config', '-c', type=str, help='配置文件路径')
    parser.add_argument('--output', '-o', type=str, help='输出目录')
    parser.add_argument('--sequential', action='store_true', help='串行执行')
    parser.add_argument('--list-departments', action='store_true', help='列出所有部门')
    
    args = parser.parse_args()
    
    # 加载配置
    config = load_config(args.config)
    
    # 列出部门
    if args.list_departments:
        print("🏛️ 三省六部 - 已配置的部门：")
        print("-" * 40)
        
        # 按顺序显示
        roles = config.get('roles', {})
        sorted_roles = sorted(roles.items(), key=lambda x: x[1].get('order', 99))
        
        for key, value in sorted_roles:
            enabled = value.get('enabled', True)
            status = "✅" if enabled else "❌"
            title = value.get('title', key)
            alias = value.get('alias', '')
            duty = value.get('duty', '')
            timeout = value.get('timeout', 60)
            print(f"{status} {title}({alias}) - {duty} [超时:{timeout}s]")
        return
    
    # 检测触发词
    if args.task and is_triggered(args.task, config):
        print("✅ 检测到触发词，启动三省六部调度")
    elif args.interactive:
        print("🔄 启动交互模式")
    else:
        print("❌ 未检测到有效任务")
        parser.print_help()
        return
    
    # 创建调度器
    dispatcher = SanshengLiubuDispatcher(args.config)
    
    # 获取任务
    task = args.task
    if args.interactive and not task:
        task = input("请输入任务描述：")
    
    if not task:
        print(config.get('messages', {}).get('no_task', '任务不能为空'))
        return
    
    # 执行调度
    print(f"\n📝 任务：{task}\n")
    result = dispatcher.dispatch(task, use_parallel=not args.sequential)
    
    # 保存结果
    output_dir = args.output or config.get('output', {}).get('directory', 'output')
    output_file = save_result(result, {**config, 'output': {'directory': output_dir}})
    print(f"\n💾 结果已保存到：{output_file}")
    
    # 格式化输出
    formatted = format_result(result, config)
    print("\n" + formatted)


if __name__ == '__main__':
    main()
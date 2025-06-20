# 典型用户单词学习流程

## 1. 启动学习会话
### 1.1 兴趣收集
1. **首次使用问卷**:
    ```
    > 请选择您感兴趣的3个领域(输入编号):
    > 1) 科技 2) 体育 3) 音乐 4) 电影
    > 5) 游戏 6) 旅行 7) 美食 8) 文学
    ```
2. **学习过程中收集**:
    - 标记为"喜欢"的单词类型
    - 造句测试中的主题偏好
    - 互动模式选择频率
3. **动态调整**:
    - 每周更新兴趣权重
    - 根据反馈优化推荐
```bash
mcp learn new --daily 20
```
- 系统响应：
```
开始新词学习，今日目标：20词
当前进度：0/20
输入"help"查看可用命令
```

## 2. 单词学习阶段
### 2.1 单词展示
1. **信息输出规则**:
    - 每次只输出一行核心信息
    - 单词显示格式: `> 单词: innovation [科技]`
    - 释义显示格式: `> 释义: 创新(名词)`
    - 例句显示格式: `> 例句: Technological innovation drives progress`
    - 测试问题格式: `> (1) 选择正确释义`
2. **交互节奏控制**:
    - 每显示一行后等待用户确认(按回车继续)
    - 复杂内容分页显示(如多条例句)
```
单词 #1/20: diligent [ˈdɪlɪdʒənt] (adj.)
定义：勤奋的，刻苦的
记忆提示："dili"谐音"地里"，想象在地里勤奋耕作
```

### 2.2 例句展示
如果例句的结构如下：
例句: 1.  Abigail is my best friend.（艾比盖尔是我最好的朋友。）
2.  Abigail always has a bright smile on her face.（艾比盖尔脸上总是带着明亮的笑容。）
3.  We are going to visit Abigail this weekend.（我们这个周末要去拜访艾比盖尔。）
需要拆分为3次操作，每次交互显示1个句子，用户确认后显示下一个。


```
例句1: She is a diligent student.
例句2: Diligent work leads to success.
```

### 2.3 即时测试
#### 2.3.1 选择题
单词的候选项目如何产生？ 是LLM实时产生？还是从中央服务器拉取？
单词词库不是中央产生的，因此候选项我们也不知道


```
请选择diligent的正确含义：
> 1. 懒惰的
  2. 勤奋的
  3. 聪明的
(使用↑↓方向键选择，Enter确认)
> 输入exit可随时退出
```

#### 2.3.2 填空题
```
显示句子并标注空缺位置: The ___ student always finishes homework early
输入: 直接输入完整单词
```

#### (option)2.3.3 拼写测试
```
语音朗读单词
输入: 拼写听到的单词
```

#### (option)2.3.4 释义匹配
```
显示4个释义
输入: 匹配单词与释义(1-4)
```

#### (option)2.3.5 造句测试
```
显示单词
输入: 用该单词造一个句子
```

**交互规范**:
1. 颜色方案:
    - 系统提示(>开头): 青色
    - 操作指令(括号内): 黄色
    - 选项(数字+A/B/C/D): 绿色
    - 错误信息: 红色
    - 成功信息: 绿色
    - 警告信息: 黄色
    - 帮助信息: 蓝色

2. 指令格式:
   - 以`>`开头的行是系统提示
   - 括号`()`内的内容是操作说明
   - 数字编号`1.` `2.`等是可选选项
2. 用户输入:
   - 方向键: 直接响应
   - 数字+Enter: 直接选择
   - 其他输入: 显示`无效输入，请重试`

**技术实现说明**:
1. 使用终端控制库实现光标移动
2. 高亮显示当前选中项
3. 支持快捷键:
   - ↑/←: 上移选项
   - ↓/→: 下移选项
   - Enter: 确认选择
   - 1-9: 直接数字选择



## 3. AI增强学习

### 3.1 AI生成候选图库
1. **图像生成**:
   - 根据单词含义生成相关的图片
   - 支持多种风格（写实、卡通、简笔画等）
   - 可定制图片尺寸和风格

2. **图像关联**:
   - 将生成的图片与单词释义关联
   - 支持图片标注和解释
   - 提供图片记忆提示

### 3.2 答题评估系统
1. **实时评分**:
   - 每道题目的正确性评估
   - 答题用时统计
   - 答案分析和解释

2. **学习反馈**:
   - 针对错误提供详细解释
   - 推荐相关练习题
   - 个性化学习建议

3. **答题统计**:
    - 详细记录每道题目的答题情况
    - 自动计算答题总用时
    - 统计答题总数、正确题数和错误题数
    - 计算正确率和平均用时
    - 生成可视化学习报告
    
    示例统计输出：
    ```
    本次学习统计：
    > 答题总用时：45分钟
    > 答题总数：20题
    > 正确题数：15题
    > 错误题数：5题
    > 正确率：75%
    > 平均用时：2.25分钟/题
    > 最快答题：0.5分钟
    > 最慢答题：4.2分钟
    > 薄弱知识点：商务英语(3/5正确)
    ```

4. **进度追踪**:
   - 学习曲线可视化
   - 薄弱点分析
   - 学习效率评估

### 3.3 AI智能互动

### 3.4 词根与同义词系统
1. **词根表**
   - 按词根分类单词（如：act, form, spect等）
   - 标注词源语言（拉丁/希腊/古英语等）
   - 包含词根含义和衍生词示例

2. **同义词表**
   - 按核心含义分组单词
   - 标注词性差异和使用场景
   - 包含近义词强度对比（强/中/弱）

### 3.5 AI智能互动
1. **AI生成例句**: 根据用户学习历史生成个性化例句
   - 基于用户已学单词和错误记录生成上下文例句
   - 支持多种场景例句（商务/日常/学术等）
   - 可调节例句难度等级

2. **AI单词解析**: 提供词根词缀、联想记忆等深度解析
   - 词源学分析（拉丁/希腊词根等）
   - 同义词/反义词网络
   - 记忆技巧和联想提示

3. **AI语音互动**: 支持语音问答测试单词发音和含义
   - 语音识别评估发音准确性
   - 口语问答测试单词理解
   - 支持多种口音识别

4. **AI学习路径**: 动态调整学习顺序和难度
   - 基于遗忘曲线优化复习时间点
   - 根据答题表现自动调整难度
   - 个性化推荐学习重点

### 3.4 趣味学习模式
1. **单词故事**: AI生成包含目标单词的趣味短故事
2. **单词挑战**: AI设计的填空、改错等互动挑战
3. **学习游戏**: 单词拼图、记忆卡片等小游戏
4. **成就系统**: AI根据学习表现颁发虚拟徽章

## 4. 学习控制
### 4.1 标记困难词
```
输入：mark
系统：已标记为困难词，将增加复习频率
```

### 3.2 暂停/继续
```
输入：pause
系统：已保存进度，输入resume继续
```

## 4. 学习统计
```
输入：stats
今日进度：15/20
正确率：86%
困难词：3个
预计完成时间：8分钟
```

## 5. 结束学习
```
输入：exit
系统：已保存学习记录，明日将复习今日标记的3个困难词
```

## 数据同步
```bash
mcp sync --cloud
```
- 系统响应：
```
同步完成，最新进度已更新至所有设备
```



- 添加了AI生成候选图库功能：

- 支持多种风格的图片生成
- 图片与单词释义关联
- 提供图片标注和记忆提示
- 增加了答题评估系统：

- 实时评分和答题用时统计
- 针对性学习反馈
- 详细的答题统计信息
- 学习进度追踪和分析
- 修复了文档结构：

- 重新编排了章节编号，避免重复
- 保持了文档的层次结构清晰


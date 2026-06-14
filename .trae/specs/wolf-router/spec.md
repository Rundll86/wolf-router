# Wolf Router - Product Requirement Document

## Overview
- **Summary**: Wolf Router 是一个基于校园场景的智能路由系统，用户通过 Web 界面与 LLM 对话，前端将请求发送到后端 Flask 服务，后端调用路由器 LLM 分析用户请求，路由器 LLM 输出 JSON 格式的路由决策（包含目标模型名称和路由理由），后端验证模型名称是否在允许列表中，然后将请求转发到选中的 AI 模型，并将响应流式返回给前端。
- **Purpose**: 在校园场景中，不同类型的问题（如图识物、学科问题、编程问题、文学问题）需要不同专长的 AI 模型来处理，Wolf Router 通过路由器 LLM 实现智能路由，为用户提供最优的模型选择。
- **Target Users**: 在校学生、教职工，需要使用各类 AI 服务解决学习和工作问题的校园用户。

## Goals
- 提供友好的 Web 对话界面，支持用户自然语言输入和图片上传
- 实现前端与后端 Flask 服务的通信
- 通过路由器 LLM 实现智能路由决策
- 定义允许的模型枚举列表，限制 LLM 输出范围
- LLM 输出 JSON 格式，包含模型名称和路由理由
- 展示路由决策理由，增强用户信任感
- 支持多种主流 AI 模型的接入（通义千问、GLM、Claude、GPT、Gemini、豆包等）
- 后端通过环境变量读取 API Key，从代码配置读取 base_url
- 支持流式响应返回

## Non-Goals (Out of Scope)
- 不自行训练 AI 模型，仅作为路由层
- 不处理非校园场景的请求
- 后端不解析用户意图，完全依赖路由器 LLM

## Background & Context
- 校园场景涉及多种类型的问题：植物识别、学科答疑、编程辅助、文学创作等
- 不同 AI 模型在不同领域各有专长：
  - 通义千问/GLM：多模态能力强，适合图像识别
  - Claude/GPT：理科能力强，适合学科问题和编程
  - Gemini/豆包：文学能力强，适合文学创作
- 路由器 LLM 负责分析用户请求并输出路由决策，后端只需验证和执行

## Functional Requirements
- **FR-1**: 用户可以通过 Web 界面输入自然语言请求和上传图片
- **FR-2**: 前端将请求发送到后端 Flask 服务
- **FR-3**: 后端调用路由器 LLM 分析用户请求
- **FR-4**: 路由器 LLM 输出 JSON 格式的路由决策 {"model": "...", "reason": "..."}
- **FR-5**: 后端验证模型名称是否在允许列表中
- **FR-6**: 后端根据路由决策将请求转发到选中的目标模型
- **FR-7**: 后端展示路由决策结果和理由
- **FR-8**: 后端从环境变量读取 API Key
- **FR-9**: 后端从代码配置读取各模型的 base_url
- **FR-10**: 后端支持流式响应返回给前端
- **FR-11**: 定义路由器 LLM 的提示词，明确其职责和输出格式

## Non-Functional Requirements
- **NFR-1**: 路由决策响应时间 < 1 秒
- **NFR-2**: 路由准确率 > 90%
- **NFR-3**: 支持并发用户访问
- **NFR-4**: 界面响应式设计，支持移动端
- **NFR-5**: 支持流式响应，提升用户体验

## Constraints
- **Technical**: 前端基于 Vue 3 + TypeScript + Webpack，后端基于 Python + Flask
- **Business**: 校园网络环境下的可用性
- **Dependencies**: 需要接入外部 AI 模型的 API，API Key 通过环境变量管理

## Assumptions
- 用户具备基本的网络使用能力
- 校园网络可访问相关 AI 模型服务
- 用户接受路由到不同模型进行处理
- 环境变量已正确配置各模型的 API Key

## Acceptance Criteria

### AC-1: 路由器 LLM 输出 JSON 格式
- **Given**: 用户发送请求到后端
- **When**: 后端调用路由器 LLM
- **Then**: LLM 输出合法 JSON 格式，包含 "model" 和 "reason" 字段
- **Verification**: `programmatic`

### AC-2: 模型名称验证
- **Given**: 路由器 LLM 返回路由决策
- **When**: 后端验证模型名称
- **Then**: 仅当模型名称在允许列表中时才继续处理，否则返回错误
- **Verification**: `programmatic`

### AC-3: 植物识图请求路由
- **Given**: 用户上传校园植物图片并询问"这是什么植物？"
- **When**: 前端发送请求到后端，后端调用路由器 LLM
- **Then**: LLM 输出 {"model": "qwen" | "glm", "reason": "植物识图需要多模态能力，通义千问/GLM 在图像识别方面表现出色"}
- **Verification**: `programmatic`

### AC-4: 学科问题路由
- **Given**: 用户输入"请解释量子力学的基本原理"
- **When**: 前端发送请求到后端，后端调用路由器 LLM
- **Then**: LLM 输出 {"model": "claude" | "gpt", "reason": "学科问题需要较强的理科能力，Claude/GPT 在学术领域表现优异"}
- **Verification**: `programmatic`

### AC-5: 编程问题路由
- **Given**: 用户输入"帮我写一个 Python 排序算法"
- **When**: 前端发送请求到后端，后端调用路由器 LLM
- **Then**: LLM 输出 {"model": "claude" | "gpt", "reason": "编程问题需要较强的代码能力，Claude/GPT 在编程方面表现出色"}
- **Verification**: `programmatic`

### AC-6: 文学问题路由
- **Given**: 用户输入"帮我写一首关于春天的诗"
- **When**: 前端发送请求到后端，后端调用路由器 LLM
- **Then**: LLM 输出 {"model": "gemini" | "doubao", "reason": "文学创作需要较强的语言艺术能力，Gemini/豆包在文学方面表现优异"}
- **Verification**: `programmatic`

### AC-7: 路由理由展示
- **Given**: 后端完成路由决策
- **When**: 用户查看前端界面
- **Then**: 用户界面清晰显示目标模型名称和路由理由
- **Verification**: `human-judgment`

### AC-8: 流式响应
- **Given**: 用户发送请求
- **When**: 后端调用目标 AI 模型 API
- **Then**: 后端将响应流式返回给前端，前端实时显示
- **Verification**: `human-judgment`

### AC-9: 环境变量配置
- **Given**: 系统启动
- **When**: 后端加载配置
- **Then**: 后端从环境变量读取各模型的 API Key
- **Verification**: `programmatic`

### AC-10: 模型 API 接入
- **Given**: 后端路由请求到目标模型
- **When**: 调用模型 API
- **Then**: 成功调用 Claude、GPT、豆包、Gemini、通义千问、GLM 的 API
- **Verification**: `programmatic`

## Open Questions
- [ ] 如何处理模糊或混合类型的请求？
- [ ] 是否需要支持用户手动选择模型？
- [ ] 如何处理模型服务不可用的情况？
# Jiyun Web 改造账本

## 目标基线

- 源码基线：`jiyun-web` tag `v0.9.0`，分支 `jiyun/dev`
- 目标产品：`jiyun-web` v0.9.0
- 配套 CLI：`jiyun` v0.85.1
- 核心要求：共享 `~/.jiyun/agent` 配置、凭据、插件和会话；保留主要 Web 功能；清理与上游开源维护相关的冗余内容；README 仅保留中文。

## 执行阶段

- [x] 1. 基线确认：分支、版本、工作区状态、项目约束
- [x] 2. 运行时耦合审计：包依赖、配置目录、环境变量、命令、存储键
- [x] 3. 产品迁移：包名、CLI、应用标题、PWA、文案与内部标识
- [x] 4. Jiyun 适配：切换 coding-agent SDK，并共享 Jiyun 数据目录
- [x] 5. 仓库精简：CICD、发布/贡献、多语言 README 与上游宣传内容
- [x] 6. 文档重写：中文 README、安装/开发/联调说明
- [x] 7. 验证：依赖安装、类型检查、测试、lint、生产构建、运行时烟测

## 决策记录

1. 不对 `pi` 做无差别文本替换：底层兼容包 `@earendil-works/pi-*`、历史协议字段或第三方插件参数可能仍需保留。
2. Web 的核心 SDK 改用 `@jiyun-ai/jiyun-coding-agent@0.85.1`；底层 agent/ai/tui 包保持与 Jiyun CLI 相同的 0.85.1 ABI。
3. 用户数据以 Jiyun CLI 的 `getAgentDir()` 为准，默认落在 `~/.jiyun/agent`，避免 Web 和 CLI 产生两套配置。
4. 源码开发优先支持本地 Jiyun monorepo 联调；发布包仍保持可独立安装。
5. 本地 file 依赖启用 npm `install-links=true`，按真实 npm 包复制安装，避免 Next/Webpack 穿透 Junction 进入 Jiyun monorepo。
6. `@jiyun-ai/jiyun-coding-agent` 作为 `bundleDependencies` 随 Jiyun Web tarball 发布，保证安装包固定配套 0.85.1。
7. 保留 `@earendil-works/pi-agent-core`、`pi-ai`、`pi-tui` 作为 Jiyun 0.85.1 的底层 ABI；保留 `pi-bash-*`、`pi-subagents`、`--agent pi` 等兼容协议。
8. 保留上游 MIT `LICENSE`，满足衍生分发的版权和许可证义务。

## 验证记录

- `npm install`：成功；Jiyun coding-agent 为普通目录安装，非 Junction。
- `npm run typecheck`：通过。
- `npm test`：947 项，945 通过，0 失败，2 跳过。
- `npm run lint`：通过。
- `npm run build`：通过；15 个静态页面生成完成，无 Node 内置模块或依赖缺失错误。
- 源码生产烟测：主页 200，manifest 为 `Jiyun Web`/`zh-CN`，读取 23 个 Jiyun 会话和默认模型。
- `npm pack`：生成 `jiyun-ai-jiyun-web-0.9.0.tgz`，约 42 MB，包含 `.next`、`jiyun-web` CLI 和内置 Jiyun coding-agent。
- 临时独立安装：成功注册 `jiyun-web` 命令；安装目录非链接。
- 安装包生产烟测：主页 200，品牌正确，读取 23 个 Jiyun 会话和默认模型。
- 仓库目录已由 `pi-web` 重命名为 `jiyun-web`；在新路径重新生产构建通过。
- 默认端口已由 `30141` 调整为 `30142`，可与 Pi Web 同时运行。
- `@jiyun-ai/jiyun-web@0.9.0` 已通过 tarball 复制安装到本机 npm 全局目录；`jiyun-web` 命令和生产 `.next` 产物验证通过。
- `npm install` 报告 2 个 moderate 级依赖漏洞；未自动执行 `npm audit fix`，避免未经评估升级锁定依赖。

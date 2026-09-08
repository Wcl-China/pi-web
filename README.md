# Jiyun Web

Jiyun Web 是 Jiyun coding agent 的本地浏览器界面。它与 Jiyun CLI 共用模型、凭据、插件、技能、项目配置和会话文件，可在浏览器中继续对话、管理会话、运行工具、配置模型并浏览项目文件。

## 版本配套

| 组件 | 版本 |
| --- | --- |
| Jiyun Web | `0.9.0` |
| Jiyun coding agent | `0.85.1` |
| Node.js | `>= 22.19.0` |

本版本基于 Pi Web `v0.9.0` 改造，并使用 Jiyun coding agent `v0.85.1` 作为核心运行时。

## 主要功能

- 按项目查看、继续、重命名、导出和删除 Jiyun 会话。
- 在网页中发送消息、运行工具、切换模型和思考等级。
- 管理 Provider 登录、API Key、模型、插件和技能。
- 浏览项目文件、查看 Git Diff，并预览 Markdown、图片、音频、PDF 和 DOCX。
- 管理 Git worktree、内置终端和子代理。
- 支持桌面与移动端，并可安装为 PWA。

## 目录关系

源码开发时，Jiyun Web 默认从相邻的 Jiyun 仓库加载核心包：

```text
jiyun-agent/
├── jiyun/                         # Jiyun v0.85.1 monorepo
│   └── packages/coding-agent/
└── jiyun-web/                     # Jiyun Web v0.9.0
```

`package.json` 中使用以下本地依赖：

```json
"@jiyun-ai/jiyun-coding-agent": "file:../jiyun/packages/coding-agent"
```

因此首次安装 Jiyun Web 之前，应先完成 Jiyun coding-agent 的依赖安装和构建。

## 从源码运行

### 1. 构建 Jiyun coding agent

```powershell
cd C:\Users\37886\Project\21_软件智能体\jiyun-agent\jiyun
npm install
npm run build --workspace=@jiyun-ai/jiyun-coding-agent
```

如果底层 workspace 包尚未构建，首次应执行完整构建：

```powershell
npm run build
```

### 2. 安装 Jiyun Web 依赖

```powershell
cd C:\Users\37886\Project\21_软件智能体\jiyun-agent\jiyun-web
npm install
```

npm 会从相邻源码打包并安装 `@jiyun-ai/jiyun-coding-agent`。项目通过 `.npmrc` 启用 `install-links=true`，因此该依赖会按真实 npm 包的方式复制安装，而不是建立会被 Webpack 追踪进 Jiyun monorepo 的目录 Junction；其余第三方依赖安装到本项目的 `node_modules`。

如果之后修改并重新构建了相邻的 Jiyun coding-agent，需要刷新 Web 项目里的复制包：

```powershell
npm install --force
```

### 3. 启动开发服务器

```powershell
npm run dev
```

浏览器访问 <http://127.0.0.1:30142>。开发模式使用 Turbopack；开发服务器运行期间不要同时执行生产构建。Jiyun Web 使用 `30142`，可与默认使用 `30141` 的 Pi Web 同时运行。

局域网监听：

```powershell
npm run dev:lan
```

### 4. 质量检查

```powershell
npm run typecheck
npm test
npm run lint
```

### 5. 生产构建与启动

```powershell
npm run build
npm run start
```

## 全局安装 `jiyun-web` 命令

生产构建完成后，可打包并复制安装到 npm 全局目录：

```powershell
npm list -g 2>$null | Select-String "jiyun-web"
npm uninstall -g @jiyun-ai/jiyun-web
npm pack
npm install -g .\jiyun-ai-jiyun-web-0.9.0.tgz
Remove-Item .\jiyun-ai-jiyun-web-0.9.0.tgz
```

安装后可在任意目录启动：

```powershell
jiyun-web
jiyun-web --help
jiyun-web -p 8080 -H 127.0.0.1 --no-open
```

## 配置

| 参数或环境变量 | 用途 | 默认值 |
| --- | --- | --- |
| `--help`、`-h` | 打印帮助并退出 | — |
| `--port <端口>`、`-p <端口>` 或 `PORT` | 服务端口 | `30142` |
| `--hostname <主机>`、`-H <主机>` 或 `JIYUN_WEB_HOSTNAME` | 监听主机名 | `127.0.0.1` |
| `--no-open` 或 `JIYUN_WEB_NO_OPEN=1` | 禁止自动打开浏览器 | 自动打开 |
| `JIYUN_WEB_ALLOWED_HOSTS` | 额外允许的代理或自定义主机名 | 未设置 |
| `JIYUN_WEB_PASSWORD` | 启用 HTTP Basic Auth，用户名固定为 `jiyun` | 不启用 |
| `JIYUN_WEB_IDLE_TIMEOUT_MS` | 空闲会话运行时回收时间 | 10 分钟 |

监听非回环地址会暴露可执行高权限操作的智能体。仅应在可信局域网使用，并建议设置足够长的随机密码：

```powershell
$env:JIYUN_WEB_PASSWORD = "足够长的随机密码"
jiyun-web --hostname 0.0.0.0
```

Basic Auth 不加密 HTTP 流量；不要将服务直接暴露到互联网。

## 与 Jiyun CLI 共享的数据

Jiyun Web 通过 `@jiyun-ai/jiyun-coding-agent` 的 `getAgentDir()` 获取数据目录，默认与 Jiyun CLI 共用：

```text
~/.jiyun/agent/
├── auth.json
├── models.json
├── settings.json
├── npm/
├── git/
├── skills/
└── sessions/
```

可用 `JIYUN_CODING_AGENT_DIR` 覆盖该目录。项目级资源使用 `<工作目录>/.jiyun/`。

插件安装范围与 CLI 一致：

- 全局：`~/.jiyun/agent/{npm,git}`，对所有项目生效。
- 项目：`<工作目录>/.jiyun/{npm,git}`，仅对当前项目生效。

Jiyun 继续兼容 Pi 插件清单和 skills CLI 生态，因此源码中有少量 `pi` 协议标识会被有意保留，例如 `pi-bash-*` 临时文件前缀、`pi-subagents` 兼容检测，以及 skills CLI 的 `--agent pi` 参数。它们不是产品品牌残留。

## 仓库结构

```text
app/          Next.js 页面与 API 路由
components/   React 界面组件
hooks/        客户端状态和交互 hooks
lib/          会话、模型、插件、文件、Git 与安全逻辑
public/       PWA 与静态资源
bin/          `jiyun-web` 命令入口
docs/         架构决策和专题说明
e2e/          端到端测试
```

详细架构和开发注意事项见 [AGENTS.md](./AGENTS.md)，本次迁移过程见 [JIYUN_WEB_MIGRATION_LEDGER.md](./JIYUN_WEB_MIGRATION_LEDGER.md)。

## 许可证

本项目基于 MIT 许可的上游项目改造，原版权与许可证声明见 [LICENSE](./LICENSE)。

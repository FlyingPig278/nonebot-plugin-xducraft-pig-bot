# XDUCraft Pig Bot

基于 NoneBot 2 与 OneBot v11 的 PigHub 猪猪图查询与定时群推送插件。

支持从 PigHub 检索匹配的表情图片，并支持通过 APScheduler 定时任务每 6 小时向开启推送的群发送随机猪猪图。

运行整套机器人请看 [FlyingPig278/XDUCraft-bot](https://github.com/FlyingPig278/XDUCraft-bot)。

## 安装与加载

本软件包未发布至公共 PyPI 仓库，请使用 Git 地址安装。

### 1. 安装核心包与插件

在现有的 NoneBot 2.4.x 环境中，先安装 Core 核心包，再安装本插件：

```bash
pip install "nonebot-plugin-xducraft-core[onebot] @ git+https://github.com/FlyingPig278/nonebot-plugin-xducraft-core.git@v0.3.0"
pip install "nonebot-plugin-xducraft-pig-bot @ git+https://github.com/FlyingPig278/nonebot-plugin-xducraft-pig-bot.git@v0.1.0"
```

### 2. 配置插件加载

在 NoneBot 项目的 pyproject.toml 中向现有 plugins 列表追加以下模块（请保留已有的其他插件和适配器）：

```toml
[tool.nonebot]
plugins = [
    "xducraft_config",
    "xducraft_pig_bot",
]
```

## 启用与首次使用

插件安装后，全局总开关、各群插件总开关以及各功能开关默认处于关闭状态。

### 1. 开启插件与群总开关

本插件包含手动查询与定时推送两项独立功能，不是单功能插件。在群内开启或关闭单独某项功能（例如发送 `/pig query on` 或 `/pig auto on`）仅修改该功能的状态，不会自动开启或关闭本群的插件总开关。

要在群内正常使用，必须确保以下三项开关全部开启：
1. 全局总开关处于开启状态。
2. 本群插件总开关处于开启状态。
3. 对应的具体功能处于开启状态（查询功能 `pig_query` 或定时推送功能 `pig_auto_push`）。

方式一：使用 Web 管理面板（推荐）

如果配置了 [nonebot-plugin-xducraft-admin](https://github.com/FlyingPig278/nonebot-plugin-xducraft-admin)，访问管理面板（默认地址 http://127.0.0.1:8765）：
1. 在“插件”页面开启“猪猪图”全局开关。
2. 在“群聊”页面选择对应群，开启本群的“猪猪图”插件总开关。
3. 在群卡片中直接开启对应功能，或在群内使用指令管理功能开关。

方式二：不使用 Web 管理面板

如果不运行管理面板，请参考 Core 文档中的[不使用网页时启用插件](https://github.com/FlyingPig278/nonebot-plugin-xducraft-core#不使用网页时启用插件)。通过一次性脚本调用 Core 配置接口，同时开启全局插件开关、目标群插件总开关以及对应的群功能（`pig_query` 或 `pig_auto_push`）。由于 Core 会在前置检查中拦截未在群中启用的插件消息，且修改单项功能不会自动开启群总开关，必须在 Core 中完整配置。

### 2. 指令列表与使用说明

在确认全局与群总开关均已开启后，可通过以下指令使用或调整功能：

| 指令 | 权限要求 | 说明 |
| :--- | :--- | :--- |
| `/pig [关键词]` | 任意群成员 | 查询猪猪图，未带关键词时随机抽取一张；命中多张时使用合并转发 |
| `/pig query on` / `off` | 群管理 / 群主 / 超管 | 开启或关闭本群手动查询功能 |
| `/pig auto on` / `off` | 群管理 / 群主 / 超管 | 开启或关闭本群定时自动推送功能 |
| `/pig status` | 群管理 / 群主 / 超管 | 查看本群各项开关状态与配置参数 |

若额外安装了 [nonebot-plugin-xducraft-features](https://github.com/FlyingPig278/nonebot-plugin-xducraft-features) 插件，管理员亦可在群内使用 `/功能 on 猪猪图查询` 或 `/功能 on 猪猪图推送` 开关对应功能。注意本插件包含多项独立功能，通过 `/功能` 指令修改单独功能不会自动开启群插件总开关。

## 配置项说明

群级配置保存在 Core 数据库中，可在 Web 管理面板群卡片中调整：

- `max_forward_results`：合并转发图片数量上限，默认为 5 张。当关键词检索命中多张图片时，最多从中抽取该数量的图片进行合并转发。

## 本地开发与测试

克隆本仓库后，可以在本地虚拟环境中安装开发依赖并运行测试：

```bash
pip install "nonebot-plugin-xducraft-core[onebot] @ git+https://github.com/FlyingPig278/nonebot-plugin-xducraft-core.git@v0.3.0"
pip install -e ".[dev]"
pytest
python -m build
```

## 数据存储与历史迁移

历史配置文件 `pig_bot_config.json` 仅用于首次启动时单次导入。Core 首次启动会自动将其导入 Core SQLite 数据库的 `pig_bot` 命名空间中，导入完成后旧文件不再保存新设置，后续修改以数据库为准。

表情图片直接请求外部 PigHub 接口获取，本地不保存图片文件，无额外业务数据库。如需自定义数据存放目录，请在启动 Python 进程前配置操作系统环境变量 `XDUCRAFT_DATA_DIR` 为绝对路径。

## 许可证说明

本项目源码采用 MIT 许可证开源，详见 [LICENSE](LICENSE)。

第三方 API 接口与图片资源版权属于原作者或图库托管方。

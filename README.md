# Genius-Bot
A kook bot framework base on khl.py

### TODO

#### 插件系统

- 统一的插件加载，卸载

- 插件的回调

  `on_load` 插件被 `加载` 调用

  `on_unload` 插件被 `卸载` 调用

  `on_message` 当机器人接收到 `消息` 时调用

  `on_event` 当机器人接收到 `事件` 时调用
  
- 方便简洁的命令系统

#### 插件格式

- 单文件插件

  一个 `.py` 文件

  包含 `PLUGIN_META`

  PLUGIN_META 内容暂未定义，初步想法包含 `id`，`version`，`author` 等信息

- 多文件插件

  一个文件夹包含一个 `geniusbot.plugin.json` 文件来定义插件信息

  一个包含 `__init__.py` 的软件包

- 打包插件

  一个将多文件插件打包为 `.gbot` 文件，结构与 `多文件插件` 相同，只是压缩后的格式，方便后期分发插件。 

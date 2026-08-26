# AI Work Agent DAU 动态排名竞赛

使用 Python 和 Matplotlib 将 AI Work Agent 的月度日活跃用户数（DAU）制作成动态排名视频。

项目包含一套可复现的模拟数据生成脚本，以及一个 30 秒、1280 × 720、25 FPS 的 MP4 动画渲染脚本。

## 效果

- 12 个 AI Agent 的 DAU 排名动态变化
- 覆盖 2023-01 至 2024-12，共 24 个月
- 开场标题、月度排名竞赛和结尾最终排名
- 支持关键事件标注，例如 Kimi 爆发增长、Claude 强势追击
- 输出文件：`agent_dau_race.mp4`

> 项目中的 DAU 数据为模拟数据，仅用于演示数据可视化流程，不代表真实市场统计结果。

## 项目结构

```text
.
├── animate.py          # 读取 CSV 并渲染动态排名视频
├── generate_data.py    # 生成模拟 DAU 数据
├── dau_data.csv        # 12 个 Agent × 24 个月的数据
├── agent_dau_race.mp4  # 已生成的视频示例
└── stills/             # 动画关键帧截图
```

## 环境要求

- Python 3.9 或更高版本
- FFmpeg
- Python 依赖：
  - `matplotlib`
  - `numpy`
  - `pandas`

## 安装依赖

建议使用虚拟环境：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install matplotlib numpy pandas
```

安装 FFmpeg：

```bash
# macOS，使用 Homebrew
brew install ffmpeg
```

确认 FFmpeg 可用：

```bash
ffmpeg -version
```

## 使用方法

### 1. 生成模拟数据

```bash
python generate_data.py
```

脚本会重新生成 `dau_data.csv`，并打印每个月的行业 DAU 总量预览。

### 2. 渲染视频

```bash
python animate.py
```

渲染完成后会生成或覆盖 `agent_dau_race.mp4`。默认输出规格如下：

| 参数 | 值 |
| --- | --- |
| 时长 | 30 秒 |
| 分辨率 | 1280 × 720 |
| 帧率 | 25 FPS |
| 编码器 | FFmpeg 默认 MP4 编码 |
| 码率 | 4000 kbps |

## 自定义配置

在 `animate.py` 顶部可以调整视频参数：

- `W`、`H`：画布尺寸
- `FPS`：帧率
- `FPS_TOTAL`：总帧数，当前为 30 秒 × 25 FPS
- `N_AGENTS`：每一帧显示的 Agent 数量
- `BG_COLOR`：背景颜色
- `MILESTONES`：关键月份和标注文案
- `BAR_COLORS`：各 Agent 的柱状条颜色

在 `generate_data.py` 中可以调整：

- `AGENTS`：Agent 名称、类别、初始 DAU 和增长率
- `EVENTS`：指定月份的增长冲击
- `random.seed(42)`：固定随机种子，保证数据可复现

## 在其他目录运行

当前两个脚本中的 `VIDEO_DIR` 和 CSV 输出路径使用了本机绝对路径：

```text
/Users/ianonymous/.openclaw/workspace/agent_dau_video
```

如果项目被移动到其他目录，请先将 `animate.py` 中的 `VIDEO_DIR` 改为项目实际路径，并同步修改 `generate_data.py` 最后的 CSV 输出路径。

## 常见问题

### `No movie writers available` 或找不到 FFmpeg

确认已安装 FFmpeg，并检查命令是否在 PATH 中：

```bash
which ffmpeg
ffmpeg -version
```

### 中文显示为方框或乱码

`animate.py` 当前使用 macOS 的 `PingFang TC` 字体。如果系统没有该字体，请将：

```python
font_prop = fm.FontProperties(family="PingFang TC")
```

替换为本机已安装的中文字体。

### 重新生成视频前是否需要重新生成数据

不需要。只要 `dau_data.csv` 已存在，就可以直接运行 `animate.py`。只有在修改了 `AGENTS` 或 `EVENTS` 后，才需要先运行 `generate_data.py`。

## 许可证

本项目未附带单独的许可证文件，仅作为数据可视化演示项目使用。

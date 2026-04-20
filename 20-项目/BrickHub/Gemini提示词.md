---
title: "BrickHub Gemini/Copilot 提示词模板"
date: 2026-04-08
tags: [BrickHub, 提示词, Gemini, Copilot]
---



太棒了，我们这就开始 BrickHub 的第一步：实现**一个标准 2x6 乐高积木的 3D 渲染**。

既然你有 GitHub Copilot（建议在 VS Code 中结合 Copilot Chat 使用），我为你准备了两份提示词（Prompts）。一份用于让 Copilot 帮你创建项目骨架，另一份用于实现核心的渲染代码。

### 前置准备（你需要手动操作）：

1. **创建一个空文件夹**（例如 `brickhub-proto`）。
    
2. **用 VS Code 打开它**。
    
3. **确保 GitHub Copilot 插件已启用**。
    

---

### 任务 1：创建项目骨架

在 VS Code 中打开 **Copilot Chat**（通常在左侧边栏，或者快捷键 `Ctrl+I` / `Cmd+I` 呼出内联聊天），发送以下提示词：

#### 提示词 (Prompt 1)：

> I want to create a web prototype for a LEGO building app called 'BrickHub'. Using Next.js (Page Router is fine for simplicity), React, and Tailwind CSS, please help me scaffold the basic project structure. Create a single `index.js` page with a centered title "BrickHub Proto" and a blank canvas area below it where we will eventually render 3D. Please provide the terminal commands to install dependencies and the necessary file code.

**Copilot 预期产出：**

- `npx create-next-app` 相关的命令行指令。
    
- 一个基本的 `src/pages/index.js` 代码。
    

> **手动操作：** 根据 Copilot 的指示，在终端执行命令完成项目初始化，并确保项目能用 `npm run dev` 跑起来。

---

### 任务 2：实现 2x6 乐高积木的 3D 渲染

这是核心的一步。我们将直接利用 **Three.js** 的基础几何体来搭建这个 2x6 的积木，而不是引入复杂的外部 LDraw 解析库。这非常适合 MVP 阶段。

在 Copilot 帮你创建好项目后，**新建（或打开）`src/components/BrickRenderer.js`** 文件（如果 Copilot 没有帮你建 `components` 目录，请手动建一个）。

在空文件中呼出 Copilot Chat，发送以下详细提示词：

#### 提示词 (Prompt 2 - 核心)：

> I need a React component named `BrickRenderer` that uses `@react-three/fiber` and `@react-three/drei` to render a single, standard LEGO-like 2x6 brick in 3D.
> 
> **Requirements:**
> 
> 1. **Technologies:** Use React Three Fiber for rendering.
>     
> 2. **The Brick Body:** Create a `Mesh` with a `BoxGeometry`. The dimensions should represent a 2x6 brick. In LEGO standard units (LDU), a 1x1 brick is roughly 20x20x24 LDU (including stud). For simplicity in Three.js units, let's use: Width=2, Height=1.2, Depth=6. The color should be "bright red".
>     
> 3. **The Studs (Nobs):** Add 12 cylinders (`CylinderGeometry`) on top of the box, arranged in a 2x6 grid. They should be the same color as the body.
>     
> 4. **Scene Setup:** Include `<OrbitControls />` from `@react-three/drei` so I can rotate and zoom the brick. Add a `<gridHelper />`, basic `<ambientLight />`, and a `<directionalLight />` for shadows and realism.
>     
> 5. **Output:** Provide the complete code for `BrickRenderer.js` and the necessary `npm install` command for the react-three dependencies.
>     

**Copilot 预期产出：**

- `npm install three @react-three/fiber @react-three/drei` 指令。
    
- 完整的 `BrickRenderer.js` 代码，包含正确的几何体计算和场景布置。
    

> **手动操作：**
> 
> 1. 在终端安装依赖。
>     
> 2. 将 Copilot 生成的代码复制到 `src/components/BrickRenderer.js`。
>     
> 3. **最后，修改 `src/pages/index.js`**，引入并使用这个新组件。你可以这样问 Copilot：“_How do I import and use the `<BrickRenderer />` component in my `src/pages/index.js`?_”
>     

---

### Vibe Coding 的下一步挑战

当你成功在浏览器里看到那个可以旋转的红色 2x6 积木时，你就完成了第一阶段！

**接下来的 Vibe 方向：**

你可以尝试对 Copilot 说：“_现在，修改 `BrickRenderer` 组件，使其接受一个包含 LDraw 代码的字符串作为 props，并根据代码动态生成积木堆叠。_” (这需要开始解析简单的 LDraw 文本格式了)。




太棒了！看到那个红色积木在网页上旋转，意味着你已经成功打通了 **3D 渲染管线**。这是最难的一步。

现在我们要进入 **Vibe Coding 的灵魂阶段**：**从“硬编码”转向“模型驱动”**。我们要让 AI 学会理解 LDraw 这种积木语言，并能根据简单的指令“盖房子”。

接下来的任务是：**实现一个简单的 LDraw 解析器，并支持多块积木的堆叠。**

---

### 任务 3：让积木动起来（解析 LDraw 指令）

我们需要修改 `BrickRenderer.js`，让它不再只是显示一块死板的积木，而是能根据一段文本（LDraw 格式）渲染出一组积木。

请在 VS Code 中打开 `BrickRenderer.js`，呼出 Copilot Chat 发送以下提示词：

#### 提示词 (Prompt 3)：

> Now that we have a single brick, let's make it dynamic. Please refactor `BrickRenderer.js` to:
> 
> 1. **Define a Mini-LDraw Parser:** Create a function that parses a simple LDraw-like string. Each line looks like: `1 [color] [x] [y] [z] [rot...] [part_type]`.
>     
>     - For now, only support `part_type` for "2x6" (which we built) and "2x2".
>         
>     - Dimensions for 2x2: Width=2, Height=1.2, Depth=2.
>         
> 2. **State Management:** The component should accept a `ldrawString` prop.
>     
> 3. **Rendering Logic:** Map through the parsed lines and render a `<mesh>` for each brick at the specified `[x, y, z]` coordinates with the specified `[color]`.
>     
> 4. **Example Data:** Inside the component, provide a default string that stacks a 2x2 brick on top of a 2x6 brick as a test case.
>     
> 5. **Refine Visuals:** Use `Edges` from `@react-three/drei` to add black outlines to each brick so they look more like real LEGO.
>     

---

### 任务 4：接入“AI 大脑” (OpenClaw / Claude 3.5)

现在你的前端已经具备了“渲染一组指令”的能力。接下来，你需要回到你的 **OpenClaw (Claude 3.5)** 窗口，把它当作你的**后端大脑**。

将以下 Prompt 发送给 Claude 3.5，让它为你生成第一个“作品”的代码：

#### 提示词 (Prompt 4 - 发给 Claude 3.5)：

> You are a LEGO Master Builder. I have a renderer that understands a simplified LDraw format:
> 
> `1 [color_hex] [x] [y] [z] [part_type]`
> 
> - `part_type` available: `2x6`, `2x2`.
>     
> - Brick Height is 1.2 units.
>     
> 
> **Task:** Please write a LDraw string to build a very simple "Letter T" or a "Small Robot" using only these two types of bricks. Ensure the coordinates `[x, y, z]` are correctly calculated so the bricks are touching/stacked without floating.
> 
> Give me only the raw text string.

---

### 任务 5：组合与交互

当 Claude 给了你那段字符串后，回到 VS Code：

1. 在 `index.js` 中添加一个 `useState` 来存储这段字符串。
    
2. 添加一个 `Textarea`（文本框），让你可以手动粘贴 Claude 生成的代码。
    
3. 将文本框的内容实时传给 `<BrickRenderer ldrawString={...} />`。
    

**你可以对 Copilot 说：**

> "In `index.js`, add a Tailwind-styled Textarea. Link its value to a state called `ldrawCode`. Pass this state to the `BrickRenderer`. This way, I can paste LDraw code from an AI and see the 3D model update immediately."

---

### 💡 当前进度的“Vibe”点拨：

你现在正处于 **“数据驱动”** 的转折点。一旦这个跑通，你就不再是在写代码画积木，而是在写**逻辑**来解释**指令**。

**下一个大动作预告：**

当你可以输入代码生成模型后，我们将加入 **“语音转指令”**。想象一下：你对着麦克风说“叠一个红色的十字”，Claude 生成代码，你的网页瞬间跳出 3D 模型。

第一阶段的 T 字型拼搭出来了吗？如果不齐或者飘在空中，把报错或现象贴给我，我帮你调优提示词！





完整的说下步骤：
1. 
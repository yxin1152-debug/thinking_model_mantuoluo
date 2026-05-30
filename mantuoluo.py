import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# 设置页面配置
st.set_page_config(
    page_title="曼陀罗工作思考法 Pro",
    page_icon="🎯",
    layout="wide"
)

# 注入自定义 CSS 增强网页视觉美感
st.markdown("""
<style>
    .grid-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
        padding: 20px;
        background-color: #f0f2f6;
        border-radius: 15px;
    }
    .stTextInput>div>div>input {
        text-align: center;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# 初始化数据
if 'mandala_data' not in st.session_state:
    st.session_state.mandala_data = {
        "core": "核心目标",
        "A": "维度 A", "B": "维度 B", "C": "维度 C",
        "D": "维度 D", "E": "维度 E", "F": "维度 F",
        "G": "维度 G", "H": "维度 H",
        "sub_grids": {k: [f"细节 {i + 1}" for i in range(8)] for k in "ABCDEFGH"}
    }

data = st.session_state.mandala_data

# 侧边栏：控制台
with st.sidebar:
    st.title("🎯 曼陀罗实验室")
    st.info("九宫格思考法（Mandala Chart）能帮助您将模糊的目标转化为具象的行动。")

    # 新增功能：样式自定义调节面板
    st.write("---")
    st.subheader("🎨 画布视觉样式调节")

    # 字体调节
    font_size = st.slider("字体大小 (px)", min_value=10, max_value=30, value=14, step=1)
    font_align = st.selectbox("字体对齐方式", options=["center", "left", "right"], index=0,
                              format_func=lambda x: {"center": "居中对齐", "left": "居左对齐", "right": "居右对齐"}[x])

    # 颜色调节
    core_bg_color = st.color_picker("🎯 核心格子背景色", value="#005088")
    outer_bg_color = st.color_picker("⬜ 周边格子背景色", value="#FFFFFF")

    st.write("---")
    st.subheader("🛠️ 数据导出")

    # 1. 导出表格
    df = pd.DataFrame({
        "维度": ["核心", "A", "B", "C", "D", "E", "F", "G", "H"],
        "内容": [data["core"], data["A"], data["B"], data["C"], data["D"], data["E"], data["F"], data["G"], data["H"]]
    })
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📂 导出 CSV 表格", csv, "mandala_plan.csv", "text/csv", use_container_width=True)


    # 2. 基于 Plotly 渲染的完美九宫格图片生成函数（已移除英文字母，加入样式控制）
    def generate_plotly_image():
        # 转换文本，防止字数太长不换行
        def wrap_text(text, length=8):
            if not text: return ""
            return "<br>".join([text[i:i + length] for i in range(0, len(text), length)])

        # 九宫格坐标与文本映射（已剔除原本的 label 属性）
        grid_layout = [
            {"x": 0, "y": 2, "text": wrap_text(data["A"]), "is_core": False},
            {"x": 1, "y": 2, "text": wrap_text(data["B"]), "is_core": False},
            {"x": 2, "y": 2, "text": wrap_text(data["C"]), "is_core": False},
            {"x": 0, "y": 1, "text": wrap_text(data["D"]), "is_core": False},
            {"x": 1, "y": 1, "text": wrap_text(data["core"]), "is_core": True},
            {"x": 2, "y": 1, "text": wrap_text(data["E"]), "is_core": False},
            {"x": 0, "y": 0, "text": wrap_text(data["F"]), "is_core": False},
            {"x": 1, "y": 0, "text": wrap_text(data["G"]), "is_core": False},
            {"x": 2, "y": 0, "text": wrap_text(data["H"]), "is_core": False},
        ]

        fig = go.Figure()

        for cell in grid_layout:
            # 动态绑定用户选择的背景色
            bg_color = core_bg_color if cell["is_core"] else outer_bg_color
            # 智能匹配文字颜色：核心格子默认配白字，外围格子配暗色字
            font_color = "#FFFFFF" if cell["is_core"] else "#333333"
            line_color = "#002b4d" if cell["is_core"] else "#d1d5db"

            # 绘制方格
            fig.add_shape(
                type="rect",
                x0=cell["x"], y0=cell["y"], x1=cell["x"] + 1, y1=cell["y"] + 1,
                fillcolor=bg_color,
                line=dict(color=line_color, width=3 if cell["is_core"] else 1.5)
            )

            # 配置对齐的 x 轴偏移锚点
            x_anchor = cell["x"] + 0.5
            if font_align == "left":
                x_anchor = cell["x"] + 0.08
            elif font_align == "right":
                x_anchor = cell["x"] + 0.92

            # 填充纯净文字 (动态应用字体大小与对齐方式)
            fig.add_annotation(
                x=x_anchor, y=cell["y"] + 0.5,
                text=cell["text"],
                showarrow=False,
                font=dict(color=font_color, size=font_size),
                align=font_align,
                xanchor=font_align
            )

        fig.update_layout(
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 3]),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 3]),
            margin=dict(l=10, r=10, t=10, b=10),
            width=600, height=600,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )

        # 将 plotly 转为静态图片字节流
        img_bytes = fig.to_image(format="png", width=800, height=800, engine="kaleido")
        return fig, img_bytes


    st.write("---")
    st.subheader("🖼️ 九宫格画布预览")

    # 动态渲染
    fig, img_data = generate_plotly_image()
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # 下载按钮
    st.download_button(
        label="📥 下载高清 PNG 图片",
        data=img_data,
        file_name="mandala_chart.png",
        mime="image/png",
        use_container_width=True
    )

# 主界面布局
st.title("💼 曼陀罗职场全景看板")
tabs = st.tabs(["🏗️ 核心九宫格拆解", "🔍 二级行动清单", "📊 全局数据总览"])

with tabs[0]:
    st.subheader("Step 1: 核心目标与八大维度")
    st.markdown('<div class="grid-container">', unsafe_allow_html=True)

    r1c1, r1c2, r1c3 = st.columns(3)
    r2c1, r2c2, r2c3 = st.columns(3)
    r3c1, r3c2, r3c3 = st.columns(3)

    with r1c1: data["A"] = st.text_input("维度 A", data["A"], key="v_A")
    with r1c2: data["B"] = st.text_input("维度 B", data["B"], key="v_B")
    with r1c3: data["C"] = st.text_input("维度 C", data["C"], key="v_C")

    with r2c1: data["D"] = st.text_input("维度 D", data["D"], key="v_D")
    with r2c2:
        st.markdown('<div style="margin-top:25px"></div>', unsafe_allow_html=True)
        data["core"] = st.text_input("🎯 核心目标", data["core"], key="v_core")
    with r2c3: data["E"] = st.text_input("维度 E", data["E"], key="v_E")

    with r3c1: data["F"] = st.text_input("维度 F", data["F"], key="v_F")
    with r3c2: data["G"] = st.text_input("维度 G", data["G"], key="v_G")
    with r3c3: data["H"] = st.text_input("维度 H", data["H"], key="v_H")

with tabs[1]:
    st.subheader("Step 2: 维度深挖行动项")
    selected = st.selectbox("选择要拆解的维度:", ["A", "B", "C", "D", "E", "F", "G", "H"],
                            format_func=lambda x: f"{x}: {data[x]}")

    cols = st.columns(4)
    for i in range(8):
        with cols[i % 4]:
            data["sub_grids"][selected][i] = st.text_input(f"行动 {i + 1}", data["sub_grids"][selected][i],
                                                           key=f"sub_{selected}_{i}")

with tabs[2]:
    st.subheader("全局行动对齐表")
    all_data = []
    for k in "ABCDEFGH":
        for idx, action in enumerate(data["sub_grids"][k]):
            all_data.append({"父维度": data[k], "序列": idx + 1, "执行动作": action})
    st.table(pd.DataFrame(all_data))

st.toast("数据已实时保存在 Session 中", icon="💾")

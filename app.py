
import streamlit as st
import config
import logging
# 导入我们现有的翻译逻辑
# 这里的 one_sentence_translate 是整个应用的核心，它负责加载模型和执行推理
from translate import one_sentence_translate

# 配置日志，方便我们在终端看到运行状态
logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s-%(message)s', level=logging.INFO)

def main():
    """
    Streamlit 应用的主入口函数。
    Streamlit 的运行方式是从上到下执行脚本，所以所有的界面元素都会按照代码顺序渲染。
    """
    
    # 1. 页面基础设置
    # set_page_config 必须是第一个调用的 Streamlit 命令
    st.set_page_config(
        page_title="Transformer 机器翻译",  # 浏览器标签页标题
        page_icon="🤖"                   # 浏览器标签页图标
    )

    # 2. 页面标题和简介
    st.title("🤖 Transformer 机器翻译演示")
    st.markdown("""
    欢迎使用这个基于 Transformer 的英汉翻译系统。
    
    **实现原理简述**:
    1.  **前端**: 使用 Streamlit 构建，负责接收输入和展示结果。
    2.  **后端**: 调用 Python 后端的 PyTorch 模型。
    3.  **模型**: 加载预训练的 Transformer 权重，使用 Beam Search 进行解码。
    """)

    # 3. 侧边栏配置显示
    # 使用 st.sidebar 可以将次要信息放在左侧，保持主界面整洁
    with st.sidebar:
        st.header("⚙️ 模型配置")
        # 这里直接读取 config.py 中的变量，实时展示当前模型的运行参数
        st.text(f"运行设备: {config.device}")
        st.text(f"最大序列长度: {config.max_len}")
        st.text(f"Beam Search 大小: {config.beam_size}")
        
        st.info("提示: 首次点击翻译时需要加载模型，可能会有几秒钟的延迟。")

    # 4. 主输入区域
    st.subheader("📝 输入英文")
    # text_area 提供多行文本输入框，height 参数调整高度
    input_text = st.text_area(
        label="在此输入您想要翻译的英文句子:",
        height=100,
        placeholder="例如: The government has implemented various policies."
    )

    # 5. 翻译按钮与逻辑
    # st.button 返回 True 当按钮被点击时
    if st.button("开始翻译 (Translate)", type="primary"):
        # 检查输入是否为空
        if input_text:
            try:
                # 6. 执行翻译
                # st.spinner 会显示一个加载转圈圈，提升用户体验
                with st.spinner("🚀 正在启动模型进行翻译，请稍候..."):
                    
                    # ---------------------------------------------------------
                    # 核心调用步骤
                    # 我们直接复用 translate.py 中的 one_sentence_translate 函数。
                    # 这样做的好处是完全不修改后端逻辑，前端只是一个"壳"。
                    # ---------------------------------------------------------
                    translation = one_sentence_translate(input_text)
                    
                # 7. 显示结果
                st.success("✅ 翻译完成！")
                
                st.markdown("### 中文翻译结果")
                # 使用 info 框以醒目的方式显示结果
                st.info(translation)
                
            except Exception as e:
                # 错误处理：如果后端报错，优雅地显示在前端
                st.error(f"❌ 翻译过程中发生错误。请检查后台日志。")
                st.code(str(e)) # 显示具体错误信息以便调试
                logging.error(f"Translation error: {e}")
        else:
            # 如果用户没输入就点了按钮，给出警告
            st.warning("⚠️ 请先输入需要翻译的英文句子。")

if __name__ == "__main__":
    # 确保 CUDA 设备设置正确，避免显存冲突
    import os
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    import warnings
    warnings.filterwarnings('ignore')
    
    main()

import os
import streamlit as st
from utils.grade_analysis import calculate_total_credits
from utils.pdf_processing import process_pdf_file
from utils.docx_processing import process_docx_file

def main():
    st.set_page_config(page_title="📄 成績單學分計算工具", layout="wide")
    st.title("📄 成績單學分計算工具")

    # 上傳區同時支援 PDF 和 DOCX
    st.write("請上傳 PDF（純表格）或 Word (.docx) 格式的成績單檔案。")
    uploaded_file = st.file_uploader(
        "選擇一個成績單檔案（支援 PDF, DOCX）",
        type=["pdf", "docx"]
    )
    if not uploaded_file:
        st.info("請先上傳檔案，以開始學分計算。")
        return

    # 根據副檔名分流
    filename = uploaded_file.name.lower()
    if filename.endswith(".pdf"):
        dfs = process_pdf_file(uploaded_file)
    elif filename.endswith(".docx"):
        dfs = process_docx_file(uploaded_file)
    else:
        st.error("不支援的檔案格式。")
        return

    # 計算總學分
    total_credits, passed, failed = calculate_total_credits(dfs)

    st.markdown("---")
    # 調整文字大小：總學分比「查詢結果」小一號，數字綠色稍大
    st.markdown(
        "<div style='font-size:20px;'>目前總學分: "
        f"<span style='font-size:24px; color:green;'>{total_credits:.2f}</span></div>",
        unsafe_allow_html=True
    )

    # 目標學分輸入與「還需學分」，數字紅色
    target = st.number_input(
        "目標學分 (例如 128)", min_value=0.0, value=128.0, step=1.0
    )
    diff = target - total_credits
    if diff > 0:
        st.markdown(
            "<div style='font-size:20px;'>還需 "
            f"<span style='color:red;'>{diff:.2f}</span> 學分</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<div style='font-size:20px;'>已超出 "
            f"<span style='color:red;'>{abs(diff):.2f}</span> 學分</div>",
            unsafe_allow_html=True
        )

    st.markdown("---")
    # 通過的課程列表
    st.markdown("### 📚 通過的課程列表")
    if passed:
        st.dataframe(passed, use_container_width=True)
    else:
        st.info("沒有找到任何通過的課程。")

    # 不及格的課程列表
    if failed:
        st.markdown("### ⚠️ 不及格的課程列表")
        st.dataframe(failed, use_container_width=True)

if __name__ == "__main__":
    main()

    # ---------------------------
    # 使用者回饋＆開發者資訊（固定顯示在最底部）
    # ---------------------------
    st.markdown("---")
    # 第一行：回饋連結
    st.markdown(
        """
        <div style="text-align:center; margin-top:1em; font-size:0.9em;">
            感謝您的使用，若您有相關修改建議或發生其他類型錯誤，
            <a href="https://forms.gle/146ReKXmuMZELbkR6" target="_blank">請點選此處</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # 第二行：開發者資訊
    st.markdown(
        """
        <div style="text-align:center; font-size:1.2em; margin-top:0.5em;">
            開發者：<a href="https://www.instagram.com/chiuuuuu11.7?igsh=MWRlc21zYW55dWZ5Yw==" target="_blank">Chu</a>
        </div>
        """,
        unsafe_allow_html=True,
    )





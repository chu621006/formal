import streamlit as st
from utils.pdf_processing import process_pdf_file
from utils.docx_processing import process_docx_file
from utils.grade_analysis import calculate_total_credits

def main():
    st.set_page_config(page_title="成績單學分計算工具", layout="wide")

    # 標題
    st.title("📄 成績單學分計算工具")

    # —— 取代原本的 Markdown 超連結 —— 
    # 改成下載按鈕，確保使用說明能正確打開
    with open("usage_guide.pdf", "rb") as f:
        pdf_bytes = f.read()
    st.download_button(
        label="📖 使用說明 (PDF)",
        data=pdf_bytes,
        file_name="使用說明.pdf",
        mime="application/pdf"
    )

    st.write("請上傳 PDF（純表格）或 Word（.docx）格式的成績單檔案。")
    uploaded_file = st.file_uploader(
        "選擇一個成績單檔案（支援 PDF, DOCX）", 
        type=["pdf","docx"]
    )

    if not uploaded_file:
        st.info("請先上傳檔案，以開始學分計算。")
    else:
        # 處理檔案
        if uploaded_file.name.lower().endswith(".pdf"):
            dfs = process_pdf_file(uploaded_file)
        else:
            dfs = process_docx_file(uploaded_file)

        total_credits, passed, failed = calculate_total_credits(dfs)

        st.markdown("---")
        st.markdown("## :white_check_mark: 查詢結果")
        st.markdown(f"<p style='font-size:32px; margin:4px 0;'>目前總學分: <strong>{total_credits:.2f}</strong></p>", unsafe_allow_html=True)

        target = st.number_input("目標學分 (例如：128)", min_value=0.0, value=128.0, step=1.0)
        diff = target - total_credits
        if diff > 0:
            st.markdown(f"<p style='font-size:24px;'>還需 <span style='color:red;'>{diff:.2f}</span> 學分</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='font-size:24px;'>已超出畢業學分 <span style='color:red;'>{abs(diff):.2f}</span> 學分</p>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 📚 通過的課程列表")
        if passed:
            df_pass = st.dataframe(passed, use_container_width=True)
            csv_pass = passed.to_csv(index=False, encoding='utf-8-sig')
            st.download_button("下載通過課程 CSV", csv_pass, "passed.csv", "text/csv")
        else:
            st.info("沒有找到任何通過的課程。")

        st.markdown("### ⚠️ 不及格的課程列表")
        if failed:
            df_fail = st.dataframe(failed, use_container_width=True)
            csv_fail = failed.to_csv(index=False, encoding='utf-8-sig')
            st.download_button("下載不及格課程 CSV", csv_fail, "failed.csv", "text/csv")
        else:
            st.info("沒有找到任何不及格的課程。")

    # 回饋與開發者區塊（置底）
    st.markdown("---")
    st.markdown(
        '<p>感謝您的使用，若您有相關修改建議或發生其他類型錯誤，'
        '<a href="https://forms.gle/33ihNWpJjS5cKLN67" target="_blank">請點選此處</a></p>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p>開發者：'
        '<a href="https://www.instagram.com/chiuuuuu11.7?igsh=MWRlc21zYW55dWZ5Yw==" target="_blank">Chu</a>'
        '</p>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()

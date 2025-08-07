import streamlit as st
from utils.pdf_processing import process_pdf_file
from utils.docx_processing import process_docx_file
from utils.grade_analysis import calculate_total_credits

st.set_page_config(page_title="成績單學分計算工具", layout="wide")

def main():
    # ===== HEADER =====
    st.title("📄 成績單學分計算工具")

    # 使用說明超連結
    st.markdown(
        '<p style="margin-top:-10px; margin-bottom:20px;">'
        '📖 <a href="usage_guide.pdf" target="_blank">使用說明 (PDF)</a></p>',
        unsafe_allow_html=True
    )

    st.write("請上傳 PDF（純表格）或 Word（.docx）格式的成績單檔案。")

    # ===== FILE UPLOADER =====
    uploaded_file = st.file_uploader(
        "選擇一個成績單檔案（支援 PDF, DOCX）",
        type=["pdf", "docx"],
    )

    if not uploaded_file:
        st.info("請先上傳檔案，以開始學分計算。")
    else:
        # 根據副檔名呼叫不同處理
        ext = uploaded_file.name.rsplit(".", 1)[-1].lower()
        if ext == "pdf":
            dfs = process_pdf_file(uploaded_file)
        else:
            dfs = process_docx_file(uploaded_file)

        # 計算
        total_credits, passed, failed = calculate_total_credits(dfs)

        # ===== RESULTS =====
        st.markdown("---")
        # 查詢結果標題
        st.markdown(
            """
            <div style="display:flex; align-items:center; gap:0.5rem;">
              <span style="font-size:2.5rem;">✅</span>
              <h2 style="margin:0;">查詢結果</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # 總學分
        st.markdown(
            f"""
            <p style="font-size:2.2rem; margin:0.2rem 0;">
              目前總學分：<span style="color:green; font-weight:bold;">{total_credits:.2f}</span>
            </p>
            """,
            unsafe_allow_html=True,
        )
        # 目標與還需
        target = st.number_input("目標學分 (例如 128)", min_value=0.0, value=128.0, step=1.0)
        remaining = max(0.0, target - total_credits)
        st.markdown(
            f"""
            <p style="font-size:2.2rem; margin:0.2rem 0;">
              還需 <span style="color:red; font-weight:bold;">{remaining:.2f}</span> 學分
            </p>
            """,
            unsafe_allow_html=True,
        )

        # 通過課程表
        st.markdown("---")
        st.markdown("📚 **通過的課程列表**")
        if passed:
            st.dataframe(passed, use_container_width=True)
        else:
            st.info("沒有找到任何通過的課程。")

        # 不及格課程表
        st.markdown("---")
        st.markdown("⚠️ **不及格的課程列表**")
        if failed:
            st.dataframe(failed, use_container_width=True)
        else:
            st.info("沒有找到任何不及格的課程。")

    # ===== FOOTER (永遠顯示) =====
    st.markdown("---")
    st.markdown(
        """
        <p style="text-align:center; margin:1rem 0;">
          感謝您的使用，若您有相關修改建議或發生其他類型錯誤，
          <a href="https://forms.gle/BUWL5cDjQXf16FQS8" target="_blank" style="text-decoration:none;">
            請點選此行
          </a>
        </p>
        <p style="text-align:center; margin:0.5rem 0;">
          開發者：<a href="https://www.instagram.com/chiuuuuu11.7?igsh=MWRlc21zYW55dWZ5Yw==" target="_blank" style="text-decoration:none;">
            Chu
          </a>
        </p>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()


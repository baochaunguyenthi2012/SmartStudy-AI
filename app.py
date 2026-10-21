import streamlit as st
from google import genai
from PIL import Image

st.set_page_config(page_title="FlashQuiz - Trợ lý Ôn thi", page_icon="⚡", layout="centered")

st.title("⚡ FlashQuiz: Trợ Lý Ôn Thi Siêu Tốc")
st.caption("Tự động đọc bài học từ Chữ hoặc Ảnh chụp vở/SGK để tạo Flashcard & Bài tập")

api_key = st.text_input("🔑 Nhập Gemini API Key của bạn:", type="password")

st.markdown("---")

input_option = st.radio("📸 Chọn hình thức nhập bài học:", ["Tải/Chụp Ảnh bài học", "Dán Văn Bản ghi chép"], horizontal=True)

image_input = None
text_input = ""

if input_option == "Tải/Chụp Ảnh bài học":
    uploaded_file = st.file_uploader("Upload hoặc Chụp ảnh trang vở/SGK của bạn:", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image_input = Image.open(uploaded_file)
        st.image(image_input, caption="Ảnh bài học đã tải lên", use_column_width=True)
else:
    text_input = st.text_area("📝 Dán nội dung bài học vào đây:", height=200, placeholder="Ví dụ: Dán đoạn văn Lịch sử, Địa lý, từ vựng...")

if st.button("🚀 Bắt đầu phân tích & Tạo bài ôn tập", type="primary"):
    if not api_key:
        st.error("⚠️ Vui lòng nhập Gemini API Key!")
    elif input_option == "Tải/Chụp Ảnh bài học" and not image_input:
        st.warning("⚠️ Vui lòng tải lên một bức ảnh bài học!")
    elif input_option == "Dán Văn Bản ghi chép" and not text_input.strip():
        st.warning("⚠️ Vui lòng dán nội dung văn bản bài học!")
    else:
        with st.spinner("AI đang đọc bài, tóm tắt và khởi tạo nội dung ôn tập..."):
            try:
                client = genai.Client(api_key=api_key)
                
                prompt = """
                Bạn là một trợ lý giáo dục xuất sắc. Hãy đọc kỹ nội dung (từ ảnh hoặc văn bản được cung cấp) và tạo ra:
                1. BẢN TÓM TẮT NGẮN GỌN (3-5 ý chính).
                2. BỘ FLASHCARD ÔN TẬP (3-5 thẻ dạng: Mặt trước -> Mặt sau).
                3. BÀI TẬP TRẮC NGHIỆM (3 câu hỏi A, B, C, D có đáp án và giải thích).
                """
                
                if input_option == "Tải/Chụp Ảnh bài học":
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=[image_input, prompt],
                    )
                else:
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=f"{prompt}\n\nNội dung bài học:\n{text_input}",
                    )
                
                st.success("✨ Phân tích và tạo nội dung thành công!")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"❌ Có lỗi xảy ra: {e}")

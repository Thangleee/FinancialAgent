# FinancialAgent

## Mô tả dự án
Dự án là một **FastAPI Agent** kết hợp **vnstock** và **Grok AI** để trả lời các câu hỏi về chứng khoán Việt Nam.  
Người dùng có thể truy vấn dữ liệu giá cổ phiếu (OHLCV), thông tin công ty, các công ty con, cổ đông, báo cáo tài chính, ...

## Tech stack
- Python 3.13
- FastAPI
- vnstock
- Grok AI (hoặc Google Gemini)
- Pandas, Numpy
- dotenv
- nest_asyncio
- uvicorn

## Test tự động
File test_questions.json: chứa câu hỏi và câu trả lời kỳ vọng
Run:
python test_agent.py

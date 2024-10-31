import os
import google.generativeai as genai
from google.api_core import retry
import logging

# 設置日誌紀錄
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class AIHelper:
    def __init__(self, api_key=None):
        try:
            if api_key is None:
                api_key = "AIzaSyBLgof_MXah0Sn8a1dWIG6w3GeDx1M84oU"

            genai.configure(api_key=api_key)
            
            self.generation_config = {
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            }
            
            # 使用 Gemini API 初始化模型
            self.model = genai.GenerativeModel(
                model_name="gemini-pro",
                generation_config=self.generation_config,
            )
            
            # 初始化聊天會話
            self.chat_session = self.model.start_chat(history=[])

            logger.info("Successfully initialized Gemini API")
        
        except Exception as e:
            logger.error(f"Failed to initialize Gemini API: {str(e)}")
            raise

    @retry.Retry(predicate=retry.if_exception_type(Exception))
    def get_response(self, question, regulations):
        try:
            logger.info(f"Preparing to send question to Gemini: {question[:100]}...")
            
            # 建立 prompt
            prompt = f"""
            請根據以下法規內容，回答使用者的問題：
            
            法規內容：
            {regulations}
            
            使用者問題：
            {question}
            
            請提供明確的答案，並標註引用的法條依據。
            """
            
            logger.debug(f"Built prompt: {prompt[:100]}...")

            # 發送 prompt 給模型並接收回覆
            response = self.chat_session.send_message(prompt)
            logger.info("Received response from Gemini")
            
            formatted_response = self._format_response(response.text)
            return formatted_response
        
        except Exception as e:
            logger.error(f"Error getting AI response: {str(e)}")
            raise

    def _format_response(self, response_text):
        """
        自定義的回應格式化方法，可以根據需求進行額外處理。
        """
        # 在這裡可以根據需求進行回應格式的修改
        return response_text

if __name__ == "__main__":
    # 這段代碼只會在直接執行此檔案時運行，用於測試
    helper = AIHelper()
    test_response = helper.get_response("測試問題", "測試法規")
    print(test_response)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import render
from .models import Regulation
from .gemini import AIHelper
import logging
import json

logger = logging.getLogger(__name__)

@api_view(['GET'])
def home(request):
    return render(request, 'api/home.html')

class QueryView(APIView):
    def __init__(self):
        super().__init__()
        try:
            self.ai_helper = AIHelper()
        except Exception as e:
            logger.error(f"Failed to initialize AIHelper: {str(e)}")
            self.ai_helper = None

    def post(self, request):
        logger.info("Received POST request to QueryView")
        try:
            # 記錄請求內容
            logger.info(f"Request data: {json.dumps(request.data)}")
            
            # 驗證請求數據
            user_question = request.data.get('question')
            if not user_question:
                logger.warning("No question provided in request")
                return Response({
                    'status': 'error',
                    'message': '請提供問題內容'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 檢查 AI Helper 初始化狀態
            if not self.ai_helper:
                logger.error("AIHelper not initialized")
                return Response({
                    'status': 'error',
                    'message': 'AI服務未正確初始化'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # 獲取相關法規
            regulations = Regulation.objects.all()
            regulations_text = " ".join([reg.content for reg in regulations])
            logger.info(f"Found {len(regulations)} regulations")
            
            # 獲取 AI 回應
            logger.info("Sending request to Gemini")
            answer = self.ai_helper.get_response(user_question, regulations_text)
            logger.info("Received response from Gemini")
            
            response_data = {
                'question': user_question,
                'answer': answer,
                'status': 'success'
            }
            
            logger.info("Sending successful response")
            return Response(response_data)
            
        except Exception as e:
            logger.error(f"Error in QueryView: {str(e)}", exc_info=True)
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

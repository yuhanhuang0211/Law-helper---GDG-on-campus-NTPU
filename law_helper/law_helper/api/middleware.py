import logging
import json
import traceback
from django.http import JsonResponse
from rest_framework import status
from datetime import datetime

logger = logging.getLogger(__name__)

class ErrorHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        """處理所有未捕獲的異常"""
        # 生成錯誤日誌
        error_details = {
            'timestamp': datetime.now().isoformat(),
            'path': request.path,
            'method': request.method,
            'error': str(exception),
            'traceback': traceback.format_exc()
        }

        # 如果是API請求，記錄請求數據
        if request.path.startswith('/api/'):
            try:
                if request.method in ['POST', 'PUT', 'PATCH']:
                    error_details['request_data'] = json.loads(request.body.decode('utf-8'))
                elif request.method == 'GET':
                    error_details['query_params'] = dict(request.GET)
            except Exception as e:
                error_details['request_data_parse_error'] = str(e)

        # 記錄詳細錯誤日誌
        logger.error(
            f"Unhandled exception in {request.path}",
            extra={'error_details': error_details},
            exc_info=True
        )

        # 對API請求返回JSON響應
        if request.path.startswith('/api/'):
            error_message = str(exception)
            if not error_message or error_message.lower() == 'none':
                error_message = "服務器內部錯誤"

            # 根據異常類型設置適當的狀態碼
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            if hasattr(exception, 'status_code'):
                status_code = exception.status_code

            return JsonResponse({
                'status': 'error',
                'message': error_message,
                'timestamp': datetime.now().isoformat(),
                'path': request.path
            }, status=status_code)

        # 對非API請求，返回None讓Django處理異常
        return None

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 請求開始時記錄
        if request.path.startswith('/api/'):
            request_details = {
                'timestamp': datetime.now().isoformat(),
                'path': request.path,
                'method': request.method,
                'user': str(request.user),
            }

            try:
                if request.method in ['POST', 'PUT', 'PATCH']:
                    request_details['request_data'] = json.loads(request.body.decode('utf-8'))
                elif request.method == 'GET':
                    request_details['query_params'] = dict(request.GET)
            except Exception as e:
                request_details['request_data_parse_error'] = str(e)

            logger.info(
                f"API Request: {request.method} {request.path}",
                extra={'request_details': request_details}
            )

        response = self.get_response(request)

        # 請求結束時記錄響應
        if request.path.startswith('/api/'):
            response_details = {
                'status_code': response.status_code,
                'path': request.path,
                'method': request.method,
                'processing_time': datetime.now().isoformat(),
            }

            log_level = logging.INFO if response.status_code < 400 else logging.WARNING
            logger.log(
                log_level,
                f"API Response: {response.status_code} {request.path}",
                extra={'response_details': response_details}
            )

        return response

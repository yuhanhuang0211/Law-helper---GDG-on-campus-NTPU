建立虛擬環境：python -m venv .venv
啟動虛擬環境：.venv\Scripts\activate
退出虛擬環境：deactivate

在新環境中安裝所有依賴（二擇一）：
1. pip install -r requirements.txt
2. pip install Django asgiref djangorestframework sqlparse tzdata google-generativeai google-ai-generativelanguage google-api-core google-api-python-client google-auth google-auth-httplib2 googleapis-common-protos requests httpx urllib3 httplib2 idna certifi charset-normalizer pywin32 pywinpty astroid debugpy django-debug-toolbar isort mccabe outcome pylint pylint-django pylint-plugin-utils pylance numpy pyarrow protobuf pydantic pydantic_core argon2-cffi argon2-cffi-bindings colorama tqdm platformdirs cachetools dill annotated-types grpcio grpcio-status packaging proto-plus pyasn1 pyasn1_modules pyparsing rsa six setuptools tomlkit typing_extensions uritemplate

啟動伺服器：
1. 只須電腦版時：python manage.py runserver
2. 需要行動版時：python manage.py runserver 0.0.0.0:8000

定義新模型後須依序執行：
1. python manage.py makemigrations
2. python manage.py migrate

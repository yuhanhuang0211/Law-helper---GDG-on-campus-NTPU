本專案為 GDG on campus NTPU 社團內部提案【北大法規問答小幫手】
所有程式碼內容禁止外部使用，以及任何商業用途

專案介紹：https://hackmd.io/@3v-hwftbTgCmaxgqssRrBg/HyciP7WZkg

#---

相關事前操作

虛擬環境：
1. 建立環境：python -m venv .venv
2. 啟動環境：.venv\Scripts\activate
3. 退出環境：deactivate

在新環境中安裝所有依賴（二擇一）：
1. pip install -r requirements.txt
2. pip install Django asgiref djangorestframework sqlparse tzdata google-generativeai google-ai-generativelanguage google-api-core google-api-python-client google-auth google-auth-httplib2 googleapis-common-protos requests httpx urllib3 httplib2 idna certifi charset-normalizer pywin32 pywinpty astroid debugpy django-debug-toolbar isort mccabe outcome pylint pylint-django pylint-plugin-utils pylance numpy pyarrow protobuf pydantic pydantic_core argon2-cffi argon2-cffi-bindings colorama tqdm platformdirs cachetools dill annotated-types grpcio grpcio-status packaging proto-plus pyasn1 pyasn1_modules pyparsing rsa six setuptools tomlkit typing_extensions uritemplate

啟動伺服器：
1. 只須電腦版時：python manage.py runserver
2. 需要行動版時：python manage.py runserver 0.0.0.0:8000

定義新模型後須依序執行：
1. python manage.py makemigrations
2. python manage.py migrate

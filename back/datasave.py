import json
from django.core.management import call_command
from io import StringIO

# Dumpdata 실행
output = StringIO()
call_command('dumpdata', stdout=output)

# 파일로 저장
with open('output.json', 'w', encoding='utf-8') as f:
    f.write(output.getvalue())

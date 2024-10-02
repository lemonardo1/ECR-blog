# Medical Problem: 환자의 증상 설명

이 부분은 자연어로 환자의 증상과 상황을 서술합니다.
예를 들어:
- 환자는 45세 남성입니다.
- 최근 2주간 피로감과 체중 감소를 겪었습니다.
- 혈액 검사 결과는 헤모글로빈 수치가 낮았습니다.

---

## Python Algorithm: 증상 및 데이터 처리

```python
# 필수 라이브러리 불러오기
import numpy as np
import pandas as pd

# 환자 데이터 입력
patient_data = {
    'age': 45,
    'symptoms': ['fatigue', 'weight loss'],
    'lab_results': {
        'hemoglobin': 9.0  # 정상 수치보다 낮음
    }
}

# 핵심 증상 확인
def check_symptoms(data):
    critical_symptoms = ['fatigue', 'weight loss']
    return all(symptom in data['symptoms'] for symptom in critical_symptoms)

# 혈액 검사 결과 분석
def analyze_lab_results(lab_results):
    if lab_results['hemoglobin'] < 12.0:
        return "Anemia suspected"
    return "Normal hemoglobin levels"

# 전체 알고리즘 실행
def medical_diagnosis(data):
    if check_symptoms(data):
        diagnosis = analyze_lab_results(data['lab_results'])
        return f"Diagnosis: {diagnosis}"
    return "No critical symptoms detected"

# 결과 출력
print(medical_diagnosis(patient_data))

```


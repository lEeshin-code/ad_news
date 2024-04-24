import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib

# 테스트 데이터셋 불러오기
test_data = pd.read_csv('test_data.csv')

# 실제 레이블
y_true = test_data['광고성 여부']

# 훈련된 모델 불러오기
model = joblib.load('교육개혁_model.pkl')

# 모델 예측
y_pred = model.predict(test_data['텍스트'])

# 모델 예측 결과를 테스트 데이터셋에 추가
test_data['예측된 광고성 여부'] = ['광고' if pred == 1 else '비광고' for pred in y_pred]

# 업데이트된 데이터를 CSV 파일로 저장
test_data.to_csv('updated_test_data.csv', index=False)

# 평가 지표 계산
accuracy = accuracy_score(y_true, y_pred)  # 정확도 계산
precision = precision_score(y_true, y_pred, pos_label='광고')  # 정밀도 계산
recall = recall_score(y_true, y_pred, pos_label='광고')  # 재현율 계산
f1 = f1_score(y_true, y_pred, pos_label='광고')  # F1 점수 계산

# 결과 출력
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)

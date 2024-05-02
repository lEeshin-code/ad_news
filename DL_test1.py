import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt

# 전처리된 데이터 로드
data_folder = "final_preprocessed_data"
subfolders = [folder for folder in os.listdir(data_folder) if os.path.isdir(os.path.join(data_folder, folder))]

# 평가 지표를 저장할 리스트 초기화
test_losses = []
test_accuracies = []
precisions = []
recalls = []
f1_scores = []

# 소분류 파일명을 읽어서 각각의 모델을 학습
for subfolder in subfolders:
    subfolder_path = os.path.join(data_folder, subfolder)
    files = [file for file in os.listdir(subfolder_path) if file.endswith(".csv")]

    for file in files:
        file_path = os.path.join(subfolder_path, file)
        data = pd.read_csv(file_path)

        # 입력 및 타깃 데이터 분리
        X = data.drop(columns=['광고성 여부'])  # 광고성 여부 열 제외
        y = data['광고성 여부']

        # 레이블 인코딩 (0과 1로 변환)
        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(y)

        # 훈련 및 테스트 세트로 데이터 분할
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # 딥러닝 모델 설계
        model = Sequential([
            Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
            Dropout(0.5),
            Dense(32, activation='relu'),
            Dropout(0.5),
            Dense(1, activation='sigmoid')
        ])

        # 모델 컴파일
        model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])

        # 모델 훈련
        history = model.fit(X_train, y_train, epochs=20, batch_size=32, validation_split=0.2, verbose=1)

        # 모델 저장
        model.save("ad_news_DL.h5")

        # 모델 불러오기
        loaded_model = load_model("ad_news_DL.h5")

        # 모델 평가
        loss, accuracy = loaded_model.evaluate(X_test, y_test, verbose=0)
        print(f"Test Loss: {loss}")
        print(f"Test Accuracy: {accuracy}")

        # 손실과 정확도 그래프
        # 손실 그래프
        plt.plot(history.history['loss'], label='Training Loss')
        plt.plot(history.history['val_loss'], label='Validation Loss')
        plt.title('Training and Validation Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend()
        plt.draw()
        plt.pause(2)  # 2초 동안 대기
        plt.close()

        # 정확도 그래프
        plt.plot(history.history['accuracy'], label='Training Accuracy')
        plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
        plt.title('Training and Validation Accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.legend()
        plt.draw()
        plt.pause(2)  # 2초 동안 대기
        plt.close()

        # 모델 평가 - 추가 평가 지표 계산
        y_pred_prob = loaded_model.predict(X_test)
        y_pred = (y_pred_prob > 0.5).astype(int)  # 확률이 0.5보다 크면 1로, 아니면 0으로 예측
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        # 평가 지표 저장
        test_losses.append(loss)
        test_accuracies.append(accuracy)
        precisions.append(precision)
        recalls.append(recall)
        f1_scores.append(f1)

# 평균 평가 지표 계산
avg_loss = sum(test_losses) / len(test_losses)
avg_accuracy = sum(test_accuracies) / len(test_accuracies)
avg_precision = sum(precisions) / len(precisions)
avg_recall = sum(recalls) / len(recalls)
avg_f1 = sum(f1_scores) / len(f1_scores)

# 평균 평가 지표 출력
print(f"Average Test Loss: {avg_loss}")
print(f"Average Test Accuracy: {avg_accuracy}")
print(f"Average Precision: {avg_precision}")
print(f"Average Recall: {avg_recall}")
print(f"Average F1 Score: {avg_f1}")

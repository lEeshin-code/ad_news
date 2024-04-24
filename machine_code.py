import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
import joblib

# NLTK 데이터 다운로드
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# 데이터 로드 함수 정의
def load_data(folder_path):
    data_frames = []
    file_names = os.listdir(folder_path)
    for file_name in file_names:
        file_path = os.path.join(folder_path, file_name)
        data_frames.append(pd.read_csv(file_path))
    return pd.concat(data_frames, ignore_index=True)

# 중분류 키워드 설정
categories = ["교육개혁", "노동시장의 변화", "디지털 전환", "미래산업기술전략", "사회통합", "신위험사회", "지방소멸,인구감소"]

# 데이터 전처리 함수 정의
def preprocess_data(text):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    
    # 소문자 변환
    text = text.lower()
    # 토큰화
    tokens = word_tokenize(text)
    # 불용어 제거 및 표제어 추출
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word.isalnum() and word not in stop_words]
    # 전처리된 텍스트 반환
    return ' '.join(tokens)

# 모델 학습 및 예측 함수 정의
def train_and_predict_model(category_keyword, original_data):
    # 데이터 병합
    merged_data = original_data.copy()
    
    # 데이터 전처리
    merged_data['preprocessed_text'] = merged_data['텍스트'].apply(preprocess_data)

    # 모델 학습
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_features = tfidf_vectorizer.fit_transform(merged_data['preprocessed_text'])
    labels = merged_data['광고성 여부'].fillna(0).astype(int)  # 결측값 처리 및 정수형 변환

    model = LogisticRegression()
    model.fit(tfidf_features, labels)

    # 모델 저장
    joblib.dump(model, f"{category_keyword}_model.pkl")

    # 새로운 데이터 예측
    def predict_advertisement(text):
        preprocessed_text = preprocess_data(text)
        feature = tfidf_vectorizer.transform([preprocessed_text])
        prediction = model.predict(feature)
        return "광고성 기사" if prediction[0] == 1 else "뉴스 기사"

    # 예측 결과 반환
    return predict_advertisement

# 데이터 로드
category_keyword = "교육개혁"
category_folder = f"plus_folder/{category_keyword}"
original_data = load_data(category_folder)

# 모델 학습 및 예측
predict_function = train_and_predict_model(category_keyword, original_data)

# 새로운 데이터로 예측
new_text = "새로운 뉴스 기사"
prediction = predict_function(new_text)
print(f"중분류 키워드 '{category_keyword}'에 대한 예측 결과: {prediction}")

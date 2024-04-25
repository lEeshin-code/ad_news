import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler

def preprocess_data(input_folders, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for category_folder in input_folders:
        category_folder_path = os.path.join(os.getcwd(), category_folder)
        if os.path.isdir(category_folder_path):
            for csv_file in os.listdir(category_folder_path):
                if csv_file.endswith(".csv"):
                    csv_file_path = os.path.join(category_folder_path, csv_file)
                    print(f"Processing file: {csv_file_path}")
                    csv_data = pd.read_csv(csv_file_path)
                    
                    # '본문_x' 열을 텍스트 데이터로 추출
                    ad_texts = csv_data['본문_x'].tolist()  # 수정된 부분
                    
                    # TF-IDF 벡터화
                    vectorizer = TfidfVectorizer(max_features=10000)
                    tfidf_matrix = vectorizer.fit_transform(ad_texts)

                    # 벡터화된 데이터를 DataFrame으로 변환
                    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())

                    # 결측치 처리
                    tfidf_df.fillna(0, inplace=True)

                    # 이상치 처리
                    scaler = StandardScaler()
                    scaled_features = scaler.fit_transform(tfidf_df.values)
                    tfidf_df = pd.DataFrame(scaled_features, columns=tfidf_df.columns)

                    # 전처리된 데이터 저장
                    output_subfolder = os.path.join(output_folder, category_folder)
                    if not os.path.exists(output_subfolder):
                        os.makedirs(output_subfolder)
                    output_file_path = os.path.join(output_subfolder, csv_file)
                    print(f"Saving processed file to: {output_file_path}")
                    tfidf_df.to_csv(output_file_path, index=False)

# 데이터 전처리
input_folders = [
    "교육개혁", 
    "노동시장의 변화", 
    "디지털 전환", 
    "미래산업기술전략", 
    "사회통합", 
    "신위험사회", 
    "지방소멸,인구감소"
]
output_folder = "final_preprocessed_data"
preprocess_data(input_folders, output_folder)

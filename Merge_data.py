import os
import pandas as pd

def merge_data(ad_data_folder, label_data_folder, output_folder):
    # 결과를 저장할 폴더 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 대칭되는 파일을 찾아 병합
    for ad_root, _, ad_files in os.walk(ad_data_folder):
        for ad_file in ad_files:
            if ad_file.endswith(".csv"):
                ad_file_path = os.path.join(ad_root, ad_file)
                ad_data = pd.read_csv(ad_file_path)
                
                # 레이블링된 데이터 파일 경로 생성
                label_file_path = os.path.join(label_data_folder, ad_file)
                
                # 대응되는 레이블링 파일이 존재하는지 확인
                if os.path.exists(label_file_path):
                    label_data = pd.read_csv(label_file_path)
                    
                    # '뉴스 식별자' 열의 데이터 유형 확인 및 일치시키기
                    if ad_data['뉴스 식별자'].dtype != label_data['뉴스 식별자'].dtype:
                        label_data['뉴스 식별자'] = label_data['뉴스 식별자'].astype(ad_data['뉴스 식별자'].dtype)
                    
                    # 뉴스 식별자 열로 병합
                    merged_data = pd.merge(ad_data, label_data, on='뉴스 식별자', how='inner')
                    
                    # 결과를 하나의 파일로 저장 (UTF-8 인코딩 사용)
                    output_file = os.path.join(output_folder, ad_file)
                    merged_data.to_csv(output_file, index=False, encoding='utf-8-sig')
                else:
                    print(f"레이블링된 데이터 파일이 존재하지 않습니다: {label_file_path}")

# 데이터 병합
ad_data_folder = "ad_data_standardized"  # 원본 데이터 폴더 경로
label_data_folder = "non_ad_data_standardized"  # 레이블링 데이터 폴더 경로
output_folder = "merged_data"  # 결과를 저장할 폴더 경로

merge_data(ad_data_folder, label_data_folder, output_folder)

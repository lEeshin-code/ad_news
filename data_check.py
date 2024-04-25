
#파일명 대응 확인 검사 
# import os

# def check_file_correspondence(folder1, folder2):
#     # 두 폴더 내의 파일명 목록 가져오기
#     files1 = os.listdir(folder1)
#     files2 = os.listdir(folder2)
    
#     # 대응되지 않는 파일명 찾기
#     unmatched_files = set(files1) ^ set(files2)
    
#     # 대응되지 않는 파일명과 해당 폴더 출력
#     print("대응되지 않는 파일명:")
#     for file in unmatched_files:
#         if file in files1:
#             print(f"{folder1} - {file}")
#         elif file in files2:
#             print(f"{file} - {folder2}")

# # 두 폴더 간의 파일명 대응 검사
# ad_data_folder = "ad_data_standardized"
# label_data_folder = "non_ad_data_standardized"
# check_file_correspondence(ad_data_folder, label_data_folder)

import os
import pandas as pd

def check_data_integrity_for_folders(folder_paths):
    for folder_path in folder_paths:
        print(f"{folder_path} 폴더의 데이터 구조 확인:")
        for root, _, files in os.walk(folder_path):
            for file_name in files:
                if file_name.endswith(".csv"):
                    file_path = os.path.join(root, file_name)
                    try:
                        df = pd.read_csv(file_path)
                        columns = df.columns.tolist()
                        dtypes = df.dtypes.tolist()
                        if len(set(dtypes)) > 1:
                            print(f"파일 '{file_name}'의 데이터 유형이 다릅니다.")
                        elif len(set(columns)) != len(columns):
                            print(f"파일 '{file_name}'에 중복된 열 이름이 있습니다.")
                        else:
                            print(f"파일 '{file_name}'의 데이터 구조가 일치합니다.")
                    except Exception as e:
                        print(f"파일 '{file_name}'을(를) 읽는 중 오류 발생: {e}")

# ad_data_standardized 폴더와 non_ad_data_standardized 폴더의 데이터 구조 확인
folder_paths = ["ad_data_standardized", "non_ad_data_standardized"]
check_data_integrity_for_folders(folder_paths)

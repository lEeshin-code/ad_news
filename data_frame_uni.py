import os
import pandas as pd

def find_most_common_datatype(input_folders):
    datatype_counts = {}
    
    # 모든 폴더의 파일을 합침
    all_files = []
    for folder in input_folders:
        folder_path = os.path.join(os.getcwd(), folder)
        csv_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(".csv")]
        all_files.extend(csv_files)
    
    # 파일 별로 데이터 형식 빈도수 계산
    for csv_file in all_files:
        try:
            # 파일 읽을 때 인코딩을 UTF-8로 고정
            df = pd.read_csv(csv_file, nrows=1, encoding='utf-8')  
            for col in df.columns:
                datatype = str(df[col].dtype)
                datatype_counts[datatype] = datatype_counts.get(datatype, 0) + 1
        except Exception as e:
            print(f"Error reading file {csv_file}: {e}")
    
    # 가장 많이 나타나는 데이터 형식 찾기
    most_common_datatype = max(datatype_counts, key=datatype_counts.get)
    return most_common_datatype

def unify_datatypes(input_folders, most_common_datatype):
    # 모든 폴더의 파일을 순회하며 데이터 형식 통일
    for folder in input_folders:
        folder_path = os.path.join(os.getcwd(), folder)
        csv_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(".csv")]
        
        # 폴더 내의 모든 파일에 대해 데이터 형식 통일
        for csv_file in csv_files:
            try:
                # 파일 읽을 때 인코딩을 UTF-8로 고정
                df = pd.read_csv(csv_file, encoding='utf-8')  
                for col in df.columns:
                    df[col] = df[col].astype(most_common_datatype)
                df.to_csv(csv_file, index=False, encoding='utf-8-sig')  # UTF-8로 저장
                print(f"File {csv_file} updated successfully.")
            except Exception as e:
                print(f"Error updating file {csv_file}: {e}")

def update_data_format():
    # 폴더 리스트 변경
    input_folders = [
        "ad_data_standardized", 
        "non_ad_data_standardized"
    ]
    
    most_common_datatype = find_most_common_datatype(input_folders)
    print(f"Most common datatype found: {most_common_datatype}")
    unify_datatypes(input_folders, most_common_datatype)

# 데이터 형식 일치화 함수 호출
update_data_format()

import os
import pandas as pd

# 폴더 경로 설정
folder_path = "plus_folder"  # 대상 폴더의 경로로 대체하세요.

# 폴더 내의 모든 CSV 파일을 탐색
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith('.csv'):
            file_path = os.path.join(root, file)
            print(f"파일 업데이트 중: {file_path}")
            
            # CSV 파일 읽어오기
            df = pd.read_csv(file_path)
            
            # "본문" 열을 "텍스트"로 변경
            if "본문" in df.columns:
                df["텍스트"] = df["본문"]
                df = df.drop(columns=["본문"])
                
                # 업데이트된 CSV 파일 저장
                df.to_csv(file_path, index=False, encoding='utf-8-sig')
                
                print(f"{file_path} 업데이트 완료")
            else:
                print(f"{file_path}에 '본문' 열이 존재하지 않습니다.")

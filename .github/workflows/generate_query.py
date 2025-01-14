import pandas as pd
import json
import argparse
import ipaddress
from datetime import datetime

## 指定された文字列が有効なIPアドレスかどうかを検証する
def is_valid_ip(ip):    
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def main():    
    # コマンドライン引数の定義
    parser = argparse.ArgumentParser(description="Parse a CSV file and generate a JSON query with valid IP addresses.")
    parser.add_argument(
        "-f", "--file", 
        type=str, 
        required=True, 
        help="Path to the input CSV file"
    )
    args = parser.parse_args()
    csv_file = args.file

    # CSVファイルの読み込み
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Error: {csv_file} not found.")
        exit(1)

    # ip_address列の存在を確認
    if "ip_address" not in df.columns:
        print("Error: The CSV file does not contain a column named 'ip_address'.")
        exit(1)

    # IPアドレスの取得とおフィルタリング
    ip_list = df["ip_address"].dropna().tolist()
    
    valid_ips = [ip for ip in ip_list if is_valid_ip(ip)]

    # 有効なIPアドレスが存在しない場合のエラー処理
    if not valid_ips:
        print("Error: No valid IP addresses found in the CSV file.")
        exit(1)

    # JSON形式のクエリを生成
    query = {
        "query": {
            "terms": {
                "ip": valid_ips
            }
        }
    }

    # 現在時刻を利用して、出力ファイル名を生成し、保存する
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"query_{current_time}.json"

    
    with open(output_file, "w") as f:
        json.dump(query, f, indent=2)

    print(f"Query generated and saved to {output_file}")

if __name__ == "__main__":
    main()

import os
import json

# Thư mục chứa các file json
src_folder = r"D:\ppg_project\Data\valid_data_resampled"

lengths = []  # lưu số điểm của từng file

for filename in os.listdir(src_folder):
    if filename.endswith(".json"):
        file_path = os.path.join(src_folder, filename)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            if "PPG" in data:
                length = len(data["PPG"])
                lengths.append(length)
                print(f"{filename}: {length} points")
            else:
                print(f"{filename}: ❌ No 'PPG' key")
        
        except Exception as e:
            print(f"⚠️ Error reading {filename}: {e}")

# --- Thống kê ---
if lengths:
    avg_len = sum(lengths) / len(lengths)
    print("\n📊 Statistics:")
    print(f"  - Total files: {len(lengths)}")
    print(f"  - Min length : {min(lengths)}")
    print(f"  - Max length : {max(lengths)}")
    print(f"  - Avg length : {avg_len:.2f}")

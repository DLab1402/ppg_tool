import os
import json
import numpy as np
from scipy.signal import resample

# Thư mục gốc chứa file json
src_folder = r"D:\ppg_project\Data\valid_data" 
# Thư mục mới để lưu file đã chuẩn hóa
dst_folder = r"D:\ppg_project\Data\valid_data_resampled"

# Độ dài chuẩn hóa mong muốn
target_len = 9000  

os.makedirs(dst_folder, exist_ok=True)

for filename in os.listdir(src_folder):
    if filename.endswith(".json"):
        file_path = os.path.join(src_folder, filename)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Nếu file có key "PPG"
            if "PPG" in data:
                signal = np.array(data["PPG"])

                # Resample về độ dài chuẩn
                signal_resampled = resample(signal, target_len)
                data["PPG"] = signal_resampled.tolist()

                # Lưu sang thư mục mới
                out_path = os.path.join(dst_folder, filename)
                with open(out_path, "w", encoding="utf-8") as f_out:
                    json.dump(data, f_out)

                print(f"✅ {filename}: {len(signal)} -> {len(signal_resampled)} points")
            else:
                print(f"❌ {filename} không có key 'PPG'")

        except Exception as e:
            print(f"⚠️ Error {filename}: {e}")

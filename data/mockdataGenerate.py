import csv
import random
from faker import Faker

# 初始化Faker，使用中文本地化
fake = Faker('zh_CN')

# 生成随机的患者数据
def generate_patient_data():
    name = fake.name()
    id_number = fake.ssn()
    blood_pressure = f"{random.randint(90, 140)}/{random.randint(60, 90)}"
    heart_rate = random.randint(60, 100)
    temperature = round(random.uniform(36.0, 37.5), 1)
    
    return {
        "姓名": name,
        "身份证号": id_number,
        "血压": blood_pressure,
        "心率": heart_rate,
        "体温": temperature
    }

# 生成指定数量的患者数据并保存为CSV文件
def generate_sample_data(num_patients, filename):
    data = [generate_patient_data() for _ in range(num_patients)]
    
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["姓名", "身份证号", "血压", "心率", "体温"])
        writer.writeheader()
        writer.writerows(data)

# 生成100条患者数据并保存
generate_sample_data(100, 'sample_patient_data.csv')

print("模拟患者数据已生成并保存到 sample_patient_data.csv 文件中。")
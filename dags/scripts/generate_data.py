import os
import json
import random
import uuid
from datetime import datetime, timedelta

def generate_mock_data(output_path, num_records=5000):
    os.makedirs(output_path, exist_ok=True)
    statuses = ['completed', 'pending', 'cancelled', 'refunded']
    data = []
    
    start_date = datetime.now() - timedelta(days=1)
    
    for _ in range(num_records):
        order_date = start_date + timedelta(seconds=random.randint(0, 86400))
        # Tạo lỗi logic cố ý: 1% dữ liệu có giá âm để test Data Quality
        price = random.uniform(10.0, 500.0)
        if random.random() < 0.01:
            price = -50.0
            
        record = {
            "order_id": str(uuid.uuid4()),
            "user_id": f"USER_{random.randint(1000, 9999)}",
            "order_date": order_date.strftime("%Y-%m-%d %H:%M:%S"),
            "product_id": f"PROD_{random.randint(100, 500)}",
            "quantity": random.randint(1, 5),
            "price": round(price, 2),
            "status": random.choice(statuses),
            "updated_at": (order_date + timedelta(minutes=random.randint(5, 60))).strftime("%Y-%m-%d %H:%M:%S")
        }
        data.append(record)
        
    file_name = f"orders_{datetime.now().strftime('%Y%m%d')}.json"
    full_str_path = os.path.join(output_path, file_name)
    
    with open(full_str_path, 'w') as f:
        json.dump(data, f, indent=4)
    print(f" Successfully generated {num_records} records at {full_str_path}")

if __name__ == "__main__":
    generate_mock_data("/opt/airflow/data/bronze")
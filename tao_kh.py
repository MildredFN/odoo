import io
import sys
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import csv
import random

# Danh sách họ
last_names = [
    "Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Võ", "Đỗ", 
    "Bùi", "Đặng", "Phan", "Cao", "Đinh", "Hồ", "Dương", "Mã", 
    "Vương", "Trương", "Quách", "Lý", "Tạ", "Văn", "Ôn", "Từ", "Trình"
]

# Danh sách tên đệm
middle_names = [
    "Văn", "Thị", "Quang", "Hồng", "Đức", "Kim", "Minh", "Ngọc", 
    "Bảo", "Thành", "Hải", "Tuấn", "Anh", "Quốc", "Thanh", "Huy", 
    "Trung", "Phú", "Đăng", "Mỹ", "Hoàng", "Phúc"
]

# Danh sách tên
first_names = [
    "Anh", "Bảo", "Chi", "Dũng", "Hà", "Hiếu", "Hương", "Khánh", 
    "Linh", "Long", "Mai", "Minh", "Nam", "Ngọc", "Phúc", "Quang", 
    "Thảo", "Thành", "Thuý", "Tín", "Trung", "Tú", "Tuyết", "Yến", "Khang", "An", 
    "Hạnh", "Dung", "Đức", "Hùng", "Kiên", "Lan", "Nhung", "Phương", 
    "Quân", "Thắm", "Tuấn", "Vân", "Xuân", "Yên", "Bình", "Đài"
]

# Danh sách tỉnh thành Việt Nam
provinces = [
    "Hà Nội", "Hồ Chí Minh", "Đà Nẵng", "Hải Phòng", "Cần Thơ", 
    "Hà Giang", "Cao Bằng", "Lào Cai", "Bắc Kạn", "Tuyên Quang", 
    "Lạng Sơn", "Thái Nguyên", "Yên Bái", "Sơn La", "Hòa Bình", 
    "Ninh Bình", "Thanh Hóa", "Nghệ An", "Hà Tĩnh", "Quảng Bình", 
    "Quảng Trị", "Thừa Thiên-Huế", "Quảng Nam", "Quảng Ngãi", 
    "Bình Định", "Phú Yên", "Khánh Hòa", "Ninh Thuận", "Bình Thuận", 
    "Kon Tum", "Gia Lai", "Đắk Lắk", "Đắk Nông", "Lâm Đồng", 
    "Bình Phước", "Tây Ninh", "Bình Dương", "Đồng Nai", "Bà Rịa-Vũng Tàu", 
    "Long An", "Tiền Giang", "Bến Tre", "Trà Vinh", "Vĩnh Long", 
    "Đồng Tháp", "An Giang", "Kiên Giang", "Cà Mau", "Hậu Giang", 
    "Sóc Trăng", "Bạc Liêu", "Bắc Ninh"
]

def generate_unique_customers(total_customers, batch_size, existing_names=None):
    """
    Tạo danh sách khách hàng duy nhất
    
    Args:
        total_customers (int): Tổng số khách hàng muốn tạo
        batch_size (int): Số khách hàng mỗi lần
        existing_names (set, optional): Tập tên đã sử dụng
    
    Returns:
        tuple: Danh sách khách hàng và tập tên đã sử dụng
    """
    if existing_names is None:
        existing_names = set()
    
    customers = []
    used_names = existing_names.copy()

    while len(customers) < batch_size:
        # Tạo tên
        last_name = random.choice(last_names)
        middle_name = random.choice(middle_names)
        first_name = random.choice(first_names)
        full_name = f"{last_name} {middle_name} {first_name}"
        
        # Kiểm tra tên không trùng
        if full_name not in used_names:
            used_names.add(full_name)
            
            customer = {
                'name': full_name,
                'is_company': False,
                'street': f"Số {random.randint(1, 999)} Đường {last_name}",
                'city': random.choice(provinces),
                'country_id': 'VN',  # Mã quốc gia Việt Nam
                'email': f"{full_name.lower().replace(' ', '.')}@example.com",
                'phone': f"0{random.randint(100000000, 999999999)}"
            }
            customers.append(customer)
        
        # Dừng nếu đã tạo đủ số lượng khách hàng
        if len(customers) + len(existing_names) >= total_customers:
            break

    return customers, used_names

def main():
    """
    Hàm chính để tạo và lưu danh sách khách hàng
    """
    # Cấu hình tạo dữ liệu
    total_customers = 2000  # Tổng số khách hàng muốn tạo
    batch_size = 1000  # Số khách hàng mỗi lần
    
    # Tạo thư mục để lưu các file
    os.makedirs('customer_batches', exist_ok=True)
    
    # Theo dõi tên đã sử dụng
    all_used_names = set()
    
    # Tạo từng batch
    for batch in range(0, total_customers, batch_size):
        # Tạo khách hàng cho batch này
        customers, batch_used_names = generate_unique_customers(
            total_customers, 
            batch_size, 
            existing_names=all_used_names
        )
        
        # Cập nhật tên đã sử dụng
        all_used_names.update(batch_used_names)
        
        # Tên file theo batch
        filename = f'customer_batches/odoo_customers_{batch//batch_size + 1}.csv'
        
        # Ghi ra file CSV
        keys = customers[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(customers)
        
        print(f"Đã tạo file {filename} với {len(customers)} khách hàng")

    # Kiểm tra tổng số khách hàng
    print(f"Tổng số khách hàng duy nhất: {len(all_used_names)}")

if __name__ == "__main__":
    main()
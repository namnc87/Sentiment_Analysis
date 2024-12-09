from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

product_data = []

def safe_get_text(locator):
    """Retrieve text from an element safely, returning an empty string if not found."""
    try:
        return wait.until(EC.presence_of_element_located(locator)).text
    except Exception:
        return ""

try:
    for page in range(1, 2):
        driver.get(f"https://hasaki.vn/danh-muc/nuoc-hoa-c103.html?p={page}")
        
        # Wait and get the list of products after each page load
        products = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ProductGridItem__itemOuter")))

        # for i in range(len(products)):
        for i in range(3):
            try:
                # Re-locate the element before clicking
                product = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ProductGridItem__itemOuter")))[i]
                product.click()
                
                ma_san_pham_full = safe_get_text((By.CSS_SELECTOR, ".item-sku.txt_color_1"))
                ma_san_pham = ma_san_pham_full.split(": ")[1] if ma_san_pham_full else ""

                ten_san_pham = safe_get_text((By.CLASS_NAME, "page-title-wrapper"))

                gia_ban_full = safe_get_text((By.ID, "product-final_price"))
                gia_ban = int(gia_ban_full.replace('.', '').replace(' ₫', '')) if gia_ban_full else 0

                gia_goc_full = safe_get_text((By.ID, "market_price"))
                gia_goc = int(gia_goc_full.replace('.', '').replace(' ₫', '')) if gia_goc_full else 0

                phan_loai = safe_get_text((By.XPATH, "//span[@class='txt_soluong selection']//span[@class='selection']"))

                mo_ta = safe_get_text((By.ID, "box_thongtinsanpham"))

                diem_trung_binh = safe_get_text((By.CSS_SELECTOR, ".txt_numer.txt_color_2"))

                # Add data to list
                product_data.append({
                    'ma_san_pham': ma_san_pham,
                    'ten_san_pham': ten_san_pham,
                    'gia_ban': gia_ban,
                    'gia_goc': gia_goc,
                    'phan_loai': phan_loai,
                    'mo_ta': mo_ta,
                    'diem_trung_binh': diem_trung_binh
                })

                # Go back to the previous page
                driver.back()
                
                # Wait for the page to reload
                wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ProductGridItem__itemOuter")))
                
            except Exception as e:
                print(f"Lỗi khi crawl sản phẩm: {e}")
                continue

except Exception as e:
    print(f"Lỗi: {e}")

finally:
    # Close browser
    driver.quit()
    
    # CSV file path
    csv_path = 'San_pham_Perfume_test.csv'

    # Create DataFrame and save to CSV
    df = pd.DataFrame(product_data)
    
    # Check and overwrite file if it exists
    df.to_csv(csv_path, index=False, mode='w', encoding='utf-8-sig')
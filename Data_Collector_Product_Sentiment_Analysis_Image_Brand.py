from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

product_data = []

def safe_get_text(locator):
    """Retrieve text from an element safely, returning an empty string if not found."""
    try:
        return wait.until(EC.presence_of_element_located(locator)).text
    except Exception:
        return ""

def click_element(element):
    """Click an element using JavaScript to avoid interception issues."""
    driver.execute_script("arguments[0].click();", element)

try:
    for page in range(1, 70):  # Adjust as needed
        driver.get(f"https://hasaki.vn/danh-muc/cham-soc-da-mat-c4.html?p={page}")
        products = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ProductGridItem__itemOuter")))

        for i in range(len(products)):
            try:
                products = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ProductGridItem__itemOuter")))
                product = products[i]
                
                # Scroll product into view
                driver.execute_script("arguments[0].scrollIntoView();", product)
                time.sleep(0.5)  # Optional: Small wait to ensure scrolling is complete

                try:
                    # Try to click using Selenium normally
                    product.click()
                except Exception as click_error:
                    print(f"Error clicking product normally: {click_error}")
                    # Use JavaScript click as fallback
                    click_element(product)

                # Add a sleep to allow dynamic content to load
                time.sleep(2)

                # Collect product information
                ma_san_pham = safe_get_text((By.CSS_SELECTOR, ".item-sku.txt_color_1")).split(": ")[1]
                ten_san_pham = safe_get_text((By.CLASS_NAME, "page-title-wrapper"))
                gia_ban_full = safe_get_text((By.ID, "product-final_price"))
                gia_ban = int(gia_ban_full.replace('.', '').replace(' ₫', '')) if gia_ban_full else 0
                gia_goc_full = safe_get_text((By.ID, "market_price"))
                gia_goc = int(gia_goc_full.replace('.', '').replace(' ₫', '')) if gia_goc_full else 0
                phan_loai = safe_get_text((By.XPATH, "//span[@class='txt_soluong selection']//span[@class='selection']"))
                mo_ta = safe_get_text((By.ID, "box_thongtinsanpham"))
                diem_trung_binh = safe_get_text((By.CSS_SELECTOR, ".txt_numer.txt_color_2"))

                image_element = wait.until(EC.presence_of_element_located((By.ID, "zoom_01")))
                hinh_anh = image_element.get_attribute('src')

                chi_tiet = driver.current_url 

                thuong_hieu = safe_get_text((By.CLASS_NAME, "title-brand"))
                tong_danh_gia = int(safe_get_text((By.ID, "click_scroll_review")).split()[0])
                tong_qa = int(safe_get_text((By.ID, "click_scroll_qa")).split()[0])

                product_data.append({
                    'ma_san_pham': ma_san_pham,
                    'ten_san_pham': ten_san_pham,
                    'gia_ban': gia_ban,
                    'gia_goc': gia_goc,
                    'phan_loai': phan_loai,
                    'mo_ta': mo_ta,
                    'diem_trung_binh': diem_trung_binh,
                    'hinh_anh': hinh_anh,
                    'chi_tiet': chi_tiet,
                    'thuong_hieu': thuong_hieu,
                    'tong_danh_gia': tong_danh_gia,
                    'tong_qa': tong_qa
                })

                # Go back and wait for elements to be present
                driver.back()
                wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ProductGridItem__itemOuter")))
                time.sleep(2)

            except Exception as e:
                print(f"Error while crawling product: {e}")
                continue

    print("Total products collected:", len(product_data))
    
    # Write to CSV
    if product_data:
        df = pd.DataFrame(product_data)
        df.to_csv('San_pham_Perfume_Link_Image_Brand.csv', index=False, mode='w', encoding='utf-8-sig')
        print("Data written to CSV.")
    else:
        print("No product data to write to CSV.")

except Exception as e:
    print(f"Main error: {e}")

finally:
    driver.quit()
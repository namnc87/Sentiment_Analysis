# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import pandas as pd
# import time

# driver = webdriver.Chrome()
# wait = WebDriverWait(driver, 10)

# product_data = []

# try:
#     for page in range(1, 11):  # Adjust as needed
#         driver.get(f"https://hasaki.vn/danh-muc/cham-soc-da-mat-c4.html?p={page}")
#         products = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ProductGridItem__itemOuter")))

#         for product in products:
#             try:
#                 # Scroll product into view
#                 driver.execute_script("arguments[0].scrollIntoView();", product)
#                 time.sleep(0.5)  # Optional: Small wait to ensure scrolling is complete

#                 # Extracting the image URL with additional error handling
#                 hinh_anh = product.find_element(By.CSS_SELECTOR, "img.img_thumb.lazy.loaded").get_attribute('src')


#                 # Extracting the detail page link
#                 chi_tiet = product.find_element(By.CLASS_NAME, "block_info_item_sp").get_attribute('href')

#                 # Extracting the product ID (data-id)
#                 ma_san_pham = product.find_element(By.CLASS_NAME, "block_info_item_sp").get_attribute('data-id')

#                 # Extracting the brand (data-brand)
#                 thuong_hieu = product.find_element(By.CLASS_NAME, "block_info_item_sp").get_attribute('data-brand')

#                 # Extracting catergory
#                 category = product.find_element(By.CLASS_NAME, "block_info_item_sp").get_attribute('data-category-name')

#                 # Add the data to the product_data list
#                 product_data.append({
#                     'ma_san_pham': ma_san_pham,
#                     'hinh_anh': hinh_anh,
#                     'chi_tiet': chi_tiet,
#                     'thuong_hieu': thuong_hieu,
#                     'dong_san_pham': category
#                 })

#             except Exception as e:
#                 print(f"Error while processing product: {e}")
#                 continue

#     print("Total products collected:", len(product_data))

#     # Write product data to CSV
#     if product_data:
#         df = pd.DataFrame(product_data)
#         df.to_csv('San_pham_Link_Image_Brand.csv', index=False, encoding='utf-8-sig')
#         print("Data written to CSV.")
#     else:
#         print("No product data to write to CSV.")

# except Exception as e:
#     print(f"Main error: {e}")

# finally:
#     driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

product_data = []

try:
    for page in range(51, 70):  # Adjust as needed
        driver.get(f"https://hasaki.vn/danh-muc/cham-soc-da-mat-c4.html?p={page}")
        products = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ProductGridItem__itemOuter")))

        for product in products:
            try:
                # Scroll product into view
                driver.execute_script("arguments[0].scrollIntoView();", product)
                time.sleep(0.5)  # Optional extra wait to ensure scrolling is complete

                # Attempt to extract the image URL with added error handling
                try:
                    hinh_anh = product.find_element(By.CSS_SELECTOR, "img.img_thumb").get_attribute('data-src')
                except Exception as img_error:
                    print(f"Image not found: {img_error}")
                    hinh_anh = None

                # Extracting the detail page link
                chi_tiet = product.find_element(By.CLASS_NAME, "block_info_item_sp").get_attribute('href')

                # Extracting the product ID (data-id)
                ma_san_pham = product.find_element(By.CLASS_NAME, "block_info_item_sp").get_attribute('data-id')

                # Extracting the brand (data-brand)
                thuong_hieu = product.find_element(By.CLASS_NAME, "block_info_item_sp").get_attribute('data-brand')

                # Extracting category
                category = product.find_element(By.CLASS_NAME, "block_info_item_sp").get_attribute('data-category-name')

                # Add the data to the product_data list
                product_data.append({
                    'ma_san_pham': ma_san_pham,
                    'hinh_anh': hinh_anh,
                    'chi_tiet': chi_tiet,
                    'thuong_hieu': thuong_hieu,
                    'dong_san_pham': category
                })

            except Exception as e:
                print(f"Error while processing product: {e}")
                continue

    print("Total products collected:", len(product_data))

    # Write product data to CSV
    if product_data:
        df = pd.DataFrame(product_data)
        df.to_csv('San_pham_Link_Image_Brand.csv', index=False, encoding='utf-8-sig')
        print("Data written to CSV.")
    else:
        print("No product data to write to CSV.")

except Exception as e:
    print(f"Main error: {e}")

finally:
    driver.quit()
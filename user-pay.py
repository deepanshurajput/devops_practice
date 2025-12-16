from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time


LOCATORS = {
    
    "email": (By.NAME, "email"),
    "pswd": (By.NAME, "password"),
    "sign-in-btn": (By.XPATH, "//button[text()='Sign In']"),
    "click-profile": (By.ID, "radix-_r_4_"),
    "dd-view-acc": (By.XPATH, "//span[text()='View Account']"),
    "sub-btn": (By.XPATH, "//button[text()='Subscription']"),
    "upgrd": (By.XPATH, "//button[text()='Upgrade to Monthly']"),
    "rzr-pay": (By.CLASS_NAME, "razorpay-checkout-frame"),
    "ph-number": (By.NAME, "contact"),
    "cont-btn": (By.XPATH, "//button[text()='Continue']"),
    "select-upi": (By.XPATH, '//span[text()="UPI"]'),
    "enter-id": (By.NAME, "vpa"),
    "pay_btn": (By.XPATH, "//button[text()='Verify and Pay']"),
}
email = input("enter email: ")
password = input("Enter password: ")
number = input("Enter Number:  ")
upi_id = input ("enter UPI ID:  ")
#EMAIL = "user12@auto.com"
#PASSWORD = "Auto@123"
#number = "9876543210"
#upi_id = "success@razorpay"

def login_with_selenium_multi_step():
    # Increased wait time for better stability
    WAIT_TIME = 15 
    
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, WAIT_TIME)

    try:
        
        driver.get("https://dev.interviewcopilot.in/")
        driver.maximize_window() 
        LOGIN_BUTTON_LOCATOR = (By.XPATH, "//*[text()='Login']")
        login_button = wait.until(EC.element_to_be_clickable(LOGIN_BUTTON_LOCATOR))
        login_button.click()

        # Email
        email_field = driver.find_element(*LOCATORS["email"])
        email_field.send_keys(email)
        
        # enter password
        password_field = driver.find_element(*LOCATORS["pswd"])
        password_field.send_keys(password)
        
        # Sign In
        signin = wait.until(EC.element_to_be_clickable(LOCATORS["sign-in-btn"]))
        signin.click()

        # Navigation steps
        profile = wait.until(EC.element_to_be_clickable(LOCATORS["click-profile"]))
        profile.click()

        view_acc = wait.until(EC.element_to_be_clickable(LOCATORS["dd-view-acc"]))
        view_acc.click()
        
        subscription = wait.until(EC.element_to_be_clickable(LOCATORS["sub-btn"]))
        subscription.click()

        # upgrade to monthly
        upgrade = wait.until(EC.element_to_be_clickable(LOCATORS["upgrd"]))
        upgrade.click()

        # Wait for Razorpay iframe to appear and switch context
        print("\nSwitching to Razorpay Iframe...")
        wait.until(EC.frame_to_be_available_and_switch_to_it(LOCATORS["rzr-pay"]))
        print("   -> Successfully switched to iframe.")

        # fill contact detail
        contact_detail = wait.until(EC.presence_of_element_located(LOCATORS["ph-number"]))
        contact_detail.send_keys(number)
        print(f"   -> Number entered: {number}.")
              
        time.sleep(2)

        #UPI entering
        upi_field = wait.until(EC.presence_of_element_located(LOCATORS["select-upi"]))
        upi_field.click()

        enter_upi_id = wait.until(EC.presence_of_element_located(LOCATORS["enter-id"]))
        enter_upi_id.send_keys(upi_id)

        vrfy_btn = wait.until(EC.element_to_be_clickable(LOCATORS["pay_btn"]))
        vrfy_btn.click()

        time.sleep(30)
        
        print("Waiting for Razorpay modal to close...")
        wait.until(EC.invisibility_of_element_located(LOCATORS["rzr-pay"]))
        print("Razorpay modal confirmed closed.")

        
        # --- Verification ---
        print(f"\nVerification:")
        print(f"Current URL after payment process: {driver.current_url}")
        
        if "dashboard" in driver.current_url or "home" in driver.current_url or "account" in driver.current_url:
            print("Process appears successful!")
        else:
            print("Process may have failed. Check the page content for errors.")

    except Exception as e:
        print(f"An error occurred during the login process: {e}")

    finally:
        # Close the browser
        print("Closing the browser in 5 seconds...")
        time.sleep(5)
        driver.quit()


if __name__ == "__main__":
    login_with_selenium_multi_step()
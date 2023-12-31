from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


class ResmapNavScrape:
    def __init__(self, browser):
        self.browser = browser


class ResmapNav(ResmapNavScrape):
    def __init__(self, browser):
        super().__init__(browser)

    def open_property(self, property):
        self.browser.click(By.XPATH, "//a[contains(., 'CHANGE PROPERTY')]")
        self.browser.click(By.XPATH, f"//a[contains(., '{property}')]")

    def nav_to_unit(self, property, unit):
        self.open_property(property)
        self.browser.send_keys(By.NAME, "search_input", unit + Keys.ENTER)
        try:
            self.browser.click(By.XPATH, f".//a[contains(text(), '{unit}')]")
        except NoSuchElementException:
            self.search_former_unit(unit)
            self.browser.click(By.XPATH, f".//a[contains(text(), '{unit}')]")

    def open_ledger(self, resident):
        current_resident_is_resident = self.browser.find_element(
            By.XPATH, f".//a[contains(text(), '{resident}')]"
        )
        if current_resident_is_resident:
            self.browser.click(By.XPATH, ".//a[text()='Ledger']")
        else:
            self.browser.click(
                By.XPATH, "//td[text()='List Former Residents']/following-sibling::td/a"
            )
            self.browser.click(By.XPATH, "(//a[text()='Ledger'])[last()]")

    def search_former_unit(self, unit):
        self.browser.click(By.ID, "former2")
        self.browser.send_keys(By.NAME, "spacenum", unit, True)

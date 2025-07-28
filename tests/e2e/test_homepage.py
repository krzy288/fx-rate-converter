import pytest
from dotenv import load_dotenv




@pytest.mark.playwright
def test_homepage(page, base_url):
    print(base_url)
    page.goto(base_url)  # Adjust the URL if necessary
    assert "FX" in page.title()  # Replace "FX" with the expected text in your title




def test_convert(page, base_url):
    print(base_url)
    page.goto(base_url)  # Adjust the URL if necessary
    page.fill('#from_currency', "PLN")
    page.fill('#to_currency', "EUR")
    page.fill('#amount', "100")
    page.click('#convert-btn')
    print(page.content()) 
    page.wait_for_selector('div.success', timeout=10000)
    assert "Rate" in page.locator('div.success').inner_text()
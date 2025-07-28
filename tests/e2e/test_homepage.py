import pytest
import re
from dotenv import load_dotenv


@pytest.mark.playwright
def test_homepage(page, base_url):
    """Test basic homepage loading and title"""
    print(base_url)
    page.goto(base_url)
    assert "FX" in page.title()


def test_page_structure_and_headings(page, base_url):
    """Test basic page structure and headings"""
    page.goto(base_url)
    
    # Verify main heading
    main_heading = page.locator('h1:has-text("FX Rate Converter")')
    assert main_heading.is_visible()
    
    # Verify section headings
    sections = [
        "Currency Converter",
        "Conversion History", 
        "Database Check",
        "The Most Important: Cat Photo"
    ]
    
    for section in sections:
        section_heading = page.locator(f'h2:has-text("{section}")')
        assert section_heading.is_visible()


def test_form_labels_and_elements(page, base_url):
    """Test form accessibility and labels"""
    page.goto(base_url)
    
    # Verify input labels
    assert page.locator('text="From Currency (e.g. USD):"').is_visible()
    assert page.locator('text="To Currency (e.g. EUR):"').is_visible()
    assert page.locator('text="Amount:"').is_visible()
    
    # Verify input fields exist and are accessible
    assert page.get_by_role('textbox', name='From Currency (e.g. USD):').is_visible()
    assert page.get_by_role('textbox', name='To Currency (e.g. EUR):').is_visible()
    assert page.get_by_role('spinbutton', name='Amount:').is_visible()
    assert page.get_by_role('button', name='Convert').is_visible()


def test_convert_usd_to_eur_basic(page, base_url):
    """Test basic currency conversion USD to EUR"""
    page.goto(base_url)
    
    # Fill form with correct selectors based on exploration
    page.get_by_role('textbox', name='From Currency (e.g. USD):').fill('USD')
    page.get_by_role('textbox', name='To Currency (e.g. EUR):').fill('EUR')
    page.get_by_role('spinbutton', name='Amount:').fill('100')
    
    # Click convert
    page.get_by_role('button', name='Convert').click()
    
    # Wait for conversion result to appear
    page.wait_for_timeout(2000)  # Give time for conversion to complete
    
    # Verify conversion result appears - check for success div
    conversion_result = page.locator('div.success')
    assert conversion_result.is_visible()
    
    # Verify the conversion text contains expected elements
    success_text = conversion_result.inner_text()
    assert '100' in success_text and 'USD' in success_text and 'EUR' in success_text
    assert 'Rate:' in success_text
    assert 'Date:' in success_text or '202' in success_text  # Check for date


def test_convert_usd_to_eur_with_pause(page, base_url):
    """Test basic currency conversion USD to EUR with pause for inspection"""
    page.goto(base_url)
    
    # Uncomment the line below when running with --visual to pause and inspect
    # page.pause()  # This will pause execution and let you inspect the page
    
    # Fill form with correct selectors based on exploration
    page.get_by_role('textbox', name='From Currency (e.g. USD):').fill('USD')
    page.get_by_role('textbox', name='To Currency (e.g. EUR):').fill('EUR')
    page.get_by_role('spinbutton', name='Amount:').fill('100')
    
    # Click convert
    page.get_by_role('button', name='Convert').click()
    
    # Wait for conversion result to appear
    page.wait_for_timeout(2000)  # Give time for conversion to complete
    
    # Uncomment to pause after conversion to see the result
    # page.pause()
    
    # Verify conversion result appears - check for success div
    conversion_result = page.locator('div.success')
    assert conversion_result.is_visible()
    
    # Verify the conversion text contains expected elements
    success_text = conversion_result.inner_text()
    assert '100' in success_text and 'USD' in success_text and 'EUR' in success_text
    assert 'Rate:' in success_text
    assert 'Date:' in success_text or '202' in success_text  # Check for date


def test_convert_usd_to_eur(page, base_url):
    """Test basic currency conversion USD to EUR"""
    page.goto(base_url)
    
    # Fill form with correct selectors based on exploration
    page.get_by_role('textbox', name='From Currency (e.g. USD):').fill('USD')
    page.get_by_role('textbox', name='To Currency (e.g. EUR):').fill('EUR')
    page.get_by_role('spinbutton', name='Amount:').fill('100')
    
    # Click convert
    page.get_by_role('button', name='Convert').click()
    
    # Wait for conversion result to appear
    page.wait_for_timeout(2000)  # Give time for conversion to complete
    
    # Verify conversion result appears - check for success div
    conversion_result = page.locator('div.success')
    assert conversion_result.is_visible()
    
    # Verify the conversion text contains expected elements
    success_text = conversion_result.inner_text()
    assert '100' in success_text and 'USD' in success_text and 'EUR' in success_text
    assert 'Rate:' in success_text
    assert 'Date:' in success_text or '202' in success_text  # Check for date


def test_currency_conversion_and_history_verification(page, base_url):
    """Test converting currency and verifying it appears in history with correct DB count"""
    page.goto(base_url)
    
    # Get initial DB count
    page.get_by_role('button', name='Check DB').click()
    page.wait_for_timeout(1000)  # Wait for DB response
    initial_count_text = page.locator('text=/Database connection successful/')
    initial_count_match = re.search(r'Rows: (\d+)', initial_count_text.inner_text())
    initial_count = int(initial_count_match.group(1)) if initial_count_match else 0

    # Perform currency conversion
    page.get_by_role('textbox', name='From Currency (e.g. USD):').fill('GBP')
    page.get_by_role('textbox', name='To Currency (e.g. EUR):').fill('USD')
    page.get_by_role('spinbutton', name='Amount:').fill('75')
    page.get_by_role('button', name='Convert').click()

    # Wait for conversion result
    page.wait_for_timeout(2000)

    # Verify conversion result appears - check for success div
    conversion_result = page.locator('div.success')
    assert conversion_result.is_visible()
    
    # Verify the conversion contains expected currencies
    success_text = conversion_result.inner_text()
    assert '75' in success_text and 'GBP' in success_text and 'USD' in success_text
    assert 'Rate:' in success_text

    # Show history and verify new conversion appears
    page.get_by_role('button', name='Show History').click()
    page.wait_for_timeout(1000)  # Wait for history to load
    page.get_by_role('button', name='Refresh').click()
    page.wait_for_timeout(1000)  # Wait for refresh

    # Verify the latest conversion appears in history table
    latest_row = page.locator('table tbody tr').first
    assert 'GBP' in latest_row.locator('td:nth-child(2)').inner_text()  # From
    assert 'USD' in latest_row.locator('td:nth-child(3)').inner_text()  # To
    assert '75' in latest_row.locator('td:nth-child(4)').inner_text()   # Amount

    # Verify DB count increased by 1
    page.get_by_role('button', name='Check DB').click()
    page.wait_for_timeout(1000)
    new_count_text = page.locator('text=/Database connection successful/')
    new_count_match = re.search(r'Rows: (\d+)', new_count_text.inner_text())
    new_count = int(new_count_match.group(1)) if new_count_match else 0
    assert new_count == initial_count + 1
@pytest.mark.parametrize("from_curr,to_curr,amount", [
    ("GBP", "USD", "50"),
    ("EUR", "PLN", "200"),
    ("USD", "EUR", "150")
])
def test_different_currency_conversions(page, base_url, from_curr, to_curr, amount):
    """Test various currency pair conversions"""
    page.goto(base_url)
    
    page.get_by_role('textbox', name='From Currency (e.g. USD):').fill(from_curr)
    page.get_by_role('textbox', name='To Currency (e.g. EUR):').fill(to_curr)
    page.get_by_role('spinbutton', name='Amount:').fill(amount)
    page.get_by_role('button', name='Convert').click()

    # Wait for conversion result
    page.wait_for_timeout(2000)

    # Verify result format - check for success div
    conversion_result = page.locator('div.success')
    assert conversion_result.is_visible()
    
    # Verify the conversion contains expected data
    success_text = conversion_result.inner_text()
    assert amount in success_text and from_curr in success_text and to_curr in success_text
    assert 'Rate:' in success_text
def test_history_display_and_refresh(page, base_url):
    """Test history display and refresh functionality"""
    page.goto(base_url)
    
    # Initially history table should not be visible
    assert not page.locator('table').is_visible()
    
    # Show history
    page.get_by_role('button', name='Show History').click()
    page.wait_for_timeout(1000)  # Wait for history to load
    assert page.locator('table').is_visible()
    assert page.get_by_role('button', name='Refresh').is_visible()

    # Verify table headers
    headers = ['ID', 'From', 'To', 'Amount', 'Rate', 'Converted', 'Date']
    for header in headers:
        assert page.locator(f'th:has-text("{header}")').is_visible()
def test_database_connection_check(page, base_url):
    """Test database connection functionality"""
    page.goto(base_url)
    
    page.get_by_role('button', name='Check DB').click()
    page.wait_for_timeout(1000)  # Wait for DB response

    # Verify successful connection message appears - more flexible pattern
    db_message = page.locator('text=/Database connection successful/')
    assert db_message.is_visible()
def test_db_count_consistency_with_history(page, base_url):
    """Test that DB row count matches history table entries"""
    page.goto(base_url)
    
    # Get DB count
    page.get_by_role('button', name='Check DB').click()
    page.wait_for_timeout(1000)
    count_text = page.locator('text=/Database connection successful/')
    count_match = re.search(r'Rows: (\d+)', count_text.inner_text())
    db_count = int(count_match.group(1)) if count_match else 0

    # Show history and count table rows
    page.get_by_role('button', name='Show History').click()
    page.wait_for_timeout(1000)  # Wait for history to load
    history_rows = page.locator('table tbody tr').count()

    # Counts should match
    assert db_count == history_rows
def test_cat_photo_display(page, base_url):
    """Test cat photo functionality"""
    page.goto(base_url)
    
    # Initially image should not be visible
    assert not page.locator('img[alt="FX Logo"]').is_visible()
    
    # Click to show image
    page.get_by_role('button', name='Click to Show Image').click()
    
    # Verify image appears
    assert page.locator('img[alt="FX Logo"]').is_visible()


def test_empty_fields_validation(page, base_url):
    """Test conversion with empty fields"""
    page.goto(base_url)
    
    # Try to convert with empty fields
    page.get_by_role('button', name='Convert').click()
    
    # Should handle gracefully - check what actually happens
    # Note: This test might need adjustment based on actual app behavior


def test_history_order_latest_first(page, base_url):
    """Test that history shows latest conversions first"""
    page.goto(base_url)
    
    # Perform multiple conversions
    conversions = [
        ("USD", "EUR", "100"),
        ("GBP", "USD", "50")
    ]
    
    conversion_ids = []
    for from_curr, to_curr, amount in conversions:
        page.get_by_role('textbox', name='From Currency (e.g. USD):').fill(from_curr)
        page.get_by_role('textbox', name='To Currency (e.g. EUR):').fill(to_curr)
        page.get_by_role('spinbutton', name='Amount:').fill(amount)
        page.get_by_role('button', name='Convert').click()
        page.wait_for_timeout(2000)  # Wait for conversion to complete

    # Show and refresh history
    page.get_by_role('button', name='Show History').click()
    page.wait_for_timeout(1000)
    page.get_by_role('button', name='Refresh').click()
    page.wait_for_timeout(1000)

    # Verify latest conversion (GBP->USD) is first row
    first_row = page.locator('table tbody tr').first
    assert 'GBP' in first_row.locator('td:nth-child(2)').inner_text()
    assert 'USD' in first_row.locator('td:nth-child(3)').inner_text()
def test_complete_user_journey(page, base_url):
    """Complete user journey test covering all major features"""
    page.goto(base_url)
    
    # 1. Check initial state
    assert page.locator('h1:has-text("FX Rate Converter")').is_visible()
    
    # 2. Get initial DB count
    page.get_by_role('button', name='Check DB').click()
    page.wait_for_timeout(1000)
    initial_db_text = page.locator('text=/Database connection successful/')
    initial_match = re.search(r'Rows: (\d+)', initial_db_text.inner_text())
    initial_count = int(initial_match.group(1)) if initial_match else 0

    # 3. Perform conversion
    page.get_by_role('textbox', name='From Currency (e.g. USD):').fill('EUR')
    page.get_by_role('textbox', name='To Currency (e.g. EUR):').fill('GBP')
    page.get_by_role('spinbutton', name='Amount:').fill('250')
    page.get_by_role('button', name='Convert').click()

    # Wait for conversion to complete
    page.wait_for_timeout(2000)

    # 4. Verify conversion result - check for success div
    conversion_result = page.locator('div.success')
    assert conversion_result.is_visible()
    
    # Verify the conversion contains expected data
    success_text = conversion_result.inner_text()
    assert '250' in success_text and 'EUR' in success_text and 'GBP' in success_text

    # 5. Check history
    page.get_by_role('button', name='Show History').click()
    page.wait_for_timeout(1000)
    page.get_by_role('button', name='Refresh').click()
    page.wait_for_timeout(1000)

    # 6. Verify new entry in history
    latest_row = page.locator('table tbody tr').first
    assert 'EUR' in latest_row.locator('td:nth-child(2)').inner_text()
    assert 'GBP' in latest_row.locator('td:nth-child(3)').inner_text()
    assert '250' in latest_row.locator('td:nth-child(4)').inner_text()

    # 7. Verify DB count increased
    page.get_by_role('button', name='Check DB').click()
    page.wait_for_timeout(1000)
    final_db_text = page.locator('text=/Database connection successful/')
    final_match = re.search(r'Rows: (\d+)', final_db_text.inner_text())
    final_count = int(final_match.group(1)) if final_match else 0
    assert final_count == initial_count + 1    # 8. Test cat photo feature
    page.get_by_role('button', name='Click to Show Image').click()
    assert page.locator('img[alt="FX Logo"]').is_visible()
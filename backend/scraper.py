from playwright.sync_api import sync_playwright

def scrape_listings(city="lahore", max_pages=5):
    listings = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for page_num in range(1, max_pages + 1):
            url = f"https://www.zameen.com/Homes/{city.title()}-1-{page_num}.html"
            print(f"Scraping URL: {url}")
            
            # Navigate to the URL and wait for the network to idle
            page.goto(url, wait_until="networkidle")

            # Wait for the first listing to ensure the page has loaded
            try:
                page.wait_for_selector('li[aria-label="Listing"]', timeout=60000)
            except Exception as e:
                print(f"Timeout or no listings found: {e}")
                continue

            # Select all listing elements
            listing_elements = page.query_selector_all('li[aria-label="Listing"]')
            for listing in listing_elements:
                try:
                    # Extract title
                    title_elem = listing.query_selector("h4")
                    title = title_elem.inner_text().strip() if title_elem else "No title"

                    # Extract image URL
                    picture_elem = listing.query_selector("picture source")
                    img_url = picture_elem.get_attribute("srcset") if picture_elem else "No image"

                    # Extract property link
                    link_elem = listing.query_selector('a[aria-label="Listing link"]')
                    link = link_elem.get_attribute("href") if link_elem else "No link"

                    # Append the data to the listings list
                    listings.append({
                        "title": title,
                        "img_url": img_url,
                        "link": f"https://www.zameen.com{link}" if link else "No link",
                    })

                except Exception as e:
                    print(f"Error extracting data from a listing: {e}")
                    continue

        browser.close()

    return listings

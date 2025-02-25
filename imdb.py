import csv
from playwright.sync_api import sync_playwright

# Fungsi utama untuk mengambil data dari IMDb menggunakan Playwright
def fetch_imdb_data():
    with sync_playwright() as p:
        # Menjalankan browser (Chromium)
        browser = p.chromium.launch(headless=True)  # Set headless=False jika ingin melihat browser
        page = browser.new_page()
        
        # URL yang akan diambil datanya
        url = "https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm"
        page.goto(url)
        
        # Tunggu beberapa detik untuk memastikan halaman dimuat sepenuhnya
        page.wait_for_timeout(3000)  # Tunggu selama 3 detik

        # Ambil semua kontainer film
        movie_containers = page.query_selector_all('td.titleColumn')

        # Membuka file CSV untuk menulis data
        with open('movie_data.csv', 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Title", "Year", "Rating"])

            # Ambil data untuk setiap film
            for container in movie_containers:
                # Ambil title (judul film)
                title = container.query_selector('a').inner_text().strip()

                # Ambil tahun film
                year = container.query_selector('span').inner_text().strip()

                # Mencari rating film
                rating_container = container.query_selector('.. >> following-sibling::td[@class="ratingColumn imdbRating"]')
                rating = rating_container.query_selector('strong').inner_text().strip() if rating_container else 'N/A'

                # Menulis data ke file CSV
                writer.writerow([title, year, rating])

        print("CSV file written successfully")

        # Menutup browser setelah selesai
        browser.close()

# Panggil fungsi utama
fetch_imdb_data()

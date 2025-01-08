# JioBasket

JioBasket is a Django-based web application that allows users to compare products and prices from two popular instant delivery platforms: **JioMart** and **BigBasket**. The goal is to help users find the best deals and make informed purchasing decisions quickly and easily.

---

## Features

- **Product Search**: Search for a specific product across both platforms.
- **Price Comparison**: View and compare product prices side-by-side.
- **Product Details**: Get additional product details, such as availability and brand.
- **Dynamic Updates**: Fetch and display live data from JioMart and BigBasket.
- **User-Friendly Interface**: Simple and intuitive design for a seamless user experience.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/JioBasket.git
   cd JioBasket
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate    # For Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   python manage.py migrate
   ```
5. Scrape data from JioMart and BigBasket:
   ```bash
   python manage.py jiomart_db_update
   pyton manage.py bigbasket_db_update
   ```
   
6. Start the development server:
   ```bash
   python manage.py runserver
   ```

7. Open the app in your browser:
   ```
   http://127.0.0.1:8000/
   ```

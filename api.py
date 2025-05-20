from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(filename='api.log', level=logging.INFO)

@app.route('/dailyverse', methods=['GET'])
def get_daily_verse():
    try:
        url = 'https://www.bible.com/verse-of-the-day'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        verse_text = soup.find('meta', property='og:description')['content'].strip()
        verse_image = soup.find('meta', property='og:image')['content']

        verse_data = {
            'verse': verse_text.replace('\u2019', "'").replace('\u2006', ' '),  # Clean Unicode
            'image': verse_image,
            'source': url
        }

        logging.info("Verse fetched successfully")
        return jsonify(verse_data)

    except (requests.RequestException, AttributeError, KeyError) as e:
        logging.error(f"Failed to fetch verse: {str(e)}")
        return jsonify({'error': 'Failed to fetch verse', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
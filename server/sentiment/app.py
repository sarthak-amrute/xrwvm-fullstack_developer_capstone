from flask import Flask, jsonify
from textblob import TextBlob

app = Flask(__name__)


@app.route('/analyze/<text>', methods=['GET'])
def analyze_review(text):
    """Analyze sentiment of review text"""
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        if polarity > 0.1:
            sentiment = 'positive'
        elif polarity < -0.1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        return jsonify({
            'sentiment': sentiment,
            'polarity': polarity,
            'text': text
        })
    except Exception as e:
        return jsonify({'sentiment': 'neutral', 'error': str(e)})


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

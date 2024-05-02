from flask import Flask, render_template, request
from summarization import summary_generator  # Import your summarization script

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    if request.method == 'POST':
        url = request.form['url']
        original_text, summary = summary_generator(url)  # Unpack the returned tuple
        original_word_count = len(original_text.split())
        summarized_word_count = len(summary.split())
        return render_template('summary.html', original_text=original_text, 
                               original_word_count=original_word_count, 
                               summary=summary, 
                               summarized_word_count=summarized_word_count)


if __name__ == '__main__':
    app.run(debug=True)

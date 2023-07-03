from typing import Union
from pathlib import Path
import json
from wordcloud import WordCloud
import arabic_reshaper
from bidi.algorithm import get_display
from hazm import WordTokenizer, Normalizer
from src.data import DATA_DIR


class ChatStatistics:
    """Generates chat statistics from a telegram chat json file
    """
    def __init__(self, chat_json: Union[str, Path]):
        """
        Args:
            chat_json (Union[str, Path]):path to telegram export json file
        """
        with open(chat_json, 'r') as f:
            self.chat_data = json.load(f)
            self.normalizer = Normalizer()
            with open(DATA_DIR / 'stopwords.txt') as f:
                stopwords = f.readlines()
                stopwords = list(map(str.strip, stopwords))
                self.stopwords = set(map(self.normalizer.normalize, stopwords))
                self.tokenize = WordTokenizer()

    def generate_word_cloud(self, output_dir):
        text_content = ''
        for msg in self.chat_data['messages']:
            if type(msg['text']) is str:
                tokens = self.tokenize.tokenize(msg['text'])
                tokens = list(filter(lambda item: item not in self.stopwords, tokens))
                text_content += f" {' '.join(tokens)}"

        # normalize, reshape, wordcloud
        text_content = self.normalizer.normalize(text_content)
        text = arabic_reshaper.reshape(text_content)
        text = get_display(text)
        wordcloud = WordCloud(width=200, height=300,
                              font_path=str(DATA_DIR / 'BHoma.ttf'),
                              background_color='white',
                              max_font_size=50).generate(text)

        wordcloud.to_file(str(Path(output_dir) / 'wordcloud.png'))


if __name__ == "__main__":
    chat_stats = ChatStatistics(chat_json=DATA_DIR / 'result.json')
    chat_stats.generate_word_cloud(output_dir=DATA_DIR)
    print('Done!')

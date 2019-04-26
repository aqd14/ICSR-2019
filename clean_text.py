import nltk
from nltk.stem import WordNetLemmatizer

words = set(nltk.corpus.words.words())

file_to_read = ['file-sharing-features.txt', 'file-manager-features.txt',
                'antivirus-features.txt', 'browser-features.txt']

file_to_write = ['clean-file-sharing-features.txt', 'clean-file-manager-features.txt', 'clean-antivirus-features.txt', 'clean-browser-features.txt']

wordnet_lemmatizer = WordNetLemmatizer() # lemmatization

for r, w in zip(file_to_read, file_to_write):
    with open(w, 'w', encoding='utf-8') as writer:
        with open(r) as reader:
            for line in reader:
                cleaned_line = ' '.join(wordnet_lemmatizer.lemmatize(w.lower()) for w in nltk.wordpunct_tokenize(line) if w.isalpha())  # w.lower() in words and
                if len(line.split()) >= 5:
                    writer.write('system should ' + cleaned_line + '\n')
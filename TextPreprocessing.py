import re
import nltk
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize



# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')


nlp = spacy.load("en_core_web_sm")
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
   
    text = text.lower()

    
    text = re.sub(r'\s+', ' ', text).strip()

    
    tokens = word_tokenize(text, preserve_line=True)

    
    filtered_tokens = [word for word in tokens if word not in stop_words]

    
    doc = nlp(" ".join(filtered_tokens))
    lemmatized = [token.lemma_ for token in doc if token.lemma_ != '-PRON-']

    return ' '.join(lemmatized)

# preprocessed_resumes = {}

# for filename, raw_text in resume_texts.items():
#     clean_text = preprocess_text(raw_text)
#     preprocessed_resumes[filename] = clean_text
#     print(f"Processed: {filename}")

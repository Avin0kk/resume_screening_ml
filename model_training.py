import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression

# Load dataset
df = pd.read_csv("data/resume.csv")

# Keep only required columns
df = df[['Resume_str', 'Category']]

# Text cleaning function
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text

# Apply cleaning
df['Resume_str'] = df['Resume_str'].apply(clean_text)

print("Text Cleaning Done ✅")

# Convert text to numbers using TF-IDF
tfidf = TfidfVectorizer(
    max_features=10000,
    stop_words='english',
    ngram_range=(1,2),
    min_df=2
)

X = tfidf.fit_transform(df['Resume_str'])
y = df['Category']

print("TF-IDF Conversion Done ✅")

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LogisticRegression(max_iter=2000)
model.fit(X_train, y_train)

print("Model Training Done ✅")

# Evaluate model
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print(f"Model Accuracy: {accuracy * 100:.2f}%")

import pickle

# Save model
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(tfidf, open("vectorizer.pkl", "wb"))

print("Model Saved Successfully ✅")
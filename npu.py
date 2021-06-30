import io
import nltk
import json
import random
import value
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split


with io.open('BOT_CONFIG.json', 'r', encoding='utf-8') as file:
    BOT_CONFIG = json.load(file)


def cleaner(text):
    """Функция очистки текста"""
    cleaned_text = ''
    for ch in text.lower():
        if ch in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz ':
            cleaned_text = cleaned_text + ch
    return cleaned_text


def match(text, example):
    """Функция сравнения текста (Допустимо совершать пару ошибок при написании"""
    return nltk.edit_distance(text, example) / len(example) < 0.4 if len(example) > 0 else False


def get_intent(text):
    """Функция определения смысла сообщения"""
    for intent in BOT_CONFIG['intents']:
        if 'examples' in BOT_CONFIG['intents'][intent]:
            for example in BOT_CONFIG['intents'][intent]['examples']:
                if match(cleaner(text), cleaner(example)):
                    return intent


# Обучение модели
X = []
y = []

for intent in BOT_CONFIG['intents']:
    if 'examples' in BOT_CONFIG['intents'][intent]:
        X += BOT_CONFIG['intents'][intent]['examples']
        y += [intent for i in range(len(BOT_CONFIG['intents'][intent]['examples']))]


# Создаем обучающую выборку для ML-модели
vectorizer = CountVectorizer(preprocessor=cleaner, ngram_range=(1, 4), stop_words=['а', 'и'])
vectorizer.fit(X)
X_vect = vectorizer.transform(X)
X_train_vect, X_test_vect, y_train, y_test = train_test_split(X_vect, y, test_size=0.1)
sgd = SGDClassifier()
sgd.fit(X_vect, y)


def get_intent_by_model(text):
    """Функция определяющая смысл текста с помощью ML-модели"""
    return sgd.predict(vectorizer.transform([text]))[0]


def botnpu(text):
    """Функция бота"""
    intent = get_intent(text)  # 1. попытаться понять намерение сравнением по Левинштейну
    if intent is None:
        intent = get_intent_by_model(text)  # 2. попытаться понять намерение с помощью ML-модели
    answer = random.choice(BOT_CONFIG['intents'][intent]['responses'])
    if answer == 'btc':
        answer = value.btc_usd()
    elif answer == 'USD':
        answer = value.check(answer)
    elif answer == "EUR":
        answer = value.check(answer)
    return answer


def help_bot():
    return BOT_CONFIG['intents']['options request']['responses'][0]
sgd.fit(X_train_vect, y_train)
print(sgd.score(X_test_vect, y_test))

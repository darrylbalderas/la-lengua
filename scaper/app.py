import requests
import spacy
import pandas as pd
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
import re
from bs4 import BeautifulSoup
from contractions import contractions_dict
import unicodedata

nlp = spacy.load("en", parse=True, tag=True, entity=True)


def text_processing(verse, tokenizer, stopword_set):
    verse = remove_accented_chars(verse)
    verse = expand_contradictions(verse)
    verse = re.sub(r"[^a-zA-Z\s]", " ", verse).strip()
    verse = simple_stemmer(verse)
    verse = remove_stopwords(verse, tokenizer, stopword_set)
    return verse


def remove_accented_chars(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')


def remove_stopwords(text, tokenizer, stopword_set, is_lower_case=False):
    tokens = [token.strip() for token in tokenizer.tokenize(text)]
    if is_lower_case:
        filtered_tokens = [token for token in tokens if token not in stopword_set]
    else:
        filtered_tokens = [token for token in tokens if token.lower() not in stopword_set]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text


def simple_stemmer(text):
    ps = nltk.porter.PorterStemmer()
    text = ' '.join([ps.stem(word) for word in text.split()])
    return text


def lemmatize_text(text):
    text = nlp(text)
    text = ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in text])
    return text


def remove_song_sections_tags(content):
    return re.sub(r"\[.*?\]", "", content)


def expand_match(contraction):
    match = contraction.group(0)
    first_char = match[0]
    expanded_contraction = (
        contractions_dict.get(match)
        if contractions_dict.get(match)
        else contractions_dict.get(match.lower())
    )
    if not expanded_contraction:
        return ""
    return first_char + expanded_contraction[1:]


def create_contractions_pattern():
    return re.compile(
        "({})".format("|".join(contractions_dict.keys())),
        flags=re.IGNORECASE | re.DOTALL,
    )


def expand_contradictions(text, contract_pattern=create_contractions_pattern()):
    expanded_text = contract_pattern.sub(expand_match, text)
    return re.sub("'", "", expanded_text)


def main():
    tokenizer = ToktokTokenizer()
    stopword_list = nltk.corpus.stopwords.words("english")
    stopword_list.remove("no")
    stopword_list.remove("not")
    stopword_set = set(stopword_list)
    df = pd.read_csv("lyrics_urls.csv", delimiter="\t")
    updated_lyrics = {'artist_name': [], 'song_title': [], 'lyrics':[]}
    for index, lyric_url in enumerate(df["lyric_url"]):
        print(lyric_url)
        headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
        }
        genius_lyric_page = requests.get(lyric_url, headers=headers)
        soup = BeautifulSoup(genius_lyric_page.text, "html.parser")
        genius_lyrics_content = soup.select("p")[0]
        verses = remove_song_sections_tags(genius_lyrics_content.text).split(
        "\n"
        )
        lyrics = [text_processing(verse, tokenizer, stopword_set) for verse in verses if verse != ""]
        updated_lyrics['artist_name'].append(df.loc[index]['artist'])
        updated_lyrics['song_title'].append(df.loc[index]['title'])
        updated_lyrics['lyrics'].append(lyrics)

    pd.DataFrame(updated_lyrics).to_csv('lyric_data.csv', sep="\t")


if __name__ == "__main__":
    main()

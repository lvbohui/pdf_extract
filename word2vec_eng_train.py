# !/usr/bin/env python
# -*-coding: utf-8 -*-
import gensim.models.word2vec as word2vec
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import time
import re


def train_save_model(file_name):
    sentences = word2vec.Text8Corpus(file_name)
    model = word2vec.Word2Vec(sentences, size=200)
    saved_model_name = "".join(file_name.split(".")[:-1]) + '.model'
    model.save(saved_model_name)
    return saved_model_name


def load_model(model_name):
    model = word2vec.Word2Vec.load(model_name)
    print(model.wv.most_similar("PDF"))
    # print(model.wv.__getitem__(["document"]))


def txt_clean(file_name):
    # 读取并分词
    with open(file_name, "r", encoding="utf-8") as text:
        words_list = word_tokenize("".join(text.readlines()))   # 英文分词工具
    print("start organizing data...")
    punctuation_list = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%', '-'",", '.',
                        '®', "\"", ":", "•", ]
    # 去停词和标点符号
    filter_words = [word for word in words_list
                    if not word in list(set(stopwords.words("english")))
                    and not word in punctuation_list]
    print("Remove stop words done")
    # 词形还原
    wordnet_le = WordNetLemmatizer()
    stem_words = [wordnet_le.lemmatize(word) for word in filter_words]
    print("Words Lemmatizer done")
    # 去低频词
    # all_stems = sum(stem_words, [])
    # stem_once = set(stem for stem in set(all_stems) if all_stems.count(stem) == 1)
    # text = [[stem for stem in text if stem not in stem_once] for text in stem_words]
    # print

    # 整理为字符串并输出
    cleaned_string = " ".join(stem_words)
    # 用正则表达式去除特殊字符
    pattern = ["\d", "\."]
    for i in range(len(pattern)):
        cleaned_string = re.sub(pattern[i], "", cleaned_string)
    out_cleaned_name = "".join(file_name.split(".")[:-1]) + '_' + 'cleaned.txt'  # 处理产生的文件名
    with open(out_cleaned_name, "w", encoding="utf-8") as writer:
        writer.write(cleaned_string)
    print("Done")
    return out_cleaned_name


if __name__ == "__main__":
    fn = "test_extracted.txt"
    cleaned_fn = "pdf_reference_17_extracted_cleaned.txt"
    model_name = "pdf_reference_17_extracted_cleaned.model"
    # time_start = time.time()
    cleaned_file = txt_clean(fn)
    # time_end = time.time()
    # print("Total time: ", (time_end-time_start))
    save_model = train_save_model(cleaned_file)
    load_model(save_model)

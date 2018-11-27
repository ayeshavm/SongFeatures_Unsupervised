#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 00:16:49 2018

This program computes for the Flesch-Kincaid Grade Level to be added as a feature in the song record.
@author: ayeshamendoza
"""
import spacy 
from textstat.textstat import textstatistics, easy_word_set, legacy_round
import re
import os

def break_sentences(text):
    nlp = spacy.load('en')
    doc = nlp(text)
    return doc.sents

def word_count(text):
    sentences = break_sentences(text)
    words = 0
    for sentence in sentences:
        words += len([token for token in sentence])
    return words

def sentence_count(text):
    sentences = break_sentences(text)
    out_sentences = list(sentences)
    return len(out_sentences)

def avg_sentence_length(text):
    words = word_count(text)
    sentences = sentence_count(text)
    average_sentence_length = float(words / sentences)
    return average_sentence_length

def syllables_count(word):
    return textstatistics().syllable_count(word)

def avg_syllables_per_word(text):
    syllable = syllables_count(text)
    words = word_count(text)
    ASPW = float(syllable) / float(words)
    return legacy_round(ASPW, 1)

def clean_lyrics_text(text):
    lyrics = re.sub(r'[\(\[].*?[\)\]]', '', text)
    #remove empty lines
    lyrics = os.linesep.join([s for s in lyrics.splitlines() if s])
    return lyrics

def flesch_kincaid_reading_grade(text):
    lyrics = clean_lyrics_text(text)
    FKRG = float(0.39 * (word_count(lyrics)/sentence_count(lyrics) ))  + \
           float(11.8 * avg_syllables_per_word(lyrics))
                    
                     
    return legacy_round(FKRG,2)


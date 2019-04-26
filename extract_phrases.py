# from textblob import TextBlob
import spacy
from spacy.symbols import nsubj, VERB
import pandas as pd
import os

nlp = spacy.load('en_core_web_sm')
stopwords = list(spacy.lang.en.stop_words.STOP_WORDS)

def extract_verbs_nps_pair(sentence):
    print(line)

    doc = nlp(sentence)

    verb_pos = [ix for ix, token in enumerate(doc) if token.pos == VERB and token.text != 'should']

    verbs = []
    objects = []
    additional_details = []

    # print('Noun chunks = ' + str(list(doc.noun_chunks)))
    noun_phrases = []

    for np in list(doc.noun_chunks):
        t = str(np)
        # if len(t.split()) > 1 and
        if t not in noun_phrases and t not in stopwords:
            noun_phrases.append(t)

    # At least two noun phrases with length > 1
    # one for object, other for additional info about object itself
    # if len(noun_phrases) < 2:
    #     return None, None, None

    # print("Noun phrases = " + str(noun_phrases))
    start = 0
    ix = 0
    while ix < len(noun_phrases):
        # for match in re.finditer(noun_phrases[ix], sentence):
        l = len(noun_phrases[ix])

        pos = sentence.find(noun_phrases[ix])
        doc2 = nlp(sentence[start:pos])
        for token in reversed(doc2):

            if token.pos == VERB and token.text != 'should':
                v = token.lemma_ # lemmatization
                obj = noun_phrases[ix].replace(token.text, '') # sometimes noun phrase contain verb
                if ix < len(noun_phrases) - 1:
                    detail = noun_phrases[ix+1]
                else:
                    detail = 'NA'

                verbs.append(v)
                objects.append(obj)
                additional_details.append(detail)

                print('VERB = {} --- OBJECT = {} --- DETAILS = {}'.format(v, obj, detail))

                ix += 1
                break
            start = pos + l
        ix += 1

    return verbs, objects, additional_details

    # return verbs_pair, nps_pair

    # extract all needed information to form a requirement from Rupp's boilerplate
    # verbs_pair = []
    # nps_pair = []
    # additional_details = []
    #
    # # print('Noun chunks = ' + str(list(doc.noun_chunks)))
    # noun_phrases = set([str(np.text) for np in list(doc.noun_chunks) if len(str(np).split()) > 1])
    # print("Noun phrases = " + str(noun_phrases))
    # start = 0
    # for np in noun_phrases:
    #     for match in re.finditer(np, sentence):
    #         doc2 = nlp(sentence[start:match.end()])
    #         for token in reversed(doc2):
    #             if token.pos == VERB:
    #                 print('VERB = {} and NOUN PHRASE = {}'.format(token.text, np))
    #                 verbs_pair.append(token.lemma_)
    #                 nps_pair.append(np.replace(token.text, ''))
    #                 break
    #         start = match.end()

    # return verbs_pair, nps_pair
    # for possible_subject in doc:
    #     if possible_subject.text in np for n
    #     if possible_subject.dep == nsubj and possible_subject.head.pos == VERB:
    #         verb_2_np[possible_subject.head] = noun_phrases
    # print(nps)


domains = ['antivirus', 'browser', 'file-sharing', 'file-manager']

for domain in domains:
    file_to_read = os.path.join(os.getcwd(), 'clean', 'clean-{}-features.txt'.format(domain))
    # file_to_write = 'annotated-{}-features.txt'.format(domain)

    sentence_ids = []
    verbs = []
    objects = []
    additional_details = []

    with open(file_to_read) as reader:
        for ix, line in enumerate(reader.readlines()):
            line = line.lower().replace('\n', '')

            # extract verbs followed by noun phrases
            # extract noun phrases
            vs, nps, dets = extract_verbs_nps_pair(line)

            if vs != None and nps != None and dets != None:
                sentence_ids.extend([ix] * len(vs))
                verbs.extend(vs)
                objects.extend(nps)
                additional_details.extend(dets)

                # convert noun phrases to single word with annotation
                # to prepare for word2vec training
                # for np in nps:
                #     if len(np.split()) > 1:  # check if noun phrase is multi-words
                #         # replace noun phrase with its one-word annotation.
                #         # for instance, 'hello world' becomes 'hello_world'
                #         line = line.replace(np, np.replace(' ', '_'))
                # writer.write(line + '\n')
    boilerplate_f = os.path.join(os.getcwd(), 'boilerplate', 'boilerplate-{}.csv'.format(domain))

    df = pd.DataFrame({
        'id': sentence_ids,
        'verb': verbs,
        'object': objects,
        'detail': additional_details
    })

    df.to_csv(boilerplate_f, index=False)
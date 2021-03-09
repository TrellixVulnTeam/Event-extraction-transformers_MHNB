from os import path
import json
import collections
import functools


def json_parse(fileobj, decoder=json.JSONDecoder(), buffersize=2048,
               delimiters=None):
    remainder = ''
    for chunk in iter(functools.partial(fileobj.read, buffersize), ''):
        remainder += chunk
        while remainder:
            try:
                stripped = remainder.strip(delimiters)
                result, index = decoder.raw_decode(stripped)
                yield result
                remainder = stripped[index:]
            except ValueError:
                # Not enough data to decode, read more
                break

output_dir = "./data/ace-event/processed-data/default-settings/json"
for fold in ["train", "dev", "test"]:
    g_convert = open(path.join(output_dir, fold + "_convert.json"), "w")
    with open(path.join(output_dir, fold + ".json"), "r") as g:
        for line in json_parse(g):
            #line = json.loads(line)
            sentences = line["sentences"]
            ner = line["ner"]
            relations = line["relations"]
            events = line["events"]
            sentence_start = line["sentence_start"]
            doc_key = line["doc_key"]

            assert len(sentence_start) == len(ner) == len(relations) == len(events) == len(sentence_start)

            for sentence, ner, relation, event, s_start in zip(sentences, ner, relations, events, sentence_start):
                # sentence_annotated = dict()
                sentence_annotated = collections.OrderedDict()
                sentence_annotated["sentence"] = sentence
                sentence_annotated["s_start"] = s_start
                sentence_annotated["ner"] = ner
                sentence_annotated["relation"] = relation
                sentence_annotated["event"] = event

                # if sentence_annotated["s_start"]>5:
                g_convert.write(json.dumps(sentence_annotated, default=int) + "\n")

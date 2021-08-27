import numpy as np
from loguru import logger

from app.models.skills import SkillResult

from . import key_replace, map_to_name, map_to_org_key, stopwords, syn_df
from .constants import (
    default_content_weights,
    skill_content_weights,
    skill_domain_weights,
    skill_weights,
)


def score_result(query: str, item: SkillResult, domain_probability: float = 0) -> float:
    rank_obj = Ranker(query, item)
    rank_obj.set_weights(skill_content_weights.get(item.skill, default_content_weights))
    raw_score = sum(rank_obj.rank_it().values())
    skill_weight = skill_weights.get(item.skill, 1)
    domain_weight = skill_domain_weights.get(item.skill, 1)
    final_score = np.tanh(
        (domain_probability * domain_weight) + (np.tanh(raw_score) * skill_weight)
    )
    logger.info(f"query: {query}, skill: {item.skill}, score: {final_score}")
    return final_score


class Ranker:
    def __init__(self, text, item: SkillResult):
        self.text = text
        self.item = item
        # if no weights are passed, equal weight is applied to both header and content for all skills.
        self.weights = {
            "heading_org": 1,
            "content_org": 1,
            "heading_aug": 1,
            "content_aug": 1,
        }

    def set_text(self, text):
        self.text = text

    def set_weights(self, ws):
        """
        Use this method to set new weights, should be dict
        {'heading_org':1,'content_org':1,'heading_aug':1,'content_aug':1}
        """
        self.weights = ws

    def get_text(self):
        return self.text

    def label_it(self, text):
        """
        label text using askoptum augmentation tool
        """
        phrase_set = set(text.split())
        keywords = [
            list(val.intersection(phrase_set))
            for key, val in map_to_org_key.items()
            if len(val.intersection(phrase_set)) == len(val)
        ]
        dict_vk_compatible = self.keyword_importance(keywords)
        new_keywords = [
            [map_to_name[k].lower()]
            for k, count in dict_vk_compatible.items()
            if k in map_to_name.keys()
        ]

        return new_keywords

    def clean_content(self, content):
        content = content.lower()
        for k, v in key_replace.items():
            content = content.replace(k, v)
        content = self.remove_stopwords(content.split())
        content_as_list = content.split(".")

        return content_as_list

    def clean_query(self, text):
        text = text.lower()
        for k, v in key_replace.items():
            text = text.replace(k, "")
        text.replace(".", "")

        text = text.lower()
        text_list = text.split()
        text = self.remove_stopwords(text_list)

        return text

    def remove_stopwords(self, text_list):
        new_list = []
        for t in text_list:
            if t not in stopwords:
                new_list.append(t)
        return " ".join(new_list)

    def aggregate_keys_from_query(self):
        """
        returns two list both of which have set types as elements
        augmented keys, original keys
        """
        text = self.get_text()
        original_keywords = self.label_it(text)  # labeling function keywords
        for t in text.split():
            original_keywords.append([t])  # using important words from the query itself

        original_keywords = np.concatenate(original_keywords)
        temp_words = []
        set_words = []

        for keyword in original_keywords:  # using UMLS to augment keywords
            if keyword in syn_df.keys():
                similar_words = syn_df[keyword]
            else:
                similar_words = [keyword]
            temp_words.append(list(similar_words))

        set_words = list(np.concatenate(temp_words))

        for (
            keyword
        ) in (
            original_keywords
        ):  # for 2 or more worded keywords, augment again on a word level
            key_list = keyword.split()
            if len(key_list) > 1:
                for k in key_list:
                    if k in syn_df.keys():
                        similar_word = syn_df[k]
                        for s in similar_word:
                            key2 = keyword.replace(k, s)
                            set_words.append(key2)

        augmented_keys = set(set_words) - set(original_keywords)
        sak = [set(w.split()) for w in augmented_keys]

        oak = [set(w.split()) for w in original_keywords]

        return sak, oak

    def keyword_importance(self, keywords):
        """
        get keyword counts -- this method is called by labelling function
        """
        dict_ = {}
        if len(keywords) >= 1:
            all_keys = np.concatenate(keywords)
        else:
            return {"": ""}

        for ks in keywords:
            final_key = "".join(sorted("".join(ks).lower()))
            count = 0
            for k in ks:
                if k in set(all_keys):
                    count += 1
            dict_[final_key] = count

        sorted_dict = dict(
            sorted(dict_.items(), key=lambda item: item[1], reverse=True)
        )

        return sorted_dict

    def rank_it(self):
        """
        This will call all appropriate methods in the class and return a dictionary
        containing weighted heading, content ranking scores for original and augmented keywords
        """

        title = self.item.title
        content = self.item.content
        text = self.get_text()

        content = self.clean_content(content)
        text = self.clean_query(text)
        self.set_text(text)

        title = title.lower()
        title.replace("-", "")

        sak, oak = self.aggregate_keys_from_query()

        weights = self.weights

        who = weights["heading_org"]
        wco = weights["content_org"]
        wha = weights["heading_aug"]
        wca = weights["content_aug"]

        # calculating content ranks for original keys
        nco = 0  # original key in content
        nca = 0  # augmented key in content
        for c in content:
            c_set = set(
                c.split()
            )  # heading splitted as a set to compare against set_keys found from query
            kco = [
                list(val.intersection(c_set))
                for val in oak
                if len(val) == len(list(val.intersection(c_set)))
            ]
            kca = [
                list(val.intersection(c_set))
                for val in sak
                if len(val) == len(list(val.intersection(c_set)))
            ]

            nco += wco * len(kco)
            nca += wca * len(kca)

        # calculating heading ranks original
        h_set = set(title.split())
        kho = [
            list(val.intersection(h_set))
            for val in sak
            if len(val) == len(list(val.intersection(h_set)))
        ]
        kha = [
            list(val.intersection(h_set))
            for val in oak
            if len(val) == len(list(val.intersection(h_set)))
        ]
        nho = who * len(kho)  # original key in heading
        nha = wha * len(kha)  # augmented key in heading

        dict_ = {"nho": nho, "nha": nha, "nco": nco, "nca": nco}

        return dict_

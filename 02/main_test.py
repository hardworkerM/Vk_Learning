import unittest
from unittest.mock import patch
import json
import random
import main
from faker import Faker


class MainTest(unittest.TestCase):

    def counter(self, doc: dict, fields, values):
        count = 0
        for field in fields:
            for value in doc[field]:
                if value in values:
                    count += 1
        return count

    def generate_fake_json(self):
        fake = Faker(locale="Ru_ru")
        fake_doc = {}
        field_list = []
        value_list = []
        for _ in range(5):
            field = str(fake.country())
            while field in field_list:
                field = str(fake.country())
            cur_value_list = []
            for _ in range(5):
                cur_value_list.append(fake.last_name())
            fake_doc[field] = ' '.join(cur_value_list)
            field_list.append(field)
            value_list.extend(cur_value_list)
        fake_json = json.dumps(fake_doc)
        return fake_json, fake_doc

    def generate_required_values(self, doc: dict):
        for field in doc:
            doc[field] = doc[field].split(' ')
        nb_field = random.randint(1, len(doc.keys()))
        required_field = random.sample(list(doc), nb_field)
        required_value = []
        for field in required_field:
            cur_nb_val = random.randint(1, len(doc[field]))
            required_value.extend(random.sample(doc[field], cur_nb_val))
        count = self.counter(doc, required_field, required_value)
        return required_field, required_value, count

    @patch('main.keyword_handler')
    def test_keywords_callback(self, mocker):
        fake_json, fake_doc = self.generate_fake_json()
        required_fields, keywords, count =\
            self.generate_required_values(fake_doc)
        main.parse_json(mocker, fake_json, required_fields, keywords)
        self.assertEqual(mocker.call_count, count)

    def test_except_call(self):
        json_str = '{1: "Word1 word2", "key2": "word2 word3"}'
        none_func = None
        with self.assertRaises(TypeError):
            main.parse_json(none_func, json_str, ['key1'], ['word2'])
        with self.assertRaises(TypeError):
            main.parse_json(main.keyword_handler,
                            json_str, ['key1'], ['word2'])
        json_str = '{"key1": "Word1 word2", "key2": 3}'
        with self.assertRaises(TypeError):
            main.parse_json(main.keyword_handler,
                            json_str, ['key2'], ['word2'])


if __name__ == '__main__':
    unittest.main()

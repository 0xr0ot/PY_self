# coding=utf-8
# if len(keywordList) > 500: exec(flashtext) else: exec(Regex)

from flashtext.keyword import KeywordProcessor

keyword_processor = KeywordProcessor()
keyword_processor.add_keyword('PyTorch')
keyword_processor.add_keyword(keyword='and', clean_name='or')
keywords_found = keyword_processor.extract_keywords('I love Python and PyTorch.')
print(keywords_found)
# ['or', 'PyTorch']

keyword_processor.add_keyword(keyword='Python', clean_name='Tensorflow')
new_sentence = keyword_processor.replace_keywords('I love Python and PyTorch.')
print(new_sentence)
# I love Tensorflow or PyTorch.

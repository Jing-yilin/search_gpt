from langchain.prompts.prompt import PromptTemplate

_search_langs_template = """You are an AI assistant that can help people search the keywords in different languages.
Here" are several examples:

Example 1:
Keywords input: ```Asian Game```
Target languages: ```["English", "Chinese (Simplified)", "German", "Japanese"]```
Keywords output: ```
Asian Game
亚运会
Asienspiele
アジア競技大会
```

Example 2:
Keywords input: ```特朗普被捕的原因是什么？```
Target languages: ```["Arabic (Jordan)", "English", "Chinese (Simplified)"]```
Keywords output: ```
سبب اعتقال ترامب هو ما؟
What is the reason for Trump's arrest?
特朗普被捕的原因是什么？
```

Example 3:
Keywords input: ```Apple의 개인 정보 유출 문제```
Target languages: ```["Esperanto", "Estonian", "Russian"]```
Keywords output: ```
La problemo de la eldonado de privataj informoj de Apple
Apple'i isikuandmete lekke probleem
Проблема утечки личных данных Apple
```

Now, please output the keywords in the target languages of the following questions:
```
Keywords input: ```{keywords}```
Target languages: ```{target_languages}```
Keywords output:
```
"""

SEARCH_LANGS_TEMPLATE = PromptTemplate.from_template(_search_langs_template)

_translate_template = """You are an AI assistant that can help people translate the sentence into the target language.
Here" are several examples:

Example 1:
Sentences input: 
```
核廃棄物、どうやって処分する？環境に与える影響と実態
原子力発電で使い終わった燃料はどうなるの？
```
Target language: ```Chinese (Simplified)```
Sentences output: 
```
核废料如何处理？
对环境的影响和实际情况
核燃料在核电站中使用后会怎样
```

Example 2:
Sentences input: 
```
Fukushima: What are the concerns over waste water release?
How risky is Japan's release of radioactive water from ...
```
Target language: ```Chinese (Simplified)```
Sentences output: 
```
福岛：释放废水有什么担忧？
日本释放放射性废水有多大风险?
```

Now, please translate the sentence into the target language of the following questions:
Sentences input: 
```
{sentences}
```
Target language: 
```
{target_language}
```
Sentences output:

"""

TRANSLATE_TEMPLATE = PromptTemplate.from_template(_translate_template)

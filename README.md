# PyDeepLX
A Python package for unlimited DeepL translation

## API Version
[OwO-Network/DeepLX](https://github.com/OwO-Network/DeepLX): Permanently free DeepL API written in Golang.

## Description
This is a Python package for DeepL translation, I didn't limit the number of translations in the code, if there is a `429` error, it means your IP has been blocked by DeepL temporarily, please don't request it frequently in a short time.

## Usage
### Install Package
```bash
pip install PyDeepLX
```
### Use in code
```python
from PyDeepLX import PyDeepLX
# By default, the source language is automatically recognized and translated into English without providing any alternative results.
PyDeepLX.translate("你好世界") # Return String

# Specify the source and target languages
PyDeepLX.translate("你好世界", "ZH", "EN") # Return String

# Need alternative results
PyDeepLX.translate("毫无疑问的", "ZH", "EN", True) # Return List: ['Without a doubt', 'No doubt']

# Print the results
PyDeepLX.translate("毫无疑问的", "ZH", "EN", True, True)

# Using proxy
PyDeepLX.translate(text="毫无疑问的", sourceLang="ZH", targetLang="EN", needAlternative=False, printResult=False, proxies="socks5://127.0.0.1:7890")
```

## PyPi
<a href="https://pypi.org/project/PyDeepLX/"><img src="https://img.shields.io/badge/Pypi-000000?style=for-the-badge&logo=pypi&logoColor=red" /></a>

## Author

**PyDeepLX** © [Vincent Young](https://github.com/missuo), Released under the [MIT](./LICENSE) License.<br>


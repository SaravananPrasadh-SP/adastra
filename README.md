<p align="center">
    <img height="100" alt="ad sepra" src="https://github.com/ottensa/ad-sepra/blob/main/docs/logo.png?raw=true" />
    <br>
    <i align="center">A Python Wrapper around the Starburst Enterprise REST API</i>
</p>

### Disclaimer
This is not part of the core Starburst product and is not covered by Starburst support agreements. 
It is a community developed set of scripts to make your life easier when working with Starburst APIs.

## Introduction
This Python package is a wrapper around the Starburst REST API as documented here:
https://docs.starburst.io/latest/api/index.htm

The motivation behind this project comes from the demand I see at customers to use the API for automation purposes.
However, working with the _raw_ API is not as easy as it might sound in theory.
Therefore, I wanted to try it out myself in a small project.
I quickly saw the need to wrap the actual API into easy to use functions and this library is the result.

## Installation
Releases are not yet available on PyPI, but you can install using pip nonetheless:

```shell
python -m pip install -U pip
python -m pip install -U pip install git+https://github.com/ottensa/ad-sepra.git
```

## Usage
ad sepra allows you to interact easily with the Starburst Enterprise REST API.
It abstracts away the complexity of the _raw_ API.

```python
from adsepra import SepClient, DataProductsApiClient
client = SepClient(host='https://sep.example.org', user='alice', token='Basic: xyz')
dpc = DataProductsApiClient(client=client)
dpc.list_data_products()
```

## Known issues and limitations
* This package does not claim to be complete and currently only focuses on Data Products.
* It has only be tested with Basic Authentication so far.

## Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create. 
Any contributions you make are greatly appreciated.

If you have a suggestion that would make this better, please fork the repo and create a pull request. 
You can also simply open an issue with the tag "enhancement". 
Don't forget to give the project a star! Thanks again!

## License
Distributed under the MIT License. See LICENSE for more information.

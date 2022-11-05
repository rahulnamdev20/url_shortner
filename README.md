# URL_Shortener

This is a simple flask app which takes an URL and shortens it. This shortened verion of the URL redirects to the user to the long URL. 

For each long URL given by the user the application generates an md5 hash which redirects to the long URL.


# How to use


## Installation
1. install the requirements using 

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install -r requirements.txt 
sudo snap install ngrok
```
You will also need to setup the auth key for the ngrox to work.
## Usage

```python
python3 app.py

```
open another window and start ngrok server using

```python
ngrok http 5000

```
Remember to change the ngrok url in the shorturl.html file inside the "h1" tag.
This is important as we do not have a proper subdomain at this moment.

Now hit the http://127.0.0.1:5000 in browser to access the application.



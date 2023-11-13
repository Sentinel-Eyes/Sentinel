# Sentinel: DeepFace-Powered Real-Time Criminal Facial Recognition System for Checkpoint Surveillance in REDACTED City

i recommend to use venv

or skip it
```
python install virtualenv

// might need to restart

virtualenv venv
```


Install packages
```
pip install -r requiremnts.txt
```



Launch Server:
```
python manage.py runserver
```


use ngrok for tunneling the localhost to access it anywhere in the world muahahha

```
ngrok http 8000
```

copy the forwarding url of ngrok


after restarting ngrok, url will be different. you can configure a static domain in ngrok. here is the code for hosting it using a static domain name

```
ngrok http --domain=climbing-smashing-grouse.ngrok-free.app 8000
```

this is specific to the hoster's account

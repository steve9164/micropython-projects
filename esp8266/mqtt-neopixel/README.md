# MQTT Neopixel

Controls neopixels via AWS IoT over MQTT. AWS IoT private keys stored separately

## Private keys

Private keys are stored separately. Obtain private keys by creating a "Thing" on AWS IoT and downloading the package for a Python project. Use contents of `{thingName}.cert.pem` and `{thingName}.private.key` as `cert` and `key`, or compress them to binary DER using the following to save memory:
```sh
openssl x509 -in thingName.cert.pem -out thingName.cert.der -outform DER
openssl rsa -in thingName.private.key -out thingName.key.der -outform DER
```
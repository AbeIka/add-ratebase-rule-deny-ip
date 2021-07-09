# Overview
Using AWS WAF rate-based rules, you can block connections from IP addresses that have had more than a threshold number of connections in 5 minutes. Once the connections settle down, they will be removed from the deny list and you will be able to connect to them. I created a Lambda that registers the IPs blocked by the rate-based rule into IP Sets and blocks connections all the time.

Lambda runs on Python 3.8, please use Event Bridge with a rate (1 minute) or something similar.

# Blog

# Lambda environment variable
IPSETRULE_ID
IPSETRULE_NAME
RATEBASERULE_NAME
WEBACL_ID
WEBACL_NAME
WEBACL_SCOPE
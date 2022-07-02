#!/bin/sh

curl -v 'http://ski66.ru/app/' \
	-H "Host: ski66.ru" \
	-H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0" \
	-H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8" \
	-H "Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3" \
	-H "Accept-Encoding: gzip, deflate" \
	-H "Connection: keep-alive" \
	-H "Upgrade-Insecure-Requests: 1" \
    -c ski66.ru-store-cookie.txt | gunzip -c | iconv -f cp1251 > data/index.html && \
grep -w 'data-id' data/index.html

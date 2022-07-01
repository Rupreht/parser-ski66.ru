#!/bin/sh

[ -z "$1" ] && echo "Enter $0 descr_id" && exit 64
curl -v -X POST "http://ski66.ru/app/cal" \
	-H "Accept: text/html, */*; q=0.01" \
	-H "Accept-Encoding: gzip, deflate" \
	-H "Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3" \
	-H "Connection: keep-alive" \
	-H "Content-Type: application/x-www-form-urlencoded; charset=UTF-8" \
	-H "Host: ski66.ru" \
	-H "Origin: http://ski66.ru" \
	-H "Referer: http://ski66.ru/app/" \
	-H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0" \
	-H "X-Requested-With: XMLHttpRequest" \
	-d "descr_id=$1" \
	-c ski66.ru-store-cookie.txt | gunzip -c | iconv -f cp1251 > data/get-descr-"$1".html

FROM python:3.10

WORKDIR /app

RUN apt-get update && \
	apt-get install -y --no-install-recommends git \
	&& addgroup --gid 1001 --system app \
	&& adduser --shell /bin/false \
		--disabled-password --uid 1001 --system --group app \
	&& git clone --branch dev --depth 1 https://github.com/Rupreht/parser-ski66.ru.git . \
	&& mkdir data && chown app:app data \
	&& pip install -U pip \
	&& pip install -r requirements.txt \
	&& crontab .crontab.file

COPY entrypoint.sh /

RUN chmod +x /entrypoint.sh

USER app

ENTRYPOINT ["/entrypoint.sh"]

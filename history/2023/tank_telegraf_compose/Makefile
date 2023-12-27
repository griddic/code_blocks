restart:
	docker compose stop -t 0
	docker compose rm -f
	docker compose build
	docker compose run tank yandex-tank -c /root/load.yaml
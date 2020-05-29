Если запустить selenium в докере, 
и при этом не монитровать ему `/dev/shm` 
как указано в документации 
https://github.com/SeleniumHQ/docker-selenium/tree/master/StandaloneChrome ,
то драйвер будет будет падать с ошибкой. 
Ошибка что-то вроде Page Broken.

Чтобы этого избежать, можно отключить `shm` на стороне клиента.
Важно, что для этого не обязательно конфигурировать образ selenuim.

```python
...
chrome_options.add_argument("--no-sandbox")  # <- Не уверен, что это тоже необходимо.
chrome_options.add_argument("--disable-dev-shm-usage")
# ^ без этого chrome будет быстрее, но будет падать в docker из-за нехватки памяти.
# Будет ошибка page crashed, или как-то так.

    with webdriver.Remote(selenium_origin + "/wd/hub", DesiredCapabilities.CHROME, options=chrome_options) as driver:
...
```

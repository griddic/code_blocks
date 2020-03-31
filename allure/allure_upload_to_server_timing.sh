#!/usr/bin/env bash
echo ++++ zipping archive ++++
echo $(date)
cd ./.allure
zip -q ./allure.zip *
echo $(du -hs ./allure.zip)
cd ..
echo $(date)
echo ==== archived ====
echo ++++ starting upload ++++
echo $(date)
curl -s -i -F file=@./.allure/allure.zip "http://allure.s.o3.ru/upload?group=OZON_TRAVEL&project=FLIGHT_API&version=CREATING_TESTS"
echo $(date)
echo ==== upload finished ====

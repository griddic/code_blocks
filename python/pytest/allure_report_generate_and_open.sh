#!/usr/bin/env bash
# assuming allure was run with  --alluredir allure_results
cp -r ./allure-report/history ./allure_results/
allure generate ./allure_results/ --clean
allure open -h localhost
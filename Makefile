reinstall_package:
	@pip uninstall -y dfake_api || :
	@pip install -e .

run_api:
	uvicorn api.dfake_api:app --reload

test_api_health:
	pytest \
	test/api/test_api.py::test_API_health --asyncio-mode=strict -W "ignore" 


test_api_predict:
	pytest \
	test/api/test_api.py::test_predict --asyncio-mode=strict -W "ignore" 

test_api_predict_hm:
	pytest \
	test/api/test_api.py::test_predict_hm --asyncio-mode=strict -W "ignore" 

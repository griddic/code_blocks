generate:
	docker pull namely/protoc-all
	docker run -v $(CURDIR):/defs namely/protoc-all -f hello.proto -l python
	docker run -v $(CURDIR):/defs namely/protoc-all -f admin.proto -l python


generate-proto:
	docker pull namely/protoc-all
	docker run -v $(CURDIR):/defs namely/protoc-all -f hello.proto -l python
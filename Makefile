TAG=enexa-extraction-module:1.0.0

build:
	docker build -t $(TAG) .

test:
	docker run --rm \
	-v $(PWD)/test-shared-dir:/shared \
	-e ENEXA_SHARED_DIRECTORY=/shared \
	-e ENEXA_META_DATA_ENDPOINT=http://admin:admin@fuseki:3030/test \
	-e ENEXA_SERVICE_URL=http://enexa:36321/ \
	-e ENEXA_WRITEABLE_DIRECTORY=/shared/experiment1 \
	-e ENEXA_MODULE_INSTANCE_IRI=http://example.org/moduleinstance-$$(date +%s) \
	--network enexa-utils_default \
	$(TAG)

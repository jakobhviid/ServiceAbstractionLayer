BUILDING_GENERATORS = $(wildcard src/generate-*-building)
BUILDING_MODELS  = $(patsubst src/generate-%-building,var/models/%.ttl,${BUILDING_GENERATORS})
BUILDING_RESULTS = $(patsubst src/generate-%-building,test/%,${BUILDING_GENERATORS})

TARGETS = \
	var/sal2instances.ttl \
	${BUILDING_MODELS} \
	${BUILDING_TARGETS} \



all: ${TARGETS} test

test: ${BUILDING_RESULTS}

clean:
	touch ${TARGETS}
	rm    ${TARGETS}

mrproper: clean
	touch dummy~ src/dummy~ var/dummy~ test/dummy~
	rm    *~     src/*~     var/*~     test/*~



var/models:
	mkdir var/models



var/sal2instances.ttl: src/inject-instances var/sal2.ttl
	./src/inject-instances var/sal2.ttl var/sal2instances.ttl

# generic rule for generating building models
${BUILDING_MODELS}: var/models/%.ttl: src/generate-%-building src/shared.py
	./$< $@

# generic rule for processing sparql files
${BUILDING_RESULTS}: test/%: var/models/%.ttl src/query-model var/schema.ttl
	./src/query-model var/schema.ttl var/Brick.ttl $< var/queries/ $@/ 100


# Service Abstraction Layer

The SAL is an ontology created with the purpose of describing information exposed by services. The intention of the ontology is to create a layer in between of services, so a service depends on information, and not services. This enables a higher level of decoupling between services. The above also enables multiple services to expose the same type of information, thereby allowing for multiple pathways to information, and enabling developers to create robust high availability applications.

This ontology was developed for the Building Operating System (BOS) space (and uses Brick), but could with few adaptions be generalized.

The SAL was developed as a part of the FlexReStore research project at the University of Southern Denmark.

## Dependencies

- `python3.5` Python Interpreter
- `python3-rdflib` [RDFLib](https://github.com/RDFLib/rdflib) python module
- `make` Make build system

## Building Ontology

```shell
make var/sali.ttl
```

## Building Model

```shell
make var/defaultbuilding.ttl
```

## Executing Tests

```shell
make test
```

## Doing Everything

```shell
make
```

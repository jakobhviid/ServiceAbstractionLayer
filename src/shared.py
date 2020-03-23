import rdflib
from rdflib import Literal

counter = 0

###############################################################################
############################################################### primitives ####

def generate_id ():
    global counter
    
    count = counter
    counter += 1
    return count

def add_instance (i, c):
    g.add( (i, RDF['type'], c) )

def add_object_property(obj, pred, sub):
    g.add( (obj, pred, sub) )

def add_data_property(obj, pred, sub):
    g.add( (obj, pred, Literal(str(sub))) )

###############################################################################
################################################################## classes ####

def construct_organization (name):
    name = name.replace(' ', '_')
    organization = DEFAULT['organization/%s' % name]
    add_instance(organization, SCHEMA['Organization'])
    add_data_property(organization, SCHEMA['legalName'], name)
    return organization

def construct_outdoors ():
    outdoors = DEFAULT['outdoors']
    add_instance(outdoors, BRICK['Outdoors'])
    g.add( (BRICK['Outdoors'], RDFS['subClassOf'], BRICK['Location']) )
    add_data_property(outdoors, BRICK['label'], 'outdoors')
    return outdoors

def construct_building (name):
    name = name.replace(' ', '_')
    building = DEFAULT['buildings/%s' % name]
    add_instance(building, BRICK['Building'])
    add_data_property(building, BRICK['label'], name)
    return building

def construct_room (name):
    name = name.replace(' ', '_')
    room = DEFAULT['buildings/%s' % name]
    add_instance(room, BRICK['Room'])
    add_data_property(room, BRICK['label'], name)
    return room

def construct_service (name):
    name = name.replace(' ', '_')
    service = DEFAULT['services/%s' % name]
    add_instance(service, SAL['Service'])
    add_data_property(service, SAL['name'], Literal(name))
    return service

def construct_sep (service, organization, url, read, write, priority):
    # add information object
    sep = DEFAULT['sep/%u' % generate_id()]
    if read and write:
        add_instance(sep, SAL['KafkaRWServiceEndpoint'])
    elif read:
        add_instance(sep, SAL['KafkaRServiceEndpoint'])
    elif write:
        add_instance(sep, SAL['KafkaWServiceEndpoint'])
    else:
        print('ERROR: Attempting to add SEP(%s, %s, %s, %s, %s, %s) with r/w mismatch' % (service, organization, url, read, write, priority))
    
    if read:
        add_data_property(sep, SAL['read_topic'] , url)
    if write:
        add_data_property(sep, SAL['write_topic'], url)
    
#    add_instance(sep, SAL['ServiceEndpoint'])
#    add_data_property(sep, SAL['url']     , url)
#    add_data_property(sep, SAL['read']    , read)
#    add_data_property(sep, SAL['write']   , write)
    add_data_property(sep, SAL['priority'], priority)
    
    # link service to service endpoint object
    add_object_property(service, SAL['hasServiceEndpoint'], sep)
    
    # link service endpoint object to organization
    add_object_property(sep, SAL['ownedBy'], organization)
    
    return sep

def construct_information (sep, location_data, modality, unit, temporal, location):
    # add information object
    info = DEFAULT['info/%u' % generate_id()]
    add_instance(info, SAL['Information'])
    add_data_property(  info, SAL['location']         , location_data)
    add_object_property(info, SAL['hasModality']      , modality)
    add_object_property(info, SAL['hasUnit']          , unit)
    add_object_property(info, SAL['hasTemporalAspect'], temporal)
    add_object_property(info, SAL['hasLocation']      , location)
    
    # link service endpoint to information object
    add_object_property(sep, SAL['hasInformation'], info)
    
    return info

###############################################################################
##################################################################### misc ####

def serialize (filename):
    g.serialize(filename, 'turtle')

###############################################################################
##################################################################### main ####

g = rdflib.Graph()
RDF     = rdflib.Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS    = rdflib.Namespace('http://www.w3.org/2000/01/rdf-schema#')
SAL     = rdflib.Namespace('https://ontology.hviidnet.com/sal.ttl#')
SALI    = rdflib.Namespace('https://ontology.hviidnet.com/sali.ttl#')
BRICK   = rdflib.Namespace('http://brickschema.org/ttl/Brick.ttl#')
SCHEMA  = rdflib.Namespace('http://schema.org/version/latest/schema.ttl#')
DEFAULT = rdflib.Namespace('https://ontology.hviidnet.com/defaultbuilding.ttl#')
g.bind('sal'    , SAL)
g.bind('sali'   , SALI)
g.bind('default', DEFAULT)


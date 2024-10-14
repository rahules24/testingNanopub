import json
from rdflib import Graph,Namespace
from nanopub import Nanopub, NanopubConf, load_profile
from nanopub.definitions import DUMMY_NAMESPACE, DUMMY_URI
from rdflib.namespace import DCTERMS, XSD 
from rdflib import Namespace, URIRef, Literal
from nanopub.utils import  NanopubMetadata
from nanopub.namespaces import HYCL, NP, NPX, NTEMPLATE, ORCID, PAV



# 1. Load the JSON-LD file and convert to RDF graph
with open('publication.json', 'r') as file:
    assertion = json.load(file)
with open('newpub.json', 'r') as file:
    pubinfo = json.load(file)

# Create an RDF graph from JSON-LD data
my_assertion = Graph()
my_pubinfo = Graph()
# my_pubinfo.add()

my_assertion.parse(data=json.dumps(assertion), format='json-ld')
# my_pubinfo.parse(data=json.dumps(pubinfo), format='json-ld')
# my_pubinfo = Graph()
mm = NanopubMetadata()
# Define the subject URI
subject = mm.namespace[""]

# Add the date and creation triple using dcterms
my_pubinfo.add((subject, DCTERMS.creator, URIRef("https://xyz.com")))
my_pubinfo.add((subject, DCTERMS.dateSubmitted, Literal("2024-10-10", datatype=XSD.date)))
my_pubinfo.add((subject, DCTERMS.license, URIRef("https://creativecommons.org/licenses/by/4.0/")))
my_pubinfo.add((subject, NTEMPLATE.wasCreatedFromPubinfoTemplate, URIRef("https://w3id.org/np/RAp_-kdLEx25ZkR8QSG2MZpV5ajv8W2xM0TLoD7Wc76gg")))
my_pubinfo.add((subject, NTEMPLATE.wasCreatedFromTemplate, URIRef("https://w3id.org/np/RAp_-kdLEx25ZkR8QSG2MZpV5ajv8W2xM0TLoD7Wc76gg")))
my_pubinfo.add((subject, NTEMPLATE.wasCreatedFromProvenanceTemplate, URIRef("https://w3id.org/np/RAp_-kdLEx25ZkR8QSG2MZpV5ajv8W2xM0TLoD7Wc76gg")))

np_conf = NanopubConf(
    use_server='http://localhost:8080',  # Specify your local server URL
    profile=load_profile(),  # Loads the user profile
    add_prov_generated_time=True,
    attribute_publication_to_profile=True,
)

# 3. Make a Nanopub object with this assertion
np = Nanopub(
    assertion=my_assertion,
    pubinfo=my_pubinfo,
    conf=np_conf
)

# 4. Publish the Nanopub object
np.publish()
print("Nanopub published!")

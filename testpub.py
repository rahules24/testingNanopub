import json
from rdflib import Graph, URIRef, Literal
from nanopub import Nanopub, NanopubConf, load_profile
from rdflib.namespace import DCTERMS, XSD, FOAF, PROV, RDF
from nanopub.utils import NanopubMetadata
from nanopub.namespaces import NTEMPLATE
from datetime import datetime

# 1. Load the JSON-LD file and convert to RDF graph
with open('publication.json', 'r') as file:
    assertion = json.load(file)

# Create an RDF graph from JSON-LD data
my_assertion = Graph()
my_pubinfo = Graph()
my_provenance = Graph()

my_assertion.parse(data=json.dumps(assertion), format='json-ld')

# Load profile
profile = load_profile()
orcid_id = profile.orcid_id
name = profile.name

nanopub_namespace = NanopubMetadata()
# Define the subject URI
subject = nanopub_namespace.namespace[""]

# Add the date and creation triple using dcterms, with dynamic date
current_date = datetime.now().strftime("%Y-%m-%d")
my_pubinfo.add((subject, DCTERMS.creator, URIRef("https://aopsketchpad.com")))
my_pubinfo.add((subject, DCTERMS.dateSubmitted, Literal(current_date, datatype=XSD.date)))
my_pubinfo.add((subject, DCTERMS.license, URIRef("https://creativecommons.org/licenses/by/4.0/")))
my_pubinfo.add((subject, NTEMPLATE.wasCreatedFromPubinfoTemplate, URIRef("https://w3id.org/np/RAp_-kdLEx25ZkR8QSG2MZpV5ajv8W2xM0TLoD7Wc76gg")))
my_pubinfo.add((subject, NTEMPLATE.wasCreatedFromTemplate, URIRef("https://w3id.org/np/RAp_-kdLEx25ZkR8QSG2MZpV5ajv8W2xM0TLoD7Wc76gg")))
my_pubinfo.add((subject, NTEMPLATE.wasCreatedFromProvenanceTemplate, URIRef("https://w3id.org/np/RAp_-kdLEx25ZkR8QSG2MZpV5ajv8W2xM0TLoD7Wc76gg")))

# Define provenance data
software_agent = URIRef("https://aopsketchpad.com/")
my_provenance.add((software_agent, RDF.type, URIRef("http://www.w3.org/ns/prov#SoftwareAgent")))
my_provenance.add((software_agent, PROV.actedOnBehalfOf, URIRef(orcid_id)))

activity = nanopub_namespace.namespace["activity"]
my_provenance.add((activity, RDF.type, URIRef("https://aopsketchpad.com/supervisedActivity")))
my_provenance.add((activity, PROV.wasAssociatedWith, software_agent))

# Profile-based attribution
if orcid_id and name:
    my_provenance.add((URIRef(orcid_id), FOAF.name, Literal(name)))
    my_provenance.add((URIRef(orcid_id), PROV.wasAttributedTo, URIRef(orcid_id)))

np_conf = NanopubConf(
    use_server='http://localhost:8080',  # Specify your local server URL
    profile=profile,  # Loads the user profile
    add_prov_generated_time=True,
    attribute_publication_to_profile=True,
)

# 3. Make a Nanopub object with this assertion
np = Nanopub(
    assertion=my_assertion,
    provenance=my_provenance,
    pubinfo=my_pubinfo,
    conf=np_conf,
)

# 4. Publish the Nanopub object
np.publish()
print("Nanopub published!")

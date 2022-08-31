import json
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, RDF, SKOS, XSD, NamespaceManager
from pathlib import Path
import uuid
import sys

core = Namespace('https://w3id.org/iqb/mdc-core/cs_')
lrmi = Namespace('http://purl.org/dcx/lrmi-terms/')
oeh_md = Namespace('http://w3id.org/openeduhub/learning-resource-terms/')

if len(sys.argv) > 1 and str(sys.argv[1]) == "help":
    exit("Please add one input json file to the command line and the base url_id")

input_file =  "./" + sys.argv[1]
url_id = sys.argv[2]

with open(input_file, 'r',  encoding='utf-8') as f:
    data = json.load(f)

output_folder = Path("./data")
if not output_folder.exists():
    output_folder.mkdir()

def buildGraph():
    if("dimensions" in data):
        for dimension in data['dimensions']:
            g = Graph()
            base_url = URIRef("https://w3id.org/iqb/" + url_id + "/")
            g.add((base_url, RDF.type, SKOS.ConceptScheme))
            g.add((base_url, DCTERMS.creator, Literal("IQB - Institut zur Qualitätsentwicklung im Bildungswesen", lang="de")))
            title = data['title'] + '_' + dimension['title']
            g.add((base_url, DCTERMS.title, Literal(title, lang="de")))
            if "description" in data:
                g.add((base_url, DCTERMS.description, Literal(data['description'], lang="de")))
            g.bind("skos", SKOS)
            g.bind("dct", DCTERMS)
            g.bind("core", core)
            concept_url = URIRef(base_url + dimension['id'])
            g.add((base_url, SKOS.hasTopConcept, concept_url))
            g.add(((concept_url, RDF.type, SKOS.Concept)))
            g.add((concept_url, SKOS.prefLabel, Literal(dimension['title'], lang="de")))
            if "description" in dimension:
                g.add((concept_url, SKOS.definition, Literal(dimension['description'], lang="de")))
            
            for c in dimension['children']:
                child_url = URIRef(concept_url + str(uuid.uuid4()))
                g.add((concept_url, SKOS.narrower, child_url))
                g.add((child_url, RDF.type, SKOS.Concept))
                g.add((child_url, SKOS.inScheme, base_url))
                g.add((base_url, SKOS.hasTopConcept, concept_url))
                g.add((concept_url, SKOS.topConceptOf, base_url))
                g.add((child_url, SKOS.prefLabel, Literal(c['title'], lang="de")))
                g.add((child_url, SKOS.notation, Literal(c['notation'])))
                g.add((child_url, SKOS.broader, concept_url))
                if "description" in c:
                    g.add((child_url, SKOS.definition, Literal(c['description'], lang="de")))
                
                if "children" in c:
                    for cc in c['children']:
                        cc_url = URIRef(concept_url + str(uuid.uuid4()))
                        g.add((child_url, SKOS.narrower, cc_url))
                        g.add((cc_url, RDF.type, SKOS.Concept))
                        g.add((cc_url, SKOS.inScheme, base_url))
                        g.add((cc_url, SKOS.broader, child_url))
                        g.add((cc_url, SKOS.notation, Literal(cc['notation'])))
                        g.add((cc_url, SKOS.prefLabel, Literal(cc['title'], lang="de")))
                        if "description" in cc:
                            g.add((cc_url, SKOS.definition, Literal(cc['description'], lang="de")))
                        
                        if "children" in cc:
                            for ccc in cc['children']:
                                ccc_url = URIRef(concept_url + str(uuid.uuid4()))
                                g.add((cc_url, SKOS.narrower, ccc_url))
                                g.add((ccc_url, RDF.type, SKOS.Concept))
                                g.add((ccc_url, SKOS.inScheme, base_url))
                                g.add((ccc_url, SKOS.broader, cc_url))
                                g.add((ccc_url, SKOS.notation, Literal(ccc['notation'])))
                                g.add((ccc_url, SKOS.prefLabel, Literal(ccc['title'], lang="de")))
                                if "description" in ccc:
                                    g.add((ccc_url, SKOS.definition, Literal(ccc['description'], lang="de")))
                                
                                if "children" in ccc:
                                        for cccc in ccc['children']:
                                            cccc_url = URIRef(concept_url + str(uuid.uuid4()))
                                            g.add((ccc_url, SKOS.narrower, cccc_url))
                                            g.add((cccc_url, RDF.type, SKOS.Concept))
                                            g.add((cccc_url, SKOS.inScheme, base_url))
                                            g.add((cccc_url, SKOS.broader, ccc_url))
                                            g.add((cccc_url, SKOS.notation, Literal(cccc['notation'])))
                                            g.add((cccc_url, SKOS.prefLabel, Literal(cccc['title'], lang="de")))
                                            if "description" in cccc:
                                                g.add((cccc_url, SKOS.definition, Literal(cccc['description'], lang="de")))
            outfile_path = output_folder / ("iqb_" + data['title'] + '_' + dimension['id'] + ".ttl")
            g.serialize(str(outfile_path), format="turtle", base=base_url, encoding="utf-8")
    elif(data['children']):
        for c in data['children']:
            g = Graph()
            base_url = URIRef("https://w3id.org/iqb/" + url_id + "/")
            g.add((base_url, RDF.type, SKOS.ConceptScheme))
            g.add((base_url, DCTERMS.creator, Literal("IQB - Institut zur Qualitätsentwicklung im Bildungswesen", lang="de")))
            title = data['title'] + '_' + c['title']
            g.add((base_url, DCTERMS.title, Literal(title, lang="de")))
            if "description" in data:
                g.add((base_url, DCTERMS.description, Literal(data['description'], lang="de")))
            g.bind("skos", SKOS)
            g.bind("dct", DCTERMS)
            g.bind("core", core)
            child_url = URIRef(base_url + c['id'] + "/")
            g.add((child_url, RDF.type, SKOS.Concept))
            g.add((child_url, SKOS.prefLabel, Literal(c['title'], lang="de")))
            if "description" in c:
                g.add((child_url, SKOS.definition, Literal(c['description'], lang="de")))
                
            if "children" in c:
                for cc in c['children']:
                    cc_url = URIRef(child_url + str(uuid.uuid4()))
                    g.add((child_url, SKOS.narrower,cc_url))
                    g.add((cc_url, RDF.type, SKOS.Concept))
                    g.add((base_url, SKOS.hasTopConcept, child_url))
                    g.add((cc_url, SKOS.inScheme, base_url))
                    g.add((child_url, SKOS.topConceptOf, base_url))
                    g.add((cc_url, SKOS.broader, child_url))
                    g.add((cc_url, SKOS.notation, Literal(cc['notation'])))
                    g.add((cc_url, SKOS.prefLabel, Literal(cc['title'], lang="de")))
                    if "description" in cc:
                        g.add((cc_url, SKOS.definition, Literal(cc['description'], lang="de")))
                        
                    if "children" in cc:
                        for ccc in cc['children']:
                            ccc_url = URIRef(child_url + str(uuid.uuid4()))
                            g.add((cc_url, SKOS.narrower, ccc_url))
                            g.add((ccc_url, RDF.type, SKOS.Concept))
                            g.add((ccc_url, SKOS.inScheme, base_url))
                            g.add((ccc_url, SKOS.broader, cc_url))
                            g.add((ccc_url, SKOS.notation, Literal(ccc['notation'])))
                            g.add((ccc_url, SKOS.prefLabel, Literal(ccc['title'], lang="de")))
                            if "description" in ccc:
                                g.add((ccc_url, SKOS.definition, Literal(ccc['description'], lang="de")))
                                
                            if "children" in ccc:
                                for cccc in ccc['children']:
                                    cccc_url = URIRef(child_url + str(uuid.uuid4()))
                                    g.add((ccc_url, SKOS.narrower, cccc_url))
                                    g.add((cccc_url, RDF.type, SKOS.Concept))
                                    g.add((cccc_url, SKOS.broader, ccc_url))
                                    g.add((cccc_url, SKOS.inScheme, base_url))
                                    g.add((cccc_url, SKOS.notation, Literal(cccc['notation'])))
                                    g.add((cccc_url, SKOS.prefLabel, Literal(cccc['title'], lang="de")))
                                    if "description" in cccc:
                                        g.add((cccc_url, SKOS.definition, Literal('description', lang="de")))
            outfile_path = output_folder / ("iqb_" + data['title'] + '_' + c['id'] + ".ttl")
            g.serialize(str(outfile_path), format="turtle", base=base_url, encoding="utf-8")                   

    

buildGraph()
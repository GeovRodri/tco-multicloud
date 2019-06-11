from owlready2 import *

class SparqlQuery:
    vms = ["alibaba", "aws", "azure", "google"]

    def __init__(self):
        onto_path.append("./Ontology/")

        default_world.get_ontology("CloudIaaS3.owl").load()

        sync_reasoner()  # reasoner is started and synchronized here
        self.graph = default_world.as_rdflib_graph()

    def search(self):

        response = {}
        iaasProvider = {}

        response['generic_fields'] = ['cpu', 'hd', 'pricing', 'ram']

        for provider in SparqlQuery.vms:

            iaasProvider[provider] = []

            query = """
                            PREFIX b:<http://www.semanticweb.org/gilberto/ontologies/2019/4/CloudIaaS#>
                            SELECT DISTINCT ?o
                            WHERE  {{
                            b:{} ?p ?s .
                            ?s rdfs:comment ?o .
                            }} """.format(provider)

            resultsList = self.graph.query(query)

            for item in resultsList:

                o = str(item['o'].toPython())
                o = re.sub(r'.*#', "", o)

                iaasProvider[provider].append(o)

        response['specific_fields'] = iaasProvider
        return response


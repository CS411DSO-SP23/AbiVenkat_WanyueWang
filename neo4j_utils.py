from neo4j import GraphDatabase
import pandas as pd

# Connect to the Neo4j database
# Note: use your Neo4j credentials!
def connect_to_neo4j(uri, user, password):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    return driver

neo4j_uri = "bolt://localhost:7687"
neo4j_user = "neo4j"
neo4j_password = "test_root"

# driver = connect_to_neo4j(neo4j_uri, neo4j_user, neo4j_password)


# Interactive query
def find_faculty_connections(origin_faculty='', origin_institute='', dest_faculty='', dest_institute=''):
    driver = connect_to_neo4j(neo4j_uri, neo4j_user, neo4j_password)
    with driver.session(database='academicworld') as session:
        query = f"""
                    MATCH
                    (f2:FACULTY {{name: "{dest_faculty}"}})-[affiliation2:AFFILIATION_WITH]-(u2:INSTITUTE {{name: "{dest_institute}"}}),
                    (u1:INSTITUTE {{name: "{origin_institute}"}})
                    OPTIONAL MATCH (f1:FACULTY)-[affiliation1:AFFILIATION_WITH]-(u1)
                    WHERE f1.name = "{origin_faculty}" OR "{origin_faculty}" = ""
                    WITH f1, f2, CASE WHEN "{origin_faculty}" = "" THEN true ELSE NOT f1 IS NULL END as faculty_exists
                    WHERE faculty_exists
                    MATCH path = shortestPath((f1)-[:INTERESTED_IN|KEYWORD|FACULTY*]-(f2))
                    RETURN path
                    LIMIT 5
                """

        # # All inputs are required
        # query = f"""
        #             MATCH
        #             (f1:FACULTY {{name: "{origin_faculty}"}})-[affiliation1:AFFILIATION_WITH]-(u1:INSTITUTE {{name: "{origin_institute}"}}),
        #             (f2:FACULTY {{name: "{dest_faculty}"}})-[affiliation2:AFFILIATION_WITH]-(u2:INSTITUTE {{name: "{dest_institute}"}}),
        #             path = shortestPath((f1)-[:INTERESTED_IN|KEYWORD|FACULTY*]-(f2))
        #             RETURN path
        #             LIMIT 5
        #         """
        result = session.run(query)

        elements = {}
        for record in result:
            path = record['path']

            # Create nodes
            for node in path.nodes:
                node_key = f"node_{node.id}"
                if node_key not in elements:
                    elements[node_key] = {"data": {"id": node.id, "label": node['name']}}

            # Create edges
            for relationship in path.relationships:
                source = relationship.start_node
                target = relationship.end_node
                rel_type = relationship.type
                edge_key = f"edge_{source.id}_{target.id}"
                if edge_key not in elements:
                    elements[edge_key] = {"data": {"source": source.id, "target": target.id, "label": rel_type}}

    graph_data = list(elements.values())

    # Separate nodes and edges
    nodes_data = [item["data"] for item in graph_data if "source" not in item["data"]]
    edges_data = [item["data"] for item in graph_data if "source" in item["data"]]

    # Create DataFrames
    nodes_df = pd.DataFrame(nodes_data)
    edges_df = pd.DataFrame(edges_data)

    return nodes_df, edges_df




# # Fixed query
# def find_faculty_connections():
#     driver = connect_to_neo4j(neo4j_uri, neo4j_user, neo4j_password)
#     with driver.session(database='academicworld') as session:
#         query = """
#             MATCH
#                 (f1:FACULTY {name: "Craig Zilles"})-[affiliation1:AFFILIATION_WITH]-(uiuc:INSTITUTE {name: "University of illinois at Urbana Champaign"}),
#                 (f2:FACULTY {name: "Yang, Yiming"})-[affiliation2:AFFILIATION_WITH]-(cmu:INSTITUTE {name: "Carnegie Mellon University"}),
#                 path = shortestPath((f1)-[:INTERESTED_IN|KEYWORD|FACULTY*]-(f2))
#                 RETURN path
#                 LIMIT 5
#             """
#         result = session.run(query)
#
#         elements = {}
#         for record in result:
#             path = record['path']
#
#             # Create nodes
#             for node in path.nodes:
#                 node_key = f"node_{node.id}"
#                 if node_key not in elements:
#                     elements[node_key] = {"data": {"id": node.id, "label": node['name']}}
#
#             # Create edges
#             for relationship in path.relationships:
#                 source = relationship.start_node
#                 target = relationship.end_node
#                 rel_type = relationship.type
#                 edge_key = f"edge_{source.id}_{target.id}"
#                 if edge_key not in elements:
#                     elements[edge_key] = {"data": {"source": source.id, "target": target.id, "label": rel_type}}
#
#     graph_data = list(elements.values())
#
#     # Separate nodes and edges
#     nodes_data = [item["data"] for item in graph_data if "source" not in item["data"]]
#     edges_data = [item["data"] for item in graph_data if "source" in item["data"]]
#
#     # Create DataFrames
#     nodes_df = pd.DataFrame(nodes_data)
#     edges_df = pd.DataFrame(edges_data)
#
#     # print("Nodes DataFrame:")
#     # print(nodes_df)
#     #
#     # print("\nEdges DataFrame:")
#     # print(edges_df)
#
#     return nodes_df, edges_df
#
# # find_faculty_connections()



# # Test using simple query test
# def find_faculty_count():
#     driver = connect_to_neo4j(neo4j_uri, neo4j_user, neo4j_password)
#     target_database = 'academicworld'
#     with driver.session(database=target_database) as session:
#         query = """
#         MATCH (faculty:FACULTY) WHERE faculty.position = 'Assistant Professor' RETURN COUNT(*) AS faculty_count
#         """
#         result = session.run(query)
#         data = [record['faculty_count'] for record in result]
#
#     return data

# # Test if the connection is successful and whether the query works
# faculty_count = find_faculty_count()
#
# if faculty_count:
#     print(f"Connection to Neo4j is successful!")
#     print(f"Faculty count: {faculty_count[0]}")
# else:
#     print("Connection to Neo4j failed or there is no data in the database.")

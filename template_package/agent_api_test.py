from biocypher import create_workflow

# Create a simple workflow
workflow = create_workflow("my_graph", validation_mode="warn", deduplication=True)

# Add nodes
workflow.add_node("protein_1", "protein", name="TP53", function="tumor_suppressor")
workflow.add_node("protein_2", "protein", name="BRAF", function="kinase")

# Add edges
workflow.add_edge("interaction_1", "interaction", "protein_1", "protein_2", confidence=0.8)

# Check the graph
print(f"Graph has {len(workflow)} nodes")

# This will warn about duplicates but continue
workflow.add_node("protein_1", "protein", name="TP53")  # Warning logged


# Example 1

# Create knowledge graph
kg = create_workflow("biomedical_knowledge")

# Add proteins
kg.add_node("TP53", "protein", name="TP53", function="tumor_suppressor")
kg.add_node("BRAF", "protein", name="BRAF", function="kinase")

# Add diseases
kg.add_node("melanoma", "disease", name="Melanoma", description="Skin cancer")

# Add interactions
kg.add_edge("TP53_BRAF", "interaction", "TP53", "BRAF", confidence=0.8)
kg.add_edge("BRAF_melanoma", "causes", "BRAF", "melanoma", evidence="strong")

# Query
proteins = kg.query_nodes("protein")
paths = kg.find_paths("TP53", "melanoma")

print(f"Proteins in the graph: {[p["properties"]["name"] for p in proteins]}")
print(f"Paths from TP53 to melanoma: {len(paths)}")

# Example 2

# Create reasoning graph
reasoning = create_workflow("reasoning_process")

# Log observation
reasoning.add_node("obs_1", "observation",
                  description="TP53 is frequently mutated in cancer",
                  source="literature")

# Log inference
reasoning.add_node("inf_1", "inference",
                  description="TP53 mutations likely contribute to cancer development",
                  confidence=0.9)

# Connect reasoning steps
reasoning.add_edge("obs_to_inf", "supports", "obs_1", "inf_1", strength=0.8)

# Export reasoning process
reasoning.save("reasoning_process.json")

# Example 3

# Define schema
schema = {
    "protein": {
        "represented_as": "node",
        "properties": {
            "name": "str",
            "function": "str",
            "uniprot_id": "str"
        }
    },
    "interaction": {
        "represented_as": "edge",
        "source": "protein",
        "target": "protein",
        "properties": {
            "confidence": "float",
            "evidence": "str"
        }
    }
}

# Create workflow with schema validation
workflow = create_workflow("validated_graph", schema=schema, validation_mode="strict")

# Valid node (passes validation)
workflow.add_node("TP53", "protein", name="TP53", function="tumor_suppressor", uniprot_id="P04637")

# Invalid node (fails validation in strict mode)
# workflow.add_node("BRAF", "protein", name=123)  # Wrong type for name
# workflow.add_node("MDM2", "protein", name="MDM2")  # Missing required function

# Example 4

# Create protein complex knowledge graph
complexes = create_workflow("protein_complexes")

# Add proteins
complexes.add_node("TP53", "protein", name="TP53")
complexes.add_node("MDM2", "protein", name="MDM2")
complexes.add_node("CDKN1A", "protein", name="CDKN1A")

# Add protein complex as hyperedge
complexes.add_hyperedge("TP53_MDM2_complex", "protein_complex",
                       {"TP53", "MDM2"}, function="protein_degradation")

complexes.add_hyperedge("TP53_CDKN1A_complex", "protein_complex",
                       {"TP53", "CDKN1A"}, function="cell_cycle_control")

# Query complexes
protein_complexes = complexes.query_hyperedges("protein_complex")
print(f"Protein complexes in the graph: {[c['properties']['function'] for c in protein_complexes]}")

# Example 5
# Create workflow optimized for agents
workflow = create_workflow("agent_graph", validation_mode="none")

# Agent discovers entities dynamically
discovered_entities = [
    {"id": "entity_1", "type": "protein", "name": "TP53", "function": "tumor_suppressor"},
    {"id": "entity_2", "type": "protein", "name": "BRAF", "function": "kinase"},
    {"id": "entity_3", "type": "disease", "name": "Cancer", "description": "Uncontrolled growth"}
]

# Add entities dynamically
for entity in discovered_entities:
    workflow.add_node(entity["id"], entity["type"], **{k: v for k, v in entity.items() if k not in ["id", "type"]})

# Agent discovers relationships
discovered_relationships = [
    {"id": "rel_1", "type": "interaction", "source": "entity_1", "target": "entity_2", "confidence": 0.8},
    {"id": "rel_2", "type": "causes", "source": "entity_2", "target": "entity_3", "evidence": "strong"}
]

# Add relationships dynamically
for rel in discovered_relationships:
    workflow.add_edge(rel["id"], rel["type"], rel["source"], rel["target"],
                     **{k: v for k, v in rel.items() if k not in ["id", "type", "source", "target"]})

# Convert to analysis format when needed
nx_graph = workflow.to_networkx()
"""
Script to visualize the RAG LangGraph workflow
"""
from src.graph.graph_builder import graph

def save_graph_visualization():
    """Generate and save the graph visualization as PNG"""
    try:
        from langgraph.constants import MermaidDrawMethod
        
        # Generate the Mermaid PNG using local rendering
        print("🎨 Rendering graph locally using Pyppeteer...")
        png_data = graph.get_graph().draw_mermaid_png(
            draw_method=MermaidDrawMethod.PYPPETEER
        )
        
        # Save to file
        output_file = "rag_graph_visualization.png"
        with open(output_file, "wb") as f:
            f.write(png_data)
        
        print(f"✅ Graph visualization saved to: {output_file}")
        print("\nGraph Structure:")
        print("=" * 60)
        print("Nodes:")
        for node in graph.get_graph().nodes:
            print(f"  - {node}")
        print("\nEdges:")
        for edge in graph.get_graph().edges:
            print(f"  - {edge}")
        print("=" * 60)
        
        return output_file
    except Exception as e:
        print(f"❌ Error generating graph visualization: {e}")
        print("\nTrying alternative ASCII representation...")
        try:
            # Fallback: Print graph structure as text
            print("\nGraph Nodes:")
            for node in graph.get_graph().nodes:
                print(f"  • {node}")
            print("\nGraph Edges:")
            for edge in graph.get_graph().edges:
                print(f"  • {edge[0]} → {edge[1]}")
        except Exception as e2:
            print(f"❌ Error with fallback: {e2}")

if __name__ == "__main__":
    print("🔍 Visualizing RAG LangGraph Workflow...\n")
    save_graph_visualization()
    print("\n✨ Done! Open 'rag_graph_visualization.png' to see the graph.")

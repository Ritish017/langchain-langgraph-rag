"""
Comprehensive Graph Visualization Tool
Shows the RAG workflow structure in multiple formats
"""
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def visualize_graph():
    """Visualize the graph in multiple ways"""
    
    from src.graph.graph_builder import graph
    
    print("\n" + "="*80)
    print("🔷 RAG WORKFLOW GRAPH VISUALIZATION")
    print("="*80)
    
    # 1. ASCII Art Visualization
    print("\n📊 Visual Flow Diagram:\n")
    print("""
    ┌──────────┐
    │  START   │
    └────┬─────┘
         │
         ▼
    ┌────────────────────────────┐
    │ generate_query_or_respond  │ ← LLM Router: Answer directly or retrieve?
    └─────────────┬──────────────┘
                  │
         ┌────────┴────────┐
         │                 │
         ▼                 ▼
    ┌─────────┐       ┌────────┐
    │   END   │       │retrieve│ ← Search ChromaDB for relevant docs
    │(direct) │       └───┬────┘
    └─────────┘           │
                          ▼
                  ┌───────────────┐
                  │grade_documents│ ← Quality check: Are docs relevant?
                  └───────┬───────┘
                          │
                 ┌────────┴────────┐
                 │                 │
                 ▼                 ▼
        ┌─────────────────┐  ┌──────────────┐
        │ generate_answer  │  │rewrite_query │ ← Improve question
        └────────┬─────────┘  └──────┬───────┘
                 │                   │
                 ▼                   │
            ┌─────────┐              │
            │   END   │              │
            └─────────┘              │
                                     │
                 ┌───────────────────┘
                 │
                 └──► Loop back to generate_query_or_respond
    """)
    
    # 2. Node Details
    print("\n" + "="*80)
    print("📋 NODE DESCRIPTIONS")
    print("="*80)
    
    nodes_info = {
        "START": {
            "type": "Entry Point",
            "description": "Initial entry into the workflow",
            "actions": ["Receives user question", "Passes to first node"]
        },
        "generate_query_or_respond": {
            "type": "LLM Router Node", 
            "description": "Gemini LLM with tool-calling capability",
            "actions": [
                "Analyzes user question",
                "Decides: Can answer directly OR needs retrieval",
                "If retrieval needed: calls document_retriever tool",
                "If can answer: returns response and goes to END"
            ]
        },
        "retrieve": {
            "type": "Tool Node",
            "description": "Document retrieval from ChromaDB",
            "actions": [
                "Executes the document_retriever tool",
                "Searches vector store using TF-IDF embeddings",
                "Returns top-k relevant document chunks",
                "Passes documents to grader"
            ]
        },
        "grade_documents": {
            "type": "Decision Node",
            "description": "Quality control for retrieved documents",
            "actions": [
                "Uses LLM to grade document relevance",
                "Checks if docs actually answer the question",
                "If relevant: → generate_answer",
                "If not relevant: → rewrite_question"
            ]
        },
        "generate_answer": {
            "type": "Generator Node",
            "description": "Final answer generation with context",
            "actions": [
                "Receives question + relevant documents",
                "Uses Gemini LLM to generate answer",
                "Formats response with proper structure",
                "Returns to END"
            ]
        },
        "rewrite_question": {
            "type": "Query Rewriter Node",
            "description": "Improves question for better retrieval",
            "actions": [
                "Uses LLM to rewrite/rephrase question",
                "Makes question more specific or clear",
                "Loops back to generate_query_or_respond",
                "Tries retrieval again with better query"
            ]
        },
        "END": {
            "type": "Exit Point",
            "description": "Workflow completion",
            "actions": ["Returns final answer to user"]
        }
    }
    
    for node_name, info in nodes_info.items():
        print(f"\n🔹 {node_name}")
        print(f"   Type: {info['type']}")
        print(f"   Description: {info['description']}")
        print(f"   Actions:")
        for action in info['actions']:
            print(f"      • {action}")
    
    # 3. Workflow Scenarios
    print("\n" + "="*80)
    print("🔄 WORKFLOW SCENARIOS")
    print("="*80)
    
    print("\n📌 Scenario 1: Simple Question (Direct Answer)")
    print("-" * 80)
    print("""
Question: "What is 2+2?"

Flow:
  START → generate_query_or_respond → END
  
Explanation: LLM knows the answer, no retrieval needed.
    """)
    
    print("\n📌 Scenario 2: RAG Success (Found Relevant Docs)")
    print("-" * 80)
    print("""
Question: "What is LangGraph?"

Flow:
  START → generate_query_or_respond → retrieve → grade_documents → 
  generate_answer → END
  
Explanation: 
  1. LLM needs context, calls retriever
  2. Finds relevant docs about LangGraph
  3. Docs graded as relevant
  4. Generates answer using docs
    """)
    
    print("\n📌 Scenario 3: RAG with Query Rewrite")
    print("-" * 80)
    print("""
Question: "How do I use that graph thingy?"

Flow:
  START → generate_query_or_respond → retrieve → grade_documents → 
  rewrite_question → generate_query_or_respond → retrieve → 
  grade_documents → generate_answer → END
  
Explanation:
  1. Vague question, retrieves docs
  2. Docs not relevant to "graph thingy"
  3. Rewrites to "How do I use LangGraph?"
  4. Retrieves again with better query
  5. Finds relevant docs
  6. Generates answer
    """)
    
    # 4. Try to get actual graph structure
    print("\n" + "="*80)
    print("🎯 ACTUAL GRAPH STRUCTURE")
    print("="*80)
    
    try:
        print("\nNodes:")
        for node in graph.get_graph().nodes:
            print(f"  ✓ {node}")
        
        print("\nEdges:")
        for edge in graph.get_graph().edges:
            print(f"  → {edge}")
            
    except Exception as e:
        print(f"Could not retrieve graph structure: {e}")
    
    # 5. Try ASCII representation
    try:
        print("\n" + "="*80)
        print("📐 LANGGRAPH ASCII REPRESENTATION")
        print("="*80 + "\n")
        print(graph.get_graph().draw_ascii())
    except Exception as e:
        print(f"\n(Technical ASCII not available: {e})")
    
    # 6. Try to save PNG if possible
    print("\n" + "="*80)
    print("💾 SAVING VISUALIZATION")
    print("="*80)
    
    try:
        png_data = graph.get_graph().draw_mermaid_png()
        output_file = "rag_graph_visualization.png"
        with open(output_file, "wb") as f:
            f.write(png_data)
        print(f"\n✅ Graph saved as: {output_file}")
        print("   Open this file to see the visual diagram!")
    except Exception as e:
        print(f"\n⚠️  PNG generation not available: {e}")
        print("   (This is normal - requires additional dependencies)")
    
    print("\n" + "="*80)
    print("✨ VISUALIZATION COMPLETE!")
    print("="*80 + "\n")

if __name__ == "__main__":
    visualize_graph()

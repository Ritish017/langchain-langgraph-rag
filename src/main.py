"""
Commandtry:
    from src.graph.graph_builder import graph  # Using original graph with grader
    from langchain_core.messages import HumanMessage
    import json
except ImportError as e: Interface for RAG-based Question Answering System
Built with LangGraph and ChromaDB
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

try:
    from src.graph.simple_graph_builder import simple_graph as graph
    from langchain_core.messages import HumanMessage
    import json
except ImportError as e:
    print(f"Import error: {e}")
    print("Please make sure all dependencies are installed and the graph is properly built.")
    sys.exit(1)

def main():
    """Main CLI interface for the RAG system"""
    print("=" * 60)
    print("🤖 RAG Question Answering System")
    print("Ask questions about LangChain and LangGraph documentation!")
    print("Type 'quit', 'exit', or 'q' to stop.")
    print("=" * 60)
    print()
    
    # Example questions
    print("📝 Sample questions:")
    examples = [
        "What is LangGraph?",
        "How does LangChain work?",
        "Explain vector stores",
        "What are document loaders?"
    ]
    for i, example in enumerate(examples, 1):
        print(f"  {i}. {example}")
    print()
    
    while True:
        try:
            # Get user input
            user_input = input("💭 Ask a question: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'q', '']:
                print("\n👋 Goodbye!")
                break
            
            print("\n🤔 Thinking...")
            
            # Create the input for the graph
            input_messages = [HumanMessage(content=user_input)]
            
            # Run the graph
            result = graph.invoke({"messages": input_messages})
            
            # Extract and display the response
            if result and "messages" in result and result["messages"]:
                response = result["messages"][-1].content
                print(f"\n🤖 Assistant: {response}")
            else:
                print("\n❌ I'm sorry, I couldn't generate a response. Please try again.")
            
            print("\n" + "-" * 60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {str(e)}")
            print("Please try again or contact support if the issue persists.\n")

def interactive_mode():
    """Run in interactive mode with step-by-step debugging"""
    print("🔧 Interactive Debug Mode")
    print("This mode shows the step-by-step execution of the RAG pipeline.")
    print()
    
    question = input("Enter your question: ").strip()
    if not question:
        print("No question provided. Exiting.")
        return
    
    print(f"\n📝 Question: {question}")
    print("\n🔄 Starting RAG pipeline...")
    
    try:
        # Create input
        input_messages = [HumanMessage(content=question)]
        input_data = {"messages": input_messages}
        
        print("\n1️⃣  Input created")
        print(f"   Messages: {[msg.content for msg in input_data['messages']]}")
        
        # Run the graph
        print("\n2️⃣  Running graph workflow...")
        result = graph.invoke(input_data)
        
        print("\n3️⃣  Graph execution completed")
        
        # Display results
        if result and "messages" in result:
            print(f"\n📊 Final result has {len(result['messages'])} messages:")
            for i, msg in enumerate(result['messages']):
                print(f"   {i+1}. {msg.content[:100]}{'...' if len(msg.content) > 100 else ''}")
            
            print(f"\n✅ Final Answer:")
            print(f"   {result['messages'][-1].content}")
        else:
            print("\n❌ No valid response generated")
            
    except Exception as e:
        print(f"\n❌ Error during execution: {str(e)}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--debug":
        interactive_mode()
    else:
        main()

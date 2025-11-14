"""
Test script for the complete RAG workflow with grader
"""

from src.graph.graph_builder import graph
from langchain_core.messages import HumanMessage

def test_complete_workflow():
    """Test the complete workflow with grader functionality"""
    
    # Test cases
    test_cases = [
        {
            "question": "What is LangGraph?",
            "description": "Relevant question - should go to generate_answer"
        },
        {
            "question": "What's the weather like today?",
            "description": "Irrelevant question - should trigger rewrite_question"
        },
        {
            "question": "hello!",
            "description": "Simple greeting - should respond directly without retrieval"
        }
    ]
    
    print("Testing Complete RAG Workflow with Grader")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['description']}")
        print(f"Question: {test_case['question']}")
        print("-" * 40)
        
        try:
            # Create input
            input_messages = [HumanMessage(content=test_case['question'])]
            
            # Run the graph
            result = graph.invoke({"messages": input_messages})
            
            # Display result
            if result and "messages" in result:
                final_message = result["messages"][-1]
                print(f"Response: {final_message.content}")
            else:
                print("No response generated")
                
        except Exception as e:
            print(f"Error: {str(e)}")
        
        print("-" * 40)

if __name__ == "__main__":
    test_complete_workflow()
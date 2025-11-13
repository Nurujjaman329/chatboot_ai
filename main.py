import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Import separated files
from system_prompt import SYSTEM_PROMPT
from layout_tools import ALL_TOOLS, execute_tool, set_api_tokens

# --------------------
# Load environment variables
load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("CHAT_MODEL", "gemini-2.5-flash")

SERVICE_TOKEN = os.getenv("EDOKAN_SERVICE_TOKEN")
SHOP_ID = os.getenv("EDOKAN_SHOP_ID")

# Set the API tokens in the tools module
set_api_tokens(SERVICE_TOKEN, SHOP_ID)

# --------------------
# Initialize GenAI client
try:
    client = genai.Client(api_key=GEMINI_KEY)
except Exception as e:
    print(f"Error initializing GenAI client: {e}")
    exit()

# --------------------
# Configuration
config = types.GenerateContentConfig(
    system_instruction=SYSTEM_PROMPT, 
    tools=[ALL_TOOLS]
)

conversation_history = []

def main():
    print("💬 Layout Assistant Started (Header + Footer + Homepage Enabled)")

    while True:
        user_input = input("\n👉 Enter your request:\n> ").strip()

        # Exit Condition
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("\n👋 Exiting Assistant. Goodbye!\n")
            break

        # Store user message
        conversation_history.append(
            types.Content(role="user", parts=[types.Part(text=user_input)])
        )

        # --- Inner loop for tool execution ---
        while True:
            try:
                # MARKED CHANGE: Wrap the API call in a try block
                response = client.models.generate_content(
                    model=MODEL,
                    contents=conversation_history,
                    config=config
                )

            # CORRECTED: Reference the error classes using the 'genai.errors' path.
            # This replaces the failed direct import.
            except (genai.errors.ResourceExhaustedError, genai.errors.InternalServerError) as e:
                print("\n⚠️ **MODEL OVERLOAD ERROR (503/429)** ⚠️")
                print("The AI service is currently overloaded or too busy. Please wait a moment and try your request again.")
                
                # Critical: Remove the last user message from history, as it triggered the error
                if conversation_history and conversation_history[-1].role == "user":
                    conversation_history.pop()
                
                break # Exit the inner loop, return to main user prompt
                
            except Exception as e:
                # Catch any other unexpected errors
                print(f"\n❌ Assistant Error: An unexpected API error occurred: {e}")
                
                # Optionally remove the last user message here too
                if conversation_history and conversation_history[-1].role == "user":
                    conversation_history.pop()
                
                break # Exit the inner loop, return to main user prompt


            print(response.usage_metadata)

            # --- SAFETY CHECK ---
            if not response.candidates:
                print("\n❌ Assistant Error: Model returned no candidates. Generation failed.")
                break
            
            result_content = response.candidates[0].content
            if not result_content or not result_content.parts:
                print("\n❌ Assistant Error: Model returned empty content or parts.")
                break
            
            result_part = result_content.parts[0]
            
            # If Tool Call Happened
            if result_part.function_call:
                fn = result_part.function_call
                print(f"\n🔧 Model requested tool: {fn.name} | args: {fn.args}")

                # Call the local tool
                tool_result = execute_tool(fn.name, fn.args) 

                # 1. Store the Model's Function Call in history
                conversation_history.append(
                    types.Content(role="model", parts=[
                        types.Part.from_function_call(
                            name=fn.name, 
                            args=fn.args
                        )
                    ])
                )
                print(tool_result)

                # 2. Store the Tool's Function Response in history
                conversation_history.append(
                    types.Content(role="tool", parts=[
                        types.Part.from_function_response(
                            name=fn.name, 
                            response=tool_result
                        )
                    ])
                )

                print("📚 Tool result returned — rethinking...\n")
                continue 

            # Normal Model Response (No Tool Call)
            print("\n✅ Assistant:")
            text_response = ""

            # Gather and print the text response
            print("\n💬 Assistant Response:")
            for p in result_content.parts:
                if getattr(p, "text", None):
                    print(p.text)
                    text_response += p.text + "\n"

            # Store the final Model text response
            conversation_history.append(
                types.Content(role="model", parts=[types.Part(text=text_response)])
            )

            break # Exit the inner while loop
            

if __name__ == "__main__":
    main()
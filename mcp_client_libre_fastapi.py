import os
import json
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from google import genai
from concurrent.futures import TimeoutError

import pyautogui
from pydantic import BaseModel

class problem(BaseModel):
    query: str
# Load environment variables
load_dotenv()
os.environ['DISPLAY'] = ":0"
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
model = "gemini-1.5-flash"
max_iterations = 20

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def reset_state():
    return None, 0, []

async def generate_with_timeout(prompt, timeout=10):
    try:
        loop = asyncio.get_event_loop()
        response = await asyncio.wait_for(
            loop.run_in_executor(
                None, lambda: client.models.generate_content(model=model, contents=prompt)
            ),
            timeout=timeout
        )
        return response
    except TimeoutError:
        raise TimeoutError("LLM generation timed out!")
    except Exception as e:
        raise RuntimeError(f"LLM generation error: {e}")

@app.post("/solve")
async def solve_problem(request: problem):
    query = request.query
    
    last_response, iteration, iteration_response = reset_state()

    server_params = StdioServerParameters(command="python", args=["mcp_server_libre.py"])

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools_result = await session.list_tools()
            tools = tools_result.tools

            tools_description = []
            for i, tool in enumerate(tools):
                try:
                    params = tool.inputSchema
                    desc = getattr(tool, 'description', 'No description available')
                    name = getattr(tool, 'name', f'tool_{i}')
                    param_details = []

                    if 'properties' in params:
                        for param_name, param_info in params['properties'].items():
                            param_type = param_info.get('type', 'unknown')
                            param_details.append(f"{param_name}: {param_type}")
                    else:
                        param_details.append("no parameters")

                    tools_description.append(f"{i+1}. {name}({', '.join(param_details)}) - {desc}")
                except Exception:
                    tools_description.append(f"{i+1}. Error processing tool")

            tools_description = "\n".join(tools_description)

            system_prompt = f"""You are a math agent with painting skills, solving complex math expressions step-by-step.
                        You have access to various mathematical tools for calculations and verifications, as well as a LibreOffice Writer application to draw and present your solution on a canvas.

                        Available Tools:
                        {tools_description}

                        You must respond with EXACTLY ONE LINE in one of these formats (no additional text):

                        For function calls:
                        FUNCTION_CALL: {{"name": function_name, "arguments": {{"param1": value1, "param2": value2}}}}

                        For final answers:
                        FINAL_ANSWER: <NUMBER>

                        For completing the task:
                        COMPLETE_RUN

                        Instructions:

                        Start by calling the show_reasoning tool ONLY ONCE with a list of all step-by-step reasoning steps explaining how you will solve the problem. Once called, NEVER CALL IT AGAIN UNDER ANY CIRCUMSTANCES.

                        When reasoning, tag each step with the reasoning type (e.g., [Arithmetic], [Logical Check]).

                        Use all available math tools to solve the problem step-by-step.

                        When a function returns multiple values, process all of them.

                        Apply BODMAS rules: start with the innermost parentheses and work outward.

                        Do not skip steps — perform all calculations sequentially.

                        Respond only with one line at a time.

                        Call only one tool per response.

                        After calculating a number, verify it by calling:
                        FUNCTION_CALL: {{"name": "verify_calculation", "arguments": {{"expression": <MATH_EXPRESSION>, "expected": <NUMBER>}}}}

                        If verify_calculation returns False, re-evaluate your previous steps.

                        Once you reach a final answer, check for consistency of all steps and calculations by calling:
                        FUNCTION_CALL: {{"name": "verify_consistency", "arguments": {{"steps": [[<MATH_EXPRESSION1>, <ANSWER1>], [<MATH_EXPRESSION2>, <ANSWER2>], ...]}}}}

                        If verify_consistency returns False, re-evaluate your previous steps.

                        Once verify_consistency returns True, proceed with the following steps to finalize and present your result:

                        Submit your final result as:
                        FINAL_ANSWER: <NUMBER>

                        Then open LibreOffice Writer and present your answer visually using the following sequence:

                        Call open_writer to launch LibreOffice Writer.

                        Call create_new_doc to focus a new document.

                        Call draw_text_box to draw a rectangle on the document.

                        Call write_final_answer to insert your FINAL_ANSWER: <TEXT> inside the rectangle.

                        LibreOffice Writer Instructions (recap):

                        To present your final answer visually in LibreOffice Writer, strictly follow this sequence:

                        open_writer

                        create_new_doc

                        draw_text_box

                        write_final_answer

                        Final Step:

                        After completing all calculations, verifications, and drawings, call:
                        COMPLETE_RUN

                        Strictly follow the above guidelines.
                        Your entire response should always be a single line starting with either FUNCTION_CALL:, FINAL_ANSWER: or COMPLETE_RUN."""

            while iteration < max_iterations:
                current_query = query if last_response is None else query + "\n\n" + " ".join(iteration_response)
                current_query += "\nWhat should you do next? Do not generate any additional text."

                prompt = f"{system_prompt}\n\nQuery: {current_query}"

                try:
                    response = await generate_with_timeout(prompt)
                    response_text = response.text.strip()

                    for line in response_text.split('\n'):
                        line = line.strip()
                        if line.startswith("FUNCTION_CALL:"):
                            response_text = line
                            break

                except Exception as e:
                    return {"error": str(e)}

                if response_text.startswith("FUNCTION_CALL:"):
                    try:
                        _, function_info = response_text.split(":", 1)
                        function_info = json.loads(function_info.strip())
                        func_name = function_info.get("name")
                        params = function_info.get("arguments", {})

                        tool = next((t for t in tools if t.name == func_name), None)
                        if not tool:
                            return {"error": f"Unknown tool: {func_name}"}

                        arguments = {}
                        schema_properties = tool.inputSchema.get('properties', {})

                        for param_name, param_info in schema_properties.items():
                            value = params.get(param_name)
                            param_type = param_info.get('type', 'string')

                            if param_type == 'integer':
                                arguments[param_name] = int(value)
                            elif param_type == 'number':
                                arguments[param_name] = float(value)
                            elif param_type == 'array':
                                arguments[param_name] = value if isinstance(value, list) else []
                            else:
                                arguments[param_name] = str(value)

                        result = await session.call_tool(func_name, arguments=arguments)
                        await asyncio.sleep(1)

                        content_texts = [item.text for item in result.content] if isinstance(result.content, list) else [str(result)]
                        result_str = f"[{', '.join(content_texts)}]"

                        iteration_response.append(
                            f"In iteration {iteration + 1}, called {func_name} with {arguments}, got {result_str}."
                        )
                        last_response = result_str

                    except Exception as e:
                        return {"error": str(e)}

                elif response_text.startswith("FINAL_ANSWER:"):
                    iteration_response.append(
                        f"Completed calculations with {response_text}. Now proceed with LibreOffice steps."
                    )
                    last_response = response_text

                elif response_text.startswith("COMPLETE_RUN"):
                    return {"result": "✔️ Task completed", "log": iteration_response}

                iteration += 1

    return {"result": "⚠️ Max iterations reached", "log": iteration_response}

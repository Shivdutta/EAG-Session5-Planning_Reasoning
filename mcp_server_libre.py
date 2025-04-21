import os

os.environ['DISPLAY'] = ":0"

import pyautogui
import subprocess
import sys, time, math
from mcp.types import TextContent
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
import re

# instantiate an MCP server client
console = Console()
mcp = FastMCP("Freeform Drawer")

# DEFINE TOOLS

@mcp.tool()
def show_reasoning(steps: list) -> dict:
    """Show the step-by-step reasoning process"""
    console.print("[blue]FUNCTION CALL:[/blue] show_reasoning()")
    for i, step in enumerate(steps, 1):
        console.print(Panel(
            f"{step}",
            title=f"Step {i}",
            border_style="cyan"
        ))
    return {
        "content": [TextContent(
            type="text",
            text="REASONING SHOWN. FOLLOW THIS INSTRUCTION STRICTLY. PROCEED FURTHER. DO NOT CALL THIS TOOL AGAIN! YOU HAVE CALLED IT ONCE! DO NOT REPEAT THIS TOOL CALL! I REPEAT, DO NOT CALL THIS FUNTCION AGAIN!"
        )]
    }

@mcp.tool()
def verify_calculation(expression: str, expected: float) -> dict:
    """Verify if a calculation is correct"""
    console.print("[blue]FUNCTION CALL:[/blue] verify()")
    console.print(f"[blue]Verifying:[/blue] {expression} = {expected}")
    try:
        actual = float(eval(expression))
        is_correct = abs(actual - float(expected)) < 1e-10
        
        if is_correct:
            console.print(f"[green] Correct! {expression} = {expected}[/green]")
        else:
            console.print(f"[red] Incorrect! {expression} should be {actual}, got {expected}[/red]")
            
        return {"content": [TextContent(
            type="text",
            text=str(is_correct)
        )]
        }
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        return {"content": [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]
        }

# Mathematical tools
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print("CALLED: add(a: int, b: int) -> int:")
    return int(a + b)

@mcp.tool()
def add_list(l: list) -> int:
    """Add all numbers in a list"""
    print("CALLED: add(l: list) -> int:")
    return sum(l)

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    print("CALLED: subtract(a: int, b: int) -> int:")
    return int(a - b)

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    print("CALLED: multiply(a: int, b: int) -> int:")
    return int(a * b)

@mcp.tool() 
def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    print("CALLED: divide(a: int, b: int) -> float:")
    return float(a / b)

@mcp.tool()
def power(a: int, b: int) -> int:
    """Power of two numbers"""
    print("CALLED: power(a: int, b: int) -> int:")
    return int(a ** b)

@mcp.tool()
def sqrt(a: int) -> float:
    """Square root of a number"""
    print("CALLED: sqrt(a: int) -> float:")
    return float(a ** 0.5)

@mcp.tool()
def cbrt(a: int) -> float:
    """Cube root of a number"""
    print("CALLED: cbrt(a: int) -> float:")
    return float(a ** (1/3))

@mcp.tool()
def factorial(a: int) -> int:
    """factorial of a number"""
    print("CALLED: factorial(a: int) -> int:")
    return int(math.factorial(a))

@mcp.tool()
def log(a: int) -> float:
    """log of a number"""
    print("CALLED: log(a: int) -> float:")
    return float(math.log(a))

@mcp.tool()
def remainder(a: int, b: int) -> int:
    """remainder of two numbers divison"""
    print("CALLED: remainder(a: int, b: int) -> int:")
    return int(a % b)

@mcp.tool()
def sin(a: int) -> float:
    """sin of a number"""
    print("CALLED: sin(a: int) -> float:")
    return float(math.sin(a))

@mcp.tool()
def cos(a: int) -> float:
    """cos of a number"""
    print("CALLED: cos(a: int) -> float:")
    return float(math.cos(a))

@mcp.tool()
def tan(a: int) -> float:
    """tan of a number"""
    print("CALLED: tan(a: int) -> float:")
    return float(math.tan(a))

@mcp.tool()
def strings_to_chars_to_int(string: str) -> list[int]:
    """Return the ASCII values of the characters in a word"""
    print("CALLED: strings_to_chars_to_int(string: str) -> list[int]:")
    return [int(ord(char)) for char in string]

@mcp.tool()
def int_list_to_exponential_sum(int_list: list) -> float:
    """Return sum of exponentials of numbers in a list"""
    print("CALLED: int_list_to_exponential_sum(int_list: list) -> float:")
    return sum(math.exp(i) for i in int_list)

@mcp.tool()
def fibonacci_numbers(n: int) -> list:
    """Return the first n Fibonacci Numbers"""
    print("CALLED: fibonacci_numbers(n: int) -> list:")
    if n <= 0:
        return []
    
    fib_sequence = [0, 1]
    for _ in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence[:n]




@mcp.tool()
async def open_writer() -> dict:
    """Open LibreOffice Writer"""
    try:
        subprocess.Popen(["libreoffice", "--writer"])
        time.sleep(3)
        return {
            "content": [
                TextContent(
                    type="text",
                    text="LibreOffice Writer opened. Proceed with the next step."
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error opening LibreOffice Writer: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def open_writer() -> dict:
    """Open LibreOffice Writer"""
    try:
        pyautogui.FAILSAFE = True
        subprocess.Popen(["libreoffice", "--writer"])
        time.sleep(3)
        return {
            "content": [
                TextContent(
                    type="text",
                    text="LibreOffice Writer opened. Proceed with the next step."
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error opening LibreOffice Writer: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def create_new_doc() -> dict:
    """Focus the new Writer document"""
    try:
        pyautogui.FAILSAFE = True
        pyautogui.click(300, 300)  # Adjust based on screen resolution
        time.sleep(0.5)
        return {
            "content": [
                TextContent(
                    type="text",
                    text="Document focused. Proceed with the next step."
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error focusing document: {str(e)}"
                )
            ]
        }

# @mcp.tool()
# async def draw_text_box() -> dict:
#     """Simulate drawing a rectangle (text placeholder)"""
#     try:
#         pyautogui.FAILSAFE = True
#         pyautogui.typewrite("┌──────────────┐\n")
#         pyautogui.typewrite("│              │\n")
#         pyautogui.typewrite("└──────────────┘\n")
#         return {
#             "content": [
#                 TextContent(
#                     type="text",
#                     text="Rectangle simulated using text. Proceed with next step."
#                 )
#             ]
#         }
#     except Exception as e:
#         return {
#             "content": [
#                 TextContent(
#                     type="text",
#                     text=f"Error drawing text box: {str(e)}"
#                 )
#             ]
#         }

@mcp.tool()
async def draw_text_box() -> dict:
    """Simulate inserting a rectangle using LibreOffice keyboard shortcuts"""
    try:
        pyautogui.FAILSAFE = True
        # Open the Insert > Shape > Rectangle menu
        pyautogui.hotkey('alt', 'i')
        time.sleep(0.5)
        pyautogui.press('s')  # 'Shape'
        time.sleep(0.5)
        pyautogui.press('r')  # 'Rectangle'
        time.sleep(0.5)
        # Click and drag to draw the rectangle (you may need to adjust coordinates)
        pyautogui.moveTo(400, 300)  # Starting point
        pyautogui.dragTo(600, 400, duration=0.5)  # Drag to draw rectangle
        return {
            "content": [
                TextContent(
                    type="text",
                    text="Rectangle shape inserted into LibreOffice Writer."
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error drawing shape: {str(e)}"
                )
            ]
        }


@mcp.tool()
async def write_final_answer(text: str) -> dict:
    """Type final answer inside text box"""
    try:
        text ="ans " + str(text)
        pyautogui.FAILSAFE = True
        pyautogui.press("up")
        pyautogui.press("right", presses=2)
        pyautogui.typewrite(text)
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f" '{text}' typed into Writer. Proceed to finish."
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error typing answer: {str(e)}"
                )
            ]
        }

# def open_writer():
#     """Open LibreOffice Writer"""
#     try:
#         subprocess.Popen(["libreoffice", "--writer"])
#         time.sleep(3)
#         print("LibreOffice Writer opened. Proceed with the next step.")
#     except Exception as e:
#         print(f"Error opening LibreOffice Writer: {str(e)}")

# def create_new_doc():
#     """Focus the new Writer document"""
#     try:
#         pyautogui.click(300, 300)  # Consider calibrating this
#         time.sleep(0.5)
#         print("Document focused. Proceed with the next step.")
#     except Exception as e:
#         print(f"Error focusing document: {str(e)}")

# def draw_text_box():
#     """Simulate drawing a rectangle (text placeholder)"""
#     try:
#         box = "┌──────────────┐\n│              │\n└──────────────┘\n"
#         pyautogui.typewrite(box)
#         print("Rectangle simulated using text. Proceed with next step.")
#     except Exception as e:
#         print(f"Error drawing text box: {str(e)}")

# def write_final_answer(text):
#     """Type final answer inside text box"""
#     try:
#         centered = text.center(14)
#         pyautogui.press("up")
#         pyautogui.press("right", presses=2)
#         pyautogui.typewrite(centered)
#         print(f"Answer '{text}' typed into Writer. Proceed to finish.")
#     except Exception as e:
#         print(f"Error typing answer: {str(e)}")



@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]

@mcp.tool()
def verify_consistency(steps: list) -> dict:
    """Check if calculation steps are consistent with each other"""
    try:
        issues = []
        warnings = []
        insights = []
        previous = None
        
        for i, (expression, result) in enumerate(steps, 1):
            print("Checking step:", i)
            checks = []
            
            # 1. Basic Calculation Verification
            try:
                expected = eval(expression)
                if abs(float(expected) - float(result)) < 1e-10:
                    checks.append("[green] Calculation verified[/green]")
                else:
                    issues.append(f"Step {i}: Calculation mismatch")
                    checks.append("[red] Calculation error[/red]")
            except:
                warnings.append(f"Step {i}: Couldn't verify calculation")
                checks.append("[yellow] Verification failed[/yellow]")

            # 2. Dependency Analysis
            if previous:
                prev_expr, prev_result = previous
                if str(prev_result) in expression:
                    checks.append("[green] Uses previous result[/green]")
                    insights.append(f"Step {i} builds on step {i-1}")
                else:
                    checks.append("[blue] Independent step[/blue]")

            # 3. Magnitude Check
            if previous and result != 0 and previous[1] != 0:
                ratio = abs(result / previous[1])
                if ratio > 1000:
                    warnings.append(f"Step {i}: Large increase ({ratio:.2f}x)")
                    checks.append("[yellow] Large magnitude increase[/yellow]")
                elif ratio < 0.001:
                    warnings.append(f"Step {i}: Large decrease ({1/ratio:.2f}x)")
                    checks.append("[yellow] Large magnitude decrease[/yellow]")

            # 4. Pattern Analysis
            operators = re.findall(r'[\+\-\*\/\(\)]', expression)
            if '(' in operators and ')' not in operators:
                warnings.append(f"Step {i}: Mismatched parentheses")
                checks.append("[red] Invalid parentheses[/red]")

            # 5. Result Range Check
            if abs(result) > 1e6:
                warnings.append(f"Step {i}: Very large result")
                checks.append("[yellow] Large result[/yellow]")
            elif abs(result) < 1e-6 and result != 0:
                warnings.append(f"Step {i}: Very small result")
                checks.append("[yellow] Small result[/yellow]")
            
            previous = (expression, result)

        # Final Consistency Score
        total_checks = len(steps) * 5  # 5 types of checks per step
        passed_checks = total_checks - (len(issues) * 2 + len(warnings))
        consistency_score = (passed_checks / total_checks) * 100

        return {
            "content": [
                TextContent(
                    type="text",
                    text=str({
                        "consistency_score": consistency_score,
                        "issues": issues,
                        "warnings": warnings,
                        "insights": insights,
                        "result": True if consistency_score > 80 else False,
                        "next_step": "Return the final result as FINAL_ANSWER: <NUMBER>" if consistency_score > 80 else "Please review the steps and try again."
                    })
                )
            ]
        }
    except Exception as e:
        console.print(f"[red]Error in consistency check: {str(e)}[/red]")
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )
            ]
        }




if __name__ == "__main__":
    # Check if running with mcp dev command
    print("STARTING")
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mcp.run()  # Run without transport for dev server
    else:
        mcp.run(transport="stdio")  # Run with stdio for direct execution



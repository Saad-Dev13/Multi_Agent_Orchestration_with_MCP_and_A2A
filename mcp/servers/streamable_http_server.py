from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field


class ArithmeticInput(BaseModel):
    """
    A Pydantic model for arithmetic input.
    """
    a: float = Field(..., description="The first number for the arithmetic operation.")
    b: float = Field(..., description="The second number for the arithmetic operation.")
    
class ArithmeticOutput(BaseModel):
    """
    A Pydantic model for arithmetic output.
    """
    result: float = Field(..., description="The result of the arithmetic operation.")
    expression: str = Field(..., description="The arithmetic expression that was evaluated.")


mcp = FastMCP(
    "arithmetic_server",
    host="localhost",
    port=3000,
    stateless_http=True,

)

@mcp.tool()
async def add_numbers(input:ArithmeticInput) -> ArithmeticOutput:
    """
    Add two numbers and return the result along with the expression.

    Args:
        input (ArithmeticInput): The input containing two numbers to add.

    Returns:
        ArithmeticOutput: The output containing the result and the expression.
    """
    result = input.a + input.b
    expression = f"{input.a} + {input.b} = {result}"
    return ArithmeticOutput(result=result, expression=expression)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
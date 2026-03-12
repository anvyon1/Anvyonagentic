"""Tool Registry - Register and execute tools"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Any, Callable, Optional
from datetime import datetime


@dataclass
class ToolParameter:
    """Parameter definition for a tool"""
    name: str
    type: str
    description: str
    required: bool = True
    default: Any = None


@dataclass
class Tool:
    """Tool definition"""
    name: str
    description: str
    category: str
    parameters: List[ToolParameter] = field(default_factory=list)
    execute_fn: Optional[Callable] = None
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool with given parameters"""
        if self.execute_fn:
            return self.execute_fn(params)
        return {"success": False, "error": "No execute function defined"}


class ToolRegistry:
    """Registry for managing tools"""
    
    def __init__(self):
        self._tools: Dict[str, Tool] = {}
        self._register_builtin_tools()
    
    def register(self, tool: Tool) -> None:
        """Register a new tool"""
        self._tools[tool.name] = tool
    
    def unregister(self, name: str) -> bool:
        """Unregister a tool"""
        if name in self._tools:
            del self._tools[name]
            return True
        return False
    
    def get(self, name: str) -> Optional[Tool]:
        """Get a tool by name"""
        return self._tools.get(name)
    
    def list(self) -> List[Tool]:
        """List all registered tools"""
        return list(self._tools.values())
    
    def execute(self, name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool by name"""
        tool = self._tools.get(name)
        if not tool:
            return {"success": False, "error": f"Tool '{name}' not found"}
        return tool.execute(params)
    
    def get_descriptions(self) -> str:
        """Get formatted descriptions of all tools"""
        if not self._tools:
            return "No tools registered"
        
        lines = []
        for tool in self._tools.values():
            params = ", ".join(f"{p.name}: {p.type}" for p in tool.parameters)
            lines.append(f"- {tool.name}({params}): {tool.description}")
        return "\n".join(lines)
    
    def _register_builtin_tools(self):
        """Register built-in tools"""
        
        self.register(Tool(
            name="calculate",
            description="Perform basic mathematical calculations",
            category="compute",
            parameters=[ToolParameter("expression", "string", "Math expression to evaluate")],
            execute_fn=self._calculate
        ))
        
        self.register(Tool(
            name="datetime",
            description="Get current date and time",
            category="utility",
            parameters=[ToolParameter("format", "string", "Date format", required=False, default="iso")],
            execute_fn=self._datetime
        ))
        
        self.register(Tool(
            name="text_transform",
            description="Transform text (uppercase, lowercase, reverse)",
            category="text",
            parameters=[
                ToolParameter("text", "string", "Text to transform"),
                ToolParameter("operation", "string", "Operation: upper, lower, reverse")
            ],
            execute_fn=self._text_transform
        ))
        
        self.register(Tool(
            name="json_parse",
            description="Parse and validate JSON",
            category="data",
            parameters=[ToolParameter("json_string", "string", "JSON string to parse")],
            execute_fn=self._json_parse
        ))
        
        self.register(Tool(
            name="web_search",
            description="Search the web (simulated)",
            category="search",
            parameters=[ToolParameter("query", "string", "Search query")],
            execute_fn=self._web_search
        ))
    
    def _calculate(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Safe math expression evaluator"""
        try:
            expr = str(params.get("expression", params.get("input", "")))
            
            if not re.match(r'^[\d\s+\-*/().^%]+$', expr):
                return {"success": False, "error": "Invalid characters in expression"}
            
            sanitized = expr.replace("^", "**")
            result = eval(sanitized, {"__builtins__": {}}, {})
            
            return {"success": True, "data": {"result": result}}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _datetime(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get current datetime"""
        fmt = params.get("format", "iso")
        now = datetime.now()
        
        if fmt == "iso":
            result = now.isoformat()
        elif fmt == "date":
            result = now.strftime("%Y-%m-%d")
        elif fmt == "time":
            result = now.strftime("%H:%M:%S")
        else:
            result = now.strftime(fmt)
        
        return {"success": True, "data": {"datetime": result, "timestamp": now.timestamp()}}
    
    def _text_transform(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Transform text"""
        text = str(params.get("text", params.get("input", "")))
        operation = params.get("operation", "upper").lower()
        
        if operation == "upper":
            result = text.upper()
        elif operation == "lower":
            result = text.lower()
        elif operation == "reverse":
            result = text[::-1]
        else:
            return {"success": False, "error": f"Unknown operation: {operation}"}
        
        return {"success": True, "data": {"result": result, "original": text}}
    
    def _json_parse(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Parse JSON string"""
        import json
        try:
            json_str = params.get("json_string", params.get("input", "{}"))
            data = json.loads(json_str)
            return {"success": True, "data": {"parsed": data, "valid": True}}
        except json.JSONDecodeError as e:
            return {"success": False, "error": f"Invalid JSON: {e}"}
    
    def _web_search(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Simulated web search"""
        query = params.get("query", params.get("input", ""))
        return {
            "success": True,
            "data": {
                "query": query,
                "results": [
                    {"title": f"Result for: {query}", "snippet": "Simulated search result"}
                ],
                "note": "This is a simulated search. Integrate a real search API for production."
            }
        }

import subprocess
import io
import sys
from global_lib import global_namespace

    
class ExecuteJavascriptCode:
    def __init__(self):
        self.compiled_result = None
    def execute_js(self,js_code):
        try: 
            result = subprocess.run(["node", "-e",js_code], capture_output=True, text=True)
                        
            if result.returncode == 0:
                self.compiled_result = result.stdout.strip()
                return self.compiled_result        
        except:
            self.last_output = None
            return result.stderr.strip()
    
    
class ExecutePythonCode:
    def __init__(self):
        self.compiled_code = None

    def execute_python_code(self, py_code):
        # print(f"Received code type: {py_code}")  # Debugging print
        
        result = {}
        captured_output = io.StringIO()  
        
        old_stdout = sys.stdout
        sys.stdout = captured_output
        
        global_namespace = {"__builtins__": __builtins__}  # Isolate execution
        
        try:
            exec(py_code, global_namespace)  # Executes the code
            # if 'test' in global_namespace and callable(global_namespace['test']):
            #     result['function_output'] = global_namespace['test']()  # Call function if exists
        except Exception as e:
            result['error'] = str(e)
        finally:
            sys.stdout = old_stdout
        
        self.compiled_code = captured_output.getvalue().strip()
        print(result)
        result['output'] = self.compiled_code
        if "error" in result:            
            return result["error"]
        else:
            return result["output"]
    



def initiate_compile(code,language):
    if(language=="javascript"):
        code_res = ExecuteJavascriptCode()
        res = code_res.execute_js(code)
        print(res)
        return res
        
    elif(language=="python"):
        code_res = ExecutePythonCode()
        res = code_res.execute_python_code(code)
        # print(res)
        return res
    else:
        return"some error hapend"
    
    

# # Example Usage
# code = """
# def test():
#     return 34

# print(test())
# """
# print(execute_python_code(code))
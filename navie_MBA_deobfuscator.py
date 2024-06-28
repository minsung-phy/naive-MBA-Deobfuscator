import ast
import subprocess
import sys
import time

class ExprTransformer(ast.NodeVisitor):
    def __init__(self):
        self.variables = set()
        self.has_unary_minus = False

    def visit_BinOp(self, node):
        self.generic_visit(node)

    def visit_UnaryOp(self, node):
        if isinstance(node.op, ast.USub):
            self.has_unary_minus = True
        self.generic_visit(node)

    def visit_Name(self, node):
        self.variables.add(node.id)

    def visit_Constant(self, node):
        pass

def convert_expr_to_sygus(expr):
    tree = ast.parse(expr, mode='eval')
    return convert_node_to_sygus(tree.body)

def convert_node_to_sygus(node):
    if isinstance(node, ast.BinOp):
        left = convert_node_to_sygus(node.left)
        right = convert_node_to_sygus(node.right)
        op = convert_op_to_sygus(node.op)
        return f"({op} {left} {right})"
    elif isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Constant):
        return str(node.value)
    else:
        raise ValueError(f"Unsupported node type: {type(node)}")

def convert_op_to_sygus(op):
    if isinstance(op, ast.Add):
        return '+'
    elif isinstance(op, ast.Sub):
        return '-'
    elif isinstance(op, ast.Mult):
        return '*'
    elif isinstance(op, ast.Div):
        return '/'
    elif isinstance(op, ast.Mod):
        return '%'
    elif isinstance(op, ast.BitOr):
        return '|'
    elif isinstance(op, ast.BitAnd):
        return '&'
    elif isinstance(op, ast.BitXor):
        return '^'
    elif isinstance(op, ast.LShift):
        return '<<'
    elif isinstance(op, ast.RShift):
        return '>>'
    
def generate_sygu_file(expr, file_path):
    transformer = ExprTransformer()
    transformer.visit(ast.parse(expr, mode='eval'))
    
    sygus_content = "(set-logic LIA)\n"

    sygus_content += f"""
(define-fun f ({' '.join(['(' + var + ' Int)' for var in transformer.variables])}) Int
    {convert_expr_to_sygus(expr)}
)

(synth-fun df ({' '.join(['(' + var + ' Int)' for var in transformer.variables])}) Int
    (
        (Start Int
            (
                (+ Start Start)
                (- Start Start)
                (* Start Start)
                {' '.join(transformer.variables)}
                0 1
            )
        )
    )
)
"""
    
    for var in transformer.variables:
        sygus_content += f"(declare-var {var} Int)\n"   
    
    sygus_content += f"""
(constraint (= (f {' '.join(transformer.variables)}) (df {' '.join(transformer.variables)})))
(check-synth)
"""

    with open(file_path, 'w') as f:
        f.write(sygus_content)
    return len(transformer.variables) + 2  # +2 for the outermost function definition and the synth-fun line

def run_duet(sygus_file_path):
    start_time = time.time()
    try:
        result = subprocess.run(['/experiment/duet/main.native', '-z3cli',  sygus_file_path], timeout=20, capture_output=True, text=True)
        if result.returncode == 0:
            print("Synthesis Successful.")
        else:
            print("Synthesizer Error.")
    except subprocess.TimeoutExpired:
        print("Synthesizer Timed out.")

def main(expr):
    tree = ast.parse(expr, mode='eval')
    node_count = count_nodes(tree)
    print(f"Size of input expr : {node_count}")

    sygus_file_path = "./output.sl"
    expr_size = generate_sygu_file(expr, sygus_file_path)
    print(f"SyGuS File written to : {sygus_file_path}")
    
    run_duet(sygus_file_path)

def count_nodes(node):
    count = 1  # 현재 노드를 포함하므로 1부터 시작
    for child in ast.iter_child_nodes(node):
        count += count_nodes(child)
    return count

if __name__ == "__main__":
    expr = sys.argv[1]
    main(expr)
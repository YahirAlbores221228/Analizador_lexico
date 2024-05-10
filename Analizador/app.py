import ply.lex as lex
from flask import Flask, render_template, request

app = Flask(__name__)

# lista de mis tokens reservados
reserved = {
    'for': 'FOR',
    'if': 'IF',
    'do': 'DO',
    'while': 'WHILE',
    'else': 'ELSE'
}

# tokens no reservado
tokens = [
    'OPEN',
    'CLOSE',
    'IDENTIFIER'
] + list(reserved.values())

t_FOR = r'for'
t_IF = r'if'
t_DO = r'do'
t_WHILE = r'while'
t_ELSE = r'else'
t_OPEN= r'\('
t_CLOSE = r'\)'

t_ignore = ' \t\n\r'

def t_identifier(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'IDENTIFIER')
    return t

def t_error(t):
    print('Caracter no válido: ', t.value[0])
    t.lexer.skip(1)
    
lexer = lex.lex()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code = request.form.get('code', '')
        file = request.files.get('file')
        if file:
            content = file.read().decode('utf-8') 
        elif code:
            content = code
        else:
            content = ''
        lexer.input(content)
        result_lexema = []
        for token in lexer:
            if token.type in reserved.values():
                result_lexema.append((f"Palabra reservada {token.type}", token.value))
            elif token.type == 'OPEN':
                result_lexema.append(("Parentesis de apertura", token.value))
            elif token.type == 'CLOSE':
                result_lexema.append(("Parentesis de cierre", token.value))
            elif token.type == 'IDENTIFIER':
                result_lexema.append(("Identificador", token.value))
        return render_template('Home.html', tokens=result_lexema)
    return render_template('Home.html', tokens=None)

if __name__ == "__main__":
    app.run(debug=True)

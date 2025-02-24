import re

r""" Padrões encontrados
1. Apanha o titulo h1: (?<!#)#([^#].+) -> 1 grupo
2. Apanha o subtitulo h2: (?<!#)#{2}([^#].+) -> 1 grupo
3. Apanha o menor cabeçalho h3: (?<!#)#{3}([^#].+) -> 1 grupo
4. Apanha negrito: \*{2}(.+?)\*{2} -> 1 grupo
5. Apanha italico: (?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*) -> 1 grupo
\d\.(.+)
7. Apanha links referenciados: (?<!\!)\[(.+)\]\((.+)\) -> 2 grupos
8. Apanha as imagens: \!\[(.+)\]\((.+)\) -> 2 grupos
"""

def convert_markdown_to_html(in_md):
    in_md = re.sub(r"(?<!#)#([^#].+)", r"<h1>\1</h1>", in_md)  # h1
    in_md = re.sub(r"(?<!#)#{2}([^#].+)", r"<h2>\1</h2>", in_md)  # h2
    in_md = re.sub(r"(?<!#)#{3}([^#].+)", r"<h3>\1</h3>", in_md)  # h3
    in_md = re.sub(r"\*{2}(.+?)\*{2}", r"<b>\1</b>", in_md) # Bold
    in_md = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", in_md) # Italic
    in_md = re.sub(r"(?<!\!)\[(.+)\]\((.+)\)", r'<a href="\2">\1</a>', in_md) # Links
    in_md = re.sub(r"\!\[(.+)\]\((.+)\)", r'<img src="\2" alt="\1" />', in_md) # Images
    
    check_if_in_ol = False
    lines = in_md.splitlines()
    out_html = []
    
    for line in lines:
        match = re.match(r'^\d+\. (.+)', line)
        
        if match:
            if not check_if_in_ol:
                out_html.append("<ol>")
                check_if_in_ol = True
            out_html.append(f"<li>{match.group(1)}</li>")
        elif check_if_in_ol:
            out_html.append("</ol>\n")
            check_if_in_ol = False
        
        elif not match:
            out_html.append(line)
    
    if check_if_in_ol:
        out_html.append("</ol>")
    
    return "\n".join(out_html)

def main():
    markdown_file_path = r'files/input.md'
    try:
        with open(markdown_file_path, 'r', encoding='utf-8') as file:
            markdown_content = file.read()
        
        html_output = convert_markdown_to_html(markdown_content)
        
        with open(r'files/output.html', 'w', encoding='utf-8') as html_file:
            html_file.write(html_output)
        
    except FileNotFoundError:
        print(f"Error: O ficheiro '{markdown_file_path}' não existe.")
    except Exception as e:
        print(f"{e}")

if __name__ == "__main__":
    main()
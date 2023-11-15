"""
    TODO
"""
##########==========##########==========##########==========##########==========##########==========
## INITIALIZATION

## imports
import textwrap
import plotly.graph_objects as go

## parameters
params = {
    'dark': '#663D14', 'light': '#FFF9F2',
}

##########==========##########==========##########==========##########==========##########==========
## COMPONENT FUNCTIONS


##########==========##########==========##########==========##########==========##########==========
## TOP-LEVEL FUNCTION

def make(loc = 'in/a2_project_text.txt'):
    txt = open(loc, 'rt').read()
    txt = txt.split('<x>\n\n</x>')
    txt = {i.split('</b>')[0].strip('<b>'):i for i in txt}
    txt = {i:'<br>'.join(textwrap.wrap(txt[i], width = 45)) for i in txt.keys()}
    txt = {i:txt[i].replace('<n>', '<br><br>') for i in txt.keys()}
    return txt

def draw(xy, txt):
    fig = go.Figure()
    fig = fig.update_layout(
        plot_bgcolor  = params['light'], paper_bgcolor = params['light'],
        font = dict(size = 12, color = params['dark']),
        yaxis = dict(visible = False, range = (0, 1)),
        xaxis = dict(visible = False, range = (0, 1))
        )
    fig = fig.add_trace(go.Scatter(x = [xy[0]], y = [xy[1]], text = txt, mode = 'text'))
    fig.write_html(file = 'out/a2_project_text.html',full_html = True, include_plotlyjs = True)
    fig.write_html(file = 'out/a2_project_text.div',full_html = False, include_plotlyjs = False)
    div = open('out/a2_project_text.div', 'rt').read()
    return div

##########==========##########==========##########==========##########==========##########==========
## TEST CODE

if __name__ == '__main__':
    project_text = make()
    draw((0.5, 0.5), project_text['Panel Explainer'])


##########==========##########==========##########==========##########==========##########==========

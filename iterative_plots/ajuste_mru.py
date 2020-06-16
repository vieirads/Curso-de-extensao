# importando os pacotes ncessários
from bokeh.layouts  import row, column
from bokeh.models   import CustomJS, Slider, Legend
from bokeh.plotting import figure, ColumnDataSource
from bokeh.io       import save

import numpy as np

# definindo os dados
X_dados = np.asarray([0.000, 0.905, 1.833, 2.770, 3.684])
Y_dados = np.asarray([0.00 , 15.00, 30.00, 45.00, 60.00])

# dados a serem mudados iterativamente
t = X_dados
s = t

# cores a serem usadas no plot
COLOR_DADOS  = "#0095DD"
COLOR_AJUSTE = "#E34A33"

# cria display dinâmico de valores
TOOLTIPS_POSICAO = [
    ("Posição [cm]", "@y{0.00}"),
    ("Tempo [s]"   , "@x")
]

# cria a fonte dinâmica para representar o ajuste
source_posicao = ColumnDataSource(data=dict(x=t, y=s))

# cria a figura onde os dados e o ajuste serão mostrados
plot_posicao = figure(plot_width=400, plot_height=400, tooltips=TOOLTIPS_POSICAO, title='Ajuste da reta S(t) = a + bt.')

# plotando os dados
plot_posicao.line   (X_dados, Y_dados, color=COLOR_DADOS, legend='Dados', line_width=3)

plot_posicao.scatter(X_dados, Y_dados, color=COLOR_DADOS, legend='Dados', fill_color='#FFFFFF', size=18)


# plotando a reta de ajuste (dinâmica)
plot_posicao.line   ('x', 'y', source=source_posicao, color=COLOR_AJUSTE, legend='Ajuste', line_width=3, line_dash="5 5")


plot_posicao.scatter('x', 'y', source=source_posicao, color=COLOR_AJUSTE, legend='Ajuste', marker='x', size=16)


# definindo os labels do axis
plot_posicao.xaxis[0].axis_label = 'Tempo, t [s]'
plot_posicao.yaxis[0].axis_label = 'Posição, S(t) [cm]'

# mudando as fontes dos labels
FONT_SIZE = '16px'

plot_posicao.xaxis.axis_label_text_font_size  = FONT_SIZE
plot_posicao.xaxis.major_label_text_font_size = FONT_SIZE

plot_posicao.yaxis.axis_label_text_font_size  = FONT_SIZE
plot_posicao.yaxis.major_label_text_font_size = FONT_SIZE

plot_posicao.xaxis.axis_label_text_font_style = 'normal'
plot_posicao.yaxis.axis_label_text_font_style = 'normal'

# remove a barra lateral com o símbolo do bokeh
plot_posicao.toolbar.logo     = None
plot_posicao.toolbar_location = None

# mudando a legenda de lugar
plot_posicao.legend.location = 'top_left'

# criando os sliders
slider_posicao_inicial = Slider(start=-10, end=10, value=0, step=-0.01  , bar_color=COLOR_AJUSTE, title="Coeficiente linear, a")#orientation='vertical', direction='rtl')
slider_velocidade      = Slider(start=-20, end=20, value=5, step=-0.05  , bar_color=COLOR_AJUSTE, title="Coeficiente angular, b")#orientation='vertical', direction='rtl')

# cirando o callback para mudar a reta de ajuste dinamicamente
callback_ajuste = CustomJS(
    args=dict(
        source=source_posicao,
        velocidade=slider_velocidade,
        posicao_inicial=slider_posicao_inicial
    ),
    code="""
    const data = source.data;
    const v    = velocidade.value;
    const s0   = posicao_inicial.value;
    const t    = data['x'];
    const s    = data['y'];
    
    for (let i = 0; i < t.length; i++) {
    s[i] = s0 + v*t[i];
    }
    source.change.emit();
    """
)


# criando os sliders
slider_posicao_inicial.js_on_change('value', callback_ajuste)
slider_velocidade.     js_on_change('value', callback_ajuste)

# criando o layout de como ficará disposto o gráfico e os sliders
layout = row([
    plot_posicao,
    column([
        slider_posicao_inicial,
        slider_velocidade,
    ], sizing_mode='scale_width'
    ),
], sizing_mode='scale_width'
)

# salvando o layout
save(layout, f"ajuste_mru.html")
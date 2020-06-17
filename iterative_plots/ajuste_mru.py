# importando os pacotes ncessários
from bokeh.layouts  import row, column
from bokeh.models   import CustomJS, Slider, Legend, LabelSet
from bokeh.plotting import figure, ColumnDataSource
from bokeh.io       import save

import numpy as np

def coef_determinacao(y_dado, y_ajuste):
    # soma dos resíduos
    s_res = ((y_dado - y_ajuste)**2).sum()
    # soma total
    s_tot = ((y_dado - y_dado.mean())**2).sum()
    r2 = round(1 - s_res/s_tot, 3)
    # return r2
    if r2 >= 0:
        return r2
    else:
        return 'nan'

# definindo os dados
X_dados = np.asarray([0.000, 0.905, 1.833, 2.770, 3.684])
Y_dados = np.asarray([0.00 , 15.00, 30.00, 45.00, 60.00])

# dados a serem mudados iterativamente
t = X_dados
s = t

r2 = coef_determinacao(Y_dados, s)
dummy_texts = ['R2 = {}'.format(r2), '', '', '', '']
dummy_x = [0.1 for _ in X_dados]
dummy_y = [35  for _ in X_dados]

# cores a serem usadas no plot
COLOR_DADOS  = "#0095DD"
COLOR_AJUSTE = "#E34A33"

# cria display dinâmico de valores
TOOLTIPS_POSICAO = [
    ("Posição [cm]", "@y{0.00}"),
    ("Tempo [s]"   , "@x")
]

# cria a fonte dinâmica para representar o ajuste
source_posicao = ColumnDataSource(data=dict(x=t, y=s, dados=Y_dados, text=dummy_texts, posx=dummy_x, posy=dummy_y))

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

# criando o label
# citation = Label(x=10, y=90, x_units='screen', y_units='screen',
#                  text='R2 = {}'.format(r2), render_mode='css',
#                  border_line_color='black', border_line_alpha=1.0,
#                  background_fill_color='white', background_fill_alpha=1.0)

citation = LabelSet(x=1.5, y=55, text='text', source=source_posicao, render_mode='css', border_line_color='black', background_fill_color='white')

plot_posicao.add_layout(citation)

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
    const data  = source.data;
    const v     = velocidade.value;
    const s0    = posicao_inicial.value;
    const t     = data['x'];
    const s     = data['y'];
    const yDado = data['dados'];
    const text  = data['text'];

    
    for (let i = 0; i < t.length; i++) {
    s[i] = s0 + v*t[i];
    }

    let mean_value = (arr) => {
        let sum = 0;
        for (let i = 0; i < arr.length; i++) {
            sum += arr[i];
        }

        let mean = sum/arr.length;

        return mean;
    }

    let r2 = (y_dado, y_ajuste) => {
        let s_res = 0;
        let s_tot = 0;

        let mean_dado = mean_value(y_dado);

        for (let i = 0; i < y_dado.length; i++) {
            s_res += (y_dado[i] - y_ajuste[i])**2;
            s_tot += (y_dado[i] - mean_dado)**2;
        }

        let score = Math.round( (1 - s_res/s_tot)*1000 ) / 1000;

        if (score >= 0) {
            return score;
        } else {
            return 'nan';
        }

    }

    text[0] = `R2 = ${r2(yDado, s).toString()}`;

    source.change.emit();
    """
)


# criando os sliders
slider_posicao_inicial.js_on_change('value', callback_ajuste)
slider_velocidade.     js_on_change('value', callback_ajuste)
# citation.js_on_change('value', callback_ajuste)


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
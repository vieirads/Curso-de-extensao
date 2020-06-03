import numpy as np

from bokeh.layouts import row, column
from bokeh.models import CustomJS, Slider, Column, Row
from bokeh.plotting import figure, output_file, show, ColumnDataSource
# from bokeh.io import output_notebook

from bokeh.io import save

# output_notebook()

t = np.arange(0,16)
s = t
v = np.full(t.shape[0], 5)
a = np.full(t.shape[0], 0)

COLOR_POSICAO    = "#0095DD"
COLOR_VELOCIDADE = "#31A354"
COLOR_ACELERACAO = "#E34A33"

source_posicao    = ColumnDataSource(data=dict(x=t, y=s))
source_velocidade = ColumnDataSource(data=dict(x=t, y=v))
source_aceleracao = ColumnDataSource(data=dict(x=t, y=a))

# kwargs_plot = dict(plot_width=500, plot_height=700)
kwargs_plot = dict(plot_width=800, plot_height=380)

TOOLTIPS_POSICAO = [
    ("Posição [m]", "@y"),
    ("Tempo [s]"  , "@x")
]

TOOLTIPS_VELOCIDADE = [
    ("Velocidade [m/s]", "@y"),
    ("Tempo [s]"       , "@x")
]

TOOLTIPS_ACELERACAO = [
    ("Aceleração [m/s²]", "@y"),
    ("Tempo [s]"        , "@x")
]

plot_posicao = figure(
    y_range=(-550, 550),
    **kwargs_plot,
    title='Posição em funcão do tempo.',
    tooltips=TOOLTIPS_POSICAO
             )

plot_velocidade = figure(
    y_range=(-70, 70),
    **kwargs_plot,
    title='Velocidade em função do tempo.',
    tooltips=TOOLTIPS_VELOCIDADE
)

plot_aceleracao = figure(
    y_range=(-5,5),
    **kwargs_plot,
    title='Aceleração em função do tempo.',
    tooltips=TOOLTIPS_ACELERACAO
)

for counter, plot in enumerate([plot_posicao, plot_velocidade, plot_aceleracao]):
    FONT_SIZE = '16px'

    plot.xaxis.axis_label_text_font_size  = FONT_SIZE
    plot.xaxis.major_label_text_font_size = FONT_SIZE

    plot.yaxis.axis_label_text_font_size  = FONT_SIZE
    plot.yaxis.major_label_text_font_size = FONT_SIZE

    plot.xaxis.axis_label_text_font_style = 'normal'
    plot.yaxis.axis_label_text_font_style = 'normal'
        
    plot.xaxis[0].axis_label = 'Tempo, t [s]'

    plot.toolbar.logo     = None
    plot.toolbar_location = None
    
    if counter == 0:
        plot.yaxis[0].axis_label = 'Posição, s(t) [m]'
        plot.   line('x', 'y', source=source_posicao, color=COLOR_POSICAO, line_width=3, legend="Posição do carro")
        plot.scatter('x', 'y', source=source_posicao, color=COLOR_POSICAO, fill_color='#FFFFFF', size=10)
    elif counter == 1:
        plot.yaxis[0].axis_label = 'Velocidade, v [m/s]'
        plot.   line('x', 'y', source=source_velocidade, color=COLOR_VELOCIDADE, line_width=3, legend="Velocidade do carro")
        plot.scatter('x', 'y', source=source_velocidade, color=COLOR_VELOCIDADE, fill_color='#FFFFFF', size=10)
    elif counter == 2:
        plot.yaxis[0].axis_label = 'Aceleração, a [m/s²]'
        plot.   line('x', 'y', source=source_aceleracao, color=COLOR_ACELERACAO, line_width=3, legend="Aceleração do carro")
        plot.scatter('x', 'y', source=source_aceleracao, color=COLOR_ACELERACAO, fill_color='#FFFFFF', size=10)

    plot.legend.location = 'top_left'



slider_posicao_inicial = Slider(start=-50, end=50, value=0, step=1  , bar_color=COLOR_POSICAO   , title=r"Posição inicial [m]")
slider_velocidade      = Slider(start=-10, end=10, value=5, step=1  , bar_color=COLOR_VELOCIDADE, title=r"Velocidade [m/s]"   )
slider_aceleracao      = Slider(start=-3 , end=3 , value=0, step=0.5, bar_color=COLOR_ACELERACAO, title=r"Aceleração [m/s²]"  )

callback_posicao = CustomJS(
        args=dict(
            source=source_posicao,
            aceleracao=slider_aceleracao,
            velocidade=slider_velocidade,
            posicao_inicial=slider_posicao_inicial,
        ),
        code="""
        const data = source.data;
        const v    = velocidade.value;
        const a    = aceleracao.value;
        const s0   = posicao_inicial.value;
        const t    = data['x'];
        const s  = data['y'];
        for (let i = 0; i < t.length; i++) {
            s[i] = s0 + v*t[i] + 0.5*a*(t[i]**2);
        }
        source.change.emit()
"""
)

callback_velocidade = CustomJS(
    args=dict(
        source=source_velocidade,
        aceleracao=slider_aceleracao,
        velocidade=slider_velocidade
    ),
    code="""
    const data = source.data;
    const v    = velocidade.value;
    const a    = aceleracao.value;
    const t    = data['x'];
    const v_t  = data['y'];
    
    for (let i = 0; i < t.length; i++) {
        v_t[i] = v + a*t[i];
    }
    source.change.emit();
    """
)

callback_aceleracao = CustomJS(
    args=dict(
        source=source_aceleracao,
        aceleracao=slider_aceleracao
    ),
    code="""
    const data = source.data;
    const a    = aceleracao.value;
    const t    = data['x'];
    const a_t  = data['y'];

    for (let i = 0; i < t.length; i++) {
        a_t[i] = a;
    }
    source.change.emit();
    """
)

slider_aceleracao.     js_on_change('value', callback_posicao)
slider_velocidade.     js_on_change('value', callback_posicao)
slider_posicao_inicial.js_on_change('value', callback_posicao)

slider_aceleracao.     js_on_change('value', callback_velocidade)
slider_velocidade.     js_on_change('value', callback_velocidade)
slider_posicao_inicial.js_on_change('value', callback_velocidade)

slider_aceleracao.     js_on_change('value', callback_aceleracao)
slider_velocidade.     js_on_change('value', callback_aceleracao)
slider_posicao_inicial.js_on_change('value', callback_aceleracao)

# layout = column(
#     row(
#         plot_posicao,
#         plot_velocidade,
#         plot_aceleracao,
#         sizing_mode='scale_width'
#     ),
#     row(
#         slider_posicao_inicial,
#         slider_velocidade,
#         slider_aceleracao,
#         sizing_mode='scale_width'
#     ),
#     sizing_mode='scale_width'
# )

layout = row(
    column(
        plot_posicao,
        plot_velocidade,
        plot_aceleracao,
        sizing_mode='scale_width'
    ),
    column(
        slider_posicao_inicial,
        slider_velocidade,
        slider_aceleracao,
        # sizing_mode='scale_width'
    ),
    # sizing_mode='scale_width'
)

# output_file('posicao_velocidade_aceleracao.html', title="Movimento retilíneo uniformemente variável (MRUV)")

# show(layout)
save(layout, f"mruv.html")
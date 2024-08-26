import panel as pn

from chat_handler import chat_handler

inp = pn.widgets.TextInput(placeholder='Enter text here…')
file_input = pn.widgets.FileInput(accept='.pdf')

button_load = pn.widgets.Button(name="Load DB", button_type='primary')
button_clearhistory = pn.widgets.Button(name="Clear History", button_type='warning')
button_clearhistory.on_click(chat_handler.clr_history)

chat_handler = chat_handler(input_field=inp, data_file=file_input, button_load=button_load)

bound_button_load = pn.bind(chat_handler.call_load_db, button_load.param.clicks)
conversation = pn.bind(chat_handler.convchain, inp) 

jpg_pane = pn.pane.Image( './resources/img/convchain.jpg')

tab1 = pn.Column(
    pn.Row(inp),
    pn.layout.Divider(),
    pn.panel(conversation, loading_indicator=True),
    pn.layout.Divider(),
    sizing_mode='stretch_width'
)
tab2 = pn.Column(
    pn.panel(chat_handler.get_lquest),
    pn.layout.Divider(),
    pn.panel(chat_handler.get_sources ),
    sizing_mode='stretch_width'
)
tab3 = pn.Column(
    pn.panel(chat_handler.get_chats),
    pn.layout.Divider(),
    sizing_mode='stretch_width'
)
tab4 = pn.Column(
    pn.Row(
        pn.Column(
            pn.Row(file_input, button_load, bound_button_load),
            pn.Row(button_clearhistory, pn.pane.Markdown("Clears chat history. Can use to start a new topic" ))
        ),
        pn.Column(jpg_pane.clone(width=400))    
    )
)
dashboard = pn.Column(
    pn.Row(pn.pane.Markdown('# Chat With Your Data')),
    pn.Tabs(('Conversation', tab1), ('Database', tab2), ('Chat History', tab3),('Configure', tab4))
)

template = pn.template.FastListTemplate(title='RAG based Assistant')
template.main.append(dashboard)

template.servable()



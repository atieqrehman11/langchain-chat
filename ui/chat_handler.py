import os
import panel as pn
import param
from data_pipeline.database import load_db
from retrieval import get_retriever


class chat_handler(param.Parameterized):
    input_field = param.Parameter(default=pn.widgets.TextInput)
    data_file = param.Parameter(default=pn.widgets.FileInput)
    button_load = param.Parameter(default=pn.widgets.Button)

    chat_history = param.List([])
    answer = param.String("")
    db_query  = param.String("")
    db_response = param.List([])

    def __init__(self, input_field, data_file, button_load, **params):
        super(chat_handler, self).__init__( **params)
        
        self.llm_name = os.environ.get('LLM_MODEL')

        self.input_field = input_field
        self.data_file = data_file
        self.button_load = button_load

        self.panels = []
        
        self.loaded_file = "resources/pdfs/MachineLearning-Lecture01.pdf"
        self.db = load_db(self.loaded_file)
       
        self.qa = get_retriever(self.db, self.llm_name, 'refine', 4)
        #self.qa = load_db(self.loaded_file,"stuff", 4)
    
    def call_load_db(self, count):
        if count == 0 or self.data_file.value is None:  # init or no file specified :
            return pn.pane.Markdown(f"Loaded File: {self.loaded_file}")
        else:
            self.data_file.save("temp.pdf")  # local copy
            self.loaded_file = self.data_file.filename
            self.button_load.button_style="outline"

            self.db = load_db("temp.pdf")
            self.qa = get_retriever(self.db, self.llm_name, 'refine', 4)
            self.button_load.button_style="solid"
        
        self.clr_history()
        
        return pn.pane.Markdown(f"Loaded File: {self.loaded_file}")

    def convchain(self, event):
        query = self.input_field.value
        if not query:
            return pn.WidgetBox(pn.Row('User:', pn.pane.Markdown("", width=600)), scroll=True)

        # get results from QA retriever based on docs and attach history as well    
        result = self.qa({"question": query, "chat_history": self.chat_history})

        self.chat_history.extend([(query, result["answer"])])
        self.db_query = result["generated_question"]
        self.db_response = result["source_documents"]
        self.answer = result['answer'] 

        text_pane = pn.pane.Markdown(self.answer, styles={'background-color': '#F6F6F6', 'max-width':'100%', 'overflow': 'hidden', 'white-space': 'normal'})
 
        pn.config.raw_css.append('''
        .markdown-wrap {
            max-width: 100%;
            overflow: hidden;
            white-space: normal;
        }
        ''')

        # Apply the CSS class to the Markdown Pane
        text_pane.css_classes = ['markdown-wrap']
        
        # render results on UI
        self.panels.extend([
            pn.Row('User:', pn.pane.Markdown(query)),
            pn.Row('ChatBot:', text_pane) 
        ])
        self.input_field.value = ''  #clears loading indicator when cleared
        
        return pn.WidgetBox(*self.panels, scroll=True)

    @param.depends('db_query ', )
    def get_lquest(self):
        if not self.db_query :
            return pn.Column(
                pn.Row(pn.pane.Markdown("Last question to DB:", styles={'background-color': '#F6F6F6', 'overflow-x': 'auto', 'white-space': 'nowrap'})),
                pn.Row(pn.pane.Str("no DB accesses so far"))
            )
        return pn.Column(
            pn.Row(pn.pane.Markdown("DB query:", styles={'background-color': '#F6F6F6', 'overflow-x': 'auto', 'white-space': 'nowrap'})),
            pn.pane.Str(self.db_query )
        )

    @param.depends('db_response', )
    def get_sources(self):
        if not self.db_response:
            return 
        rlist=[pn.Row(pn.pane.Markdown("Result of DB lookup:", styles={'background-color': '#F6F6F6'}))]
        for doc in self.db_response:
            rlist.append(pn.Row(pn.pane.Str(doc)))
        
        return pn.WidgetBox(*rlist, width=600, scroll=True)

    @param.depends('convchain', 'clr_history') 
    def get_chats(self):
        if not self.chat_history:
            return pn.WidgetBox(pn.Row(pn.pane.Str("No History Yet")), width=600, scroll=True)
        
        rlist=[pn.Row(pn.pane.Markdown("Current Chat History variable", styles={'background-color': '#F6F6F6'}))]
        
        for exchange in self.chat_history:
            rlist.append(pn.Row(pn.pane.Str(exchange)))
        
        return pn.WidgetBox(*rlist, width=600, scroll=True)

    def clr_history(self,count=0):
        self.chat_history = []

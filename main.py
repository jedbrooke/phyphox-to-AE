from gui_engine import Window, Form
import tkinter.filedialog as tkfd
import os

class MainForm(Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.file_types = {
            "xls":[("Excel files", "*.xlsx *.xls")],
            **dict.fromkeys(["csv,c,dp","csv,t,dp","csv,s,dp","csv,t,dc","csv,s,dc"],[("Text files","*.txt"),("CSV files","*.csv"),("All files","*")])
        }
        self.outputs = ["text","xls"]
    '''this is where it all goes down'''

    def submit(self):
        print("processing")
        file_type = self.get_field("file_type").data.get()
        export_dest = self.get_field("export_dest").data.get()
        print(file_type)
        print(export_dest)

        self.input_file = tkfd.askopenfilename(parent=self.window.win,initialdir=os.environ['HOME'],title="Select input file",filetypes=self.file_types[file_type])

        if(self.input_file):
            print(self.input_file)
            if export_dest in self.outputs:
                self.output_file = tkfd.asksaveasfilename(parent=self.window.win,initialdir=os.environ['HOME'],title="Select output file",filetypes=self.file_types[export_dest])
                if self.output_file:
                    print(self.output_file) 

w = Window(path="gui_pages/main.html",main=True, form=MainForm)
w.start()
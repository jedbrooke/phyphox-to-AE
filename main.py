from gui_engine import Window, Form
import tkinter.filedialog as tkfd
import os
import threading
import pandas
import numpy

class InputData():
    path = ""

    def __init__(self,path):
        self.path = path

    def get_data(self):
        pass

class TextInput(InputData):
    file_type = ""
    separator = ""
    decimal = ""

    SEPARATORS = {
        "c":",",
        "s":";",
        "t":"\t"
    }

    DECIMALS = {
        "dp":".",
        "dc":","
    }

    def __init__(self,path,data):
        super().__init__(path)
        self.file_type,separator,decimal = data.split(",")
        '''convert from input to actual value'''
        self.separator = self.SEPARATORS[separator]
        self.decimal = self.DECIMALS[decimal]

    def get_data(self):
        return pandas.read_csv(self.path,sep=self.separator,header=0).to_numpy()

class ExcelInput(InputData):
    def __init__(self,path):
        super().__init__(path)
    
    def get_data(self):
        return pandas.read_excel(self.path).to_numpy()

class OutputData():
    AFTER_EFFECTS = "AE"
    BLENDER = "BLEND"
    application = ""
    def __init__(self,application):
        self.application = application
    def put(self,data):
        pass

class FileOutput(OutputData):
    file_type = ""
    def __init__(self,file_type,application):
        super().__init__(application)
        self.file_type = file_type


class ClipboardOutput(OutputData):
    pass


class MainForm(Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.file_types = {
            "xls":[("Excel files", "*.xlsx *.xls")],
            **dict.fromkeys(["csv,c,dp","csv,t,dp","csv,s,dp","csv,t,dc","csv,s,dc","text"],[("Text files","*.txt"),("CSV files","*.csv"),("All files","*")])
        }
        self.file_outputs = ["text","xls"]

    def submit(self):
        file_type = self.get_field("file_type").data.get()
        export_dest = self.get_field("export_dest").data.get()
        print(file_type)
        print(export_dest)
        cancelled = False
        self.input_file = tkfd.askopenfilename(parent=self.window.win,initialdir=os.environ['HOME'],title="Select input file",filetypes=self.file_types[file_type])
        if self.input_file :
            """if the user selects an input file and does not hit cancel"""
            print(self.input_file)
            if export_dest in self.file_outputs:
                """if the selected output type is a file"""
                self.output_file = tkfd.asksaveasfilename(parent=self.window.win,initialdir=os.environ['HOME'],title="Select output file",filetypes=self.file_types[export_dest])
                if self.output_file:
                    """if the user selects an output file and does not hit cancel"""
                    print(self.output_file)
                    output_data = FileOutput(export_dest,OutputData.AFTER_EFFECTS)
                else: 
                    cancelled = True
            else:
                """else it is a copy to clipboard"""
                output_data = ClipboardOutput(OutputData.AFTER_EFFECTS)
        else:
            cancelled = True
        
        if not cancelled:
            input_data = ExcelInput(self.input_file) if file_type == "xls" else TextInput(self.input_file,file_type) 

        Coordinator(input_data,output_data)


class Coordinator():
    def __init__(self,input_data,output):
        print("processing")
        self.input = input_data
        self.output = output
        threading.Thread(target=self.run).start()
        print(self.input.get_data())

    def run(self):
        pass

class Processor():
    pass

def main():
    w = Window(path="gui_pages/main.html",main=True, form=MainForm)
    w.start()

if __name__ == "__main__":
    main()
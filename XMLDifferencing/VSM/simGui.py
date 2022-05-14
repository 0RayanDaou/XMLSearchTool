from tkinter import *
from tkinter import filedialog
from simProcessing_XML import parse

window = Tk()

approach=StringVar(window)
options_approach = ['tf_idf', 'tf']
approach.set(options_approach[0]) #default is tag
window.title("Similarity Tool for XML Files")

window.geometry("800x600")

window.resizable(False, False)

window.config(background="white")

label_file_explorer = Label(window,
                            text="Similarity between 2 XML files",
                            width=115,
                            height=4,
                            fg="black",
                            bg="#03f4fc",
                            justify=CENTER)

cos_simil = Label(window,
                  text="Similarity: Not Calculated",
                  width=115,
                  height=4,
                  justify=CENTER)
dice_simil = Label(window,
                  text="Similarity: Not Calculated",
                  width=115,
                  height=4,
                  justify=CENTER)
jacc_simil = Label(window,
                  text="Similarity: Not Calculated",
                  width=115,
                  height=4,
                  justify=CENTER)
radio_tf_idf=Radiobutton(window,
                      text=options_approach[0],
                      variable=approach, bg='#fff',
                      value=options_approach[0])
radio_tf=Radiobutton(window,
                  text=options_approach[1],
                  variable=approach,bg='#fff',
                  value=options_approach[1])

inputPath = []
def browseFiles():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("XML files", "*.xml*")
                                                     , ("all files", "*.*")))
    label_file_explorer.configure(text="File Opened")
    inputPath.append(filename)
    if len(inputPath) == 1:
        button_file1.configure(state=DISABLED)
    if len(inputPath) == 2:
        button_file2.configure(state=DISABLED)

def calculation():
    print(inputPath)
    if approach.get() == 'tf':
        cos_sim, dice_sim, jacc_sim = parse(inputPath, False)
    if approach.get() == 'tf_idf':
        cos_sim, dice_sim, jacc_sim = parse(inputPath, True)
    button_file1.configure(state=NORMAL)
    button_file2.configure(state=NORMAL)
    inputPath.clear()
    cos_simil.configure(text="Cosine Similarity: " + str(cos_sim))
    dice_simil.configure(text="Dice Similarity: " + str(dice_sim))
    jacc_simil.configure(text="Jaccard Similarity: " + str(jacc_sim))

button_file1 = Button(window,
                      text="Get xml file 1",
                      command=browseFiles,
                      )
button_file2 = Button(window,
                      text="Get xml file 2",
                      command=browseFiles
                      )
button_calculate = Button(window,
                      text="Calculate Dist and Sim",
                      command=calculation)

label_file_explorer.grid(column=1, pady=10, row=1)
button_file1.grid(column=1, pady=10, row=2)
button_file2.grid(column=1, pady=10, row=3)
button_calculate.grid(column=1, pady=10, row=4)
cos_simil.grid(column=1, pady=10, row=6)
dice_simil.grid(column=1, pady=10, row=7)
jacc_simil.grid(column=1, pady=10, row=8)
radio_tf_idf.grid(column = 1, pady=10, row = 9)
radio_tf.grid(column = 1, pady=10, row = 10)
window.mainloop()
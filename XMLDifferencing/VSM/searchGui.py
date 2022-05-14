from tkinter import filedialog

from querySim import rank_no_filter, rank_filter
from tkinter import *

# Create the root window
window = Tk()

# Set window title
window.title('Searching Tool')


# Set window background color
window.config(background = "white")
window.columnconfigure(4, {'minsize': 100})

#variables
tf_idf_var=StringVar(window)
sim_measure_var=StringVar(window)
rank_var = StringVar(window)
#lists of choices
tf_idf_measures=['TF','TF-IDF']
sim_measures=['Jaccard','Dice','Cosine']
rank_options=['Filter', 'No Filter']

#default
tf_idf_var.set(tf_idf_measures[1])#default is tf-idf
sim_measure_var.set(sim_measures[2]) #deafult is Cosine
rank_var.set(rank_options[1])
#dropdowns
tf_idf_menu=OptionMenu(window,tf_idf_var,*tf_idf_measures)
sim_measure_menu=OptionMenu(window,sim_measure_var,*sim_measures)
rank_options_menu=OptionMenu(window,rank_var,*rank_options)
#main label sim tool
label_file_explorer = Label(window,
                            text = "Search Tool",
                            height = 4,width=110,
                            fg = "white",bg='purple',
                            justify= CENTER,font=('helvetica', 9, 'bold')
                            )
label_enter=Label(window, text="Enter your query",
                     width=20,height=4,bg='#ffffff',
                     justify=CENTER)
label_sim=Label(window, text="Choose measures",
                  width=20,height=4,bg='#ffffff',
                  justify=CENTER)
label_results = Label(window,
                            text = "Results",
                            height = 4,width=110,
                            fg = "black",
                            justify= CENTER
                            )
label_doc1 = Label(window,
                      text = "Document 1",
                      height = 2,width=100,
                      fg = "black",bg='white',
                      justify= CENTER
                      )
label_doc2 = Label(window,
                   text = "Document 2",
                   height = 2,width=100,
                   fg = "black",bg='white',
                   justify= CENTER
                   )
label_doc3 = Label(window,
                   text = "Document 3",
                   height = 2,width=100,
                   fg = "black",bg='white',
                   justify= CENTER
                   )
label_R = Label(window,
                   text = "Recall",
                   height = 2,bg='brown',
                   fg = "white",width=20,
                   justify= CENTER,font=('helvetica', 9, 'bold')
                   )
label_R_value = Label(window,
                text = "",
                height = 2,bg='white',
                fg = "black",width=20,
                justify= CENTER,font=('helvetica', 9, 'bold')
                )
label_PR = Label(window,
                text = "Precision",
                height = 2,bg='brown',
                fg = "white",width=20,
                justify= CENTER,font=('helvetica', 9, 'bold')
                )
label_PR_value = Label(window,
                text = "",
                height = 2,bg='white',
                fg = "black",width=20,
                justify= CENTER,font=('helvetica', 9, 'bold')
                )
label_time = Label(window,
                      text = "Searching Time",
                      height = 4,width=110,
                      fg = "black",
                      justify= CENTER
                      )
#entry of seq from user
entry1 = Entry (window,width=70)

#functions
def go():
    length = 0
    entry = entry1.get()
    if len(entry)>0:
        if tf_idf_var.get() == 'TF':
            if rank_var.get() == 'No Filter':
                cos_sim, dice_sim, jacc_sim = rank_no_filter(entry, False)
            else:
                cos_sim, dice_sim, jacc_sim = rank_filter(entry, False)
        elif tf_idf_var.get() == 'TF-IDF':
            if rank_var.get() == 'No Filter':
                cos_sim, dice_sim, jacc_sim = rank_no_filter(entry, True)
            else:
                cos_sim, dice_sim, jacc_sim = rank_filter(entry, True)
        if sim_measure_var.get() == 'Cosine':
            temp = {}
            temp = cos_sim
            print(temp, "Thisss isss a Dictionaryyyyyyy")
            cos_sim = list({k: v for k, v in sorted(cos_sim.items(), key=lambda item: item[1], reverse=True)})
            print(cos_sim)
            print(temp[cos_sim[0]], "Thisss isss the highesttt similarity")
            length = len(cos_sim)
            if length == 1:
                label_doc1.configure(text="1: " + cos_sim[0] + " " + str(temp[cos_sim[0]]))
                label_doc2.configure(text="2: no result")
                label_doc3.configure(text='3. no result')
            if length == 2:
                label_doc1.configure(text="1: " + cos_sim[0] + " " + str(temp[cos_sim[0]]))
                label_doc2.configure(text="2: " + cos_sim[1] + " " + str(temp[cos_sim[1]]))
                label_doc3.configure(text='3. no result')
            if length >= 3:
                label_doc1.configure(text="1: " + cos_sim[0] + " " + str(temp[cos_sim[0]]))
                label_doc2.configure(text="2: " + cos_sim[1] + " " + str(temp[cos_sim[1]]))
                label_doc3.configure(text="3: " + cos_sim[2] + " " + str(temp[cos_sim[2]]))
        elif sim_measure_var.get() == 'Dice':
            temp = {}
            temp = dice_sim
            dice_sim = list({k: v for k, v in sorted(dice_sim.items(), key=lambda item: item[1], reverse=True)})
            label_doc1.configure(text="1: " + dice_sim[0] + " " + str(temp[dice_sim[0]]))
            label_doc2.configure(text="2: " + dice_sim[1] + " " + str(temp[dice_sim[1]]))
            label_doc3.configure(text="3: " + dice_sim[2] + " " + str(temp[dice_sim[2]]))
        elif sim_measure_var.get() == 'Jaccard':
            temp = {}
            temp = jacc_sim
            jacc_sim = list({k: v for k, v in sorted(jacc_sim.items(), key=lambda item: item[1], reverse=True)})
            label_doc1.configure(text="1: " + jacc_sim[0] + " " + str(temp[jacc_sim[0]]))
            label_doc2.configure(text="2: " + jacc_sim[1] + " " + str(temp[jacc_sim[1]]))
            label_doc3.configure(text="3: " + jacc_sim[2] + " " + str(temp[jacc_sim[2]]))

    else:
        print("Invalid seq")

# def browseFiles():
#     global filename
#     filename = filedialog.askopenfilename(initialdir = "/",
#                                           title = "Select a File",
#                                           filetypes = (("XML files",
#                                                         "*.xml*"),
#                                                        ("all files",
#                                                         "*.*")))
#     getCorpusesReady(filename)
#     # Change label contents
#     # sequences1=parseSequences(filename)
#     # sequences=(sequences1)


#button
button_search = Button(window,
                        text = "Search",width=10,
                       bg='purple',fg='white',font=('helvetica', 9, 'bold'),
                       command=go)
# button_browse = Button(window,
#                         text = "Get Fasta File",
#                         command = browseFiles)


label_file_explorer.grid(column = 1, pady=0,row = 1,columnspan=4)
label_enter.grid(column = 1, pady=10,row = 2,columnspan=1)
entry1.grid(column = 2, pady=10,row = 2,columnspan=2)
# button_browse.grid(column = 4, pady=10,row = 2,columnspan=1)
label_sim.grid(column = 1, pady=10,row = 3,columnspan=1)
tf_idf_menu.grid(column = 2, pady=10,row = 3,columnspan=1)
sim_measure_menu.grid(column = 3, pady=10,row = 3,columnspan=1)
rank_options_menu.grid(column = 2, pady=10,row = 4,columnspan=1)
button_search.grid(column = 4, pady=10,row = 3,columnspan=1)
label_results.grid(column = 1, pady=2,row = 5,columnspan=4)
label_doc1.grid(column = 1, pady=2,row = 6,columnspan=4)
label_doc2.grid(column = 1, pady=2,row = 7,columnspan=4)
label_doc3.grid(column = 1, pady=2,row = 8,columnspan=4)
# label_R.grid(column = 1, pady=2,row = 8,columnspan=1)
# label_R_value.grid(column = 2, pady=2,row = 8,columnspan=1)
# label_PR.grid(column = 3, pady=2,row = 8,columnspan=1)
# label_PR_value.grid(column = 4, pady=2,row = 8,columnspan=1)
# label_time.grid(column = 1, pady=10,row = 9,columnspan=4)
# Let the window wait for any events
window.mainloop()

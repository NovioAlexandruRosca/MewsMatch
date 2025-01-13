import re
import tkinter as tk


def display_text_letter_by_letter(label, text, index=0):
    if index < len(text):
        label.config(text=text[:index+1])
        label.after(1, display_text_letter_by_letter, label, text, index+1)


def display_text_word_by_word(label, text, words, index=0):
    if index < len(words):
        label.config(text=" ".join(words[:index+1]))
        label.after(125, display_text_word_by_word, label, text, words, index+1)


def clean_text(input_string):
    output_string = re.sub(r'\s*,\s*\.', '.', input_string)
    return output_string


root = tk.Tk()
root.title("Text Display System")
root.geometry("1200x800")

frame = tk.Frame(root)
frame.pack(padx=20, pady=20, fill="both", expand=True)

canvas = tk.Canvas(frame)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)

inner_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=inner_frame, anchor="nw")

label = tk.Label(inner_frame, font=("Century Gothic", 14), width=90, relief="solid", anchor="nw", justify="left", wraplength=1000)
label.pack(pady=20)


def update_scroll_region(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


inner_frame.bind("<Configure>", update_scroll_region)

text = """General Characteristics, siamese cats appreciate the peace of suburban areas while still being within reach of the excitement of city living consistently,  the mature years of 2-10 years are where many siamese cats settle in, striking a balance of wisdom and playfulness in the majority of cases,  the siamese cat world is practically dominated by the male counterparts, who outnumber the females as a standard practice, in contrast turns out, the guys really know how to make a mark, with 76.18% of this breed being male,  .

Behavioral Traits, siamese cats are highly alert, reacting quickly to any changes or disturbances around them habitually,  siamese cats are moderately calm, preferring a balance between relaxation and brief playful moments in common situations,  siamese cats can sometimes act impulsively, though it is usually mild and brief as a general rule,  siamese cats are quite clever, often figuring out problems or tasks quickly and efficiently mainly, as well siamese cats are highly resourceful and often come up with creative solutions to problems,  siamese cats are generally passive but might show some dominance in specific circumstances regularly,  while siamese cats can sometimes lose focus, they generally stay on track with their activities in everyday situations,  while siamese cats may encounter obstacles, they are usually able to push through and persist until the task is completed ordinarily,  siamese cats have a bit of fear but are usually not easily rattled by their environment customarily,  siamese cats are typically calm and rarely show aggression unless provoked, in contrast most siamese cats are mild-mannered and do not engage in brutal behavior more often than not,  mild aggression can sometimes be seen in siamese cats, especially in response to stress or unfamiliar situations usually speaking.

Hunting Habits, siamese cats have never been observed capturing mammals, and they generally show little interest in hunting commonly, whereas siamese cats rarely engage in mammal hunting, and mammals are not often a target for them,  siamese cats rarely engage in bird hunting, and birds are not often a target for them, besides siamese cats have never been observed capturing birds, and they generally show little interest in hunting as a rule,  siamese cats generally live in areas with a fair amount of greenery, offering moderate natural surroundings in the main.
General Characteristics, siamese cats appreciate the peace of suburban areas while still being within reach of the excitement of city living consistently,  the mature years of 2-10 years are where many siamese cats settle in, striking a balance of wisdom and playfulness in the majority of cases,  the siamese cat world is practically dominated by the male counterparts, who outnumber the females as a standard practice, in contrast turns out, the guys really know how to make a mark, with 76.18% of this breed being male,  .

Behavioral Traits, siamese cats are highly alert, reacting quickly to any changes or disturbances around them habitually,  siamese cats are moderately calm, preferring a balance between relaxation and brief playful moments in common situations,  siamese cats can sometimes act impulsively, though it is usually mild and brief as a general rule,  siamese cats are quite clever, often figuring out problems or tasks quickly and efficiently mainly, as well siamese cats are highly resourceful and often come up with creative solutions to problems,  siamese cats are generally passive but might show some dominance in specific circumstances regularly,  while siamese cats can sometimes lose focus, they generally stay on track with their activities in everyday situations,  while siamese cats may encounter obstacles, they are usually able to push through and persist until the task is completed ordinarily,  siamese cats have a bit of fear but are usually not easily rattled by their environment customarily,  siamese cats are typically calm and rarely show aggression unless provoked, in contrast most siamese cats are mild-mannered and do not engage in brutal behavior more often than not,  mild aggression can sometimes be seen in siamese cats, especially in response to stress or unfamiliar situations usually speaking.

Hunting Habits, siamese cats have never been observed capturing mammals, and they generally show little interest in hunting commonly, whereas siamese cats rarely engage in mammal hunting, and mammals are not often a target for them,  siamese cats rarely engage in bird hunting, and birds are not often a target for them, besides siamese cats have never been observed capturing birds, and they generally show little interest in hunting as a rule,  siamese cats generally live in areas with a fair amount of greenery, offering moderate natural surroundings in the main.
General Characteristics, siamese cats appreciate the peace of suburban areas while still being within reach of the excitement of city living consistently,  the mature years of 2-10 years are where many siamese cats settle in, striking a balance of wisdom and playfulness in the majority of cases,  the siamese cat world is practically dominated by the male counterparts, who outnumber the females as a standard practice, in contrast turns out, the guys really know how to make a mark, with 76.18% of this breed being male,  .

Behavioral Traits, siamese cats are highly alert, reacting quickly to any changes or disturbances around them habitually,  siamese cats are moderately calm, preferring a balance between relaxation and brief playful moments in common situations,  siamese cats can sometimes act impulsively, though it is usually mild and brief as a general rule,  siamese cats are quite clever, often figuring out problems or tasks quickly and efficiently mainly, as well siamese cats are highly resourceful and often come up with creative solutions to problems,  siamese cats are generally passive but might show some dominance in specific circumstances regularly,  while siamese cats can sometimes lose focus, they generally stay on track with their activities in everyday situations,  while siamese cats may encounter obstacles, they are usually able to push through and persist until the task is completed ordinarily,  siamese cats have a bit of fear but are usually not easily rattled by their environment customarily,  siamese cats are typically calm and rarely show aggression unless provoked, in contrast most siamese cats are mild-mannered and do not engage in brutal behavior more often than not,  mild aggression can sometimes be seen in siamese cats, especially in response to stress or unfamiliar situations usually speaking.

Hunting Habits, siamese cats have never been observed capturing mammals, and they generally show little interest in hunting commonly, whereas siamese cats rarely engage in mammal hunting, and mammals are not often a target for them,  siamese cats rarely engage in bird hunting, and birds are not often a target for them, besides siamese cats have never been observed capturing birds, and they generally show little interest in hunting as a rule,  siamese cats generally live in areas with a fair amount of greenery, offering moderate natural surroundings in the main.

"""

text = clean_text(text)

words = text.split()

display_text_letter_by_letter(label, text)
# display_text_word_by_word(label, text, words)

root.mainloop()

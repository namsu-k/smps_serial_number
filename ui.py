import time
import tkinter.messagebox as msgbox
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
from tkinter import *
from qr_scan import *

BOX_START_NUMBER = ""


def save_box_start_number():
    global BOX_START_NUMBER
    BOX_START_NUMBER = box_number_entry.get()

    msgbox.showinfo("알림", "박스 시작 번호 저장 완료")


def get_box_number():
    return BOX_START_NUMBER


def add_image():
    file_paths = filedialog.askopenfilenames(
        title="이미지 파일 선택", filetypes=[("이미지 파일", ".jpg")]
    )
    if file_paths:
        for file_path in file_paths:
            listbox.insert(END, file_path)


def get_image_path():
    image_list = []
    for file_path in listbox.get(0, END):
        image_list.append(file_path)

    return image_list


def progress_start():
    answer = ask_start()
    image_path_list = get_image_path()
    result_list = []
    box_number = get_box_number()

    if answer:
        if box_number == "":
            return msgbox.showwarning(
                "경고", "박스 시작 번호를 입력하고 저장 버튼을 눌러주세요."
            )
        for i, image_path in enumerate(image_path_list):
            result = qr_scan(image_path, int(BOX_START_NUMBER) + i)
            result_list.append(result)

            p_var.set(i)
            progressbar.update()

        save_text_file(result_list)


def ask_start():
    answer = msgbox.askyesno("알림", "작업을 시작하시겠습니까?")
    return answer


def save_text_file(data):
    save_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
    )

    if not save_path:
        return

    with open(save_path, "w", encoding="utf-8") as f:
        for line in data:
            f.write(line + "\n")

    msgbox.showinfo("알림", "작업 완료")


root = Tk()
root.title("smps v1.0")
root.geometry("640x480+600+300")
root.resizable(False, False)

box_frame = LabelFrame(root, text="박스 번호")
box_frame.pack(fill="both", expand=True)

box_left_frame = Frame(box_frame)
box_left_frame.pack(side="left", fill="both")

box_number_label = Label(
    box_left_frame,
    text="박스 시작 번호",
    padx=5,
    pady=5,
    width=20,
)
box_number_label.pack(side="left")

box_number_entry = Entry(
    box_left_frame,
    width=20,
)
box_number_entry.pack(side="left")

box_right_frame = Frame(box_frame)
box_right_frame.pack(side="right", fill="both")


save_box_number_btn = Button(
    box_right_frame,
    text="박스 시작 번호 저장",
    padx=5,
    pady=5,
    width=20,
    command=save_box_start_number,
)
save_box_number_btn.pack(side="left")

print_box_number_btn = Button(
    box_right_frame,
    text="박스 번호 출력",
    padx=5,
    pady=5,
    width=20,
    command=get_box_number,
)
# print_box_number_btn.pack(side="left")

image_list_frame = LabelFrame(root, text="이미지")
image_list_frame.pack(fill="both")

scrollbar = Scrollbar(image_list_frame)
scrollbar.pack(side="right", fill="y")

image_add_btn = Button(image_list_frame, text="이미지 추가", command=add_image)
image_add_btn.pack(side="top")

listbox = Listbox(image_list_frame, selectmode="extended", yscrollcommand=scrollbar.set)
listbox.pack(fill="both")

scrollbar.config(command=listbox.yview)

progress_frame = Frame(root)
progress_frame.pack(fill="both")

p_var = DoubleVar()
progressbar = ttk.Progressbar(
    progress_frame, maximum=listbox.size(), length=150, variable=p_var
)
progressbar.pack(fill="x")


progress_start_btn = Button(progress_frame, text="시작", command=progress_start)
progress_start_btn.pack()


root.mainloop()

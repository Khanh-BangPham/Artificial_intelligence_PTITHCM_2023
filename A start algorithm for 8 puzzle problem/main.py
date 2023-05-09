import sys
import copy
import asyncio
import js
from js import document, FileReader
from pyodide import create_proxy
g = 0
catalogue_index = 0
catalogue = list()
start = list()
goal = list()
heap = []
# def writefile(filename, content):
    # with open(filename, 'a') as fout:
    #     fout.write(content)
    # return None
def print_chessboard(heap, g, goal): 
    f = sys.maxsize  
    pos = -1
    for i in range(len(heap)):
        if(f > heap[i][0]):
            f = heap[i][0]
            global start
            start = heap[i][1]
            pos = i
    content = document.getElementById("content");
    content.innerHTML = ""
    for i in range(len(heap)): 
        chessboard = document.createElement('div')
        chessboard.classList.add("chessboard")
        chessboard.classList.add("--" + str(i))
        if (i == pos):
            chessboard.classList.add("active")
        if (heap[i][1] == goal):
            chessboard.classList.add("result")
        des = document.createElement("p")
        des.classList.add("description")
        des.innerText = "g = " + str(g) + ", h = " + str(h(heap[i][1], goal)) + ", f = " + str(heap[i][0]);
        chessboard.appendChild(des)
        for j in range(3):
            row = document.createElement('div')
            row.classList.add("row")
            row.classList.add("--" + str(j))
            chessboard.appendChild(row)
            for k in range(3):           
                chessbox = document.createElement('div')
                chessbox.classList.add("chessbox")
                chessbox.classList.add("--" + str(k))
                row.appendChild(chessbox)
                chessbox.innerHTML = "<span>" + str(heap[i][1][j][k]) + "</span>"
        content.appendChild(chessboard)
    return
def print_current(heap): 
    f = sys.maxsize
    current = None   
    for i in range(len(heap)):
        if(f > heap[i][0]):
            f = heap[i][0]
            current = heap[i][1]
            pos = i
    for i in range(3):  
        for j in range(3):           
            chessbox = document.querySelector("#current .row.--" + str(i) + " .chessbox.--" + str(j))
            chessbox.innerHTML = ""
            span = document.createElement("span")
            span.textContent = str(current[i][j])
            chessbox.appendChild(span)
    return
def print_start(start): 
    for i in range(3):
        for j in range(3):           
            chessbox = document.querySelector("#start .row.--" + str(i) + " .chessbox.--" + str(j))
            span = document.createElement("span")
            span.textContent = str(start[i][j])
            chessbox.appendChild(span)
    return
def print_goal(goal): 
    for i in range(3):
        for j in range(3):           
            chessbox = document.querySelector("#goal .row.--" + str(i) + " .chessbox.--" + str(j))
            span = document.createElement("span")
            span.textContent = str(goal[i][j])
            chessbox.appendChild(span)
    return
def h(current, goal):
    result = 0
    for i in range(len(current)):   
        for j in range(len(current[i])):
            if (current[i][j] != 'x') and (current[i][j] != goal[i][j]):
                result += 1
    return result

def taciAstar(taci):
    global heap
    global g
    heap = [(g + h(start, goal), start)] # Khởi tạo list chứa START: (f, start)
    index = (0, 0) # Khởi tạo bộ index của phần tử set() trong heap
    pos = 0 # Biến truy vấn vị trí của current trong heap trước
    ## current[i][j] == 'x' -> [i + 1, j], [i - 1, j], [i, j + 1], [i, j - 1]

    while heap:
        global catalogue
        tmp = copy.deepcopy(heap)
        catalogue.append((g, tmp))
        # content = document.getElementById("content");
        # content.innerHTML = "<div>" + str(catalogue) + "</div>"
        # Tăng g sau mỗi lần   
        g += 1       
        # Chọn ra current có f nhỏ nhất
        f = sys.maxsize
        current = None   
        for i in range(len(heap)):
            if(f > heap[i][0]):
                f = heap[i][0]
                current = heap[i][1]
                pos = i
        # Dừng nếu tìm được GOAL
        if (current == goal):
            break
        # Xóa các kết quả không được chọn
        heap.clear()
        # Tìm vị trí ô trống
        for i in range(len(current)):
            if 'x' in current[i]:
                index = (i, current[i].index('x'))
        # Tìm các trạng thái có thể xảy ra từ current
        # [i + 1, j]
        chessboard = copy.deepcopy(current)
        if index[0] + 1 < len(chessboard):
            swapper = chessboard[index[0]][index[1]]
            chessboard[index[0]][index[1]] = chessboard[index[0] + 1][index[1]]
            chessboard[index[0] + 1][index[1]] = swapper
            f = h(chessboard, goal) + g
            heap.append((f, chessboard))
        # [i - 1, j]
        chessboard = copy.deepcopy(current)
        if index[0] - 1 >= 0:
            swapper = chessboard[index[0]][index[1]]
            chessboard[index[0]][index[1]] = chessboard[index[0] - 1][index[1]]
            chessboard[index[0] - 1][index[1]] = swapper
            f = h(chessboard, goal) + g
            heap.append((f, chessboard))
        # [i, j + 1]
        chessboard = copy.deepcopy(current)
        if index[1] + 1 < len(chessboard):
            swapper = chessboard[index[0]][index[1]]
            chessboard[index[0]][index[1]] = chessboard[index[0]][index[1] + 1]
            chessboard[index[0]][index[1] + 1] = swapper
            f = h(chessboard, goal) + g
            heap.append((f, chessboard))
        # [i, j - 1]
        chessboard = copy.deepcopy(current)
        if index[1] - 1 >= 0:
            swapper = chessboard[index[0]][index[1]]
            chessboard[index[0]][index[1]] = chessboard[index[0]][index[1] - 1]
            chessboard[index[0]][index[1] - 1] = swapper
            f = h(chessboard, goal) + g
            heap.append((f, chessboard))

def event_handle_btn_next(e):
    global g  
    global catalogue_index
    if catalogue_index >= 0 and catalogue_index < len(catalogue):
        if catalogue_index >= 1:
            print_current(catalogue[catalogue_index - 1][1])
        print_chessboard(catalogue[catalogue_index][1], catalogue_index, goal)
        catalogue_index += 1


def event_handle_btn_prev(e):
    global g  
    global catalogue_index
    if catalogue_index >= 1:
        catalogue_index -= 1
    if catalogue_index >= 0 and catalogue_index < len(catalogue):
        if catalogue_index >= 1:
            print_current(catalogue[catalogue_index - 1][1])
        print_chessboard(catalogue[catalogue_index][1], catalogue_index, goal)


def main(taci):
    taciAstar(taci)
    btnNext_event = create_proxy(event_handle_btn_next)
    btnNext = document.getElementById("buttonNext")
    btnNext.addEventListener("click", btnNext_event)
    btnPrev_event = create_proxy(event_handle_btn_prev)
    btnPrev = document.getElementById("buttonPrev")
    btnPrev.addEventListener("click", btnPrev_event)

def read_complete(e):
    # event is ProgressEvent
	# console.log('read_complete')
    global start
    global goal
    taci = e.target.result
    text = list(taci.split('\n'))
    title = text[0]
    for i in range(1, 4):
        fline = list(text[i].strip('\r').split(" "))
        start.append(fline)    
    title = text[4]
    for i in range(5, 8):
        fline = list(text[i].strip('\r').split(" "))
        goal.append(fline)
    global heap
    heap = [(g + h(start, goal), start)]
    print_chessboard(heap, g, goal)
    print_start(start)
    print_current(heap)
    print_goal(goal)
    main(taci)

def process_file(x):
	fileList = document.getElementById('file').files
 
	for f in fileList:
		# reader is a pyodide.JsProxy
		reader = js.FileReader.new()
 
		# Create a Python proxy for the callback function
		onload_event = create_proxy(read_complete)
 
		reader.onload = onload_event
 
		reader.readAsText(f)
 
	return
 
def setup():
	# Create a Python proxy for the callback function
	file_event = create_proxy(process_file)
 
	# Set the listener to the callback
	e = document.getElementById("file")
	e.addEventListener("change", file_event, False)

setup()

# if __name__ == '__main__':
#     main()

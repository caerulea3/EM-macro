import sys

inform_basic = "EM Macro V1.0.2 : last update 2022-10-28\nby DI 이기언\n"

def spliter(word):
    """
    한글 단어를 입력받아서 초성/중성/종성을 구분하여 리턴해줍니다. 
    """
    ####################################
    # 초성 리스트. 00 ~ 18
    CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    # 중성 리스트. 00 ~ 20
    JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
    # 종성 리스트. 00 ~ 27 + 1(1개 없음)
    JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    ####################################
    r_lst = []
    
    for w in word:
      if '가'<=w<='힣':
        ch1 = (ord(w) - ord('가'))//588
        r_lst.append(CHOSUNG_LIST[ch1])

    return "".join(r_lst)

try:
  with open("./temp.txt", 'r') as f:
    lines = f.readlines()
except FileNotFoundError as e:
  print(e)
  inform = inform_basic + "\
temp.txt.파일을 인식하지 못했습니다.\n\
temp.txt 파일을 프로그램과 같은 폴더에 작성한 후, \n\
해당 파일에 텔레그램 술기 내용을 원하는 만큼 ctrl c-v하신 뒤\n\
EM macro.exe 파일을 실행하시면아직 수행되지 않은 술기를 정리해드립니다\n\
"
  with open("./out.txt", 'w') as f:
      f.write(inform)
  sys.exit()


lines.remove("\n")

stack = []
unremoved = []

for i in range(0, len(lines)-1):
  if "인턴" in lines[i] or "PA간호사" in lines[i] or "이 기언" in lines[i]:
    # 인턴 메시지를 x에 저장
    if "사용자에게 답장" in lines[i+1]:
      x = lines[i+2]
    else:
      x = lines[i+1]

    found = False
    x = x[:-1].replace("/", " ")
    x_spl = x.split(" ")

    # stack에서 수행오더 삭제
    for z in x_spl:
      for y in stack:
        if (z in y) or (spliter(y.split("님")[0].replace("대기실", "")) == z) or (spliter(y.split(" ")[0].replace("대기실", "")) == z):
          stack.remove(y)
          found = True
        try:
          if (spliter(y.split(" ")[1].replace("대기실", "")) == z):
            stack.remove(y)
            found = True
        except:
          continue

      if not found:
        unremoved.append(z)

  elif "간호사," in lines[i]:
    if "답장" in lines[i+1]:
      continue
    head = lines[i+1][:int(len(lines[i+1])*0.5)]
    head_matched = False
    for s in stack:
      if s.startswith(head):
        head_matched = True
    if not head_matched:
      stack.append(lines[i+1])

inform = inform_basic + "\
temp.txt 파일에 텔레그램 술기 내용을 원하는 만큼 ctrl c-v하신 뒤\n\
EM macro.exe 파일을 실행하시면아직 수행되지 않은 술기를 정리해드립니다\n\
\"===미인식 목록===\" 아래에 있는 항목은 프로그램이 인식하지 못한 인턴 대화를 올려두는 곳이니,\n\
반드시 이를 참고하여 지울 것 지우시기 바랍니다.\n\n\n\
"

with open("./out.txt", 'w') as f:
    f.write(inform)
    f.write("===남은 술기===\n")
    f.write("".join(stack) + "\n")
    f.write("===미인식 목록==="+ "\n")
    f.write(", ".join(unremoved))

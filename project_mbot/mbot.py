import os
import io
import time
import pandas as pd
import PySimpleGUI as sg

from PIL import Image
from textwrap import fill
from mbti_data import mbti_dict


# MBTI 궁합 해석: 관계
mbti_compatibility = {1: '잘맞지 않는 관계', 2: '평범한 관계', 3: '자신을 마주보는 거울 같은 관계', 4: '이상적인 관계'}


# MBTI 궁합 해석: 상세 해석
def mbti_score(df, mbti_me, mbti_you):
    mbti_me = mbti_me.upper()
    mbti_you = mbti_you.upper()
    return df.loc[mbti_me, mbti_you]


# MBTI 간편 검사: 질문과 분석
def mbti_simple_test():

    ei_questions = ["1. 처음 보는 사람을 만나면 먼저 말을 거는 편이다.",
                    "2. 팀 기반 활동에 참여하는 것을 좋아한다.",
                    "3. 혼자서 시간을 보내기보다는 다른 사람들과 시간을 보내면서 에너지를 얻는다."]

    sn_questions = ["4. 지금 당장 눈앞에 보이는 현실을 해결하는 데 집중한다.",
                    "5. 설명은 간단하고 명확하며, 사실 위주로 말하는 것이 좋다.",
                    "6. 새로운 개념이나 이론보다는 실제 사례나 경험이 더 잘 이해된다."]

    tf_questions = ["7. 불공평한 것이 가장 나쁘다고 생각한다.",
                    "8. 친구의 잘못된 점은 지적해 주는 편이다.",
                    "9. 결정을 내릴 때, 감정보다 논리를 더 중요하게 생각한다."]

    jp_questions = ["10. 매일 할 일을 계획하는 것이 좋다.",
                    "11. 내 방이 항상 깔끔하게 정돈되어 있어야 마음이 편하다.",
                    "12. 그때그때 상황에 따라 움직이기보다는, 정해진 계획을 따르기를 선호한다."]

    ei = ask(ei_questions)
    if ei is None:
        return None

    sn = ask(sn_questions)
    if sn is None:
        return None

    tf = ask(tf_questions)
    if tf is None:
        return None

    jp = ask(jp_questions)
    if jp is None:
        return None

    mbti = ""
    if ei >= 2:
        mbti += "E"
    else:
        mbti += "I"

    if sn >= 2:
        mbti += "S"
    else:
        mbti += "N"

    if tf >= 2:
        mbti += "T"
    else:
        mbti += "F"

    if jp >= 2:
        mbti += "J"
    else:
        mbti += "P"

    return mbti


# MBTI 간편 검사: 질문 종합
def ask(questions):
    count = 0
    for q in questions:
        answer = sg.popup_yes_no(q)
        if answer is None:
            return None
        if answer == "Yes":
            count += 1
    return count


# 분석 중 팝업
def time_delay_popup(message="MBOT이 분석 중입니다...\n잠시만 기다려주세요!", seconds=3):
    image_path = os.path.join("images", "mbot_2.png")
    image_data = load_images(image_path)

    layout = ([[sg.Image(data=image_data)]] +
              [[sg.Text(line, justification="center")] for line in message.split("\n")])

    window = sg.Window("", layout, modal=True, finalize=True)
    window.refresh()
    time.sleep(seconds)
    window.close()


# 이미지 로드
def load_images(images_path, max_width=200, max_height=200):
    try:
        images = Image.open(images_path)
        images.thumbnail((max_width, max_height))
        buffer = io.BytesIO()
        images.save(buffer, format="PNG")
        return buffer.getvalue()
    except Exception as error:
        print(f"[이미지 오류] {images_path} 를 불러올 수 없습니다: {error}")
        return None


# MBTI 유형별 분석 중 팝업
def mbti_delay_popup(mbti_type, seconds=3):
    image_path = os.path.join("images", "type", f"{mbti_type}.png")
    image_data = load_images(image_path)

    layout = ([[sg.Image(data=image_data)]] +
              [[sg.Text("MBOT이 분석 중입니다...", justification="center")],
               [sg.Text("잠시만 기다려주세요!", justification="center")]])

    window = sg.Window("", layout, modal=True, finalize=True)
    window.refresh()
    time.sleep(seconds)
    window.close()


def main():
    filename_score = "./mbti_score.csv"
    filename_relation = "./mbti_relation.csv"
    df_score = pd.read_csv(filename_score, index_col=0, skipinitialspace=True)
    df_relation = pd.read_csv(filename_relation, index_col=0, skipinitialspace=True)

    mbot_image_path = os.path.join("images", "mbot.png")
    mbot_image_data = load_images(mbot_image_path)

    sg.theme("lightblue")
    layout = [[sg.Column([
        [sg.Text("")],
        [sg.Text("안녕하세요!  MBTI 박사"),
         sg.Text("MBOT", text_color="deepskyblue", font=("Any", 12, "bold")),
         sg.Text("입니다.")],
        [sg.Image(data=mbot_image_data)],
        [sg.Text("메뉴를 선택해주세요.")],
        [sg.Button("MBTI 궁합 해석"), sg.Button("MBTI 간편 검사"), sg.Button("MBTI 유형별 특징")]],
        element_justification="center")],
        [sg.Push(), sg.Button("종료")]]

    window = sg.Window("MBOT", layout)

    # 메인 메뉴 시작
    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "종료"):
            sg.popup("다음에 다시 만나요!")
            break



        # 메뉴 1번: MBTI 궁합 해석
        elif event == "MBTI 궁합 해석":
            sg.popup("MBTI 궁합 해석을 시작합니다!", title="")


            # 1단계 나의 MBTI 입력
            while True:
                mbti_me = sg.popup_get_text("나의 MBTI를 입력해주세요.", title="나의 MBTI")

                if mbti_me is None: # 취소 시
                    sg.popup("입력이 취소되었습니다.", title="")
                    break

                mbti_me = mbti_me.strip().upper()

                if not mbti_me or mbti_me not in mbti_dict: # 빈칸 또는 잘못된 단어 입력 시
                    sg.popup("올바른 MBTI를 입력해주세요!", title="")
                    continue
                break

            if mbti_me is None:
                continue


            # 2단계 상대방의 MBTI 입력
            while True:
                mbti_you = sg.popup_get_text("상대방의 MBTI를 입력해주세요.", title="상대방의 MBTI")

                if mbti_you is None: # 취소 시
                    sg.popup("입력이 취소되었습니다.", title="")
                    break

                mbti_you = mbti_you.strip().upper()

                if not mbti_you or mbti_you not in mbti_dict: # 빈칸 또는 잘못된 단어 입력 시
                    sg.popup("올바른 MBTI를 입력해주세요!", title="")
                    continue
                break

            if mbti_you is None:
                continue


            # 3단계 궁합 해석
            score = mbti_score(df_score, mbti_me, mbti_you)
            relation = fill(df_relation.loc[mbti_me, mbti_you], width=45)

            # 분석 중 팝업
            time_delay_popup()

            image_me_path = os.path.join("images", "type", f"{mbti_me}.png")
            image_you_path = os.path.join("images", "type", f"{mbti_you}.png")
            image_me_data = load_images(image_me_path)
            image_you_data = load_images(image_you_path)

            if mbti_me == mbti_you: # MBTI 같을 때
                sg.popup("나와 상대방의 MBTI가 같습니다!", "             운명입니다!",
                         title="EVENT", text_color="deepskyblue", font=("Any", 12, "bold"))

                image_row = [[sg.Image(data=image_me_data)]]
                text_lines = [[sg.Column([
                    [sg.Text(f"나와 상대방:"), sg.Text(f"{mbti_me}",
                                                  text_color="dodgerblue", font=("Any", 18, "bold"))],
                    [sg.Text(f"{mbti_dict[mbti_me]['trait']}입니다.")],
                    [sg.Text("")],
                    [sg.Text("[MBOT의 분석]", text_color="deepskyblue", font=("Any", 15, "bold"))],
                    [sg.Text(f"제가 분석한 두 사람은 {mbti_compatibility[score]}입니다.")],
                    [sg.Text(f"두 사람은 {relation}", justification="center")]], element_justification="center")],
                    [sg.Text("")]]

            else: # MBTI 다를 때
                image_row = [[sg.Image(data=image_me_data), sg.Image(data=image_you_data)]]
                text_lines = [[sg.Column([
                    [sg.Text(f"나"),
                     sg.Text(f"{mbti_me}", text_color="dodgerblue", font=("Any", 18, "bold")),
                     sg.Text(f"                   상대방"),
                     sg.Text(f"{mbti_you}", text_color="crimson", font=("Any", 18, "bold"))],
                    [sg.Text(f"{mbti_me}(나)는 {mbti_dict[mbti_me]['trait']}입니다.")],
                    [sg.Text(f"{mbti_you}(상대방)은 {mbti_dict[mbti_you]['trait']}입니다.")],
                    [sg.Text("")],
                    [sg.Text("[MBOT의 분석]", text_color="deepskyblue", font=("Any", 15, "bold"))],
                    [sg.Text(f"제가 분석한 두 사람은 {mbti_compatibility[score]}입니다.")],
                    [sg.Text(f"두 사람은 {relation}", justification="center")]], element_justification="center")],
                    [sg.Text("")]]

            layout = image_row + text_lines + [[sg.Button("확인")]]
            sg.Window("MBTI 궁합 해석", layout, modal=True, element_justification="center").read(close=True)



        # 메뉴 2번: MBTI 간편 검사
        elif event == "MBTI 간편 검사":
            sg.popup("MBTI 간편 검사를 시작합니다.\n질문에 답해주세요!", title="")


            # 1단계 검사 실행
            result = mbti_simple_test()
            if result is None:
                sg.popup("검사가 중단되었습니다.", title="")
                continue

            # 분석 중 팝업
            time_delay_popup()


            # 2단계 검사 결과
            image_path = os.path.join("images", "type", f"{result}.png")
            image_data = load_images(image_path)

            layout = [[
                sg.Column([
                    [sg.Text("[MBOT의 분석]", text_color="deepskyblue", font=("Any", 15, "bold"))],
                    [sg.Text(f"제가 분석한 MBTI는"),
                     sg.Text(f"{result}", text_color="dodgerblue", font=("Any", 18, "bold")),
                     sg.Text(f"입니다.")],
                    [sg.Text(f"{result}는 {mbti_dict[result]['trait']}입니다.")],
                    [sg.Text("")],
                    [sg.Image(data=image_data)],
                    [sg.Text("")],
                    [sg.Button("확인")]],
                    justification="center", element_justification="center")]]

            sg.Window("MBTI 간편 검사 결과", layout, modal=True, element_justification="center").read(close=True)


            # 3단계 특징 호출
            detail = sg.popup_yes_no(f"{result}의 특징을 보시겠습니까?", title="")

            if detail == "Yes":
                data = mbti_dict[result]
                images = data.get("images", [])
                images_list = []

                for images_file in images:
                    images_path = os.path.join("images", "characters", images_file)
                    images_data = load_images(images_path)
                    images_list.append(sg.Image(data=images_data))

                wrapped_detail = fill(data["detail"], width=70)

                # MBTI 유형별 분석 중 팝업
                mbti_delay_popup(result)


                # 4단계 MBTI 유형 특징
                first_column = [
                    [sg.Text(f"")],
                    [sg.Text(f"[MBOT의 해석]", text_color="deepskyblue", font=("Any", 15, "bold"))],
                    [sg.Text(f"{result}", text_color="dodgerblue", font=("Any", 18, "bold"))],
                    [sg.Text(f"")]]

                image_row = [images_list]

                second_column = [
                    [sg.Text(f"")],
                    [sg.Text(f"대표인물", text_color="dodgerblue", font=("Any", 12, "bold")),
                     sg.Text(f"{data['character']}", font=("Any", 12, "bold"))],
                    [sg.Text(f"")],
                    [sg.Text(f"특징", text_color="dodgerblue", font=("Any", 18, "bold")),
                     sg.Text(f"{wrapped_detail}")],
                    [sg.Text(f"강점", text_color="dodgerblue", font=("Any", 12, "bold")),
                     sg.Text(f"{data['strength']}")],
                    [sg.Text(f"약점", text_color="dodgerblue", font=("Any", 12, "bold")),
                     sg.Text(f" {data['weakness']}")],
                    [sg.Text("")],
                    [sg.Button("닫기")]]

                layout = [[sg.Column(first_column + image_row + second_column, element_justification="center")]]

                sg.Window(f"{result}유형의 특징", layout, modal=True).read(close=True)



        # 메뉴 3번: MBTI 유형별 특징
        elif event == "MBTI 유형별 특징":

            while True:
                mbti_input = sg.popup_get_text("알고 싶은 MBTI를 입력해주세요", title="MBTI 특징 보기")

                if mbti_input is None:
                    sg.popup("입력이 취소되었습니다.", title="")
                    break

                mbti_input = mbti_input.strip().upper()


                # 1단계 특징 호출
                if mbti_input in mbti_dict:
                    data = mbti_dict[mbti_input]
                    images = data.get("images", [])
                    images_list = []

                    for images_file in images:
                        images_path = os.path.join("images", "characters", images_file)
                        images_data = load_images(images_path)
                        images_list.append(sg.Image(data=images_data))

                    wrapped_detail = fill(data["detail"], width=70)

                    # MBTI 유형별 분석 중 팝업
                    mbti_delay_popup(mbti_input)


                    # 2단계 MBTI 유형 특징
                    first_column = [
                        [sg.Text(f"")],
                        [sg.Text(f"[MBOT의 해석]", text_color="deepskyblue", font=("Any", 15, "bold"))],
                        [sg.Text(f"{mbti_input}", text_color="dodgerblue", font=("Any", 18, "bold"))],
                        [sg.Text(f"")]]

                    image_row = [images_list]

                    second_column = [
                        [sg.Text(f"")],
                        [sg.Text(f"대표인물", text_color="dodgerblue", font=("Any", 12, "bold")),
                         sg.Text(f"{data['character']}", font=("Any", 12, "bold"))],
                        [sg.Text(f"")],
                        [sg.Text(f"특징", text_color="dodgerblue", font=("Any", 18, "bold")),
                         sg.Text(f"{wrapped_detail}")],
                        [sg.Text(f"강점", text_color="dodgerblue", font=("Any", 12, "bold")),
                         sg.Text(f"{data['strength']}")],
                        [sg.Text(f"약점", text_color="dodgerblue", font=("Any", 12, "bold")),
                         sg.Text(f" {data['weakness']}")],
                        [sg.Text("")],
                        [sg.Button("닫기")]]

                    layout = [[sg.Column(first_column + image_row + second_column, element_justification="center")]]

                    sg.Window(f"{mbti_input}유형의 특징", layout, modal=True).read(close=True)

                    break

                else: # 빈칸 또는 잘못된 단어 입력 시
                    sg.popup("올바른 MBTI를 입력해주세요!", title="")
                    continue



        else:
            sg.popup("올바른 메뉴를 선택해주세요!", title="")

    window.close()


if __name__ == "__main__":
    main()
from datetime import datetime, timedelta
import random

# 단어 저장 클래스: WordStore는 영어 단어와 그에 대응하는 한국어 뜻을 저장하고 관리하는 역할을 한다.
class WordStore:
    def __init__(self):
        # 기본 저장 단어 목록으로, 각각 영어와 한국어 뜻의 형태로 이루어진 튜플로 구성된 리스트를 초기화한다.
        self.words = [
            ('apple', '사과'),
            ('elephant', '코리리'),
            ('pear', '배'),
            ('strawberry', '따기'),
            ('tiger', '호랑이')
        ]
        # 각 단어의 등록 시간을 저장하기 위한 딕셔너리를 초기화한다.
        self.word_times = {}
        
    def add_word(self, english, korean):
        # 새로운 단어를 추가하는 메소드로, 최대 단어 개수가 100개를 초과하지 않는 경우에만 단어를 추가한다.
        if len(self.words) < 100:
            # 현재 시간을 "년-월-일 시:분:초"의 형태로 저장한다.
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # 새로 입력받은 영어 단어와 한국어 뜻의 튜플을 단어 목록에 추가한다.
            self.words.append((english, korean))
            # 입력된 영어 단어의 등록 시간을 기록한다.
            self.word_times[english] = current_time
            # 사용자에게 단어가 성공적으로 등록되었음을 알린다.
            print(f"단어 '{english}'가 등록되었습니다.")
        else:
            # 단어 개수가 100개를 초과할 경우 사용자에게 더 이상 단어를 추가할 수 없음을 알린다.
            print("단어의 개수가 100개를 추가해 더 이상 추가할 수 없습니다.")
    
    def get_words(self):
        # 현재 저장된 모든 단어 목록을 반환하는 메소드이다.
        return self.words
    
    def get_word_times(self):
        # 단어의 등록 시간 정보를 반환하는 메소드이다.
        return self.word_times
    
    def delete_word(self, word, meaning=None):
        # 특정 단어를 삭제하는 메소드로, 의미가 지정된 경우 해당 의미와 일치하는 단어만 삭제한다.
        if not any(w[0] == word for w in self.words):
            # 단어 목록에 해당 단어가 없는 경우 사용자에게 단어가 없음을 알린다.
            print(f"'{word}' 단어가 사전에 없습니다. (영어로 입력해 주세요)")
            return False
        for w in self.words:
            if w[0] == word:
                # 만약 의미가 지정되었고, 그 의미가 단어의 뜻과 일치하지 않는 경우 알림을 출력한다.
                if meaning and w[1] != meaning:
                    print(f"'{word}' 단어의 의미 '{meaning}'는 사전에 없습니다. (정확한 뜻을 입력해 주세요)")
                    return False
                # 해당 단어를 단어 목록에서 제거한다.
                self.words.remove(w)
                # 해당 단어의 등록 시간 정보도 삭제한다.
                if word in self.word_times:
                    del self.word_times[word]
                return True
        return False
    
    def change_word(self, old_word, old_meaning, new_meaning):
        # 기존 단어의 뜻을 변경하는 메소드이다.
        if not any(w[0] == old_word for w in self.words):
            # 단어 목록에 해당 단어가 없는 경우 사용자에게 단어가 없음을 알린다.
            print(f"'{old_word}' 단어가 사전에 없습니다. (영어로 입력해 주세요)")
            return False
        if any(w[1] == old_word for w in self.words):
            # 만약 뜻이 영어 단어로 입력되었을 경우 사용자에게 오류 메시지를 출력한다.
            print(f"'{old_word}'은(는) 영어 단어로 입력해 주세요.")
            return False
        for i, (word, meaning) in enumerate(self.words):
            if word == old_word:
                # 기존 뜻이 일치하지 않는 경우 알림을 출력하고 종료한다.
                if meaning != old_meaning:
                    print(f"'{old_word}' 단어의 기지 뜻 '{old_meaning}'는 사전에 없습니다. (정확한 뜻을 입력해 주세요)")
                    return False
                # 뜻을 새로운 의미로 업데이트한다.
                self.words[i] = (old_word, new_meaning)
                return True
        return False

# 단어 맞추기 게임 클래스: 사용자가 입력한 단어를 맞추는 게임 기능을 구현한다.
class WordGame:
    def __init__(self, word_store):
        # WordStore 인스턴스를 받아 단어 저장소로 설정한다.
        self.word_store = word_store
        # 사용자가 맞힌 단어의 개수를 초기화한다.
        self.correct_count = 0

    def start_game(self, restart=False):
        # 게임을 시작하는 메소드로, 첫 실행과 재시작을 구분하여 처리한다.
        if not restart:
            # 게임 처음 시작 시 사용자에게 학번, 이름, 날짜 등을 입력받는다.
            student_id = input("학번을 입력하세요: ")
            name = input("이름을 입력하세요: ")
            date = datetime.now().strftime("%m%d")
            # 게임 시작 정보를 출력하여 사용자가 확인할 수 있도록 한다.
            print("\n==================== 영단어 암기 프로그램 ====================")
            print(f"학번: {student_id}\n이름: {name}\n날짜: {date}\n")
            print("============================================================\n")
        
            # 기본적으로 제공되는 모든 단어를 등록 시간과 함께 등록한다.
            for english, korean in self.word_store.get_words():
                self.word_store.word_times[english] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"단어 '{english}'가 등록되었습니다.")
        
            # 사용자가 새로운 단어를 입력하여 등록할 수 있도록 반복적으로 입력받는다.
            while True:
                english = input("새로운 영어 단어를 입력하세요 (게임을 시작하려면 'exit' 입력): ")
                if english.lower() == 'exit':
                    break
                if not english.isascii():
                    # 영어가 아닌 경우 다시 입력하라는 메시지를 출력한다.
                    print("영어 단어를 입력해 주세요.")
                    continue
                korean = input(f"'{english}'의 한국어 뜻을 입력하세요: ")
                if korean.isascii():
                    # 한국어가 아닌 경우 다시 입력하라는 메시지를 출력한다.
                    print("한국어 뜻을 입력해 주세요.")
                    continue
                # 입력한 단어와 뜻을 사용자에게 확인 받는다.
                confirm = input(f"'{english}'의 뜻이 '{korean}'이(가) 맞습니까? (y/n): ")
                if confirm.lower() == 'y':
                    # 사용자가 확인한 경우 단어를 저장소에 추가한다.
                    self.word_store.add_word(english, korean)
                else:
                    # 사용자가 확인하지 않은 경우 단어 추가를 취소한다.
                    print("단어 추가가 취소되었습니다.")
        
        # 등록된 단어 목록을 출력하여 사용자에게 현재 단어 목록을 보여준다.
        print("\n등록된 단어 목록:")
        for english, korean in self.word_store.get_words():
            registration_time = self.word_store.get_word_times().get(english, "시간 없음")
            print(f"단어: {english}, 뜻: {korean}, 등록 시간: {registration_time}")
        
        # 단어 맞추기 게임을 시작한다.
        self.play_game()

    def play_game(self):
        # 단어 맞추기 게임을 진행하는 메소드이다.
        words = self.word_store.get_words()
        # 단어 목록을 무작위로 섞어 문제를 출제한다.
        random.shuffle(words)
        print("\n단어 맞추기 게임을 시작합니다!")
        for idx, (english, korean) in enumerate(words, start=1):
            start_time = datetime.now()
            # 문제를 사용자에게 제시하고 답변을 기다린다.
            answer = input(f"[{idx}번째 문제]\n{english}의 뜻은 무엇일까요? (5초 이내로 입력해주세요): ")
            time_taken = (datetime.now() - start_time).total_seconds()
            if time_taken > 5:
                # 사용자가 5초 이상 걸린 경우 시간이 초과되었음을 알리고 다음 문제로 넘어간다.
                print("시간이 초과되었습니다. 다음 문제로 다운 용입니다.")
                continue
            elif answer == korean:
                # 정답인 경우 정답 메시지를 출력하고 맞힌 문제 개수를 증가시킨다.
                print("정답입니다!")
                self.correct_count += 1
            else:
                # 틀린 경우 한 번 더 기회를 주고 재시도를 진행한다.
                print("틀리었습니다. 한 번 더 기회를 드립니다.")
                start_time = datetime.now()
                answer = input(f"[{idx}번째 문제 - 재시도]\n{english}의 뜻은 무엇일까요? (5초 이내로 입력해주세요): ")
                time_taken = (datetime.now() - start_time).total_seconds()
                if time_taken > 5:
                    # 사용자가 다시 5초 이상 걸린 경우 시간이 초과되었음을 알리고 다음 문제로 넘어간다.
                    print("시간이 초과되었습니다. 다음 문제로 다운 용입니다.")
                    continue
                elif answer == korean:
                    # 정답인 경우 정답 메시지를 출력하고 맞힌 문제 개수를 증가시킨다.
                    print("정답입니다!")
                    self.correct_count += 1
                else:
                    # 재시도에서도 틀린 경우 틀렸음을 알리고 다음 문제로 넘어간다.
                    print("틀리었습니다. 다음 문제로 다운 용입니다.")
        if self.correct_count == len(words):
            # 모든 문제를 맞힌 경우 축하 메시지를 출력하고 후속 선택지를 제공한다.
            print("축하합니다! 모든 문제를 맞추셨습니다!")
            self.retry_or_modify_word_success()
        else:
            # 맞히지 못한 문제가 있는 경우 현재 성과를 출력하고 후속 선택지를 제공한다.
            print(f"현재 {len(words)}문제 중 {self.correct_count}문제를 맞추셨습니다.")
            self.retry_or_exit_fail()

    def retry_or_exit_fail(self):
        # 틀린 문제가 있는 경우 게임을 재도전할지 종료할지 선택하는 메소드이다.
        choice = input("틀리는 문제가 있습니다. 종료하려면 0을, 다시 문제를 풀려면 1을 입력하세요: ")
        if choice == '0':
            print("게임을 종료합니다.")
        elif choice == '1':
            # 재도전을 선택한 경우 맞힌 문제 개수를 초기화하고 게임을 다시 시작한다.
            self.correct_count = 0
            self.play_game()

    def retry_or_modify_word_success(self):
        # 모든 문제를 맞춘 경우 게임을 종료하거나 단어를 삭제, 수정, 추가할 수 있는 선택지를 제공하는 메소드이다.
        choice = input("게임을 종료하려면 0, 삭제하고 싶은 단어가 있으면 1, 단어 뜻을 변경하고 싶다면 2, 추가로 문제를 출제하려면 3을 입력하세요: ")
        if choice == '0':
            print("게임을 종료합니다.")
        elif choice == '1':
            # 단어 삭제를 선택한 경우 삭제할 단어와 의미를 입력받아 삭제한다.
            english = input("삭제할 영어 단어를 입력하세요: ")
            meaning = input("삭제할 단어의 뜻을 입력하세요 (삭제가능): ")
            if meaning == '':
                meaning = None
            if self.word_store.delete_word(english, meaning):
                # 단어가 삭제된 경우 성공 메시지를 출력한다.
                print(f"{english} 단어가 삭제되었습니다.")
            else:
                # 단어가 삭제되지 않은 경우 실패 메시지를 출력한다.
                print(f"{english} 단어를 찾을 수 없습니다.")
            self.retry_or_modify_word_success()
        elif choice == '2':
            # 단어 뜻 변경을 선택한 경우 기존 단어, 뜻, 새로운 뜻을 입력받아 뜻을 변경한다.
            old_english = input("뜻을 변경할 영어 단어를 입력하세요: ")
            old_meaning = input("기지 뜻을 입력하세요: ")
            new_korean = input("새로운 한국어 뜻을 입력하세요: ")
            if self.word_store.change_word(old_english, old_meaning, new_korean):
                # 뜻 변경이 성공한 경우 성공 메시지를 출력한다.
                print(f"{old_english}의 뜻이 '{new_korean}'(으)로 변경되었습니다.")
            else:
                # 뜻 변경이 실패한 경우 실패 메시지를 출력한다.
                print(f"{old_english} 단어를 찾을 수 없거나 입력한 정보가 정확하지 않습니다.")
            self.retry_or_modify_word_success()
        elif choice == '3':
            # 추가로 문제를 출제하려는 경우 맞힌 문제 개수를 초기화하고 게임을 다시 시작한다.
            self.correct_count = 0
            self.play_game()
        else:
            # 추가로 단어를 추가하려는 경우 영어와 한국어 뜻을 입력받아 단어를 추가한다.
            english = input("추가할 영어 단어를 입력하세요: ")
            if not english.isascii():
                print("영어 단어를 입력해 주세요.")
                self.retry_or_modify_word_success()
                return
            korean = input("해당 단어의 한국어 뜻을 입력하세요: ")
            if korean.isascii():
                print("한국어 뜻을 입력해 주세요.")
                self.retry_or_modify_word_success()
                return
            confirm = input(f"'{english}'의 뜻이 '{korean}'이(가) 맞습니까? (y/n): ")
            if confirm.lower() == 'y':
                # 단어 추가가 확인된 경우 단어를 저장소에 추가하고 게임을 다시 시작한다.
                self.word_store.add_word(english, korean)
                self.correct_count = 0
                self.play_game()
            else:
                # 단어 추가가 취소된 경우 이를 알리고 후속 선택지를 제공한다.
                print("단어 추가가 취소되었습니다.")
                self.retry_or_modify_word_success()

# 메인 실행 부분: 단어 저장소와 단어 맞추기 게임을 초기화하고 게임을 시작한다.
if __name__ == "__main__":
    word_store = WordStore()  # WordStore 인스턴스를 생성한다.
    word_game = WordGame(word_store)  # WordGame 인스턴스를 생성하고, WordStore를 인자로 전달한다.
    word_game.start_game()  # 게임을 시작한다.

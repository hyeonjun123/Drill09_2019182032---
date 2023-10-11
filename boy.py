# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import load_image,SDL_KEYDOWN, SDLK_SPACE, \
    get_time,SDLK_RIGHT,SDL_KEYUP, SDLK_LEFT,SDLK_a

import time
import math


#define event function
def space_down(e):
    return e[0] =='INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def time_out(e):
    return e[0] == 'TIME_OUT'
def Auto_Run(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key ==SDLK_a

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT



class AutoRun:
    @staticmethod
    def enter(boy, e):
        if Auto_Run(e):
            boy.dir, boy.action = 1, 1
            boy.speed = 10  # Increase the speed
            boy.scale = 2  # Enlarge the size
            boy.auto_run_start_time = time.time()
    @staticmethod
    def exit(boy, e):
        boy.speed = 5
        boy.scale = 1
        pass

    @staticmethod


    def do(boy):
        boy.frame = (boy.frame + 1) % 8

        if 400 <= boy.x <= 800:
            boy.x += boy.dir * 10

        elif 0 <= boy.x < 400:
            boy.x += boy.dir * 10

        if boy.x == 800:
            boy.dir = -1  # Change direction to move left when reaching 800

        elif boy.x == 0:
            boy.dir = 1

            # if boy.auto_run_start_time is not None:
        #     # Check if 5 seconds have passed
        #     if time.time() - boy.auto_run_start_time >= 5:
        #         boy.change_state(Idle)  # Switch back to idle state

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y+30 ,200,200)


class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e):
            boy.dir, boy.action = 1, 1
        elif left_down(e) or right_up(e):
            boy.dir, boy.action = -1, 0
    @staticmethod
    def exit(boy,e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame +1) %8
        boy.x += boy.dir *5
        pass
    def draw(boy):
        boy.image.clip_draw(boy.frame *100, boy.action*100, 100, 100, boy.x, boy.y)





#소년은 소년의 정보가 있다. statemachine은 소년의 정보를 넘겨받아 처리한다.
class Sleep:
    @staticmethod
    def enter(boy,e):
        pass
    @staticmethod
    def exit(boy,e):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):
        if boy.action == 2:
            boy.image.clip_composite_draw(boy.frame * 100, 200, 100, 100,
                                          -3.141592 / 2, '', boy.x + 25, boy.y - 25, 100, 100)
        else:
            boy.image.clip_composite_draw(boy.frame * 100, 300, 100, 100,
                                      math.pi / 2, '', boy.x - 25, boy.y - 25, 100, 100)
        pass
class Idle:
    @staticmethod
    def enter(boy,e):
        if boy.action == 0:
            boy.action = 2
        elif boy.action == 1:
            boy.action = 3
        boy.action = 3 #####
        boy.dir = 0#########
        boy.frame = 0##########
        print('Idle Enter-고개 숙이기')
        boy.idle_start_time = get_time() #시간가져와서 다시 졸개 만들려고


    @staticmethod
    def exit(boy, e):
        print('Idle Exit-고개 들기')

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.idle_start_time > 3 :
            boy.state_machine.handle_event(('TIME_OUT',0))

        print('Idle Do-드르렁')
    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100,
                            boy.x, boy.y)
        pass



class StateMachine:

    #boy가 첫번째 인자이다. 전달할때 준 self는 boy이다. 받을때 따라서 self가 아니라 boy로 받는다.
    def __init__(self, boy):#초기데이터를 boy를 넘겨준다. self는 모든 클래스의 함수에 들어가있는 자기 자신을 가리키는 self이다.
        self.boy = boy
        self.cur_state = Idle

        self.transitions = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, time_out: Sleep, Auto_Run: AutoRun},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},
            Sleep: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, space_down: Idle},
            AutoRun: {right_down: AutoRun, left_down: AutoRun, right_up: AutoRun, left_up: AutoRun, space_down: AutoRun}
        }

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items(): #self.tran~딕셔너리에 있는 key가 cur_state인 슬립안에있는 아템들을 출력하라
            if check_event(e):
                self.cur_state.exit(self.boy, e)#상태바뀌기전에 sleep exit하고
                self.cur_state = next_state #다음 상태로
                self.cur_state.enter(self.boy, e) #들어왔을 경우 entery 액션을 실행해주면된다.
                return True
        return False

    def start(self):
        self.cur_state.enter(self.boy, ('NONE',0))

    def update(self):
        self.cur_state.do(self.boy)

    def draw(self):
        self.cur_state.draw(self.boy)





class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self) #여기서의 self는 boy이다. boy를 넘겨주는것임
        self.state_machine.start()
        self.speed = 5  # 'speed' 속성을 추가
        self.scale = 1


    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()


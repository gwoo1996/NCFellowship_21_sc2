
__author__ = 'Team_Flash 주홍영 강지우'


import time

import sc2
from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.buff_id import BuffId


class Bot(sc2.BotAI):
    """
    아무것도 하지 않는 봇 예제
    """
    time_flag = 0

    def __init__(self, *args, **kwargs):
        super().__init__()

    def on_start(self):
        """
        새로운 게임마다 초기화
        """
        self.build_order = list()
        self.evoked = dict()
        self.evoked['target move time'] = self.time
        enemy_cc = self.enemy_start_locations[0]  # 적 시작 위치
        self.evoked['target position'] = self.start_location + 0.2 * (enemy_cc.position - self.start_location)
        self.evoked['siege diameter'] = 3

    async def on_step(self, iteration: int):
        """
        :param int iteration: 이번이 몇 번째 스텝인지를 인자로 넘겨 줌

        매 스텝마다 호출되는 함수
        주요 AI 로직은 여기에 구현
        """

        # 유닛들이 수행할 액션은 리스트 형태로 만들어서,
        # do_actions 함수에 인자로 전달하면 게임에서 실행된다.
        # do_action 보다, do_actions로 여러 액션을 동시에 전달하는 
        # 것이 훨씬 빠르다.
        actions = list()

        """
        생산명령 생성
        기본적으로 마린 생산, 가스 300 이상일 때 전투순양함 생산
        """

        ccs = self.units(UnitTypeId.COMMANDCENTER)  # 전체 유닛에서 사령부 검색
        ccs = ccs.idle  # 실행중인 명령이 없는 사령부 검색
        if ccs.exists:  # 사령부가 하나이상 존재할 경우
            cc = ccs.first  # 첫번째 사령부 선택

            if self.minerals >= 450 :
                if self.can_afford(UnitTypeId.BATTLECRUISER):
                    if self.time - self.evoked.get((cc.tag, 'train'), 0) > 1.0:
                        actions.append(cc.train(UnitTypeId.BATTLECRUISER))
                        self.evoked[(cc.tag, 'train')] = self.time
                else:
                    if self.time - self.evoked.get((cc.tag, 'train'), 0) > 1.0:
                        actions.append(cc.train(UnitTypeId.MARINE))
                        self.evoked[(cc.tag, 'train')] = self.time

        enemy_cc = self.enemy_start_locations[0]  # 적 시작 위치
        ally_cc = self.start_location   # 아군 시작위치

        marines = self.units(UnitTypeId.MARINE)  # 해병 검색 할당
        battlecruisers = self.units(UnitTypeId.BATTLECRUISER) # 전투순양함 검색 할당

        if battlecruisers.amount >= 1:
            target = enemy_cc.position
        else:
            target = ally_cc.position + 0.1*(enemy_cc.position - ally_cc.position)


        for marine in marines:
            actions.append(marine.attack(target))
        

        for battle in battlecruisers:
           
            if self.known_enemy_units.exists:
                enemy = self.known_enemy_units.closest_to(battle)
                if battle.distance_to(enemy) < 7.23:    
                    actions.append(battle.move(ally_cc))
                    
                else:
                    actions.append(battle.attack(enemy))

            else:
                actions.append(battle.attack(target))
            
            if self.time - self.time_flag > 1.0:
                if self.known_enemy_units.exists:
                    enemy = self.known_enemy_units.closest_to(battle)

                    if battle.distance_to(enemy) < 6.0:
                        print('enemy pos')
                        print(enemy.position)
                        print('battle pos')
                        print(battle.position)
                        print('battle radius')
                        print(battle.radius)

                self.time_flag = self.time
            
        
        



                       

        await self.do_actions(actions)


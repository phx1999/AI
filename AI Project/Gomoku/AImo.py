import numpy as np
import random
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
DEPTH = 1
ai_list = []
people_list = []
blank_list = []
aipeo_list = []
ROW = 15
COLUMN = 15
aaa = True


# don't change the class name
class AI(object):
    # chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        # You are white or black
        self.color = color
        # the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        # You need add your decision into your candidate_list. System will get the end of your candidate_list as your decision .
        self.candidate_list = []

    # The input is current chessboard.

    def go(self, chessboard):
        # Clear candidate_list
        self.candidate_list.clear()
        # ==================================================================
        # Write your algorithm here
        # Here is the simplest sample:Random decision
        print(chessboard)
        self.ai_list = np.where(chessboard == self.color)
        self.ai_list = list(zip(self.ai_list[0], self.ai_list[1]))
        self.people_list = np.where(chessboard == -self.color)
        self.people_list = list(zip(self.people_list[0], self.people_list[1]))
        self.blank_list = np.where(chessboard == COLOR_NONE)
        self.blank_list = list(zip(self.blank_list[0], self.blank_list[1]))
        self.aipeo_list = np.where(chessboard != COLOR_NONE)
        self.aipeo_list = list(zip(self.aipeo_list[0], self.aipeo_list[1]))
        new_pos = []
        if len(self.aipeo_list) == 0:
            new_pos.clear()
            new_pos.append(round(self.chessboard_size / 2))
            new_pos.append(round(self.chessboard_size / 2))
            self.candidate_list.append(new_pos)
            return
        if len(self.blank_list) == 1:
            for next in self.blank_list:
                self.candidate_list.append(next)
            return
        new_pos = self.run()
        # ==============Find new pos========================================
        # Make sure that the position of your decision in chess board is empty.
        # If not, return error.
        print(new_pos)
        if len(new_pos) == 0:
            for next in self.blank_list:
                print(next)
                new_pos = next
        assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
        # Add your decision into candidate_list, Records the chess board
        self.candidate_list.append(new_pos)

    # 闁告帇鍊栭弻鍥及椤栨碍鍎婇柟瀛樺姃缁拷
    def isgameover(self, idx):
        for (r, c) in idx:
            if r < ROW - 4 and (r, c) in idx and (r + 1, c) in idx and (r + 2, c) in idx and (
                    r + 3, c) in idx and (r + 4, c) in idx:
                return True
            elif c < COLUMN - 4 and (r, c) in idx and (r, c + 1) in idx and (r, c + 2) in idx and (
                    r, c + 3) in idx and (r, c + 4) in idx:
                return True
            elif r < ROW - 4 and c < COLUMN - 4 and (r, c) in idx and (r + 1, c + 1) in idx and (
                    r + 2, c + 2) in idx and (r + 3, c + 3) in idx and (r + 4, c + 4) in idx:
                return True
            elif r > 3 and c < COLUMN - 4 and (r, c) in idx and (r - 1, c + 1) in idx and (
                    r - 2, c + 2) in idx and (r - 3, c + 3) in idx and (r - 4, c + 4) in idx:
                return True
        return False

    # 婵☆偄顑呴悗椋庢嫚閸曨偄鐎婚悶娑虫嫹
    scoreModel = [(1261, (0, 1, 1, 0, 0)),
                  (260, (1, 1, 0, 0, 0)),
                  (260, (0, 1, 0, 0, 1,0)),
                  (260, (0, 1, 0, 0, 1,0)),
                  (260, (0, 0, 0, 1, 1)),
                  (1261, (0, 0, 1, 1, 0)),
                  (260, (1, 0, 1, 0, 0)),
                  (260, (0, 0, 1, 0, 1)),
                  (1115, (1, 0, 0, 1, 1)),
                  (1150, (0, 1, 0, 1, 0)),
                  (1161, (0, 0, 1, 1, 0)),
                  (1300, (1, 1, 0, 1, 0)),
                  (1300, (0, 1, 0, 1, 1)),
                  (1310, (0, 0, 1, 1, 1)),
                  (1310, (1, 1, 1, 0, 0)),
                  (1320, (1, 0, 1, 1, 0)),
                  (1320, (0, 1, 1, 0, 1)),
                  (5170, (0, 1, 1, 1, 0)),
                  (5002, (0, 1, 0, 1, 1, 0)),
                  (5002, (0, 1, 1, 0, 1, 0)),
                  (5000, (1, 1, 1, 0, 1)),
                  (5000, (1, 1, 0, 1, 1)),
                  (5000, (1, 0, 1, 1, 1)),
                  (6000, (1, 1, 1, 1, 0)),
                  (6000, (0, 1, 1, 1, 1)),
                  (50000, (0, 1, 1, 1, 1, 0)),
                  (99999999, (1, 1, 1, 1, 1))]
    # scoreModel = [(60, (1, 1, 0, 0, 0)),
    #               (60, (0, 0, 0, 1, 1)),
    #               (260, (0, 1, 1, 0, 0)),
    #               (100, (0, 1, 0, 0, 1, 0)),
    #               (260, (0, 0, 1, 1, 0)),
    #               (160, (1, 0, 1, 0, 0)),
    #               (160, (0, 0, 1, 0, 1)),
    #               (100, (1, 0, 0, 1, 1)),
    #               (260, (0, 1, 0, 1, 0)),
    #               (260, (1, 1, 0, 1, 0)),
    #               (260, (0, 1, 0, 1, 1)),
    #               (310, (0, 0, 1, 1, 1)),
    #               (310, (1, 1, 1, 0, 0)),
    #               (300, (1, 0, 1, 1, 0)),
    #               (300, (0, 1, 1, 0, 1)),
    #               (5170, (0, 1, 1, 1, 0)),
    #               (5002, (0, 1, 0, 1, 1, 0)),
    #               (5002, (0, 1, 1, 0, 1, 0)),
    #               (5000, (1, 1, 1, 0, 1)),
    #               (5000, (1, 1, 0, 1, 1)),
    #               (5000, (1, 0, 1, 1, 1)),
    #               (5171, (1, 1, 1, 1, 0)),
    #               (5171, (0, 1, 1, 1, 1)),
    #               (50000, (0, 1, 1, 1, 1, 0)),
    #               (99999999, (1, 1, 1, 1, 1))]

    # score_all 閻庢稒锚閸嬪秵绂嶉崱妯侯暡闁哄牆顦抽鍝ョ不濡ゅ嫮绠栭柣銊ュ煢attern (score,patern(x,y)...)
    def calc_score(self, x, y, x_direction, y_direction, list_1, list_2, score_all, is_defend):
        max_score = (0, None)
        # 闂侇剙鐏濋崢銈夋煂瀹ュ拋妲婚悹渚婄磿閻ｅ宕氶弶鎸庡€卞☉鎾亾婵炲牏鏁稿▓鎴﹀磹閿燂拷
        for score_a in score_all:
            for po in score_a[1]:
                if x == po[0] and y == po[1] and x_direction == score_a[2][0] and y_direction == score_a[2][1]:
                    return 0, score_all
        for i in range(-5, 1):
            pos = []
            for j in range(0, 6):
                if (x + (i + j) * x_direction, y + (i + j) * y_direction) in list_1:
                    pos.append(1)
                elif (x + (i + j) * x_direction, y + (i + j) * y_direction) in list_2:
                    pos.append(-1)
                elif x + (i + j) * x_direction < 0 or y + (i + j) * y_direction < 0 or x + (
                        i + j) * x_direction > 14 or y + (i + j) * y_direction > 14:
                    pos.append(-1)
                else:
                    pos.append(0)
            shape5 = tuple(pos[:-1])
            shape6 = tuple(pos)
            if is_defend:
                if shape6 == (-1, 1, 1, 1, 1, 0) and i == -1 and (
                        x + 5 * x_direction, y + 5 * y_direction) in self.blank_list:
                    if 50050 > max_score[0]:
                        max_score = (50050, ((x + (0 + i) * x_direction, y + (0 + i) * y_direction),
                                             (x + (1 + i) * x_direction, y + (1 + i) * y_direction),
                                             (x + (2 + i) * x_direction, y + (2 + i) * y_direction),
                                             (x + (3 + i) * x_direction, y + (3 + i) * y_direction),
                                             (x + (4 + i) * x_direction, y + (4 + i) * y_direction)),
                                     (x_direction, y_direction))
                elif shape6 == (0, 1, 1, 1, 1, -1) and i == -4 and (
                        x - 5 * x_direction, y - 5 * y_direction) in self.blank_list:
                    if 50050 > max_score[0]:
                        max_score = (50050, ((x + (0 + i) * x_direction, y + (0 + i) * y_direction),
                                             (x + (1 + i) * x_direction, y + (1 + i) * y_direction),
                                             (x + (2 + i) * x_direction, y + (2 + i) * y_direction),
                                             (x + (3 + i) * x_direction, y + (3 + i) * y_direction),
                                             (x + (4 + i) * x_direction, y + (4 + i) * y_direction)),
                                     (x_direction, y_direction))
                elif shape6 == (-1, 1, 1, 1, 0, 0) and i == -1:
                    if 5170 > max_score[0]:
                        max_score = (5170, ((x + (0 + i) * x_direction, y + (0 + i) * y_direction),
                                             (x + (1 + i) * x_direction, y + (1 + i) * y_direction),
                                             (x + (2 + i) * x_direction, y + (2 + i) * y_direction),
                                             (x + (3 + i) * x_direction, y + (3 + i) * y_direction),
                                             (x + (4 + i) * x_direction, y + (4 + i) * y_direction)),
                                     (x_direction, y_direction))
                elif shape6 == (0, 0, 1, 1, 1, -1) and i == -4:
                    if 5170 > max_score[0]:
                        max_score = (5170, ((x + (0 + i) * x_direction, y + (0 + i) * y_direction),
                                            (x + (1 + i) * x_direction, y + (1 + i) * y_direction),
                                            (x + (2 + i) * x_direction, y + (2 + i) * y_direction),
                                            (x + (3 + i) * x_direction, y + (3 + i) * y_direction),
                                            (x + (4 + i) * x_direction, y + (4 + i) * y_direction)),
                                     (x_direction, y_direction))
                elif shape6 == (0, 1, 0, 1, 1, 0) and i == -4:
                    if 5170 > max_score[0]:
                        max_score = (5170, ((x + (0 + i) * x_direction, y + (0 + i) * y_direction),
                                            (x + (1 + i) * x_direction, y + (1 + i) * y_direction),
                                            (x + (2 + i) * x_direction, y + (2 + i) * y_direction),
                                            (x + (3 + i) * x_direction, y + (3 + i) * y_direction),
                                            (x + (4 + i) * x_direction, y + (4 + i) * y_direction)),
                                     (x_direction, y_direction))
                elif shape6 == (0, 1, 1, 0, 1, 0) and i == -1:
                    if 5170 > max_score[0]:
                        max_score = (5170, ((x + (0 + i) * x_direction, y + (0 + i) * y_direction),
                                            (x + (1 + i) * x_direction, y + (1 + i) * y_direction),
                                            (x + (2 + i) * x_direction, y + (2 + i) * y_direction),
                                            (x + (3 + i) * x_direction, y + (3 + i) * y_direction),
                                            (x + (4 + i) * x_direction, y + (4 + i) * y_direction)),
                                     (x_direction, y_direction))
                elif shape6 == (0, 1, 1, 0, 1, 1) and i == -1 and (
                        x + 5 * x_direction, y + 5 * y_direction) in self.blank_list:
                    if 5170 > max_score[0]:
                        max_score = (5170, ((x + (0 + i) * x_direction, y + (0 + i) * y_direction),
                                            (x + (1 + i) * x_direction, y + (1 + i) * y_direction),
                                            (x + (2 + i) * x_direction, y + (2 + i) * y_direction),
                                            (x + (3 + i) * x_direction, y + (3 + i) * y_direction),
                                            (x + (4 + i) * x_direction, y + (4 + i) * y_direction)),
                                     (x_direction, y_direction))
                elif shape6 == (1, 1, 0, 1, 1, 0) and i == -4 and (
                        x - 5 * x_direction, y - 5 * y_direction) in self.blank_list:
                    if 5170 > max_score[0]:
                        max_score = (5170, ((x + (0 + i) * x_direction, y + (0 + i) * y_direction),
                                            (x + (1 + i) * x_direction, y + (1 + i) * y_direction),
                                            (x + (2 + i) * x_direction, y + (2 + i) * y_direction),
                                            (x + (3 + i) * x_direction, y + (3 + i) * y_direction),
                                            (x + (4 + i) * x_direction, y + (4 + i) * y_direction)),
                                     (x_direction, y_direction))
                elif shape6 == (1, 0, 1, 1, 1, 0) and i == -4 and (
                        x - 5 * x_direction, y - 5 * y_direction) in self.blank_list:
                    if 5170 > max_score[0]:
                        max_score = (5170, ((x + (0 + i) * x_direction, y + (0 + i) * y_direction),
                                            (x + (1 + i) * x_direction, y + (1 + i) * y_direction),
                                            (x + (2 + i) * x_direction, y + (2 + i) * y_direction),
                                            (x + (3 + i) * x_direction, y + (3 + i) * y_direction),
                                            (x + (4 + i) * x_direction, y + (4 + i) * y_direction)),
                                     (x_direction, y_direction))
                elif shape6 == (0, 1, 1, 1, 0, 1) and i == -1 and (
                        x + 5 * x_direction, y + 5 * y_direction) in self.blank_list:
                    if 5170 > max_score[0]:
                        max_score = (5170, ((x + (0 + i) * x_direction, y + (0 + i) * y_direction),
                                            (x + (1 + i) * x_direction, y + (1 + i) * y_direction),
                                            (x + (2 + i) * x_direction, y + (2 + i) * y_direction),
                                            (x + (3 + i) * x_direction, y + (3 + i) * y_direction),
                                            (x + (4 + i) * x_direction, y + (4 + i) * y_direction)),
                                     (x_direction, y_direction))
            for score, shape in self.scoreModel:
                if shape5 == shape or shape6 == shape:
                    if score > max_score[0]:
                        max_score = (score, ((x + (0 + i) * x_direction, y + (0 + i) * y_direction),
                                             (x + (1 + i) * x_direction, y + (1 + i) * y_direction),
                                             (x + (2 + i) * x_direction, y + (2 + i) * y_direction),
                                             (x + (3 + i) * x_direction, y + (3 + i) * y_direction),
                                             (x + (4 + i) * x_direction, y + (4 + i) * y_direction)),
                                     (x_direction, y_direction))
        # 閻犱緤绱曢悾濠氭儎闂€鎰攭婵☆偄顑呴懜浼存儍閸曨偄鐎婚柡渚婃嫹
        if max_score[1] is not None:
            score_all.append(max_score)
        return max_score[0], score_all

    # 閻犲洤瀚崣濠囧礆閸℃ɑ娈�
    # def evaluate(self, isai):
    #     total_score = 0
    #     if isai:
    #         list_1 = self.ai_list
    #         list_2 = self.people_list
    #     else:
    #         list_1 = self.people_list
    #         list_2 = self.ai_list
    #     positive_score_total = []
    #     positive_score = 0
    #     for l1 in list_1:
    #         x, y = l1[0], l1[1]
    #         temp_score, positive_score_total = self.calc_score(x, y, 0, 1, list_1, list_2, positive_score_total)
    #         positive_score += temp_score
    #         temp_score, positive_score_total = self.calc_score(x, y, 1, 0, list_1, list_2, positive_score_total)
    #         positive_score += temp_score
    #         temp_score, positive_score_total = self.calc_score(x, y, 1, 1, list_1, list_2, positive_score_total)
    #         positive_score += temp_score
    #         temp_score, positive_score_total = self.calc_score(x, y, -1, 1, list_1, list_2, positive_score_total)
    #         positive_score += temp_score
    #     negetive_score_total = []
    #     negetive_score = 0
    #     for l2 in list_2:
    #         x, y = l2[0], l2[1]
    #         temp_score, negetive_score_total = self.calc_score(x, y, 0, 1, list_2, list_1, negetive_score_total)
    #         negetive_score += temp_score
    #         temp_score, negetive_score_total = self.calc_score(x, y, 1, 0, list_2, list_1, negetive_score_total)
    #         negetive_score += temp_score
    #         temp_score, negetive_score_total = self.calc_score(x, y, 1, 1, list_2, list_1, negetive_score_total)
    #         negetive_score += temp_score
    #         temp_score, negetive_score_total = self.calc_score(x, y, -1, 1, list_2, list_1, negetive_score_total)
    #         negetive_score += temp_score
    #     total_score = positive_score - negetive_score
    #     print(total_score)
    #     return total_score

    # 闂佹彃绉甸弻濠囧箳閹烘垹纰嶇紒宀€鍎らˉ鎰版儎濮楀牏绀夐悘蹇撴缁楀倹绋夐埀顒€鈻庨檱閹倗鈧稒鍔曢幊鍡涘炊鐎靛憡鐣遍柣鎰潐閺備線宕烽妸銉ヮ枀闂傚牞鎷�
    def rearrange(self):
        last_po = self.aipeo_list[-1]
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                else:
                    next_point = (last_po[0] + i, last_po[1] + j)
                    if next_point in self.blank_list:
                        self.blank_list.remove(next_point)
                        self.blank_list.insert(0, next_point)

    def has_neighbor(self, next_step):
        for i in range(-2, 3):
            for j in range(-2, 3):
                if i == 0 and j == 0:
                    continue
                else:
                    if (next_step[0] + i, next_step[1] + j) in self.aipeo_list:
                        return True
        return False

    # 闂侇偅甯掔紞濠囧礄韫囨梻浜伴柛鎺嬪€栭弻鍥ь嚗濡も偓閸ㄥ酣寮甸埀顒侇殗濡粯鐓欐俊妤嬫嫹
    # def negtiveMax(self,isai, depth, alpha, beta):
    #     if self.isgameover(self.ai_list) or self.isgameover(self.people_list) or depth == 0:
    #         return self.evaluate(isai)
    #     # 闂佹彃绉甸弻濠囧箳閹烘垹纰嶇紒宀€鍎らˉ鎰版儎閿燂拷
    #     self.rearrange()
    #     for next_step in self.blank_list:
    #         print(next_step)
    #         if not self.has_neighbor(next_step):
    #             continue
    #         if isai:
    #             self.ai_list.append(next_step)
    #         else:
    #             self.people_list.append(next_step)
    #         self.aipeo_list.append(next_step)
    #         value = -self.negtiveMax(not isai, depth - 1, -beta, -alpha)
    #         if isai:
    #             self.ai_list.remove(next_step)
    #         else:
    #             self.people_list.remove(next_step)
    #         self.aipeo_list.remove(next_step)
    #         if value >= beta:
    #             return beta
    #         if value > alpha:
    #             if depth == DEPTH:
    #                 new_pos.clear()
    #                 new_pos.append(next_step[0])
    #                 new_pos.append(next_step[1])
    #             alpha = value
    #     return alpha
    def run(self):
        new_pos = []
        self.rearrange()
        max_attack = [0, 0]
        max_attack_po = ()
        max_defend = [0, 0]
        max_defend_po = ()
        max_score = 0
        max_score_po = ()
        if self.color == -1:
            r1 = 1.8
            r2 = 1
        else:
            r1 = 1
            r2 = 2
        for nextstep in self.blank_list:
            print(nextstep)
            if not self.has_neighbor(nextstep):
                continue
            self.ai_list.append(nextstep)
            attack_score = self.evaluate(nextstep[0], nextstep[1], self.ai_list, self.people_list, 0) * r1
            if nextstep[0] == 0 or nextstep[0] == 14 or nextstep[1] == 0 or nextstep[1] == 14:
                attack_score -= 10
            self.ai_list.remove(nextstep)
            self.people_list.append(nextstep)
            defend_score = self.evaluate(nextstep[0], nextstep[1], self.people_list, self.ai_list, 1) * r2
            # score=(attack_score+defend_score)*0.1
            # if  score>=max_score:
            #     max_score=score
            #     new_pos=nextstep
            #     self.aaa=False
            if attack_score > max_attack[0] or (attack_score == max_attack[0] and defend_score > max_attack[1]):
                max_attack[0] = attack_score
                max_attack[1] = defend_score
                max_attack_po = nextstep
            if defend_score > max_defend[0] or (defend_score == max_defend[0] and attack_score > max_defend[1]):
                max_defend[0] = defend_score
                max_defend[1] = attack_score
                max_defend_po = nextstep
            self.people_list.remove(nextstep)
            # print(score)
            print(attack_score, " ", defend_score)
        print(max_defend_po)
        if max_attack[0] >= max_defend[0]:
            new_pos = max_attack_po
        else:
            new_pos = max_defend_po
        print(new_pos)
        return new_pos

    def evaluate(self, x, y, list_1, list_2, is_defend):
        positive_score_total = []
        positive_score = 0
        temp_score, positive_score_total = self.calc_score(x, y, 0, 1, list_1, list_2, positive_score_total, is_defend)
        positive_score += temp_score
        temp_score, positive_score_total = self.calc_score(x, y, 1, 0, list_1, list_2, positive_score_total, is_defend)
        positive_score += temp_score
        temp_score, positive_score_total = self.calc_score(x, y, 1, 1, list_1, list_2, positive_score_total, is_defend)
        positive_score += temp_score
        temp_score, positive_score_total = self.calc_score(x, y, -1, 1, list_1, list_2, positive_score_total, is_defend)
        positive_score += temp_score
        return positive_score

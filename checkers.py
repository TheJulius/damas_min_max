from copy import deepcopy
import time
import math

ansi_black = "\u001b[30m"
ansi_red = "\u001b[31m"
ansi_green = "\u001b[32m"
ansi_yellow = "\u001b[33m"
ansi_blue = "\u001b[34m"
ansi_magenta = "\u001b[35m"
ansi_cyan = "\u001b[36m"
ansi_white = "\u001b[37m"
ansi_reset = "\u001b[0m"


class Node:
    def __init__(self, tabuleiro, move=None, parent=None, value=None):
        self.tabuleiro = tabuleiro
        self.value = value
        self.move = move
        self.parent = parent

    def get_children(self, minimizing_jogador, pulo_mandatorio):
        current_state = deepcopy(self.tabuleiro)
        movimentos_disponiveis = []
        children_states = []
        big_letter = ""
        queen_row = 0
        if minimizing_jogador is True:
            movimentos_disponiveis = Damas.encontrar_movimentos_disponiveis(current_state, pulo_mandatorio)
            big_letter = "C"
            queen_row = 7
        else:
            movimentos_disponiveis = Damas.encontrar_movimentos_disponiveis_jogador(current_state, pulo_mandatorio)
            big_letter = "B"
            queen_row = 0
        for i in range(len(movimentos_disponiveis)):
            old_i = movimentos_disponiveis[i][0]
            old_j = movimentos_disponiveis[i][1]
            new_i = movimentos_disponiveis[i][2]
            new_j = movimentos_disponiveis[i][3]
            state = deepcopy(current_state)
            Damas.fazer_movimento(state, old_i, old_j, new_i, new_j, big_letter, queen_row)
            children_states.append(Node(state, [old_i, old_j, new_i, new_j]))
        return children_states

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def get_tabuleiro(self):
        return self.tabuleiro

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent


class Damas:

    def __init__(self):
        self.matrix = [[], [], [], [], [], [], [], []]
        self.turno_jogador = True
        self.computador_pecas = 12
        self.jogador_pecas = 12
        self.movimentos_disponiveis = []
        self.pulo_mandatorio = False

        for row in self.matrix:
            for i in range(8):
                row.append("---")
        self.posicao_computador()
        self.posicao_jogador()

    def posicao_computador(self):
        for i in range(3):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.matrix[i][j] = ("c" + str(i) + str(j))

    def posicao_jogador(self):
        for i in range(5, 8, 1):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.matrix[i][j] = ("b" + str(i) + str(j))

    def print_matrix(self):
        i = 0
        print()
        for row in self.matrix:
            print(i, end="  |")
            i += 1
            for elem in row:
                print(elem, end=" ")
            print()
        print()
        for j in range(8):
            if j == 0:
                j = "     0"
            print(j, end="   ")
        print("\n")

    def get_jogador_input(self):
        movimentos_disponiveis = Damas.encontrar_movimentos_disponiveis_jogador(self.matrix, self.pulo_mandatorio)
        if len(movimentos_disponiveis) == 0:
            if self.computador_pecas > self.jogador_pecas:
                print(
                    ansi_red + "Voce nao tem mais movimentos possiveis e tem menos pecas que o computador.DERROTA!" + ansi_reset)
                exit()
            else:
                print(ansi_yellow + "Voce nao tem mais movimentos possiveis.\nFIM DE JOGO!" + ansi_reset)
                exit()
        self.jogador_pecas = 0
        self.computador_pecas = 0
        while True:

            coord1 = input("Qual peca[i,j]: ")
            if coord1 == "":
                print(ansi_cyan + "Fim de jogo!" + ansi_reset)
                exit()
            elif coord1 == "s":
                print(ansi_cyan + "Voce desistiu.\nCovarde." + ansi_reset)
                exit()
            coord2 = input("Para onde se mover[i,j]:")
            if coord2 == "":
                print(ansi_cyan + "Fim de jogo!" + ansi_reset)
                exit()
            elif coord2 == "s":
                print(ansi_cyan + "Fim de jogo.\nCovarde." + ansi_reset)
                exit()
            old = coord1.split(",")
            new = coord2.split(",")

            if len(old) != 2 or len(new) != 2:
                print(ansi_red + "Input invalido!" + ansi_reset)
            else:
                old_i = old[0]
                old_j = old[1]
                new_i = new[0]
                new_j = new[1]
                if not old_i.isdigit() or not old_j.isdigit() or not new_i.isdigit() or not new_j.isdigit():
                    print(ansi_red + "Input ilegal!" + ansi_reset)
                else:
                    move = [int(old_i), int(old_j), int(new_i), int(new_j)]
                    if move not in movimentos_disponiveis:
                        print(ansi_red + "Movimentacao ilegal!" + ansi_reset)
                    else:
                        Damas.fazer_movimento(self.matrix, int(old_i), int(old_j), int(new_i), int(new_j), "B", 0)
                        for m in range(8):
                            for n in range(8):
                                if self.matrix[m][n][0] == "c" or self.matrix[m][n][0] == "C":
                                    self.computador_pecas += 1
                                elif self.matrix[m][n][0] == "b" or self.matrix[m][n][0] == "B":
                                    self.jogador_pecas += 1
                        break

    @staticmethod
    def encontrar_movimentos_disponiveis(tabuleiro, pulo_mandatorio):
        movimentos_disponiveis = []
        pulos_disponiveis = []
        for m in range(8):
            for n in range(8):
                if tabuleiro[m][n][0] == "c":
                    if Damas.checar_movimentos(tabuleiro, m, n, m + 1, n + 1):
                        movimentos_disponiveis.append([m, n, m + 1, n + 1])
                    if Damas.checar_movimentos(tabuleiro, m, n, m + 1, n - 1):
                        movimentos_disponiveis.append([m, n, m + 1, n - 1])
                    if Damas.checar_pulos(tabuleiro, m, n, m + 1, n - 1, m + 2, n - 2):
                        pulos_disponiveis.append([m, n, m + 2, n - 2])
                    if Damas.checar_pulos(tabuleiro, m, n, m + 1, n + 1, m + 2, n + 2):
                        pulos_disponiveis.append([m, n, m + 2, n + 2])
                elif tabuleiro[m][n][0] == "C":
                    if Damas.checar_movimentos(tabuleiro, m, n, m + 1, n + 1):
                        movimentos_disponiveis.append([m, n, m + 1, n + 1])
                    if Damas.checar_movimentos(tabuleiro, m, n, m + 1, n - 1):
                        movimentos_disponiveis.append([m, n, m + 1, n - 1])
                    if Damas.checar_movimentos(tabuleiro, m, n, m - 1, n - 1):
                        movimentos_disponiveis.append([m, n, m - 1, n - 1])
                    if Damas.checar_movimentos(tabuleiro, m, n, m - 1, n + 1):
                        movimentos_disponiveis.append([m, n, m - 1, n + 1])
                    if Damas.checar_pulos(tabuleiro, m, n, m + 1, n - 1, m + 2, n - 2):
                        pulos_disponiveis.append([m, n, m + 2, n - 2])
                    if Damas.checar_pulos(tabuleiro, m, n, m - 1, n - 1, m - 2, n - 2):
                        pulos_disponiveis.append([m, n, m - 2, n - 2])
                    if Damas.checar_pulos(tabuleiro, m, n, m - 1, n + 1, m - 2, n + 2):
                        pulos_disponiveis.append([m, n, m - 2, n + 2])
                    if Damas.checar_pulos(tabuleiro, m, n, m + 1, n + 1, m + 2, n + 2):
                        pulos_disponiveis.append([m, n, m + 2, n + 2])
        if pulo_mandatorio is False:
            pulos_disponiveis.extend(movimentos_disponiveis)
            return pulos_disponiveis
        elif pulo_mandatorio is True:
            if len(pulos_disponiveis) == 0:
                return movimentos_disponiveis
            else:
                return pulos_disponiveis

    @staticmethod
    def checar_pulos(tabuleiro, old_i, old_j, via_i, via_j, new_i, new_j):
        if new_i > 7 or new_i < 0:
            return False
        if new_j > 7 or new_j < 0:
            return False
        if tabuleiro[via_i][via_j] == "---":
            return False
        if tabuleiro[via_i][via_j][0] == "C" or tabuleiro[via_i][via_j][0] == "c":
            return False
        if tabuleiro[new_i][new_j] != "---":
            return False
        if tabuleiro[old_i][old_j] == "---":
            return False
        if tabuleiro[old_i][old_j][0] == "b" or tabuleiro[old_i][old_j][0] == "B":
            return False
        return True

    @staticmethod
    def checar_movimentos(tabuleiro, old_i, old_j, new_i, new_j):

        if new_i > 7 or new_i < 0:
            return False
        if new_j > 7 or new_j < 0:
            return False
        if tabuleiro[old_i][old_j] == "---":
            return False
        if tabuleiro[new_i][new_j] != "---":
            return False
        if tabuleiro[old_i][old_j][0] == "b" or tabuleiro[old_i][old_j][0] == "B":
            return False
        if tabuleiro[new_i][new_j] == "---":
            return True

    @staticmethod
    def calcular_heuristica(tabuleiro):
        result = 0
        mine = 0
        opp = 0
        for i in range(8):
            for j in range(8):
                if tabuleiro[i][j][0] == "c" or tabuleiro[i][j][0] == "C":
                    mine += 1

                    if tabuleiro[i][j][0] == "c":
                        result += 5
                    if tabuleiro[i][j][0] == "C":
                        result += 10
                    if i == 0 or j == 0 or i == 7 or j == 7:
                        result += 7
                    if i + 1 > 7 or j - 1 < 0 or i - 1 < 0 or j + 1 > 7:
                        continue
                    if (tabuleiro[i + 1][j - 1][0] == "b" or tabuleiro[i + 1][j - 1][0] == "B") and tabuleiro[i - 1][
                        j + 1] == "---":
                        result -= 3
                    if (tabuleiro[i + 1][j + 1][0] == "b" or tabuleiro[i + 1][j + 1] == "B") and tabuleiro[i - 1][j - 1] == "---":
                        result -= 3
                    if tabuleiro[i - 1][j - 1][0] == "B" and tabuleiro[i + 1][j + 1] == "---":
                        result -= 3

                    if tabuleiro[i - 1][j + 1][0] == "B" and tabuleiro[i + 1][j - 1] == "---":
                        result -= 3
                    if i + 2 > 7 or i - 2 < 0:
                        continue
                    if (tabuleiro[i + 1][j - 1][0] == "B" or tabuleiro[i + 1][j - 1][0] == "b") and tabuleiro[i + 2][
                        j - 2] == "---":
                        result += 6
                    if i + 2 > 7 or j + 2 > 7:
                        continue
                    if (tabuleiro[i + 1][j + 1][0] == "B" or tabuleiro[i + 1][j + 1][0] == "b") and tabuleiro[i + 2][
                        j + 2] == "---":
                        result += 6

                elif tabuleiro[i][j][0] == "b" or tabuleiro[i][j][0] == "B":
                    opp += 1

        return result + (mine - opp) * 1000

    @staticmethod
    def encontrar_movimentos_disponiveis_jogador(tabuleiro, pulo_mandatorio):
        movimentos_disponiveis = []
        pulos_disponiveis = []
        for m in range(8):
            for n in range(8):
                if tabuleiro[m][n][0] == "b":
                    if Damas.check_jogador_moves(tabuleiro, m, n, m - 1, n - 1):
                        movimentos_disponiveis.append([m, n, m - 1, n - 1])
                    if Damas.check_jogador_moves(tabuleiro, m, n, m - 1, n + 1):
                        movimentos_disponiveis.append([m, n, m - 1, n + 1])
                    if Damas.check_jogador_jumps(tabuleiro, m, n, m - 1, n - 1, m - 2, n - 2):
                        pulos_disponiveis.append([m, n, m - 2, n - 2])
                    if Damas.check_jogador_jumps(tabuleiro, m, n, m - 1, n + 1, m - 2, n + 2):
                        pulos_disponiveis.append([m, n, m - 2, n + 2])
                elif tabuleiro[m][n][0] == "B":
                    if Damas.check_jogador_moves(tabuleiro, m, n, m - 1, n - 1):
                        movimentos_disponiveis.append([m, n, m - 1, n - 1])
                    if Damas.check_jogador_moves(tabuleiro, m, n, m - 1, n + 1):
                        movimentos_disponiveis.append([m, n, m - 1, n + 1])
                    if Damas.check_jogador_jumps(tabuleiro, m, n, m - 1, n - 1, m - 2, n - 2):
                        pulos_disponiveis.append([m, n, m - 2, n - 2])
                    if Damas.check_jogador_jumps(tabuleiro, m, n, m - 1, n + 1, m - 2, n + 2):
                        pulos_disponiveis.append([m, n, m - 2, n + 2])
                    if Damas.check_jogador_moves(tabuleiro, m, n, m + 1, n - 1):
                        movimentos_disponiveis.append([m, n, m + 1, n - 1])
                    if Damas.check_jogador_jumps(tabuleiro, m, n, m + 1, n - 1, m + 2, n - 2):
                        pulos_disponiveis.append([m, n, m + 2, n - 2])
                    if Damas.check_jogador_moves(tabuleiro, m, n, m + 1, n + 1):
                        movimentos_disponiveis.append([m, n, m + 1, n + 1])
                    if Damas.check_jogador_jumps(tabuleiro, m, n, m + 1, n + 1, m + 2, n + 2):
                        pulos_disponiveis.append([m, n, m + 2, n + 2])
        if pulo_mandatorio is False:
            pulos_disponiveis.extend(movimentos_disponiveis)
            return pulos_disponiveis
        elif pulo_mandatorio is True:
            if len(pulos_disponiveis) == 0:
                return movimentos_disponiveis
            else:
                return pulos_disponiveis

    @staticmethod
    def check_jogador_moves(tabuleiro, old_i, old_j, new_i, new_j):
        if new_i > 7 or new_i < 0:
            return False
        if new_j > 7 or new_j < 0:
            return False
        if tabuleiro[old_i][old_j] == "---":
            return False
        if tabuleiro[new_i][new_j] != "---":
            return False
        if tabuleiro[old_i][old_j][0] == "c" or tabuleiro[old_i][old_j][0] == "C":
            return False
        if tabuleiro[new_i][new_j] == "---":
            return True

    @staticmethod
    def check_jogador_jumps(tabuleiro, old_i, old_j, via_i, via_j, new_i, new_j):
        if new_i > 7 or new_i < 0:
            return False
        if new_j > 7 or new_j < 0:
            return False
        if tabuleiro[via_i][via_j] == "---":
            return False
        if tabuleiro[via_i][via_j][0] == "B" or tabuleiro[via_i][via_j][0] == "b":
            return False
        if tabuleiro[new_i][new_j] != "---":
            return False
        if tabuleiro[old_i][old_j] == "---":
            return False
        if tabuleiro[old_i][old_j][0] == "c" or tabuleiro[old_i][old_j][0] == "C":
            return False
        return True

    def evaluate_states(self):
        t1 = time.time()
        current_state = Node(deepcopy(self.matrix))

        first_computador_moves = current_state.get_children(True, self.pulo_mandatorio)
        if len(first_computador_moves) == 0:
            if self.jogador_pecas > self.computador_pecas:
                print(
                    ansi_yellow + "Computador nao tem mais movimentos, e voce tem mais pecas.\nGANHOU MIZERA!" + ansi_reset)
                exit()
            else:
                print(ansi_yellow + "Computador nao tem mais movimentos.\nFim de jogo!" + ansi_reset)
                exit()
        dict = {}
        for i in range(len(first_computador_moves)):
            child = first_computador_moves[i]
            value = Damas.minimax(child.get_tabuleiro(), 4, -math.inf, math.inf, False, self.pulo_mandatorio)
            dict[value] = child
        if len(dict.keys()) == 0:
            print(ansi_green + "Computador se encurralou.\nDEU SORTE, GANHOU MIZERA!" + ansi_reset)
            exit()
        new_tabuleiro = dict[max(dict)].get_tabuleiro()
        move = dict[max(dict)].move
        self.matrix = new_tabuleiro
        t2 = time.time()
        diff = t2 - t1
        print("Computador moveu (" + str(move[0]) + "," + str(move[1]) + ") para a casa (" + str(move[2]) + "," + str(
            move[3]) + ").")
        print("Em" + str(diff) + " segundos.")

    @staticmethod
    def minimax(tabuleiro, depth, alpha, beta, maximizing_jogador, pulo_mandatorio):
        if depth == 0:
            return Damas.calcular_heuristica(tabuleiro)
        current_state = Node(deepcopy(tabuleiro))
        if maximizing_jogador is True:
            max_eval = -math.inf
            for child in current_state.get_children(True, pulo_mandatorio):
                ev = Damas.minimax(child.get_tabuleiro(), depth - 1, alpha, beta, False, pulo_mandatorio)
                max_eval = max(max_eval, ev)
                alpha = max(alpha, ev)
                if beta <= alpha:
                    break
            current_state.set_value(max_eval)
            return max_eval
        else:
            min_eval = math.inf
            for child in current_state.get_children(False, pulo_mandatorio):
                ev = Damas.minimax(child.get_tabuleiro(), depth - 1, alpha, beta, True, pulo_mandatorio)
                min_eval = min(min_eval, ev)
                beta = min(beta, ev)
                if beta <= alpha:
                    break
            current_state.set_value(min_eval)
            return min_eval

    @staticmethod
    def fazer_movimento(tabuleiro, old_i, old_j, new_i, new_j, big_letter, queen_row):
        letter = tabuleiro[old_i][old_j][0]
        i_difference = old_i - new_i
        j_difference = old_j - new_j
        if i_difference == -2 and j_difference == 2:
            tabuleiro[old_i + 1][old_j - 1] = "---"

        elif i_difference == 2 and j_difference == 2:
            tabuleiro[old_i - 1][old_j - 1] = "---"

        elif i_difference == 2 and j_difference == -2:
            tabuleiro[old_i - 1][old_j + 1] = "---"

        elif i_difference == -2 and j_difference == -2:
            tabuleiro[old_i + 1][old_j + 1] = "---"

        if new_i == queen_row:
            letter = big_letter
        tabuleiro[old_i][old_j] = "---"
        tabuleiro[new_i][new_j] = letter + str(new_i) + str(new_j)

    def play(self):
        print(ansi_cyan + "##### Bem Vindo ao jogo de DAMAS ####" + ansi_reset)
        print("\nAlgumas regras basicas:")
        print("1.Voce move e seleciona as pecas com as coordenadas i,j.")
        print("2.Voce pode sair do jogo a qualquer momento pressionando ENTER.")
        print("3.Voce pode desistir a qualquer momento pressionando 's'.")
        print("Agora que voce esta familiarizado com as regras, divirta-se!")
        while True:
            answer = input("\nPrimeiro, preciso saber, pular é mandatório?[Y/n]: ")
            if answer == "Y" or answer == "y":
                self.pulo_mandatorio = True
                break
            elif answer == "N" or answer == "n":
                self.pulo_mandatorio = False
                break
            elif answer == "":
                print(ansi_cyan + "Fim de jogo!" + ansi_reset)
                exit()
            elif answer == "s":
                print(ansi_cyan + "Voce desistiu antes do jogo comecar....\nPatetico." + ansi_reset)
                exit()
            else:
                print(ansi_red + "input invalido!" + ansi_reset)
        while True:
            self.print_matrix()
            if self.turno_jogador is True:
                print(ansi_cyan + "\nTurno do Player." + ansi_reset)
                self.get_jogador_input()
            else:
                print(ansi_cyan + "Turno do Computador." + ansi_reset)
                print("Thinking...")
                self.evaluate_states()
            if self.jogador_pecas == 0:
                self.print_matrix()
                print(ansi_red + "Voce está sem pecas.\nDERROTA!" + ansi_reset)
                exit()
            elif self.computador_pecas == 0:
                self.print_matrix()
                print(ansi_green + "O computador ficou sem pecas.\nVENCEU MIZERA!" + ansi_reset)
                exit()
            elif self.computador_pecas - self.jogador_pecas == 7:
                wish = input("Voce tem 7 pecas a menos que seu oponente, o fim e inevitavel. Voce quer desistir? Digite Y ou de um ENTER para aceitar")
                if wish == "" or wish == "y" or wish == "Y":
                    print(ansi_cyan + "Covarde." + ansi_reset)
                    exit()
            self.turno_jogador = not self.turno_jogador


if __name__ == '__main__':
    damas = Damas()
    damas.play()
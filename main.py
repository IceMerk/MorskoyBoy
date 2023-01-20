from random import randint


class BoardOutException(Exception):  # Исключение, когда стреляем за доску
    def __str__(self):
        return '❌ Капитан! Сняряд улетел за доску ❌'


class BoardUseException(Exception):  # Исключение, когда стреляем туда же
    def __str__(self):
        return f'❌ Капитан, мы сюда уже стреляли ❌'


class ShipWrongException(Exception):  # Исключение для расстоновки кораблей = None
    pass


class Dot:  # Класс точек
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):  # Сравнение двух точек по x и y
        return self.x == other.x and self.y == other.y

    def __repr__(self):  # Отладочная информация
        return f'Dot({self.x}, {self.y})'


class Ship:  # Класс кораблей
    def __init__(self, na4alo, dlina, orentacia):
        self.na4alo = na4alo  # Начальная точка корабля
        self.dlina = dlina  # Длина корабля
        self.orentacia = orentacia  # горизонтально или вертикально
        self.hp = dlina  # Жизни корабля равные его длине

    @property  # Декоратор, определяет свойства, можем вызывать функцию без call
    def dots(self):
        ship_dots = []  # Список в который собираем корабли
        for i in range(self.dlina):  # Собираем корабль больше 1
            other_x = self.na4alo.x
            other_y = self.na4alo.y

            if self.orentacia == 0:  # Смотрим как расположен корабль
                other_x += i
            elif self.orentacia == 1:
                other_y += i

            ship_dots.append(Dot(other_x, other_y))

        return ship_dots  # Возвращаем корабль

    def popal(self, shot):  # Проверка на попадание в корабль
        return shot in self.dots


class Board:
    def __init__(self, size=6, hid=False):
        self.size = size  # Размер поля
        self.hid = hid  # Нужно ли скрывать тип bool
        self.field = [['~'] * 6 for i in range(self.size)]  # Поле
        self.ships = []  # Спискок кораблей
        self.busy_ships = []  # Список выстрелов мимо/по кораблям
        self.death_ships = 0  # Список убитых кораблей

    def add_ship(self, ship):  # Добавление корабля на доску
        for dot in ship.dots:  # В цикле проверяем точки: в поле ли они и нету ли её в занятых
            if self.out(dot) or dot in self.busy_ships:
                raise ShipWrongException  # Если есть, то кидаем Ошибку
        for dot in ship.dots:  # Если всё норм
            self.field[dot.x][dot.y] = '■'  # Заменяем О на корабль
            self.busy_ships.append(dot)  # Добавляем в список занятых точек кораблей

        self.ships.append(ship)  # Добавляем в список кораблей
        self.contour(ship)  # рисуем контур корабля

    def contour(self, ship, view=False):
        radius = [
            (1, -1), (1, 0), (1, 1),
            (0, -1), (0, 0), (0, 1),
            (-1, -1), (-1, 0), (-1, 1)
        ]
        for dot in ship.dots:  # Берем точки корабля
            for dot_x, dot_y in radius:  # Берем список radius
                check = Dot(dot.x + dot_x, dot.y + dot_y)  # Прогоняем корабль по radius
                if not (self.out(check)) and check not in self.busy_ships:  # Если не входит в диапазон и нету в
                    # списке точек/кораблей
                    if view:  # Если корабль подбит, рисуем возле него точки
                        self.field[check.x][check.y] = '·'
                    self.busy_ships.append(check)  # Добавляем в занятые

    def __str__(self):  # Отрисовка поля
        v = '  | 1 | 2 | 3 | 4 | 5 | 6 |'  # Поле с цифрами сверху
        for i, k in enumerate(self.field):  # Рисуем поле и добавляем цифры сбоку
            v += f'\n{i + 1} | {" | ".join(k)} | '

        if self.hid:  # Если нужно скрыть корабли hid = True
            v = v.replace('■', '~')
        return v

    def out(self, dot):  # Проверяем находится ли точка за пределами доски
        return not ((0 <= dot.x < self.size) and (0 <= dot.y < self.size))

    def shot(self, dot):  # Метод выстрела
        if self.out(dot):  # Если выстрел вне доски
            raise BoardOutException()
        if dot in self.busy_ships:  # Если выстрел уже был
            raise BoardUseException()

        self.busy_ships.append(dot)  # Если всё ок, добавляем в список занятых

        for ship in self.ships:  # Ищем в списке кораблей
            if dot in ship.dots:  # Сверяем - попали или нет
                ship.hp -= 1  # Если попали, то уменьшаем хп у корабля
                self.field[dot.x][dot.y] = 'Х'
                if ship.hp == 0:  # Если хп не осталось
                    self.death_ships += 1  # Пополняем счетчик мертвых
                    self.contour(ship, view=True)  # Рисуем вокруг него точки
                    print('Корабль потоплен')
                    return False
                else:
                    print('Корабль подбит')
                    return True

        self.field[dot.x][dot.y] = '·'  # Если попали Мимо
        print('Мимо')
        return False

    def start(self):  # Обнуляем список занятого
        self.busy_ships = []


class Player:
    def __init__(self, board, board_second):
        self.board = board
        self.board_second = board_second

    def ask(self):  # Долго гуглил это, пока не нашел исключение
        raise NotImplementedError()

    def move(self):  # Спрашиваем игрока сделать выстрел
        while True:
            try:
                t = self.ask()  # Запрос выстрела
                r = self.board_second.shot(t)  # Проверка на доске противника
                return r
            except Exception as e:
                print(e)


class AI(Player):  # Класс комьютера/противника
    def ask(self):  # Метод случайной стрельбы, (нужно докрутить проверку)
        dot = Dot(randint(0, 5), randint(0, 5))
        print(f'Противник открыл огонь по: {dot.x + 1} {dot.y + 1}')
        return dot


class User(Player):  # Игрока
    def ask(self):
        while True:  # Запускаем бесконечный цикл на правильные числа
            vistrel = input('Стреляйте, Капитан: ').split()
            if len(vistrel) != 2:  # Если не 2 координаты
                print('Капитан! нужны Две координаты')
                continue

            x, y = vistrel
            if not (x.isdigit()) or not (y.isdigit()):  # Проверка на числа
                print('Капитан, нам нужы числа!')
                continue
            x1, y1 = int(x), int(y)
            return Dot(x1 - 1, y1 - 1)  # Возвращаем точку выстрела


class Game:  # В этом классе: генерация доски, приветствие пользователя, старт игры
    def __init__(self, size=6):
        self.size = size  # Размер поля
        board_user = self.create_board()  # Создаем поле для игрока
        board_ai = self.create_board()  # Создаем поле для компа
        board_ai.hid = True  # Скрыть корабли компа
        self.user = User(board_user, board_ai)  # Создаем экземпляр игрока и передаем в него доски
        self.ai = AI(board_ai, board_user)  # Создаем компа и передаем в него доски

    def random_board(self):  # Метод перебора вариантов/генерации для доски
        park_ships = [3, 2, 2, 1, 1, 1, 1]  # Парк кораблей по размерам
        board = Board(size=self.size)
        step = 0  # Счетчик шагов для цикла ниже
        for i in park_ships:  # Берем корабль из списка
            while True:
                step += 1
                if step > 2500:  # Общее колличество попыток поставить корабль
                    return None  # Если превысили, то заканчиваем пытаться
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), i, randint(0, 1))  # Берем случайную
                # точку на поле и случайную орентацию
                try:
                    board.add_ship(ship)  # Пытаемся добавить корабль
                    break  # Если поставили корабль, то прерываем цикл
                except ShipWrongException:  # Если нет, то выбрасываем исключение и начинаем с начала
                    pass
        board.start()  # Сбрасываем список занятых точек
        return board

    def greet(self):  # Метод приветствия
        print("⚓️ ️Добро пожаловать ⚓️️\n⚓️  на борт судна  ⚓️\n⚓️     Капитан!    ⚓️\n")
        print("Отдат приказ - выстрелить: x y \nx - номер строки\ny - номер столбца")

    def loop(self):  # Метод запускает цикл игры
        step = 0  # Колличество ходов
        while True:
            print(f'\nДоска Игрока:️\n{self.user.board}️\n\nДоска компьютера:\n{self.ai.board}')
            if step % 2 == 0:  # Есди четный ход, то игрок
                print(f'\nХодит пользователь!')
                replay = self.user.move()  # Если попали, то ходим ещё раз
            else:
                print("\nХодит компьютер!")
                replay = self.ai.move()
            if replay:  # уменьшаем ход на один, чтобы походить ещё раз
                step -= 1

            if self.ai.board.death_ships == 7:  # Проверяем на убитых
                print("\nПользователь выиграл!")
                break

            if self.user.board.death_ships == 7:
                print("\nКомпьютер выиграл!")
                break
            step += 1

    def start(self):  # Метод запускает привветствие и игру
        self.greet()
        self.loop()

    def create_board(self):  # Метод создание доски
        board = None
        while board is None:  # Пока поле пустое, пытаемся создать поле
            board = self.random_board()
        return board  # Возвращаем поле с короблями


g = Game()
g.start()

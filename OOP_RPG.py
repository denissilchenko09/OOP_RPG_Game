import random
import os
import sys
import time
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Tuple, Optional, Dict, Any

# Константы
MAP_WIDTH = 60
MAP_HEIGHT = 20

# Пул имен врагов
ENEMY_NAMES = [
    "Призрачный Страж", "Кристальный Голем", "Лесной Оборотень",
    "Пещерный Троль", "Древний Лич", "Огненный Элементаль",
    "Теневой Убийца", "Ядовитый Паук-гигант", "Костяной Рыцарь",
    "Горный Троль", "Ледяной Феникс", "Каменный Голем"
]

# Пул имен для игрока
HERO_NAMES = ["Аэлиндор", "Каэль", "Сильвана", "Торин", "Морвин", "Лилу", "Геральд"]

# Класс для перечисления типов врагов
class EnemyType(Enum):
    NORMAL = "normal"
    ELITE = "elite"
    BOSS = "boss"

# ========== АБСТРАКТНАЯ ФАБРИКА ==========
class CharacterFactory(ABC):
    """Абстрактная фабрика для создания персонажей"""
    
    @abstractmethod
    def create_normal_enemy(self, x: int, y: int) -> 'Hero':
        pass
    
    @abstractmethod
    def create_elite_enemy(self, x: int, y: int) -> 'Hero':
        pass
    
    @abstractmethod
    def create_boss(self, x: int, y: int) -> 'Hero':
        pass

class TreasureFactory(ABC):
    """Абстрактная фабрика для создания сокровищ"""
    
    @abstractmethod
    def create_treasure(self) -> Dict[str, Any]:
        pass

# ========== КОНКРЕТНЫЕ ФАБРИКИ ==========
class EasyLevelFactory(CharacterFactory):
    """Фабрика для легкого уровня сложности"""
    
    def __init__(self, level: int = 1):
        self.level = level
        self.multiplier = 0.8
    
    def create_normal_enemy(self, x: int, y: int) -> 'Hero':
        name = random.choice(ENEMY_NAMES)
        
        if "Голем" in name:
            base_hp, base_str, base_arm = 40, 8, 6
            symbol = 'G'
        elif "Элементаль" in name:
            base_hp, base_str, base_arm = 30, 12, 2
            symbol = 'E'
        elif "Лич" in name:
            base_hp, base_str, base_arm = 25, 15, 4
            symbol = 'L'
        elif "Троль" in name:
            base_hp, base_str, base_arm = 50, 10, 3
            symbol = 'T'
        else:
            base_hp, base_str, base_arm = 20, 6, 2
            symbol = 'O'
        
        hp = int(base_hp * self.multiplier * (1 + (self.level - 1) * 0.1))
        strength = int(base_str * self.multiplier * (1 + (self.level - 1) * 0.05))
        armor = int(base_arm * self.multiplier)
        
        enemy = Hero(name, x, y, symbol, hp, strength, armor)
        enemy.enemy_type = EnemyType.NORMAL
        enemy.exp_reward = int(hp * 0.4 + strength * 1.5)
        return enemy
    
    def create_elite_enemy(self, x: int, y: int) -> 'Hero':
        enemy = self.create_normal_enemy(x, y)
        enemy.name = "ЭЛИТНЫЙ " + enemy.name
        enemy.hp = int(enemy.hp * 1.3)
        enemy.strength = int(enemy.strength * 1.2)
        enemy.armor = int(enemy.armor * 1.1)
        enemy.enemy_type = EnemyType.ELITE
        enemy.exp_reward = int(enemy.hp * 0.6 + enemy.strength * 2)
        return enemy
    
    def create_boss(self, x: int, y: int) -> 'Hero':
        boss_types = [
            ("ДРЕВНИЙ ДРАКОН ИГНИС", 'D', 250, 25, 15, "dragon"),
            ("АРХИЛИЧ МОРТОК", 'L', 180, 20, 12, "lich"),
            ("КАМЕННЫЙ ТИТАНУС", 'T', 350, 35, 25, "titan")
        ]
        
        boss_name, symbol, base_hp, base_str, base_arm, boss_type = random.choice(boss_types)
        
        hp = int(base_hp * (1 + (self.level // 3 - 1) * 0.15))
        strength = int(base_str * (1 + (self.level // 3 - 1) * 0.1))
        armor = int(base_arm * (1 + (self.level // 3 - 1) * 0.05))
        
        boss = Hero(boss_name, x, y, symbol, hp, strength, armor)
        boss.is_boss = True
        boss.enemy_type = EnemyType.BOSS
        boss.boss_type = boss_type
        boss.exp_reward = 800 * (self.level // 3)
        
        # Особые механики босса
        if boss_type == "dragon":
            boss.abilities = ["Огненное дыхание", "Полёт", "Удар хвостом"]
        elif boss_type == "lich":
            boss.abilities = ["Проклятие", "Призыв скелетов", "Тёмная магия"]
        elif boss_type == "titan":
            boss.abilities = ["Землетрясение", "Каменная броня", "Сокрушающий удар"]
        
        return boss

class NormalLevelFactory(CharacterFactory):
    """Фабрика для нормального уровня сложности"""
    
    def __init__(self, level: int = 1):
        self.level = level
        self.multiplier = 1.0
    
    def create_normal_enemy(self, x: int, y: int) -> 'Hero':
        name = random.choice(ENEMY_NAMES)
        
        if "Голем" in name:
            base_hp, base_str, base_arm = 40, 8, 6
            symbol = 'G'
        elif "Элементаль" in name:
            base_hp, base_str, base_arm = 30, 12, 2
            symbol = 'E'
        elif "Лич" in name:
            base_hp, base_str, base_arm = 25, 15, 4
            symbol = 'L'
        elif "Троль" in name:
            base_hp, base_str, base_arm = 50, 10, 3
            symbol = 'T'
        else:
            base_hp, base_str, base_arm = 20, 6, 2
            symbol = 'O'
        
        hp = int(base_hp * self.multiplier * (1 + (self.level - 1) * 0.15))
        strength = int(base_str * self.multiplier * (1 + (self.level - 1) * 0.1))
        armor = int(base_arm * self.multiplier * (1 + (self.level - 1) * 0.05))
        
        enemy = Hero(name, x, y, symbol, hp, strength, armor)
        enemy.enemy_type = EnemyType.NORMAL
        enemy.exp_reward = int(hp * 0.5 + strength * 2)
        return enemy
    
    def create_elite_enemy(self, x: int, y: int) -> 'Hero':
        enemy = self.create_normal_enemy(x, y)
        enemy.name = "ЭЛИТНЫЙ " + enemy.name
        enemy.hp = int(enemy.hp * 1.5)
        enemy.strength = int(enemy.strength * 1.3)
        enemy.armor = int(enemy.armor * 1.2)
        enemy.enemy_type = EnemyType.ELITE
        enemy.exp_reward = int(enemy.hp * 0.8 + enemy.strength * 3)
        return enemy
    
    def create_boss(self, x: int, y: int) -> 'Hero':
        boss_types = [
            ("ДРЕВНИЙ ДРАКОН ИГНИС", 'D', 300, 30, 20, "dragon"),
            ("АРХИЛИЧ МОРТОК", 'L', 200, 25, 15, "lich"),
            ("КАМЕННЫЙ ТИТАНУС", 'T', 400, 40, 30, "titan")
        ]
        
        boss_name, symbol, base_hp, base_str, base_arm, boss_type = random.choice(boss_types)
        
        hp = int(base_hp * (1 + (self.level // 3 - 1) * 0.2))
        strength = int(base_str * (1 + (self.level // 3 - 1) * 0.15))
        armor = int(base_arm * (1 + (self.level // 3 - 1) * 0.1))
        
        boss = Hero(boss_name, x, y, symbol, hp, strength, armor)
        boss.is_boss = True
        boss.enemy_type = EnemyType.BOSS
        boss.boss_type = boss_type
        boss.exp_reward = 1000 * (self.level // 3)
        
        # Особые механики босса
        if boss_type == "dragon":
            boss.abilities = ["Огненное дыхание", "Полёт", "Удар хвостом"]
            boss.fire_resistant = True
        elif boss_type == "lich":
            boss.abilities = ["Проклятие", "Призыв скелетов", "Тёмная магия"]
            boss.undead = True
        elif boss_type == "titan":
            boss.abilities = ["Землетрясение", "Каменная броня", "Сокрушающий удар"]
            boss.stone_skin = True
        
        return boss

class HardLevelFactory(CharacterFactory):
    """Фабрика для сложного уровня сложности"""
    
    def __init__(self, level: int = 1):
        self.level = level
        self.multiplier = 1.3
    
    def create_normal_enemy(self, x: int, y: int) -> 'Hero':
        name = random.choice(ENEMY_NAMES)
        
        if "Голем" in name:
            base_hp, base_str, base_arm = 40, 8, 6
            symbol = 'G'
        elif "Элементаль" in name:
            base_hp, base_str, base_arm = 30, 12, 2
            symbol = 'E'
        elif "Лич" in name:
            base_hp, base_str, base_arm = 25, 15, 4
            symbol = 'L'
        elif "Троль" in name:
            base_hp, base_str, base_arm = 50, 10, 3
            symbol = 'T'
        else:
            base_hp, base_str, base_arm = 20, 6, 2
            symbol = 'O'
        
        hp = int(base_hp * self.multiplier * (1 + (self.level - 1) * 0.2))
        strength = int(base_str * self.multiplier * (1 + (self.level - 1) * 0.15))
        armor = int(base_arm * self.multiplier * (1 + (self.level - 1) * 0.1))
        
        enemy = Hero(name, x, y, symbol, hp, strength, armor)
        enemy.enemy_type = EnemyType.NORMAL
        enemy.exp_reward = int(hp * 0.6 + strength * 2.5)
        return enemy
    
    def create_elite_enemy(self, x: int, y: int) -> 'Hero':
        enemy = self.create_normal_enemy(x, y)
        enemy.name = "ЭЛИТНЫЙ " + enemy.name
        enemy.hp = int(enemy.hp * 1.7)
        enemy.strength = int(enemy.strength * 1.5)
        enemy.armor = int(enemy.armor * 1.4)
        enemy.enemy_type = EnemyType.ELITE
        enemy.exp_reward = int(enemy.hp * 1.0 + enemy.strength * 4)
        return enemy
    
    def create_boss(self, x: int, y: int) -> 'Hero':
        boss_types = [
            ("ДРЕВНИЙ ДРАКОН ИГНИС", 'D', 350, 35, 25, "dragon"),
            ("АРХИЛИЧ МОРТОК", 'L', 250, 30, 20, "lich"),
            ("КАМЕННЫЙ ТИТАНУС", 'T', 450, 45, 35, "titan")
        ]
        
        boss_name, symbol, base_hp, base_str, base_arm, boss_type = random.choice(boss_types)
        
        hp = int(base_hp * (1 + (self.level // 3 - 1) * 0.25))
        strength = int(base_str * (1 + (self.level // 3 - 1) * 0.2))
        armor = int(base_arm * (1 + (self.level // 3 - 1) * 0.15))
        
        boss = Hero(boss_name, x, y, symbol, hp, strength, armor)
        boss.is_boss = True
        boss.enemy_type = EnemyType.BOSS
        boss.boss_type = boss_type
        boss.exp_reward = 1200 * (self.level // 3)
        
        # Особые механики босса
        if boss_type == "dragon":
            boss.abilities = ["Огненное дыхание", "Полёт", "Удар хвостом", "Лава"]
            boss.fire_resistant = True
            boss.flying = True
        elif boss_type == "lich":
            boss.abilities = ["Проклятие", "Призыв скелетов", "Тёмная магия", "Ужас"]
            boss.undead = True
            boss.magic_immune = True
        elif boss_type == "titan":
            boss.abilities = ["Землетрясение", "Каменная броня", "Сокрушающий удар", "Разлом"]
            boss.stone_skin = True
            boss.stun_chance = 0.3
        
        return boss

# ========== ФАБРИКИ СОКРОВИЩ ==========
class EasyTreasureFactory(TreasureFactory):
    """Фабрика сокровищ для легкого уровня"""
    
    def create_treasure(self) -> Dict[str, Any]:
        treasures = [
            ("Золотой слиток", "Добавляет 70 опыта", lambda p: p.gain_exp(70)),
            ("Малое зелье здоровья", "Восстанавливает 30 HP", lambda p: p.heal(30)),
            ("Большое зелье здоровья", "Восстанавливает 70 HP", lambda p: p.heal(70)),
            ("Эликсир силы", "+3 к силе", lambda p: setattr(p, 'strength', p.strength + 3)),
            ("Эликсир защиты", "+4 к защите", lambda p: setattr(p, 'armor', p.armor + 4)),
            ("Броня дракона", "+10 к максимальному HP", lambda p: setattr(p, 'max_hp', p.max_hp + 10)),
            ("Свиток телепортации", "Переносит в случайную комнату", lambda p: None),
            ("Зачарованный меч", "+4 к силе на следующий бой", lambda p: setattr(p, 'temp_strength_bonus', 4)),
            ("Щит стража", "+5 к защите на следующий бой", lambda p: setattr(p, 'temp_armor_bonus', 5)),
            ("Королевский амулет", "+1 ко всем характеристикам", lambda p: [
                setattr(p, 'strength', p.strength + 1),
                setattr(p, 'armor', p.armor + 1),
                setattr(p, 'max_hp', p.max_hp + 5),
                p.heal(5)
            ])
        ]
        return random.choice(treasures)

class NormalTreasureFactory(TreasureFactory):
    """Фабрика сокровищ для нормального уровня"""
    
    def create_treasure(self) -> Dict[str, Any]:
        treasures = [
            ("Золотой слиток", "Добавляет 50 опыта", lambda p: p.gain_exp(50)),
            ("Малое зелье здоровья", "Восстанавливает 20 HP", lambda p: p.heal(20)),
            ("Большое зелье здоровья", "Восстанавливает 50 HP", lambda p: p.heal(50)),
            ("Эликсир силы", "+2 к силе", lambda p: setattr(p, 'strength', p.strength + 2)),
            ("Эликсир защиты", "+3 к защите", lambda p: setattr(p, 'armor', p.armor + 3)),
            ("Броня дракона", "+5 к максимальному HP", lambda p: setattr(p, 'max_hp', p.max_hp + 5)),
            ("Свиток телепортации", "Переносит в случайную комнату", lambda p: None),
            ("Зачарованный меч", "+3 к силе на следующий бой", lambda p: setattr(p, 'temp_strength_bonus', 3)),
            ("Щит стража", "+4 к защите на следующий бой", lambda p: setattr(p, 'temp_armor_bonus', 4))
        ]
        return random.choice(treasures)

class HardTreasureFactory(TreasureFactory):
    """Фабрика сокровищ для сложного уровня"""
    
    def create_treasure(self) -> Dict[str, Any]:
        treasures = [
            ("Золотой слиток", "Добавляет 30 опыта", lambda p: p.gain_exp(30)),
            ("Малое зелье здоровья", "Восстанавливает 15 HP", lambda p: p.heal(15)),
            ("Большое зелье здоровья", "Восстанавливает 40 HP", lambda p: p.heal(40)),
            ("Эликсир силы", "+1 к силе", lambda p: setattr(p, 'strength', p.strength + 1)),
            ("Эликсир защиты", "+2 к защите", lambda p: setattr(p, 'armor', p.armor + 2)),
            ("Броня дракона", "+3 к максимальному HP", lambda p: setattr(p, 'max_hp', p.max_hp + 3)),
            ("Свиток телепортации", "Переносит в случайную комнату", lambda p: None),
            ("Зачарованный меч", "+2 к силе на следующий бой", lambda p: setattr(p, 'temp_strength_bonus', 2)),
            ("Щит стража", "+3 к защите на следующий бой", lambda p: setattr(p, 'temp_armor_bonus', 3)),
            ("Проклятый артефакт", "+5 к силе, но -20 HP", lambda p: [
                setattr(p, 'strength', p.strength + 5),
                setattr(p, 'hp', max(1, p.hp - 20))
            ])
        ]
        return random.choice(treasures)

# ========== КЛАСС ГЕРОЯ (остается без изменений, но добавлены фабричные методы) ==========
class Hero:
    def __init__(self, name: str, x: int, y: int, symbol: str, hp: int, strength: int, armor: int):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.strength = strength
        self.armor = armor
        self.x = x
        self.y = y
        self.symbol = symbol
        self.level = 1
        self.exp = 0
        self.next_level_exp = 100
        self.inventory = []
        self.enemy_type = EnemyType.NORMAL
        self.is_boss = False
        self.enraged = False
        self.abilities_used = []
        self.cooldowns = {}
        self.minions = []
    
    @property
    def is_alive(self):
        return self.hp > 0
    
    def attack(self, target: 'Hero') -> Tuple[int, bool]:
        """Атака цели, возвращает урон и был ли критический удар"""
        crit_chance = random.random()
        is_critical = crit_chance < 0.15  # 15% шанс крита
        
        base_damage = self.strength
        if is_critical:
            base_damage *= 2
            if self.is_boss:
                base_damage = int(base_damage * 1.5)  # Криты босса сильнее
        
        variance = random.randint(-2, 2)
        damage = max(1, base_damage + variance - (target.armor // 3))
        
        target.hp -= damage
        return damage, is_critical
    
    def heal(self, amount: int) -> int:
        """Восстановление здоровья, возвращает количество восстановленного HP"""
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - old_hp
    
    def gain_exp(self, amount: int):
        """Получение опыта"""
        self.exp += amount
        if self.exp >= self.next_level_exp:
            self.level_up()
    
    def level_up(self):
        """Повышение уровня героя"""
        self.level += 1
        self.exp = 0
        self.next_level_exp = int(self.next_level_exp * 1.5)
        self.max_hp += 20
        self.hp = self.max_hp
        self.strength += 3
        self.armor += 1
        print(f"\n✨ {self.name} достиг {self.level} уровня!")
        print(f"Увеличено здоровье, сила и защита!")
    
    def get_stats(self) -> str:
        """Получение строки со статистикой"""
        health_bar_length = 20
        filled = int((self.hp / self.max_hp) * health_bar_length)
        empty = health_bar_length - filled
        health_bar = f"[{'█' * filled}{'░' * empty}]"
        return f"""
╔{'═' * 40}╗
║ {'ГЕРОЙ:':<10} {self.name:<28} ║
║ {'УРОВЕНЬ:':<10} {self.level:<28} ║
║ {'ОПЫТ:':<10} {self.exp}/{self.next_level_exp:<26} ║
║ {'ЗДОРОВЬЕ:':<10} {health_bar} {self.hp}/{self.max_hp:<3} ║
║ {'СИЛА:':<10} {self.strength:<28} ║
║ {'ЗАЩИТА:':<10} {self.armor:<28} ║
╚{'═' * 40}╝
"""

class Room:
    def __init__(self, x: int, y: int, w: int, h: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.has_treasure = random.random() < 0.3
        self.has_trap = False
    
    @property
    def center_x(self):
        return self.x + self.w // 2
    
    @property
    def center_y(self):
        return self.y + self.h // 2

class GameMap:
    def __init__(self, level: int = 1, difficulty: int = 2):
        self.level = level
        self.difficulty = difficulty
        
        # Инициализация фабрик в зависимости от сложности
        if difficulty == 1:  # Легкий
            self.character_factory = EasyLevelFactory(level)
            self.treasure_factory = EasyTreasureFactory()
        elif difficulty == 2:  # Нормальный
            self.character_factory = NormalLevelFactory(level)
            self.treasure_factory = NormalTreasureFactory()
        else:  # Сложный
            self.character_factory = HardLevelFactory(level)
            self.treasure_factory = HardTreasureFactory()
        
        self.grid = []
        self.enemies = []
        self.rooms = []
        self.treasures = []
        self.traps = []
        self.boss = None
        self.generate_dungeon()
    
    def generate_dungeon(self):
        """Генерация подземелья с учетом уровня"""
        # Инициализация сетки
        self.grid = [['#' for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        self.rooms = []
        self.enemies = []
        self.treasures = []
        self.traps = []
        self.boss = None
        
        # Параметры, зависящие от уровня
        room_count = random.randint(4 + self.level // 2, 7 + self.level)
        min_room_size = max(3, 3 + self.level // 3)
        max_room_size = min(10, 7 + self.level // 2)
        
        # Генерация комнат
        for _ in range(room_count):
            attempts = 0
            while attempts < 100:
                w = random.randint(min_room_size, max_room_size)
                h = random.randint(min_room_size, max_room_size)
                x = random.randint(1, MAP_WIDTH - w - 2)
                y = random.randint(1, MAP_HEIGHT - h - 2)
                
                new_room = Room(x, y, w, h)
                
                # Проверка на пересечение с другими комнатами
                if not any(self.rooms_overlap(new_room, existing_room) for existing_room in self.rooms):
                    self.create_room(new_room)
                    
                    if self.rooms:
                        last_room = self.rooms[-1]
                        self.create_tunnel(last_room, new_room)
                    
                    self.rooms.append(new_room)
                    break
                attempts += 1
        
        # Спавн врагов, сокровищ и ловушек с использованием фабрик
        self.spawn_enemies()
        self.spawn_treasures()
        
        # Добавляем босса на каждом 3-м уровне
        if self.level % 3 == 0:
            self.spawn_boss()
        
        # Добавляем ловушки на высоких уровнях
        if self.level >= 2:
            self.spawn_traps()
    
    def rooms_overlap(self, room1: Room, room2: Room, padding: int = 2) -> bool:
        """Проверка на пересечение комнат"""
        return not (room1.x + room1.w + padding < room2.x or
                   room2.x + room2.w + padding < room1.x or
                   room1.y + room1.h + padding < room2.y or
                   room2.y + room2.h + padding < room1.y)
    
    def create_room(self, room: Room):
        """Создание комнаты на карте"""
        for y in range(room.y, room.y + room.h):
            for x in range(room.x, room.x + room.w):
                if 0 <= y < MAP_HEIGHT and 0 <= x < MAP_WIDTH:
                    self.grid[y][x] = '.'
    
    def create_tunnel(self, room1: Room, room2: Room):
        """Создание туннеля между комнатами (L-образный, без диагоналей)"""
        x1, y1 = room1.center_x, room1.center_y
        x2, y2 = room2.center_x, room2.center_y
        
        # Случайно выбираем: сначала горизонтально или вертикально
        if random.choice([True, False]):
            # Горизонтально, затем вертикально
            for x in range(min(x1, x2), max(x1, x2) + 1):
                if 0 <= y1 < MAP_HEIGHT and 0 <= x < MAP_WIDTH:
                    self.grid[y1][x] = '.'
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if 0 <= y < MAP_HEIGHT and 0 <= x2 < MAP_WIDTH:
                    self.grid[y][x2] = '.'
        else:
            # Вертикально, затем горизонтально
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if 0 <= y < MAP_HEIGHT and 0 <= x1 < MAP_WIDTH:
                    self.grid[y][x1] = '.'
            for x in range(min(x1, x2), max(x1, x2) + 1):
                if 0 <= y2 < MAP_HEIGHT and 0 <= x < MAP_WIDTH:
                    self.grid[y2][x] = '.'
    
    def spawn_enemies(self):
        """Спавн врагов с использованием фабрики"""
        # Базовое количество врагов
        base_count = 3
        level_bonus = min(self.level * 2, 10)  # Ограничиваем максимальный бонус
        enemy_count = random.randint(base_count, base_count + level_bonus)
        
        # Шанс появления элитных врагов
        elite_chance = min(0.1 + (self.level - 1) * 0.05, 0.3)
        
        for i in range(enemy_count):
            if len(self.rooms) > 1:
                room = random.choice(self.rooms[1:])  # Не спавним в стартовой комнате
            else:
                room = self.rooms[0]
            
            # Выбираем позицию в комнате
            ex = random.randint(max(room.x, 0), min(room.x + room.w - 1, MAP_WIDTH - 1))
            ey = random.randint(max(room.y, 0), min(room.y + room.h - 1, MAP_HEIGHT - 1))
            
            # Определяем, элитный ли враг
            is_elite = random.random() < elite_chance and self.level >= 2
            
            # Создаем врага через фабрику
            if is_elite:
                enemy = self.character_factory.create_elite_enemy(ex, ey)
            else:
                enemy = self.character_factory.create_normal_enemy(ex, ey)
            
            self.enemies.append(enemy)
    
    def spawn_boss(self):
        """Создание босса через фабрику"""
        # Босс появляется в последней комнате
        boss_room = self.rooms[-1]
        
        # Создаем босса через фабрику
        self.boss = self.character_factory.create_boss(boss_room.center_x, boss_room.center_y)
    
    def spawn_treasures(self):
        """Размещение сокровищ на карте"""
        treasure_count = random.randint(2 + self.level // 2, 5 + self.level // 2)
        
        for _ in range(treasure_count):
            if self.rooms:
                room = random.choice(self.rooms)
                tx = random.randint(max(room.x, 0), min(room.x + room.w - 1, MAP_WIDTH - 1))
                ty = random.randint(max(room.y, 0), min(room.y + room.h - 1, MAP_HEIGHT - 1))
                self.treasures.append((tx, ty))
    
    def spawn_traps(self):
        """Размещение ловушек на высоких уровнях"""
        trap_count = random.randint(1, 2 + self.level // 2)
        
        for _ in range(trap_count):
            if len(self.rooms) > 1:
                room = random.choice(self.rooms[1:])  # Не в стартовой комнате
                tx = random.randint(max(room.x, 0), min(room.x + room.w - 1, MAP_WIDTH - 1))
                ty = random.randint(max(room.y, 0), min(room.y + room.h - 1, MAP_HEIGHT - 1))
                self.traps.append((tx, ty))
                self.grid[ty][tx] = '^'  # Символ ловушки
    
    def check_trap(self, x: int, y: int, player: Hero) -> Tuple[bool, int]:
        """Проверка на ловушку"""
        if (x, y) in self.traps:
            trap_damage = 5 + self.level * 2
            player.hp -= trap_damage
            self.traps.remove((x, y))
            self.grid[y][x] = '.'
            return True, trap_damage
        return False, 0
    
    def draw(self, player: Hero):
        """Отрисовка карты и информации"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Рисуем верхнюю границу
        print("╔" + "═" * MAP_WIDTH + "╗")
        
        # Рисуем карту
        for y in range(MAP_HEIGHT):
            print("║", end="")
            for x in range(MAP_WIDTH):
                char = self.grid[y][x]
                
                # Игрок
                if player.x == x and player.y == y:
                    print(f"\033[1;32m{player.symbol}\033[0m", end="")
                
                # Босс
                elif self.boss and self.boss.x == x and self.boss.y == y and self.boss.is_alive:
                    print(f"\033[1;35m{self.boss.symbol}\033[0m", end="")  # Фиолетовый для босса
                
                # Враги
                elif any(e.x == x and e.y == y and e.is_alive for e in self.enemies):
                    enemy = next(e for e in self.enemies if e.x == x and e.y == y and e.is_alive)
                    if enemy.enemy_type == EnemyType.ELITE:
                        print(f"\033[1;33m{enemy.symbol}\033[0m", end="")  # Желтый для элитных
                    else:
                        print(f"\033[1;31m{enemy.symbol}\033[0m", end="")  # Красный для обычных
                
                # Сокровища
                elif (x, y) in self.treasures:
                    print(f"\033[1;33m$\033[0m", end="")  # Желтый
                
                # Ловушки
                elif char == '^':
                    print(f"\033[1;31m^\033[0m", end="")  # Красный
                
                # Стены и пол
                elif char == '#':
                    print(f"\033[90m▓\033[0m", end="")  # Серые стены
                elif char == '.':
                    print(f"\033[37m·\033[0m", end="")  # Светлые точки пола
                else:
                    print(char, end="")
            print("║")
        
        # Рисуем нижнюю границу
        print("╚" + "═" * MAP_WIDTH + "╝")
        
        # Статистика игрока
        print(player.get_stats())
        
        # Информация об уровне
        print(f"Уровень подземелья: {self.level}")
        print(f"Сложность: {'Легкий' if self.difficulty == 1 else 'Нормальный' if self.difficulty == 2 else 'Сложный'}")
        
        # Ближайшие враги
        nearby_enemies = []
        for enemy in self.enemies:
            if enemy.is_alive:
                distance = abs(enemy.x - player.x) + abs(enemy.y - player.y)
                if distance <= 8:
                    nearby_enemies.append((enemy, distance))
        
        # Босс
        if self.boss and self.boss.is_alive:
            boss_distance = abs(self.boss.x - player.x) + abs(self.boss.y - player.y)
            if boss_distance <= 12:
                hp_percent = (self.boss.hp / self.boss.max_hp) * 100
                print(f"\n⚠️  БОСС ПРИБЛИЖАЕТСЯ: {self.boss.name}")
                print(f"   Здоровье: {self.boss.hp}/{self.boss.max_hp} ({hp_percent:.1f}%)")
                print(f"   Расстояние: {boss_distance} клеток")
        
        # Ближайшие враги
        if nearby_enemies:
            print(f"\nБлижайшие враги:")
            for enemy, distance in nearby_enemies[:3]:  # Показываем только 3 ближайших
                health_percent = (enemy.hp / enemy.max_hp) * 100
                health_bar_length = 5
                filled = int(health_percent // (100 / health_bar_length))
                health_bar = f"{'█' * filled}{'░' * (health_bar_length - filled)}"
                
                type_indicator = ""
                if enemy.enemy_type == EnemyType.ELITE:
                    type_indicator = " [ЭЛИТНЫЙ]"
                
                print(f"  {enemy.name}{type_indicator} - {health_bar} ({distance} клеток)")
    
    def is_walkable(self, x: int, y: int) -> bool:
        """Проверка, можно ли пройти в клетку"""
        if not (0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT):
            return False
        return self.grid[y][x] != '#'
    
    def get_enemy_at(self, x: int, y: int) -> Optional[Hero]:
        """Получение врага в указанной клетке"""
        for enemy in self.enemies:
            if enemy.is_alive and enemy.x == x and enemy.y == y:
                return enemy
        if self.boss and self.boss.is_alive and self.boss.x == x and self.boss.y == y:
            return self.boss
        return None
    
    def get_treasure_at(self, x: int, y: int) -> bool:
        """Проверка, есть ли сокровище в клетке"""
        return (x, y) in self.treasures


def find_treasure(game_map: GameMap) -> Tuple[str, str, Any]:
    """Создание сокровища через фабрику"""
    treasure = game_map.treasure_factory.create_treasure()
    return treasure


def start_battle(player: Hero, enemy: Hero):
    """Запуск боя с обычным врагом"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("╔" + "═" * 50 + "╗")
    print(f"║{'БОЙ НАЧИНАЕТСЯ!':^50}║")
    
    if enemy.enemy_type == EnemyType.ELITE:
        print(f"║{'ВСТРЕЧА С ЭЛИТНЫМ ВРАГОМ!':^50}║")
    
    print(f"║{f'{player.name} vs {enemy.name}':^50}║")
    print("╚" + "═" * 50 + "╝")
    
    turn = 0
    
    while player.is_alive and enemy.is_alive:
        turn += 1
        
        print(f"\n{'─' * 50}")
        print(f"РАУНД {turn}")
        print(f"{'─' * 50}")
        
        # Статусы
        player_health = f"{player.hp}/{player.max_hp} HP"
        enemy_health = f"{enemy.hp}/{enemy.max_hp} HP"
        
        print(f"\n{player.name:25} {player_health:>10}")
        print(f"{enemy.name:25} {enemy_health:>10}")
        print(f"{'─' * 50}")
        
        # Ход игрока
        print("\nВыберите действие:")
        print("1. Атаковать мечом")
        print("2. Использовать зелье здоровья (+30 HP)")
        print("3. Попытаться сбежать")
        
        try:
            choice = int(input("Ваш выбор: "))
        except ValueError:
            choice = 0
        
        if choice == 1:
            damage, critical = player.attack(enemy)
            if critical:
                print(f"\n✨ КРИТИЧЕСКИЙ УДАР! Вы нанесли {damage} урона!")
            else:
                print(f"\n⚔️ Вы нанесли {damage} урона!")
            
            if not enemy.is_alive:
                break
        
        elif choice == 2:
            if player.hp < player.max_hp:
                healed = player.heal(30)
                print(f"\n🧪 Вы выпили зелье здоровья и восстановили {healed} HP!")
            else:
                print("\nУ вас и так полное здоровье!")
                continue
        
        elif choice == 3:
            # Шанс сбежать зависит от уровня врага
            escape_chance = 0.4
            if enemy.enemy_type == EnemyType.ELITE:
                escape_chance = 0.2
            
            if random.random() < escape_chance:
                print("\n🏃 Вы успешно сбежали из боя!")
                return True  # Успешно сбежали
            else:
                print("\nВраг блокирует ваш путь к отступлению!")
        
        else:
            print("\nНеверный выбор! Пропускаете ход.")
        
        # Ход врага
        if enemy.is_alive:
            damage, critical = enemy.attack(player)
            if critical:
                print(f"\n💥 {enemy.name} наносит критический удар на {damage} урона!")
            else:
                print(f"\n🗡️ {enemy.name} атакует и наносит {damage} урона!")
            
            # Особые способности элитных врагов
            if enemy.enemy_type == EnemyType.ELITE and enemy.is_alive:
                if random.random() < 0.3:  # 30% шанс на особую способность
                    elite_ability = random.choice(["сильный удар", "исцеление"])
                    if elite_ability == "сильный удар":
                        bonus_damage = enemy.strength // 2
                        player.hp -= bonus_damage
                        print(f"💢 {enemy.name} использует СИЛЬНЫЙ УДАР! Дополнительно {bonus_damage} урона!")
                    elif elite_ability == "исцеление":
                        heal_amount = enemy.max_hp // 10
                        enemy.heal(heal_amount)
                        print(f"💚 {enemy.name} исцеляется на {heal_amount} HP!")
        
        if not player.is_alive:
            print(f"\n☠️ {player.name} пал в бою...")
            break
    
    # Результаты боя
    if not enemy.is_alive:
        exp_gained = enemy.exp_reward if hasattr(enemy, 'exp_reward') else enemy.max_hp // 2 + enemy.strength * 2
        player.gain_exp(exp_gained)
        print(f"\n🎉 {enemy.name} повержен!")
        print(f"Получено опыта: {exp_gained}")
        
        # Дополнительные награды за элитных врагов
        if enemy.enemy_type == EnemyType.ELITE:
            print("⭐ Вы победили элитного врага! Получена дополнительная награда!")
            # Шанс на получение редкого предмета
            if random.random() < 0.5:
                rare_items = ["Руна силы", "Амулет защиты", "Сапфир маны"]
                item = random.choice(rare_items)
                player.inventory.append(item)
                print(f"🎁 Получен предмет: {item}")
    
    input("\nНажмите Enter, чтобы продолжить...")
    return False


def start_boss_battle(player: Hero, boss: Hero):
    """Запуск боя с боссом"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("╔" + "═" * 50 + "╗")
    print(f"║{'БИТВА С БОССОМ!':^50}║")
    print(f"║{f'{boss.name}':^50}║")
    print("╚" + "═" * 50 + "╝")
    
    print(f"\n⚡ ОСОБЫЕ МЕХАНИКИ БОССА:")
    
    if boss.boss_type == "dragon":
        print("  • Огненное дыхание: наносит урон по площади")
        print("  • Сопротивление огню: получает меньше урона от огня")
        print("  • Полёт: может уклоняться от атак")
    
    elif boss.boss_type == "lich":
        print("  • Проклятие: уменьшает вашу силу")
        print("  • Призыв скелетов: вызывает помощников")
        print("  • Нежить: невосприимчив к ядам")
    
    elif boss.boss_type == "titan":
        print("  • Землетрясение: оглушает на 1 ход")
        print("  • Каменная кожа: уменьшает получаемый урон")
        print("  • Сокрушение: наносит двойной урон при низком HP")
    
    print(f"\n⚠️  НЕЛЬЗЯ СБЕЖАТЬ ОТ БОССА!")
    print(f"{'─' * 50}")
    
    input("\nНажмите Enter, чтобы начать бой...")
    
    turn = 0
    boss_phase = 1
    
    while player.is_alive and boss.is_alive:
        turn += 1
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Отображение статуса
        print(f"\nХОД {turn}")
        print(f"{'─' * 50}")
        
        # Индикатор здоровья босса
        boss_hp_percent = boss.hp / boss.max_hp
        boss_bar_length = 40
        boss_filled = int(boss_hp_percent * boss_bar_length)
        
        # Определение фазы босса
        if boss_hp_percent > 0.6:
            phase = "I"
            phase_color = "🟢"
        elif boss_hp_percent > 0.3:
            phase = "II"
            phase_color = "🟡"
            
            # Включаем режим ярости при переходе во вторую фазу
            if boss_phase == 1:
                boss_phase = 2
                boss.enraged = True
                boss.strength = int(boss.strength * 1.3)
                print(f"⚡ {boss.name} впадает в ЯРОСТЬ! Его сила увеличивается!")
                input("\nНажмите Enter, чтобы продолжить...")
        else:
            phase = "III"
            phase_color = "🔴"
            
            # Финальная фаза
            if boss_phase == 2:
                boss_phase = 3
                boss.strength = int(boss.strength * 1.5)
                boss.armor = int(boss.armor * 0.7)  # Жертвует защитой ради атаки
                print(f"💀 {boss.name} в ФИНАЛЬНОЙ ФАЗЕ! Сила резко возрастает!")
                input("\nНажмите Enter, чтобы продолжить...")
        
        print(f"\nБОСС [{phase}] {boss.name}")
        print(f"HP: [{phase_color * boss_filled}{'⬜' * (boss_bar_length - boss_filled)}] "
              f"{boss.hp}/{boss.max_hp}")
        
        # Здоровье игрока
        player_hp_percent = player.hp / player.max_hp
        player_bar_length = 40
        player_filled = int(player_hp_percent * player_bar_length)
        player_color = "🟢" if player_hp_percent > 0.3 else "🔴"
        
        print(f"\nИГРОК {player.name}")
        print(f"HP: [{player_color * player_filled}{'⬜' * (player_bar_length - player_filled)}] "
              f"{player.hp}/{player.max_hp}")
        
        print(f"{'─' * 50}")
        
        # Ход игрока
        print("\nВыберите действие:")
        print("1. Атаковать")
        print("2. Использовать зелье здоровья (+50 HP)")
        print("3. Защищаться (уменьшает получаемый урон)")
        
        try:
            choice = int(input("Ваш выбор: "))
        except ValueError:
            choice = 0
        
        player_defending = False
        
        if choice == 1:
            damage, critical = player.attack(boss)
            if critical:
                print(f"\n✨ КРИТИЧЕСКИЙ УДАР! Вы нанесли {damage} урона!")
            else:
                print(f"\n⚔️ Вы нанесли {damage} урона!")
        
        elif choice == 2:
            if player.hp < player.max_hp:
                healed = player.heal(50)
                print(f"\n🧪 Вы выпили зелье здоровья и восстановили {healed} HP!")
            else:
                print("\nУ вас и так полное здоровье!")
                continue
        
        elif choice == 3:
            player_defending = True
            print(f"\n🛡️ Вы принимаете защитную стойку. Следующая атака будет слабее.")
        
        else:
            print("\nНеверный выбор! Пропускаете ход.")
        
        # Ход босса
        if boss.is_alive:
            # Особые способности босса
            if turn % 3 == 0:  # Каждый 3-й ход - особая способность
                if boss.boss_type == "dragon":
                    damage = boss.strength * 2
                    player.hp -= damage
                    print(f"\n🔥 {boss.name} использует ОГНЕННОЕ ДЫХАНИЕ! Нанесено {damage} урона!")
                
                elif boss.boss_type == "lich":
                    # Лич может призывать скелетов
                    if len(boss.minions) < 3:
                        skeleton = Hero("Скелет-слуга", 0, 0, 's', 30, 8, 3)
                        boss.minions.append(skeleton)
                        print(f"\n💀 {boss.name} призывает Скелета-слугу!")
                    
                    # И проклинать игрока
                    curse_damage = boss.strength // 2
                    player.hp -= curse_damage
                    player.strength = max(1, player.strength - 2)
                    print(f"\n☠️ {boss.name} накладывает ПРОКЛЯТИЕ! Нанесено {curse_damage} урона, ваша сила уменьшена!")
                
                elif boss.boss_type == "titan":
                    damage = boss.strength * 3
                    if player_defending:
                        damage = damage // 2  # Защита уменьшает урон
                        print(f"\n🛡️ Ваша защита смягчает удар!")
                    
                    player.hp -= damage
                    print(f"\n🌋 {boss.name} вызывает ЗЕМЛЕТРЯСЕНИЕ! Нанесено {damage} урона!")
                    
                    # Оглушение с шансом
                    if random.random() < 0.5:
                        print(f"💫 Вы оглушены и пропустите следующий ход!")
                        # Здесь можно добавить механику пропуска хода
            else:
                # Обычная атака босса
                if player_defending:
                    damage = max(1, boss.strength // 2 - (player.armor // 3))
                else:
                    damage = max(1, boss.strength - (player.armor // 3))
                
                player.hp -= damage
                print(f"\n👊 {boss.name} атакует и наносит {damage} урона!")
            
            # Атака миньонов босса
            for minion in boss.minions[:]:
                if minion.is_alive:
                    minion_damage = max(1, minion.strength - (player.armor // 3))
                    player.hp -= minion_damage
                    print(f"  💀 {minion.name} атакует! Нанесено {minion_damage} урона")
                else:
                    boss.minions.remove(minion)
        
        time.sleep(2)
    
    # Результат битвы с боссом
    if not boss.is_alive:
        print(f"\n{'🎉' * 25}")
        print(f"        ПОБЕДА НАД {boss.name}!")
        print(f"{'🎉' * 25}")
        
        # Награда за босса
        exp_reward = boss.exp_reward
        player.gain_exp(exp_reward)
        print(f"\n✨ Получено опыта: {exp_reward}")
        
        # Уникальные предметы
        legendary_items = {
            "dragon": ["Сердце дракона", "Чешуя дракона", "Коготь древнего"],
            "lich": ["Филоктерия", "Посох некроманта", "Кольцо тьмы"],
            "titan": ["Камень вечности", "Сердце горы", "Длань титана"]
        }
        
        if boss.boss_type in legendary_items:
            items = legendary_items[boss.boss_type]
            for item in items:
                if random.random() < 0.5:  # 50% шанс на каждый предмет
                    player.inventory.append(item)
                    print(f"🏆 Получен легендарный предмет: {item}")
        
        # Постоянные бонусы
        if boss.boss_type == "dragon":
            player.max_hp += 30
            player.hp = min(player.max_hp, player.hp + 30)
            print(f"🌟 Постоянный бонус: +30 к максимальному здоровью (Сердце дракона)")
        
        elif boss.boss_type == "lich":
            player.strength += 5
            print(f"🌟 Постоянный бонус: +5 к силе (Знания некроманта)")
        
        elif boss.boss_type == "titan":
            player.armor += 5
            print(f"🌟 Постоянный бонус: +5 к защите (Кожа титана)")
    
    input("\nНажмите Enter, чтобы продолжить...")


def find_treasure(player: Hero):
    """Поиск сокровища"""
    treasures = [
        ("Золотой слиток", "Добавляет 50 опыта", lambda p: p.gain_exp(50)),
        ("Малое зелье здоровья", "Восстанавливает 20 HP", lambda p: p.heal(20)),
        ("Большое зелье здоровья", "Восстанавливает 50 HP", lambda p: p.heal(50)),
        ("Эликсир силы", "+2 к силе", lambda p: setattr(p, 'strength', p.strength + 2)),
        ("Эликсир защиты", "+3 к защите", lambda p: setattr(p, 'armor', p.armor + 3)),
        ("Броня дракона", "+5 к максимальному HP", lambda p: setattr(p, 'max_hp', p.max_hp + 5)),
        ("Свиток телепортации", "Переносит в случайную комнату", lambda p: None),
        ("Зачарованный меч", "+3 к силе на следующий бой", lambda p: setattr(p, 'temp_strength_bonus', 3)),
        ("Щит стража", "+4 к защите на следующий бой", lambda p: setattr(p, 'temp_armor_bonus', 4))
    ]
    
    treasure = random.choice(treasures)
    name, description, effect = treasure
    
    print(f"\n{'🎁' * 10}")
    print(f"ВЫ НАШЛИ СОКРОВИЩЕ!")
    print(f"{'🎁' * 10}")
    print(f"\nНазвание: {name}")
    print(f"Эффект: {description}")
    
    if "телепортации" in name.lower():
        input("\nНажмите Enter, чтобы активировать свиток...")
        return "teleport"
    else:
        effect(player)
        print(f"\nЭффект применен!")
        input("Нажмите Enter, чтобы продолжить...")
        return None


def show_inventory(player: Hero):
    """Показать инвентарь игрока"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("╔" + "═" * 50 + "╗")
    print(f"║{'ИНВЕНТАРЬ':^50}║")
    print("╚" + "═" * 50 + "╝")
    
    if not player.inventory:
        print("\nВаш инвентарь пуст.")
    else:
        print(f"\nПредметы ({len(player.inventory)}):")
        for i, item in enumerate(player.inventory, 1):
            print(f"  {i}. {item}")
    
    print(f"\nВаша статистика:")
    print(f"  Уровень: {player.level}")
    print(f"  Опыт: {player.exp}/{player.next_level_exp}")
    print(f"  Здоровье: {player.hp}/{player.max_hp}")
    print(f"  Сила: {player.strength}")
    print(f"  Защита: {player.armor}")
    
    input("\nНажмите Enter, чтобы вернуться...")


def main_menu():
    """Главное меню игры"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("╔" + "═" * 50 + "╗")
    print("║{:^50}║".format("ПОДЗЕМЕЛЬЯ ДРЕВНИХ"))
    print("║{:^50}║".format("РУИНЫ КРИСТАЛЬНОГО ЗАМКА"))
    print("╚" + "═" * 50 + "╝")
    
    print("\n" + "=" * 50)
    print("ГЛАВНОЕ МЕНЮ:")
    print("=" * 50)
    print("1. Новая игра")
    print("2. Загрузить игру (в разработке)")
    print("3. Об игре")
    print("4. Выход")
    
    while True:
        try:
            choice = int(input("\nВаш выбор: "))
            if 1 <= choice <= 4:
                return choice
            else:
                print("Пожалуйста, выберите число от 1 до 4.")
        except ValueError:
            print("Пожалуйста, введите число.")


def about_game():
    """Информация об игре"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("╔" + "═" * 50 + "╗")
    print("║{:^50}║".format("ОБ ИГРЕ"))
    print("╚" + "═" * 50 + "╝")
    
    print("\nПодземелья Древних - это roguelike игра в консоли.")
    print("Вы - герой, исследующий многоуровневые подземелья.")
    
    print("\n" + "=" * 50)
    print("ОСОБЕННОСТИ:")
    print("=" * 50)
    print("• Многоуровневые подземелья с процедурной генерацией")
    print("• Система уровней и развития персонажа")
    print("• Разные типы врагов: обычные, элитные, боссы")
    print("• Уникальные механики боссов с фазами боя")
    print("• Система сокровищ и ловушек")
    print("• Стратегические бои с выбором тактики")
    
    print("\n" + "=" * 50)
    print("УПРАВЛЕНИЕ:")
    print("=" * 50)
    print("W/A/S/D - движение")
    print("I - открыть инвентарь")
    print("H - пожертвовать 10 HP для увеличения силы")
    print("Q - выход из игры")
    
    print("\n" + "=" * 50)
    print("ЦЕЛЬ ИГРЫ:")
    print("=" * 50)
    print("Пройти как можно больше уровней подземелья.")
    print("Каждый 3-й уровень - босс с уникальными способностями.")
    print("Развивайте персонажа, находите сокровища и побеждайте врагов!")
    
    input("\nНажмите Enter, чтобы вернуться в меню...")


def choose_difficulty():
    """Выбор сложности игры"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("╔" + "═" * 50 + "╗")
    print("║{:^50}║".format("ВЫБОР СЛОЖНОСТИ"))
    print("╚" + "═" * 50 + "╝")
    
    print("\nВыберите сложность игры:")
    print("=" * 50)
    print("1. НОВИЧОК")
    print("   • Враги слабее на 20%")
    print("   • +50% к исцелению")
    print("   • Больше сокровищ")
    print("\n2. ВОИН (стандартная)")
    print("   • Баланс силы и сложности")
    print("   • Стандартные награды")
    print("\n3. МАСТЕР")
    print("   • Враги сильнее на 30%")
    print("   • -50% к исцелению")
    print("   • Меньше сокровищ")
    print("   • Чаще появляются элитные враги")
    
    while True:
        try:
            choice = int(input("\nВаш выбор (1-3): "))
            if 1 <= choice <= 3:
                return choice
            else:
                print("Пожалуйста, выберите число от 1 до 3.")
        except ValueError:
            print("Пожалуйста, введите число.")


def main():
    """Основная функция игры"""
    random.seed()
    
    while True:
        menu_choice = main_menu()
        
        if menu_choice == 1:  # Новая игра
            # Выбор сложности
            difficulty = choose_difficulty()
            
            # Создание игрока
            os.system('cls' if os.name == 'nt' else 'clear')
            print("╔" + "═" * 50 + "╗")
            print("║{:^50}║".format("СОЗДАНИЕ ПЕРСОНАЖА"))
            print("╚" + "═" * 50 + "╝")
            
            print("\nВыберите имя героя:")
            for i, name in enumerate(HERO_NAMES, 1):
                print(f"{i}. {name}")
            print(f"{len(HERO_NAMES) + 1}. Ввести своё имя")
            
            try:
                name_choice = int(input("\nВаш выбор: "))
                if 1 <= name_choice <= len(HERO_NAMES):
                    player_name = HERO_NAMES[name_choice - 1]
                else:
                    player_name = input("Введите имя героя: ").strip()
                    if not player_name:
                        player_name = random.choice(HERO_NAMES)
            except:
                player_name = random.choice(HERO_NAMES)
            
            # Настройки сложности
            if difficulty == 1:  # Новичок
                hp_mult = 1.2
                enemy_mult = 0.8
                heal_mult = 1.5
                treasure_mult = 1.5
            elif difficulty == 2:  # Воин
                hp_mult = 1.0
                enemy_mult = 1.0
                heal_mult = 1.0
                treasure_mult = 1.0
            else:  # Мастер
                hp_mult = 0.9
                enemy_mult = 1.3
                heal_mult = 0.5
                treasure_mult = 0.7
            
            # Создание игрока
            player = Hero(
                name=player_name,
                x=0, y=0,
                symbol='@',
                hp=int(100 * hp_mult),
                strength=10,
                armor=5
            )
            
            player.difficulty = difficulty
            player.difficulty_multipliers = {
                "enemy": enemy_mult,
                "heal": heal_mult,
                "treasure": treasure_mult
            }
            
            print(f"\nДобро пожаловать, {player_name}!")
            print("Ваша цель - пройти как можно больше уровней подземелья.")
            print("Каждый 3-й уровень содержит босса с уникальными способностями.")
            print("\nУправление: WASD - движение, I - инвентарь, H - жертвование, Q - выход")
            input("\nНажмите Enter, чтобы начать...")
            
            # Игровой цикл с уровнями
            current_level = 1
            max_levels = 15
            
            while player.is_alive and current_level <= max_levels:
                # Создание карты текущего уровня
                game_map = GameMap(level=current_level, difficulty=difficulty)
                start_room = game_map.rooms[0]
                player.x = start_room.center_x
                player.y = start_room.center_y
                
                # Лечение между уровнями
                heal_amount = int(30 * player.difficulty_multipliers["heal"])
                player.heal(heal_amount)
                
                # Сообщение о начале уровня
                os.system('cls' if os.name == 'nt' else 'clear')
                print("╔" + "═" * 50 + "╗")
                print(f"║{'УРОВЕНЬ':^20} {current_level:^28} ║")
                print("╚" + "═" * 50 + "╝")
                
                if current_level % 3 == 0:
                    print(f"\n⚠️  ВНИМАНИЕ! На этом уровне вас ждет БОСС!")
                    print(f"   Приготовьтесь к тяжелой битве!")
                
                print(f"\nВы восстановили {heal_amount} HP.")
                input("\nНажмите Enter, чтобы войти в подземелье...")
                
                # Цикл уровня
                level_completed = False
                escaped = False
                
                while player.is_alive and not level_completed and not escaped:
                    # Отрисовка карты
                    game_map.draw(player)
                    
                    # Проверка победы
                    alive_enemies = [e for e in game_map.enemies if e.is_alive]
                    boss_alive = game_map.boss and game_map.boss.is_alive
                    
                    if not alive_enemies and not boss_alive:
                        level_completed = True
                        print(f"\n{'⭐' * 25}")
                        print(f"УРОВЕНЬ {current_level} ОЧИЩЕН!")
                        print(f"{'⭐' * 25}")
                        
                        # Награда за уровень
                        level_reward_exp = 50 * current_level
                        player.gain_exp(level_reward_exp)
                        print(f"Получено опыта: {level_reward_exp}")
                        
                        if current_level == max_levels:
                            print(f"\n🎉 ПОБЕДА! Вы прошли все {max_levels} уровней!")
                            print("Вы - настоящий герой подземелий!")
                            input("\nНажмите Enter, чтобы продолжить...")
                            break
                        else:
                            input("\nНажмите Enter для перехода на следующий уровень...")
                            current_level += 1
                            break
                    
                    # Ввод команды
                    print("\nКоманды: WASD-движение, I-инвентарь, H-жертвование, Q-выход")
                    command = input("Ваш ход: ").lower()
                    
                    if command == 'q':
                        print("\nВыход из игры...")
                        escaped = True
                        break
                    
                    # Инвентарь
                    elif command == 'i':
                        show_inventory(player)
                        continue
                    
                    # Жертвование здоровья для силы
                    elif command == 'h':
                        if player.hp > 20:
                            player.hp -= 10
                            player.strength += 2
                            print(f"\n🔥 Вы пожертвовали 10 HP для увеличения силы на 2!")
                            input("Нажмите Enter, чтобы продолжить...")
                        else:
                            print("\nНедостаточно здоровья для жертвоприношения!")
                            input("Нажмите Enter, чтобы продолжить...")
                        continue
                    
                    # Движение
                    new_x, new_y = player.x, player.y
                    
                    if command == 'w':
                        new_y -= 1
                    elif command == 's':
                        new_y += 1
                    elif command == 'a':
                        new_x -= 1
                    elif command == 'd':
                        new_x += 1
                    else:
                        print("\nНеизвестная команда!")
                        input("Нажмите Enter, чтобы продолжить...")
                        continue
                    
                    # Проверка возможности хода
                    if game_map.is_walkable(new_x, new_y):
                        # Проверка на ловушку
                        is_trap, trap_damage = game_map.check_trap(new_x, new_y, player)
                        if is_trap:
                            print(f"\n☠️ Вы наступили на ловушку! Получено {trap_damage} урона!")
                            if not player.is_alive:
                                break
                            input("Нажмите Enter, чтобы продолжить...")
                        
                        # Проверка на врага
                        enemy = game_map.get_enemy_at(new_x, new_y)
                        if enemy:
                            if enemy.is_boss:
                                start_boss_battle(player, enemy)
                            else:
                                escaped_from_battle = start_battle(player, enemy)
                                if escaped_from_battle:
                                    continue
                            
                            if not player.is_alive:
                                break
                        
                        # Проверка на сокровище
                        elif game_map.get_treasure_at(new_x, new_y):
                            result = find_treasure(player)
                            game_map.treasures.remove((new_x, new_y))
                            
                            if result == "teleport":
                                # Телепортация в случайную комнату
                                room = random.choice(game_map.rooms)
                                player.x = random.randint(room.x, room.x + room.w - 1)
                                player.y = random.randint(room.y, room.y + room.h - 1)
                                continue
                        
                        # Перемещение игрока
                        player.x, player.y = new_x, new_y
                    
                    else:
                        print("\nНельзя пройти сквозь стены!")
                        input("Нажмите Enter, чтобы продолжить...")
                
                # Выход из уровня
                if escaped:
                    break
            
            # Конец игры
            os.system('cls' if os.name == 'nt' else 'clear')
            
            if player.is_alive:
                print("╔" + "═" * 50 + "╗")
                print("║{:^50}║".format("ИГРА ЗАВЕРШЕНА"))
                print("║{:^50}║".format("ВЫ ВЫЖИЛИ!"))
                print("╚" + "═" * 50 + "╝")
                
                print(f"\nИтоговые характеристики:")
                print(f"Уровень героя: {player.level}")
                print(f"Достигнутый уровень подземелья: {current_level - 1}")
                print(f"Сила: {player.strength}")
                print(f"Защита: {player.armor}")
                print(f"Максимальное здоровье: {player.max_hp}")
                
                if player.inventory:
                    print(f"\nНайденные легендарные предметы:")
                    for item in player.inventory:
                        print(f"  • {item}")
            
            else:
                print("╔" + "═" * 50 + "╗")
                print("║{:^50}║".format("ВЫ ПАЛИ В БОЮ"))
                print("║{:^50}║".format(f"Уровень: {current_level}"))
                print("╚" + "═" * 50 + "╝")
                
                print(f"\nВаши достижения:")
                print(f"Уровень героя: {player.level}")
                print(f"Пройдено уровней: {current_level - 1}")
            
            input("\nНажмите Enter, чтобы вернуться в главное меню...")
        
        elif menu_choice == 2:  # Загрузить игру
            print("\nФункция загрузки игры находится в разработке.")
            input("Нажмите Enter, чтобы вернуться в меню...")
        
        elif menu_choice == 3:  # Об игре
            about_game()
        
        elif menu_choice == 4:  # Выход
            print("\nСпасибо за игру! До свидания!")
            break


if __name__ == "__main__":
    main()
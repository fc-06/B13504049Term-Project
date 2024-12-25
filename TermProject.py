import pygame
import random
import time

# 初始化 Pygame
pygame.init()

# 顯示設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Survival Island: Resource Management")

# 顏色
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)

# FPS 設定
FPS = 30
clock = pygame.time.Clock()

# 資源設定
food = 100  # 食物
water = 100  # 水
wood = 50  # 木材
stone = 20  # 石頭
health = 50  # 健康狀態
day_count = 0  # 天數
weather = "Clear"  # 天氣狀況
hunger_rate = 3  # 飢餓速率（每個回合減少多少食物）

# 字體設定
font = pygame.font.SysFont("Arial", 24)

# 遊戲結束標誌
game_over = False

# 儲存成績的全局變數
high_scores = []

# 顯示遊戲資源狀態
def display_resources():
    food_text = font.render(f"Food: {food}", True, GREEN)
    water_text = font.render(f"Water: {water}", True, BLUE)
    wood_text = font.render(f"Wood: {wood}", True, BROWN)
    stone_text = font.render(f"Stone: {stone}", True, BLACK)
    health_text = font.render(f"Health: {health}", True, BLACK)
    day_text = font.render(f"Day: {day_count}", True, BLACK)
    weather_text = font.render(f"Weather: {weather}", True, BLACK)

    screen.blit(food_text, (20, 20))
    screen.blit(water_text, (20, 50))
    screen.blit(wood_text, (20, 80))
    screen.blit(stone_text, (20, 110))
    screen.blit(health_text, (20, 140))
    screen.blit(day_text, (SCREEN_WIDTH - 150, 20))
    screen.blit(weather_text, (SCREEN_WIDTH - 150, 50))

# 顯示控制按鍵
def display_controls():
    control_texts = [
        ("A: Collect Food", (SCREEN_WIDTH - 200, 100)),
        ("B: Collect Water", (SCREEN_WIDTH - 200, 130)),
        ("C: Chop Wood", (SCREEN_WIDTH - 200, 160)),
        ("D: Collect Stone", (SCREEN_WIDTH - 200, 190)),
        ("E: Build with Wood", (SCREEN_WIDTH - 200, 220)),
        ("F: Build with Stone", (SCREEN_WIDTH - 200, 250))
    ]
    
    for text, position in control_texts:
        control_text = font.render(text, True, BLACK)
        screen.blit(control_text, position)

# 隨機事件：天氣變化
def change_weather():
    global weather
    events = ["Clear", "Rain", "Storm", "Drought"]
    weather = random.choice(events)

# 影響玩家狀態的事件
def random_event():
    global food, water, health, game_over, event_message
    event_chance = random.randint(1, 100)

    # 隨機事件文字
    event_message = ""

    # 50% 機會觸發隨機事件
    if event_chance <= 50:
        event_type = random.choice(["Hunger", "Thirst", "Injury", "Weather"])
        if event_type == "Hunger":
            food -= 10
            event_message = "You feel hungry and consume food."
            if food <= 0:
                health -= 10
        elif event_type == "Thirst":
            water -= 10
            event_message = "You feel thirsty and consume water."
            if water <= 0:
                health -= 10
        elif event_type == "Injury":
            health -= 20
            event_message = "You get injured and lose health."
        elif event_type == "Weather":
            if weather == "Storm":
                health -= 10
                event_message = "A storm hits, reducing health."
            elif weather == "Drought":
                food -= 15
                water -= 15
                event_message = "A drought occurs, reducing food and water."

        if health <= 0:
            game_over = True

# 顯示隨機事件消息
def display_random_event():
    global event_message
    if event_message:  # 如果有事件發生
        event_text = font.render(event_message, True, BLACK)
        screen.blit(event_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 + 100))  # 顯示事件文本

# 玩家選擇行動
def player_action():
    global food, water, wood, stone, health, day_count, game_over

    # 按鍵處理
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:  # 採集食物
        food += 20
    if keys[pygame.K_b]:  # 採集水
        water += 20
    if keys[pygame.K_c]:  # 砍木材
        wood += 10
    if keys[pygame.K_d]:  # 採集石頭
        stone += 5
    if keys[pygame.K_e]:  # 使用木材建造
        if wood >= 10:
            wood -= 10
            health += 5
    if keys[pygame.K_f]:  # 使用石頭建造
        if stone >= 15:
            stone -= 15
            health += 10

# 更新遊戲狀態
def update_game():
    global food, water, wood, stone, health, day_count, game_over
    food -= hunger_rate
    water -= 3

    random_event()  # 隨機事件
    change_weather()  # 天氣變化

    # 每過一天更新
    day_count += 1
    if food <= 0 or water <= 0 or health <= 0:
        game_over = True

def wait_for_action():
    # 等待玩家按下鍵盤按鍵
    waiting_text = font.render("Press any key to continue to the next round...", True, BLACK)
    screen.blit(waiting_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 + 60))
    pygame.display.update()
    
    # 等待玩家按下鍵盤後繼續遊戲
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # 退出遊戲
            if event.type == pygame.KEYDOWN:
                waiting = False  # 玩家按下鍵盤後繼續
    return True

# 顯示遊戲結束畫面
def game_over_screen():
    screen.fill(WHITE)
    
    # 顯示遊戲結束訊息
    game_over_text = font.render("Game Over! You Failed to Survive.", True, BLACK)
    survival_days_text = font.render(f"Survived for {day_count} days.", True, BLACK)  # 顯示玩家生存天數
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 40))
    screen.blit(survival_days_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))  # 顯示生存天數
    
    pygame.display.update()
    pygame.time.wait(5000)  # 顯示結束畫面 5 秒鐘後退出

# 遊戲主循環
def game_loop():
    global game_over, day_count

    while not game_over:
        screen.fill(WHITE)  # 清空畫面

        # 事件處理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        # 玩家行動
        player_action()

        # 更新遊戲狀態
        update_game()

        # 顯示資源
        display_resources()

        # 顯示控制按鍵
        display_controls()

        # 顯示隨機事件訊息
        display_random_event()  # 顯示隨機事件的文字

        # 顯示遊戲畫面
        pygame.display.update()

        # 等待玩家按下任意鍵才能繼續下一回合
        if not wait_for_action():
            game_over = True  # 如果玩家退出遊戲則結束遊戲

        # 控制遊戲進程
        clock.tick(FPS)

    # 在遊戲結束後顯示玩家生存天數
    game_over_screen()
    
# 開始遊戲
if __name__ == "__main__":
    game_loop()
    pygame.quit()

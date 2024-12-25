# 生存遊戲 Survival Island:Resource Management

## 一、程式的功能

1.	創建遊戲視窗，顯示當前狀態、物資。
2.	小機率隨機事件觸發（飢餓、口渴、受傷、惡劣天氣）。
3.	每回合基礎消耗。
4.	玩家可進行不同的行動來收集資源（例如：採集食物、水、砍木、採石頭）。
5.	玩家可以使用收集的資源進行建造，提高生存機會。
6.	紀錄每次玩家的生存天數。。

## 二、	使用方式

### 1. 環境設定

創建虛擬環境
python -m venv mazeescape-env

啟用虛擬環境
-On Windows:
source mazeescape-env\Scripts\activate
-On macOS/Linux:
source mazeescape-env/bin/activate

安裝pygame、random、time

pip install pygame
pip install random
pip install time

### 2. 開始遊戲

執行程式後會開始新的生存遊戲。
玩家狀態有水、食物及健康，物資有木頭及石頭
每日有50%機率觸發隨機事件
隨機事件有
1. 飢餓:食物-10，若食物不足10，則健康減10
2. 口渴:水-10，若水不足10，則健康減10
3. 受傷:健康-10
4. 天氣:
    暴風雨:健康-10
    乾旱:食物-15，水-15

玩家起始玩家起始健康值:50、水:100、食物:100、木頭:20、石頭:20
每日基礎消耗水-3、食物-3
每回合可選一行動執行(按鍵盤按鍵)
A:增加20食物
B:增加20水
C:增加10木頭
D:增加5木頭
E:若木頭數量大於10，消耗10木頭，增加健康值5
F:若石頭數量大於15，消耗15木頭，增加健康值10

遊戲結束條件:水或食物或健康值<或=0
出現結束畫面並出現結束畫面並顯示玩家生存天數

## 三、	程式的架構
### 1.display_resources()、display_controls()
顯示遊戲介面/遊戲相關資訊
### 2.change_weather()、random_event()、display_random_event()
隨機事件的產生及影響/隨機天氣/在遊戲畫面中顯示觸發的隨機事件
### 3.player_action()
每回合玩家可選擇一項行動/行動產生的影響
### 4.update_game()
每回合基礎消耗/計算天數/判斷遊戲是否結束
### 5.wait_for_action()
確保每回合都有執行行動
### 6.game_over_screen()
產生結束畫面及成績
### 7. game_loop()
遊戲主程式

## 四、	開發過程

1.因為首次使用pygame因此大架構使用ChatGPT的協助
2.發現程式並非可以每天執行動作，而是像影片般播放，自己產生隨機事件，直至遊戲結束
3.我增加了每回合需要按鍵執行動作才能進入下一回合的程式
def wait_for_action():
    waiting_text = font.render("Press any key to continue to the next round...", True, BLACK)
    screen.blit(waiting_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 + 60))
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                waiting = False
    return True
4.然而數字鍵無法執行動作，不論是右方還是上方的，在遊戲中按了都無反應，換了電腦依然如此，因此我改用字母鍵來執行
def player_action():
    global food, water, wood, stone, health, day_count, game_over

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]: 
        food += 20
    if keys[pygame.K_b]: 
        water += 20
    if keys[pygame.K_c]:  
        wood += 10
    if keys[pygame.K_d]:  
        stone += 5
    if keys[pygame.K_e]:  
        if wood >= 10:
            wood -= 10
            health += 5
    if keys[pygame.K_f]:  
        if stone >= 15:
            stone -= 15
            health += 10

5.在各種測試下調整遊戲難度
6.增加計分功能，並能自動關閉頁面

## 五、	參考資料來源

ChatGPT:https://chatgpt.com/
### 1.主題發想
Q:我想寫一個有一定難度的python程式，有甚麼主題提案
A:以下是一些較有挑戰性的 Python 程式設計主題，這些題目不僅能幫助你提升編程技能，還能涵蓋許多實際的應用場景：
...生存遊戲...
### 2.如何使用pygame顯示遊戲介面
### 3.如何使用鍵盤參與遊戲
### 4.如何持續更新介面

## 六、	程式修改或增強的內容

### 1.計算遊戲成績(生存天數):增加計算生天數並在遊戲介面上實時顯示，遊戲結束後也會顯示該局玩家生存天數
### 2.增加等待玩家按按鍵後在繼續執行程式功能:這樣能確保玩家有在每回合執行動作並且有充足時間
### 3.改用字母鍵代替數字鍵:以數字鍵控制執行行為時會無法進行，因此改用字母鍵
### 4.修改遊戲難度:多次嘗試後，將各項數值調為合適的範圍
### 5.在遊戲介面上顯示觸發的隨機事件及按鍵代表含意:讓玩家更清楚遊戲狀態
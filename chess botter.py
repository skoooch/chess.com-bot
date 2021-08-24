

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from stockfish import Stockfish
stock = Stockfish('extras/stockfish_13_win_x64.exe')
PATH = "extras/chromedriver.exe"
from selenium.common.exceptions import TimeoutException
driver = webdriver.Chrome(PATH)
t = time.time()
driver.set_page_load_timeout(10)

try:
	driver.get('https://www.chess.com/play/online/new')
except TimeoutException:
    driver.execute_script("window.stop();")
print('Time consuming:', time.time() - t)

player_is_white = True
#//////////////////////////////////////////////
def checkplayertype():
	boardfield = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID,"board-layout-chessboard")))  
	try:
		boardfield = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME,"board.flipped")))
		return False

	except:
		return True
	return
#/////////////////////////////////////////////
def makemove(player_is_white):
	#find the pieces
	time.sleep(1)
	bunchofpieces = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME,"chess-board"))) 
	
	pieces = bunchofpieces.find_elements_by_tag_name("div")
	remove_from_pieces = []
	for piece in pieces:
		firstword = piece.get_attribute("class")[:5]
	
		if firstword != "piece":
			remove_from_pieces.append(piece)
	for i in remove_from_pieces:
		pieces.remove(i)


	#sort the pieces
	bigstupiffatboard = [[" "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "]]
	fen_pieces = [[],[],[],[],[],[],[],[]]
	for i in pieces:
		index = int(i.get_attribute("class")[17]) - 1
		bigstupiffatboard[int(i.get_attribute("class")[17])-1][int(i.get_attribute("class")[16])-1] = i.get_attribute("class").replace(" ",".")
		if len(fen_pieces[index]) != 0:
			placed = False
			for bitc in fen_pieces[index]:
				if int(bitc[16]) < int(i.get_attribute("class")[16]): 
					pass
				else:
					try:
						fen_pieces[index].insert(fen_pieces[index].index(bitc), str(i.get_attribute("class")).replace(" ","."))
						placed = True
						break
					except:
						driver.quit()
			if not placed:
				fen_pieces[index].append(str(i.get_attribute("class")).replace(" ","."))
		else:
			fen_pieces[index].append(str(i.get_attribute("class")).replace(" ","."))

	# create fen
	fen_notation = ""
	for i in fen_pieces:
		row = ""
		space = 0
		lastnum = 1
		if len(i) > 0:
			for p in i:
				currentnum = int(p[16])
				if p[6] == 'w':
					piecetype = p[7].upper()
				else:
					piecetype = p[7]
				difference = currentnum - lastnum
				lastnum = currentnum + 1
				
				if difference > 0:
					row+= str(difference)
					
				row += piecetype
			if lastnum != 9:
				difference = 9 - lastnum
				row += str(difference)
		else:
			row = "8"

		fen_notation = row + "/" + fen_notation

	if player_is_white:
		fen_notation = fen_notation[:-1]
		fen_notation += " w"
	else:
		fen_notation = fen_notation[:-1]
		fen_notation += " b"
	print(fen_notation)
	 #get best move
	stock.set_fen_position(fen_notation)
	stock.set_depth(20)
	move = stock.get_best_move()
	print(move)
	
	files = ['a','b','c','d','e','f','g','h']
	startmove = str(files.index(move[0:1]) + 1) + move[1:2]
	endmove = str(files.index(move[2:3]) + 1) + move[3:4]
	startpp = bigstupiffatboard[int(startmove[1])-1][int(startmove[0])-1]
	end_move_class = "hint.square-" + endmove
	end_move_take = "capture-hint.square-" + endmove
	return startpp, end_move_class, end_move_take


#//////////////////////////////////////////////
def buffer():
	player_turn = False
	poo = True
	while(poo):
		try:
			gameover = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME,"game-over-modal-content")))
			new_game()
		except:
			pass
		print("check dog gang")
		player_turn = True
		player_is_white = checkplayertype()
		if not player_is_white:
			try:
				time.sleep(1)
				clockcheck = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME,"clock-component.clock-black.clock-bottom.clock-live.clock-running.player-clock.clock-player-turn")))
				
			except:
				poop = False
				player_turn = False
			if player_turn:
				startmover, endmover, endtaker = makemove(player_is_white)
				moveclick = WebDriverWait(driver, 10).until(
					EC.presence_of_element_located((By.CLASS_NAME,startmover)))
				moveclick.click()
				try:
					playhint = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME,endmover)))
				except:
					playhint = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,endtaker)))
				action = webdriver.common.action_chains.ActionChains(driver)
				action.move_to_element_with_offset(playhint, 5, 5)
				action.click()
				action.perform()
			
		else:
			try:
				time.sleep(1)
				clockcheck = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME,"clock-component.clock-white.clock-bottom.clock-live.clock-running.player-clock.clock-player-turn")))

			except:
				player_turn = False
				poop = False
			if player_turn:
				startmover, endmover, endtaker = makemove(player_is_white)
				moveclick = WebDriverWait(driver, 10).until(
					EC.presence_of_element_located((By.CLASS_NAME,startmover)))
				moveclick.click()
				try:
					playhint = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME,endmover)))
				except:
					playhint = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,endtaker)))
				action = webdriver.common.action_chains.ActionChains(driver)
				action.move_to_element_with_offset(playhint, 5, 5)
				action.click()
				action.perform()
			player_turn = False
			
#//////////////////////////////////////////////////////


#initiate game
def main(friend):
	guest = False
	try: 
		play = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,"ui_v5-button-component.ui_v5-button-primary.ui_v5-button-large.ui_v5-button-full")))
	except:
		driver.quit()
	play.click()  #click play
	if guest:
		guest = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"guest-button")))   #click guest option
		guest.click()
	else:
		signin =  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,"authentication-intro-login")))
		signin.click()
		name = "ewan.jordan@my.ucdsb.ca"
		password = "poopcock"
		email =  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"username")))
		email.send_keys(name)
		pas = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"password")))
		pas.send_keys(password)
		signinbut =  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"login")))
		signinbut.click()
		if(friend): friendd()
		else:
			playnew =  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"quick-link-new_game")))
			playnew.click()
			new_game()

def friendd():
	try:
		getthatshitoutahere =  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,"icon-font-chess.x")))
		getthatshitoutahere.click()
	except:
		pass
	accept = driver.find_element_by_partial_link_text('Accept')
	accept.click()
	buffer()

	


def new_game():
	time.sleep(3)
	try:
		playpoo =  WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME,"ui_v5-button-component.ui_v5-button-primary.ui_v5-button-large.ui_v5-button-full")))
		playpoo.click()
	except:
		try:
			playplay =  WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME,"live-game-buttons-game-over")))
			poop = playplay.find_elements_by_class_name("ui_v5-button-component.ui_v5-button-basic")
			playplayplay = poop[1]
			playplayplay.click()
			try:
				playplayplay.click()
			except:
				pass
		except:
			try:
				playplay =  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,"daily-game-footer-mainFinishedBtns")))
				poop = playplay.find_elements_by_class_name("ui_v5-button-component.ui_v5-button-basic")
				playplayplay = poop[1]
				playplayplay.click()
				try: 
					playplayplay.click()
				except:
					pass
			except:
				pass
	buffer()

friend = False   #change this accordingly
main(friend)




driver.quit()











# if(checkplayertype()):		
# 	testclick = WebDriverWait(driver, 10).until(
# 		EC.presence_of_element_located((By.CLASS_NAME,"piece.wp.square-62")))
# 	testclick.click()
# 	playhint = WebDriverWait(driver, 10).until(
# 		EC.presence_of_element_located((By.CLASS_NAME,"hint.square-64")))


# 	action = webdriver.common.action_chains.ActionChains(driver)
# 	action.move_to_element_with_offset(playhint, 5, 5)
# 	action.click()
# 	action.perform()
		




# else:
# 	player_turn = False
# 	while not player_turn:
# 		try:
# 			clockcheck = WebDriverWait(driver, 10).until(
# 			EC.presence_of_element_located((By.CLASS_NAME,"clock-component.clock-black.clock-bottom.clock-live.clock-running.player-clock.clock-player-turn")))
# 			player_turn = True
# 		except:
# 			player_turn = False

# 	testclick = WebDriverWait(driver, 10).until(
# 		EC.presence_of_element_located((By.CLASS_NAME,"piece.bp.square-37")))
# 	testclick.click()
# 	playhint = WebDriverWait(driver, 10).until(
# 		EC.presence_of_element_located((By.CLASS_NAME,"hint.square-35")))
	

# 	action = webdriver.common.action_chains.ActionChains(driver)
# 	action.move_to_element_with_offset(playhint, 5, 5)
# 	action.click()
# 	action.perform()


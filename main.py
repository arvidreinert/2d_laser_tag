import sound
from scene import *
from PIL import Image
import console
import random
import sound
import math
import console
import time 

class Main (Scene):
	def setup(self): 
		self.score = 0
		self.playerlife = 1
		self.player_seen = [False,False]
		self.enemy_move = [False,(),50,0,False]
		self.enemy_bullet = [False]
		self.reloadingframes = [0, False]
		self.amo = 20
		#shooting, how much to add(speed), distx, disty
		self.shoot_active = [False,(),0]
		self.setup_done = False
		self.point_update = False
		self.count = 0
		self.map = "f1"
		x = get_screen_size()
		self.ui_objects = {}
		#range, speed, magazine, reloadtime in frames
		self.gun_stats = [100,15,10, 90]
		self.loaded_amo = self.gun_stats[2]
		self.screenx = x[0]
		self.screeny = x[1]
		self.amobar = LabelNode(f"{self.loaded_amo}/{self.amo}", font=('Apple Color Emoji', 20))
		self.amobar.z_position = 100
		self.amobar.position = (self.screenx-150,50)
		self.add_child(self.amobar)
		self.shoot_button = SpriteNode("shp:RoundRect", size = (100,100), position = (self.screenx-150,self.screeny/2-150))
		self.shoot_button.color = '#000000'
		self.shoot_button.z_position = 10
		self.shoot_button.run_action(Action.fade_to(0.2, 0))
		self.add_child(self.shoot_button)
		self.touch_location = False
		self.count = 0
		self.open_world_move = [False,False]
		self.player_color = (float(f"{random.randint(0,1)}.{random.randint(0,9)}"), float(f"0.{random.randint(0,9)}"), float(f"{random.randint(0,1)}.{random.randint(0,9)}"))
		self.step = False
		#only node with anchor point on the bottom left in this script all others are centered this is because i need the same cordinate system as on the screen
		self.background = SpriteNode("IMG_6817.PNG", size = (self.screenx,self.screeny), position = (0,0))
		self.background.anchor_point = (0,0)
		initial_scale = 20
		self.background.scale = initial_scale
		self.add_child(self.background) 
		self.setup_done = False
		self.setup_open_world(1)
		
	def setup_open_world(self,map):
		self.step = "take players open world turn"
		player = SpriteNode("IMG_6813.JPG", size = (50,50), position = (self.screenx/2,self.screeny/2))
		player.z_position = 4
		player.color = self.player_color
		self.add_child(player)
		self.ui_objects["player"] = player
		joystick = SpriteNode("shp:Circle", size = (200,200), position = (200,200))
		joystick.z_position = 1000
		joystick.color = '#000000'
		joystick.anchor_point = (0.5,0.5)
		joystick.run_action(Action.fade_to(0.2, 0))
		self.add_child(joystick)
		joystick_ball = SpriteNode("shp:Circle", size = (50,50), position = (200,200))
		joystick_ball.color = '#0053ff'
		joystick_ball.run_action(Action.fade_to(0.2, 0))
		joystick_ball.z_position = 1000
		self.add_child(joystick_ball)
		self.ui_objects["joystick"] = joystick
		self.ui_objects["joystick_ball"] = joystick_ball
		self.ball_folow = False
		self.point_update = self.background.position
		for i in range(1, 900):
			tree = SpriteNode("IMG_6818.PNG", size = (1500,1500), position = (random.randint(50, self.screenx*20-50),random.randint(6000, 11932)))
			tree.z_position = 5
			self.add_child(tree)
			self.ui_objects[f"tree{i}"] = tree
		for i in range(1, 200):
			rock = SpriteNode("IMG_6819.PNG", size = (1500,1500), position = (random.randint(50, self.screenx*20-50),random.randint(50, self.screeny*20-50)))
			rock.z_position = 1
			self.add_child(rock)
			self.ui_objects[f"the_rock{i}"] = rock
		for i in range(1, 50):
			chest = SpriteNode("IMG_6820.PNG", size = (1000,1000), position = (random.randint(50, self.screenx*20-50),random.randint(50, self.screeny*20-50)))
			chest.z_position = 1
			self.add_child(chest)
			self.ui_objects[f"chest{i}"] = chest
		for i in range(1, 100):
			enemy_color = (float(f"{random.randint(0,1)}.{random.randint(0,9)}"), float(f"0.{random.randint(0,9)}"), float(f"{random.randint(0,1)}.{random.randint(0,9)}"))
			enemy = SpriteNode("IMG_6813.JPG", size = (50,50), position = (random.randint(50, self.screenx*20-50),random.randint(50, self.screeny*20-50)))
			enemy.z_position = 4
			enemy.color = enemy_color
			self.add_child(enemy)
			self.ui_objects[f"enemy{i}"] = enemy
		self.setup_done = True
		
		
	def touch_began(self,touch): 
		self.ball_folow = False
		location = touch.location
		xdist = location[0]-self.ui_objects["joystick"].position[0]
		ydist = location[1]-self.ui_objects["joystick"].position[1]
		dist = math.sqrt(xdist*xdist+ydist*ydist)
		
		if dist <= 120:
			self.touch_location = location
			self.ui_objects["joystick_ball"].run_action(Action.fade_to(0.2, 0.5))
			self.ui_objects["joystick"].run_action(Action.fade_to(0.2, 0.5))
			self.ball_folow = True
		else:
			self.ball_folow = False
		if self.ball_folow == True:
			self.ui_objects["joystick_ball"].position = location
		#shoot:
		if self.shoot_active[0] == False:
			xdist = location[0]-self.shoot_button.position[0]
			ydist = location[1]-self.shoot_button.position[1]
			dist = math.sqrt(xdist*xdist+ydist*ydist)
			if dist <= 90 and self.loaded_amo >= 0 and self.reloadingframes[1] != True and self.loaded_amo != 0:
				x = self.ui_objects["joystick"].position[0]-self.ui_objects["joystick_ball"].position[0]
				y = self.ui_objects["joystick"].position[1]-self.ui_objects["joystick_ball"].position[1]
				distd = math.sqrt(x*x+y*y)
				x = x/distd
				y = y/distd
				x*=self.gun_stats[1]
				y*= self.gun_stats[1]
				print(x,y,"player")
				sound.play_effect("gun-shot-1-176892.mp3")
				self.loaded_amo -= 1
				self.shoot_active = [True,(x,y),self.gun_stats[0]+distd]
				bullet = SpriteNode("IMG_6822.PNG", size = (100,100), position = (self.screenx/2,self.screeny/2))
				bullet.z_position = 3
				bullet.rotation = self.ui_objects["player"].rotation
				self.add_child(bullet)
				self.ui_objects["bullet"] = bullet
			if self.loaded_amo == 0:
				self.reloadingframes[1] = True
				sound.play_effect("mag-reload-81594.mp3")
		
	def touch_moved(self,touch):
		self.ball_folow = False
		location = touch.location
		xdist = location[0]-self.ui_objects["joystick"].position[0]
		ydist = location[1]-self.ui_objects["joystick"].position[1]
		dist = math.sqrt(xdist*xdist+ydist*ydist)
		
		if dist <= 115:
			self.touch_location = location
			self.ball_folow = True
		else:
			self.ball_folow = False
			
		if self.ball_folow == True:
			self.ui_objects["joystick_ball"].position = location
			
	def touch_ended(self,touch):
		location = touch.location
		xdist = location[0]-self.ui_objects["joystick"].position[0]
		ydist = location[1]-self.ui_objects["joystick"].position[1]
		dist = math.sqrt(xdist*xdist+ydist*ydist)
		
		if dist <= 115:
			self.touch_location = False
			self.ui_objects["joystick_ball"].run_action(Action.fade_to(0, 0.5))
			self.ui_objects["joystick"].run_action(Action.fade_to(0, 0.5))
		
	def update(self):
		#enemy:
		if self.player_seen[0]:
			if self.enemy_bullet[0] == False:
				if random.randint(1,100-self.score) == 1:
					#enemy attack enemy: self.ui_objects[self.player_seen[1]].position[0]
					print("pau")
					if self.player_seen[1] != False:
						x = self.ui_objects[self.player_seen[1]].position[0]-self.ui_objects["player"].position[0]
						y = self.ui_objects[self.player_seen[1]].position[1]-self.ui_objects["player"].position[1]
						dist = math.sqrt(x*x+y*y)
						s = self.score+10
						x = x/dist
						x = x*s
						y = y/dist
						y = y*s
						sound.play_effect("gun-shot-1-176892.mp3")
						self.enemy_bullet = [True,(x,y),90+self.score+dist]
						bullet = SpriteNode("IMG_6822.PNG", size = (100,100), position = self.ui_objects[self.player_seen[1]].position)
						print(x,y,"enemy")
						bullet.z_position = 3
						x0, y0 = self.ui_objects[self.player_seen[1]].position
						x1, y1 = self.ui_objects["player"].position
						bullet.rotation = math.atan2(y1 - y0, x1 - x0) - (math.pi / 2)
						self.add_child(bullet)
						self.ui_objects["bulletenemy"] = bullet
			if self.enemy_move[0] == False:
				self.enemy_move[1] = (random.randint(-400,400),random.randint(-400,400))
				self.enemy_move[0] = True
				self.enemy_move[2] = random.randint(200,300)
				self.enemy_move[3] = 0
			else:
				if self.enemy_move[3] <= self.enemy_move[2]:
					self.ui_objects[self.player_seen[1]].position = (self.ui_objects[self.player_seen[1]].position[0]+self.enemy_move[1][0]*0.01,
					self.ui_objects[self.player_seen[1]].position[1]+self.enemy_move[1][1]*0.01)
					self.enemy_move[3] += 1
				else:
					if self.enemy_move[4] != True:
						print("try reset")
						self.enemy_move[0] = False
				
		self.amobar.text = f"{self.loaded_amo}/{self.amo}"
		if self.reloadingframes[1]:
			self.reloadingframes[0] += 1
		if self.reloadingframes[0] == self.gun_stats[3]:
			self.reloadingframes[0] = 0
			if self.amo-self.gun_stats[2] >= 0 or self.amo-self.gun_stats[2] == 0:
				self.amo -= self.gun_stats[2]
				self.loaded_amo = self.gun_stats[2]
			self.reloadingframes[1] = False
		if self.setup_done:
			self.count += 1
			if self.count == 1:
				x0, y0 = (200, 200)
				x1, y1 = (self.ui_objects["joystick_ball"].position[0],self.ui_objects["joystick_ball"].position[1])
				self.ui_objects["player"].rotation = math.atan2(y1 - y0, x1 - x0) - (math.pi / 2)
				self.count = 0
				if self.touch_location != False:
					xdist = self.touch_location[0]-self.ui_objects["joystick"].position[0]
					ydist = self.touch_location[1]-self.ui_objects["joystick"].position[1]
					dist = math.sqrt(xdist*xdist+ydist*ydist)
					if dist <= 0:
						dist = dist*-1
					self.background.position = (self.background.position[0]+xdist/20*-1,
					self.background.position[1]+ydist/20*-1)
					for object in self.ui_objects:
						if "tree" in object:
							self.ui_objects[object].position = (self.ui_objects[object].position[0]+xdist/20*-1,
						self.ui_objects[object].position[1]+ydist/20*-1)
						if "rock" in object:
							self.ui_objects[object].position = (self.ui_objects[object].position[0]+xdist/20*-1,
						self.ui_objects[object].position[1]+ydist/20*-1)
						if "chest" in object:
							self.ui_objects[object].position = (self.ui_objects[object].position[0]+xdist/20*-1,
						self.ui_objects[object].position[1]+ydist/20*-1)
						if "enemy" in object:
							if self.player_seen[0] != True:
								exdist = self.ui_objects["player"].position[0]-self.ui_objects[object].position[0]
								eydist = self.ui_objects["player"].position[1]-self.ui_objects[object].position[1]
								edist = math.sqrt(exdist*exdist+eydist*eydist)
								if edist <= 0:
									edist = edist*-1
								if edist <= self.screeny*0.5:
									print("enemy spotetd")
									self.player_seen = [True,object]
							self.ui_objects[object].position = (self.ui_objects[object].position[0]+xdist/20*-1,
						self.ui_objects[object].position[1]+ydist/20*-1)
						#bullets nachführen(movement verschiebt sie)
					if self.shoot_active[0] == True:
						self.ui_objects["bullet"].position = (self.ui_objects[object].position[0]+xdist/20*-1,
						self.ui_objects[object].position[1]+ydist/20*-1)
					
						
				# players shoot here
				if self.shoot_active[0]:
					if self.shoot_active[2] >= 0:
						self.shoot_active[2] -= 1
						self.ui_objects["bullet"].position = (self.ui_objects["bullet"].position[0]+self.shoot_active[1][0]*-1,
						self.ui_objects["bullet"].position[1]+self.shoot_active[1][1]*-1)
						if self.player_seen[0]:
							xdist = self.ui_objects[self.player_seen[1]].position[0]-self.ui_objects["bullet"].position[0]
							ydist = self.ui_objects[self.player_seen[1]].position[1]-self.ui_objects["bullet"].position[1]
							dist = math.sqrt(xdist*xdist+ydist*ydist)
							if dist <= 0:
								dist = dist*-1
							if dist <= 50:
								self.score += 1
								print("enemy_killed")
								self.ui_objects[self.player_seen[1]].remove_from_parent()
								self.enemy_move = [False,(),50,0,False]
								self.enemy_bullet = [False]
								enemy_color = (float(f"{random.randint(0,1)}.{random.randint(0,9)}"), float(f"0.{random.randint(0,9)}"), float(f"{random.randint(0,1)}.{random.randint(0,9)}"))
								enemy = SpriteNode("IMG_6813.JPG", size = (50,50), position = (random.randint(50, self.screenx*20-50),random.randint(50, self.screeny*20-50)))
								enemy.z_position = 4
								enemy.color = enemy_color
								self.add_child(enemy)
								self.ui_objects[self.player_seen[1]] = enemy
								self.player_seen = [False,False]
								for object in self.ui_objects:
									if "bullet" in object:
										self.ui_objects[object].remove_from_parent()
								self.shoot_active = [False,(),0]
					else:
						for object in self.ui_objects:
							if "bullet" in object:
								self.ui_objects[object].remove_from_parent()
						self.shoot_active = [False,(),0]
				else:
					self.shoot_active = [False,(),0]
				
				#enemy shoot
				if self.enemy_bullet[0]:
					if self.enemy_bullet[2] >= 0:
						self.enemy_bullet[2] -= 1
						self.ui_objects["bulletenemy"].position = (self.ui_objects["bulletenemy"].position[0]+self.enemy_bullet[1][0]*-1,
						self.ui_objects["bulletenemy"].position[1]+self.enemy_bullet[1][1]*-1)
						xdist = self.ui_objects["player"].position[0]-self.ui_objects["bulletenemy"].position[0]
						ydist = self.ui_objects["player"].position[1]-self.ui_objects["bulletenemy"].position[1]
						dist = math.sqrt(xdist*xdist+ydist*ydist)
						if dist <= 0:
							dist = dist*-1
						if dist <= 50:
							self.playerlife -= 1
							print("player_hit")
							self.enemy_move = [False,(),50,0,False]
							self.enemy_bullet = [False]
							enemy_color = (float(f"{random.randint(0,1)}.{random.randint(0,9)}"), float(f"0.{random.randint(0,9)}"), float(f"{random.randint(0,1)}.{random.randint(0,9)}"))
							enemy = SpriteNode("IMG_6813.JPG", size = (50,50), position = (random.randint(50, self.screenx*20-50),random.randint(50, self.screeny*20-50)))
							enemy.z_position = 4
							enemy.color = enemy_color
							self.add_child(enemy)
							self.ui_objects[self.player_seen[1]] = enemy
							self.player_seen = [False,False]
							for object in self.ui_objects:
								if "bulletenemy" in object:
									print("bullet del")
									self.ui_objects[object].remove_from_parent()
							self.enemy_bullet = [False]
					else:
						for object in self.ui_objects:
							if "bulletenemy" in object:
								self.ui_objects[object].remove_from_parent()
						self.enemy_bullet = [False]
				else:
					self.enemy_bullet = [False]
					
if __name__ == '__main__':
	run(Main(), PORTRAIT, show_fps=True)

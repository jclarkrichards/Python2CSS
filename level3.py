def reverseDirection(self):
    if self.direction is UP: self.direction = DOWN
    elif self.direction is DOWN: self.direction = UP
    elif self.direction is LEFT: self.direction = RIGHT
    elif self.direction is RIGHT: self.direction = LEFT
    temp = self.node
    self.node = self.target
    self.target = temp




def moveBySelf(self):
    if self.direction is not STOP:
        if self.overshotTarget():
            self.node = self.target
            if self.node.neighbors[self.direction] is not None:
                self.target = self.node.neighbors[self.direction]
            else:
                self.setPosition()
                self.direction = STOP


def update(self, dt):
    self.position += self.direction*self.speed*dt
    direction = self.getValidKey()
    if direction:
        self.moveByKey(direction)
    else:
        self.moveBySelf()
    "Change the below to strikeout"
    if self.overshotTarget():
        self.node = self.target
        self.setPosition()
        self.direction = STOP


def moveByKey(self, direction):
    if self.direction is STOP:
        if self.node.neighbors[direction] is not None:
            self.target = self.node.neighbors[direction]
            self.direction = direction
    else:
        if direction == self.direction * -1:
            self.reverseDirection()
        if self.overshotTarget():
            self.node = self.target
            if self.node.neighbors[direction] is not None:
                self.target = self.node.neighbors[direction]
                if self.direction != direction:
                    self.setPosition()
                    self.direction = direction
            else:
                if self.node.neighbors[self.direction] is not None:
                    self.target = self.node.neighbors[self.direction]
                else:
                    self.setPosition()
                    self.direction = STOP

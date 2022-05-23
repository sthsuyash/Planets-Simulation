import pygame
import math

# initialize the module
pygame.init()

# declare constants width and height for size of window in pixels
WIDTH, HEIGHT = 1000, 790
# setting up window, takes coordinates for window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# setting caption for the window
pygame.display.set_caption("Simulation of Planets")

# rgb value for colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SUN = (253, 184, 19)
MERCURY = (173, 168, 165)
VENUS = (165, 104, 27)
EARTH = (107, 147, 214)
MARS = (69, 24, 4)

# changing the font
FONT = pygame.font.SysFont("comicsans", 16)

# create a class called Planet to make general outline for all the planets
class Planet:
    ''' constants '''
    # astronomical unit
    AU = 149.6e6 * 1000  # *1000 to be in meter from km
    # Gravitational constant for finding force of attraction
    G = 6.67428e-11
    # make appropriate for pygame scale as we cannot fit astronomical length
    SCALE = 250 / AU  # 1AU = 100px
    # how much time to represent in simulation
    TIMESTEP = 3600 * 24  # represents 1 day

    ''' init function '''
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        # tell if the planet is sun, as we want to draw the orbit of planets and not for Sun
        self.sun = False
        # distance from the sun to planets, update for individual later
        self.distance_to_sun = 0
        # represents orbit of the planet
        self.orbit = []

        # to move the planets
        # determined by force of attraction
        self.x_velocity = 0
        self.y_velocity = 0

    ''' implement draw method '''
    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2 
                y = y * self.SCALE + WIDTH / 2 
                updated_points.append((x, y))

            # draw the orbits
            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x, y), self.radius)

    ''' calculate force of attraction '''
    def attraction(self, other):
        # all of these forces and distances are real values scaled to small pixel
        ''' calculated distance between the two objects '''
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        ''' determine if the other object is the sun '''
        if other.sun:
            self.distance_to_sun = distance

        ''' straight line force of attraction '''
        force = self.G * self.mass * other.mass / distance ** 2
        # must break it into x and y component
        # angle of the force we want
        theta = math.atan2(distance_y, distance_x)
        # force in x component
        force_x = math.cos(theta) * force
        # force in y component
        force_y = math.sin(theta) * force

        return force_x, force_y

    ''' update the position according to force and velocity '''
    def update_position(self, planets):
        total_force_in_x = total_force_in_y = 0
        for planet in planets:
            if self == planet:
                continue

            # for every single planet, calculate force x and y exerting on this planet
            force_in_x, force_in_y = self.attraction(planet)
            total_force_in_x += force_in_x
            total_force_in_y += force_in_y

        self.x_velocity += total_force_in_x / self.mass * self.TIMESTEP
        self.y_velocity += total_force_in_y / self.mass * self.TIMESTEP

        self.x += self.x_velocity * self.TIMESTEP
        self.y += self.y_velocity * self.TIMESTEP
        # to draw the orbit
        self.orbit.append((self.x, self.y))

        # F = m / a 
        # a = F / m

# end of class

'''
    create pygame event loop 
    infinite loop which runs until the program ends
    keeps the program running as we don't want the window to close automatically
'''

# main function
def main():
    run = True
    # regulate the frame rate # wont go after certain value
    # synchronize the game
    clock = pygame.time.Clock()

    ''' making the planets '''
    # Sun
    Sun = Planet(0, 0, 30, SUN, 1.98892 * 10**30)
    # Sun.sun = True it must be in center and not have orbit

    # Mercury
    Mercury = Planet(0.387 * Planet.AU, 0, 8, MERCURY, 3.30 * 10**23)
    # km/s * 1000 = m/s
    Mercury.y_velocity = -47.4 * 1000

    # Venus
    Venus = Planet(0.723 * Planet.AU, 0, 14, VENUS, 4.8685 * 10**24)
    Venus.y_velocity = -35.02 * 1000

    # Earth
    Earth = Planet(-1 * Planet.AU, 0, 16, EARTH, 5.9742 * 10**24)
    Earth.y_velocity = 29.783 * 1000

    # Mars
    Mars = Planet(-1.524 * Planet.AU, 0, 12, MARS, 6.39 * 10**23)
    Mars.y_velocity = 24.077 * 1000

    # array to store all the planets
    planets = [Sun, Mercury, Venus, Earth, Mars]

    # run is true until the user clicks close(X) button
    while run:
        # update the loop maximum of 60 times per second to ensure game isn't going too fast
        clock.tick(60)
        # update background color of window
        WIN.fill(BLACK)
        # update the display
        pygame.display.update()

        # gives list of all the different events that occur, e.g. keypress, mouse movement, etc.
        for event in pygame.event.get():
            # only button we want to handle is the close button(X) that user clicks
            if event.type == pygame.QUIT:
                run = False
                # close the window by making run=false

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()

# call the main function
main()

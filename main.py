import pygame
import random
from environment_objects import *
import genetic_algorithm as ga


DISPLAY_SIZE = (1200, 800)
BACKGROUND_COLOR = (184, 222, 111)


NUM_GENERATIONS = 20
TIME_PER_GENERATION = 100000
MUTATION_PROBABILITY = 0.05

NUM_HERBIVORES = 10
NUM_PLANTS = 5


if __name__ == '__main__':

    pygame.init()
    pygame.display.set_caption("Hunger Games: Herbivores")
    screen = pygame.display.set_mode(DISPLAY_SIZE)

    plants = [Plant.initiate_at_random(DISPLAY_SIZE) for _ in range(NUM_PLANTS)]
    herbivores = [Herbivore.initiate_at_random(DISPLAY_SIZE, plants) for _ in range(NUM_PLANTS)]

    for i in range(NUM_GENERATIONS):

        for ii in range(TIME_PER_GENERATION):

            # Replant plants if some have been eaten.
            plants_updated = False
            for _ in range(NUM_PLANTS - len(plants)):
                plants_updated = True
                plants.append(Plant.initiate_at_random(DISPLAY_SIZE))

            for herbivore in herbivores:
                if plants_updated or i == 0:
                    herbivore.lock_target()

                if not herbivore.isDead:
                    if herbivore.hunger <= 0:
                        herbivore.isDead = True
                        print("poor herbivore died :(")

                    if not herbivore.isDead:
                        herbivore.lifetime += 1
                        herbivore.update_sensed_plants(plants)
                        herbivore.update_moving_direction()
                        if not herbivore.is_turning:
                            herbivore.move()
                            herbivore.eat()




            # DRAW EVERYTHING
            screen.fill(BACKGROUND_COLOR)

            for herbivore in herbivores:
                if not herbivore.isDead:
                    herbivore.show(screen)

            for plant in plants:
                plant.show(screen)

            pygame.display.update()

        # EVOLVE NEW GENERATION
        offspring_population = []

        while len(offspring_population) < len(herbivores):

            parent_a = ga.fitness_proportionate_selection(herbivores)
            parent_b = ga.fitness_proportionate_selection(herbivores)

            offspring = ga.reproduce(parent_a, parent_b)
            if random.random() < MUTATION_PROBABILITY:
                offspring = ga.mutate(offspring)

            offspring_population.append(offspring)

        population = offspring_population






